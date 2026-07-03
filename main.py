# ==============================================================================
# 🏛️ LSOEP PORTAL PLATFORM ENGINE - INTEGRATED MASTER ROUTER
# Project: Balanga and Billiri Federal Constituency (Hon. Ali Isa JC, PhD)
# File: main.py (V51.0 - Native CSS Key Class Interceptor Engine)
# ==============================================================================

import sys
import asyncio
import warnings
import streamlit as st

# --- 1. SUPER-EARLY STATE INITIALIZATION (CRITICAL CRASH PREVENTION) ---
if "current_route" not in st.session_state:
    st.session_state.current_route = "HOME"

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
    "🏛️ BEYOND RHETORICS PROJECT EXECUTION",
    "🗣️ SPEAK TO ME DIRECTLY",
    "🛡️ LOCAL LEADERSHIP VOUCHING",
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

st.sidebar.caption("Engine Architecture: v51.0 | Native Class Target")

# --- 6. GLOBAL ROUTER ENGINE ---
selected_route = st.session_state.current_route

if selected_route == "HOME":
    render_hero_banner()
    render_marquee_header()

    st.markdown(
        "<h2 class='nav-title' style='margin-top: 25px !important;'>CONSTITUENCY ENGAGEMENT CHANNELS</h2>",
        unsafe_allow_html=True,
    )

    # 🎨 INJECT DYNAMIC ADAPTIVE INTERFACE AND KEY-LOCKED CONTINUOUS PULSING ANIMATIONS
    st.markdown(
        """
        <style>
            /* Apply uniform auto-height and wrap constraints to all gateway nodes */
            div.stButton > button {
                height: auto !important;
                min-height: 85px !important;
                white-space: normal !important;
                word-wrap: break-word !important;
                overflow-wrap: break-word !important;
                padding: 12px 10px !important;
                line-height: 1.3 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                transition: transform 0.4s ease-in-out, box-shadow 0.4s ease-in-out, background-color 0.4s !important;
            }
            div.stButton > button p {
                white-space: normal !important;
                word-wrap: break-word !important;
                overflow-wrap: break-word !important;
            }

            /* ✨ CONTINUOUS POP IN AND OUT BREATHING EMULSION KEYFRAMES */
            @keyframes compilerPulsePop {
                0% {
                    transform: scale(1.0);
                    box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.2);
                }
                50% {
                    transform: scale(1.04);
                    box-shadow: 0 6px 18px rgba(212, 175, 55, 0.45);
                    border: 1px solid #D4AF37 !important;
                    background-color: #041d3d !important;
                }
                100% {
                    transform: scale(1.0);
                    box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.2);
                }
            }

            /* 🎯 Target specific instances using compiler-generated st-key class maps */
            
            /* 1. LEGISLATIVE FOOTPRINTS (key: nav_card_0) */
            div.st-key-nav_card_0 button {
                animation: compilerPulsePop 2.5s infinite ease-in-out !important;
            }
            
            /* 2. BEYOND RHETORICS PROJECT EXECUTION (key: nav_card_6) */
            div.st-key-nav_card_6 button {
                animation: compilerPulsePop 2.5s infinite ease-in-out !important;
            }
            
            /* 3. SPEAK TO ME DIRECTLY (key: nav_card_7) */
            div.st-key-nav_card_7 button {
                animation: compilerPulsePop 2.5s infinite ease-in-out !important;
            }
        </style>
    """,
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
    render_marquee_header()
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
        elif selected_route == "🏛️ BEYOND RHETORICS PROJECT EXECUTION":
            panels.render_project_verifications()
        elif selected_route == "🗣️ SPEAK TO ME DIRECTLY":
            panels.render_speak_directly_panel()
        elif selected_route == "🛡️ LOCAL LEADERSHIP VOUCHING":
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
