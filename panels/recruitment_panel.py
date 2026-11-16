import json
import tempfile
import threading
import textwrap
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import streamlit as st

from auth import _authorization_config, current_email, require_role
from intelligence.scrapers import fetch_live_federal_listings
from panels import _valid_phone
from persistence import PersistenceError, list_submissions, submit_submission
from registry import LGA_WARD_DATA


_BASELINE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "constituency_baseline.json"
)
_BASELINE_LOCK = threading.Lock()
_UNCONFIRMED_QUOTA = "Unconfirmed - Pending Quota Allocation"
_LGAS = ("Balanga", "Billiri", "Kaltungo", "Shongom")


def _badge(listing):
    if listing.get("source_badge") == "Live Agency Feed":
        return "Live Agency Feed"
    if listing.get("office_verified") is True:
        return "Verified Constituency Office Registry"
    return "Pending Office Verification"


def _source(listing):
    if _badge(listing) != "Live Agency Feed":
        return "Constituency office registry"
    return urlparse(listing.get("url", "")).hostname or "Official agency"


def _quota(listing):
    slots = listing.get("slots")
    if isinstance(slots, int) and not isinstance(slots, bool) and slots >= 0:
        return f"{slots:,}"
    return _UNCONFIRMED_QUOTA


def _render_opportunities(listings):
    st.markdown("### 💼 FEDERAL & CONSTITUENCY VACANCY PORTAL")
    st.write("---")
    
    if not listings:
        st.info("No opportunities are currently available to display.")
        return

    # High-contrast search and filter controls
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input(
            "🔍 Search opportunities",
            placeholder="Search by job title, agency, or keywords...",
            key="vacancy_search",
        )
    with col2:
        categories = sorted(set(l.get("category", "Other") for l in listings))
        selected_category = st.selectbox(
            "📋 Filter by category",
            ["All Categories"] + categories,
            key="vacancy_category_filter",
        )

    # Filter listings based on search and category
    filtered_listings = listings
    if search_query:
        search_lower = search_query.lower()
        filtered_listings = [
            l for l in filtered_listings
            if search_lower in l.get("title", "").lower()
            or search_lower in l.get("description", "").lower()
            or search_lower in l.get("category", "").lower()
        ]
    
    if selected_category != "All Categories":
        filtered_listings = [
            l for l in filtered_listings
            if l.get("category") == selected_category
        ]

    if not filtered_listings:
        st.info("No opportunities match your search criteria.")
        return

    st.caption(f"📊 Showing {len(filtered_listings)} of {len(listings)} opportunities")
    st.write("")

    # Render high-contrast card grid
    for listing in filtered_listings:
        badge = _badge(listing)
        source = _source(listing)
        quota = _quota(listing)
        category = listing.get("category", "Not stated")
        title = listing.get("title", "Untitled")
        deadline = listing.get("deadline", "Not confirmed")
        status = listing.get("status", "Availability unconfirmed")
        description = listing.get("description", "")
        url = listing.get("url", "")

        # High-contrast card styling
        card_html = textwrap.dedent(f"""\
<div style="background: linear-gradient(135deg, #12161F 0%, #0E1117 100%); border: 1.5px solid #D4AF37; border-radius: 8px; padding: 18px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.15);">
<h4 style="color: #D4AF37; margin: 0 0 8px 0; font-size: 1.15rem;">{title}</h4>
<div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 10px;"><span style="display: inline-block; margin-right: 12px;"><strong style="color: #F7FAFC;">Agency:</strong> {source}</span><span style="display: inline-block;"><strong style="color: #F7FAFC;">Category:</strong> {category}</span></div>
<div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 10px;"><span style="display: inline-block; margin-right: 12px;"><strong style="color: #F7FAFC;">Status:</strong> {status}</span><span style="display: inline-block;"><strong style="color: #F7FAFC;">Deadline:</strong> {deadline}</span></div>
<div style="color: #A0AEC0; font-size: 0.85rem; margin-bottom: 12px;"><strong style="color: #F7FAFC;">Allocation:</strong> {quota}</div>
<div style="background-color: #1B202C; border-left: 3px solid #D4AF37; padding: 10px; border-radius: 4px; margin-bottom: 12px; color: #F7FAFC; font-size: 0.9rem;">{description}</div>
<div style="background-color: #161B26; padding: 8px 12px; border-radius: 4px; display: inline-block; margin-bottom: 12px;"><span style="color: #D4AF37; font-weight: 600; font-size: 0.8rem;">🏛️ {badge}</span></div>
</div>""")
        st.markdown(card_html, unsafe_allow_html=True)

        # Apply button row
        if badge == "Live Agency Feed" and url:
            st.link_button(
                "🌐 Apply Now at Official Portal",
                url,
                use_container_width=True,
            )
        st.write("")  # Spacing


