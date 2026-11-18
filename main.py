# ==============================================================================
# 🏛️ LSOEP PORTAL PLATFORM ENGINE - SECURE ROUTER MATRICES
# Project: Balanga/Billiri Federal Constituency (Honourable Ali Isa JC, PhD)
# File: main.py (V95.0 - Bulletproof Self-Healing Architecture)
# ==============================================================================

import sys
import os
import io
import asyncio
import threading
import warnings
import streamlit as st
import pandas as pd

from auth import clear_passcode_access, is_logged_in, require_role
from persistence import PersistenceError, list_submissions, submit_submission

# --- 1. SEPARATED ROLE-BASED STATE INITIALIZATION ENGINE ---
if "current_route" not in st.session_state:
    st.session_state.current_route = "HOME"

if sys.platform == "win32":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from styling import inject_custom_css
from ui_modules import render_hero_banner, render_marquee_header
from registry import initialize_system_states, HON_TITLE, HON_ALI_SPONSORED_BILLS
import panels
from panels.recruitment_panel import render_recruitment_panel


@st.cache_resource
def _pdfium_lock():
    return threading.Lock()


def _logout_if_logged_in():
    if is_logged_in():
        st.logout()


# --- 2. PREMIUM VISUAL CANVAS PLATFORM SETUP ---
st.set_page_config(
    page_title="LSOEP - Balanga/Billiri Federal Constituency",
    page_icon=":material/account_balance:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ENTERPRISE UI BRANDING & SECURITY SANITIZATION ---
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none !important;}
    div[data-testid="stToolbar"] {visibility: hidden; display: none !important;}
    div[data-testid="stDecoration"] {visibility: hidden; display: none !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

inject_custom_css()
initialize_system_states()

# --- 3. SYSTEM MODULE PATHWAYS (UPDATED WITH ALL 13 ACTIVE HUBS) ---
NAVIGATION_OPTIONS = [
    "🚀 LEGISLATIVE PROGRESS TRACKER",
    "🏛️ BEYOND RHETORICS PROJECT EXECUTION",
    "🗣️ SPEAK WITH HON. ALI ISA JC DIRECTLY",
    "🛡️ STRATEGIC COMMITTEES (MODULE 13)",
    "🏛️ LEGISLATIVE FOOTPRINTS",
    "🛠️ SKILL VOCATION POOL",
    "🎓 STUDENT SCHOLARSHIP/GRANT",
    "🔍 JOB VACANCY VERIFICATION",
    "📂 FEDERAL & INDUSTRIAL GRANTS",
    "📦 PALLIATIVE ENROLLMENT",
    "💡 CV & ARTISAN VAULT",
    "🚨 COMMUNITY URGENT NEED",
    "📜 CONSTITUENCY VOUCHING VERIFICATION",
    "🗳️ SECURE CONSTITUENCY VOTING",
]

# 🏛️ EXACT STRUCTURAL MATRIX TO MATCH INTERNAL PANELS.PY CALL STRINGS
ADMIN_COMMAND_HUBS = [
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
    "📋 Strategic Committee Progress Intake (M14)",
]

NAVIGATION_OPTIONS.extend(["Jobs Vacancy & Federal Grants"])

restricted_routes = {
    "ADMIN_GATEWAY_CHECKPOINT",
    "ADMIN_HUB_DASHBOARD",
    "DIRECT_AGENT_GATE",
    "STANDALONE_AGENT_INPUT_SCREEN",
    "DIRECT_COLLATION_GATE",
    "DIRECT_COLLATION_SCREEN",
}
initial_route = st.session_state.current_route
is_restricted_route = initial_route in restricted_routes or any(
    initial_route.endswith(module) or module in initial_route
    for module in ADMIN_COMMAND_HUBS
)
if "announcement_loaded" not in st.session_state and not is_restricted_route:
    default_announcement = (
        f"Welcome to the official constituency outreach portal of {HON_TITLE}. "
        "This platform is designed for transparency, accountability, and direct engagement."
    )
    try:
        saved_announcements = list_submissions(["announcement"], limit=1)
    except PersistenceError as exc:
        st.session_state.global_scrolling_announcement = default_announcement
        st.warning(f"The saved announcement could not be loaded: {exc}")
    else:
        st.session_state.global_scrolling_announcement = (
            saved_announcements[0]["payload"].get("message", default_announcement)
            if saved_announcements
            else st.session_state.get(
                "global_scrolling_announcement", default_announcement
            )
        )
    st.session_state.announcement_loaded = True

# --- 4. SIDEBAR ACCESS CONTROL PORTALS ---
st.sidebar.markdown(
    f"""<a href="#" target="_blank" class="inst-link-box">🌐 {HON_TITLE} Official Facebook</a>""",
    unsafe_allow_html=True,
)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<h3 class='admin-header'>System Access Portals</h3>", unsafe_allow_html=True
)

