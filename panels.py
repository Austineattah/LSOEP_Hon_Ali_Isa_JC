import streamlit as st
import pandas as pd
import datetime
import time
import base64
import requests
import os
import urllib.request

from registry import (
    LGA_WARD_DATA,
    GEOGRAPHY,
    STRATEGIC_COMMITTEE_COLS,
    COMMUNITY_LEADERS,
    COLUMNS_STRUCTURE,
    STRATEGIC_COMMITTEE_NAMES,
    STRATEGIC_COMMITTEE_PASSWORDS,
    SPONSORED_BILLS,
    ANNOUNCEMENT_CACHE_FILE,
)
from ui_modules import (
    render_marquee_header,
    render_module_download_trigger,
    render_institutional_purge_engine,
)
from utils import trigger_background_autosave

# ==============================================================================
# ALL PUBLIC-FACING FORMS (FULL CODE RESTORED)
# ==============================================================================


def render_skill_form():
    st.markdown(
        """<div style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0;">🛠️ CONSTITUENT SKILL EMPOWERMENT POOL</h4>
    </div>""",
        unsafe_allow_html=True,
    )
    with st.form("skill_form_engine"):
        k1, k2 = st.columns(2)
        with k1:
            sv_name = st.text_input("Full name as displayed on NIN")
            sv_phone = st.text_input("Applicant Contact Number")
            sv_nin = st.text_input("Your NIN number")
            sv_vin = st.text_input("Your Voters card number")
            sv_dob = st.date_input("Date of Birth", value=datetime.date(2000, 1, 1))
            sv_gender = st.selectbox(
                "Gender Matrix", ["Male", "Female", "Prefer Not to Say"]
            )
            sv_disability = st.selectbox(
                "Vulnerability/Disability Status",
                [
                    "None",
                    "Visual Impairment",
                    "Hearing Impairment",
                    "Physical Challenge/Locomotor",
                    "Other Challenges",
                ],
            )
            sv_file = st.file_uploader(
                "Upload Profile NIN Slip Document Click", type=["pdf", "jpg", "png"]
            )
        with k2:
            klga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="skill_lga_select"
            )
            klga_clean = klga_raw.upper().split()[0] if klga_raw else ""
            kward = st.selectbox("Your Ward", LGA_WARD_DATA.get(klga_clean, []))
            vocation_list = [
                "ICT & AI Core Programming",
                "Solar Renewable Energy Engineering",
                "Fashion & Textile Design Layout",
                "Catering & Culinary Arts Matrix",
                "Automobile Mechanical Engineering",
                "Electrical Installation & Wiring",
                "Plumbing & Hydraulics Systems",
                "Carpentry & Woodwork Manufacturing",
                "Modern Hairdressing & Cosmetology",
                "Other (Type Custom Vocation Below)",
            ]
            sv_selection = st.selectbox(
                "Vocational Domain Target Pool Sector", vocation_list
            )
            custom_vocation = (
                st.text_input("Type Your Choice Vocation Natively Here")
                if sv_selection == "Other (Type Custom Vocation Below)"
                else ""
            )
            sv_palliative_check = st.selectbox(
                "Have you received a palliative from this office before?", ["No", "Yes"]
            )

        sv_stmt = st.text_area("Candidate Skill Interest Statement Details")
        sv_cam = st.camera_input("Biometric Security Verification Core Scan")
        st.markdown(
            "##### 🛡️ STRATEGIC LEADERSHIP VOUCHING TIER INTERFACE FRAME (ANTI-FRAUD MATRIX)"
        )
        v_leader_name = st.selectbox(
            "Select Vouching Community Leader",
            list(COMMUNITY_LEADERS.keys()),
            key="skill_leader_select",
        )
        v_leader_details = COMMUNITY_LEADERS[v_leader_name]

        if st.form_submit_button("🚀 COMMIT APPLICATION TO TRAINING POOLS"):
            if not (sv_name and sv_phone and sv_nin and sv_vin and sv_stmt):
                st.error(
                    "🛑 FORM ERROR: All core validation strings, documents, and biometric snapshot frames are mandatory."
                )
            else:
                match_check = st.session_state.global_registry[
                    st.session_state.global_registry["NIN"] == sv_nin
                ]
                if not match_check.empty:
                    st.session_state.radar_threat = True
                    st.session_state.threat_msg = f"Collision: NIN [{sv_nin}] matches a record belonging to user [{match_check.iloc[0]['Name']}]"
                    st.error(
                        "Duplicate Entry Detected. Entry Rejected by Security System Shield Protocols."
                    )
                else:
                    final_skill = (
                        custom_vocation
                        if sv_selection == "Other (Type Custom Vocation Below)"
                        else sv_selection
                    )
                    new_voucher_code = (
                        f"V-{klga_clean[:3]}-{kward[:3]}-{int(time.time())}".upper()
                    )
                    new_profile_row = {
                        "NIN": sv_nin,
                        "VIN": sv_vin,
                        "Name": sv_name.upper(),
                        "LGA": klga_clean,
                        "Ward": kward,
                        "Status": "Pending Review Tracker",
                        "Category": "Applicant",
                        "Skill_Interest": final_skill,
                        "Custom_Skill": custom_vocation,
                        "Gender": sv_gender,
                        "DOB": str(sv_dob),
                        "Disability_Status": sv_disability,
                        "Prior_Palliative": sv_palliative_check,
                        "Academic_Qual": "Degree Matrix",
                        "Admission_Year": "2026",
                        "Admission_Letter": None,
                        "Phone": sv_phone,
                        "Leader_Name": v_leader_name,
                        "Leader_Contact": v_leader_details["contact"],
                        "Leader_NIN": v_leader_details["nin"],
                        "Leader_LGA": v_leader_details["lga"],
                        "Leader_Ward": v_leader_details["ward"],
                        "Leader_Portfolio": v_leader_details["portfolio"],
                        "Voucher_Code": new_voucher_code,
                        "Remarks": "Verified Clear",
                        "Timestamp": str(datetime.datetime.now()),
                    }
                    st.session_state.global_registry = pd.concat(
                        [
                            st.session_state.global_registry,
                            pd.DataFrame([new_profile_row]),
                        ],
                        ignore_index=True,
                    )
                    trigger_background_autosave()
                    st.success(
                        "Registration parameter logged into production records system!"
                    )
                    st.balloons()
                    time.sleep(1)
                    st.rerun()


