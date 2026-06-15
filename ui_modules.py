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
    Hides branding/menu while explicitly preserving navigation elements.
    """
    hide_css = """
    <style>
        /* Hide menu, footer, and developer tools */
        #MainMenu {visibility: hidden;}          
        footer {visibility: hidden;}             
        [data-testid="stToolbar"] {visibility: hidden !important;} 
        
        /* Ensure navigation and header controls remain visible */
        [data-testid="stSidebarNav"] {visibility: visible !important;}
        button[kind="header"] {visibility: visible !important;}
        header {visibility: visible !important; background: transparent !important;}
    </style>
    """
    st.markdown(hide_css, unsafe_allow_html=True)