def _render_application_form(listings):
    st.subheader("Constituent Application & Verification Form")
    if not listings:
        st.info("An opportunity is required before applying.")
        return

    st.caption(
        "Your identity and contact information will be stored for "
        "constituency office verification."
    )
    lga = st.selectbox(
        "LGA",
        _LGAS,
        index=None,
        placeholder="Select your LGA",
        key="recruitment_application_lga",
    )
    with st.form("constituent_recruitment_application", clear_on_submit=False):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone")
        identity = st.text_input("NIN / Voter ID", type="password")
        wards = LGA_WARD_DATA.get(lga.upper(), []) if lga else []
        if wards:
            ward = st.selectbox("Ward", wards, index=None)
        else:
            ward = st.text_input("Ward")
        selected = st.selectbox(
            "Target Program",
            range(len(listings)),
            index=None,
            format_func=lambda index: (
                f"{listings[index]['title']} - {_source(listings[index])}"
            ),
        )
        submitted = st.form_submit_button("Submit application")

    if not submitted:
        return
    name = name.strip()
    phone = phone.strip()
    identity = identity.strip()
    ward = (ward or "").strip()
    if not all((name, phone, identity, lga, ward)) or selected is None:
        st.error("Complete every required application field.")
        return
    if not _valid_phone(phone):
        st.error("Enter a valid contact phone number.")
        return

    listing = listings[selected]
    try:
        submit_submission(
            "recruitment_application",
            {
                "name": name,
                "phone": phone,
                "identity_number": identity,
                "lga": lga,
                "ward": ward,
                "target_program": listing["title"],
                "program_source": _source(listing),
                "program_url": listing.get("url", ""),
                "submitted_at": datetime.now().astimezone().isoformat(),
            },
            dedupe_fields=["identity_number", "target_program", "program_source"],
        )
    except PersistenceError as exc:
        st.error(f"Application could not be saved: {exc}")
        return
    st.success("Your application was submitted for office verification.")


def _admin_access():
    if not _authorization_config().get("admin_emails"):
        st.error(
            "Configure authorization.admin_emails and authenticated login "
            "before using the recruitment admin war room."
        )
        return False
    return require_role("admin")


def _latest_decisions(records):
    decisions = {}
    for record in records:
        if record.get("submission_type") != "recruitment_vetting_decision":
            continue
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        application_id = payload.get("application_id")
        if application_id and application_id not in decisions:
            decisions[application_id] = payload
    return decisions


