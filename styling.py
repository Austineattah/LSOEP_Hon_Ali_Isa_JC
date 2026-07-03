import streamlit as st


def inject_custom_css():
    """Injects the global CSS block only — does NOT call st.set_page_config().
    main.py's lazy-loading router calls st.set_page_config() itself, exactly
    once, as the very first Streamlit command, then calls this function."""
    st.markdown(
        """
    <style>
    /* Hide Streamlit hamburger menu and footer for clean, secure production view */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Correct PhD Casing */
    .phd-text {
        text-transform: none !important;
    }

    [data-testid="stSidebar"] {
        background-color: #020C1B !important;
        border-right: 1px solid rgba(212, 175, 55, 0.2) !important;
    }
    [data-testid="stSidebarUserContent"] {
        padding: 2rem 1.1rem !important;
        background-color: #020C1B !important;
    }

    .admin-launch-zone {
        border: 2px dashed #00E5FF; padding: 15px; border-radius: 14px;
        background-color: rgba(0, 229, 255, 0.08); margin-bottom: 15px;
    }

    .inst-link-box {
        display: block; background: linear-gradient(90deg, #0B3C5D 0%, #061A33 100%) !important;
        color: #FFFFFF !important; padding: 12px; border-radius: 10px;
        text-align: center; font-weight: 900; margin-bottom: 10px; text-decoration: none;
        font-size: 14px; letter-spacing: 1px; text-transform: uppercase;
        border: 1px solid #D4AF37;
    }

    .stButton>button {
        width: 100% !important; height: 48px !important; font-weight: 800 !important;
        font-size: 14px !important; margin-bottom: 10px !important; border: 2px solid #D4AF37 !important;
        border-radius: 10px !important; color: #FFFFFF !important; transition: all 0.3s ease;
        text-transform: uppercase; letter-spacing: 1px; background: #0A192F;
    }
    .stButton>button:hover {
        border-color: #FFFFFF !important;
        color: #D4AF37 !important;
    }

    /* Key-specific button styles */
    button[key="nav_btn_bills"] { background: linear-gradient(90deg, #D4AF37 0%, #B48811 100%) !important; }
    button[key="nav_btn_skill"] { background: linear-gradient(90deg, #00B4DB 0%, #0083B0 100%) !important; }
    button[key="nav_btn_sch"] { background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important; }
    button[key="nav_btn_pal"] { background: linear-gradient(90deg, #2e8b57 0%, #38ef7d 100%) !important; }
    button[key="nav_btn_cv"] { background: linear-gradient(90deg, #8E2DE2 0%, #4A00E0 100%) !important; }
    button[key="nav_btn_cun_redirect"] { background: #0b1e36 !important; border: 2px solid #00E5FF !important; }

    @keyframes master_chroma_flow {
        0% { border-color: #FFD700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); }
        50% { border-color: #00E5FF; box-shadow: 0 0 45px rgba(0, 229, 255, 0.9); }
        100% { border-color: #FFD700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); }
    }

    @keyframes swing { 20% {transform: rotate3d(0, 0, 1, 15deg);} 40% {transform: rotate3d(0, 0, 1, -10deg);} 60% {transform: rotate3d(0, 0, 1, 5deg);} 80% {transform: rotate3d(0, 0, 1, -5deg);} 100% {transform: rotate3d(0, 0, 1, 0deg);} }
    .swing-in { transform-origin: top center; animation: swing 1s ease-out; }

    @keyframes mace-swing-anim { 0% { transform: rotate(-8deg); } 50% { transform: rotate(8deg); } 100% { transform: rotate(-8deg); } }

    .unified-command-vault {
        display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important;
        width: 100% !important; height: 330px !important;
        background: linear-gradient(-45deg, #04142c, #0b264f, #020a17, #071e3d) !important;
        background-size: 400% 400% !important;
        border: 5px solid #FFD700 !important;
        animation: master_chroma_flow 6s infinite ease-in-out !important;
        padding: 0px !important; border-radius: 24px !important; margin-top: 5px !important;
        box-shadow: inset 0 0 50px rgba(255, 215, 0, 0.35), 0 20px 45px rgba(0, 0, 0, 0.65) !important;
        overflow: hidden !important;
    }

    .mace-vault-shield {
        flex-shrink: 0 !important; display: flex !important; align-items: center !important; justify-content: center !important;
        width: 310px !important; height: 100% !important;
        background: rgba(4, 20, 48, 0.7) !important; overflow: hidden !important;
        border-right: 3px solid rgba(255, 215, 0, 0.3);
    }
    .mace-vault-shield img { height: 90% !important; width: 90% !important; object-fit: contain !important; filter: drop-shadow(0px 0px 20px rgba(255, 215, 0, 0.85)) contrast(1.4) brightness(1.1); transform-origin: bottom center; animation: mace-swing-anim 3s ease-in-out infinite; }
    .photo-vault-shield { flex-shrink: 0 !important; display: flex !important; align-items: center !important; justify-content: center !important; width: 450px !important; height: 100% !important; background: rgba(2, 10, 23, 0.5) !important; overflow: hidden !important; border-left: 3px solid rgba(0, 229, 255, 0.3); }
    .photo-vault-shield img { height: 100% !important; width: 100% !important; object-fit: cover !important; filter: contrast(1.3) brightness(1.05) drop-shadow(-10px 0px 25px rgba(0,0,0,0.8)); }

    .vault-text-block { flex-grow: 2 !important; text-align: center !important; padding: 0 20px !important; }
    .vault-text-block h1 { color: #FFFF00 !important; font-size: 2.2rem !important; font-weight: 950 !important; text-transform: uppercase !important; }
    .vault-text-block .sub-title { color: #FFFFFF !important; font-size: 1.2rem !important; font-weight: 800 !important; text-transform: uppercase !important; }
    .vault-text-block .geo-stamp { color: #00E5FF !important; font-size: 1.4rem !important; font-weight: 900 !important; text-transform: uppercase !important; }

    .supervisor-header { background-color: #B71C1C; color: #FFFFFF !important; padding: 6px; border-radius: 8px; text-align: center; font-weight: 900; display: block; width: 100%; font-size: 15px; margin-bottom: 12px; letter-spacing: 1px; text-transform: uppercase; }
    .radar-sticky-threat { background-color: #B71C1C; color: #FFFFFF; padding: 10px; border-radius: 8px; border: 2px solid #FFFFFF; text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 15px; }
    .printable-slip-box { background-color: #FFFFFF !important; color: #000000 !important; padding: 25px; border: 3px double #8B0000; border-radius: 4px; font-family: 'Courier New', Courier, monospace; margin-top: 15px; }
    .slip-header { text-align: center; font-weight: 900; font-size: 16px; margin-bottom: 15px; border-bottom: 2px dashed #000; padding-bottom: 10px; }
    .slip-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; font-weight: bold; }

    .beyond-rhetoric-header { background: linear-gradient(135deg, #0D243E, #040F1A); padding: 20px; border-radius: 12px; border-left: 6px solid #D4AF37; margin-bottom: 20px; }
    .beyond-title { color: #D4AF37; font-size: 1.8rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.5px; text-shadow: 1px 1px 3px rgba(0,0,0,0.5); }

    /* =====================================================================
       ✨ NEW & UPDATED STYLES FOR V40 LAYOUT
       ===================================================================== */
    .admin-header {
        text-align: center;
        border-bottom: 2px solid #0000FF;
        padding-bottom: 5px;
        margin-bottom: 15px;
        color: #0000FF !important;
        font-size: 1.5rem;
    }
    .nav-title {
        text-align: center;
        color: #0000FF;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: 1px;
        margin-top: 40px;
        margin-bottom: 30px;
        font-size: 2.2rem;
        border-bottom: 2px solid #0000FF; /* Sharp blue underline for public channels */
        padding-bottom: 10px;
    }
    .nav-card-link {
        text-decoration: none;
    }
    .nav-card {
        background: linear-gradient(145deg, #0A192F, #0D243E);
        border: 2px solid #D4AF37;
        border-radius: 12px;
        padding: 20px 15px;
        margin-bottom: 20px;
        text-align: center;
        color: #FFFFFF;
        transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .nav-card:hover {
        transform: scale(1.06);
        box-shadow: 0 10px 30px rgba(0, 229, 255, 0.4);
        background: linear-gradient(145deg, #0D243E, #1A3A5F);
        border-color: #00E5FF;
    }
    .nav-card-icon {
        font-size: 2.8rem;
        margin-bottom: 12px;
        line-height: 1;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.7));
    }
    .nav-card-text {
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        line-height: 1.3;
    }
    h1, h2, h3 {
        color: #D4AF37;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
    }
    p {
        color: #F8F9FA;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def apply_styling():
    """Backward-compatible wrapper: sets page config AND injects CSS in one call.
    Kept for any code path still calling apply_styling() instead of the new
    split set_page_config() + inject_custom_css() pattern used in main.py."""
    st.set_page_config(
        page_title="LSOEP TITAN GOMBE | HON. ALI ISA JC, PhD HUB",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_custom_css()
