# --- CONSOLIDATED GEOGRAPHICAL CONFIGURATION ---
# Updated with Billiri and Balanga LGAs
LGA_WARD_DATA = {
    "BILLIRI": [
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
    "BALANGA": [
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

# The Column structure remains optimal and unchanged
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


def get_wards(lga_name):
    """Helper function to dynamically retrieve wards based on LGA selection."""
    return LGA_WARD_DATA.get(lga_name.upper(), [])
