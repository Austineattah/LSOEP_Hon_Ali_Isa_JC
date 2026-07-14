# ==============================================================================
# 🏛️ LSOEP PORTAL PLATFORM ENGINE - STYLING INTERFACE ENGINE
# Project: Balanga/Billiri Federal Constituency (Honourable Ali Isa JC, PhD)
# File: styling.py (V65.0 - Full 171-Line High-Prestige Extended Matrix)
# ==============================================================================

import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
            /* ==========================================================================
               1. GLOBAL APP VIEW CONTAINERS & OVERRIDES
               ========================================================================== */
            html {
                color: #F0F0F0 !important;
            }
            body {
                color: #F0F0F0 !important;
            }
            [data-testid="stAppViewContainer"] {
                color: #F0F0F0 !important;
                background-color: #021024 !important;
            }
            
            /* ==========================================================================
               2. SECURE SIDEBAR INTERFACE OVERRIDES
               ========================================================================== */
            [data-testid="stSidebar"] {
                background-color: #041d3d !important;
                border-right: 2px solid #D4AF37 !important;
            }
            .st-emotion-cache-16txtl3 {
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            .admin-header {
                font-size: 1.5rem !important;
                color: #D4AF37 !important;
                text-align: center !important;
                margin-bottom: 1rem !important;
                font-weight: 700 !important;
                letter-spacing: 1px !important;
            }
            
            /* ==========================================================================
               3. GATEWAY TITLES & NAVIGATION HEADER TYPOGRAPHY
               ========================================================================== */
            .nav-title {
                text-align: center !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 1.5px !important;
            }
            
            /* ==========================================================================
               4. GIGANTIC CHANNELS CONTINUOUS PULSE ANIMATION MATRIX
               ========================================================================== */
            @keyframes pulse-glow {
                0% {
                    transform: scale(1);
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
                    border-color: #D4AF37;
                }
                50% {
                    transform: scale(1.02);
                    box-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
                    border-color: #00E5FF;
                }
                100% {
                    transform: scale(1);
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
                    border-color: #D4AF37;
                }
            }
            .pulse-wrapper button {
                animation: pulse-glow 3s ease-in-out infinite !important;
            }
            
            /* ==========================================================================
               5. CHANNEL TABS DESIGN ENGINE (GIGANTIC BOX CONFIGURATION)
               ========================================================================== */
            .stButton>button {
                border-radius: 16px !important;
                border-top: 3px solid #D4AF37 !important;
                border-bottom: 3px solid #D4AF37 !important;
                border-left: 3px solid #D4AF37 !important;
                border-right: 3px solid #D4AF37 !important;
                background-color: #0B3C5D !important;
                color: #FFFFFF !important;
                font-weight: 800 !important;
                padding-top: 2.2rem !important;
                padding-bottom: 2.2rem !important;
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
                font-size: 1.35rem !important;
                min-height: 140px !important; 
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                letter-spacing: 0.5px !important;
                line-height: 1.4 !important;
                transition: background-color 0.3s, color 0.3s, border-color 0.3s, transform 0.2s, box-shadow 0.2s !important;
            }
            .stButton>button:hover {
                background-color: #D4AF37 !important;
                border-top: 3px solid #FFFFFF !important;
                border-bottom: 3px solid #FFFFFF !important;
                border-left: 3px solid #FFFFFF !important;
                border-right: 3px solid #FFFFFF !important;
                color: #021024 !important;
                transform: scale(1.05) translateY(-4px) !important; 
                box-shadow: 0 12px 35px rgba(212, 175, 55, 0.5) !important;
            }

            /* ==========================================================================
               6. SECURE NAVIGATION RETURN GATEWAY BLOCK
               ========================================================================== */
            div.stButton > button[key*="nav_btn_return"] {
                padding-top: 2.5rem !important;
                padding-bottom: 2.5rem !important;
                padding-left: 2.5rem !important;
                padding-right: 2.5rem !important;
                font-size: 2.2rem !important; 
                font-weight: 900 !important; 
                background: linear-gradient(90deg, #0B3C5D, #041d3d) !important;
                border-top: 4px solid #00E5FF !important;
                border-bottom: 4px solid #00E5FF !important;
                border-left: 4px solid #00E5FF !important;
                border-right: 4px solid #00E5FF !important;
                min-height: 100px !important;
                width: 100% !important;
                box-shadow: 0 0 25px rgba(0, 229, 255, 0.4) !important;
                text-shadow: 0 0 8px rgba(255,255,255,0.6) !important;
            }
            div.stButton > button[key*="nav_btn_return"]:hover {
                background: #00E5FF !important;
                color: #021024 !important;
                border-top: 4px solid #FFFFFF !important;
                border-bottom: 4px solid #FFFFFF !important;
                border-left: 4px solid #FFFFFF !important;
                border-right: 4px solid #FFFFFF !important;
                box-shadow: 0 0 40px rgba(0, 229, 255, 0.8) !important;
            }

            /* ==========================================================================
               7. INSTITUTIONAL SOCIAL EMBED LINKS
               ========================================================================== */
            .inst-link-box {
                display: block !important;
                background-color: #D4AF37 !important;
                color: #061A33 !important;
                padding: 12px !important;
                border-radius: 8px !important;
                text-align: center !important;
                font-weight: bold !important;
                text-decoration: none !important;
                border: 1px solid #FFFFFF !important;
                transition: background-color 0.3s, transform 0.2s !important;
            }
            .inst-link-box:hover {
                background-color: #b89b31 !important;
                transform: scale(1.03) !important;
            }

            /* ==========================================================================
               8. FORM FIELDS, TEXT RECEPTACLES & DROPDOWN CONTAINERS
               ========================================================================== */
            .stTextInput>div>div>input {
                color: #FFFFFF !important;
                background-color: rgba(6, 26, 51, 0.8) !important;
                border: 2px solid #0B3C5D !important;
                border-radius: 8px !important;
            }
            .stSelectbox>div>div>div {
                color: #FFFFFF !important;
                background-color: rgba(6, 26, 51, 0.8) !important;
                border: 2px solid #0B3C5D !important;
                border-radius: 8px !important;
            }
            .stTextArea>div>div>textarea {
                color: #FFFFFF !important;
                background-color: rgba(6, 26, 51, 0.8) !important;
                border: 2px solid #0B3C5D !important;
                border-radius: 8px !important;
            }
            .stTextInput, .stSelectbox, .stDateInput, .stTextArea, .stFileUploader, .stCameraInput {
                margin-bottom: 12px !important;
            }

            /* ==========================================================================
               9. FIELD OFFICE INTERNAL MODULE HEADERS
               ========================================================================== */
            .supervisor-header {
                background-color: #0B3C5D !important;
                color: #D4AF37 !important;
                padding: 1.5rem !important;
                border-radius: 12px !important;
                margin-bottom: 1.8rem !important;
                border-left: 6px solid #D4AF37 !important;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
            }
            
            /* ==========================================================================
               10. PRINTABLE DISBURSEMENT SLIP BLOCK
               ========================================================================== */
            .printable-slip-box {
                 background-color: #FFFFFF !important;
                 color: #1A1A1A !important;
                 border: 3px double #D4AF37 !important;
                 border-radius: 10px !important;
                 padding: 25px !important;
                 font-family: 'Courier New', Courier, monospace !important;
                 margin-top: 20px !important;
                 box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            }
            .slip-header {
                 font-size: 1.3rem !important;
                 font-weight: bold !important;
                 text-align: center !important;
                 border-bottom: 2px dashed #0B3C5D !important;
                 margin-bottom: 18px !important;
                 padding-bottom: 12px !important;
                 color: #0B3C5D !important;
            }
            .slip-row {
                 display: flex !important;
                 justify-content: space-between !important;
                 margin-bottom: 10px !important;
                 font-size: 1.05rem !important;
                 border-bottom: 1px dotted #E0E0E0 !important;
                 padding-bottom: 4px !important;
            }
            .slip-row span:first-child {
                 font-weight: bold !important;
                 color: #333333 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
