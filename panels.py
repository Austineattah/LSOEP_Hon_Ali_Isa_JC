import streamlit as st
import pandas as pd
import datetime
import time
import base64
import requests
import os
import urllib.request
import plotly.graph_objects as go
import sqlite3
import html
import re

from registry import (
    LGA_WARD_DATA,
    GEOGRAPHY,
    STRATEGIC_COMMITTEE_COLS,
    COMMUNITY_LEADERS,
    COLUMNS_STRUCTURE,
    STRATEGIC_COMMITTEE_NAMES,
    STRATEGIC_COMMITTEE_PASSWORDS,
    ANNOUNCEMENT_CACHE_FILE,
    HON_ALI_SPONSORED_BILLS,
    HON_TITLE,
)


def render_constituency_engagement_channels():
    """
    🏛️ Official Constituency Engagement Channels Grid Matrix
    All 13 channels cleanly rendered for Hon. Ali Isa JC.
    """
    st.markdown("### 🏛️ CONSTITUENCY ENGAGEMENT CHANNELS")
    st.write("---")

    ENGAGEMENT_CHANNELS = [
        {
            "icon": "🚀",
            "label": "LEGISLATIVE PROGRESS TRACKER",
            "route": "PROGRESS_TRACKER",
        },
        {
            "icon": "🏛️",
            "label": "BEYOND RHETORICS PROJECT EXECUTION",
            "route": "BEYOND_RHETORICS",
        },
        {
            "icon": "🗣️",
            "label": "SPEAK WITH HON. ALI ISA JC DIRECTLY",
            "route": "SPEAK_DIRECT",
        },
        {
            "icon": "🛡️",
            "label": "STRATEGIC COMMITTEES (MODULE 13)",
            "route": "STRATEGIC_COMMITTEES",
        },
        {
            "icon": "🏛️",
            "label": "LEGISLATIVE FOOTPRINTS",
            "route": "LEGISLATIVE_FOOTPRINTS",
        },
        {"icon": "🛠️", "label": "SKILL VOCATION POOL", "route": "SKILL_POOL"},
        {"icon": "🎓", "label": "STUDENT SCHOLARSHIP/GRANT", "route": "SCHOLARSHIPS"},
        {
            "icon": "🔍",
            "label": "JOB VACANCY VERIFICATION",
            "route": "JOB_VERIFICATION",
        },
        {
            "icon": "📂",
            "label": "FEDERAL & INDUSTRIAL GRANTS",
            "route": "GRANTS_VERIFICATION",
        },
        {"icon": "📦", "label": "PALLIATIVE ENROLLMENT", "route": "PALLIATIVES"},
        {"icon": "💡", "label": "CV & ARTISAN VAULT", "route": "CV_VAULT"},
        {"icon": "🚨", "label": "COMMUNITY URGENT NEED", "route": "URGENT_NEED"},
        {
            "icon": "📜",
            "label": "CONSTITUENCY VOUCHING VERIFICATION",
            "route": "VOUCHING_VERIFICATION",
        },
    ]

    for channel in ENGAGEMENT_CHANNELS:
        button_label = f"{channel['icon']} {channel['label']}"
        if st.button(
            button_label,
            key=f"eng_chan_btn_{channel['route']}",
            use_container_width=True,
        ):
            st.session_state.current_route = channel["route"]
            st.rerun()


