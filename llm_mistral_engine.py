# llm_mistral_engine.py

import subprocess
import json
import re
from rag_engine import load_rag_context
from standardize import compute_severity_score  # Ensure this exists
from recommendation_engine import generate_recommendations   # >>> ADDED FOR MILESTONE 3 <<<


# -------------------------------
# JSON Extraction Helper
# -------------------------------
def extract_json(text):
    if not text:
        return None

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


# -------------------------------
# LLM Reasoning (Model 2 & 3)
# -------------------------------
def run_mistral_llm(model1_df):
    """
    Model 2: Pattern Identification + Confidence
    Model 3: Risk Level + Risk Score + Summary
    Milestone 3: Personalized Lifestyle Recommendations
    """

    # -------------------------------
    # 1. Extract abnormal parameters
    # -------------------------------
    abnormalities = {}
    for _, row in model1_df.iterrows():
        status = row.get("status", "")
        if status in ["High", "Low"]:
            test = row.get("test_name", "")
            abnormalities[test] = status

    # If nothing abnormal → simple JSON output
    if not abnormalities:
        base = {
            "patterns": [{"pattern": "No significant abnormalities", "confidence": 1.0}],
            "risk_level": "Low",
            "risk_score": 0,
            "summary": "All evaluated parameters are within normal limits.",
        }
        # >>> ADDED FOR MILESTONE 3 <<<
        base["recommendations"] = ["Maintain routine health checkups and a balanced lifestyle."]
        return base

    # -------------------------------
    # 2. Compute severity score
    # -------------------------------
    severity_score = compute_severity_score(model1_df)

    # -------------------------------
    # 3. Load RAG Context
    # -------------------------------
    rag_context = load_rag_context()

    # -------------------------------
    # 4. One-shot Prompt
    # -------------------------------
    prompt = f"""
You are a medical reasoning assistant.

STRICT RULES:
- DO NOT diagnose diseases
- DO NOT recommend treatment or medications
- DO NOT mention drugs
- Use cautious language ("possible", "may suggest")
- Output ONLY valid JSON
- Start with {{ and end with }}

REFERENCE CONTEXT:
{rag_context}

EXAMPLE:
Input:
CRP: High
WBC: High
Severity Score: 4

Output:
{{
  "patterns": [
    {{"pattern": "Possible inflammatory or infectious process", "confidence": 0.85}}
  ],
  "risk_level": "Moderate",
  "risk_score": 60,
  "summary": "Elevated inflammatory markers may suggest an ongoing systemic process."
}}

PATIENT INPUT:
{json.dumps(abnormalities, indent=2)}
Severity Score: {severity_score}

RETURN STRICT JSON:
{{
  "patterns": [
    {{"pattern": "", "confidence": 0.0}}
  ],
  "risk_level": "",
  "risk_score": 0,
  "summary": ""
}}
"""

    # -------------------------------
    # 5. Run LLM (Ollama)
    # -------------------------------
    result = subprocess.run(
        ["ollama", "run", "mistral:7b-instruct"],
        input=prompt,
        text=True,
        capture_output=True
    )

    raw_output = result.stdout.strip()
    print("\nRAW LLM OUTPUT:\n", raw_output, "\n")

    # -------------------------------
    # 6. JSON Extraction
    # -------------------------------
    parsed_json = extract_json(raw_output)

    # -------------------------------
    # 7. Safety Fallbacks
    # -------------------------------
    if parsed_json is None:
        # fallback using severity only
        parsed_json = {
            "patterns": [{"pattern": "Abnormal parameters detected", "confidence": 0.5}],
            "risk_level": "Unknown",
            "risk_score": min(100, severity_score * 10),
            "summary": "LLM output could not be parsed properly."
        }

    # ensure patterns exist
    if "patterns" not in parsed_json or not parsed_json["patterns"]:
        parsed_json["patterns"] = [{"pattern": "Abnormal parameters detected", "confidence": 0.5}]

    # ensure confidence exists
    for pat in parsed_json["patterns"]:
        if "confidence" not in pat:
            pat["confidence"] = 0.5

    # ensure risk_score exists
    if "risk_score" not in parsed_json or not isinstance(parsed_json["risk_score"], (int, float)):
        parsed_json["risk_score"] = min(100, severity_score * 10)

    # ensure risk_level exists
    if not parsed_json.get("risk_level"):
        rs = parsed_json["risk_score"]
        if rs <= 20:
            parsed_json["risk_level"] = "Low"
        elif rs <= 60:
            parsed_json["risk_level"] = "Moderate"
        else:
            parsed_json["risk_level"] = "High"

    # -------------------------------
    # 8. Milestone 3 Recommendation Engine
    # -------------------------------
    patterns = [p["pattern"] for p in parsed_json.get("patterns", [])]
    recommendations = generate_recommendations(patterns)  # >>> ADDED FOR MILESTONE 3 <<<
    parsed_json["recommendations"] = recommendations      # >>> ADDED FOR MILESTONE 3 <<<

    return parsed_json
