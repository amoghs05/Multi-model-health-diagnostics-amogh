import pandas as pd
import re

REFERENCE_RANGES = {
    "hemoglobin": (13.0, 17.0),
    "platelet": (150000, 450000),
    "wbc": (4000, 11000),
    "crp": (0, 5),
}

def normalize_test_name(name):
    name = name.lower()
    if "hemoglobin" in name or "haemoglobin" in name:
        return "hemoglobin"
    if "platelet" in name:
        return "platelet"
    if "wbc" in name or "white blood" in name:
        return "wbc"
    if "crp" in name:
        return "crp"
    return None

def clean_numeric(val):
    if val is None:
        return None
    val = str(val)
    match = re.search(r"\d+\.?\d*", val)
    if not match:
        return None
    return float(match.group())

def classify(test_key, value):
    if test_key not in REFERENCE_RANGES or value is None:
        return "Unknown"
    low, high = REFERENCE_RANGES[test_key]
    if value < low:
        return "Low"
    if value > high:
        return "High"
    return "Normal"

def compute_severity_score(model1_df):
    score = 0
    for _, row in model1_df.iterrows():
        if row["status"] == "High":
            score += 2
        elif row["status"] == "Low":
            score += 1
    return score


def run_model1(parsed_df):
    """
    This IS Model 1
    """
    rows = []

    for _, row in parsed_df.iterrows():
        test_name = row["test_name"]
        raw_value = row["value"]

        test_key = normalize_test_name(test_name)
        value = clean_numeric(raw_value)
        status = classify(test_key, value)

        rows.append({
            "test_name": test_name,
            "value": value,
            "unit": row.get("unit"),
            "status": status
        })

    return pd.DataFrame(rows)
