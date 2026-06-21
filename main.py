# ==============================================================================
# 🏛️ LSOEP PORTAL PLATFORM ENGINE - INTEGRATED MASTER ROUTER
# Project: Balanga and Billiri Federal Constituency (Hon. Ali Isa JC, PhD)
# File: main.py (Optimized Lazy-Loading Framework Engine)
# ==============================================================================

import sys
import asyncio
import warnings
import streamlit as st

if sys.platform == "win32":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from styling import inject_custom_css
from ui_modules import render_hero_banner, render_marquee_header

# 1. Initialize Page Config FIRST — must be the very first Streamlit command.
st.set_page_config(
    page_title="LSOEP - Hon. Ali Isa JC Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inject Styling Layers Exactly Once at Root Entry
inject_custom_css()

# 3. Core session state (lightweight — registry.py itself is small, this is cheap)
from registry import initialize_system_states, HON_TITLE

initialize_system_states()

# ==============================================================================
# 🗺️ NAVIGATION SETUP & ALIGNMENT MATRIX
# ==============================================================================

# Precise 13-Module Ordering Hierarchy (Footprints Positioned First)
NAVIGATION_OPTIONS = [
    "🏛️ LEGISLATIVE FOOTPRINTS",
    "🛠️ SKILL VOCATION POOL",
    "🎓 STUDENT SCHOLARSHIP/GRANT",
    "📦 PALLIATIVE ENROLLMENT",
    "💡 CV & ARTISAN VAULT",
    "🚨 COMMUNITY URGENT NEED",
    "🏛️ BEYOND RHETORICS",
    "🛡️ STRATEGIC COMMITTEES (MODULE 13)",
    "🗳️ POLLING UNIT AGENT HUB",
    "🛡️ WARD COLLATION OFFICER HUB",
    "🔑 EXECUTIVE CONTROL ROOM",
]

# Ensure System Tracks State Cleanly Without Resource Exhaustion
if "current_route" not in st.session_state:
    st.session_state.current_route = NAVIGATION_OPTIONS[0]

# ==========================================
# 🎨 RENDER CONTAINERIZED SIDEBAR MENU GRID
# ==========================================
if st.session_state.get("radar_threat", False):
    st.sidebar.markdown(
        f"""<div style="background-color:#FF4B4B; color:white; padding:10px; border-radius:4px; font-weight:bold; font-size:12px; margin-bottom:10px;">
            🚨 SECURITY WARNING: ANTI-FRAUD RADAR MATCH<br>{st.session_state.get("threat_msg", "")}
        </div>""",
        unsafe_allow_html=True,
    )

st.sidebar.markdown(
    f"""<a href="https://web.facebook.com/hon.isa.ali.jc/?_rdc=1&_rdr#" target="_blank" style="text-decoration:none;">
    <div style="background-color:#0B3C5D; color:white; text-align:center; padding:8px; border-radius:4px; font-size:14px; font-weight:bold; margin-bottom:10px;">
        🌐 {HON_TITLE} Official Facebook
    </div>
</a>""",
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div style="
        background: linear-gradient(180deg, #0A192F 0%, #020C1B 100%);
        border: 1px solid #D4AF37;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: -15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
    ">
        <h3 class="acrobatic-heading" style="
            color: #D4AF37; 
            font-family: 'Helvetica Neue', sans-serif; 
            letter-spacing: 1.5px; 
            font-size: 16px;
            font-weight: 800;
            text-align: center;
            margin: 0 0 5px 0;
            text-transform: uppercase;
        ">
            🗺️ SYSTEM NAVIGATION
        </h3>
        <p style="
            color: #8892B0; 
            font-size: 12px; 
            text-align: center; 
            margin: 0;
        ">
            Select an institutional core command asset
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Render the Interactive Selector Component Directly Inside the Sidebar Flow
selected_tab = st.sidebar.selectbox(
    label="Navigation Matrix Control",
    options=NAVIGATION_OPTIONS,
    index=NAVIGATION_OPTIONS.index(st.session_state.current_route),
    label_visibility="collapsed",
    key="portal_navigation_router_matrix",
)

# Bind selection cleanly back to routing state
st.session_state.current_route = selected_tab

# Structural Breathing Space Padding
st.sidebar.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
st.sidebar.caption("Engine Architecture: v38.0.0 | Gombe Node — Lazy-Load Router")

# ==============================================================================
# 🎛️ MEMORY-ISOLATED LAZY ROUTING MODULES
# Each branch imports ONLY what it needs, exactly when it's selected.
# ==============================================================================
current = st.session_state.current_route

# --- MODULE 1: LEGISLATIVE FOOTPRINTS (MASTER LANDING ENTRY) ---
if current == "🏛️ LEGISLATIVE FOOTPRINTS":
    from panels import render_sponsored_bills_panel

    render_hero_banner()
    render_sponsored_bills_panel()

# --- MODULE 3: SKILL VOCATION POOL ---
elif current == "🛠️ SKILL VOCATION POOL":
    from panels import render_skill_form

    render_marquee_header()
    render_skill_form()

# --- MODULE 4: STUDENT SCHOLARSHIP/GRANT ---
elif current == "🎓 STUDENT SCHOLARSHIP/GRANT":
    from panels import render_scholarship_form

    render_marquee_header()
    render_scholarship_form()

# --- MODULE 5: PALLIATIVE ENROLLMENT ---
elif current == "📦 PALLIATIVE ENROLLMENT":
    from panels import render_palliative_form

    render_marquee_header()
    render_palliative_form()

# --- MODULE 6: CV & ARTISAN VAULT ---
elif current == "💡 CV & ARTISAN VAULT":
    from panels import render_cv_vault

    render_marquee_header()
    render_cv_vault()

# --- MODULE 7: COMMUNITY URGENT NEED ---
elif current == "🚨 COMMUNITY URGENT NEED":
    from panels import render_cun_trigger

    render_marquee_header()
    render_cun_trigger()

# --- MODULE 9: BEYOND RHETORICS ---
elif current == "🏛️ BEYOND RHETORICS":
    import panels

    st.title("Project Verification Hub")
    panels.render_project_verifications()

# --- MODULE 10: STRATEGIC COMMITTEES (MODULE 13) ---
elif current == "🛡️ STRATEGIC COMMITTEES (MODULE 13)":
    import panels

    panels.strategic_committees_panel()

# --- MODULE 11: POLLING UNIT AGENT HUB ---
elif current == "🗳️ POLLING UNIT AGENT HUB":
    import panels

    panels.agent_panel()

# --- MODULE 12: WARD COLLATION OFFICER HUB ---
elif current == "🛡️ WARD COLLATION OFFICER HUB":
    import panels

    panels.ward_collation_officer_panel()

# --- MODULE 13: EXECUTIVE CONTROL ROOM ---
elif current == "🔑 EXECUTIVE CONTROL ROOM":
    # 🚨 Hero Banner intentionally omitted here to prevent double card-like
    # container rendering on the secure admin panels.
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
