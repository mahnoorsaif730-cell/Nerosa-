import os
import re
from difflib import get_close_matches

import pandas as pd


# ---------------------------------------------------------
# FIND CSV FILE
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "medicines.csv"
)


# ---------------------------------------------------------
# CHECK CSV EXISTS
# ---------------------------------------------------------

if not os.path.exists(CSV_PATH):

    raise FileNotFoundError(
        "medicines.csv was not found. "
        "Please upload medicines.csv to the same "
        "GitHub repository as app.py."
    )


# ---------------------------------------------------------
# LOAD CSV
# ---------------------------------------------------------

try:

    df = pd.read_csv(
        CSV_PATH
    )

except Exception as error:

    raise RuntimeError(
        f"Could not read medicines.csv: {error}"
    )


# ---------------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------------

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
)


# ---------------------------------------------------------
# REQUIRED COLUMNS
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    "medicine_name",
    "drug_type",
    "main_use",
    "common_forms",
    "safety_note",
    "source_reference",
]


missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]


if missing_columns:

    raise ValueError(
        "The CSV is missing these required columns: "
        + ", ".join(missing_columns)
    )


# ---------------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------------

for column in REQUIRED_COLUMNS:

    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# Convert dataframe into a list of dictionaries

MEDICINES = df.to_dict(
    orient="records"
)


# ---------------------------------------------------------
# TEXT NORMALIZATION
# ---------------------------------------------------------

def normalize_text(text):

    text = str(text).lower().strip()

    # Replace common punctuation with spaces

    text = re.sub(
        r"[^a-z0-9\s-]",
        "",
        text
    )

    # Remove extra spaces

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ---------------------------------------------------------
# MEDICINE SEARCH
# ---------------------------------------------------------

def retrieve_info(user_input):

    if not user_input:
        return None

    query = normalize_text(
        user_input
    )

    if not query:
        return None


    # -----------------------------------------------------
    # 1. EXACT MATCH
    # -----------------------------------------------------

    for medicine in MEDICINES:

        medicine_name = normalize_text(
            medicine["medicine_name"]
        )

        if query == medicine_name:

            return medicine


    # -----------------------------------------------------
    # 2. PARTIAL MATCH
    # -----------------------------------------------------

    for medicine in MEDICINES:

        medicine_name = normalize_text(
            medicine["medicine_name"]
        )

        if (
            query in medicine_name
            or medicine_name in query
        ):

            return medicine


    # -----------------------------------------------------
    # 3. FUZZY MATCH
    # -----------------------------------------------------

    medicine_names = [
        normalize_text(
            medicine["medicine_name"]
        )
        for medicine in MEDICINES
    ]


    matches = get_close_matches(
        query,
        medicine_names,
        n=1,
        cutoff=0.60
    )


    if matches:

        matched_name = matches[0]

        for medicine in MEDICINES:

            medicine_name = normalize_text(
                medicine["medicine_name"]
            )

            if medicine_name == matched_name:

                return medicine


    # -----------------------------------------------------
    # NO MATCH
    # -----------------------------------------------------

    return None


# ---------------------------------------------------------
# GET ALL MEDICINES
# ---------------------------------------------------------

def get_all_medicines():

    return MEDICINES
