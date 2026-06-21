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
        background-color: #030f21 !important; 
        border-right: 4px solid #8B0000 !important;
    }
    
    .admin-launch-zone {
        border: 2px dashed #00E5FF; padding: 15px; border-radius: 14px;
        background-color: rgba(0, 229, 255, 0.08); margin-bottom: 15px;
    }
    
    .inst-link-box {
        display: block; background: linear-gradient(90deg, #8B0000 0%, #4A0000 100%) !important;
        color: #FFFFFF !important; padding: 12px; border-radius: 10px; 
        text-align: center; font-weight: 900; margin-bottom: 10px; text-decoration: none;
        font-size: 14px; letter-spacing: 1px; text-transform: uppercase;
    }
    
    .stButton>button { 
        width: 100% !important; height: 48px !important; font-weight: 800 !important; 
        font-size: 14px !important; margin-bottom: 10px !important; border: 2px solid #8B0000 !important;
        border-radius: 10px !important; color: #FFFFFF !important; transition: all 0.3s ease;
        text-transform: uppercase; letter-spacing: 1px;
    }

    button[key="nav_btn_bills"] { background: linear-gradient(90deg, #D4AF37 0%, #B48811 100%) !important; }
    button[key="nav_btn_skill"] { background: linear-gradient(90deg, #00B4DB 0%, #0083B0 100%) !important; }
    button[key="nav_btn_sch"] { background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important; }
    button[key="nav_btn_pal"] { background: linear-gradient(90deg, #2e8b57 0%, #38ef7d 100%) !important; }
    button[key="nav_btn_cv"] { background: linear-gradient(90deg, #8E2DE2 0%, #4A00E0 100%) !important; }
    button[key="nav_btn_cun_redirect"] { background: #0b1e36 !important; border: 2px solid #00E5FF !important; }

    @keyframes master_chroma_flow {
        0% { border-color: #FFD700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); background-position: 0% 50%; }
        50% { border-color: #00E5FF; box-shadow: 0 0 45px rgba(0, 229, 255, 0.9); background-position: 100% 50%; }
        100% { border-color: #FFD700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.6); background-position: 0% 50%; }
    }

    @keyframes radar_flash {
        0% { background-color: #FF0000; color: #FFFFFF; box-shadow: 0 0 20px #FF0000; }
        50% { background-color: #330000; color: #FF0000; box-shadow: 0 0 0px #000000; }
        100% { background-color: #FF0000; color: #FFFFFF; box-shadow: 0 0 20px #FF0000; }
    }

    @keyframes swing {
        20% {
            transform: rotate3d(0, 0, 1, 15deg);
        }
        40% {
            transform: rotate3d(0, 0, 1, -10deg);
        }
        60% {
            transform: rotate3d(0, 0, 1, 5deg);
        }
        80% {
            transform: rotate3d(0, 0, 1, -5deg);
        }
        100% {
            transform: rotate3d(0, 0, 1, 0deg);
        }
    }

    .swing-in {
        transform-origin: top center;
        animation: swing 1s ease-out;
    }

    @keyframes mace-swing-anim {
        0% { transform: rotate(-8deg); }
        50% { transform: rotate(8deg); }
        100% { transform: rotate(-8deg); }
    }

    @keyframes acrobatic-text {
        0% { transform: scale(1) rotate(0deg); color: #D4AF37; }
        25% { transform: scale(1.05) rotate(-3deg); color: #FFFFFF; }
        50% { transform: scale(1) rotate(0deg); color: #D4AF37; }
        75% { transform: scale(1.05) rotate(3deg); color: #FFFFFF; }
        100% { transform: scale(1) rotate(0deg); color: #D4AF37; }
    }

    .acrobatic-heading {
        animation: acrobatic-text 4s ease-in-out infinite;
    }

    .unified-command-vault {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        height: 330px !important; 
        background: linear-gradient(-45deg, #04142c, #0b264f, #020a17, #071e3d) !important;
        background-size: 400% 400% !important;
        border: 5px solid #FFD700 !important;
        animation: master_chroma_flow 6s infinite ease-in-out !important;
        padding: 0px !important; 
        border-radius: 24px !important;
        backdrop-filter: blur(35px) !important;
        -webkit-backdrop-filter: blur(35px) !important;
        margin-top: 5px !important;
        box-shadow: inset 0 0 50px rgba(255, 215, 0, 0.35), 0 20px 45px rgba(0, 0, 0, 0.65) !important;
        overflow: hidden !important;
        transition: all 0.5s ease-in-out;
    }

    .mace-vault-shield {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 310px !important; 
        height: 100% !important; 
        background: rgba(4, 20, 48, 0.7) !important; 
        overflow: hidden !important;
        border-right: 3px solid rgba(255, 215, 0, 0.3);
    }

    .mace-vault-shield img {
        height: 90% !important; 
        width: 90% !important; 
        object-fit: contain !important; 
        filter: drop-shadow(0px 0px 20px rgba(255, 215, 0, 0.85)) contrast(1.4) brightness(1.1);
        transform-origin: bottom center;
        animation: mace-swing-anim 3s ease-in-out infinite;
    }

    .photo-vault-shield {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 450px !important; 
        height: 100% !important; 
        background: rgba(2, 10, 23, 0.5) !important; 
        overflow: hidden !important;
        border-left: 3px solid rgba(0, 229, 255, 0.3);
    }

    .photo-vault-shield img {
        height: 100% !important;
        width: 100% !important; 
        object-fit: cover !important; 
        filter: contrast(1.3) brightness(1.05) drop-shadow(-10px 0px 25px rgba(0,0,0,0.8));
    }

    .vault-text-block {
        flex-grow: 2 !important;
        text-align: center !important;
        padding: 0 20px !important;
    }

    .vault-text-block h1 {
        color: #FFFF00 !important;
        margin: 0 !important;
        font-size: 2.2rem !important;
        font-weight: 950 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        text-shadow: 2px 2px 6px #000000, 0 0 15px rgba(255,255,0,0.3) !important;
        line-height: 1.2 !important;
    }

    .vault-text-block .sub-title {
        color: #FFFFFF !important;
        margin: 6px 0 0 0 !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
        line-height: 1.2 !important;
    }

    .vault-text-block .geo-stamp {
        color: #00E5FF !important;
        margin: 6px 0 0 0 !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9) !important;
        display: block !important;
    }

    .mobile-return-banner {
        display: none; background: linear-gradient(90deg, #0b1e36 0%, #05101e 100%);
        border: 2px solid #00E5FF; padding: 12px; border-radius: 8px; text-align: center;
        margin-bottom: 15px; cursor: pointer; text-transform: uppercase; font-weight: 800; letter-spacing: 1px;
    }

    @media (max-width: 1024px) {
        .unified-command-vault { flex-direction: column !important; height: auto !important; padding: 30px 10px !important; gap: 20px !important; }
        .mace-vault-shield { width: 100% !important; height: 200px !important; border-right: none; border-bottom: 3px solid rgba(255, 215, 0, 0.3); }
        .photo-vault-shield { width: 100% !important; height: 260px !important; border-left: none; border-top: 3px solid rgba(0, 229, 255, 0.3); }
        .vault-text-block h1 { font-size: 1.9rem !important; line-height: 1.2 !important; }
        .vault-text-block .sub-title { font-size: 1.05rem !important; }
        .vault-text-block .geo-stamp { font-size: 1.15rem !important; }
        .mobile-return-banner { display: block !important; }
    }

    .supervisor-header {
        background-color: #B71C1C;
        color: #FFFFFF !important;
        padding: 6px;
        border-radius: 8px;
        text-align: center; font-weight: 900; 
        display: block; width: 100%; font-size: 15px;
        margin-bottom: 12px; letter-spacing: 1px; text-transform: uppercase;
    }
    .radar-sticky-threat {
        animation: radar_flash 0.5s infinite; padding: 15px; border-radius: 8px; border: 3px solid #FFFFFF;
        text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 15px;
    }
    .tier-box { display: inline-block; padding: 10px 20px; margin: 5px; border-radius: 6px; font-weight: bold; color: white; text-align: center; border: 2px solid #FFFFFF; }
    .tier-box.tier-pres { background-color: #FF4B4B !important; }
    .tier-box.tier-sen { background-color: #1F77B4 !important; }
    .tier-box.tier-rep { background-color: #2CA02C !important; }
    .tier-box.tier-gov { background-color: #9467BD !important; }
    .tier-box.tier-house { background-color: #FF7F0E !important; }
    
    .printable-slip-box { background-color: #FFFFFF !important; color: #000000 !important; padding: 25px; border: 3px double #8B0000; border-radius: 4px; font-family: 'Courier New', Courier, monospace; margin-top: 15px; }
    .slip-header { text-align: center; font-weight: 900; font-size: 16px; margin-bottom: 15px; border-bottom: 2px dashed #000; padding-bottom: 10px; }
    .slip-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; font-weight: bold; }
    
    .stTextInput label p { color: #00E5FF !important; font-weight: 700 !important; }

    .beyond-rhetoric-header {
        background: linear-gradient(135deg, #0D243E, #040F1A);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #D4AF37;
        margin-bottom: 20px;
    }
    .beyond-title {
        color: #D4AF37;
        font-size: 1.8rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }

    /* =====================================================================
       📍 SIDEBAR & NAVIGATION DROPDOWN CUSTOM STYLING
       Added for the sidebar selectbox-based navigation router in main.py
       ===================================================================== */

    [data-testid="stSidebarUserContent"] {
        padding-top: 2rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
        background-color: #020C1B !important;
    }
    [data-testid="stSidebar"] {
        background-color: #020C1B !important;
        border-right: 1px solid rgba(212, 175, 55, 0.2) !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #0A192F !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
        border-color: #FFFFFF !important;
        box-shadow: 0px 4px 12px rgba(212, 175, 55, 0.4) !important;
    }
    div[data-testid="stSelectbox"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.5px;
    }
    div[data-testid="stSelectbox"] svg {
        fill: #D4AF37 !important;
    }

    /* =====================================================================
       🏛️ GLOBAL TYPOGRAPHY CORRECTIONS
       Note: h1/h2/h3 here are intentionally NOT !important so the more
       specific .vault-text-block h1 rule above (which IS !important) keeps
       full control over the hero banner's title styling and is unaffected.
       ===================================================================== */
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
