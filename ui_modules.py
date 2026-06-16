import streamlit as st
import os
import pandas as pd
import datetime
import time
from utils import image_to_base64, trigger_background_autosave
from registry import COLUMNS_STRUCTURE


def render_mace_flash(image_path="mace_emblem.png"):
    """
    Renders an intermittent flash of the mace emblem.
    'image_path' should point to your local file.
    """
    mace_placeholder = st.empty()

    # This loop runs the animation; you can wrap this in a
    # persistent session state if you want it to loop indefinitely.
    for _ in range(3):  # Number of flashes
        # Display the image
        mace_placeholder.image(
            image_path, width=150, caption="OFFICE OF THE SENATE PRESIDENT"
        )
        time.sleep(0.5)  # Time the image stays visible

        # Clear the space (the "Fade off" effect)
        mace_placeholder.empty()
        time.sleep(1.0)  # Time the image stays hidden


def render_marquee_header():
    mace_path = os.path.join("assets", "digital_mace.png")
    portrait_path = os.path.join("assets", "hon_ali.png")

    mace_base64 = image_to_base64(mace_path)
    portrait_base64 = image_to_base64(portrait_path)

    mace_html = (
        f'<img src="data:image/png;base64,{mace_base64}">'
        if mace_base64
        else "<p>Mace image not found</p>"
    )
    portrait_html = (
        f'<img src="data:image/png;base64,{portrait_base64}">'
        if portrait_base64
        else "<p>Portrait not found. Please upload 'hon_ali.png' to the 'assets' folder.</p>"
    )

    st.markdown(
        f"""
        <div class="unified-command-vault">
            <div class="mace-vault-shield">
                {mace_html}
            </div>
            <div class="vault-text-block">
                <h1>HONOURABLE ALI ISA JC PhD</h1>
                <div class="sub-title">MINORITY WHIP<br>BILLIRI/BALANGA FEDERAL CONSTITUENCY</div>
                <div class="geo-stamp">GOMBE STATE</div>
            </div>
            <div class="photo-vault-shield">
                {portrait_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="margin-top:15px; background:linear-gradient(180deg, #061a33 0%, #020b17 100%); padding:8px; border-radius:8px;">'
        '  <marquee scrollamount="4" style="color:#FFFFFF; font-weight:800; font-size:16px; letter-spacing:1.5px; font-family:sans-serif;">'
        "    HONOURABLE ALI ISA JC CARES..... SAME VISION BUT DIFFERENT PLATFORM TO SERVE THE GOOD PEOPLE OF BILLIRI/BALANGA WITH INTEGRITY, TRANSPARENCY, ACCOUNTABILITY DRIVEN BY PEOPLE ORIENTED PROGRAMS."
        "  </marquee>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_module_download_trigger(data_source, filename_prefix, unique_key):
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
    st.markdown("---")
    st.subheader("🚨 Institutional Data Purge Zone")
    confirm_purge = st.text_input(
        "Type 'PURGE SYSTEM DATA' to authorize reset:", key=f"purge_box_{key_suffix}"
    )
    if st.button(
        "💥 EXECUTE SYSTEM PURGE afresh", type="primary", key=f"purge_btn_{key_suffix}"
    ):
        if confirm_purge == "PURGE SYSTEM DATA":
            st.session_state.global_registry = pd.DataFrame(columns=COLUMNS_STRUCTURE)
            st.session_state.submitted_wards = {}
            st.session_state.submitted_pus = {}
            trigger_background_autosave()
            st.success("System tracking layers reset completely.")
            st.sidebar.rerun()
