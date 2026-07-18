# ==============================================================================
# 🎨 LSOEP PLATFORM UI CUSTOM STYLING SHEET OVERLAYS
# Project: Balanga/Billiri Federal Constituency (Hon. Ali Isa JC)
# File: styling.py (V94.0 - Ultra-Compact Spacing Realignment)
# ==============================================================================

import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
            /* --- GLOBAL BACKGROUND OVERHAUL & EXECUTIVE TYPOGRAPHY --- */
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=500;600;700;800&family=Space+Grotesk:wght=500;600;700;800&family=Cabinet+Grotesk:wght=800&display=swap');

            .stApp {
                background: radial-gradient(circle at 50% 0%, #051625 0%, #020b12 60%, #000306 100%) !important;
                background-attachment: fixed !important;
            }

            .stApp::before {
                content: "";
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background-image: 
                    linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 1px);
                background-size: 50px 50px;
                background-position: center top;
                pointer-events: none;
                z-index: 0;
                opacity: 0.6;
            }

            body, html, [data-testid="stAppViewContainer"] {
                color: #F8FAFC !important;
                font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Space Grotesk', system-ui, sans-serif !important;
                color: #FFFFFF !important;
            }

            /* --- 🌐 SIDEBAR COLOR SEPARATION MATRIX --- */
            [data-testid="stSidebar"] {
                background-color: #01080f !important;
                border-right: 1px solid rgba(15, 54, 87, 0.5) !important;
            }

            /* e2) Admin Checkpoints Elements / Selectors Styling */
            .sidebar-admin-checkpoint {
                background: linear-gradient(135deg, #1e1602 0%, #0f0b01 100%) !important;
                border: 1px solid #D4AF37 !important;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 10px;
                color: #E2BB3C !important;
                font-family: 'Space Grotesk', sans-serif;
            }

            /* e2) Command Hub Active Streams / Analytics Styling */
            .sidebar-command-hub {
                background: linear-gradient(135deg, #020f1c 0%, #01060d 100%) !important;
                border: 1px solid #00E5FF !important;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 10px;
                color: #00E5FF !important;
                font-family: 'Space Grotesk', sans-serif;
            }

            /* --- 🏛️ ELITE INTERACTIVE PROFILE BANNER HERO CARD --- */
            .honourable-profile-hero {
                position: relative;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: linear-gradient(135deg, rgba(6, 30, 56, 0.9) 0%, rgba(3, 15, 28, 0.98) 100%) !important;
                backdrop-filter: blur(12px) saturate(160%) !important;
                border: 1px solid rgba(214, 175, 55, 0.4) !important;
                border-radius: 8px !important;
                padding: 14px 20px !important;
                margin-bottom: 16px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
                overflow: hidden;
                min-height: 135px;
            }

            .hero-left-content {
                flex: 1;
                padding-right: 150px;
                z-index: 2;
            }

            .hero-badge-strip {
                display: flex;
                gap: 6px;
                margin-bottom: 4px;
            }

            .hero-title-main {
                color: #FFFFFF !important;
                font-size: 1.35rem !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin: 0 !important;
                line-height: 1.2;
            }

            .hero-subtitle-sub {
                color: #D4AF37 !important;
                font-size: 0.9rem !important;
                font-weight: 600 !important;
                margin-top: 2px !important;
            }

            .hero-right-portrait {
                position: absolute !important;
                top: 0 !important;
                bottom: 0 !important;
                right: 0 !important;
                width: 150px !important;
                height: 100% !important;
                background-size: cover !important;
                background-position: center top !important;
                background-repeat: no-repeat !important;
                border-radius: 0 7px 7px 0 !important;
                z-index: 1;
            }

            .honourable-profile-hero::after {
                content: "";
                position: absolute;
                top: 0; bottom: 0; right: 110px; left: 0;
                background: linear-gradient(90deg, rgba(3, 15, 28, 1) 0%, rgba(6, 30, 56, 0.9) 65%, transparent 100%);
                z-index: 1;
                pointer-events: none;
            }

            /* --- ⚡ CONSTITUENCY ENGAGEMENT CHANNELS HEADER MATRIX (TIGHTENED VERTICAL SPACING) --- */
            .nav-title {
                font-family: 'Cabinet Grotesk', 'Space Grotesk', sans-serif !important;
                font-weight: 800 !important;
                font-size: 2.4rem !important;
                letter-spacing: -0.03em !important;
                text-transform: uppercase;
                text-align: center;
                margin-top: 15px !important; /* Pulled down sharply below vacancy tracker */
                margin-bottom: 10px !important; /* Brought significantly closer to the tabs */
                background: linear-gradient(135deg, #FFF6D6 0%, #D4AF37 50%, #AA7C11 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                text-shadow: 0px 4px 20px rgba(214, 175, 55, 0.15) !important;
            }

            /* Ambient Glow Background Wrapper Around Heading Framework (Optimized Padding) */
            div[data-testid="stVerticalBlock"] > div:has(.nav-title) {
                background: radial-gradient(circle at 50% 0%, rgba(20, 35, 65, 0.45) 0%, rgba(2, 16, 36, 0) 75%) !important;
                padding: 10px 20px 5px 20px !important; /* Collapsed top/bottom inner whitespace padding */
                margin-bottom: 5px !important; /* Drastically reduced outer lower margin frame */
            }

            /* --- 🛠️ 13 CONSTITUENCY NAVIGATION GRID CHANNELS TILE MATRIX --- */
            div[data-testid="stHorizontalBlock"] button {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.12rem !important;
                letter-spacing: 0.01em !important;
                color: #FFFFFF !important;
                background: linear-gradient(135deg, #051329 0%, #0A2246 100%) !important;
                border: 1px solid rgba(214, 175, 55, 0.35) !important;
                border-radius: 12px !important;
                padding: 26px 16px !important; 
                min-height: 105px !important; 
                width: 100% !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            }

            div[data-testid="stHorizontalBlock"] button:hover {
                border-color: #D4AF37 !important;
                background: linear-gradient(135deg, #0A2246 0%, #103365 100%) !important;
                color: #D4AF37 !important;
                transform: translateY(-4px) scale(1.015) !important;
                box-shadow: 0 8px 25px rgba(214, 175, 55, 0.25) !important;
            }

            div[data-testid="stHorizontalBlock"] button:active {
                transform: translateY(-1px) scale(0.99) !important;
                box-shadow: 0 2px 10px rgba(214, 175, 55, 0.1) !important;
            }

            /* --- 🔑 SYSTEM ACCESS PORTAL TABS SIDEBAR BUTTONS --- */
            [data-testid="stSidebar"] button {
                font-family: 'Space Grotesk', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.10rem !important;
                letter-spacing: 0.02em !important;
                padding: 12px 10px !important;
            }

            /* --- 🌐 OFFICIAL FACEBOOK BOX ANCHOR --- */
            .inst-link-box {
                display: block !important;
                text-align: center !important;
                background: rgba(214, 175, 55, 0.08) !important;
                border: 1px dashed rgba(214, 175, 55, 0.4) !important;
                padding: 14px 12px !important;
                border-radius: 8px !important;
                color: #D4AF37 !important;
                text-decoration: none !important;
                font-weight: 700 !important;
                font-size: 1.15rem !important;
                transition: background 0.2s ease !important;
            }
            
            .inst-link-box:hover {
                background: rgba(214, 175, 55, 0.15) !important;
                border-style: solid !important;
            }

            /* --- ⚡ LEGACY NAV GRID LAYOUT CONFIGURATIONS --- */
            .premium-nav-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 8px;
                margin-top: 6px;
                margin-bottom: 14px;
            }

            .premium-nav-card {
                background: linear-gradient(145deg, rgba(7, 28, 51, 0.85) 0%, rgba(3, 15, 28, 0.95) 100%) !important;
                backdrop-filter: blur(8px) !important;
                border: 1px solid rgba(15, 54, 87, 0.8) !important;
                border-radius: 6px !important;
                padding: 10px 8px !important;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35);
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .premium-nav-card:hover {
                border-color: #D4AF37 !important;
                background: linear-gradient(145deg, rgba(12, 45, 82, 0.9) 0%, rgba(7, 28, 51, 0.95) 100%) !important;
                box-shadow: 0 6px 18px rgba(0, 229, 255, 0.15);
                transform: translateY(-2px);
            }

            .premium-card-text {
                font-family: 'Space Grotesk', system-ui, sans-serif !important;
                color: #FFFFFF !important;
                font-weight: 600 !important;
                font-size: 0.82rem !important;
                letter-spacing: 0.3px;
                text-transform: uppercase;
                margin-top: 4px !important;
                line-height: 1.2;
            }

            .premium-card-badge {
                display: inline-block;
                padding: 1px 5px;
                background: rgba(214, 175, 55, 0.1) !important;
                border: 1px solid rgba(214, 175, 55, 0.3) !important;
                color: #E2BB3C !important;
                font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
                font-size: 0.6rem;
                font-weight: 700;
                border-radius: 3px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 2px;
            }

            /* --- 🛡️ COLOR SEPARATION BOXES --- */
            .admin-checkpoint-box {
                background: linear-gradient(135deg, #1e1602 0%, #0f0b01 100%) !important;
                border: 1px solid #D4AF37 !important;
                box-shadow: 0 8px 24px rgba(214, 175, 55, 0.15) !important;
                border-radius: 8px;
                padding: 18px;
                margin-bottom: 15px;
            }
            
            .command-hub-pane {
                background: linear-gradient(135deg, #020f1c 0%, #01060d 100%) !important;
                border: 1px solid #00E5FF !important;
                box-shadow: 0 8px 30px rgba(0, 229, 255, 0.1) !important;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
            }

            /* --- NATIVE DIRECT INTERACTION PRINT ENGINE INJECTION --- */
            .lsoep-print-engine-btn {
                display: block;
                width: 100%;
                text-align: center;
                background-color: rgba(5, 22, 43, 0.8) !important;
                color: #00E5FF !important;
                border: 1px solid rgba(0, 229, 255, 0.4) !important;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
                font-size: 0.75rem;
                text-transform: uppercase;
                text-decoration: none !important;
                transition: all 0.2s ease;
            }
            .lsoep-print-engine-btn:hover {
                background-color: #00E5FF !important;
                color: #020b12 !important;
                border-color: #FFFFFF !important;
            }

            div[data-testid="stForm"], .stButton>button {
                background: rgba(5, 22, 43, 0.5) !important;
                backdrop-filter: blur(10px) saturate(140%) !important;
                border: 1px solid #0B3C5D !important;
                border-radius: 4px !important;
            }

            .stButton>button {
                color: #FFFFFF !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                font-size: 0.8rem;
                padding: 4px 12px !important;
                transition: all 0.2s ease;
            }
            .stButton>button:hover {
                background-color: #D4AF37 !important;
                border-color: #FFFFFF !important;
                color: #031424 !important;
                transform: scale(1.01);
            }

            /* --- SIDEBAR MISC ELEMENTS MATRIX --- */
            .admin-header {
                font-family: 'Space Grotesk', sans-serif !important;
                color: #D4AF37 !important;
                font-size: 1.1rem !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 15px !important;
            }

            @media print {
                body, .stApp {
                    background: #FFFFFF !important;
                    color: #000000 !important;
                }
                div[data-testid="stForm"], .stApp::before, header, [data-testid="stSidebar"], button, .honourable-profile-hero::after {
                    display: none !important;
                }
                .stDataFrame div, table, tr, td, th {
                    color: #000000 !important;
                    background-color: #FFFFFF !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 🎨 LSOEP PLATFORM UI CUSTOM STYLING SHEET OVERLAYS
# Project: Balanga/Billiri Federal Constituency (Hon. Ali Isa JC)
# File: styling.py (V94.0 - Ultra-Compact Spacing Realignment)
# ==============================================================================

import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
            /* --- GLOBAL BACKGROUND OVERHAUL & EXECUTIVE TYPOGRAPHY --- */
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=500;600;700;800&family=Space+Grotesk:wght=500;600;700;800&family=Cabinet+Grotesk:wght=800&display=swap');

            .stApp {
                background: radial-gradient(circle at 50% 0%, #051625 0%, #020b12 60%, #000306 100%) !important;
                background-attachment: fixed !important;
            }

            .stApp::before {
                content: "";
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background-image: 
                    linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 1px);
                background-size: 50px 50px;
                background-position: center top;
                pointer-events: none;
                z-index: 0;
                opacity: 0.6;
            }

            body, html, [data-testid="stAppViewContainer"] {
                color: #F8FAFC !important;
                font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Space Grotesk', system-ui, sans-serif !important;
                color: #FFFFFF !important;
            }

            /* --- 🌐 SIDEBAR COLOR SEPARATION MATRIX --- */
            [data-testid="stSidebar"] {
                background-color: #01080f !important;
                border-right: 1px solid rgba(15, 54, 87, 0.5) !important;
            }

            /* e2) Admin Checkpoints Elements / Selectors Styling */
            .sidebar-admin-checkpoint {
                background: linear-gradient(135deg, #1e1602 0%, #0f0b01 100%) !important;
                border: 1px solid #D4AF37 !important;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 10px;
                color: #E2BB3C !important;
                font-family: 'Space Grotesk', sans-serif;
            }

            /* e2) Command Hub Active Streams / Analytics Styling */
            .sidebar-command-hub {
                background: linear-gradient(135deg, #020f1c 0%, #01060d 100%) !important;
                border: 1px solid #00E5FF !important;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 10px;
                color: #00E5FF !important;
                font-family: 'Space Grotesk', sans-serif;
            }

            /* --- 🏛️ ELITE INTERACTIVE PROFILE BANNER HERO CARD --- */
            .honourable-profile-hero {
                position: relative;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: linear-gradient(135deg, rgba(6, 30, 56, 0.9) 0%, rgba(3, 15, 28, 0.98) 100%) !important;
                backdrop-filter: blur(12px) saturate(160%) !important;
                border: 1px solid rgba(214, 175, 55, 0.4) !important;
                border-radius: 8px !important;
                padding: 14px 20px !important;
                margin-bottom: 16px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
                overflow: hidden;
                min-height: 135px;
            }

            .hero-left-content {
                flex: 1;
                padding-right: 150px;
                z-index: 2;
            }

            .hero-badge-strip {
                display: flex;
                gap: 6px;
                margin-bottom: 4px;
            }

            .hero-title-main {
                color: #FFFFFF !important;
                font-size: 1.35rem !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin: 0 !important;
                line-height: 1.2;
            }

            .hero-subtitle-sub {
                color: #D4AF37 !important;
                font-size: 0.9rem !important;
                font-weight: 600 !important;
                margin-top: 2px !important;
            }

            .hero-right-portrait {
                position: absolute !important;
                top: 0 !important;
                bottom: 0 !important;
                right: 0 !important;
                width: 150px !important;
                height: 100% !important;
                background-size: cover !important;
                background-position: center top !important;
                background-repeat: no-repeat !important;
                border-radius: 0 7px 7px 0 !important;
                z-index: 1;
            }

            .honourable-profile-hero::after {
                content: "";
                position: absolute;
                top: 0; bottom: 0; right: 110px; left: 0;
                background: linear-gradient(90deg, rgba(3, 15, 28, 1) 0%, rgba(6, 30, 56, 0.9) 65%, transparent 100%);
                z-index: 1;
                pointer-events: none;
            }

            /* --- ⚡ CONSTITUENCY ENGAGEMENT CHANNELS HEADER MATRIX (TIGHTENED VERTICAL SPACING) --- */
            .nav-title {
                font-family: 'Cabinet Grotesk', 'Space Grotesk', sans-serif !important;
                font-weight: 800 !important;
                font-size: 2.4rem !important;
                letter-spacing: -0.03em !important;
                text-transform: uppercase;
                text-align: center;
                margin-top: 15px !important; /* Pulled down sharply below vacancy tracker */
                margin-bottom: 10px !important; /* Brought significantly closer to the tabs */
                background: linear-gradient(135deg, #FFF6D6 0%, #D4AF37 50%, #AA7C11 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                text-shadow: 0px 4px 20px rgba(214, 175, 55, 0.15) !important;
            }

            /* Ambient Glow Background Wrapper Around Heading Framework (Optimized Padding) */
            div[data-testid="stVerticalBlock"] > div:has(.nav-title) {
                background: radial-gradient(circle at 50% 0%, rgba(20, 35, 65, 0.45) 0%, rgba(2, 16, 36, 0) 75%) !important;
                padding: 10px 20px 5px 20px !important; /* Collapsed top/bottom inner whitespace padding */
                margin-bottom: 5px !important; /* Drastically reduced outer lower margin frame */
            }

            /* --- 🛠️ 13 CONSTITUENCY NAVIGATION GRID CHANNELS TILE MATRIX --- */
            div[data-testid="stHorizontalBlock"] button {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.12rem !important;
                letter-spacing: 0.01em !important;
                color: #FFFFFF !important;
                background: linear-gradient(135deg, #051329 0%, #0A2246 100%) !important;
                border: 1px solid rgba(214, 175, 55, 0.35) !important;
                border-radius: 12px !important;
                padding: 26px 16px !important; 
                min-height: 105px !important; 
                width: 100% !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            }

            div[data-testid="stHorizontalBlock"] button:hover {
                border-color: #D4AF37 !important;
                background: linear-gradient(135deg, #0A2246 0%, #103365 100%) !important;
                color: #D4AF37 !important;
                transform: translateY(-4px) scale(1.015) !important;
                box-shadow: 0 8px 25px rgba(214, 175, 55, 0.25) !important;
            }

            div[data-testid="stHorizontalBlock"] button:active {
                transform: translateY(-1px) scale(0.99) !important;
                box-shadow: 0 2px 10px rgba(214, 175, 55, 0.1) !important;
            }

            /* --- 🔑 SYSTEM ACCESS PORTAL TABS SIDEBAR BUTTONS --- */
            [data-testid="stSidebar"] button {
                font-family: 'Space Grotesk', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.10rem !important;
                letter-spacing: 0.02em !important;
                padding: 12px 10px !important;
            }

            /* --- 🌐 OFFICIAL FACEBOOK BOX ANCHOR --- */
            .inst-link-box {
                display: block !important;
                text-align: center !important;
                background: rgba(214, 175, 55, 0.08) !important;
                border: 1px dashed rgba(214, 175, 55, 0.4) !important;
                padding: 14px 12px !important;
                border-radius: 8px !important;
                color: #D4AF37 !important;
                text-decoration: none !important;
                font-weight: 700 !important;
                font-size: 1.15rem !important;
                transition: background 0.2s ease !important;
            }
            
            .inst-link-box:hover {
                background: rgba(214, 175, 55, 0.15) !important;
                border-style: solid !important;
            }

            /* --- ⚡ LEGACY NAV GRID LAYOUT CONFIGURATIONS --- */
            .premium-nav-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 8px;
                margin-top: 6px;
                margin-bottom: 14px;
            }

            .premium-nav-card {
                background: linear-gradient(145deg, rgba(7, 28, 51, 0.85) 0%, rgba(3, 15, 28, 0.95) 100%) !important;
                backdrop-filter: blur(8px) !important;
                border: 1px solid rgba(15, 54, 87, 0.8) !important;
                border-radius: 6px !important;
                padding: 10px 8px !important;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35);
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .premium-nav-card:hover {
                border-color: #D4AF37 !important;
                background: linear-gradient(145deg, rgba(12, 45, 82, 0.9) 0%, rgba(7, 28, 51, 0.95) 100%) !important;
                box-shadow: 0 6px 18px rgba(0, 229, 255, 0.15);
                transform: translateY(-2px);
            }

            .premium-card-text {
                font-family: 'Space Grotesk', system-ui, sans-serif !important;
                color: #FFFFFF !important;
                font-weight: 600 !important;
                font-size: 0.82rem !important;
                letter-spacing: 0.3px;
                text-transform: uppercase;
                margin-top: 4px !important;
                line-height: 1.2;
            }

            .premium-card-badge {
                display: inline-block;
                padding: 1px 5px;
                background: rgba(214, 175, 55, 0.1) !important;
                border: 1px solid rgba(214, 175, 55, 0.3) !important;
                color: #E2BB3C !important;
                font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
                font-size: 0.6rem;
                font-weight: 700;
                border-radius: 3px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 2px;
            }

            /* --- 🛡️ COLOR SEPARATION BOXES --- */
            .admin-checkpoint-box {
                background: linear-gradient(135deg, #1e1602 0%, #0f0b01 100%) !important;
                border: 1px solid #D4AF37 !important;
                box-shadow: 0 8px 24px rgba(214, 175, 55, 0.15) !important;
                border-radius: 8px;
                padding: 18px;
                margin-bottom: 15px;
            }
            
            .command-hub-pane {
                background: linear-gradient(135deg, #020f1c 0%, #01060d 100%) !important;
                border: 1px solid #00E5FF !important;
                box-shadow: 0 8px 30px rgba(0, 229, 255, 0.1) !important;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
            }

            /* --- NATIVE DIRECT INTERACTION PRINT ENGINE INJECTION --- */
            .lsoep-print-engine-btn {
                display: block;
                width: 100%;
                text-align: center;
                background-color: rgba(5, 22, 43, 0.8) !important;
                color: #00E5FF !important;
                border: 1px solid rgba(0, 229, 255, 0.4) !important;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
                font-size: 0.75rem;
                text-transform: uppercase;
                text-decoration: none !important;
                transition: all 0.2s ease;
            }
            .lsoep-print-engine-btn:hover {
                background-color: #00E5FF !important;
                color: #020b12 !important;
                border-color: #FFFFFF !important;
            }

            div[data-testid="stForm"], .stButton>button {
                background: rgba(5, 22, 43, 0.5) !important;
                backdrop-filter: blur(10px) saturate(140%) !important;
                border: 1px solid #0B3C5D !important;
                border-radius: 4px !important;
            }

            .stButton>button {
                color: #FFFFFF !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                font-size: 0.8rem;
                padding: 4px 12px !important;
                transition: all 0.2s ease;
            }
            .stButton>button:hover {
                background-color: #D4AF37 !important;
                border-color: #FFFFFF !important;
                color: #031424 !important;
                transform: scale(1.01);
            }

            /* --- SIDEBAR MISC ELEMENTS MATRIX --- */
            .admin-header {
                font-family: 'Space Grotesk', sans-serif !important;
                color: #D4AF37 !important;
                font-size: 1.1rem !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 15px !important;
            }

            @media print {
                body, .stApp {
                    background: #FFFFFF !important;
                    color: #000000 !important;
                }
                div[data-testid="stForm"], .stApp::before, header, [data-testid="stSidebar"], button, .honourable-profile-hero::after {
                    display: none !important;
                }
                .stDataFrame div, table, tr, td, th {
                    color: #000000 !important;
                    background-color: #FFFFFF !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
