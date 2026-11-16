from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from auth import require_role
from persistence import ALLOWED_EVIDENCE_TYPES, MAX_EVIDENCE_BYTES

_COLUMNS = [
    "LGA",
    "Ward",
    "PU_Code",
    "PU_Name",
    "BVAS_Serial",
    "Accredited_Voters",
    "Total_Votes_Cast",
    "Party_A",
    "Party_B",
    "Form_EC8A_Status",
    "Agent",
]
_LGAS = ("Balanga", "Billiri", "Kaltungo", "Shongom")


def _validate_evidence(upload):
    if upload is None:
        return "Upload the signed Form EC8A."
    content_type = upload.type
    data = upload.getvalue()
    if content_type not in ALLOWED_EVIDENCE_TYPES:
        return "Evidence must be a PDF, JPEG, or PNG file."
    if not data or len(data) > MAX_EVIDENCE_BYTES:
        return "Evidence must be non-empty and no larger than 10 MB."
    signatures = {
        "application/pdf": b"%PDF-",
        "image/jpeg": b"\xff\xd8\xff",
        "image/png": b"\x89PNG\r\n\x1a\n",
    }
    if not data.startswith(signatures[content_type]):
        return "The uploaded file content does not match its file type."
    return None


def _render_field_form():
    st.subheader("Field Agent Form EC8A upload portal")
    with st.form("election_war_room_field_agent", clear_on_submit=False):
        lga = st.selectbox("LGA", _LGAS, index=None)
        ward = st.text_input("Ward")
        pu_code = st.text_input("Polling Unit Code")
        pu_name = st.text_input("Polling Unit Name")
        bvas_serial = st.text_input("BVAS Serial")
        agent = st.text_input("Agent")
        accredited = st.number_input("Accredited Voters", min_value=0, step=1)
        total = st.number_input("Total Votes Cast", min_value=0, step=1)
        party_a = st.number_input("Party A Votes", min_value=0, step=1)
        party_b = st.number_input("Party B Votes", min_value=0, step=1)
        evidence = st.file_uploader("Signed Form EC8A", type=["pdf", "jpg", "png"])
        submitted = st.form_submit_button("Add polling unit result")

    if not submitted:
        return
    ward = ward.strip()
    pu_code = pu_code.strip()
    pu_name = pu_name.strip()
    bvas_serial = bvas_serial.strip()
    agent = agent.strip()
    if not all((lga, ward, pu_code, pu_name, bvas_serial, agent)):
        st.error("Complete all polling unit and agent fields.")
        return
    if total > accredited or party_a + party_b > total:
        st.error(
            "Total votes cannot exceed accredited voters, and party votes "
            "cannot exceed total votes cast."
        )
        return
    if evidence is None:
        st.error("Upload the signed Form EC8A.")
        return
    error = _validate_evidence(evidence)
    if error:
        st.error(error)
        return

    if any(
        row["LGA"].casefold() == lga.casefold()
        and row["Ward"].casefold() == ward.casefold()
        and row["PU_Code"].casefold() == pu_code.casefold()
        for row in st.session_state.election_data
    ):
        st.error("A result for this polling unit is already in this session.")
        return

    record = {
        "LGA": lga,
        "Ward": ward,
        "PU_Code": pu_code,
        "PU_Name": pu_name,
        "BVAS_Serial": bvas_serial,
        "Accredited_Voters": int(accredited),
        "Total_Votes_Cast": int(total),
        "Party_A": int(party_a),
        "Party_B": int(party_b),
        "Form_EC8A_Status": "Uploaded - Awaiting Verification",
        "Agent": agent,
    }
    st.session_state.election_data.append(record)
    evidence_key = (lga, ward, pu_code)
    st.session_state.election_evidence[evidence_key] = {
        "name": evidence.name,
        "type": evidence.type,
        "data": evidence.getvalue(),
        "received_at": datetime.now().astimezone().isoformat(),
    }
    st.rerun()


def _render_dashboard():
    frame = pd.DataFrame(st.session_state.election_data, columns=_COLUMNS)
    filter_lga = st.selectbox(
        "Filter by LGA", ["All"] + sorted(frame["LGA"].unique().tolist())
    )
    filter_status = st.selectbox(
        "Filter by Form EC8A status",
        ["All"] + sorted(frame["Form_EC8A_Status"].unique().tolist()),
    )
    if filter_lga != "All":
        frame = frame[frame["LGA"] == filter_lga]
    if filter_status != "All":
        frame = frame[frame["Form_EC8A_Status"] == filter_status]

    columns = st.columns(4)
    columns[0].metric("Polling units", len(frame))
    columns[1].metric("Accredited voters", f"{frame['Accredited_Voters'].sum():,}")
    columns[2].metric("Total votes cast", f"{frame['Total_Votes_Cast'].sum():,}")
    columns[3].metric(
        "Awaiting verification",
        int((frame["Form_EC8A_Status"] == "Uploaded - Awaiting Verification").sum()),
    )
    if frame.empty:
        st.info("No results match the selected filters.")
        return

    shares = pd.DataFrame(
        {
            "Party": ["Party A", "Party B"],
            "Votes": [frame["Party_A"].sum(), frame["Party_B"].sum()],
        }
    )
    if shares["Votes"].sum() > 0:
        st.plotly_chart(
            px.pie(shares, names="Party", values="Votes", title="A/B vote share"),
            width="stretch",
        )
    else:
        st.info("Party A and Party B have no recorded votes to chart.")

    by_lga = (
        frame.groupby("LGA", as_index=False)[["Party_A", "Party_B"]]
        .sum()
        .melt(id_vars="LGA", var_name="Party", value_name="Votes")
    )
    st.plotly_chart(
        px.bar(by_lga, x="LGA", y="Votes", color="Party", barmode="group"),
        width="stretch",
    )
    st.dataframe(frame, hide_index=True)


def _render_evidence_download():
    if not st.session_state.election_evidence:
        return
    selected = st.selectbox(
        "Session evidence",
        list(st.session_state.election_evidence),
        format_func=lambda value: " / ".join(value),
    )
    evidence = st.session_state.election_evidence[selected]
    st.download_button(
        "Download session Form EC8A",
        data=evidence["data"],
        file_name=evidence["name"],
        mime=evidence["type"],
    )


def render_election_war_room():
    if not require_role("admin"):
        return

    if "election_data" not in st.session_state:
        st.session_state.election_data = []
    if "election_evidence" not in st.session_state:
        st.session_state.election_evidence = {}

    st.subheader("Election War Room")
    st.warning(
        "Results and evidence are private to this browser session; they are "
        "not shared or saved after the session ends."
    )
    _render_dashboard()
    _render_field_form()
    _render_evidence_download()