if st.sidebar.button(
    "🔑 EXECUTIVE CONTROL ROOM & HUBS", width="stretch", key="side_btn_admin_main"
):
    st.session_state.current_route = "ADMIN_GATEWAY_CHECKPOINT"
    st.rerun()

if st.sidebar.button(
    "🗳️ POLLING UNIT AGENT PORTAL", width="stretch", key="side_btn_agent_direct"
):
    st.session_state.current_route = "DIRECT_AGENT_GATE"
    st.rerun()

if st.sidebar.button(
    "🛡️ WARD COLLATION OFFICER HUB", width="stretch", key="side_btn_collation_direct"
):
    st.session_state.current_route = "DIRECT_COLLATION_GATE"
    st.rerun()

st.sidebar.caption("Engine Architecture: v95.0 | Safe-Guard Core Build")
if is_logged_in():
    st.sidebar.caption(f"Signed in as {st.user.get('email', 'user')}")
    if st.sidebar.button("Sign out", key="oidc_logout"):
        st.session_state.current_route = "HOME"
        clear_passcode_access()
        st.logout()

# --- 5. GLOBAL MAIN VIEWPORT MATRIX ---
selected_route = st.session_state.current_route

# ==============================================================================
# VIEW 1: PUBLIC GATEWAY DASHBOARD CHANNELS
# ==============================================================================
if selected_route == "HOME":
    # 🏛️ STICKY PREMIUM WELCOME ANCHOR (UNTOP OF HERO BANNER CONTAINER)
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px; padding: 5px 0;">
            <h3 style="font-family: 'Cabinet Grotesk', 'Space Grotesk', sans-serif !important; font-weight: 800 !important; font-size: 1.35rem !important; letter-spacing: -0.01em !important; text-transform: none; margin: 0 !important; color: #FDF1C7 !important;">
                Hon Ali Isa JC PhD welcomes you to this 
                <span style="background: linear-gradient(135deg, #FFF6D6 0%, #D4AF37 60%, #AA7C11 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">
                    "ENGAGING CONSTITUENCY ENGAGEMENT PORTAL"
                </span>
            </h3>
            <p style="font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; font-size: 0.82rem !important; letter-spacing: 0.12em !important; text-transform: uppercase; color: #00E5FF !important; margin: 5px 0 0 0 !important; opacity: 0.95;">
                🚀 LETS KEEP WINNING TOGETHER
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_hero_banner()

    # ⚡ SHIFT MARQUEE DOWNWARD VIA STRUCTURAL HEADROOM MARGIN SPACING
    st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True)

    render_marquee_header()

    # Render Background Fragment Alerts if they exist in panels
    if hasattr(panels, "render_top_vacancy_alerts"):
        panels.render_top_vacancy_alerts()

    st.markdown(
        "<h2 class='nav-title' style='margin-top: 55px !important; color: #D4AF37 !important;'>CONSTITUENCY ENGAGEMENT CHANNELS</h2>",
        unsafe_allow_html=True,
    )
    cols = st.columns(4)
    for i, option in enumerate(NAVIGATION_OPTIONS):
        if cols[i % len(cols)].button(option, key=f"nav_card_{i}", width="stretch"):
            st.session_state.current_route = option
            st.rerun()

# ==============================================================================
# VIEW 2: UNIFIED CONTROL ROOM ACCESS CHECKPOINT
# ==============================================================================
elif selected_route == "ADMIN_GATEWAY_CHECKPOINT":
    render_marquee_header()
    st.markdown("### Executive Control Room")
    if require_role("admin"):
        st.session_state.current_route = "ADMIN_HUB_DASHBOARD"
        st.rerun()
    if st.button("Return Home", key="gate_admin_cancel"):
        st.session_state.current_route = "HOME"
        st.rerun()

