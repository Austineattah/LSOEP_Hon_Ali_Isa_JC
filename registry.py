# ==============================================================================
# 🏛️ LSOEP FEDERAL MASTER REGISTRY & GEOGRAPHIC DATA LAYER
# Project: Balanga/Billiri Federal Constituency (HONOURABLE ALI ISA JC, PhD)
# File: registry.py (Aggregated Master Data & Session Memory State Core)
# ==============================================================================

import streamlit as st
import pandas as pd

# Institutional Software Display Branding Variables
HON_TITLE = "HONOURABLE ALI ISA JC, PhD"
CONSTITUENCY_DESC = "BALANGA/BILLIRI FEDERAL CONSTITUENCY (GOMBE STATE)"

GEOGRAPHY = {
    "BALANGA": [
        "Bambam",
        "Bangu",
        "Dadiya",
        "Degri",
        "Gelengu",
        "Kindiyo",
        "Mona",
        "Nyuwar/Jessu",
        "Swa",
        "Talasse/Dung/Reme",
    ],
    "BILLIRI": [
        "Banganje North",
        "Banganje South",
        "Bare",
        "Billiri North",
        "Billiri South",
        "Kalmai",
        "Tal",
        "Tanglang",
        "Todi",
        "Tudu-Kwaya",
    ],
}

LGA_WARD_DATA = {
    "BALANGA": GEOGRAPHY["BALANGA"],
    "BILLIRI": GEOGRAPHY["BILLIRI"],
    "Balanga": GEOGRAPHY["BALANGA"],
    "Billiri": GEOGRAPHY["BILLIRI"],
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

# ==============================================================================
# VERIFIED FEDERAL GOVERNMENT INDUSTRIAL GRANTS & SCHEMES
# ==============================================================================
FEDERAL_INDUSTRIAL_GRANTS = [
    {
        "title": "SMEDAN Conditional Grant Scheme (CGS)",
        "agency": "Small & Medium Enterprises Development Agency of Nigeria (SMEDAN)",
        "funding_type": "Non-Repayable Grant",
        "funding_amount": "₦50,000",
        "eligibility": "Nano/Micro businesses (1-4 employees) with employment commitment; Nigerian citizens aged 18+",
        "description": "Non-repayable grant for nano and micro business operators with commitment to employment creation. Supports business registration, equipment, and working capital.",
        "key_requirements": [
            "Business registration (CAC/BN verification)",
            "Employment commitment (minimum 1 new job)",
            "Valid NIN and business identification",
            "Completion of SMEDAN business skills training",
        ],
        "application_url": "https://smedan.gov.ng/our-programs/cgs/",
        "status": "Active",
        "updated": "2026-11-15",
    },
    {
        "title": "Bank of Industry (BOI) Intervention Programmes",
        "agency": "Bank of Industry (BOI)",
        "funding_type": "Financing & Intervention Funds",
        "funding_amount": "Varies (up to ₦500M)",
        "eligibility": "MSME operators, industries, manufacturing; registered businesses with 6+ months operation",
        "description": "Multiple intervention programs including iProgrammes (tech startups), RAPID (rapid finance for businesses), and Women Fund for female entrepreneurs. Flexible terms and competitive rates.",
        "key_requirements": [
            "MSME or industrial business registration",
            "6+ months business operation history",
            "Valid business plan and financial statements",
            "Collateral as per program requirements",
        ],
        "application_url": "https://iprogrammes.boi.ng/",
        "status": "Active",
        "updated": "2026-11-15",
    },
    {
        "title": "Presidential Conditional Grant Scheme (PCGS) & MSME Clinics",
        "agency": "Federal Ministry of Industry, Trade and Investment (FMITI)",
        "funding_type": "Non-Repayable Conditional Grant",
        "funding_amount": "Varies by category (₦100,000 - ₦5M)",
        "eligibility": "Nigerian MSMEs, cooperatives, artisans; meet FMITI classification criteria",
        "description": "Federal MSME grant portal offering multiple schemes for business expansion, equipment purchase, and capacity building. Includes MSME clinics for business advisory support.",
        "key_requirements": [
            "FMITI MSME registration",
            "Viable business plan",
            "Financial transparency (6-12 months records)",
            "Compliance with environmental/safety standards",
        ],
        "application_url": "https://fedgrantandloan.gov.ng/",
        "status": "Active",
        "updated": "2026-11-15",
    },
    {
        "title": "NEPC Export Expansion Grant (EEG)",
        "agency": "Nigerian Export Promotion Council (NEPC)",
        "funding_type": "Non-Oil Export Grant",
        "funding_amount": "Up to ₦10M",
        "eligibility": "Non-oil export businesses, manufacturers, agro-exporters; registered NEPC members",
        "description": "Government support for non-oil export businesses seeking to expand export capacity, access international markets, and build export competitiveness.",
        "key_requirements": [
            "Export capability demonstration",
            "NEPC membership",
            "Product/service quality certification",
            "Market access or export contract",
        ],
        "application_url": "https://nepc.gov.ng/",
        "status": "Active",
        "updated": "2026-11-15",
    },
    {
        "title": "Federal Ministry of Education Student Venture Capital Grant (S-VCG)",
        "agency": "Federal Ministry of Education & Federal Ministry of Youth Development",
        "funding_type": "Venture Capital Grant",
        "funding_amount": "Up to ₦50M (STEM startups)",
        "eligibility": "Nigerian students, recent graduates (under 35); STEM, tech, and innovation-focused ventures",
        "description": "Federal government support for student and graduate entrepreneurs with STEM-focused business ideas. Includes mentorship, training, and non-dilutive funding.",
        "key_requirements": [
            "STEM/tech/innovation focus",
            "Registered business or startup",
            "Viable business plan with market research",
            "Evidence of student/recent graduate status",
        ],
        "application_url": "https://svcg.education.gov.ng/",
        "status": "Active",
        "updated": "2026-11-15",
    },
    {
        "title": "FIRS Business Partners Program (FBP)",
        "agency": "Federal Inland Revenue Service (FIRS)",
        "funding_type": "Tax Incentives & Support",
        "funding_amount": "Tax relief up to 3 years (varies by sector)",
        "eligibility": "New businesses in priority sectors (agriculture, manufacturing, tech); registered with FIRS",
        "description": "Tax incentive program supporting new businesses in priority sectors with exemptions and reduced rates for initial operational years.",
        "key_requirements": [
            "Business in designated priority sectors",
            "FIRS tax registration",
            "Business plan and financial projections",
            "Compliance with corporate governance standards",
        ],
        "application_url": "https://www.firs.gov.ng/",
        "status": "Active",
        "updated": "2026-11-15",
    },
]

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