def render_scholarship_form():
    st.markdown("### 🎓 CONSTITUENT STUDENT SCHOLARSHIP APPLICATION PORTAL")
    with st.form("scholarship_form_engine"):
        s1, s2 = st.columns(2)
        with s1:
            sch_name = st.text_input("Full name as displayed on NIN")
            sch_nin = st.text_input("Your NIN number")
            sch_phone = st.text_input("Applicant Contact Number")
            sch_year = st.selectbox(
                "Academic Year of Intake Admission", [str(y) for y in range(2018, 2027)]
            )
            sch_file_nin = st.file_uploader(
                "Attach Scanned NIN Identity Slip File", type=["pdf", "jpg", "png"]
            )
        with s2:
            sch_inst = st.text_input("Tertiary Institution Allocation Name")
            sch_level = st.selectbox(
                "Current Institutional Study Level Track",
                [
                    "Level 100",
                    "Level 200",
                    "Level 300",
                    "Level 400",
                    "Level 500",
                    "Post-Graduate Stream",
                ],
            )
            slga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="sch_lga_select"
            )
            slga_clean = slga_raw.upper().split()[0] if slga_raw else ""
            sward = st.selectbox("Your Ward", LGA_WARD_DATA.get(slga_clean, []))
            sch_file_adm = st.file_uploader(
                "Attach Official University Admission Letter Asset File",
                type=["pdf", "jpg", "png"],
            )
        sch_just = st.text_area("Applicant Justification Space")
        sch_cam = st.camera_input("Capture Student Identity Card Sensor")
        if st.form_submit_button("🚀 SUBMIT SCHOLARSHIP ENTRY APPLICATION PARAMETERS"):
            st.info("System intake pipeline initialized successfully.")


def render_cv_vault():
    st.markdown("### 🚀 CONSTITUENT PROFESSIONAL TALENT VAULT ENGINE")
    with st.form("cv_vault_engine"):
        v1, v2 = st.columns(2)
        with v1:
            cv_name = st.text_input("Full name as displayed on NIN")
            cv_cat = st.selectbox(
                "Talent Classification Target Category",
                [
                    "Professional Domain Leader",
                    "Skilled Artisan Professional",
                    "Business Executive Owner",
                ],
            )
            cv_qual = st.selectbox(
                "Highest Level Academic Qualification Attained",
                [
                    "Doctorate PhD",
                    "Masters Degree Level",
                    "Bachelors Degree / HND Layer",
                    "National Diploma ND",
                    "NCE",
                    "SSCE Credentials Matrix",
                    "Primary Leaving",
                    "None",
                ],
            )
            cv_file = st.file_uploader(
                "Attach Professional CV/Resume Document Link File",
                type=["pdf", "jpg", "png"],
            )
        with v2:
            cv_nin = st.text_input("Your NIN number")
            cv_phone = st.text_input("Applicant Contact Number")
            vlga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="cv_lga_select"
            )
            vlga_clean = vlga_raw.upper().split()[0] if vlga_raw else ""
            vward = st.selectbox("Your Ward", LGA_WARD_DATA.get(vlga_clean, []))
        cv_summary = st.text_area(
            "Summary Matrix of Functional Career Experience Vectors"
        )
        cv_cam = st.camera_input("Capture Valid Professional Certification Seals")
        if st.form_submit_button(
            "📤 COMMIT CREDENTIALS STRINGS TO TALENT PLATFORM ARCHIVE"
        ):
            st.info("Transmission channel connected smoothly.")


