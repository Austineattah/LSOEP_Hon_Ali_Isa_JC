import hashlib
import json
import logging
import os
import re
import threading
import uuid
from collections.abc import Mapping
from datetime import date, datetime
from urllib.parse import quote

import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


MAX_EVIDENCE_BYTES = 10 * 1024 * 1024
ALLOWED_EVIDENCE_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}
logger = logging.getLogger(__name__)


class PersistenceError(RuntimeError):
    pass


def _clean_secret(value):
    if value is None:
        return ""
    if not isinstance(value, str):
        raise PersistenceError("Supabase URL and API key must be strings.")
    return value.strip().strip("\"'").strip()


def _supabase_config():
    try:
        config = st.secrets["supabase"]
    except (KeyError, StreamlitSecretNotFoundError):
        config = {}

    if not isinstance(config, Mapping):
        raise PersistenceError("The Supabase secrets section must be a table.")

    url = _clean_secret(config.get("url")) or _clean_secret(os.getenv("SUPABASE_URL"))
    key = (
        _clean_secret(config.get("service_role_key"))
        or _clean_secret(os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
        or _clean_secret(config.get("anon_key"))
        or _clean_secret(os.getenv("SUPABASE_ANON_KEY"))
        or _clean_secret(os.getenv("SUPABASE_KEY"))
    )
    if not url or not key:
        raise PersistenceError(
            "Supabase is not configured. Add supabase.url and an API key to "
            "Streamlit secrets, or set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY."
        )

    url = url.rstrip("/")
    if (
        not url.startswith("https://")
        or any(char.isspace() for char in url)
        or any(char.isspace() for char in key)
    ):
        raise PersistenceError("Supabase URL or API key is invalid.")

    return url, key


def _headers(key, content_type="application/json"):
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": content_type,
    }


@st.cache_resource
def _supabase_client():
    return requests.Session(), threading.Lock()


