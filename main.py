import streamlit as st
import datetime
import time
import pandas as pd

from styling import apply_styling
from utils import initialize_and_recover_system_states, trigger_background_autosave
from registry import LGA_WARD_DATA
from ui_modules import render_marquee_header, render_mace_flash
from panels import supervisor_panel, agent_panel, main_dashboard

# ==============================================================================
# INITIALIZATION
# ==============================================================================
apply_styling()
initialize_and_recover_system_states()

# ==============================================================================
# DATABASE CONNECTION
# ==============================================================================

# Initialize connection.
# conn = st.connection("supabase", type=SupabaseConnection)
conn = None  # Mock connection

# ==============================================================================
# PAGE ROUTING
# ==============================================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "skill_form"

if st.session_state.get("adm_v30_auth") == "ali 2027":
    st.session_state.current_page = "main_dashboard"
elif st.session_state.get("sup_v30_auth_sidebar") == "ali 2027":
    st.session_state.current_page = "supervisor_panel"
elif st.session_state.get("agt_v30_auth_sidebar") == "ali 2027":
    st.session_state.current_page = "agent_panel"

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    if st.session_state.radar_threat:
        st.markdown(
            f'<div class="radar-sticky-threat">🚨 SECURITY WARNING: IDENTITY DUPLICATION COLLISION<br>{st.session_state.threat_msg}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="admin-launch-zone">', unsafe_allow_html=True)
    adm_key = st.text_input("COMMAND HUB KEY", type="password", key="adm_v30_auth")
    st.markdown(
        '<a href="https://web.facebook.com/hon.isa.ali.jc/?_rdc=1&_rdr#" target="_blank" class="inst-link-box">🌐 Hon. Ali Isa JC Official Facebook</a>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("🛠️ SKILL VOCATION POOL", key="btn_skill"):
        st.session_state.current_page = "skill_form"
    if st.button("🎓 STUDENT SCHOLARSHIP/GRANT", key="btn_sch"):
        st.session_state.current_page = "scholarship_form"
    if st.button("📦 CONSTITUENT PALLIATIVE ENROLLMENT", key="btn_pal"):
        st.session_state.current_page = "palliative_gateway"
    if st.button("🚀 CV & ARTISAN VAULT", key="btn_cv"):
        st.session_state.current_page = "cv_vault"

    st.markdown(
        '<div class="sidebar-red-flash">🚨 COMMUNITY URGENT NEED</div>',
        unsafe_allow_html=True,
    )
    if st.button("TRIGGER REGISTRATION INTERFACE", key="btn_cun_redirect"):
        st.session_state.current_page = "cun_trigger"

    if st.sidebar.button("Activate Prestige Aura"):
        render_mace_flash("assets/mace.png")

    st.divider()
    st.divider()
    st.markdown(
        "<p style='color:#8B0000; font-weight:bold; text-transform: uppercase;'>🔒 Field Authentication Core</p>",
        unsafe_allow_html=True,
    )

    sup_key_input = st.text_input(
        "WARD SUPERVISOR KEY", type="password", key="sup_v30_auth_sidebar"
    )
    agt_key_input = st.text_input(
        "POLLING UNIT AGENT KEY", type="password", key="agt_v30_auth_sidebar"
    )

    if sup_key_input:
        st.text_area(
            "Supervisor Remarks/Field Observations",
            key="sup_remarks",
            placeholder="Field log entry space...",
        )
    if agt_key_input:
        st.text_area(
            "Agent Remarks/Field Observations",
            key="agt_remarks",
            placeholder="Unit log entry space...",
        )

    st.caption(f"Engine: v34.0.73-BILLIRI-BALANGA | {datetime.date.today()}")

# ==============================================================================
# PAGE RENDERING
# ==============================================================================
if st.session_state.current_page == "supervisor_panel":
    supervisor_panel()
elif st.session_state.current_page == "agent_panel":
    agent_panel()
elif st.session_state.current_page == "main_dashboard":
    main_dashboard(conn)
elif st.session_state.current_page == "skill_form":
    render_marquee_header()
    st.markdown(
        '<div class="white-registry-header">🛠 CONSTITUENT SKILL EMPOWERMENT POOL</div>',
        unsafe_allow_html=True,
    )
    with st.form("skill_form_engine"):
        k1, k2 = st.columns(2)
        with k1:
            sv_name = st.text_input("Full name as displayed on NIN")
            sv_phone = st.text_input("Applicant Contact Number")
            sv_nin = st.text_input("Your NIN number")
            sv_vin = st.text_input("your Voters card number")
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
            klga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            kward = st.selectbox("Your Ward", LGA_WARD_DATA.get(klga, []))
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
            custom_vocation = ""
            if sv_selection == "Other (Type Custom Vocation Below)":
                custom_vocation = st.text_input(
                    "Type Your Choice Vocation Natively Here"
                )
            st.divider()
            sv_palliative_check = st.selectbox(
                "Have you received a palliative from this office before?", ["No", "Yes"]
            )

        sv_stmt = st.text_area("Candidate Skill Interest Statement Details")
        sv_cam = st.camera_input("Biometric Security Verification Core Scan")

        if st.form_submit_button("🚀 COMMIT APPLICATION TO TRAINING POOLS"):
            if (
                not sv_name
                or not sv_phone
                or not sv_nin
                or not sv_vin
                or not sv_stmt
                or sv_file is None
                or sv_cam is None
                or (
                    sv_selection == "Other (Type Custom Vocation Below)"
                    and not custom_vocation
                )
            ):
                st.error(
                    "🛑 FORM ERROR: All field entries on this registration pool form are strictly mandatory. Uploads and biometric camera checks must be valid."
                )
            else:
                match_check = st.session_state.global_registry[
                    st.session_state.global_registry["NIN"] == sv_nin
                ]
                if not match_check.empty:
                    st.session_state.radar_threat = True
                    st.session_state.threat_msg = f"Collision: NIN [{sv_nin}] matches a record belonging to user [{match_check.iloc[0]['Name']}]."
                    st.error(
                        "Duplicate Entry Detected. Entry Rejected by Security System Shield Protocols."
                    )
                else:
                    final_skill = (
                        custom_vocation
                        if sv_selection == "Other (Type Custom Vocation Below)"
                        else sv_selection
                    )
                    new_profile_row = {
                        "NIN": sv_nin,
                        "VIN": sv_vin,
                        "Name": sv_name,
                        "LGA": klga,
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
                        "Leader_Name": "Hon. Ali Isa JC Vouched",
                        "Leader_Contact": "080",
                        "Leader_NIN": "000",
                        "Leader_LGA": "BILLIRI",
                        "Leader_Ward": "CENTRAL",
                        "Leader_Portfolio": "Directorate Node",
                        "Voucher_Code": "V-GMB",
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
                    st.success("Thanks for your submission! You are appreciated.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()

elif st.session_state.current_page == "scholarship_form":
    render_marquee_header()
    st.markdown("### 🎓 CONSTITUENT STUDENT SCHOLARSHIP APPLICATION PORTAL")
    with st.form("scholarship_form_engine"):
        s1, s2 = st.columns(2)
        with s1:
            sch_name = st.text_input("Full name as displayed on NIN")
            sch_nin = st.text_input("Your NIN number")
            sch_phone = st.text_input("Applicant Contact Number")
            sch_year = st.selectbox(
                "Academic Year of Intake Admission",
                [str(year_token) for year_token in range(2018, 2027)],
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
            slga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            sward = st.selectbox("Your Ward", LGA_WARD_DATA.get(slga, []))
        sch_file_adm = st.file_uploader(
            "Attach Official University Admission Letter Asset File",
            type=["pdf", "jpg", "png"],
        )
        sch_just = st.text_area("Applicant Justification Space")
        sch_cam = st.camera_input("Capture Student Identity Card Sensor")

        if st.form_submit_button("🚀 SUBMIT SCHOLARSHIP ENTRY APPLICATION PARAMETERS"):
            if (
                not sch_name
                or not sch_nin
                or not sch_phone
                or not sch_inst
                or not sch_just
                or sch_file_nin is None
                or sch_file_adm is None
                or sch_cam is None
            ):
                st.error(
                    "🛑 FORM ERROR: Absolute processing requirement failed. All input fields, historical assets, and live card capture parameters are required."
                )
            else:
                st.success("Thanks for your submission! You are appreciated.")
                st.balloons()

elif st.session_state.current_page == "cv_vault":
    render_marquee_header()
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
            vlga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            vward = st.selectbox("Your Ward", LGA_WARD_DATA.get(vlga, []))
        cv_summary = st.text_area(
            "Summary Matrix of Functional Career Experience Vectors"
        )
        cv_cam = st.camera_input("Capture Valid Professional Certification Seals")

        if st.form_submit_button(
            "📤 COMMIT CREDENTIALS STRINGS TO TALENT PLATFORM ARCHIVE MATRIX"
        ):
            if (
                not cv_name
                or not cv_nin
                or not cv_phone
                or not cv_summary
                or cv_file is None
                or cv_cam is None
            ):
                st.error(
                    "🛑 FORM ERROR: System cannot commit strings. Please completely populate all input arrays and provide file/camera captures."
                )
            else:
                st.success("Thanks for your submission! You are appreciated.")
                st.balloons()

elif st.session_state.current_page == "cun_trigger":
    render_marquee_header()
    st.markdown("### 🚨 COMMUNITY URGENT NEED FIELD DEFICIT REPORT GATEWAY")
    with st.form("cun_form_engine"):
        cun_member = st.text_input("Reporting Community member")
        cun_phone = st.text_input("Applicant Contact Number")
        clga = st.selectbox("Affected LGA", list(LGA_WARD_DATA.keys()))
        cward = st.selectbox("Affected Ward", LGA_WARD_DATA.get(clga, []))
        cun_area = st.selectbox(
            "Area of urgent government Attention",
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

        if st.form_submit_button(
            "🚨 TRIGGER COMMAND INCIDENT VECTOR ALERT TO CORE MASTER LEDGERS"
        ):
            if (
                not cun_member
                or not cun_phone
                or not cun_logs
                or cun_file is None
                or cun_cam is None
            ):
                st.error(
                    "🛑 FORM ERROR: Core matrix validation failed. Satisfy all reporting details, identification files, and site images."
                )
            else:
                st.success("Thanks for your submission! You are appreciated.")
                st.balloons()

else:
    render_marquee_header()
    st.markdown("### 📦 CONSTITUENT PALLIATIVE ENROLLMENT REGISTRY")
    with st.form("palliative_form_engine"):
        p1, p2 = st.columns(2)
        with p1:
            p_name = st.text_input("Full name as displayed on NIN")
            p_nin = st.text_input("Your NIN number")
            p_vin = st.text_input("your Voters card number")
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
            plga = st.selectbox("Your LGA", list(LGA_WARD_DATA.keys()))
            pward = st.selectbox("Your Ward", LGA_WARD_DATA.get(plga, []))
            p_agro_select = st.selectbox(
                "Specific Area of Agro Intervention and Others",
                ["Fertilizer", "Seedlings", "Other Area of Likely Intervention"],
            )
            p_expect = st.text_input("Type Your Expectation")

        st.divider()
        st.markdown(
            "### 🛡️ FULL STRATEGIC LEADERSHIP VOUCHING TIER INTERFACE FRAME (ANTI-FRAUD MATRIX)"
        )
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            v_leader = st.text_input("Vouching Community Leader Full Legal Name")
            v_lphone = st.text_input(
                "Vouching Leader Mobile Communication Contact Phone"
            )
            v_lnin = st.text_input(
                "Vouching Leader National ID Validation String (NIN)"
            )
            vl_lga = st.selectbox(
                "Vouching Leader LGA Registration Link", list(LGA_WARD_DATA.keys())
            )
        with v_col2:
            vl_ward = st.selectbox(
                "Vouching Leader Ward Area Code Linking Check (Auto)",
                LGA_WARD_DATA.get(vl_lga, []),
            )
            v_port = st.text_input(
                "Current Portfolio/Traditional Leadership Title Stamped Within Community"
            )
            v_file_leader = st.file_uploader(
                "Upload Vouching Leader Authentic NIN Verification Slip Document File",
                type=["pdf", "jpg", "png"],
            )

        p_remarks = st.text_area(
            "Leader Affirmation Testimony Verification Remarks Statement"
        )
        p_cam = st.camera_input(
            "Biometric Face Capture Matrix Core Verification Face Scan"
        )

        if st.form_submit_button(
            "🚀 COMPLETE TRANSACTION: AUTHORIZE PALLIATIVE NOMINATION RECORD"
        ):
            if (
                not p_name
                or not p_nin
                or not p_vin
                or not p_phone
                or not p_expect
                or not p_vuln
                or not v_leader
                or not v_lphone
                or not v_lnin
                or not v_port
                or not p_remarks
                or p_file_nin is None
                or v_file_leader is None
                or p_cam is None
            ):
                st.error(
                    "🛑 FORM ERROR: Enrollment verification failed. All fields, agro specifications, physical identity files, and live camera captures are required."
                )
            else:
                match_check = st.session_state.global_registry[
                    st.session_state.global_registry["NIN"] == p_nin
                ]
                if not match_check.empty:
                    st.session_state.radar_threat = True
                    st.session_state.threat_msg = f"Collision Trace Block: Identification NIN Token [{p_nin}] already allocated inside database system matrix arrays."
                    st.error(
                        "Duplicate Registration Attempt Dropped Instantly. Verification Engine Locked Transaction Block."
                    )
                else:
                    new_profile_row = {
                        "NIN": p_nin,
                        "VIN": p_vin,
                        "Name": p_name,
                        "LGA": plga,
                        "Ward": pward,
                        "Status": "Verified Clear",
                        "Category": "Applicant",
                        "Skill_Interest": f"Agro: {p_agro_select}",
                        "Custom_Skill": p_expect,
                        "Gender": "Not Specified",
                        "DOB": "Not Specified",
                        "Disability_Status": ", ".join(p_vuln),
                        "Prior_Palliative": "Yes",
                        "Academic_Qual": "None",
                        "Admission_Year": "2026",
                        "Admission_Letter": None,
                        "Phone": p_phone,
                        "Leader_Name": v_leader,
                        "Leader_Contact": v_lphone,
                        "Leader_NIN": v_lnin,
                        "Leader_LGA": vl_lga,
                        "Leader_Ward": vl_ward,
                        "Leader_Portfolio": v_port,
                        "Voucher_Code": "P-GMB",
                        "Remarks": p_remarks,
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
                    st.success("Thanks for your submission! You are appreciated.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
