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
