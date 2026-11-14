import os
import base64
import streamlit as st
import pandas as pd
import json
from json import JSONDecodeError

OFFLINE_REGISTRY_CACHE = "offline_registry_cache.csv"
OFFLINE_METADATA_CACHE = "offline_metadata_cache.json"
COLUMNS_STRUCTURE = [
    "NIN",
    "VIN",
    "Name",
    "LGA",
    "Ward",
    "Status",
    "Category",
    "Skill_Interest",
    "Custom_Skill",
    "Gender",
    "DOB",
    "Disability_Status",
    "Prior_Palliative",
    "Academic_Qual",
    "Admission_Year",
    "Admission_Letter",
    "Phone",
    "Leader_Name",
    "Leader_Contact",
    "Leader_NIN",
    "Leader_LGA",
    "Leader_Ward",
    "Leader_Portfolio",
    "Voucher_Code",
    "Remarks",
    "Timestamp",
]


def image_to_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def trigger_background_autosave():
    try:
        st.session_state.global_registry.to_csv(OFFLINE_REGISTRY_CACHE, index=False)
        meta_payload = {
            "submitted_wards": st.session_state.submitted_wards,
            "submitted_pus": st.session_state.submitted_pus,
        }
        with open(OFFLINE_METADATA_CACHE, "w") as f:
            json.dump(meta_payload, f)
    except (OSError, TypeError, ValueError) as e:
        st.caption(f"Autosave sync bypass: {e}")


def initialize_and_recover_system_states():
    if "global_registry" not in st.session_state:
        if os.path.exists(OFFLINE_REGISTRY_CACHE):
            try:
                st.session_state.global_registry = pd.read_csv(OFFLINE_REGISTRY_CACHE)
            except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
                st.warning(f"The offline registry cache could not be read: {exc}")
                os.remove(OFFLINE_REGISTRY_CACHE)

        if "global_registry" not in st.session_state:
            st.session_state.global_registry = pd.DataFrame(
                columns=COLUMNS_STRUCTURE
            )

    if (
        "submitted_wards" not in st.session_state
        or "submitted_pus" not in st.session_state
    ):
        recovered_meta = False
        if os.path.exists(OFFLINE_METADATA_CACHE):
            try:
                with open(OFFLINE_METADATA_CACHE, "r") as f:
                    meta_payload = json.load(f)
                st.session_state.submitted_wards = meta_payload.get(
                    "submitted_wards", {}
                )
                st.session_state.submitted_pus = meta_payload.get("submitted_pus", {})
                recovered_meta = True
            except (OSError, JSONDecodeError, TypeError) as exc:
                st.warning(f"The offline metadata cache could not be read: {exc}")
                os.remove(OFFLINE_METADATA_CACHE)

        if not recovered_meta:
            st.session_state.submitted_wards = {}
            st.session_state.submitted_pus = {}

    if "current_page" not in st.session_state:
        st.session_state.current_page = "skill_form"
    if "radar_threat" not in st.session_state:
        st.session_state.radar_threat = False
    if "threat_msg" not in st.session_state:
        st.session_state.threat_msg = ""
    if "recycle_bin_registry" not in st.session_state:
        st.session_state.recycle_bin_registry = None
    if "recycle_bin_wards" not in st.session_state:
        st.session_state.recycle_bin_wards = {}
    if "recycle_bin_pus" not in st.session_state:
        st.session_state.recycle_bin_pus = {}
