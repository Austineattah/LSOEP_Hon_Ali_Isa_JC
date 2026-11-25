import streamlit as st
import pandas as pd
import datetime
import time
import hmac
import os
import html
import re
import textwrap

from auth import has_committee_access, is_logged_in, render_login_prompt, require_role
from panels.election_war_room import render_election_war_room
from persistence import (
    PersistenceError,
    find_mock_submissions,
    list_submissions,
    purge_mock_submissions,
    submit_submission,
)
from registry import (
    LGA_WARD_DATA,
    STRATEGIC_COMMITTEE_NAMES,
    HON_ALI_SPONSORED_BILLS,
    HON_TITLE,
    FEDERAL_INDUSTRIAL_GRANTS,
)


def _commit_submission(submission_type, payload, uploads=None, dedupe_fields=None):
    try:
        submit_submission(
            submission_type,
            payload,
            uploads=uploads,
            dedupe_fields=dedupe_fields,
        )
    except PersistenceError as exc:
        st.error(str(exc))
        return False
    return True


def _valid_phone(value):
    digits = re.sub(r"\D", "", value)
    return 10 <= len(digits) <= 15


def render_constituency_engagement_channels():
    """
    🏛️ Official Constituency Engagement Channels Grid Matrix
    All 13 channels cleanly rendered for Hon. Ali Isa JC.
    """
    st.markdown("### 🏛️ CONSTITUENCY ENGAGEMENT CHANNELS")
    st.write("---")

    ENGAGEMENT_CHANNELS = [
        {
            "label": "LEGISLATIVE PROGRESS TRACKER",
            "route": "PROGRESS_TRACKER",
        },
        {
            "label": "BEYOND RHETORICS PROJECT EXECUTION",
            "route": "BEYOND_RHETORICS",
        },
        {
            "label": "SPEAK WITH HON. ALI ISA JC DIRECTLY",
            "route": "SPEAK_DIRECT",
        },
        {
            "label": "STRATEGIC COMMITTEES (MODULE 13)",
            "route": "STRATEGIC_COMMITTEES",
        },
        {
            "label": "LEGISLATIVE FOOTPRINTS",
            "route": "LEGISLATIVE_FOOTPRINTS",
        },
        {"label": "SKILL VOCATION POOL", "route": "SKILL_POOL"},
        {"label": "STUDENT SCHOLARSHIP/GRANT", "route": "SCHOLARSHIPS"},
        {
            "label": "JOB VACANCY VERIFICATION",
            "route": "JOB_VERIFICATION",
        },
        {
            "label": "FEDERAL & INDUSTRIAL GRANTS",
            "route": "GRANTS_VERIFICATION",
        },
        {"label": "PALLIATIVE ENROLLMENT", "route": "PALLIATIVES"},
        {"label": "CV & ARTISAN VAULT", "route": "CV_VAULT"},
        {"label": "COMMUNITY URGENT NEED", "route": "URGENT_NEED"},
        {
            "label": "CONSTITUENCY VOUCHING VERIFICATION",
            "route": "VOUCHING_VERIFICATION",
        },
    ]

    for channel in ENGAGEMENT_CHANNELS:
        button_label = channel["label"]
        if st.button(
            button_label,
            key=f"eng_chan_btn_{channel['route']}",
            width="stretch",
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
    except OSError as exc:
        st.warning(f"The announcement file could not be read: {exc}")
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
            "🔒 LOCK ANNOUNCEMENT AND RE-PROPAGATE MARQUEE", width="stretch"
        ):
            if new_ticker.strip():
                try:
                    submit_submission("announcement", {"message": new_ticker.strip()})
                except PersistenceError as exc:
                    st.error(str(exc))
                else:
                    st.session_state.global_scrolling_announcement = new_ticker.strip()
                    st.success("The announcement was saved and published.")
                    st.rerun()
            else:
                st.warning("Please specify a valid text announcement.")


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
        st.markdown("##### 🛡️ OPTIONAL COMMUNITY LEADER REFERRAL")
        v_leader_name = st.text_input("Referring Community Leader (optional)")
        v_leader_phone = st.text_input("Leader Contact Number (optional)")

        if st.form_submit_button(
            "🚀 COMMIT APPLICATION TO TRAINING POOLS", width="stretch"
        ):
            final_ward = manual_kward.strip() if manual_kward.strip() else kward
            if not (
                sv_name and sv_phone and sv_nin and sv_vin and sv_stmt and final_ward
            ):
                st.error(
                    "🛑 FORM ERROR: All core validation strings, documents, and biometric snapshot frames are mandatory."
                )
            elif len(sv_nin) != 11 or not sv_nin.isdigit():
                st.error("NIN must contain exactly 11 digits.")
            elif not _valid_phone(sv_phone):
                st.error("Enter a valid contact phone number.")
            elif not sv_file or not sv_cam:
                st.error(
                    "Upload the NIN slip and provide the requested camera capture."
                )
            else:
                saved = _commit_submission(
                    "skill_application",
                    {
                        "name": sv_name.strip(),
                        "phone": sv_phone.strip(),
                        "nin": sv_nin,
                        "vin": sv_vin.strip(),
                        "date_of_birth": sv_dob,
                        "gender": sv_gender,
                        "disability_status": sv_disability,
                        "ward": final_ward,
                        "lga": klga_clean,
                        "skill_interest": custom_vocation or sv_selection,
                        "prior_palliative": sv_palliative_check,
                        "statement": sv_stmt.strip(),
                        "leader_name": v_leader_name.strip(),
                        "leader_contact": v_leader_phone.strip(),
                    },
                    uploads={"nin_slip": sv_file, "biometric_capture": sv_cam},
                    dedupe_fields=["nin"],
                )
                if saved:
                    st.success("Your skill application was saved successfully.")
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
            width="stretch",
        ):
            final_ward = manual_sward.strip() if manual_sward.strip() else sward
            if not (
                sch_name
                and sch_nin
                and sch_phone
                and sch_inst
                and sch_just
                and final_ward
            ):
                st.error("Please fill all required fields.")
            elif len(sch_nin) != 11 or not sch_nin.isdigit():
                st.error("NIN must contain exactly 11 digits.")
            elif not _valid_phone(sch_phone):
                st.error("Enter a valid contact phone number.")
            elif not sch_file_nin or not sch_file_adm or not sch_cam:
                st.error(
                    "Upload both required documents and provide the student ID capture."
                )
            else:
                saved = _commit_submission(
                    "scholarship_application",
                    {
                        "name": sch_name.strip(),
                        "nin": sch_nin,
                        "phone": sch_phone.strip(),
                        "academic_year": sch_year,
                        "institution": sch_inst.strip(),
                        "study_level": sch_level,
                        "lga": slga_clean,
                        "ward": final_ward,
                        "justification": sch_just.strip(),
                    },
                    uploads={
                        "nin_slip": sch_file_nin,
                        "admission_letter": sch_file_adm,
                        "student_id": sch_cam,
                    },
                    dedupe_fields=["nin"],
                )
                if saved:
                    st.success("Your scholarship application was saved successfully.")
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
            width="stretch",
        ):
            final_ward = manual_vward.strip() if manual_vward.strip() else vward
            if not (cv_name and cv_nin and cv_phone and final_ward and cv_summary):
                st.error("Please fill all required fields.")
            elif len(cv_nin) != 11 or not cv_nin.isdigit():
                st.error("NIN must contain exactly 11 digits.")
            elif not _valid_phone(cv_phone):
                st.error("Enter a valid contact phone number.")
            elif not cv_file or not cv_cam:
                st.error("Upload your CV and provide the certification capture.")
            else:
                saved = _commit_submission(
                    "cv_application",
                    {
                        "name": cv_name.strip(),
                        "category": cv_cat,
                        "qualification": cv_qual,
                        "nin": cv_nin,
                        "phone": cv_phone.strip(),
                        "lga": vlga_clean,
                        "ward": final_ward,
                        "summary": cv_summary.strip(),
                    },
                    uploads={"cv": cv_file, "certification_capture": cv_cam},
                    dedupe_fields=["nin"],
                )
                if saved:
                    st.success("Your talent profile was saved successfully.")
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
            "🚨 TRIGGER COMMAND INCIDENT VECTOR ALERT", width="stretch"
        ):
            final_ward = manual_cward.strip() if manual_cward.strip() else cward
            if not (cun_member and cun_phone and final_ward and cun_logs):
                st.error("Please fill all required fields.")
            elif not _valid_phone(cun_phone):
                st.error("Enter a valid contact phone number.")
            elif not cun_file or not cun_cam:
                st.error("Upload the requested ID document and field evidence photo.")
            else:
                saved = _commit_submission(
                    "community_urgent_need",
                    {
                        "reporter_name": cun_member.strip(),
                        "phone": cun_phone.strip(),
                        "lga": clga_clean,
                        "ward": final_ward,
                        "request_area": cun_area,
                        "situation_report": cun_logs.strip(),
                    },
                    uploads={"identity_document": cun_file, "field_photo": cun_cam},
                )
                if saved:
                    st.success("Your community urgent-need report was saved.")
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
        key=(
            "app_pathway_toggle_vouching"
            if focus_on_vouching
            else "app_pathway_toggle_direct"
        ),
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
        if st.button("🗳️ Submit Direct Self-Application Profile", width="stretch"):
            if len(p_nin) != 11 or not p_nin.isdigit():
                st.error(
                    "🛑 Your National Identity Number (NIN) must be exactly 11 digits."
                )
            elif not p_name or not p_phone or p_lga == "Select LGA..." or not p_ward:
                st.error(
                    "🛑 Please complete all required personal identity, geography, and ward details."
                )
            elif not _valid_phone(p_phone):
                st.error("Enter a valid contact phone number.")
            elif not p_request_area:
                st.error("🛑 Please describe your specific relief request area.")
            elif not uploaded_nin:
                st.error("Provide the requested NIN photo or document.")
            else:
                saved = _commit_submission(
                    "palliative_direct",
                    {
                        "name": p_name.strip(),
                        "phone": p_phone.strip(),
                        "nin": p_nin,
                        "voter_id": p_voter.strip(),
                        "lga": p_lga,
                        "ward": p_ward.strip(),
                        "address": p_addr.strip(),
                        "request_area": p_request_area.strip(),
                    },
                    uploads={"identity_document": uploaded_nin},
                    dedupe_fields=["nin"],
                )
                if saved:
                    st.success(
                        "Your direct palliative application was saved successfully."
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
        if st.button("🗳️ Register Certified Welfare Vouching Profile", width="stretch"):
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
            elif (
                leader_lga == "Select LGA..."
                or applicant_lga == "Select LGA..."
                or not leader_phone
                or not applicant_phone
            ):
                st.error("Select both LGAs and provide both contact phone numbers.")
            elif not _valid_phone(leader_phone) or not _valid_phone(applicant_phone):
                st.error("Both contact phone numbers must be valid.")
            elif not v_applicant_request_area:
                st.error("🛑 Please describe the applicant's specific request area.")
            elif not applicant_nin_file:
                st.error("Provide the requested applicant NIN photo or document.")
            else:
                saved = _commit_submission(
                    "palliative_vouching",
                    {
                        "leader_title": leader_title,
                        "leader_name": leader_name.strip(),
                        "leader_phone": leader_phone.strip(),
                        "leader_lga": leader_lga,
                        "leader_ward": leader_ward.strip(),
                        "leader_nin": leader_nin,
                        "leader_voter_id": leader_voter.strip(),
                        "applicant_name": applicant_name.strip(),
                        "applicant_phone": applicant_phone.strip(),
                        "applicant_lga": applicant_lga,
                        "applicant_ward": applicant_ward.strip(),
                        "applicant_nin": applicant_nin,
                        "applicant_voter_id": applicant_voter.strip(),
                        "request_area": v_applicant_request_area.strip(),
                    },
                    uploads={"applicant_identity_document": applicant_nin_file},
                    dedupe_fields=["applicant_nin"],
                )
                if saved:
                    st.success("The vouching application was saved successfully.")
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
                status_indicator = (
                    "[Passed]" if "Passed" in item["status"] else "[In progress]"
                )
                st.markdown(
                    f"**📋 Current Status:** {status_indicator} {item['status']}"
                )
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
    if not require_role("collation"):
        return

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
            ndc_votes = st.number_input("NDC Votes", min_value=0)
            adc_votes = st.number_input("ADC Votes", min_value=0)

            incident_occurred = st.selectbox("Incident Occurred?", ["No", "Yes"])
            incident_details = ""
            if incident_occurred == "Yes":
                incident_details = st.text_area("Incident Form Scenario")

        collation_evidence = st.camera_input(
            "Live Capture Sensor Matrix: Form EC8A Sheet"
        )

        if st.form_submit_button(
            "🔍 GENERATE SYSTEM INTEGRITY PREVIEW RECORD SLIP", width="stretch"
        ):
            final_ward = (
                manual_sup_ward.strip() if manual_sup_ward.strip() else sup_ward
            )
            if not (sup_name and sup_phone and final_ward and bvas_serial):
                st.error(
                    "Supervisor name, phone, ward, and BVAS serial number are required."
                )
            elif not _valid_phone(sup_phone):
                st.error("Enter a valid contact phone number.")
            elif apc_votes + pdp_votes + ndc_votes + adc_votes > accredited_voters:
                st.error("The party vote total cannot exceed accredited voters.")
            elif not collation_evidence:
                st.error(
                    "Capture the Form EC8A evidence before generating the receipt."
                )
            else:
                st.session_state.sup_slip_preview = {
                    "Supervisor": sup_name,
                    "Phone": sup_phone,
                    "LGA": sup_lga_clean,
                    "Ward": final_ward,
                    "APC_Votes": apc_votes,
                    "PDP_Votes": pdp_votes,
                    "NDC_Votes": ndc_votes,
                    "ADC_Votes": adc_votes,
                    "BVAS_Serial_Number": bvas_serial,
                    "Accredited_Voters": accredited_voters,
                    "Incident_Occurred": incident_occurred,
                    "Incident_Details": incident_details,
                    "Evidence": collation_evidence,
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.rerun()

    if st.session_state.sup_slip_preview is not None:
        p_data = st.session_state.sup_slip_preview
        safe_data = {
            key: html.escape(str(value))
            for key, value in p_data.items()
            if key != "Evidence"
        }
        st.markdown(
            f"""
            <div class="printable-slip-box">
                <div class="slip-header">LSOEP WARD COLLATION INTEGRITY RECEIPT</div>
                <div class="slip-row"><span>TIMESTAMP:</span> <span>{safe_data['Timestamp']}</span></div>
                <div class="slip-row"><span>SUPERVISOR:</span> <span>{safe_data['Supervisor']}</span></div>
                <div class="slip-row"><span>LGA:</span> <span>{safe_data['LGA']}</span></div>
                <div class="slip-row"><span>WARD:</span> <span>{safe_data['Ward']}</span></div>
                <div class="slip-row"><span>ACCREDITED:</span> <span>{safe_data['Accredited_Voters']}</span></div>
                <div class="slip-row"><span>BVAS S/N:</span> <span>{safe_data['BVAS_Serial_Number']}</span></div>
                <div class="slip-row" style="color:blue;"><span>APC:</span> <span>{safe_data['APC_Votes']}</span></div>
                <div class="slip-row" style="color:green;"><span>PDP:</span> <span>{safe_data['PDP_Votes']}</span></div>
                <div class="slip-row" style="color:red;"><span>NDC:</span> <span>{safe_data.get('NDC_Votes', safe_data.get('LP_Votes', 0))}</span></div>
                <div class="slip-row" style="color:orange;"><span>ADC:</span> <span>{safe_data.get('ADC_Votes', safe_data.get('NNPP_Votes', 0))}</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("🔒 CONFIRM & LOG METRICS", width="stretch"):
                payload = {
                    key: value
                    for key, value in p_data.items()
                    if key not in {"Evidence", "Timestamp"}
                }
                payload["timestamp"] = p_data["Timestamp"]
                saved = _commit_submission(
                    "ward_collation",
                    payload,
                    uploads={"ec8a_sheet": p_data["Evidence"]},
                    dedupe_fields=["BVAS_Serial_Number"],
                )
                if saved:
                    st.session_state.sup_slip_preview = None
                    st.success("The collation report was saved successfully.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
        with col_v2:
            if st.button("❌ ABORT TRANSACTION", width="stretch"):
                st.session_state.sup_slip_preview = None
                st.warning("Preview cleared.")
                st.rerun()


def agent_panel():
    if not require_role("agent"):
        return

    st.markdown("### 🗳️ POLLING UNIT AGENT COMMAND CONTROL NODE")
    st.write("---")

    ac1, ac2 = st.columns([5, 2])
    with ac2:
        if st.button(
            "🔒 Seal Node & Close Terminal Session",
            key="seal_agent_node_btn_v9",
            width="stretch",
        ):
            st.session_state.current_route = "HOME"
            st.logout()

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
            v_ndc = st.number_input(
                "NDC Score Tally:", min_value=0, value=0, key="v_ndc_in"
            )
        with col_p4:
            v_adc = st.number_input(
                "ADC Score Tally:", min_value=0, value=0, key="v_adc_in"
            )

        pu_description = st.text_area(
            "Field Operator Narrative Notes & Structural Situation Report Description *:",
            key="pu_desc_notes",
        )

        st.markdown("---")
        st.markdown("###### 📸 Section 4: Physical Evidence Document Capture")
        pu_evidence = st.camera_input(
            "Optical Sensor Frame: Capture Signed Polling Unit Result Slip Picture *",
            key="pu_cam_slip",
        )

        if st.form_submit_button(
            "📤 TRANSMIT SECURE FIELD PAYLOAD TO BALANCING HARMONY CORE",
            width="stretch",
        ):
            final_ward = manual_pu_ward.strip() if manual_pu_ward.strip() else pu_ward
            calculated_sum = v_apc + v_pdp + v_ndc + v_adc

            if not (
                pu_officer and pu_phone and final_ward and pu_bvas_id and pu_description
            ):
                st.error(
                    "🛑 DATA TRANSMISSION REFUSED: All credential fields, hardware serial tracking, and situational notes must be filled."
                )
            elif not _valid_phone(pu_phone):
                st.error("Enter a valid contact phone number.")
            elif not pu_evidence:
                st.error(
                    "Capture the signed polling-unit result slip before submitting."
                )
            elif calculated_sum > pu_accredited:
                st.error(
                    f"🚨 MATHEMATICAL IMPOSSIBILITY: Aggregate party votes ({calculated_sum:,}) cannot exceed total accredited voters ({pu_accredited:,})."
                )
            else:
                saved = _commit_submission(
                    "polling_unit_tally",
                    {
                        "officer_name": pu_officer.strip(),
                        "phone": pu_phone.strip(),
                        "bvas_serial": pu_bvas_id.strip(),
                        "lga": pu_lga,
                        "ward": final_ward,
                        "election_tier": pu_tier,
                        "accredited_voters": pu_accredited,
                        "incident": pu_incident_flag,
                        "party_votes": {
                            "APC": v_apc,
                            "PDP": v_pdp,
                            "NDC": v_ndc,
                            "ADC": v_adc,
                        },
                        "total_votes": calculated_sum,
                        "description": pu_description.strip(),
                    },
                    uploads={"result_slip": pu_evidence},
                    dedupe_fields=["bvas_serial"],
                )
                if saved:
                    st.success(
                        f"Field tally for {final_ward.upper()} was saved successfully."
                    )
                    st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)


def main_dashboard(conn):
    if not require_role("admin"):
        return

    st.markdown(
        """<h2 class="swing-in" style="font-size: 1.8rem; text-transform: uppercase;">🏛️ Executive Control Command Dashboard</h2>""",
        unsafe_allow_html=True,
    )
    admin_modules = [
        "📊 Master Registry Matrix",
        "🗣️ Citizen Feedback",
        "Mock Data Purge",
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
        try:
            records = list_submissions(
                [
                    "palliative_direct",
                    "palliative_vouching",
                    "skill_application",
                    "scholarship_application",
                    "cv_application",
                ]
            )
        except PersistenceError as exc:
            st.error(str(exc))
        else:
            if records is None:
                return
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Submission Type": record["submission_type"],
                            "Created At": record["created_at"],
                            **record["payload"],
                        }
                        for record in records
                    ]
                ),
                hide_index=True,
                width="stretch",
            )
    elif selected_module == "🗣️ Citizen Feedback":
        st.subheader("🗣️ Citizen Feedback Messages")
        _render_saved_submissions(["speak_direct", "community_urgent_need"])
def _get_mock_purge_passcode():
    try:
        sec_code = st.secrets.get("mock_purge_passcode")
        if isinstance(sec_code, str) and sec_code.strip():
            return sec_code.strip()
    except Exception:
        pass
    env_code = os.getenv("MOCK_PURGE_PASSCODE", "")
    if env_code.strip():
        return env_code.strip()
    return "aliisa2027"


def render_admin_mock_purge_control():
    if not require_role("admin"):
        return

    st.markdown("### Mock Data Dry-Run & Scoped Purge")
    st.caption(
        "Matches ONLY rows explicitly tagged as mock/drill records (is_mock=True or a configured prefix such as MOCK- / DRILL-) and cleans up linked private-evidence files."
    )

    marker_prefix = st.text_input(
        "Mock Payload Prefix Filter",
        value="MOCK-",
        key="admin_mock_purge_prefix",
    ).strip()

    try:
        mock_rows = find_mock_submissions(marker_prefix=marker_prefix or "MOCK-", limit=1000)
    except PersistenceError as exc:
        st.error(f"Could not scan mock submissions: {exc}")
        return

    st.metric("Matched Mock Submissions (Dry-Run)", len(mock_rows))

    if not mock_rows:
        st.info("No mock submissions match the active filter. Nothing to purge.")
        return

    preview_rows = []
    for r in mock_rows:
        pl = r.get("payload") if isinstance(r.get("payload"), dict) else {}
        ev = pl.get("evidence_paths")
        ev_count = len(ev) if isinstance(ev, (dict, list)) else 0
        summary_str = ", ".join(
            f"{k}={v}" for k, v in list(pl.items())[:4] if k != "evidence_paths"
        )
        preview_rows.append(
            {
                "ID": r.get("id"),
                "Type": r.get("submission_type"),
                "Created": r.get("created_at"),
                "Evidence Files": ev_count,
                "Payload Preview": summary_str[:120],
            }
        )

    st.dataframe(preview_rows, width="stretch")

    st.warning(
        "Double-guarded action: Enter the purge passcode, confirm you exported a backup snapshot, and type PURGE MOCK DATA to execute."
    )
    entered_purge_code = st.text_input(
        "Purge Authorization Passcode",
        type="password",
        key="admin_mock_purge_passcode",
    )
    backup_confirmed = st.checkbox(
        "I confirm a pre-purge backup snapshot has been exported.",
        key="admin_mock_purge_backup_chk",
    )
    typed_phrase = st.text_input(
        "Type PURGE MOCK DATA to confirm",
        key="admin_mock_purge_phrase",
    )

    guards_ok = (
        bool(entered_purge_code)
        and hmac.compare_digest(entered_purge_code.strip(), _get_mock_purge_passcode())
        and backup_confirmed
        and typed_phrase.strip() == "PURGE MOCK DATA"
    )

    if st.button(
        "Execute Scoped Mock Purge",
        key="admin_mock_purge_exec_btn",
        disabled=not guards_ok,
        width="stretch",
    ):
        ids_to_delete = [r.get("id") for r in mock_rows if r.get("id") is not None]
        try:
            result = purge_mock_submissions(
                ids_to_delete, marker_prefix=marker_prefix or "MOCK-"
            )
        except PersistenceError as exc:
            st.error(f"Purge failed: {exc}")
            return

        st.success(
            f"Purged {len(result['deleted_ids'])} mock rows and {result['deleted_evidence_count']} evidence files."
        )
        if result["errors"]:
            for err in result["errors"]:
                st.error(err)
        st.rerun()


    elif selected_module == "Mock Data Purge":
        render_admin_mock_purge_control()
    elif selected_module == "📢 Admin Announcement Control":
        render_admin_announcement_control()
    elif selected_module == "📝 Ground Truth Form EC8A Data":
        st.subheader("📝 Ground Truth Form EC8A Audited Verification Schema")
        _render_saved_submissions(["ward_collation", "polling_unit_tally"])
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


def _render_saved_submissions(submission_types):
    try:
        records = list_submissions(submission_types)
    except PersistenceError as exc:
        st.error(str(exc))
        return

    if records is None:
        return
    if not records:
        st.info("No saved submissions are available for this view.")
        return

    # Convert records to DataFrame for processing and flatten nested party_votes
    flattened_rows = []
    for record in records:
        payload = dict(record.get("payload") or {})
        party_votes = payload.pop("party_votes", None)
        if isinstance(party_votes, dict):
            for party_name, votes in party_votes.items():
                payload.setdefault(f"{party_name}_Votes", votes)

        flattened_rows.append(
            {
                "Submission Type": record["submission_type"],
                "Created At": record["created_at"],
                "ID": record.get("id", ""),
                **payload,
            }
        )

    df = pd.DataFrame(flattened_rows)

    # Add search and filter controls
    st.markdown("### 📊 Live Submission Metrics & Management")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Submissions", len(df))
    with col2:
        st.metric(
            "Submission Types",
            df["Submission Type"].nunique() if "Submission Type" in df.columns else 0,
        )
    with col3:
        st.metric(
            "Latest Update",
            df["Created At"].max() if "Created At" in df.columns else "N/A",
        )

    # Ward & LGA agent coverage summary for Form EC8A / collation sync
    has_ward = "ward" in df.columns and df["ward"].dropna().astype(str).str.strip().ne("").any()
    has_lga = "lga" in df.columns and df["lga"].dropna().astype(str).str.strip().ne("").any()
    if has_ward or has_lga:
        cov1, cov2, cov3 = st.columns(3)
        with cov1:
            unique_lgas = df["lga"].dropna().astype(str).str.strip().nunique() if has_lga else 0
            st.metric("LGAs Synced", unique_lgas)
        with cov2:
            unique_wards = df["ward"].dropna().astype(str).str.strip().nunique() if has_ward else 0
            st.metric("Wards Covered", unique_wards)
        with cov3:
            active_agents = (
                df["officer_name"].dropna().astype(str).str.strip().nunique()
                if "officer_name" in df.columns
                else 0
            )
            st.metric("Reporting Field Agents", active_agents)

    st.write("---")

    # Search and filter
    search_col, filter_col = st.columns(2)
    with search_col:
        search_term = st.text_input(
            "🔍 Search submissions",
            placeholder="Search by name, phone, ward, BVAS serial, or any field...",
            key="admin_submissions_search",
        )

    with filter_col:
        if "Submission Type" in df.columns:
            all_types = ["All Types"] + sorted(df["Submission Type"].unique().tolist())
            filter_type = st.selectbox(
                "📋 Filter by type",
                all_types,
                key="admin_submissions_filter",
            )
        else:
            filter_type = "All Types"

    # Apply filters
    filtered_df = df
    if search_term:
        mask = (
            filtered_df.astype(str)
            .apply(lambda x: x.str.contains(search_term, case=False, na=False))
            .any(axis=1)
        )
        filtered_df = filtered_df[mask]

    if filter_type != "All Types" and "Submission Type" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Submission Type"] == filter_type]

    # Display results
    st.caption(
        f"📊 Showing {len(filtered_df)} of {len(df)} submissions "
        f"({len(df) - len(filtered_df)} filtered out)"
    )

    # Searchable/filterable dataframe
    st.dataframe(
        filtered_df.drop(columns=["ID"], errors="ignore"),
        hide_index=True,
        width="stretch",
        use_container_width=True,
    )

    # Export functionality
    st.markdown("---")
    export_col1, export_col2, export_col3 = st.columns([1, 1, 1])

    with export_col1:
        # CSV Export
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export as CSV",
            data=csv_data,
            file_name=f"submissions_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with export_col2:
        # Excel Export (if openpyxl available)
        try:
            from io import BytesIO

            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                filtered_df.to_excel(writer, index=False, sheet_name="Submissions")
            excel_data = output.getvalue()
            st.download_button(
                label="📊 Export as Excel",
                data=excel_data,
                file_name=f"submissions_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except ImportError:
            st.info("ℹ️ Excel export requires openpyxl package")


def render_admin_submissions(submission_types=None):
    if require_role("admin"):
        _render_saved_submissions(submission_types)


def strategic_committees_panel():
    st.markdown(
        """<div class="supervisor-header swing-in" style="font-size: 1.7rem; text-transform: uppercase;">🛡️ MODULE 13: STRATEGIC COMMITTEES (1-10) ACCESS GATEWAY</div>""",
        unsafe_allow_html=True,
    )

    selected_committee = st.selectbox(
        "Select Your Assigned Committee:", options=[""] + STRATEGIC_COMMITTEE_NAMES
    )

    if not selected_committee:
        return
    if not is_logged_in():
        render_login_prompt("committee membership")
        return
    if not has_committee_access(selected_committee):
        st.error("Your account is not authorized for the selected committee.")
        return

    st.markdown(f"### 📋 Member Registration for: {selected_committee}")
    with st.form(key=f"strategic_reg_form_{selected_committee}", clear_on_submit=False):
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
            width="stretch",
        ):
            final_ward = manual_ward.strip() if manual_ward.strip() else selected_ward
            if not all(
                [
                    member_name,
                    member_phone,
                    selected_ward,
                    final_ward,
                    nin_number,
                    pvc_number,
                    account_name,
                    account_number,
                    bank_name,
                ]
            ):
                st.error("Complete all member, identity, location, and bank fields.")
            elif len(nin_number) != 11 or not nin_number.isdigit():
                st.error("NIN must contain exactly 11 digits.")
            elif len(account_number) != 10 or not account_number.isdigit():
                st.error("Account number must contain exactly 10 digits.")
            elif not _valid_phone(member_phone):
                st.error("Enter a valid contact phone number.")
            elif not nin_slip or not captured_image:
                st.error(
                    "Upload the NIN slip and provide the requested biometric capture."
                )
            else:
                saved = _commit_submission(
                    "committee_member",
                    {
                        "committee": selected_committee,
                        "name": member_name.strip(),
                        "phone": member_phone.strip(),
                        "lga": selected_lga,
                        "ward": final_ward,
                        "nin": nin_number,
                        "voter_id": pvc_number.strip(),
                        "account_name": account_name.strip(),
                        "account_number": account_number,
                        "bank": bank_name.strip(),
                    },
                    uploads={
                        "nin_slip": nin_slip,
                        "biometric_capture": captured_image,
                    },
                    dedupe_fields=["nin"],
                )
                if saved:
                    st.success(
                        f"{member_name} was registered for {selected_committee}."
                    )
                    st.balloons()

    st.markdown(f"#### Registered Members for: {selected_committee}")
    try:
        records = list_submissions(["committee_member"])
    except PersistenceError as exc:
        st.error(str(exc))
    else:
        if records is None:
            return
        members = [
            {
                "Name": record["payload"].get("name"),
                "Phone": record["payload"].get("phone"),
                "LGA": record["payload"].get("lga"),
                "Ward": record["payload"].get("ward"),
                "Created At": record["created_at"],
            }
            for record in records
            if record["payload"].get("committee") == selected_committee
        ]
        st.dataframe(pd.DataFrame(members), hide_index=True, width="stretch")


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

        if st.form_submit_button("🚀 Transmit Message to Leader", width="stretch"):
            final_ward = manual_ward.strip() if manual_ward.strip() else selected_ward
            if not (full_name and message_body and final_ward):
                st.error(
                    "⚠️ Please fill in your Name, Ward, and Message before transmitting."
                )
            elif not _valid_phone(phone_num):
                st.error("Enter a valid contact phone number.")
            else:
                saved = _commit_submission(
                    "speak_direct",
                    {
                        "name": full_name.strip(),
                        "phone": phone_num.strip(),
                        "lga": selected_lga,
                        "ward": final_ward,
                        "subject": subject.strip(),
                        "message": message_body.strip(),
                    },
                )
                if saved:
                    st.success("Your message was saved for review.")
                    st.balloons()


def render_committee_compliance_form():
    if not require_role("admin"):
        return

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
            "🔒 Transmit Report to Executive Control Room", width="stretch"
        ):
            if not (
                officer_name.strip()
                and regional_scope.strip()
                and activity_summary.strip()
            ):
                st.error(
                    "Provide the reporting official, location, and activity summary."
                )
            else:
                saved = _commit_submission(
                    "committee_compliance",
                    {
                        "committee_group": committee_group,
                        "officer_name": officer_name.strip(),
                        "regional_scope": regional_scope.strip(),
                        "activity_summary": activity_summary.strip(),
                        "expenditure_vouched": expenditure_vouched,
                    },
                )
                if saved:
                    st.success(
                        f"Report for {officer_name} was saved under {committee_group.split(':')[0]}."
                    )
                    st.balloons()


def render_election_analytical_sync():
    if not require_role("admin"):
        return

    st.markdown("### \U0001F4CA LIVE ELECTION ANALYTICAL SYNC DISPLAY")
    try:
        records = list_submissions(["polling_unit_tally", "ward_collation"])
    except PersistenceError as exc:
        st.error(str(exc))
        return

    if records is None:
        return
    if not records:
        st.info("No polling-unit or ward collation tallies have been recorded yet.")
        return

    rows = []
    tot_apc = tot_pdp = tot_ndc = tot_adc = 0
    for r in records:
        pl = r.get("payload", {})
        rt = r.get("submission_type", "polling_unit_tally")
        if rt == "ward_collation" or "APC_Votes" in pl:
            apc = int(pl.get("APC_Votes", 0) or 0)
            pdp = int(pl.get("PDP_Votes", 0) or 0)
            ndc = int(pl.get("NDC_Votes", 0) or 0)
            adc = int(pl.get("ADC_Votes", 0) or 0)
            acc = int(pl.get("Accredited_Voters", 0) or 0)
            lga = pl.get("LGA")
            ward = pl.get("Ward")
            bvas = pl.get("BVAS_Serial_Number")
            off = pl.get("Supervisor")
            tier = "Ward Collation (EC8A)"
        else:
            pv = pl.get("party_votes", {})
            apc = int(pv.get("APC", 0) or 0)
            pdp = int(pv.get("PDP", 0) or 0)
            ndc = int(pv.get("NDC", 0) or 0)
            adc = int(pv.get("ADC", 0) or 0)
            acc = int(pl.get("accredited_voters", 0) or 0)
            lga = pl.get("lga")
            ward = pl.get("ward")
            bvas = pl.get("bvas_serial")
            off = pl.get("officer_name")
            tier = pl.get("election_tier", "Polling Unit Tally")

        tot_apc += apc
        tot_pdp += pdp
        tot_ndc += ndc
        tot_adc += adc
        rows.append(
            {
                "Timestamp": r.get("created_at"),
                "Source Feed": tier,
                "LGA": lga,
                "Ward": ward,
                "BVAS S/N": bvas,
                "Officer": off,
                "Accredited": acc,
                "APC": apc,
                "PDP": pdp,
                "NDC": ndc,
                "ADC": adc,
                "Total Valid": apc + pdp + ndc + adc,
            }
        )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Reports", f"{len(rows):,}")
    c2.metric("APC Total", f"{tot_apc:,}")
    c3.metric("PDP Total", f"{tot_pdp:,}")
    c4.metric("NDC Total", f"{tot_ndc:,}")
    c5.metric("ADC Total", f"{tot_adc:,}")

    chart_df = pd.DataFrame(
        {"Party": ["APC", "PDP", "NDC", "ADC"], "Votes": [tot_apc, tot_pdp, tot_ndc, tot_adc]}
    ).set_index("Party")
    st.bar_chart(chart_df)
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

    st.markdown("---")
    st.markdown("### \U0001F5F3\uFE0F ELECTION WAR ROOM (SECURE ADMIN ONLY)")
    render_election_war_room()


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
    st.markdown("### Verified Federal & Constituency Recruitment Listings")
    st.markdown(
        "Official employment opportunities, federal agency placements, and constituency empowerment programs."
    )
    listings = [
        {
            "title": "Federal Ministries, Departments & Agencies (MDA) Regularization Batch",
            "category": "Federal Civil Service",
            "deadline": "Active - Open for Verification",
            "status": "Verified Active",
            "description": "Verification window for constituents nominated under federal manpower development and specialized MDAs.",
            "slots": "150 Allocated Slots",
        },
        {
            "title": "Constituency ICT & Digital Skills Empowerment Training",
            "category": "Capacity Building",
            "deadline": "Ongoing Registration",
            "status": "Open for Applications",
            "description": "Hands-on technical training program covering software development, data analytics, and digital entrepreneurship.",
            "slots": "300 Trainee Slots",
        },
        {
            "title": "Agricultural Mechanization & Agro-Allied Support Scheme",
            "category": "Agric & Rural Enterprise",
            "deadline": "Next Batch Commencing Soon",
            "status": "Verification in Progress",
            "description": "Distribution of improved seedlings, fertilizers, and modern farming implements for registered farmers cooperatives.",
            "slots": "Cooperative Level",
        },
    ]
    for item in listings:
        with st.container():
            st.markdown(f"**{item['title']}**")
            cols = st.columns(3)
            cols[0].caption(f"**Category:** {item['category']}")
            cols[1].caption(f"**Status:** {item['status']}")
            cols[2].caption(f"**Timeline:** {item['deadline']}")
            st.write(item["description"])
            st.info(f"**Scope:** {item['slots']}")
            st.divider()
    st.success(
        "To verify your application status or submit required credentials, use the Candidate Verification portal tab."
    )


@st.cache_data(ttl=3600, show_spinner="Loading verified federal grants...")
def _load_federal_grants_cached():
    """Cache verified federal grants for 1 hour."""
    return FEDERAL_INDUSTRIAL_GRANTS


def render_grants_verification_panel():
    """
    📂 FEDERAL INDUSTRIAL GRANTS & SCHEMES VERIFICATION PORTAL
    Displays verified, active Nigerian Federal Government industrial grants
    with direct application links and eligibility information.
    """
    st.header("📂 Federal Industrial Grants & Schemes Portal")
    st.caption(
        "Verified active federal government intervention programs for Nigerian MSMEs, startups, and exporters. "
        "Always verify eligibility and application requirements directly with the implementing agency."
    )
    st.warning(
        "🔐 **Security Vetting Advisory:** Authentic federal government schemes will **never** demand processing fees, "
        "bank account details, or your NIN/card PIN codes upfront. Verify all communications through official portals only."
    )
    st.write("---")

    # Load grants
    grants = _load_federal_grants_cached()

    if not grants:
        st.info("No verified grant listings are currently available. Please check back soon.")
        return

    # Search & Filter Controls
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input(
            "🔍 Search grants",
            placeholder="Search by title, agency, or keywords...",
            key="grants_search",
        )
    with col2:
        filter_agency = st.selectbox(
            "Filter by implementing agency",
            options=["All Agencies"] + sorted(list(set(g["agency"] for g in grants))),
            key="grants_filter",
        )

    # Apply filters
    filtered_grants = grants
    if search_term:
        search_lower = search_term.lower()
        filtered_grants = [
            g
            for g in filtered_grants
            if search_lower in g["title"].lower()
            or search_lower in g["agency"].lower()
            or search_lower in g["description"].lower()
            or search_lower in " ".join(g.get("key_requirements", [])).lower()
        ]

    if filter_agency != "All Agencies":
        filtered_grants = [g for g in filtered_grants if g["agency"] == filter_agency]

    # Display metrics
    st.markdown(f"**📊 Showing {len(filtered_grants)} of {len(grants)} grants**")
    st.write("---")

    # Render grants as high-contrast cards
    if not filtered_grants:
        st.info("No grants match your search. Try different keywords or filters.")
        return

    for grant in filtered_grants:
        # Build requirements list HTML
        reqs_html = "\n".join(
            f"<li style='color: #F7FAFC;'>{html.escape(req)}</li>"
            for req in grant.get("key_requirements", [])
        )

        # Create card HTML without leading indentation
        card_html = textwrap.dedent(f"""\
<div style="background: linear-gradient(135deg, #12161F 0%, #0E1117 100%); border: 1px solid #D4AF37; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.1);">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
<div>
<h3 style="color: #FFFFFF; margin: 0 0 4px 0; font-size: 18px; font-weight: 600;">{html.escape(grant['title'])}</h3>
<p style="color: #D4AF37; margin: 0; font-size: 13px; font-weight: 500;">{html.escape(grant['agency'])}</p>
</div>
<span style="background: #D4AF37; color: #0E1117; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;">{grant['status']}</span>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #D4AF37; opacity: 0.9;">
<div>
<p style="color: #A0AEC0; margin: 0 0 4px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Funding Type</p>
<p style="color: #FFFFFF; margin: 0; font-size: 14px; font-weight: 500;">{html.escape(grant['funding_type'])}</p>
</div>
<div>
<p style="color: #A0AEC0; margin: 0 0 4px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Funding Amount</p>
<p style="color: #D4AF37; margin: 0; font-size: 14px; font-weight: 600;">{html.escape(grant['funding_amount'])}</p>
</div>
</div>
<p style="color: #F7FAFC; margin: 0 0 12px 0; font-size: 14px; line-height: 1.6;">{html.escape(grant['description'])}</p>
<div style="margin-bottom: 12px;">
<p style="color: #A0AEC0; margin: 0 0 6px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Eligibility</p>
<p style="color: #F7FAFC; margin: 0; font-size: 13px; line-height: 1.5;">{html.escape(grant['eligibility'])}</p>
</div>
<div style="margin-bottom: 16px;">
<p style="color: #A0AEC0; margin: 0 0 8px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Key Requirements</p>
<ul style="color: #F7FAFC; margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.6;">
{reqs_html}
</ul>
</div>
</div>""")

        # Render card
        st.markdown(card_html, unsafe_allow_html=True)

        # Application button row
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.link_button(
                "🔗 Apply on Official Portal",
                url=grant["application_url"],
                help=f"Direct link to {grant['agency']} application portal",
                use_container_width=True,
            )
        with col2:
            st.caption(f"Updated: {grant['updated']}")
        with col3:
            st.caption(grant["status"])

        st.write("")  # Spacing


def render_top_vacancy_alerts():
    st.caption("Live federal vacancy alerts are not currently available.")


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
