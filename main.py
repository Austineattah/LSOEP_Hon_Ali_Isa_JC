# ==============================================================================
# 🏛️ LSOEP PORTAL PLATFORM ENGINE - INTEGRATED MASTER ROUTER
# Project: Balanga and Billiri Federal Constituency (Hon. Ali Isa JC, PhD)
# File: main.py (V43.0 - Hardened Initialization & Crash Fix)
# ==============================================================================

import sys
import asyncio
import warnings
import streamlit as st

# --- 1. SUPER-EARLY STATE INITIALIZATION (CRITICAL CRASH PREVENTION) ---
# This block runs before almost anything else to guarantee 'current_route'
# exists on every single script run, preventing initialization crashes.
if "current_route" not in st.session_state:
    st.session_state.current_route = "HOME"

# --- Now, import other project modules ---
if sys.platform == "win32":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from styling import inject_custom_css
from ui_modules import render_hero_banner, render_marquee_header
from registry import initialize_system_states, HON_TITLE
import panels

# --- 2. PAGE CONFIG & STYLING ---
st.set_page_config(
    page_title="LSOEP - Hon. Ali Isa JC Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_custom_css()

# --- 3. STANDARD INITIALIZATIONS ---
initialize_system_states()

# --- 4. NAVIGATION SETUP ---
NAVIGATION_OPTIONS = [
    "🏛️ LEGISLATIVE FOOTPRINTS",
    "🛠️ SKILL VOCATION POOL",
    "🎓 STUDENT SCHOLARSHIP/GRANT",
    "📦 PALLIATIVE ENROLLMENT",
    "💡 CV & ARTISAN VAULT",
    "🚨 COMMUNITY URGENT NEED",
    "🏛️ BEYOND RHETORICS",
    "🗣️ SPEAK TO ME DIRECTLY",
    "🛡️ STRATEGIC LEADERSHIP VOUCHING TIER",
]
ADMIN_OPTIONS = {
    "CONTROL_ROOM": "🔑 EXECUTIVE CONTROL ROOM",
    "STRATEGIC_COMMITTEES": "🛡️ STRATEGIC COMMITTEES (MODULE 13)",
    "AGENT_HUB": "🗳️ POLLING UNIT AGENT HUB",
    "COLLATION_HUB": "🛡️ WARD COLLATION OFFICER HUB",
}

# --- 5. SIDEBAR RENDERING ---
st.sidebar.markdown(
    f"""<a href="https://web.facebook.com/hon.isa.ali.jc/?_rdc=1&_rdr#" target="_blank" class="inst-link-box">🌐 {HON_TITLE} Official Facebook</a>""",
    unsafe_allow_html=True,
)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<h3 class='admin-header'>Admin Portals</h3>", unsafe_allow_html=True
)

if st.sidebar.button(
    ADMIN_OPTIONS["CONTROL_ROOM"], use_container_width=True, key="nav_btn_admin"
):
    st.session_state.current_route = ADMIN_OPTIONS["CONTROL_ROOM"]
    st.rerun()
if st.sidebar.button(
    ADMIN_OPTIONS["STRATEGIC_COMMITTEES"],
    use_container_width=True,
    key="nav_btn_committee",
):
    st.session_state.current_route = ADMIN_OPTIONS["STRATEGIC_COMMITTEES"]
    st.rerun()
if st.sidebar.button(
    ADMIN_OPTIONS["AGENT_HUB"], use_container_width=True, key="nav_btn_agent"
):
    st.session_state.current_route = ADMIN_OPTIONS["AGENT_HUB"]
    st.rerun()
if st.sidebar.button(
    ADMIN_OPTIONS["COLLATION_HUB"], use_container_width=True, key="nav_btn_collation"
):
    st.session_state.current_route = ADMIN_OPTIONS["COLLATION_HUB"]
    st.rerun()

st.sidebar.caption("Engine Architecture: v43.0 | Hardened Router")

# --- 6. GLOBAL MARQUEE & ROUTER ---
render_marquee_header()
selected_route = st.session_state.current_route

if selected_route == "HOME":
    render_hero_banner()
    st.markdown(
        "<h2 class='nav-title'>CONSTITUENCY ENGAGEMENT CHANNELS........</h2>",
        unsafe_allow_html=True,
    )

    cols = st.columns(5)
    for i, option in enumerate(NAVIGATION_OPTIONS):
        if cols[i % len(cols)].button(
            option, key=f"nav_card_{i}", use_container_width=True
        ):
            st.session_state.current_route = option
            st.rerun()
else:
    if st.button(
        "↩️ Return to Main Gateway", use_container_width=True, key="nav_btn_return"
    ):
        st.session_state.current_route = "HOME"
        st.rerun()
    st.markdown("<hr class='nav-divider'>", unsafe_allow_html=True)

    # --- Render Content Panels ---
    if selected_route in [opt for opt in NAVIGATION_OPTIONS]:
        if selected_route == "🏛️ LEGISLATIVE FOOTPRINTS":
            panels.render_sponsored_bills_panel()
        elif selected_route == "🛠️ SKILL VOCATION POOL":
            panels.render_skill_form()
        elif selected_route == "🎓 STUDENT SCHOLARSHIP/GRANT":
            panels.render_scholarship_form()
        elif selected_route == "📦 PALLIATIVE ENROLLMENT":
            panels.render_palliative_form()
        elif selected_route == "💡 CV & ARTISAN VAULT":
            panels.render_cv_vault()
        elif selected_route == "🚨 COMMUNITY URGENT NEED":
            panels.render_cun_trigger()
        elif selected_route == "🏛️ BEYOND RHETORICS":
            panels.render_project_verifications()
        elif selected_route == "🗣️ SPEAK TO ME DIRECTLY":
            panels.render_speak_directly_panel()
        elif selected_route == "🛡️ STRATEGIC LEADERSHIP VOUCHING TIER":
            panels.render_vouching_form()

    # --- Render Admin Panels ---
    elif selected_route in ADMIN_OPTIONS.values():
        if selected_route == ADMIN_OPTIONS["CONTROL_ROOM"]:
            st.markdown("### 🔑 Executive Command System Authorization")
            admin_key = st.text_input(
                "Enter Command Hub Key:", type="password", key="admin_key"
            )
            if admin_key == "ali 2027":
                panels.main_dashboard(conn=None)
            elif admin_key:
                st.error("🛑 SYSTEM ACCESS REJECTED")

        elif selected_route == ADMIN_OPTIONS["STRATEGIC_COMMITTEES"]:
            panels.strategic_committees_panel()

        elif selected_route == ADMIN_OPTIONS["AGENT_HUB"]:
            st.markdown("### 🗳️ Polling Unit Agent Security Checkpoint")
            agent_key = st.text_input(
                "Enter Agent Authorization Key:", type="password", key="gate_agent_key"
            )
            if agent_key == "ali 2027":
                panels.agent_panel()
            elif agent_key:
                st.error("🛑 ACCESS REJECTED: Invalid Agent Authorization Signature.")

        elif selected_route == ADMIN_OPTIONS["COLLATION_HUB"]:
            st.markdown("### 🛡️ Ward Collation Command Security Checkpoint")
            collation_key = st.text_input(
                "Enter Collation Officer Key:",
                type="password",
                key="gate_collation_key",
            )
            if collation_key == "ali 2027":
                panels.ward_collation_officer_panel()
            elif collation_key:
                st.error("🛑 ACCESS REJECTED: Invalid Collation Authority Signature.")
