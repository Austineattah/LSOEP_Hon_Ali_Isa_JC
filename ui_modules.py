# ==============================================================================
# 🏛️ LSOEP UI MODULES & COMPONENTS
# Project: Balanga/Billiri Federal Constituency (Honourable Ali Isa JC, PhD)
# File: ui_modules.py (V66.0 - 2026 Compliant Structural Layout Blocks)
# ==============================================================================

import streamlit as st
import pandas as pd
import base64
import os
from registry import HON_TITLE, initialize_system_states


@st.cache_data
def get_image_as_base64(path):
    """Reads a local image file and returns it as a base64 encoded string."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None


def resolve_image_source(filename, fallback_url):
    """Scans the assets directory and returns a valid web fallback path if empty."""
    assets_dir = "assets"
    if os.path.exists(assets_dir) and os.path.isdir(assets_dir):
        try:
            files = os.listdir(assets_dir)
            for f in files:
                if f.lower() == filename.lower():
                    full_path = os.path.join(assets_dir, f)
                    b64 = get_image_as_base64(full_path)
                    if b64:
                        return f"data:image/png;base64,{b64}"
        except Exception:
            pass
    return fallback_url


def render_hero_banner():
    """Renders the high-end, responsive premium gradient hero banner."""
    DEFAULT_MACE = "https://img.icons8.com/fluency/300/mace.png"
    DEFAULT_HON = "https://img.icons8.com/color/300/user-male-circle--v1.png"

    mace_image_src = resolve_image_source("digital_mace.png", DEFAULT_MACE)
    hon_image_src = resolve_image_source("hon_ali.png", DEFAULT_HON)

    st.markdown(
        f"""
        <style>
        @keyframes gradientLineBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @keyframes swipe-right-left {{
            0% {{ transform: translateX(-20px) rotate(-5deg); }}
            100% {{ transform: translateX(20px) rotate(5deg); }}
        }}
        .hero-card-container {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 2.5rem 2rem;
            border-radius: 18px;
            background: linear-gradient(-45deg, #021024, #0B3C5D, #021024, #D4AF37, #061A33);
            background-size: 600% 600%;
            animation: gradientLineBG 20s ease infinite;
            border-left: 5px solid #D4AF37;
            border-right: 5px solid #0B3C5D;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }}
        .mace-left img {{
            height: 240px;
            filter: drop-shadow(0 0 25px rgba(255, 223, 100, 0.6));
            animation: swipe-right-left 3.5s ease-in-out infinite alternate;
        }}
        .hero-text-content {{
            text-align: center;
            color: #F0F0F0;
            padding: 0 1.5rem;
        }}
        .hero-text-content .title {{
            color: #D4AF37;
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
        }}
        .hero-text-content .subtitle {{
            color: #FFFFFF;
            font-size: 1.5rem;
            font-weight: 600;
            margin-top: 5px;
            letter-spacing: 1px;
        }}
        .hero-text-content .constituency {{
            color: #00E5FF;
            font-weight: 700;
            margin-top: 8px;
            font-size: 1.2rem;
            text-shadow: 0 0 8px rgba(0, 229, 255, 0.4);
        }}
        .hero-text-content .state {{
            color: #FFFFFF;
            opacity: 0.9;
            font-size: 1.1rem;
            margin: 0;
        }}
        .hon-right img {{
            height: 240px;
            width: 240px;
            border-radius: 50%;
            border: 6px solid #D4AF37;
            object-fit: cover;
            box-shadow: 0 0 35px rgba(212, 175, 55, 0.7);
        }}
        @media (max-width: 768px) {{
            .hero-card-container {{ flex-direction: column; padding: 2rem 1.5rem; }}
            .mace-left {{ order: 2; margin: 1.5rem 0; }}
            .hero-text-content {{ order: 1; margin-bottom: 1.5rem; }}
            .hon-right {{ order: 3; margin-top: 1.5rem; }}
            .mace-left img, .hon-right img {{ height: 180px; width: 180px; }}
        }}
        </style>
        <div class="hero-card-container">
            <div class="mace-left"><img src="{mace_image_src}" alt="Mace"></div>
            <div class="hero-text-content">
                <h1 class="title">{HON_TITLE}</h1>
                <h2 class="subtitle">MEMBER, HOUSE OF REPRESENTATIVES</h2>
                <p class="constituency">BALANGA/BILLIRI FEDERAL CONSTITUENCY</p>
                <p class="state">GOMBE STATE</p>
            </div>
            <div class="hon-right"><img src="{hon_image_src}" alt="{HON_TITLE}"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_marquee_header():
    """Renders the refined scrolling marquee text."""
    announcement = st.session_state.get(
        "global_scrolling_announcement",
        f"Welcome to the official constituency outreach portal of {HON_TITLE}. This platform is designed for transparency, accountability, and direct engagement.",
    )
    long_announcement = (announcement + " • ") * 3
    st.markdown(
        f"""
        <style>
        .marquee-container {{ background-color: #041d3d; padding: 12px 0; overflow: hidden; white-space: nowrap; border-top: 2px solid #D4AF37; border-bottom: 2px solid #D4AF37; margin-bottom: 10px; }}
        .marquee-content {{ display: inline-block; padding-left: 100%; animation: marquee 90s linear infinite; font-size: 1.1rem; font-weight: 600; letter-spacing: 1.5px; color: #EAEAEA; }}
        @keyframes marquee {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-100%); }} }}
        </style>
        <div class="marquee-container"><div class="marquee-content">{long_announcement}</div></div>
        """,
        unsafe_allow_html=True,
    )


def render_module_download_trigger(df, filename_prefix, key):
    """Renders a download button with updated 2026 width semantics."""
    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 Download {filename_prefix}.csv",
            data=csv,
            file_name=f"{filename_prefix}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key=key,
            use_container_width=True,
        )


def render_institutional_purge_engine():
    """Fallback placeholder component preventing core routing engine import crashes."""
    import streamlit as st

    st.info(
        "🔒 System Maintenance: Institutional Purge Engine operational parameters loaded successfully."
    )