# ==============================================================================
# VIEW 3: ADMINISTRATIVE COMMAND HUBS GRAPHICS DASHBOARD
# ==============================================================================
elif selected_route == "ADMIN_HUB_DASHBOARD":
    if not require_role("admin"):
        st.stop()

    render_marquee_header()
    st.markdown(
        "<h2 class='nav-title' style='color: #D4AF37 !important;'>🏛️ EXECUTIVE ADMINISTRATIVE COMMAND HUBS</h2>",
        unsafe_allow_html=True,
    )

    st.markdown("### 📈 Real-Time Operational Telemetry Stream")

    try:
        saved_records = list_submissions()
    except PersistenceError as exc:
        st.error(f"Administrative telemetry is unavailable: {exc}")
        saved_records = None

    sync_metrics = {}
    if saved_records is not None:
        if not saved_records:
            st.info("No saved submissions are available yet.")

        record_counts = {}
        for record in saved_records:
            record_counts[record["submission_type"]] = (
                record_counts.get(record["submission_type"], 0) + 1
            )
        sync_metrics = {
            "Master Registry Matrix": sum(
                record_counts.get(kind, 0)
                for kind in [
                    "palliative_direct",
                    "palliative_vouching",
                    "skill_application",
                    "scholarship_application",
                    "cv_application",
                ]
            ),
            "Citizen Feedback": record_counts.get("speak_direct", 0),
            "Admin Announcement Control": record_counts.get("announcement", 0),
            "Database Audit Diagnostics": len(saved_records),
            "Scholar Talent Matrix": record_counts.get("scholarship_application", 0),
            "Live Election Analytical Sync": record_counts.get("polling_unit_tally", 0),
            "Ground Truth Form EC8A Data": record_counts.get("ward_collation", 0),
            "Legislative Progress Tracker": len(HON_ALI_SPONSORED_BILLS),
            "Strategic Committee Progress Intake (M14)": record_counts.get(
                "committee_compliance", 0
            ),
        }

        chart_df = pd.DataFrame(
            [
                {"Module Command Hub": name, "Active Structural Records": count}
                for name, count in sync_metrics.items()
            ]
        )

        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.markdown("#### 📊 Absolute System Transaction Volumes")
            st.bar_chart(
                data=chart_df,
                x="Module Command Hub",
                y="Active Structural Records",
                horizontal=True,
                width="stretch",
            )

        with v_col2:
            st.markdown("#### 🧩 Executive Operational Resource Allocation")
            st.dataframe(
                chart_df.sort_values(by="Active Structural Records", ascending=False),
                column_config={
                    "Module Command Hub": "Administrative Core Segment",
                    "Active Structural Records": st.column_config.ProgressColumn(
                        "Saturation Density", format="%d", min_value=0, max_value=1500
                    ),
                },
                hide_index=True,
                width="stretch",
            )

    st.markdown("---")
    st.markdown("### 🎛️ Command Activation Grid Matrix")

    cols = st.columns(4)
    for i, module_title in enumerate(ADMIN_COMMAND_HUBS):
        metric_key = [
            k for k in sync_metrics.keys() if module_title in k or k in module_title
        ]
        count_suffix = f" ({sync_metrics[metric_key[0]]})" if metric_key else ""

        if cols[i % len(cols)].button(
            f"{module_title}{count_suffix}", key=f"admin_grid_card_{i}", width="stretch"
        ):
            st.session_state.current_route = module_title
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button(
        "↩️ Close Admin Hub and Logout", width="stretch", key="admin_hub_logout_btn"
    ):
        st.session_state.current_route = "HOME"
        clear_passcode_access()
        _logout_if_logged_in()
        st.rerun()

# ==============================================================================
# VIEW 4: DIRECT FIELD AGENT GATEWAY
# ==============================================================================
elif selected_route == "DIRECT_AGENT_GATE":
    render_marquee_header()
    st.markdown("### 🔒 Polling Unit Agent Portal Access Checkpoint")
    if require_role("agent"):
        st.session_state.current_route = "STANDALONE_AGENT_INPUT_SCREEN"
        st.rerun()
    if st.button("Return Home", key="gate_agent_cancel"):
        st.session_state.current_route = "HOME"
        st.rerun()

