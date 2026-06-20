# ==============================================================================
# 🏛️ LSOEP MASTER PORTAL PLATFORM LIFE-CYCLE ENGINE
# Project: Balanga and Billiri Federal Constituency (Hon. Ali Isa JC, PhD)
# File: main.py — Lazy-Loading Sidebar Radio Router (Low Resource Overhead)
# ==============================================================================

import sys
import asyncio
import warnings
import streamlit as st

if sys.platform == "win32":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import styling

# 1. Initialize Page Config FIRST — must be the very first Streamlit command.
st.set_page_config(
    page_title="LSOEP TITAN GOMBE | HON. ALI ISA JC PhD HUB",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inject CSS Once Globally
styling.inject_custom_css()

# 3. Core session state (lightweight — registry.py itself is small, this is cheap)
from registry import initialize_system_states, HON_TITLE

initialize_system_states()

# 4. Initialize the Navigation State if it doesn't exist
MENU_OPTIONS = [
    "📊 Dashboard Overview",
    "🏛️ Legislative Footprints",
    "🛠️ Skill Vocation Pool",
    "🎓 Student Scholarship/Grant",
    "📦 Palliative Enrollment",
    "💡 CV & Artisan Vault",
    "🚨 Community Urgent Need",
    "📋 Voter Registry & NIN Sync",
    "🏛️ Project Verification",
    "🛡️ Strategic Committees (Module 13)",
    "🗳️ Polling Unit Agent Hub",
    "🛡️ Ward Collation Officer Hub",
    "🔑 Executive Control Room",
]

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "📊 Dashboard Overview"

# ==========================================
# SIDEBAR NAVIGATION (Low Resource Overhead)
# ==========================================
st.sidebar.markdown("### 🏛️ LSOEP CONTROL PANEL")

if st.session_state.get("radar_threat", False):
    st.sidebar.markdown(
        f"""<div style="background-color:#FF4B4B; color:white; padding:10px; border-radius:4px; font-weight:bold; font-size:12px; margin-bottom:10px;">
            🚨 SECURITY WARNING: ANTI-FRAUD RADAR MATCH<br>{st.session_state.get("threat_msg", "")}
        </div>""",
        unsafe_allow_html=True,
    )

st.sidebar.markdown(
    f"""<a href="https://web.facebook.com/hon.isa.ali.jc/?_rdc=1&_rdr#" target="_blank" style="text-decoration:none;">
    <div style="background-color:#0B3C5D; color:white; text-align:center; padding:8px; border-radius:4px; font-size:12px; font-weight:bold; margin-bottom:10px;">
        🌐 {HON_TITLE} Official Facebook
    </div>
</a>""",
    unsafe_allow_html=True,
)

selected_menu = st.sidebar.radio(
    "Navigation Menu",
    MENU_OPTIONS,
    index=MENU_OPTIONS.index(st.session_state.current_tab),
)
st.session_state.current_tab = selected_menu

st.sidebar.markdown("---")
st.sidebar.caption("Engine Architecture: v37.0.0 | Gombe Node — Lazy-Load Router")

# ==========================================
# THE DYNAMIC ROUTER (The Core Fix)
# Each branch imports ONLY what it needs, exactly when it's selected.
# ==========================================
current = st.session_state.current_tab

if current == "📊 Dashboard Overview":
    import ui_modules

    ui_modules.render_hero_banner()
    ui_modules.render_quick_stats()

elif current == "🏛️ Legislative Footprints":
    import ui_modules
    from panels import render_sponsored_bills_panel

    ui_modules.render_marquee_header()
    render_sponsored_bills_panel()

elif current == "🛠️ Skill Vocation Pool":
    import ui_modules
    from panels import render_skill_form

    ui_modules.render_marquee_header()
    render_skill_form()

elif current == "🎓 Student Scholarship/Grant":
    import ui_modules
    from panels import render_scholarship_form

    ui_modules.render_marquee_header()
    render_scholarship_form()

elif current == "📦 Palliative Enrollment":
    import ui_modules
    from panels import render_palliative_form

    ui_modules.render_marquee_header()
    render_palliative_form()

elif current == "💡 CV & Artisan Vault":
    import ui_modules
    from panels import render_cv_vault

    ui_modules.render_marquee_header()
    render_cv_vault()

elif current == "🚨 Community Urgent Need":
    import ui_modules
    from panels import render_cun_trigger

    ui_modules.render_marquee_header()
    render_cun_trigger()

elif current == "📋 Voter Registry & NIN Sync":
    # --- Heavy database code is deferred until clicked ---
    import registry

    st.title("Constituency Master Registry")
    registry.render_registry_management()

elif current == "🏛️ Project Verification":
    # --- Heavy 43MB PDF structures stay completely DORMANT until now ---
    import panels

    st.title("Project Verification Hub")
    panels.render_project_verifications()

elif current == "🛡️ Strategic Committees (Module 13)":
    import panels

    panels.strategic_committees_panel()

elif current == "🗳️ Polling Unit Agent Hub":
    import panels

    panels.agent_panel()

elif current == "🛡️ Ward Collation Officer Hub":
    import panels

    panels.ward_collation_officer_panel()

elif current == "🔑 Executive Control Room":
    import ui_modules

    ui_modules.render_marquee_header()
    st.markdown("### 🔑 Executive Command System Authorization Security Checkpoint")
    admin_key_input = st.text_input(
        "Enter Command Hub Key to Unroll Operational Data Logs:",
        type="password",
        key="checkpoint_admin_key",
    )
    if admin_key_input == "ali 2027":
        import panels

        conn = None
        panels.main_dashboard(conn)
    elif admin_key_input:
        st.error("🛑 SYSTEM ACCESS REJECTED: Command signature authorization mismatch.")
