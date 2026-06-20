# ==============================================================================
# 🏛️ LSOEP MASTER PORTAL PLATFORM LIFE-CYCLE ENGINE
# Project: Balanga and Billiri Federal Constituency (Hon. Ali Isa JC, PhD)
# File: main.py (Fully Aggregated Operational Core Router)
# ==============================================================================

import streamlit as st
import datetime
import time
import pandas as pd
import sys
import asyncio
import warnings

if sys.platform == "win32":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from styling import apply_styling
from registry import initialize_system_states, HON_TITLE
from ui_modules import render_marquee_header
from panels import (
    ward_collation_officer_panel,
    agent_panel,
    main_dashboard,
    strategic_committees_panel,
    render_beyond_rhetoric_panel,
    render_skill_form,
    render_scholarship_form,
    render_cv_vault,
    render_cun_trigger,
    render_palliative_form,
    render_sponsored_bills_panel,
)
from utils import trigger_background_autosave

apply_styling()
initialize_system_states()

app_tabs = st.tabs(
    [
        "Gateway Terminal Portal",
        "Beyond Rhetorics Project",
        "Module 13: Strategic Committees",
        "Polling Unit Agent Hub",
        "Ward Collation Officer Hub",
        "Executive Control Room",
    ]
)

with app_tabs[0]:
    render_marquee_header()
    if "current_page" not in st.session_state:
        st.session_state.current_page = "bills"

    with st.sidebar:
        if st.session_state.get("radar_threat", False):
            st.markdown(
                f"""<div style="background-color:#FF4B4B; color:white; padding:10px; border-radius:4px; font-weight:bold; font-size:12px; margin-bottom:10px;">
                    🚨 SECURITY WARNING: ANTI-FRAUD RADAR MATCH<br>{st.session_state.get("threat_msg", "")}
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<p style='color:#D4AF37; font-weight:bold; margin-bottom:2px;'>🏛️ PUBLIC REGISTRY INTERFACES</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<a href="https://web.facebook.com/hon.isa.ali.jc/?_rdc=1&_rdr#" target="_blank" style="text-decoration:none;">
            <div style="background-color:#0B3C5D; color:white; text-align:center; padding:8px; border-radius:4px; font-size:12px; font-weight:bold; margin-bottom:10px;">
                🌐 {HON_TITLE} Official Facebook
            </div>
        </a>""",
            unsafe_allow_html=True,
        )

        if st.button(
            "🏛️ LEGISLATIVE FOOTPRINTS", key="nav_btn_bills", use_container_width=True
        ):
            st.session_state.current_page = "bills"

        st.divider()

        if st.button(
            "🛠️ SKILL VOCATION POOL", key="nav_btn_skill", use_container_width=True
        ):
            st.session_state.current_page = "skill_form"
        if st.button(
            "🎓 STUDENT SCHOLARSHIP/GRANT", key="nav_btn_sch", use_container_width=True
        ):
            st.session_state.current_page = "scholarship_form"
        if st.button(
            "📦 CONSTITUENT PALLIATIVE ENROLLMENT",
            key="nav_btn_pal",
            use_container_width=True,
        ):
            st.session_state.current_page = "palliative_gateway"
        if st.button(
            "💡 CV & ARTISAN VAULT", key="nav_btn_cv", use_container_width=True
        ):
            st.session_state.current_page = "cv_vault"

        st.markdown(
            "<div style='background-color:#8B0000; color:white; text-align:center; font-size:11px; font-weight:bold; padding:3px; margin-top:10px;'>🚨 COMMUNITY URGENT NEED</div>",
            unsafe_allow_html=True,
        )
        if st.button(
            "TRIGGER FIELD REPORT", key="nav_btn_cun_redirect", use_container_width=True
        ):
            st.session_state.current_page = "cun_trigger"

        st.divider()
        st.caption("Engine Architecture: v36.0.0 | Gombe Node")

    page = st.session_state.get("current_page", "bills")
    if page == "bills":
        render_sponsored_bills_panel()
    elif page == "skill_form":
        render_skill_form()
    elif page == "scholarship_form":
        render_scholarship_form()
    elif page == "cv_vault":
        render_cv_vault()
    elif page == "cun_trigger":
        render_cun_trigger()
    else:
        render_palliative_form()

with app_tabs[1]:
    render_beyond_rhetoric_panel()
with app_tabs[2]:
    strategic_committees_panel()
with app_tabs[3]:
    agent_panel()
with app_tabs[4]:
    ward_collation_officer_panel()
with app_tabs[5]:
    st.markdown("### 🔑 Executive Command System Authorization Security Checkpoint")
    admin_key_input = st.text_input(
        "Enter Command Hub Key to Unroll Operational Data Logs:",
        type="password",
        key="checkpoint_admin_key",
    )
    if admin_key_input == "ali 2027":
        conn = None
        main_dashboard(conn)
    elif admin_key_input:
        st.error("🛑 SYSTEM ACCESS REJECTED: Command signature authorization mismatch.")