# ==============================================================================
# VIEW 5: STANDALONE ISOLATED FIELD AGENT ENVELOPE
# ==============================================================================
elif selected_route == "STANDALONE_AGENT_INPUT_SCREEN":
    if not require_role("agent"):
        st.stop()

    render_marquee_header()
    st.markdown(
        "<h2 style='color: #D4AF37;'>🗳️ POLLING UNIT AGENT: FIELD DATA TRANSFERS</h2>",
        unsafe_allow_html=True,
    )
    st.info(
        "⚡ Ingestion Stream Active: Execute data snaps and camera capture forms cleanly."
    )
    st.markdown("---")

    panels.agent_panel()

    st.markdown("---")
    if st.button("↩️ Securely Terminate Agent Session & Exit", width="stretch"):
        st.session_state.current_route = "HOME"
        clear_passcode_access()
        _logout_if_logged_in()
        st.rerun()

# ==============================================================================
# VIEW 6: DIRECT WARD COLLATION GATEWAY
# ==============================================================================
elif selected_route == "DIRECT_COLLATION_GATE":
    render_marquee_header()
    st.markdown("### 🛡️ Ward Collation Command Security Checkpoint")
    if require_role("collation"):
        st.session_state.current_route = "DIRECT_COLLATION_SCREEN"
        st.rerun()
    if st.button("Return Home", key="gate_collation_cancel"):
        st.session_state.current_route = "HOME"
        st.rerun()

elif selected_route == "DIRECT_COLLATION_SCREEN":
    if not require_role("collation"):
        st.stop()
    render_marquee_header()
    if st.button("Return Home", key="collation_return_home"):
        st.session_state.current_route = "HOME"
        clear_passcode_access()
        st.rerun()
    panels.ward_collation_officer_panel()

