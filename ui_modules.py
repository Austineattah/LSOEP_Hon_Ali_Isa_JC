# ==============================================================================
# 🏛️ LSOEP PORTAL PLATFORM VISUAL INTERFACE COMPONENT LAYER
# Project: Balanga and Billiri Federal Constituency (Hon. Ali Isa JC, PhD)
# File: ui_modules.py (Aggregated Layout Modules & Data Engines)
# ==============================================================================

import streamlit as st
import os
import pandas as pd
import datetime
import time
from utils import image_to_base64, trigger_background_autosave
from registry import (
    COLUMNS_STRUCTURE,
    STRATEGIC_COMMITTEE_COLS,
    LITIGATION_AGENT_COLS,
    ANNOUNCEMENT_CACHE_FILE,
)


def render_marquee_header():
    """Renders the official institutional banner with dual base64 assets and scrolling marquee."""
    mace_path = os.path.join("assets", "digital_mace.png")
    portrait_path = os.path.join("assets", "hon_ali.png")

    mace_base64 = image_to_base64(mace_path)
    portrait_base64 = image_to_base64(portrait_path)

    mace_html = (
        f"""<img src="data:image/png;base64,{mace_base64}">""" if mace_base64 else ""
    )
    portrait_html = (
        f"""<img src="data:image/png;base64,{portrait_base64}">"""
        if portrait_base64
        else ""
    )

    # Fetch dynamic session announcements or fall back to default institutional marquee text
    announcement_text = st.session_state.get(
        "global_scrolling_announcement",
        "🦅 LEGISLATIVE STRATEGIC OUTREACH PORTAL • HON. ALI ISA JC • DELIVERING VERIFIABLE EXCELLENCE",
    )

    # Replaced old marquee markup with your fully integrated modern CSS block structure
    st.markdown(
        f"""
        <div style="background-color: #020C1B; padding: 10px; border-radius: 5px; margin-top: 15px; margin-bottom: 20px;">
            <marquee behavior="scroll" direction="left" scrollamount="4" style="color: #D4AF37; font-weight: bold; font-size: 18px; letter-spacing: 1.5px; font-family: sans-serif;">
                {announcement_text}
            </marquee>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_banner():
    """Lightweight Dashboard Overview banner — engineered with flexbox overrides to prevent viewport text clipping."""
    mace_path = os.path.join("assets", "digital_mace.png")
    portrait_path = os.path.join("assets", "hon_ali.png")

    mace_base64 = image_to_base64(mace_path)
    portrait_base64 = image_to_base64(portrait_path)

    mace_html = (
        f"""<img src="data:image/png;base64,{mace_base64}" style="height: 130px !important; width: auto !important; max-width: 100% !important; object-fit: contain !important;">"""
        if mace_base64
        else ""
    )
    portrait_html = (
        f"""<img src="data:image/png;base64,{portrait_base64}" style="height: 140px !important; width: auto !important; max-width: 100% !important; object-fit: contain !important; border-radius: 6px !important;">"""
        if portrait_base64
        else ""
    )

    st.markdown(
        f"""
        <div class="unified-command-vault" style="
            display: flex !important;
            flex-direction: row !important;
            justify-content: space-between !important;
            align-items: center !important;
            width: 100% !important;
            min-height: 180px !important;
            height: auto !important;
            padding: 20px 25px !important;
            box-sizing: border-box !important;
            overflow: visible !important;
            word-wrap: break-word !important;
            white-space: normal !important;
            gap: 15px !important;
        ">
            <div class="mace-vault-shield" style="flex-shrink: 0 !important; height: auto !important; max-height: 100% !important; display: flex !important; align-items: center !important; justify-content: center !important; overflow: visible !important;">
                {mace_html}
            </div>
            <div class="vault-text-block" style="
                flex-grow: 1 !important;
                text-align: center !important;
                overflow: visible !important;
                white-space: normal !important;
                word-break: keep-all !important;
            ">
                <h1 style="white-space: normal !important; word-wrap: break-word !important; font-size: calc(1.5rem + 1vw) !important; margin-bottom: 8px !important; line-height: 1.2 !important;">
                    HONOURABLE ALI ISA JC, <span class="phd-text">PhD</span>
                </h1>
                <div class="sub-title" style="white-space: normal !important; word-wrap: break-word !important; font-size: calc(0.8rem + 0.3vw) !important; line-height: 1.4 !important; font-weight: 600 !important;">
                    MEMBER HOUSE OF REPRESENTATIVES<br>REPRESENTING BALANGA/BILLIRI FEDERAL CONSTITUENCY
                </div>
                <div class="geo-stamp" style="margin-top: 8px !important; font-weight: 700 !important; letter-spacing: 2px !important;">
                    GOMBE STATE
                </div>
            </div>
            <div class="photo-vault-shield" style="flex-shrink: 0 !important; height: auto !important; max-height: 100% !important; display: flex !important; align-items: center !important; justify-content: center !important; overflow: visible !important;">
                {portrait_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_stats():
    """Lightweight Dashboard Overview KPI strip — cheap len() lookups only,
    no heavy dataframe scans, by design (keeps the Dashboard Overview page fast)."""
    st.markdown(
        """<h3 class="swing-in">📊 Quick System Snapshot</h3>""", unsafe_allow_html=True
    )

    registry_df = st.session_state.get("global_registry")
    committee_df = st.session_state.get("strategic_committee_registry")
    submitted_wards = st.session_state.get("submitted_wards", {})
    submitted_pus = st.session_state.get("submitted_pus", {})

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Constituent Registrations", len(registry_df) if registry_df is not None else 0
    )
    c2.metric(
        "Strategic Committee Submissions",
        len(committee_df) if committee_df is not None else 0,
    )
    c3.metric("Wards Reported", len(submitted_wards))
    c4.metric("Polling Units Reported", len(submitted_pus))

    if st.session_state.get("radar_threat", False):
        st.error(f"🚨 Active fraud alert: {st.session_state.get('threat_msg', '')}")
    else:
        st.success("✅ No active anti-fraud alerts.")


def render_module_download_trigger(data_source, filename_prefix, unique_key):
    """Generates an immediate CSV data export object wrapper for active logs dataframes."""
    try:
        csv_bytes = pd.DataFrame(data_source).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 DOWNLOAD SYSTEM LOG EXPORT",
            data=csv_bytes,
            file_name=f"{filename_prefix}_{datetime.date.today()}.csv",
            mime="text/csv",
            key=f"dl_btn_{unique_key}",
        )
    except Exception as e:
        st.caption(f"Download entry failure: {e}")


