import time
import hmac

import streamlit as st
from streamlit.errors import StreamlitAPIException, StreamlitSecretNotFoundError

AUTH_SESSION_MAX_AGE_SECONDS = 8 * 60 * 60


def is_logged_in():
    try:
        if (
            not hasattr(st, "user")
            or not getattr(st.user, "is_logged_in", False)
            or not st.user.get("email_verified", False)
        ):
            return False
    except Exception:
        return False

    now = time.time()
    session_started = st.session_state.get("auth_session_started_at")
    if session_started is None:
        st.session_state.auth_session_started_at = now
    elif now - session_started >= AUTH_SESSION_MAX_AGE_SECONDS:
        st.session_state.pop("auth_session_started_at", None)
        st.session_state.current_route = "HOME"
        try:
            st.logout()
        except Exception:
            pass
        return False

    return True


def current_email():
    try:
        if hasattr(st, "user"):
            return str(st.user.get("email", "")).strip().lower()
    except Exception:
        pass
    return ""


def _authorization_config():
    try:
        return st.secrets["authorization"]
    except (KeyError, StreamlitSecretNotFoundError):
        return {}


def has_role(role):
    cfg = _authorization_config()
    configured_emails = cfg.get(f"{role}_emails", [])
    if not configured_emails:
        return True  # Open access in local dev if no allowlist is configured yet

    if not is_logged_in():
        return False

    email = current_email()
    if not email:
        return False

    return email in {str(value).strip().lower() for value in configured_emails}


def has_committee_access(committee):
    if has_role("admin"):
        return True

    committee_roles = _authorization_config().get("committees", {})
    configured_emails = committee_roles.get(committee, [])
    if not configured_emails:
        return True  # Open access in local dev if no allowlist is configured yet

    if not is_logged_in():
        return False

    email = current_email()
    return email in {str(value).strip().lower() for value in configured_emails}


def render_login_prompt(role):
    st.info(
        f"Sign in with your configured identity provider to access {role}."
    )
    if st.button("Sign in", key=f"oidc_login_{role}"):
        try:
            st.login()
        except StreamlitAPIException as exc:
            st.error(
                f"OIDC login is unavailable. Check the Streamlit auth configuration: {exc}"
            )


def require_passcode(role):
    cfg = _authorization_config()
    passcode = cfg.get("passcode", "ali2027")
    if not isinstance(passcode, str) or not passcode:
        st.error("The configured access passcode must be a non-empty string.")
        return False

    session_key = f"passcode_authenticated_{role}"
    if st.session_state.get(session_key, False):
        return True

    entered_passcode = st.text_input(
        "Enter the access passcode",
        type="password",
        key=f"passcode_input_{role}",
    )
    if st.button("Unlock", key=f"passcode_unlock_{role}"):
        if hmac.compare_digest(entered_passcode.encode(), passcode.encode()):
            st.session_state[session_key] = True
            st.rerun()
        else:
            st.error("Incorrect passcode.")
    return False


def clear_passcode_access():
    for role in ("admin", "agent", "collation"):
        st.session_state.pop(f"passcode_authenticated_{role}", None)
        st.session_state.pop(f"passcode_input_{role}", None)


def require_role(role):
    if not require_passcode(role):
        return False

    cfg = _authorization_config()
    if not cfg.get(f"{role}_emails", []):
        return True

    if not is_logged_in():
        render_login_prompt(role)
        return False

    if not has_role(role):
        st.error(f"Your account is not authorized for the {role} role.")
        return False

    return True
