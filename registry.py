# ==============================================================================
# 🏛️ LSOEP FEDERAL MASTER REGISTRY & GEOGRAPHIC DATA LAYER
# Project: Balanga and Billiri Federal Constituency (Hon. Ali Isa JC, PhD)
# File: registry.py (Aggregated Master Data & Session Memory State Core)
# ==============================================================================

import streamlit as st
import pandas as pd
import os
import json

# Institutional Software Display Branding Variables
HON_TITLE = "Hon. Ali Isa JC, PhD"
CONSTITUENCY_DESC = "Balanga and Billiri Federal Constituency (Gombe State)"

GEOGRAPHY = {
    "Billiri LGA": [
        "BAGANJE NORTH",
        "BAGANJE SOUTH",
        "BARE",
        "BILLIRI NORTH",
        "BILLIRI SOUTH",
        "KALMAI",
        "TAL",
        "TANGLANG",
        "TODI",
        "TUDU KWAYA",
    ],
    "Balanga LGA": [
        "BAMBAM",
        "BANGU",
        "DADIYA",
        "GELENGU / BALANGA",
        "KINDIYO",
        "KULANI / DEGRE / SIKKAM",
        "MWONA",
        "NYUWAR / JESSU",
        "SWA / REF / W. WAJA",
        "TALASSE / DONG / REME",
    ],
}

LGA_WARD_DATA = {
    "BILLIRI": GEOGRAPHY["Billiri LGA"],
    "BALANGA": GEOGRAPHY["Balanga LGA"],
}

# 🏛️ EXPLICIT COMMUNITY STAKEHOLDER DIRECTORY
COMMUNITY_LEADERS = {
    "Hon. Ali Isa JC, PhD": {
        "contact": "08000000000",
        "nin": "00000000000",
        "lga": "BALANGA",
        "ward": "CENTRAL",
        "portfolio": "Federal Representative, Balanga/Billiri",
    },
    "Dr. Musa Tango": {
        "contact": "08011111111",
        "nin": "11111111111",
        "lga": "BILLIRI",
        "ward": "TAL",
        "portfolio": "Director of Skills, LSOEP",
    },
    "Hajia Amina S. Ahmed": {
        "contact": "08022222222",
        "nin": "22222222222",
        "lga": "BALANGA",
        "ward": "DADIYA",
        "portfolio": "Women Mobilization Lead, Gombe South",
    },
}

# ==============================================================================
# NEW: LEGISLATIVE DATA
# ==============================================================================
SPONSORED_BILLS = [
    {
        "title": "A Bill for an Act to Establish the Federal College of Horticulture, Dadin Kowa",
        "status": "Passed",
        "summary": "This landmark bill establishes a specialized Federal College of Horticulture in Dadin Kowa, Gombe State. It aims to promote agricultural education, develop modern horticultural practices, and create a hub for research and innovation in the North-East, thereby boosting food security and providing employment opportunities for the youth.",
    },
    {
        "title": "A Bill for an Act to amend the Trafficking in Persons (Prohibition) Enforcement and Administration Act, 2015",
        "status": "In Committee",
        "summary": "This bill seeks to strengthen the legal framework for combating human trafficking by introducing stricter penalties for offenders, enhancing victim protection measures, and improving the operational capacity of NAPTIP to investigate and prosecute trafficking cases.",
    },
    {
        "title": "A Bill for an Act to Establish the National Skills and Innovation Development Council",
        "status": "First Reading",
        "summary": "Proposes the creation of a national council to streamline and regulate vocational and technical training across Nigeria. The goal is to standardize certification, promote innovation, and align skill acquisition programs with the demands of the modern economy.",
    },
    {
        "title": "Motion on the Need to Address the Menace of Soil Erosion in Balanga/Billiri Federal Constituency",
        "status": "Adopted",
        "summary": "A successful motion that called the Federal Government's attention to the severe ecological degradation caused by soil erosion in the constituency. The motion urged relevant agencies like the Ecological Fund Office to implement urgent intervention projects to protect farmlands, infrastructure, and residential areas.",
    },
]

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
    """Aggregated Session State Initializer Engine called natively by main.py."""
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