def render_institutional_purge_engine(key_suffix):
    """Provides a secured interface checkpoint to reset and clear operational session arrays."""
    st.markdown("---")
    st.subheader("🚨 Institutional Data Purge Zone")
    confirm_purge = st.text_input(
        "Type 'PURGE SYSTEM DATA' to authorize reset:", key=f"purge_box_{key_suffix}"
    )
    if f"purge_btn_{key_suffix}" in st.session_state or st.button(
        "💥 EXECUTE SYSTEM PURGE", type="primary", key=f"purge_btn_{key_suffix}"
    ):
        if confirm_purge == "PURGE SYSTEM DATA":
            st.session_state.global_registry = pd.DataFrame(columns=COLUMNS_STRUCTURE)
            st.session_state.submitted_wards = {}
            st.session_state.submitted_pus = {}
            st.session_state.strategic_committee_registry = pd.DataFrame(
                columns=STRATEGIC_COMMITTEE_COLS
            )
            st.session_state.committee_double_dipping_ledger = {}
            st.session_state.agent_field_registry = pd.DataFrame(
                columns=LITIGATION_AGENT_COLS
            )

            try:
                with open(ANNOUNCEMENT_CACHE_FILE, "w") as f:
                    f.write("")
                st.session_state.global_scrolling_announcement = ""
            except:
                pass

            trigger_background_autosave()
            st.success("System tracking layers reset completely.")
            st.rerun()
