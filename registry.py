# ==============================================================================
# 🏛️ LSOEP FEDERAL MASTER REGISTRY & GEOGRAPHIC DATA LAYER
# Project: Balanga/Billiri Federal Constituency (HONOURABLE ALI ISA JC, PhD)
# File: registry.py (Aggregated Master Data & Session Memory State Core)
# ==============================================================================

import streamlit as st
import pandas as pd
import os
import json

# Institutional Software Display Branding Variables
HON_TITLE = "HONOURABLE ALI ISA JC, PhD"
CONSTITUENCY_DESC = "BALANGA/BILLIRI FEDERAL CONSTITUENCY (GOMBE STATE)"

GEOGRAPHY = {
    "BALANGA": [
        "Wuro-dadiya",
        "Gelengu",
        "Bangu",
        "Dala-waja",
        "Nyuwar",
        "Jessu",
        "Kindiyo",
        "Kulani",
        "Sikkam",
        "Chama",
    ],
    "BILLIRI": ["Billiri-North", "Billiri-South", "Kalmai", "Tal", "Todi"],
}

LGA_WARD_DATA = {
    "BALANGA": GEOGRAPHY["BALANGA"],
    "BILLIRI": GEOGRAPHY["BILLIRI"],
}

# 🏛️ EXPLICIT COMMUNITY STAKEHOLDER DIRECTORY
COMMUNITY_LEADERS = {
    "HONOURABLE ALI ISA JC, PhD": {
        "contact": "08000000000",
        "nin": "00000000000",
        "lga": "BILLIRI",
        "ward": "Billiri-South",
        "portfolio": "Federal Representative, Balanga/Billiri",
    },
}

# ==============================================================================
# LEGISLATIVE DATA - STATUTORY BILLS & GROUND TRUTH MOTIONS
# ==============================================================================
SPONSORED_BILLS = [
    {
        "title": "A Bill for an Act to Establish the Federal College of Horticulture, Dadin Kowa, Gombe State",
        "description": "This bill seeks to establish a specialized federal institution for horticultural studies in Dadin Kowa, aiming to boost the agricultural sector, provide specialized training, and promote modern horticultural practices in Gombe State and the nation.",
        "status": "Awaiting Second Reading",
        "date": "2023-11-20",
        "progress": 30,
    },
    {
        "title": "A Motion on the Need to Address the Devastating Effects of Erosion in Balanga/Billiri Federal Constituency",
        "description": "This motion calls for urgent federal intervention through the Ecological Fund Office to address severe erosion threatening communities, farmlands, and infrastructure across the Balanga and Billiri LGAs.",
        "status": "Passed",
        "date": "2024-01-25",
        "progress": 100,
    },
    {
        "title": "Motion on the Urgent Need to Rehabilitate the Billiri-Filiya-Taraba Border Federal Highway",
        "description": "Urgent directive targeting the Federal Ministry of Works and FERMA to reconstruct collapsed portions and bridges along the critical economic trade road connecting Gombe and Taraba states.",
        "status": "Passed (Referred to Committee on Works)",
        "date": "2024-05-14",
        "progress": 100,
    },
    {
        "title": "Motion Deploring Outbreak of Waterborne Diseases and Urging Federal Intervention in Balanga Communities",
        "description": "Compelled the Federal Ministry of Water Resources and NCDC to instantly provide clean modular water facilities and medical disaster deployment to rural wards across Balanga LGA.",
        "status": "Passed (Monitored for Compliance)",
        "date": "2024-10-09",
        "progress": 100,
    },
    {
        "title": "Motion on Enhancing Security Coverage and Border Patrols along Gombe-Taraba-Adamawa Axis",
        "description": "Demanded additional tactical deployments, mobile military operational structures, and enhanced local surveillance logistics around the vulnerability perimeters of Balanga and Billiri.",
        "status": "Passed (Executive Action Pending)",
        "date": "2025-02-18",
        "progress": 100,
    },
    {
        "title": "A Bill for an Act to Amend the National Agricultural Development Fund Act",
        "description": "Seeks to restructure fiscal allocations to prioritize underserved savannah zones and guarantee dry-season agricultural inputs directly to smallholder cooperatives inside rural constituencies.",
        "status": "First Reading Passed",
        "date": "2025-06-11",
        "progress": 15,
    },
]

