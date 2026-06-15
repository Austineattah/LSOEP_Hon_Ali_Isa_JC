import streamlit as st


def styled_header(text, color="#191970", font_size="28px"):
    """Renders a header in uppercase, with specified color and font size."""
    html = f"""
    <h2 style="
        color: {color}; 
        font-size: {font_size}; 
        text-transform: uppercase; 
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 10px;
    ">
        {text}
    </h2>
    """
    st.markdown(html, unsafe_allow_html=True)


def remove_streamlit_chrome():
    """
    Aggressive removal of all Streamlit branding, including logos,
    deploy buttons, and developer menus, while preserving navigation.
    """
    hide_css = """
    <style>
        /* Hide Hamburger Menu, Footer, and Toolbar */
        #MainMenu, footer, [data-testid="stToolbar"] {
            visibility: hidden !important;
            display: none !important;
        }

        /* Hide 'About' link, deployment button, and default Streamlit logos */
        [data-testid="stAppDeployButton"], 
        [data-testid="stLogo"], 
        [data-testid="stDecoration"] {
            display: none !important;
        }

        /* Ensure header and navigation buttons remain visible */
        header {
            visibility: visible !important; 
            background: transparent !important;
        }
        
        button[kind="header"], [data-testid="stSidebarNav"], button {
            visibility: visible !important;
            z-index: 9999 !important;
        }
    </style>
    """
    st.markdown(hide_css, unsafe_allow_html=True)