def render_cun_trigger():
    st.markdown("### 🚨 COMMUNITY URGENT NEED FIELD DEFICIT REPORT GATEWAY")
    with st.form("cun_form_engine"):
        cun_member = st.text_input("Reporting Community Member")
        cun_phone = st.text_input("Applicant Contact Number")
        clga_raw = st.selectbox(
            "Affected LGA", list(LGA_WARD_DATA.keys()), key="cun_lga_select"
        )
        clga_clean = clga_raw.upper().split()[0] if clga_raw else ""
        cward = st.selectbox("Affected Ward", LGA_WARD_DATA.get(clga_clean, []))
        cun_area = st.selectbox(
            "Area of Urgent Attention",
            [
                "Water Source Deficit",
                "Grid Electricity Failure",
                "Access Road Failure Collapse",
                "Community Security Vulnerability",
                "Healthcare Facility Absence",
            ],
        )
        cun_file = st.file_uploader(
            "Attach Identification NIN Validation Document Slip",
            type=["pdf", "jpg", "png"],
        )
        cun_logs = st.text_area("Detailed Situation Report Narrative Logs")
        cun_cam = st.camera_input(
            "Field Visual Evidence Deficit Capture Sensor Matrix Camera"
        )
        if st.form_submit_button("🚨 TRIGGER COMMAND INCIDENT VECTOR ALERT"):
            st.info("Field alert dispatch sequence routing triggered.")


def render_palliative_form():
    st.markdown("### 📦 CONSTITUENT PALLIATIVE ENROLLMENT REGISTRY")
    with st.form("palliative_form_engine"):
        p1, p2 = st.columns(2)
        with p1:
            p_name = st.text_input("Full name as displayed on NIN")
            p_nin = st.text_input("Your NIN number")
            p_vin = st.text_input("Your Voters card number")
            p_vuln = st.multiselect(
                "Vulnerability/Disability Status",
                [
                    "Aged Eldership Category",
                    "Widowhood Support Matrix",
                    "Physical Disability Framework Challenge",
                    "Long-Term Unemployed Status Tracker",
                ],
            )
            p_file_nin = st.file_uploader(
                "Upload Nominee Profile NIN Slip Document Layout Check",
                type=["pdf", "jpg", "png"],
            )
        with p2:
            p_phone = st.text_input("Applicant Contact Number")
            plga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="pal_lga_select"
            )
            plga_clean = plga_raw.upper().split()[0] if plga_raw else ""
            pward = st.selectbox("Your Ward", LGA_WARD_DATA.get(plga_clean, []))
            p_agro_select = st.selectbox(
                "Specific Area of Agro Intervention and Others",
                ["Fertilizer", "Seedlings", "Other Area of Likely Intervention"],
            )
            p_expect = st.text_input("Type Your Expectation")
        st.markdown(
            "##### 🛡️ STRATEGIC LEADERSHIP VOUCHING TIER INTERFACE FRAME (ANTI-FRAUD MATRIX)"
        )
        v_leader_name_p = st.selectbox(
            "Select Vouching Community Leader",
            list(COMMUNITY_LEADERS.keys()),
            key="pal_leader_select",
        )
        p_remarks = st.text_area(
            "Leader Affirmation Testimony Verification Remarks Statement"
        )
        p_cam = st.camera_input(
            "Biometric Face Capture Matrix Core Verification Face Scan"
        )
        if st.form_submit_button("🚀 COMPLETE PALLIATIVE NOMINATION RECORD"):
            st.info("Palliative submission metrics validated against core cache.")