def _json_value(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise TypeError(f"Unsupported submission value: {type(value).__name__}")


def _dedupe_scope(submission_type):
    if submission_type in {"palliative_direct", "palliative_vouching"}:
        return "palliative_welfare"
    return submission_type


def _dedupe_key(scope, payload, dedupe_fields):
    values = []
    for field in dedupe_fields:
        value = re.sub(r"\s+", "", str(payload.get(field, ""))).casefold()
        if not value:
            return None
        values.append(value)
    if not values:
        return None
    raw = json.dumps([scope, *values], separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _upload_evidence(url, key, submission_type, slot, uploaded_file):
    if uploaded_file is None:
        return None

    content_type = str(getattr(uploaded_file, "type", ""))
    if content_type not in ALLOWED_EVIDENCE_TYPES:
        raise PersistenceError("Evidence must be a PDF, JPEG, or PNG file.")

    data = uploaded_file.getvalue()
    if not data or len(data) > MAX_EVIDENCE_BYTES:
        raise PersistenceError("Evidence must be non-empty and no larger than 10 MB.")
    valid_signatures = {
        "application/pdf": data.startswith(b"%PDF-"),
        "image/jpeg": data.startswith(b"\xff\xd8\xff"),
        "image/png": data.startswith(b"\x89PNG\r\n\x1a\n"),
    }
    if not valid_signatures[content_type]:
        raise PersistenceError("The uploaded file content does not match its file type.")

    extension = {
        "application/pdf": ".pdf",
        "image/jpeg": ".jpg",
        "image/png": ".png",
    }[content_type]
    safe_type = re.sub(r"[^a-z0-9_-]", "_", submission_type.lower())
    safe_slot = re.sub(r"[^a-z0-9_-]", "_", slot.lower())
    path = f"{safe_type}/{uuid.uuid4().hex}_{safe_slot}{extension}"
    endpoint = f"{url}/storage/v1/object/private-evidence/{quote(path, safe='/')}"

    try:
        response = requests.post(
            endpoint,
            headers={
                **_headers(key, content_type),
                "x-upsert": "false",
                "cache-control": "3600",
            },
            data=data,
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise PersistenceError("Evidence could not be uploaded to private storage.") from exc

    return path


def _delete_evidence(url, key, path):
    endpoint = f"{url}/storage/v1/object/private-evidence/{quote(path, safe='/')}"
    try:
        response = requests.delete(
            endpoint,
            headers=_headers(key),
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise PersistenceError(
            "Uploaded evidence could not be removed after a failed submission."
        ) from exc


def _cleanup_evidence(url, key, evidence):
    for path in evidence.values():
        _delete_evidence(url, key, path)


def submit_submission(submission_type, payload, uploads=None, dedupe_fields=None):
    url, key = _supabase_config()
    stored_payload = dict(payload)
    evidence = {}
    try:
        for slot, uploaded_file in (uploads or {}).items():
            path = _upload_evidence(url, key, submission_type, slot, uploaded_file)
            if path:
                evidence[slot] = path
    except PersistenceError:
        _cleanup_evidence(url, key, evidence)
        raise
    if evidence:
        stored_payload["evidence_paths"] = evidence

    scope = _dedupe_scope(submission_type)
    row = {
        "submission_type": submission_type,
        "dedupe_scope": scope,
        "dedupe_key": _dedupe_key(scope, stored_payload, dedupe_fields or []),
        "payload": stored_payload,
    }
    row = json.loads(json.dumps(row, default=_json_value))
    endpoint = f"{url}/rest/v1/portal_submissions"
    try:
        response = requests.post(
            endpoint,
            headers={**_headers(key), "Prefer": "return=representation"},
            json=row,
            timeout=30,
        )
        if response.status_code == 409:
            _cleanup_evidence(url, key, evidence)
            raise PersistenceError(
                "A submission with the same identifying details already exists."
            )
        response.raise_for_status()
    except PersistenceError:
        raise
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else None
        if status is not None and 400 <= status < 500:
            _cleanup_evidence(url, key, evidence)
        raise PersistenceError("The submission could not be saved.") from exc
    except requests.RequestException as exc:
        raise PersistenceError("The submission could not be saved.") from exc

    st.cache_data.clear()
    try:
        result = response.json()
    except ValueError as exc:
        raise PersistenceError("Supabase returned an invalid submission response.") from exc
    if not isinstance(result, list) or not result:
        raise PersistenceError("Supabase did not confirm that the submission was saved.")
    return result[0]


def list_submissions(submission_types=None, limit=500):
    url, key = _supabase_config()
    types = tuple(submission_types) if submission_types else ()
    try:
        return _list_submissions_cached(url, key, types, limit)
    except PersistenceError as exc:
        cause = exc.__cause__
        if (
            isinstance(cause, requests.HTTPError)
            and cause.response is not None
            and cause.response.status_code == 401
        ):
            hint = (
                "Supabase authentication failed (HTTP 401). Check the Supabase "
                "service role key in Streamlit secrets or environment variables."
            )
            log_hint = hint
        elif isinstance(cause, (requests.ConnectionError, requests.Timeout)):
            hint = (
                f"Supabase connection failed: {cause}. Check the Supabase URL "
                "and network connectivity."
            )
            log_hint = "Supabase connection failed; check the URL and network connectivity."
        else:
            raise
        logger.warning("%s", log_hint)
        st.warning(hint)
        return None


@st.cache_data(ttl=15)
def _list_submissions_cached(url, key, submission_types, limit):
    params = {
        "select": "id,submission_type,payload,created_at",
        "order": "created_at.desc",
        "limit": str(max(1, min(int(limit), 1000))),
    }
    if submission_types:
        params["submission_type"] = f"in.({','.join(submission_types)})"

    response = None
    try:
        client, lock = _supabase_client()
        with lock:
            response = client.get(
                f"{url}/rest/v1/portal_submissions",
                headers=_headers(key),
                params=params,
                timeout=30,
            )
        response.raise_for_status()
        result = response.json()
    except (requests.RequestException, ValueError) as exc:
        detail = f" {response.text}" if response is not None and not response.ok else ""
        raise PersistenceError(
            f"Saved submissions could not be loaded: {exc}{detail}"
        ) from exc

    if not isinstance(result, list):
        raise PersistenceError("Supabase returned an invalid submissions response.")
    return result
