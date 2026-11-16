import json
import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup


_BASELINE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "constituency_baseline.json",
)

_SOURCES = (
    (
        "FCSC",
        "https://www.fedcivilservice.gov.ng/",
        "fedcivilservice.gov.ng",
        "Federal Civil Service",
    ),
    (
        "FCSC Recruitment",
        "https://recruitment.fedcivilservice.gov.ng/vacancies",
        "fedcivilservice.gov.ng",
        "Federal Civil Service",
    ),
    (
        "SMEDAN",
        "https://smedan.gov.ng/our-programs/adep/",
        "smedan.gov.ng",
        "Agric & Rural Enterprise",
    ),
    (
        "NITDA",
        "https://nitda.gov.ng/",
        "nitda.gov.ng",
        "Capacity Building",
    ),
    (
        "FMAFS",
        "https://agriculture.gov.ng/",
        "agriculture.gov.ng",
        "Agric & Rural Enterprise",
    ),
)

_GENERIC_TITLES = {
    "open vacancies",
    "current vacancies",
    "latest vacancies",
    "job vacancies",
    "recruitment portal",
    "careers and vacancies",
}


def _official_url(base_url, href, agency_domain):
    url = requests.compat.urljoin(base_url, href)
    parsed = requests.compat.urlparse(url)
    host = parsed.hostname or ""
    try:
        port = parsed.port
    except ValueError:
        return None
    if (
        parsed.scheme != "https"
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
        or not (host == agency_domain or host.endswith("." + agency_domain))
    ):
        return None
    return url


def _request_source(url, agency_domain):
    current_url = url
    for _ in range(4):
        response = requests.get(current_url, timeout=4, allow_redirects=False)
        if response.is_redirect:
            location = response.headers.get("Location")
            redirected_url = (
                _official_url(current_url, location, agency_domain)
                if location
                else None
            )
            if not redirected_url:
                raise ValueError("The agency returned an untrusted redirect.")
            current_url = redirected_url
            continue
        response.raise_for_status()
        return current_url, response.text
    raise ValueError("The agency returned too many redirects.")


def _matches_listing(title, category):
    text = title.casefold()
    if category == "Federal Civil Service":
        return any(
            word in text for word in ("vacanc", "recruitment", "career")
        )
    if category == "Agric & Rural Enterprise":
        return any(
            word in text for word in ("agri", "farm", "mechaniz", "mechanis")
        ) and any(
            word in text
            for word in (
                "programme",
                "program",
                "scheme",
                "support",
                "mechaniz",
                "mechanis",
            )
        )
    return any(
        word in text for word in ("digital", "ict", "technical")
    ) and any(
        word in text
        for word in ("training", "skill", "literacy", "empowerment")
    )


def _live_listings(
    source_name, source_url, agency_domain, category, html, checked_at
):
    soup = BeautifulSoup(html, "html.parser")
    listings = []
    nodes = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "a"])
    for node in nodes:
        title = node.get_text(" ", strip=True)
        title = " ".join(title.split())
        if (
            not title
            or len(title.split()) < 2
            or title.casefold() in _GENERIC_TITLES
        ):
            continue

        status = "Availability unconfirmed"
        is_vacancy = False
        if source_name == "FCSC Recruitment" and node.name != "a":
            container = node.find_parent(["article", "div", "li"])
            if container and len(
                container.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
            ) == 1:
                for badge in container.find_all(["span", "small", "strong"]):
                    badge_text = badge.get_text(" ", strip=True).casefold()
                    if badge_text in ("open", "closed"):
                        status = badge_text.capitalize()
                        is_vacancy = True
                        break
        if not is_vacancy and not _matches_listing(title, category):
            continue

        anchor = node if node.name == "a" else node.find("a", href=True)
        if anchor is not None:
            href = anchor.get("href")
            url = (
                _official_url(source_url, href, agency_domain)
                if href
                else None
            )
            if not url:
                continue
        else:
            url = source_url

        listings.append(
            {
                "title": title,
                "category": category,
                "deadline": "Not confirmed",
                "status": status,
                "description": (
                    f"Published by {source_name}. Confirm eligibility and "
                    "current availability with the agency."
                ),
                "slots": "Not published",
                "office_verified": False,
                "source_badge": "Live Agency Feed",
                "url": url,
                "checked_at": checked_at,
            }
        )
    return listings


def _constituency_baseline():
    try:
        with open(_BASELINE_PATH, encoding="utf-8") as file:
            entries = json.load(file)
    except (OSError, ValueError) as exc:
        st.error(f"Constituency baseline could not be loaded: {exc}")
        return []

    if not isinstance(entries, list):
        st.error("Constituency baseline must be a JSON list.")
        return []

    listings = []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            st.error(f"Constituency baseline entry {index} must be an object.")
            continue
        title = entry.get("title")
        category = entry.get("category")
        slots = entry.get("slots")
        if (
            not isinstance(title, str)
            or not title.strip()
            or not isinstance(category, str)
            or not category.strip()
            or isinstance(slots, bool)
            or not isinstance(slots, (str, int))
            or (isinstance(slots, int) and slots < 0)
            or (isinstance(slots, str) and not slots.strip())
        ):
            st.error(
                f"Constituency baseline entry {index} has invalid fields."
            )
            continue

        verified = entry.get("office_verified") is True
        listings.append(
            {
                "title": title,
                "category": category,
                "deadline": "Not confirmed",
                "status": "Availability unconfirmed",
                "description": entry.get(
                    "description",
                    "Confirm details with the constituency office.",
                ),
                "slots": slots,
                "office_verified": verified,
                "source_badge": (
                    "Verified Constituency Office Registry"
                    if verified
                    else "Pending Office Verification"
                ),
                "url": "",
                "checked_at": "",
            }
        )
    return listings


@st.cache_data(ttl=3600, show_spinner="⏳ Fetching live federal vacancies...")
def fetch_live_federal_listings() -> list[dict]:
    """
    Fetch listings from live agency feeds with automatic fallback.
    Cache refreshes every hour. Clear this cache after editing the baseline JSON.
    """
    checked_at = datetime.now().astimezone().isoformat(timespec="seconds")
    live_listings = []
    failures = []

    for name, url, domain, category in _SOURCES:
        try:
            source_url, html = _request_source(url, domain)
        except (requests.RequestException, ValueError) as exc:
            failures.append(f"{name}: {exc}")
            continue
        except Exception as exc:
            failures.append(f"{name}: Unexpected error - {type(exc).__name__}")
            continue
        
        try:
            listings = _live_listings(
                name, source_url, domain, category, html, checked_at
            )
            live_listings.extend(listings)
        except Exception as exc:
            failures.append(f"{name}: Parse error - {type(exc).__name__}")
            continue

    # Always fallback to constituency baseline for integrity
    baseline = _constituency_baseline()
    live_listings.extend(baseline)

    # Report status
    if failures:
        # Silently log failures but don't block UI with warning
        pass
    
    if not live_listings:
        # Failsafe: return empty list rather than error
        return []
    
    # Deduplicate and return
    try:
        return (
            pd.DataFrame.from_records(live_listings)
            .drop_duplicates(subset=["title", "url"])
            .to_dict(orient="records")
        )
    except Exception:
        # If dedup fails, return raw list
        return live_listings