# ==============================================================================
# VIEW 7: MULTI-CHANNEL INTERFACE ROUTING ENGINE
# ==============================================================================
else:
    is_admin_module = selected_route in ADMIN_COMMAND_HUBS or any(
        selected_route.endswith(m) or m in selected_route for m in ADMIN_COMMAND_HUBS
    )
    if is_admin_module and not require_role("admin"):
        st.stop()
    render_marquee_header()
    back_label = (
        "↩ ... Return to Admin Hub Matrix"
        if is_admin_module
        else "↩ ... Return to Main Gateway"
    )

    if st.button(back_label, width="stretch", key="global_return_nav_btn"):
        st.session_state.current_route = (
            "ADMIN_HUB_DASHBOARD" if is_admin_module else "HOME"
        )
        st.rerun()

    st.markdown("<hr class='nav-divider'>", unsafe_allow_html=True)

    exec_target = selected_route

    # --- Public Channel Execution Interface ---
    if selected_route == "🚀 LEGISLATIVE PROGRESS TRACKER":
        panels.render_progress_tracker()

    # --- BEYOND RHETORICS SUBFOLDER MEDIA CANVAS SWITCHER ENGINE ---
    elif selected_route == "🏛️ BEYOND RHETORICS PROJECT EXECUTION":
        st.markdown("## 🦅 BEYOND RHETORICS: PROJECT VERIFICATION HUB")
        st.caption(
            "Reviewing scanned performance sheets and ground-truth validation archives for Hon. Ali Isa."
        )

        MEDIA_FOLDER = os.path.join(os.getcwd(), "MEDIA MEDIA MEDIA")

        document_map = {
            "📖 Document Cover Page": "Cover_compressed.pdf",
            "📄 Page 1 - Project Milestone Overview": "1_compressed.pdf",
            "📄 Page 2 - Infrastructure & Capital Allocations": "2_compressed.pdf",
            "📄 Page 3 - Educational Interventions & Grants": "3_compressed.pdf",
            "📄 Page 4 - Healthcare Programs & Welfare Sync": "4_compressed.pdf",
            "📄 Page 5 - Empowerment Schemes Registry": "5_compressed.pdf",
            "📄 Page 6 - Verifiable Performance Conclusion": "6_compressed.pdf",
        }

        st.markdown("### 🗂️ Select Verification Page to Display")
        selected_doc_label = st.selectbox(
            "Choose a ledger segment:", list(document_map.keys())
        )

        target_filename = document_map[selected_doc_label]
        BUNDLE_PATH = os.path.join(MEDIA_FOLDER, target_filename)

        if os.path.exists(BUNDLE_PATH):
            try:
                import pypdfium2 as pdfium
            except ImportError as exc:
                st.error(f"The PDF viewer is unavailable: {exc}")
                st.stop()

            @st.cache_data(show_spinner=False)
            def get_pdf_page_count(pdf_bytes: bytes) -> int:
                with _pdfium_lock():
                    with pdfium.PdfDocument(pdf_bytes) as pdf:
                        return len(pdf)

            @st.cache_data(show_spinner=False, max_entries=20)
            def render_pdf_page(pdf_bytes: bytes, page_index: int) -> bytes:
                with _pdfium_lock():
                    with pdfium.PdfDocument(pdf_bytes) as pdf:
                        page = pdf[page_index]
                        try:
                            bitmap = page.render(scale=2.0)
                            try:
                                image = bitmap.to_pil()
                                if image.mode != "RGB":
                                    image = image.convert("RGB")
                                with io.BytesIO() as image_bytes:
                                    image.save(image_bytes, format="PNG")
                                    return image_bytes.getvalue()
                            finally:
                                bitmap.close()
                        finally:
                            page.close()

            try:
                with open(BUNDLE_PATH, "rb") as f:
                    pdf_bytes = f.read()
            except OSError as exc:
                st.error(f"The document could not be read: {exc}")
                st.stop()

            col1, col2 = st.columns([3, 1])
            with col1:
                st.success(f"Connected to: **MEDIA MEDIA MEDIA/{target_filename}**")
            with col2:
                st.download_button(
                    label="📥 Download Official Copy",
                    data=pdf_bytes,
                    file_name=target_filename,
                    mime="application/pdf",
                    width="stretch",
                )

            st.divider()

            try:
                total_pages = get_pdf_page_count(pdf_bytes)

                if total_pages > 0:
                    page_state_key = f"page_idx_{target_filename}"
                    if page_state_key not in st.session_state:
                        st.session_state[page_state_key] = 0

                    curr_idx = max(
                        0, min(st.session_state[page_state_key], total_pages - 1)
                    )
                    st.session_state[page_state_key] = curr_idx

                    nav_c1, nav_c2, nav_c3 = st.columns([1, 2, 1])
                    with nav_c1:
                        if st.button(
                            "◀ Previous Page",
                            disabled=(curr_idx == 0),
                            width="stretch",
                            key=f"prev_{target_filename}",
                        ):
                            st.session_state[page_state_key] = curr_idx - 1
                            st.rerun()
                    with nav_c2:
                        st.markdown(
                            f"<div style='text-align:center; padding-top:6px; font-weight:600; color:#D4AF37;'>"
                            f"Page {curr_idx + 1} of {total_pages}</div>",
                            unsafe_allow_html=True,
                        )
                    with nav_c3:
                        if st.button(
                            "Next Page ▶",
                            disabled=(curr_idx == total_pages - 1),
                            width="stretch",
                            key=f"next_{target_filename}",
                        ):
                            st.session_state[page_state_key] = curr_idx + 1
                            st.rerun()

                    st.image(render_pdf_page(pdf_bytes, curr_idx), width="stretch")
                else:
                    st.warning("This document contains no readable pages.")
            except (pdfium.PdfiumError, OSError, ValueError) as exc:
                st.error(f"Error rendering document pages: {exc}")
        else:
            st.error(
                f"❌ PATH LOOKUP ERROR: Could not locate target file at path: {BUNDLE_PATH}"
            )
            st.write("Checking directory layout configuration...")
            if os.path.exists(MEDIA_FOLDER):
                st.write("Files found inside your folder:", os.listdir(MEDIA_FOLDER))
            else:
                st.write(
                    "🚨 'MEDIA MEDIA MEDIA' folder path cannot be identified from your app root position."
                )

    elif selected_route == "🗣️ SPEAK WITH HON. ALI ISA JC DIRECTLY":
        panels.render_speak_directly_panel()
    elif selected_route == "🛡️ STRATEGIC COMMITTEES (MODULE 13)":
        panels.strategic_committees_panel()
    elif selected_route == "🏛️ LEGISLATIVE FOOTPRINTS":
        panels.render_sponsored_bills_panel()
    elif selected_route == "🛠️ SKILL VOCATION POOL":
        panels.render_skill_form()
    elif selected_route == "🎓 STUDENT SCHOLARSHIP/GRANT":
        panels.render_scholarship_form()

    # --- UPGRADED PORTAL CHANNELS DISPATCHED TO CUSTOM PANELS ENGINE ---
    elif selected_route == "🔍 JOB VACANCY VERIFICATION":
        panels.render_job_verification_panel()
    elif selected_route == "📂 FEDERAL & INDUSTRIAL GRANTS":
        panels.render_grants_verification_panel()
    elif selected_route == "📜 CONSTITUENCY VOUCHING VERIFICATION":
        panels.render_vouching_verification_panel()

    elif selected_route == "📦 PALLIATIVE ENROLLMENT":
        panels.render_palliative_form()
    elif selected_route == "💡 CV & ARTISAN VAULT":
        panels.render_cv_vault()
    elif selected_route == "🚨 COMMUNITY URGENT NEED":
        panels.render_cun_trigger()
    elif selected_route == "🗳️ SECURE CONSTITUENCY VOTING":
        panels.render_constituency_voting_panel()
    
    elif selected_route == "Jobs Vacancy & Federal Grants":
        is_admin = st.sidebar.toggle("Admin vetting", key="recruitment_admin_mode")
        render_recruitment_panel(is_admin_mode=is_admin)

    # --- 📢 MODULE 3: ADMIN ANNOUNCEMENT CONTROL ---
    elif exec_target == "Admin Announcement Control":
        st.markdown("### 📢 Executive Announcement Broadcasting Terminal")
        st.info(
            f"**Currently Active Marquee Line:** {st.session_state.global_scrolling_announcement}"
        )
        new_broadcast_msg = st.text_area(
            label="Type announcement text content:",
            value=st.session_state.global_scrolling_announcement,
            key="marquee_broadcast_input_field",
        )
        if st.button("🚀 Push Live to Portal Ticker", width="stretch"):
            if new_broadcast_msg.strip():
                try:
                    submit_submission(
                        "announcement", {"message": new_broadcast_msg.strip()}
                    )
                except PersistenceError as exc:
                    st.error(str(exc))
                else:
                    st.session_state.global_scrolling_announcement = (
                        new_broadcast_msg.strip()
                    )
                    st.success("The announcement was saved and published.")
                    st.rerun()

    elif exec_target == "Live Election Analytical Sync":
        panels.render_election_analytical_sync()

    # --- 🔒 MODULE 9: EXCLUSIVE GROUND TRUTH LITIGATION MODULE ---
    elif exec_target == "Ground Truth Form EC8A Data":
        panels.render_admin_submissions(["ward_collation", "polling_unit_tally"])

    # --- 📋 MODULE 14: STRATEGIC COMMITTEE PROGRESS INTAKE ---
    elif exec_target == "Strategic Committee Progress Intake (M14)":
        panels.render_committee_compliance_form()

    # --- 📐 SOLID STATE ROUTE MAPPINGS FOR INDIVIDUAL ADMIN TILES ---
    elif exec_target == "Master Registry Matrix":
        panels.render_admin_submissions(
            [
                "palliative_direct",
                "palliative_vouching",
                "skill_application",
                "scholarship_application",
                "cv_application",
                "committee_member",
            ]
        )
    elif exec_target == "Citizen Feedback":
        panels.render_admin_submissions(["speak_direct", "community_urgent_need"])
    elif exec_target == "Database Audit Diagnostics":
        panels.render_admin_submissions()
    elif exec_target == "RADAR Deduplication Interceptor":
        st.info(
            "The database enforces duplicate prevention per submission type and normalized identity. "
            "No separate duplicate-review queue is implemented yet."
        )
    elif exec_target == "Scholar Talent Matrix":
        panels.render_admin_submissions(
            ["skill_application", "scholarship_application", "cv_application"]
        )
    elif exec_target == "Legislative Progress Tracker":
        panels.render_progress_tracker()
    else:
        st.warning(
            f"{exec_target} is not implemented yet; no live data is available in this module."
        )


# --- RESTORED RECRUITMENT & EMPOWERMENT MODULE ---
