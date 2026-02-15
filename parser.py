# parser_engine.py
import re
import pandas as pd

# BLOOD REPORT KEYWORDS
BLOOD_KEYS = [
    "hemoglobin", "haemoglobin", "hb",
    "rbc", "wbc", "platelet", "plt",
    "mcv", "mch", "mchc", "rdw",
    "mpv", "pdw", "p-lcr",
    "hematocrit", "pcv",
    "neutrophils", "lymphocytes",
    "eosinophils", "monocytes", "basophils",
    "esr", "crp", "c-reactive protein",
    "platelet indices"
]


def clean_text(text):
    text = text.replace("\x0c", "")
    text = re.sub(r"[|•·]+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def extract_patient_name(text):
    patterns = [
        r"Patient Name[:\- ]+([A-Za-z ]+)",
        r"Name[:\- ]+([A-Za-z ]+)",
        r"PATIENT[:\- ]+([A-Za-z ]+)"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return re.sub(r"[^A-Za-z ]", "", m.group(1).strip())
    return "No patient name"


def parse_blood_tests(text):
    pattern = re.compile(
        r"""
        (?P<name>[A-Za-z0-9()\- +./%]+?)   
        \s*[:\- ]\s*
        (?P<value>\d+\.?\d*)               
        \s*
        (?P<flag>\[[A-Za-z]\])?            
        \s*
        (?P<unit>[A-Za-z/%0-9\^\.\-µ]+)?    
        \s*
        (?P<range>\d+\.?\d*\s*[-–]\s*\d+\.?\d*)?
        """,
        re.VERBOSE | re.IGNORECASE
    )

    rows = []
    for m in pattern.finditer(text):
        name = m.group("name").lower()

        if not any(k in name for k in BLOOD_KEYS):
            continue

        rng = m.group("range")
        ref_low, ref_high = None, None
        if rng and "-" in rng:
            parts = re.split(r"[-–]", rng)
            if len(parts) == 2:
                ref_low, ref_high = parts[0].strip(), parts[1].strip()

        rows.append({
            "test_name": m.group("name"),
            "value": m.group("value"),
            "unit": m.group("unit"),
            "flag": m.group("flag"),
            "ref_low": ref_low,
            "ref_high": ref_high
        })

    return rows


def extract_structured(pdf_text):
    text = clean_text(pdf_text)

    patient = extract_patient_name(text)
    tests = parse_blood_tests(text)

    if not tests:
        return pd.DataFrame({"patient_name": [patient], "message": ["No blood values found"]})

    df = pd.DataFrame(tests)
    df.insert(0, "patient_name", patient)

    return df