def _render_vetting():
    try:
        records = list_submissions(
            ["recruitment_application", "recruitment_vetting_decision"],
            limit=1000,
        )
    except PersistenceError as exc:
        st.error(f"Applications could not be loaded: {exc}")
        return
    if records is None:
        return

    decisions = _latest_decisions(records)
    applications = [
        record
        for record in records
        if record.get("submission_type") == "recruitment_application"
        and record.get("id")
        and isinstance(record.get("payload"), dict)
    ]
    st.caption("Showing up to the 1,000 most recent application and review records.")
    if not applications:
        st.info("No applications are available for vetting.")
        return

    summary = []
    for application in applications:
        payload = application["payload"]
        decision = decisions.get(application["id"], {})
        summary.append(
            {
                "Name": payload.get("name", ""),
                "LGA": payload.get("lga", ""),
                "Ward": payload.get("ward", ""),
                "Program": payload.get("target_program", ""),
                "Decision": decision.get("decision", "Pending"),
                "Application ID": application["id"],
            }
        )
    st.dataframe(pd.DataFrame(summary), hide_index=True)

    selected_id = st.selectbox(
        "Application to review",
        [application["id"] for application in applications],
        format_func=lambda identifier: next(
            f"{item['payload'].get('name', '')} - "
            f"{item['payload'].get('target_program', '')} ({identifier})"
            for item in applications
            if item["id"] == identifier
        ),
    )
    application = next(item for item in applications if item["id"] == selected_id)
    payload = application["payload"]
    st.write(f"Phone: {payload.get('phone', '')}")
    st.write(f"NIN / Voter ID: {payload.get('identity_number', '')}")
    current = decisions.get(selected_id, {}).get("decision", "Pending")
    st.write(f"Current decision: {current}")

    with st.form("recruitment_vetting_decision"):
        decision = st.radio("Decision", ("Approved", "Rejected"), horizontal=True)
        submitted = st.form_submit_button("Save decision")
    if submitted:
        try:
            submit_submission(
                "recruitment_vetting_decision",
                {
                    "application_id": selected_id,
                    "decision": decision,
                    "reviewed_by": current_email(),
                    "reviewed_at": datetime.now().astimezone().isoformat(),
                },
            )
        except PersistenceError as exc:
            st.error(f"Decision could not be saved: {exc}")
            return
        st.success(f"Application marked {decision.lower()}.")
        st.rerun()


def _read_baseline():
    raw = _BASELINE_PATH.read_text(encoding="utf-8")
    entries = json.loads(raw)
    if not isinstance(entries, list) or not all(
        isinstance(entry, dict) and isinstance(entry.get("title"), str)
        for entry in entries
    ):
        raise ValueError("The constituency baseline must contain titled records.")
    return raw, entries


def _save_baseline(expected_raw, index, verified, slots):
    with _BASELINE_LOCK:
        current_raw, entries = _read_baseline()
        if current_raw != expected_raw:
            raise ValueError(
                "The baseline changed during editing. Reload before saving."
            )
        entries[index]["office_verified"] = verified
        entries[index]["slots"] = slots
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=_BASELINE_PATH.parent,
                delete=False,
            ) as file:
                temporary_path = Path(file.name)
                json.dump(entries, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temporary_path.replace(_BASELINE_PATH)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
    fetch_live_federal_listings.clear()


def _render_baseline_editor():
    st.markdown("#### Constituency office registry")
    st.caption(
        "Updates modify the local baseline file. Use persistent shared storage "
        "if the deployment has multiple instances or ephemeral filesystems."
    )
    try:
        raw, entries = _read_baseline()
    except (OSError, ValueError) as exc:
        st.error(f"Constituency registry could not be loaded: {exc}")
        return
    if not entries:
        st.info("The constituency registry is empty.")
        return

    index = st.selectbox(
        "Constituency program",
        range(len(entries)),
        format_func=lambda item: entries[item]["title"],
    )
    entry = entries[index]
    current_slots = entry.get("slots")
    confirmed = (
        isinstance(current_slots, int)
        and not isinstance(current_slots, bool)
        and current_slots >= 0
    )
    with st.form("constituency_registry_update"):
        verified = st.checkbox(
            "Office verified", value=entry.get("office_verified") is True
        )
        quota_confirmed = st.checkbox("Quota confirmed", value=confirmed)
        slots = st.number_input(
            "Confirmed slot count",
            min_value=0,
            value=current_slots if confirmed else 0,
            step=1,
        )
        submitted = st.form_submit_button("Save registry changes")
    if submitted:
        try:
            _save_baseline(
                raw,
                index,
                verified,
                int(slots) if quota_confirmed else _UNCONFIRMED_QUOTA,
            )
        except (OSError, ValueError) as exc:
            st.error(f"Constituency registry could not be saved: {exc}")
            return
        st.success("Constituency registry updated.")
        st.rerun()


def render_recruitment_panel(is_admin_mode: bool = False):
    listings = fetch_live_federal_listings()
    _render_opportunities(listings)
    _render_application_form(listings)
    if is_admin_mode:
        st.subheader("Admin War Room: Constituency Vetting Firewall")
        if not _admin_access():
            return
        _render_vetting()
        _render_baseline_editor()