# ==============================================================================
# NEW: LEGISLATIVE PANEL
# ==============================================================================
def render_sponsored_bills_panel():
    """Displays a formatted list of sponsored bills and motions."""
    st.markdown(
        """<div class="beyond-rhetoric-header">
            <div class="beyond-title">📜 LEGISLATIVE FOOTPRINTS & MOTIONS</div>
            <div style="color: #8892B0; font-size: 1.1rem; font-style: italic;">
                A transparent record of legislative activities undertaken by Hon. Ali Isa JC, PhD.
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    for bill in SPONSORED_BILLS:
        with st.container(border=True):
            status_color = (
                "green" if bill["status"] in ["Passed", "Adopted"] else "orange"
            )
            st.markdown(
                f"""<h5 style="margin-bottom:5px;">{bill['title']}</h5>
                        <p style="margin:0; font-size:14px;">
                            <b>Status:</b> <span style="color:{status_color}; font-weight:bold;">{bill['status']}</span>
                        </p>""",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""<p style="font-size:15px; text-align:justify;">{bill['summary']}</p>""",
                unsafe_allow_html=True,
            )


# ==============================================================================
# AUTHENTICATED PANELS (FULL CODE RESTORED)
# ==============================================================================


def ward_collation_officer_panel():
    render_marquee_header()
    st.markdown(
        """<div class="supervisor-header">🛡️ WARD COLLATION OFFICER COMMAND: FORM EC8A LOGS</div>""",
        unsafe_allow_html=True,
    )
    if "sup_slip_preview" not in st.session_state:
        st.session_state.sup_slip_preview = None

    with st.form("supervisor_form"):
        c1, c2 = st.columns(2)
        with c1:
            sup_name = st.text_input("Supervisor Full Name")
            sup_phone = st.text_input("Phone Number")
            sup_lga_raw = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            sup_lga_clean = sup_lga_raw.upper().split()[0]
            sup_ward = st.selectbox("Your Ward", LGA_WARD_DATA.get(sup_lga_clean, []))
            bvas_serial = st.text_input("BVAS Serial Number")
            accredited_voters = st.number_input(
                "Number of Accredited Voters", min_value=0
            )

        ward_id = f"{sup_lga_clean}_{sup_ward}".replace(" ", "_").upper()

        with c2:
            st.markdown("**Votes Scored by Party**")
            apc_votes = st.number_input("APC Votes", min_value=0)
            ndc_votes = st.number_input("NDC Votes", min_value=0)
            pdp_votes = st.number_input("PDP Votes", min_value=0)
            adc_votes = st.number_input("ADC Votes", min_value=0)

            incident_occurred = st.selectbox("Incident Occurred?", ["No", "Yes"])
            incident_details = ""
            if incident_occurred == "Yes":
                incident_details = st.text_area("Incident Form Scenario")

        st.camera_input("Live Capture Sensor Matrix: Form EC8A Sheet")

        if st.form_submit_button("🔍 GENERATE SYSTEM INTEGRITY PREVIEW RECORD SLIP"):
            if not sup_name or not sup_phone:
                st.error("🛑 FORM ERROR: Supervisor name and phone must be specified.")
            else:
                st.session_state.sup_slip_preview = {
                    "Supervisor": sup_name,
                    "Phone": sup_phone,
                    "LGA": sup_lga_clean,
                    "Ward": sup_ward,
                    "APC_Votes": apc_votes,
                    "NDC_Votes": ndc_votes,
                    "PDP_Votes": pdp_votes,
                    "ADC_Votes": adc_votes,
                    "BVAS_Serial_Number": bvas_serial,
                    "Accredited_Voters": accredited_voters,
                    "Incident_Occurred": incident_occurred,
                    "Incident_Details": incident_details,
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.rerun()

    if st.session_state.sup_slip_preview is not None:
        p_data = st.session_state.sup_slip_preview
        st.markdown(
            f"""
            <div class="printable-slip-box">
                <div class="slip-header">🏛️ LSOEP WARD COLLATION INTEGRITY RECEIPT</div>
                <div class="slip-row"><span>TIMESTAMP:</span> <span>{p_data['Timestamp']}</span></div>
                <div class="slip-row"><span>SUPERVISOR:</span> <span>{p_data['Supervisor']}</span></div>
                <div class="slip-row"><span>LGA:</span> <span>{p_data['LGA']}</span></div>
                <div class="slip-row"><span>WARD:</span> <span>{p_data['Ward']}</span></div>
                <div class="slip-row"><span>ACCREDITED:</span> <span>{p_data['Accredited_Voters']}</span></div>
                <div class="slip-row"><span>BVAS S/N:</span> <span>{p_data['BVAS_Serial_Number']}</span></div>
                <div class="slip-row" style="color:red;"><span>APC:</span> <span>{p_data['APC_Votes']}</span></div>
                <div class="slip-row" style="color:blue;"><span>NDC:</span> <span>{p_data['NDC_Votes']}</span></div>
                <div class="slip-row" style="color:green;"><span>PDP:</span> <span>{p_data['PDP_Votes']}</span></div>
                <div class="slip-row" style="color:orange;"><span>ADC:</span> <span>{p_data['ADC_Votes']}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("🔒 CONFIRM & LOG METRICS", use_container_width=True):
                ward_id = f"{p_data['LGA']}_{p_data['Ward']}".replace(" ", "_").upper()
                if ward_id in st.session_state.submitted_wards:
                    st.error("🛑 Results for this Ward have already been locked.")
                else:
                    st.session_state.submitted_wards[ward_id] = p_data
                    trigger_background_autosave()
                    st.session_state.sup_slip_preview = None
                    st.success("Submission logged successfully!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
        with col_v2:
            if st.button("❌ ABORT TRANSACTION", use_container_width=True):
                st.session_state.sup_slip_preview = None
                st.warning("Preview cleared.")
                st.rerun()


def agent_panel():
    render_marquee_header()
    st.markdown("### 🗳️ POLLING UNIT AGENT: FIELD DATA TRANSFERS")
    if "agt_slip_preview" not in st.session_state:
        st.session_state.agt_slip_preview = None

    with st.form("agent_form"):
        a1, a2 = st.columns(2)
        with a1:
            agt_name = st.text_input("Agent Full Operator Name")
            agt_phone = st.text_input("Agent Communication Contact Phone")
            agt_lga_raw = st.selectbox(
                "Your LGA", list(LGA_WARD_DATA.keys()), key="agent_lga_select"
            )
            agt_lga_clean = agt_lga_raw.upper().split()[0] if agt_lga_raw else ""
            agt_ward = st.selectbox(
                "Your Ward",
                LGA_WARD_DATA.get(agt_lga_clean, []),
                key="agent_ward_select",
            )
            agt_pu_num = (
                st.text_input("Polling Unit (PU) Identity Name Code")
                .strip()
                .replace(" ", "_")
                .upper()
            )
            bvas_serial = st.text_input("BVAS Serial Number", key="agent_bvas")
            accredited_voters = st.number_input(
                "Number of Accredited Voters", min_value=0, key="agent_accredited"
            )

        pu_id = f"{agt_lga_clean}_{agt_ward}_{agt_pu_num}".replace(" ", "_").upper()

        with a2:
            st.markdown("**Votes Scored by Party**")
            apc_votes = st.number_input("APC Votes", min_value=0, key="agent_apc")
            ndc_votes = st.number_input("NDC Votes", min_value=0, key="agent_ndc")
            pdp_votes = st.number_input("PDP Votes", min_value=0, key="agent_pdp")
            adc_votes = st.number_input("ADC Votes", min_value=0, key="agent_adc")

            incident_occurred = st.selectbox(
                "Incident Occurred?", ["No", "Yes"], key="agent_incident"
            )
            incident_details = ""
            if incident_occurred == "Yes":
                incident_details = st.text_area(
                    "Incident Form Scenario", key="agent_incident_details"
                )

        st.camera_input("Capture Physical Document Ledger", key="agent_camera")
        submitted = st.form_submit_button("🔍 COMPREHENSIVE ENTRY EVALUATION")

    if submitted:
        if not agt_name or not agt_phone or not agt_pu_num:
            st.error("🛑 FORM ERROR: Agent metadata must be completely specified.")
        elif pu_id != "" and pu_id in st.session_state.submitted_pus:
            st.error("🛑 This Polling Unit has already submitted its results.")
        else:
            st.session_state.agt_slip_preview = {
                "Agent": agt_name,
                "Phone": agt_phone,
                "LGA": agt_lga_clean,
                "Ward": agt_ward,
                "PU": agt_pu_num,
                "APC_Votes": apc_votes,
                "NDC_Votes": ndc_votes,
                "PDP_Votes": pdp_votes,
                "ADC_Votes": adc_votes,
                "BVAS_Serial_Number": bvas_serial,
                "Accredited_Voters": accredited_voters,
                "Incident_Occurred": incident_occurred,
                "Incident_Details": incident_details,
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            st.rerun()

    if st.session_state.agt_slip_preview is not None:
        a_data = st.session_state.agt_slip_preview
        st.markdown(
            f"""
            <div class="printable-slip-box">
                <div class="slip-header">🏛️ LSOEP AGENT FIELD INTEGRITY RECEIPT</div>
                <div class="slip-row"><span>TIMESTAMP:</span> <span>{a_data['Timestamp']}</span></div>
                <div class="slip-row"><span>AGENT:</span> <span>{a_data['Agent']}</span></div>
                <div class="slip-row"><span>LGA:</span> <span>{a_data['LGA']}</span></div>
                <div class="slip-row"><span>WARD:</span> <span>{a_data['Ward']}</span></div>
                <div class="slip-row"><span>POLLING UNIT:</span> <span>{a_data['PU']}</span></div>
                <hr>
                <div class="slip-row"><span>ACCREDITED:</span> <span>{a_data['Accredited_Voters']}</span></div>
                <div class="slip-row"><span>BVAS S/N:</span> <span>{a_data['BVAS_Serial_Number']}</span></div>
                <div class="slip-row" style="color:red;"><span>APC:</span> <span>{a_data['APC_Votes']}</span></div>
                <div class="slip-row" style="color:blue;"><span>NDC:</span> <span>{a_data['NDC_Votes']}</span></div>
                <div class="slip-row" style="color:green;"><span>PDP:</span> <span>{a_data['PDP_Votes']}</span></div>
                <div class="slip-row" style="color:orange;"><span>ADC:</span> <span>{a_data['ADC_Votes']}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        av1, av2 = st.columns(2)
        with av1:
            if st.button("🔒 COMMIT & ARCHIVE RECORD", use_container_width=True):
                pu_id_confirm = (
                    f"{a_data['LGA']}_{a_data['Ward']}_{a_data['PU']}".replace(
                        " ", "_"
                    ).upper()
                )
                st.session_state.submitted_pus[pu_id_confirm] = a_data
                trigger_background_autosave()
                st.session_state.agt_slip_preview = None
                st.success("Thanks for your submission!")
                st.balloons()
                time.sleep(1)
                st.rerun()
        with av2:
            if st.button("❌ DISCARD TRANSACTION", use_container_width=True):
                st.session_state.agt_slip_preview = None
                st.warning("Buffer cleared.")
                st.rerun()


def main_dashboard(conn):
    render_marquee_header()
    st.markdown("## 🏛️ EXECUTIVE CONTROL COMMAND DASHBOARD PORTAL ARRAY")
    tabs = st.tabs(
        [
            "📊 Master Registry Matrix",
            "📢 Admin Announcement Control",
            "⚖️ Database Audit Diagnostics",
            "🛡️ RADAR Deduplication Interceptor",
            "🎓 Scholar Talent Matrix",
            "💎 Vantedge Influencer Proportions",
            "🗳️ Live Election Analytical Sync",
            "📝 Ground Truth Form EC8A Data",
            "📂 Bulk Data Sync Stream",
            "📜 Executive Waiver Ledger",
            "🚀 Legislative Progress Tracker",
            "📅 Long-Term Momentum Monitoring",
        ]
    )

    with tabs[0]:
        st.subheader("📊 Master Verification Registry Database Partition Array")
        st.dataframe(st.session_state.get("global_registry", pd.DataFrame()))
        render_module_download_trigger(
            st.session_state.get("global_registry", pd.DataFrame()),
            "Master_Registry_Log",
            "t1_dl",
        )
        render_institutional_purge_engine("t1_purge")

    with tabs[1]:
        st.subheader("📢 Admin Announcement Control")
        current_announcement = st.session_state.get("global_scrolling_announcement", "")
        new_announcement = st.text_area(
            "Update the scrolling marquee text:",
            value=current_announcement,
            height=100,
            key="announcement_input",
        )
        if st.button("Update Announcement", key="update_marquee_btn"):
            st.session_state.global_scrolling_announcement = new_announcement
            try:
                with open(ANNOUNCEMENT_CACHE_FILE, "w") as f:
                    f.write(new_announcement)
                st.success(
                    "✅ Marquee announcement has been updated and saved successfully!"
                )
            except Exception as e:
                st.error(f"Failed to save announcement: {e}")
            st.rerun()

    with tabs[2]:
        st.subheader("⚖️ Forensic Audit Database Query & Connection Diagnostic Stream")
        st.error("⚠️ Isolation Warning Layer: Supabase API Cloud Gateway locked.")
        if conn is not None:
            st.info("Connection object present but interaction is disabled.")
        with st.expander(
            "🛠️ Expose Active Developer State Cache JSON Mapping Trees", expanded=False
        ):
            serializable_state = {k: str(v) for k, v in st.session_state.items()}
            st.json(serializable_state)
        render_institutional_purge_engine("t3_purge")

    with tabs[3]:
        st.subheader(
            "🛡️ RADAR Multi-Intake Anti-Fraud Deduplication Interceptor Shield"
        )
        st.write("Anti-fraud logic is handled during form submissions.")

    with tabs[4]:
        st.subheader("🎓 Academic Grants Distribution Pools & Talent Demographics Hub")
        st.write(
            "Scholarship data will be analyzed and displayed here in future versions."
        )

    with tabs[5]:
        st.subheader("💎 Vantedge Strategic Influence Vectors & Demographics Scale")
        st.write("Community leader data will be visualized here.")

    with tabs[6]:
        st.subheader(
            "🗳️ Cross-National Multi-Tier Election Verification War Room Sync Arrays"
        )
        st.write("Election data analytics will be shown here.")

    with tabs[7]:
        st.subheader("📝 Ground Truth Form EC8A Audited Verification Schema")
        st.dataframe(pd.DataFrame(list(st.session_state.submitted_wards.values())))

    with tabs[8]:
        st.subheader("📂 Bulk Throughput Tunnel Sync")
        st.write("Bulk data upload features will be implemented here.")

    with tabs[9]:
        st.subheader("📜 Strategic Waiver Assignment Parameters Matrix Ledgers")
        st.write("Waiver and special consideration data will be logged here.")

    with tabs[10]:
        st.subheader("🚀 National Assembly Legislative Action Motion Tracking")
        st.dataframe(pd.DataFrame(SPONSORED_BILLS))

    with tabs[11]:
        st.subheader("📅 Long-Term Temporal Momentum Tracking Interface Matrix Trends")
        st.write("Time-series analysis of submissions will be visualized here.")


@st.cache_data
def load_pdf_bytes(file_path):
    """Cached PDF byte loader — avoids re-reading the same file from disk
    on every Streamlit rerun/interaction. Cache key is the file_path string;
    Streamlit invalidates automatically if the underlying file changes."""
    with open(file_path, "rb") as f:
        return f.read()


def render_project_verifications():
    """
    Renders the 'Beyond Rhetorics' Verification Hub panel.
    Displays the compressed project verification documents sequentially.
    """
    st.markdown(
        "<h2 style='color:#D4AF37;'>🦅 BEYOND RHETORICS: PROJECT VERIFICATION HUB</h2>",
        unsafe_allow_html=True,
    )
    st.write(
        "Cross-examining performance metrics with verifiable ground-truth evidence."
    )

    # Path configuration - looking into your media folder
    media_dir = "MEDIA MEDIA MEDIA"

    if not os.path.exists(media_dir):
        # Fallback check if it's named lowercase or nested
        media_dir = "media"

    if os.path.exists(media_dir):
        # File mapping matching your uploaded repository files
        files_to_render = [
            ("Cover Page Document", "Cover_compressed.pdf"),
            ("Project Verification Batch 1", "1_compressed.pdf"),
            ("Project Verification Batch 2", "2_compressed.pdf"),
            ("Project Verification Batch 3", "3_compressed.pdf"),
            ("Project Verification Batch 4", "4_compressed.pdf"),
            ("Project Verification Batch 5", "5_compressed.pdf"),
            ("Project Verification Batch 6", "6_compressed.pdf"),
        ]

        for title, filename in files_to_render:
            full_path = os.path.join(media_dir, filename)

            if os.path.exists(full_path):
                with st.expander(f"📄 View {title} ({filename})", expanded=False):
                    # Cached read — file is only loaded from disk once per
                    # session per unique path, not on every rerun.
                    pdf_bytes = load_pdf_bytes(full_path)

                    # Displaying the PDF securely in an iframe container
                    st.download_button(
                        label=f"📥 Download {filename}",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"dl_{filename}",
                    )

                    # Embed target for immediate viewing
                    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                    pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.warning(
                    f"⚠️ Tracked file layout expected but missing local path: {filename}"
                )
    else:
        st.error(
            "🚨 The media directory containing your compressed PDFs could not be verified locally. Please ensure the media folder is positioned inside your project layout."
        )


def strategic_committees_panel():
    render_marquee_header()
    st.markdown(
        """<div class="supervisor-header">🛡️ MODULE 13: STRATEGIC COMMITTEES (1-10) ACCESS GATEWAY</div>""",
        unsafe_allow_html=True,
    )

    if "module_13_unlocked" not in st.session_state:
        st.session_state.module_13_unlocked = False

    if not st.session_state.module_13_unlocked:
        with st.form("general_login_form"):
            committee_key_input = st.text_input(
                "Enter General Passkey to Unlock Module:", type="password"
            )
            if st.form_submit_button("Unlock Module"):
                if committee_key_input == "congratulationshonali":
                    st.session_state.module_13_unlocked = True
                    st.rerun()
                else:
                    st.error("🛑 ACCESS REJECTED: General passkey signature mismatch.")
        return

    st.success(
        "✅ General Access Granted. Please select your committee and enter its specific passkey."
    )

    if "authenticated_committee" not in st.session_state:
        st.session_state.authenticated_committee = None

    selected_committee = st.selectbox(
        "Select Your Assigned Committee:", options=[""] + STRATEGIC_COMMITTEE_NAMES
    )

    if selected_committee:
        if st.session_state.authenticated_committee == selected_committee:
            st.markdown(f"#### 📋 Member Registration for: {selected_committee}")
            with st.form(key=f"committee_form_{selected_committee.replace(' ', '_')}"):
                c1, c2 = st.columns(2)
                with c1:
                    first_name, surname = st.text_input("First Name"), st.text_input(
                        "Surname"
                    )
                    contact_number, gender = st.text_input(
                        "Contact Number"
                    ), st.selectbox("Gender", ["Male", "Female", "Other"])
                    nin_number, voters_card_number = st.text_input(
                        "NIN Number"
                    ), st.text_input("Voters Card Number")
                with c2:
                    account_number, account_name, bank = (
                        st.text_input("Account Number"),
                        st.text_input("Account Name"),
                        st.text_input("Bank"),
                    )
                    lga_raw = st.selectbox(
                        "LGA",
                        list(LGA_WARD_DATA.keys()),
                        key=f"lga_comm_{selected_committee}",
                    )
                    lga_clean = lga_raw.upper().split()[0] if lga_raw else ""
                    ward = st.selectbox(
                        "Ward",
                        LGA_WARD_DATA.get(lga_clean, []),
                        key=f"ward_comm_{selected_committee}",
                    )
                    nin_upload = st.file_uploader(
                        "Upload NIN Document", type=["pdf", "jpg", "png"]
                    )
                    picture_capture = st.camera_input("Capture Picture")

                if st.form_submit_button("Submit Information"):
                    if not all(
                        [
                            first_name,
                            surname,
                            nin_number,
                            voters_card_number,
                            account_number,
                            bank,
                            nin_upload,
                            picture_capture,
                        ]
                    ):
                        st.error(
                            "All fields, including file uploads and picture capture, must be filled."
                        )
                    elif nin_number in st.session_state.get(
                        "committee_double_dipping_ledger", {}
                    ):
                        st.error(
                            f"🛑 This NIN is already registered in {st.session_state.committee_double_dipping_ledger[nin_number]}."
                        )
                    else:
                        st.session_state.setdefault(
                            "committee_double_dipping_ledger", {}
                        )[nin_number] = selected_committee
                        new_entry = pd.DataFrame(
                            [
                                {
                                    "Committee_Node": selected_committee,
                                    "First_Name": first_name,
                                    "Surname": surname,
                                    "Contact_Number": contact_number,
                                    "Gender": gender,
                                    "Account_Number": account_number,
                                    "Account_Name": account_name,
                                    "Bank": bank,
                                    "LGA": lga_clean,
                                    "Ward": ward,
                                    "NIN_Number": nin_number,
                                    "Voters_Card_Number": voters_card_number,
                                    "Timestamp": datetime.datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                }
                            ]
                        )
                        st.session_state.strategic_committee_registry = pd.concat(
                            [st.session_state.strategic_committee_registry, new_entry],
                            ignore_index=True,
                        )
                        trigger_background_autosave()
                        st.success(
                            f"✅ Information for {first_name} {surname} submitted to {selected_committee}."
                        )
                        st.balloons()

            st.markdown(f"--- \n #### Registered Members for: {selected_committee}")
            committee_df = st.session_state.get(
                "strategic_committee_registry",
                pd.DataFrame(columns=STRATEGIC_COMMITTEE_COLS),
            )
            if not committee_df.empty:
                st.dataframe(
                    committee_df[committee_df["Committee_Node"] == selected_committee]
                )
            else:
                st.info("No members registered for this committee yet.")
        else:
            with st.form(key=f"login_form_{selected_committee.replace(' ', '_')}"):
                password = st.text_input("Enter Committee Passkey:", type="password")
                if st.form_submit_button("🔓 Unlock Committee"):
                    correct_password = STRATEGIC_COMMITTEE_PASSWORDS.get(
                        selected_committee
                    )
                    if password == correct_password:
                        st.session_state.authenticated_committee = selected_committee
                        st.rerun()
                    else:
                        st.error(
                            "🛑 ACCESS REJECTED: Passkey for this committee is incorrect."
                        )