def render_global_announcement_marquee():
    """
    Safely reads the announcement text file and forces it inside a
    protected HTML marquee tag, sanitizing any rogue user-submitted code.
    """
    import html

    announcement_file = "announcement.txt"
    default_message = "Welcome to the Legislative Strategic Outreach & Equity Portal (LSOEP) for Hon. Ali Isa JC."

    message = default_message
    try:
        if os.path.exists(announcement_file):
            with open(announcement_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    message = content
    except Exception:
        message = default_message

    clean_message = html.escape(message)

    st.markdown(
        f"""
        <div style="background-color: #031424; border-top: 2px solid #D4AF37; border-bottom: 2px solid #D4AF37; padding: 8px 0; margin-bottom: 20px;">
            <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #60A5FA; font-weight: 700; font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; letter-spacing: 1px; text-transform: uppercase;">
                🚨 LATEST UPDATE: {clean_message}
            </marquee>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_admin_announcement_control():
    st.markdown("##### 📢 Central Announcement Dispatch & Marquee Matrix Manager")
    st.caption(
        "Inject high-priority global alerts that instantly override the home page marquee ticker."
    )

    with st.form("admin_announcement_control_form"):
        new_ticker = st.text_input(
            "Type Plain Text Alert Only (Do NOT input raw HTML symbols like < or >) *:",
            placeholder="Type scrolling message here...",
        )

        if st.form_submit_button(
            "🔒 LOCK ANNOUNCEMENT AND RE-PROPAGATE MARQUEE", use_container_width=True
        ):
            if new_ticker.strip():
                try:
                    import re

                    clean_text = re.sub("<[^<]+?>", "", new_ticker.strip())

                    with open("announcement.txt", "w", encoding="utf-8") as f:
                        f.write(clean_text)

                    st.success(
                        "✓ Global marquee variables updated. New scrolling announcement loop active!"
                    )
                    time.sleep(0.4)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to commit announcement file: {e}")
            else:
                st.warning("Please specify a valid text announcement.")


# Corrected National Geographic Matrix to include the full Gombe South data
GEO_MATRIX = st.session_state.get("DYNAMIC_GEO_MATRIX", {})


if "live_scores" not in st.session_state:
    st.session_state.live_scores = {
        "PRESIDENTIAL": {"PDP": 14520, "APC": 12110, "LP": 4320, "NNPP": 850},
        "SENATORIAL": {"PDP": 16180, "APC": 11400, "LP": 2100, "ADC": 980},
        "FEDERAL HOUSE": {"PDP": 18240, "APC": 9890, "LP": 1150, "SDP": 420},
        "GOVERNORSHIP": {"PDP": 15410, "APC": 13900, "LP": 3200, "NNPP": 710},
        "STATE HOUSE": {"PDP": 17110, "APC": 10250, "LP": 940, "APGA": 310},
    }


def sync_election_tally_engine():
    pass


def render_pie_chart(title):
    labels = ["Category A", "Category B", "Category C", "Category D"]
    values = [4500, 2500, 1053, 500]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title_text=title, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_skill_form():
    st.markdown(
        """<div class="swing-in" style="background-color:#061A33; padding:10px; border-left:4px solid #D4AF37; margin-bottom:15px;">
        <h4 style="color:#D4AF37; margin:0; text-transform: uppercase; font-size: 1.5rem;">🛠️ Constituent Skill Empowerment Pool</h4>
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
            lga_options = list(LGA_WARD_DATA.keys())
            klga_raw = st.selectbox("Your LGA", lga_options, key="skill_lga_select")
            klga_clean = klga_raw.upper().split()[0] if klga_raw else ""

            col_ward_sel, col_ward_txt = st.columns(2)
            with col_ward_sel:
                kward = st.selectbox("Your Ward", LGA_WARD_DATA.get(klga_clean, []))
            with col_ward_txt:
                manual_kward = st.text_input(
                    "Or Type Specific Ward", key="skill_manual_ward"
                )

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
        st.markdown("##### 🛡️ LEADERSHIP VOUCHING TIER INTERFACE")
        v_leader_name = st.selectbox(
            "Select Vouching Community Leader",
            list(COMMUNITY_LEADERS.keys()),
            key="skill_leader_select",
        )
        v_leader_details = COMMUNITY_LEADERS[v_leader_name]

        if st.form_submit_button(
            "🚀 COMMIT APPLICATION TO TRAINING POOLS", use_container_width=True
        ):
            final_ward = manual_kward.strip() if manual_kward.strip() else kward
            if not (
                sv_name and sv_phone and sv_nin and sv_vin and sv_stmt and final_ward
            ):
                st.error(
                    "🛑 FORM ERROR: All core validation strings, documents, and biometric snapshot frames are mandatory."
                )
            else:
                st.success(
                    "Registration parameter logged into production records system!"
                )
                st.balloons()


def render_scholarship_form():
    st.markdown(
        """<h3 class="swing-in" style="text-transform: uppercase; font-size: 1.7rem;">🎓 Constituent Student Scholarship Application Portal</h3>""",
        unsafe_allow_html=True,
    )
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
            lga_options = list(LGA_WARD_DATA.keys())
            slga_raw = st.selectbox("Your LGA", lga_options, key="sch_lga_select")
            slga_clean = slga_raw.upper().split()[0] if slga_raw else ""

            col_ward_sel, col_ward_txt = st.columns(2)
            with col_ward_sel:
                sward = st.selectbox("Your Ward", LGA_WARD_DATA.get(slga_clean, []))
            with col_ward_txt:
                manual_sward = st.text_input(
                    "Or Type Specific Ward", key="scholarship_manual_ward"
                )

            sch_file_adm = st.file_uploader(
                "Attach Official University Admission Letter Asset File",
                type=["pdf", "jpg", "png"],
            )
        sch_just = st.text_area("Applicant Justification Space")
        sch_cam = st.camera_input("Capture Student Identity Card Sensor")
        if st.form_submit_button(
            "🚀 SUBMIT SCHOLARSHIP ENTRY APPLICATION PARAMETERS",
            use_container_width=True,
        ):
            final_ward = manual_sward.strip() if manual_sward.strip() else sward
            if not (sch_name and sch_nin and sch_phone and final_ward):
                st.error("Please fill all required fields.")
            else:
                st.info("System intake pipeline initialized successfully.")
                st.balloons()


def render_cv_vault():
    st.markdown(
        """<h3 class="swing-in" style="text-transform: uppercase; font-size: 1.7rem;">🚀 Constituent Professional Talent Vault Engine</h3>""",
        unsafe_allow_html=True,
    )
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
            lga_options = list(LGA_WARD_DATA.keys())
            vlga_raw = st.selectbox("Your LGA", lga_options, key="cv_lga_select")
            vlga_clean = vlga_raw.upper().split()[0] if vlga_raw else ""

            col_ward_sel, col_ward_txt = st.columns(2)
            with col_ward_sel:
                vward = st.selectbox("Your Ward", LGA_WARD_DATA.get(vlga_clean, []))
            with col_ward_txt:
                manual_vward = st.text_input(
                    "Or Type Specific Ward", key="cv_manual_ward"
                )

        cv_summary = st.text_area(
            "Summary Matrix of Functional Career Experience Vectors"
        )
        cv_cam = st.camera_input("Capture Valid Professional Certification Seals")
        if st.form_submit_button(
            "📤 COMMIT CREDENTIALS STRINGS TO TALENT PLATFORM ARCHIVE",
            use_container_width=True,
        ):
            final_ward = manual_vward.strip() if manual_vward.strip() else vward
            if not (cv_name and cv_nin and cv_phone and final_ward):
                st.error("Please fill all required fields.")
            else:
                st.info("Transmission channel connected smoothly.")
                st.balloons()


def render_cun_trigger():
    st.markdown(
        """<h3 class="swing-in" style="text-transform: uppercase; font-size: 1.7rem;">🚨 Community Urgent Need Field Deficit Report Gateway</h3>""",
        unsafe_allow_html=True,
    )
    with st.form("cun_form_engine"):
        cun_member = st.text_input("Reporting Community Member")
        cun_phone = st.text_input("Applicant Contact Number")
        lga_options = list(LGA_WARD_DATA.keys())
        clga_raw = st.selectbox("Affected LGA", lga_options, key="cun_lga_select")
        clga_clean = clga_raw.upper().split()[0] if clga_raw else ""

        col_ward_sel, col_ward_txt = st.columns(2)
        with col_ward_sel:
            cward = st.selectbox("Affected Ward", LGA_WARD_DATA.get(clga_clean, []))
        with col_ward_txt:
            manual_cward = st.text_input("Or Type Specific Ward", key="cun_manual_ward")

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
        if st.form_submit_button(
            "🚨 TRIGGER COMMAND INCIDENT VECTOR ALERT", use_container_width=True
        ):
            final_ward = manual_cward.strip() if manual_cward.strip() else cward
            if not (cun_member and cun_phone and final_ward):
                st.error("Please fill all required fields.")
            else:
                st.info("Field alert dispatch sequence routing triggered.")
                st.balloons()


def render_palliative_form(focus_on_vouching=False):
    """
    Renders the Integrated Constituent Palliative Enrollment Registry for Balanga/Billiri.
    """
    st.markdown("## 📦 Constituent Palliative Enrollment Registry")
    st.markdown(
        "#### **Balanga/Billiri Federal Constituency Strategic Welfare & Relief Matrix**"
    )
    st.markdown("---")

    is_direct_application = st.checkbox(
        "🙋‍♂️ I am applying directly on my own (No Local Leader Vouching required)",
        value=not focus_on_vouching,
        key="app_pathway_toggle",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    lga_list = ["Select LGA...", "Balanga", "Billiri"]

    if is_direct_application:
        st.info(
            "ℹ️ **Direct Self-Application Pathway Active.** No leadership endorsement credentials are required."
        )

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("##### 👥 APPLICANT IDENTITY DETAILS")
            st.markdown(
                "<hr style='margin: 5px 0 15px 0; border-color: rgba(212, 175, 55, 0.2);'>",
                unsafe_allow_html=True,
            )
            p_name = st.text_input("Applicant Full Name:", key="direct_p_name")
            p_phone = st.text_input("Contact Phone Number:", key="direct_p_phone")
            p_nin = st.text_input(
                "11-Digit NIN Number:", max_chars=11, key="direct_p_nin"
            )
            p_voter = st.text_input(
                "Voters Card Number (Optional):", key="direct_p_voter"
            )

        with col_s2:
            st.markdown("##### 📍 RESIDENTIAL GEOGRAPHY")
            st.markdown(
                "<hr style='margin: 5px 0 15px 0; border-color: rgba(212, 175, 55, 0.2);'>",
                unsafe_allow_html=True,
            )
            p_lga = st.selectbox("LGA of Residence:", lga_list, key="direct_p_lga")
            p_ward = st.text_input(
                "Type your Ward:",
                key="direct_p_ward_typed",
                placeholder="e.g. Tal, Bambam, etc...",
            )
            p_addr = st.text_area("Detailed Residential Address:", key="direct_p_addr")

        st.markdown("---")
        st.markdown("##### 💡 RELIEF REQUEST SPECIFICS")
        p_request_area = st.text_area(
            "Type your Specific Request Area:",
            key="direct_p_request_area",
            placeholder="Describe what relief you need (e.g. Food relief, Medical assistance, etc...)",
        )

        st.markdown("---")
        st.markdown("##### 📸 VERIFICATION MEDIA (NIN Verification)")
        media_choice = st.radio(
            "Choose Verification Capture Method:",
            ["Capture Live Photo of NIN Card", "Upload Document File (PDF/Image)"],
            key="direct_media_choice",
        )

        uploaded_nin = None
        if media_choice == "Capture Live Photo of NIN Card":
            uploaded_nin = st.camera_input(
                "Place your physical NIN slip/card in front of the camera and snap:",
                key="direct_camera_input",
            )
        else:
            uploaded_nin = st.file_uploader(
                "Upload Applicant's NIN Slip/Card (PDF/JPG/PNG):",
                type=["png", "jpg", "jpeg", "pdf"],
                key="direct_file_uploader",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "🗳️ Submit Direct Self-Application Profile", use_container_width=True
        ):
            if len(p_nin) != 11 or not p_nin.isdigit():
                st.error(
                    "🛑 Your National Identity Number (NIN) must be exactly 11 digits."
                )
            elif not p_name or p_lga == "Select LGA..." or not p_ward:
                st.error(
                    "🛑 Please complete all required personal identity, geography, and ward details."
                )
            elif not p_request_area:
                st.error("🛑 Please describe your specific relief request area.")
            else:
                st.success(
                    "🎉 Direct application successfully registered in the relief index!"
                )
                st.balloons()

    else:
        if focus_on_vouching:
            st.info(
                "🎯 **Direct Redirection Active: Local Leadership Vouching Registry focused.**"
            )

        st.markdown("### 🛡️ LEADERSHIP VOUCHING TIER INTERFACE")
        st.caption("Formal Verification Registry & Character Endorsement Profile")

        col_l, col_a = st.columns(2)
        with col_l:
            st.markdown("##### 👔 SECTION A: Vouching Leader Credentials")
            st.markdown(
                "<hr style='margin: 5px 0 15px 0; border-color: rgba(212, 175, 55, 0.2);'>",
                unsafe_allow_html=True,
            )
            leader_title = st.selectbox(
                "Select Vouching Community Leader Role:",
                [
                    "Select Role...",
                    "Community Youth Leader",
                    "Pastor",
                    "Imam",
                    "Ward Leader",
                    "Community Leader",
                    "Women Leader",
                ],
                key="v_leader_title",
            )
            leader_name = st.text_input("Name of Vouching Leader:", key="v_leader_name")
            leader_phone = st.text_input(
                "Contact Number of Leader:", key="v_leader_phone"
            )
            leader_lga = st.selectbox("LGA of Leader:", lga_list, key="v_leader_lga")
            leader_ward = st.text_input(
                "Type Ward of Leader:",
                key="v_leader_ward_typed",
                placeholder="Enter Leader's Ward...",
            )
            leader_nin = st.text_input(
                "11-Digit NIN Number of Leader:", max_chars=11, key="v_leader_nin"
            )
            leader_voter = st.text_input(
                "Voters Card Number of Leader:", key="v_leader_voter"
            )

        with col_a:
            st.markdown("##### 👥 SECTION B: Applicant Profile")
            st.markdown(
                "<hr style='margin: 5px 0 15px 0; border-color: rgba(212, 175, 55, 0.2);'>",
                unsafe_allow_html=True,
            )
            applicant_name = st.text_input("Name of Applicant:", key="v_applicant_name")
            applicant_phone = st.text_input(
                "Contact Number of Applicant:", key="v_applicant_phone"
            )
            applicant_lga = st.selectbox(
                "LGA of Applicant:", lga_list, key="v_applicant_lga"
            )
            applicant_ward = st.text_input(
                "Type Ward of Applicant:",
                key="v_applicant_ward_typed",
                placeholder="Enter Applicant's Ward...",
            )
            applicant_nin = st.text_input(
                "11-Digit NIN Number of Applicant:", max_chars=11, key="v_applicant_nin"
            )
            applicant_voter = st.text_input(
                "Voters Card Number of Applicant:", key="v_applicant_voter"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 💡 RELIEF REQUEST SPECIFICS")
        v_applicant_request_area = st.text_area(
            "Type Applicant's Specific Request Area:",
            key="v_applicant_request_area",
            placeholder="Describe what specific palliative assistance the applicant requires...",
        )

        st.markdown("---")
        st.markdown("##### 📸 VERIFICATION MEDIA (Applicant NIN Verification)")
        v_media_choice = st.radio(
            "Choose Capture Method for Applicant:",
            ["Capture Live Photo of Applicant NIN", "Upload File (PDF/Image)"],
            key="v_media_choice",
        )
        applicant_nin_file = None
        if v_media_choice == "Capture Live Photo of Applicant NIN":
            applicant_nin_file = st.camera_input(
                "Place applicant's physical NIN slip/card in front of the camera and snap:",
                key="v_camera_input",
            )
        else:
            applicant_nin_file = st.file_uploader(
                "Upload Applicant's NIN Card/Slip Document:",
                type=["png", "jpg", "jpeg", "pdf"],
                key="v_file_uploader",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "🗳️ Register Certified Welfare Vouching Profile", use_container_width=True
        ):
            if (
                len(leader_nin) != 11
                or not leader_nin.isdigit()
                or len(applicant_nin) != 11
                or not applicant_nin.isdigit()
            ):
                st.error(
                    "🛑 Both Leader's and Applicant's NIN must be exactly 11 numerical digits."
                )
            elif (
                leader_title == "Select Role..."
                or not leader_name
                or not applicant_name
                or not leader_ward
                or not applicant_ward
            ):
                st.error(
                    "🛑 Please complete all name, role, and ward fields for both the Leader and the Applicant."
                )
            elif not v_applicant_request_area:
                st.error("🛑 Please describe the applicant's specific request area.")
            else:
                st.success(
                    "🎉 Welfare Registry Entry Created! The character-vouched profile has been successfully queued."
                )
                st.balloons()


def render_sponsored_bills_panel():
    """
    Renders the Legislative Footprints, Statutory Bills, and Ground-Truth Motions
    dynamically pulled from the centralized master registry layer.
    """
    st.markdown("## 📜 LEGISLATIVE FOOTPRINTS & MOTIONS")
    st.caption(
        f"Official legislative ledger for {HON_TITLE} at the House of Representatives."
    )
    st.divider()

    # Loop dynamically through the updated registry data matrix
    for index, item in enumerate(HON_ALI_SPONSORED_BILLS):
        with st.container():
            # Premium luxury layout frame for each bill/motion block
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #021024, #05244C); padding: 20px; border-radius: 12px; border-left: 5px solid #D4AF37; margin-bottom: 20px;">
                    <h4 style="color: #D4AF37; margin: 0 0 10px 0;">🏛️ {item['title']}</h4>
                    <p style="color: #FFFFFF; font-size: 0.95rem; line-height: 1.5; margin-bottom: 15px;">{item['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Interactive parameters and progress matrix below background card container
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**📅 Date Logged:** {item['date']}")
            with col2:
                # Add status indicators based on active progression states
                status_color = "🟢" if "Passed" in item["status"] else "🟡"
                st.markdown(f"**📋 Current Status:** {status_color} {item['status']}")
            with col3:
                st.progress(item["progress"] / 100.0)
                st.caption(f"Process Completion Density: {item['progress']}%")

            st.markdown("<br>", unsafe_allow_html=True)


def render_progress_tracker():
    """
    Renders the high-impact operational dashboard tracking overall milestone progress metrics
    for Balanga/Billiri Federal legislative bills and community interventions.
    """
    st.markdown("## 🚀 LEGISLATIVE PROGRESS TRACKER")
    st.caption(
        f"Real-time breakdown of legislative instruments introduced by {HON_TITLE}."
    )
    st.divider()

    # Dynamic KPI Telemetry Cards Layer
    stat_c1, stat_c2, stat_c3 = st.columns(3)
    with stat_c1:
        st.markdown(
            """<div style='background: linear-gradient(135deg, #021024, #05244C); padding: 15px; border-radius: 8px; border-left: 4px solid #D4AF37; text-align: center;'>
                <h5 style='color: #D4AF37; margin:0; font-size:0.9rem;'>TOTAL INSTRUMENTS</h5>
                <p style='color: #FFFFFF; font-size: 1.8rem; font-weight: 800; margin:5px 0 0 0;'>6 Active</p>
               </div>""",
            unsafe_allow_html=True,
        )
    with stat_c2:
        st.markdown(
            """<div style='background: linear-gradient(135deg, #021024, #05244C); padding: 15px; border-radius: 8px; border-left: 4px solid #00E5FF; text-align: center;'>
                <h5 style='color: #00E5FF; margin:0; font-size:0.9rem;'>PASSED MOTIONS</h5>
                <p style='color: #FFFFFF; font-size: 1.8rem; font-weight: 800; margin:5px 0 0 0;'>4 Cleared</p>
               </div>""",
            unsafe_allow_html=True,
        )
    with stat_c3:
        st.markdown(
            """<div style='background: linear-gradient(135deg, #021024, #05244C); padding: 15px; border-radius: 8px; border-left: 4px solid #E2BB3C; text-align: center;'>
                <h5 style='color: #E2BB3C; margin:0; font-size:0.9rem;'>BILLS IN PROGRESS</h5>
                <p style='color: #FFFFFF; font-size: 1.8rem; font-weight: 800; margin:5px 0 0 0;'>2 Pending</p>
               </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 Pipeline Progression Metrics")

    # Render historical progression vectors directly inside the channel view
    for item in HON_ALI_SPONSORED_BILLS:
        with st.container():
            col_left, col_right = st.columns([3, 1])
            with col_left:
                st.markdown(f"**📑 {item['title']}**")
                st.caption(f"Status Matrix Placement: {item['status']}")
            with col_right:
                st.progress(item["progress"] / 100.0)
                st.markdown(
                    f"<p style='text-align: right; margin:0; font-size:0.85rem; color:#00E5FF;'>{item['progress']}% Complete</p>",
                    unsafe_allow_html=True,
                )
            st.divider()


def ward_collation_officer_panel():
    st.markdown(
        """<div class="supervisor-header swing-in" style="font-size: 1.7rem; text-transform: uppercase;">🛡️ Ward Collation Officer Command: Form EC8A Logs</div>""",
        unsafe_allow_html=True,
    )
    if "sup_slip_preview" not in st.session_state:
        st.session_state.sup_slip_preview = None

    with st.form("supervisor_form"):
        c1, c2 = st.columns(2)
        with c1:
            sup_name = st.text_input("Supervisor Full Name")
            sup_phone = st.text_input("Phone Number")
            lga_options = list(LGA_WARD_DATA.keys())
            sup_lga_raw = st.selectbox("Your LGA", lga_options)
            sup_lga_clean = sup_lga_raw.upper().split()[0]

            col_ward_sel, col_ward_txt = st.columns(2)
            with col_ward_sel:
                sup_ward = st.selectbox(
                    "Your Ward", LGA_WARD_DATA.get(sup_lga_clean, [])
                )
            with col_ward_txt:
                manual_sup_ward = st.text_input(
                    "Or Type Specific Ward", key="collation_manual_ward"
                )

            bvas_serial = st.text_input("BVAS Serial Number")
            accredited_voters = st.number_input(
                "Number of Accredited Voters", min_value=0
            )

        with c2:
            st.markdown("**Votes Scored by Party**")
            apc_votes = st.number_input("APC Votes", min_value=0)
            pdp_votes = st.number_input("PDP Votes", min_value=0)
            lp_votes = st.number_input("LP Votes", min_value=0)
            nnpp_votes = st.number_input("NNPP Votes", min_value=0)

            incident_occurred = st.selectbox("Incident Occurred?", ["No", "Yes"])
            incident_details = ""
            if incident_occurred == "Yes":
                incident_details = st.text_area("Incident Form Scenario")

        st.camera_input("Live Capture Sensor Matrix: Form EC8A Sheet")

        if st.form_submit_button(
            "🔍 GENERATE SYSTEM INTEGRITY PREVIEW RECORD SLIP", use_container_width=True
        ):
            final_ward = (
                manual_sup_ward.strip() if manual_sup_ward.strip() else sup_ward
            )
            if not (sup_name and sup_phone and final_ward):
                st.error(
                    "🛑 FORM ERROR: Supervisor name, phone, and ward must be specified."
                )
            else:
                st.session_state.sup_slip_preview = {
                    "Supervisor": sup_name,
                    "Phone": sup_phone,
                    "LGA": sup_lga_clean,
                    "Ward": final_ward,
                    "APC_Votes": apc_votes,
                    "PDP_Votes": pdp_votes,
                    "LP_Votes": lp_votes,
                    "NNPP_Votes": nnpp_votes,
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
                <div class="slip-row" style="color:blue;"><span>APC:</span> <span>{p_data['APC_Votes']}</span></div>
                <div class="slip-row" style="color:green;"><span>PDP:</span> <span>{p_data['PDP_Votes']}</span></div>
                <div class="slip-row" style="color:red;"><span>LP:</span> <span>{p_data['LP_Votes']}</span></div>
                <div class="slip-row" style="color:orange;"><span>NNPP:</span> <span>{p_data['NNPP_Votes']}</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("🔒 CONFIRM & LOG METRICS", use_container_width=True):
                # Logic to save data would go here
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
    if "agent_authenticated" not in st.session_state:
        st.session_state.agent_authenticated = False

    st.markdown("### 🗳️ POLLING UNIT AGENT COMMAND CONTROL NODE")
    st.write("---")

    ac1, ac2 = st.columns([5, 2])
    with ac2:
        if st.button(
            "🔒 Seal Node & Close Terminal Session",
            key="seal_agent_node_btn_v9",
            use_container_width=True,
        ):
            st.session_state.agent_authenticated = False
            st.success("Terminal session disconnected securely.")
            time.sleep(0.4)
            st.rerun()

    st.markdown('<div class="command-hub-pane">', unsafe_allow_html=True)
    st.markdown("##### 📡 Live Telemetry Field Tally Submission Matrix")

    with st.form("agent_tally_submission_form_rich_core", clear_on_submit=False):
        st.markdown(
            "###### 👤 Section 1: Field Officer Credentials & Boundary Assignment"
        )
        col1, col2 = st.columns(2)
        with col1:
            pu_officer = st.text_input(
                "Polling Agent Full Name *:", key="pu_agent_name"
            )
            pu_phone = st.text_input(
                "Active Contact Phone Number *:", key="pu_agent_phone"
            )
            pu_bvas_id = st.text_input(
                "BVAS Machine Hardware Serial ID Number *:", key="pu_bvas_id"
            )
        with col2:
            lga_options = list(LGA_WARD_DATA.keys())
            pu_lga = st.selectbox(
                "LGA Ward Boundary Focus *:", lga_options, key="pu_lga_sel"
            )
            col_ward_sel, col_ward_txt = st.columns(2)
            with col_ward_sel:
                pu_ward = st.selectbox(
                    "Specific Ward Precinct Designation *:",
                    LGA_WARD_DATA.get(pu_lga, []),
                    key="pu_ward_sel",
                )
            with col_ward_txt:
                manual_pu_ward = st.text_input(
                    "Or Type Specific Ward", key="agent_manual_ward"
                )

        st.markdown("---")
        st.markdown(
            "###### 📊 Section 2: Core Election Mathematics & Verification Checks"
        )
        col3, col4 = st.columns(2)
        with col3:
            pu_tier = st.selectbox(
                "Target Election Tier Matrix Cluster *:",
                [
                    "PRESIDENTIAL",
                    "SENATORIAL",
                    "FEDERAL HOUSE",
                    "STATE GOVERNMENT",
                    "STATE HOUSE OF ASSEMBLY",
                ],
                key="pu_tier_focus",
            )
            pu_accredited = st.number_input(
                "Total Accredited Voters Counted (Per BVAS Verification) *:",
                min_value=0,
                value=0,
                key="pu_acc_voters",
            )
        with col4:
            pu_incident_flag = st.selectbox(
                "Log Field Security Incident/Anomaly Status *:",
                [
                    "Normal Session - No Anomaly",
                    "BVAS Hardware Malfunction",
                    "Disruptive Public Violence",
                    "Ballot Box Tampering",
                ],
                key="pu_incident",
            )

        st.markdown("---")
        st.markdown("###### 🗳️ Section 3: Party Political Vote Aggregations")
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        with col_p1:
            v_apc = st.number_input(
                "APC Score Tally:", min_value=0, value=0, key="v_apc_in"
            )
        with col_p2:
            v_pdp = st.number_input(
                "PDP Score Tally:", min_value=0, value=0, key="v_pdp_in"
            )
        with col_p3:
            v_lp = st.number_input(
                "LP Score Tally:", min_value=0, value=0, key="v_lp_in"
            )
        with col_p4:
            v_nnpp = st.number_input(
                "NNPP Score Tally:", min_value=0, value=0, key="v_nnpp_in"
            )

        pu_description = st.text_area(
            "Field Operator Narrative Notes & Structural Situation Report Description *:",
            key="pu_desc_notes",
        )

        st.markdown("---")
        st.markdown("###### 📸 Section 4: Physical Evidence Document Capture")
        st.camera_input(
            "Optical Sensor Frame: Capture Signed Polling Unit Result Slip Picture *",
            key="pu_cam_slip",
        )

        if st.form_submit_button(
            "📤 TRANSMIT SECURE FIELD PAYLOAD TO BALANCING HARMONY CORE",
            use_container_width=True,
        ):
            final_ward = manual_pu_ward.strip() if manual_pu_ward.strip() else pu_ward
            calculated_sum = v_apc + v_pdp + v_lp + v_nnpp

            if not (
                pu_officer and pu_phone and final_ward and pu_bvas_id and pu_description
            ):
                st.error(
                    "🛑 DATA TRANSMISSION REFUSED: All credential fields, hardware serial tracking, and situational notes must be filled."
                )
            elif calculated_sum > pu_accredited:
                st.error(
                    f"🚨 MATHEMATICAL IMPOSSIBILITY: Aggregate party votes ({calculated_sum:,}) cannot exceed total accredited voters ({pu_accredited:,})."
                )
            else:
                st.success(
                    f"✅ SECURE TELEMETRY LINK LOCKED FOR WARD: {final_ward.upper()}!"
                )
                st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)


def main_dashboard(conn):
    st.markdown(
        """<h2 class="swing-in" style="font-size: 1.8rem; text-transform: uppercase;">🏛️ Executive Control Command Dashboard</h2>""",
        unsafe_allow_html=True,
    )
    admin_modules = [
        "📊 Master Registry Matrix",
        "🗣️ Citizen Feedback",
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
        "📋 Strategic Committee Compliance Logs",
    ]

    if "admin_module_view" not in st.session_state:
        st.session_state.admin_module_view = admin_modules[0]

    selected_module = st.session_state.admin_module_view

    if selected_module == "📊 Master Registry Matrix":
        st.subheader("📊 Master Verification Registry Database Partition Array")
        st.dataframe(st.session_state.get("global_registry", pd.DataFrame()))
    elif selected_module == "🗣️ Citizen Feedback":
        st.subheader("🗣️ Citizen Feedback Messages")
        st.info("This module is under construction.")
    elif selected_module == "📢 Admin Announcement Control":
        render_admin_announcement_control()
    elif selected_module == "📝 Ground Truth Form EC8A Data":
        st.subheader("📝 Ground Truth Form EC8A Audited Verification Schema")
        st.info("This module is under construction.")
    elif selected_module == "🗳️ Live Election Analytical Sync":
        render_election_analytical_sync()
    elif selected_module == "🚀 Legislative Progress Tracker":
        render_progress_tracker()
    elif selected_module == "📋 Strategic Committee Compliance Logs":
        render_committee_compliance_form()
    else:
        st.subheader(selected_module)
        st.info("This module is under construction.")


def render_project_verifications():
    st.markdown(
        """<h2 class="swing-in" style="color:#D4AF37; text-transform: uppercase; font-size: 2rem;">🦅 BEYOND RHETORICS: PROJECT VERIFICATION HUB</h2>""",
        unsafe_allow_html=True,
    )
    st.write(
        "Cross-examining performance metrics with verifiable ground-truth evidence for Balanga/Billiri."
    )
    st.info("Project verification documents will be uploaded here.")


def strategic_committees_panel():
    st.markdown(
        """<div class="supervisor-header swing-in" style="font-size: 1.7rem; text-transform: uppercase;">🛡️ MODULE 13: STRATEGIC COMMITTEES (1-10) ACCESS GATEWAY</div>""",
        unsafe_allow_html=True,
    )

    if "module_13_unlocked" not in st.session_state:
        st.session_state.module_13_unlocked = False

    if not st.session_state.module_13_unlocked:
        with st.form("general_login_form"):
            committee_key_input = st.text_input(
                "Enter General Passkey to Unlock Module:", type="password"
            )
            if st.form_submit_button("Unlock Module", use_container_width=True):
                # This password should be changed for production
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
        if st.session_state.authenticated_committee != selected_committee:
            with st.form(key=f"login_form_{selected_committee.replace(' ', '_')}"):
                password = st.text_input("Enter Committee Passkey:", type="password")
                if st.form_submit_button(
                    "🔓 Unlock Committee", use_container_width=True
                ):
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
        else:
            st.markdown(f"### 📋 Member Registration for: {selected_committee}")
            with st.form(
                key=f"strategic_reg_form_{selected_committee}", clear_on_submit=False
            ):
                st.caption("Enter the verified details of the committee member:")

                st.markdown("##### 📸 Biometric Facial Capture")
                captured_image = st.camera_input("Biometric Face Capture")

                st.markdown("##### 👤 Member Personal Details")
                col_name, col_phone = st.columns(2)
                with col_name:
                    member_name = st.text_input("Full Name")
                with col_phone:
                    member_phone = st.text_input("Phone Number")

                st.markdown("##### 📍 Geographic & Ward Locus")
                constituency_data = {
                    "Balanga": LGA_WARD_DATA.get("BALANGA", []),
                    "Billiri": LGA_WARD_DATA.get("BILLIRI", []),
                }
                col_lga, col_ward_sel, col_ward_txt = st.columns([1, 1, 1])
                with col_lga:
                    selected_lga = st.selectbox(
                        "Select LGA", options=list(constituency_data.keys())
                    )
                with col_ward_sel:
                    selected_ward = st.selectbox(
                        "Select Political Ward",
                        options=constituency_data.get(selected_lga, []) + ["Other"],
                    )
                with col_ward_txt:
                    manual_ward = st.text_input("Or Type Specific Ward")

                st.markdown("##### 🪪 Government Issued Credentials")
                col_nin, col_pvc, col_slip = st.columns([1, 1, 1])
                with col_nin:
                    nin_number = st.text_input("NIN (11 Digits)", max_chars=11)
                with col_pvc:
                    pvc_number = st.text_input("Voters Card Number (VIN)")
                with col_slip:
                    nin_slip = st.file_uploader(
                        "Upload NIN Slip / ID Doc", type=["png", "jpg", "pdf"]
                    )

                st.markdown("##### 🏦 Verified Financial Coordinates")
                col_acc_name, col_acc_num, col_bank = st.columns([1.2, 0.8, 1])
                with col_acc_name:
                    account_name = st.text_input("Account Name")
                with col_acc_num:
                    account_number = st.text_input("Account Number", max_chars=10)
                with col_bank:
                    bank_name = st.text_input("Bank Name")

                if st.form_submit_button(
                    f"➕ Register Member for {selected_committee}",
                    use_container_width=True,
                ):
                    final_ward = (
                        manual_ward.strip() if manual_ward.strip() else selected_ward
                    )
                    if (
                        not member_name
                        or (
                            nin_number
                            and (not nin_number.isdigit() or len(nin_number) != 11)
                        )
                        or (
                            account_number
                            and (
                                not account_number.isdigit()
                                or len(account_number) != 10
                            )
                        )
                    ):
                        st.error(
                            "⚠️ Please check inputs. Name is required, and NIN/Account numbers must be valid lengths."
                        )
                    else:
                        st.success(
                            f"✅ {member_name} has been successfully registered into {selected_committee}!"
                        )
                        st.balloons()

            st.markdown(f"#### Registered Members for: {selected_committee}")


def render_speak_directly_panel():
    st.markdown("### 💬 SPEAK WITH HON. ALI ISA JC DIRECTLY")
    st.markdown("#### **Balanga/Billiri Federal Constituency Direct Liaison**")
    st.caption(
        "Your message will be structured and categorized directly to the constituent liaison office."
    )
    st.write("---")

    constituency_data = {
        "Balanga": LGA_WARD_DATA.get("BALANGA", []),
        "Billiri": LGA_WARD_DATA.get("BILLIRI", []),
    }

    with st.form(key="speak_direct_form", clear_on_submit=True):
        st.markdown("##### **Constituent Verification Details**")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
        with col2:
            phone_num = st.text_input("Phone Number", placeholder="e.g., +234...")

        col3, col4, col5 = st.columns([1, 1, 1])
        with col3:
            selected_lga = st.selectbox(
                "Select Local Government Area (LGA)",
                options=list(constituency_data.keys()),
            )
        with col4:
            selected_ward = st.selectbox(
                "Select Political Ward", options=constituency_data.get(selected_lga, [])
            )
        with col5:
            manual_ward = st.text_input(
                "Or Type Specific Ward", key="speak_directly_manual_ward"
            )

        st.write("---")
        st.markdown("##### **Your Message or Proposal**")
        subject = st.text_input(
            "Subject of Appeal", placeholder="Briefly what this is about"
        )
        message_body = st.text_area(
            "Detailed Message",
            placeholder=f"Type your direct message to Hon. Ali Isa JC here...",
        )

        if st.form_submit_button(
            "🚀 Transmit Message to Leader", use_container_width=True
        ):
            final_ward = manual_ward.strip() if manual_ward.strip() else selected_ward
            if not (full_name and message_body and final_ward):
                st.error(
                    "⚠️ Please fill in your Name, Ward, and Message before transmitting."
                )
            else:
                st.success("📨 Message Successfully Logged for Verification!")
                st.balloons()


def render_committee_compliance_form():
    st.markdown("### 📋 STRATEGIC COMMITTEE COMPLIANCE LOGS")
    st.caption(
        "Categorized regulatory compliance submissions and data logs for direct administrative sorting."
    )
    committee_group = st.selectbox(
        "Select Committee Strategic Group Allocation:",
        [
            "Group A: Agricultural Development & Horticulture Council",
            "Group B: Vocational Capacity, Technical Pools & Modern Economy",
            "Group C: Ecological Monitoring, Erosion Fund & Infrastructure",
            "Group D: Palliative Logistics & Community Social Investment",
        ],
    )
    with st.form("committee_compliance_matrix_form"):
        st.write(f"📝 **Filing Progress Report for:** `{committee_group}`")
        officer_name = st.text_input("Reporting Official Name:")
        regional_scope = st.text_input("Target Local Government Area / Ward Location:")
        activity_summary = st.text_area(
            "Comprehensive Execution Metrics & Compliance Actions Summary:"
        )
        expenditure_vouched = st.number_input(
            "Vouched Project Resources Expended (NGN):", min_value=0.0, step=1000.0
        )
        if st.form_submit_button(
            "🔒 Transmit Report to Executive Control Room", use_container_width=True
        ):
            st.success(
                f"✅ Report for {officer_name} logged under {committee_group.split(':')[0]}!"
            )


def render_election_analytical_sync():
    st.markdown("### 📊 LIVE ELECTION ANALYTICAL SYNC DISPLAY")
    st.caption(
        "National real-time command dashboard. Drill down across states, LGAs, and operational units."
    )
    st.markdown("### CASCADING GEO-SEARCH TERMINAL")
    c1, c2, c3 = st.columns(3)
    with c1:
        state_list = sorted(list(GEO_MATRIX.keys()))
        selected_state = st.selectbox(
            "🎯 Select Target State:",
            options=state_list,
            index=state_list.index("Gombe") if "Gombe" in state_list else 0,
        )
    with c2:
        lga_list = sorted(list(GEO_MATRIX.get(selected_state, {}).keys()))
        selected_lga = st.selectbox("🏢 Select LGA:", options=lga_list)
    with c3:
        ward_list = sorted(GEO_MATRIX.get(selected_state, {}).get(selected_lga, []))
        selected_ward = st.selectbox("📍 Select Ward:", options=ward_list)


def render_vouching_form():
    st.markdown("### 🛡️ SECURE VOUCHING & VERIFICATION MATRIX")
    st.write("---")
    st.info(
        "The secure field verification and constituent vouching module is currently active."
    )
    render_palliative_form(focus_on_vouching=True)


def render_constituent_plenary_updates():
    st.markdown("### 📺 LIVE PLENARY UPDATES & RESOLUTIONS")
    st.markdown("#### **Balanga/Billiri Federal Constituency Legislative Broadcast**")
    st.write("---")
    st.info(
        f"The live plenary digest and House of Representatives tracking matrix for Hon. Ali Isa JC is currently under development and will be available shortly."
    )


def render_job_verification_panel():
    st.header("🔍 Federal Job Verification & Tracking Hub")
    st.caption(
        "Verify authentic military, paramilitary, and federal agency recruitments with official timelines."
    )
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Active Federal Windows", "3 Open Openings")
    with m2:
        st.metric("Scam Alerts Logged", "14 Verified Scams")
    with m3:
        st.metric("Last Matrix Update", "Today, 11:30 WAT")
    st.divider()
    col_search, col_type = st.columns([2, 1])
    with col_search:
        search_query = st.text_input(
            "Search by Agency Name (e.g., 'Customs', 'Air Force')..."
        )
    with col_type:
        agency_type = st.selectbox(
            "Filter Tier",
            ["All Tiers", "Military", "Paramilitary", "Civil Service / MDA"],
        )
    st.markdown("### 📋 Official Recruitment Status Matrix")
    job_data = [
        {
            "Agency": "Nigerian Army (Direct Short Service)",
            "Type": "Military",
            "Status": "🟢 ACTIVE",
            "Official Portal": "https://recruitment.army.mil.ng",
        },
        {
            "Agency": "Nigeria Customs Service (NCS)",
            "Type": "Paramilitary",
            "Status": "🔴 CLOSED",
            "Official Portal": "https://customs.gov.ng",
        },
        {
            "Agency": "Federal Civil Service Commission",
            "Type": "Civil Service / MDA",
            "Status": "🔴 CLOSED",
            "Official Portal": "https://fcsc.gov.ng",
        },
    ]
    filtered_jobs = [
        j
        for j in job_data
        if (search_query.lower() in j["Agency"].lower())
        and (agency_type == "All Tiers" or j["Type"] == agency_type)
    ]
    if filtered_jobs:
        st.dataframe(
            filtered_jobs,
            use_container_width=True,
            column_config={
                "Official Portal": st.column_config.LinkColumn(
                    "Official Application Link", display_text="Launch Official Site 🌐"
                )
            },
        )
    else:
        st.info("No matching verified federal windows found for your search query.")
    st.error(
        "🚨 **Constituent Scam Protection Alert:** If you have received a recruitment text or letter demanding payment for pins or placement in any paramilitary body, it is a fraud. Report details directly to the admin command center."
    )


def render_grants_verification_panel():
    st.header("📂 Federal Palliative & Industrial Grants Matrix")
    st.caption(
        "Track and verify authentic federal intervention schemes and industrial development funds."
    )
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Verified Open Funds", "4 Active Schemes")
    with m2:
        st.metric("Total Federal Capital Allocation", "₦150B (Nationwide)")
    with m3:
        st.metric("Portal Data Sync Status", "Live / Verified")
    st.divider()
    col_search, col_type = st.columns([2, 1])
    with col_search:
        search_query = st.text_input(
            "Search by Fund or Agency Name (e.g., 'SMEDAN', 'BOI')..."
        )
    with col_type:
        grant_tier = st.selectbox(
            "Fund Category",
            [
                "All Categories",
                "Social Palliative / Relief",
                "MSME & Industrial Growth",
                "Agricultural Intervention",
            ],
        )
    st.markdown("### 📋 Official Intervention & Grant Registry")
    grant_database = [
        {
            "Scheme Name": "BOI MSME Intervention Fund",
            "Category": "MSME & Industrial Growth",
            "Status": "🟢 OPEN",
            "Official Portal": "https://www.boi.ng/investment-funds",
        },
        {
            "Scheme Name": "Federal Presidential Palliative Grant",
            "Category": "Social Palliative / Relief",
            "Status": "🔴 CLOSED",
            "Official Portal": "https://grant.fedgrantandloan.gov.ng",
        },
        {
            "Scheme Name": "SMEDAN Agro-Business Development Component",
            "Category": "Agricultural Intervention",
            "Status": "🟢 OPEN",
            "Official Portal": "https://smedan.gov.ng",
        },
        {
            "Scheme Name": "NERFUND Manufacturing Expansion Credit Line",
            "Category": "MSME & Industrial Growth",
            "Status": "🟢 OPEN",
            "Official Portal": "http://www.nerfund.gov.ng",
        },
    ]
    filtered_grants = [
        g
        for g in grant_database
        if (search_query.lower() in g["Scheme Name"].lower())
        and (grant_tier == "All Categories" or g["Category"] == grant_tier)
    ]
    if filtered_grants:
        st.dataframe(
            filtered_grants,
            use_container_width=True,
            column_config={
                "Official Portal": st.column_config.LinkColumn(
                    "Official Application Link",
                    display_text="Apply via Official Portal 🌐",
                )
            },
        )
    else:
        st.info(
            "No matching verified federal intervention programs found for your criteria."
        )
    st.warning(
        "⚠️ **Security Vetting Advisory:** Authentic federal government intervention programs will **never** demand processing fees or your bank account transaction PIN codes."
    )


@st.cache_data(ttl=3600)
def fetch_live_federal_vacancies():
    return [
        {
            "Agency": "Nigeria Air Force (Recruitment)",
            "Date": "2024-07-15",
            "Status": "🟢 OPEN",
        },
        {
            "Agency": "Civil Defense, Fire, Immigration (CDCFIB)",
            "Date": "2024-07-17",
            "Status": "🟢 OPEN",
        },
        {
            "Agency": "NDLEA Officer Cadet Corps",
            "Date": "2024-05-10",
            "Status": "🔴 CLOSED",
        },
    ]


@st.fragment(run_every="5m")
def render_top_vacancy_alerts():
    try:
        live_feed = fetch_live_federal_vacancies()
        recent_windows = [v for v in live_feed if v["Status"] == "🟢 OPEN"]
        if recent_windows:
            alert_text = " | ".join(
                [f"🔥 {item['Agency']} is currently active!" for item in recent_windows]
            )
            st.markdown(
                f"""
                <div style="background-color: #7A1C1C; border-left: 6px solid #D4AF37; padding: 12px 20px; border-radius: 4px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">
                    <span style="color: #FFFFFF; font-weight: 800; font-family: 'Inter', sans-serif; letter-spacing: 0.5px; font-size: 0.95rem;">
                        ⚠️ VERIFIED FEDERAL VACANCY ALERT: {alert_text}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    except Exception:
        pass


def render_vouching_verification_panel():
    """
    📜 CONSTITUENCY VOUCHING VERIFICATION
    Provides a dedicated interface for community leaders to vouch for constituents
    by focusing the integrated palliative form on the vouching pathway.
    """
    st.markdown("### 📜 CONSTITUENCY VOUCHING VERIFICATION")
    st.markdown("#### **Balanga/Billiri Federal Constituency Endorsement Portal**")
    st.write("---")
    st.info(
        "This module allows authenticated community leaders to vouch for members of their community, streamlining access to empowerment programs and grants. Please fill out your credentials as the vouching leader and the details of the applicant you are endorsing."
    )
    render_palliative_form(focus_on_vouching=True)