# Primary interface mapping data hook
HON_ALI_SPONSORED_BILLS = SPONSORED_BILLS

# ==============================================================================
# STRATEGIC COMMITTEE CREDENTIALS
# ==============================================================================
STRATEGIC_COMMITTEE_NAMES = [
    "Committee 1: Finance & Appropriations",
    "Committee 2: Healthcare & Social Welfare",
    "Committee 3: Education & Human Capital",
    "Committee 4: Infrastructure & Public Works",
    "Committee 5: Agriculture & Rural Development",
    "Committee 6: Security & Community Affairs",
    "Committee 7: Youth & Sports Development",
    "Committee 8: Women Affairs & Inclusion",
    "Committee 9: Legislative Liaison & Compliance",
    "Committee 10: Constituency Outreach & Engagement",
]

STRATEGIC_COMMITTEE_PASSWORDS = {
    "Committee 1: Finance & Appropriations": "ten",
    "Committee 2: Healthcare & Social Welfare": "nine",
    "Committee 3: Education & Human Capital": "eight",
    "Committee 4: Infrastructure & Public Works": "seven",
    "Committee 5: Agriculture & Rural Development": "six",
    "Committee 6: Security & Community Affairs": "five",
    "Committee 7: Youth & Sports Development": "four",
    "Committee 8: Women Affairs & Inclusion": "three",
    "Committee 9: Legislative Liaison & Compliance": "two",
    "Committee 10: Constituency Outreach & Engagement": "one",
}

PROJECT_PARTITION_ID = "Balanga/Billiri_GOMBE"
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
STRATEGIC_COMMITTEE_COLS = [
    "Committee_Node",
    "First_Name",
    "Surname",
    "Contact_Number",
    "Gender",
    "Account_Number",
    "Account_Name",
    "Bank",
    "LGA",
    "Ward",
    "NIN_Number",
    "Voters_Card_Number",
    "Timestamp",
]
LITIGATION_AGENT_COLS = [
    "Polling_Unit_Name",
    "Ward_Collation_Officer_Key",
    "Accredited_Voters",
    "APC_Votes",
    "NDC_Votes",
    "PDP_Votes",
    "ADC_Votes",
    "BVAS_Serial_Number",
    "Incident_Occurred",
    "Incident_Form_Scenario",
    "Timestamp",
]

OFFLINE_REGISTRY_CACHE = "offline_registry_cache.csv"
OFFLINE_METADATA_CACHE = "offline_metadata_cache.json"
ANNOUNCEMENT_CACHE_FILE = "announcement_cache.txt"


def initialize_system_states():
    if "global_scrolling_announcement" not in st.session_state:
        try:
            with open(ANNOUNCEMENT_CACHE_FILE, "r") as f:
                st.session_state.global_scrolling_announcement = f.read()
        except FileNotFoundError:
            st.session_state.global_scrolling_announcement = "NOTICE: OFFICIAL DIGITAL LEDGER GATEWAY DEPLOYED FOR TRANSPARENT ACCOUNTABILITY."
    if "global_registry" not in st.session_state:
        st.session_state.global_registry = pd.DataFrame(columns=COLUMNS_STRUCTURE)
    if "strategic_committee_registry" not in st.session_state:
        st.session_state.strategic_committee_registry = pd.DataFrame(
            columns=STRATEGIC_COMMITTEE_COLS
        )
    if "committee_double_dipping_ledger" not in st.session_state:
        st.session_state.committee_double_dipping_ledger = {}
    if "submitted_wards" not in st.session_state:
        st.session_state.submitted_wards = {}
    if "submitted_pus" not in st.session_state:
        st.session_state.submitted_pus = {}
    if "agent_field_registry" not in st.session_state:
        st.session_state.agent_field_registry = pd.DataFrame(
            columns=LITIGATION_AGENT_COLS
        )
    if "radar_threat" not in st.session_state:
        st.session_state.radar_threat = False
    if "threat_msg" not in st.session_state:
        st.session_state.threat_msg = ""
    if "authenticated_committee" not in st.session_state:
        st.session_state.authenticated_committee = None
