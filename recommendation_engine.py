# recommendation_engine.py

def rule_based_recommendations(patterns):
    """
    Rule-based mapping from patterns → recommendations.
    Can be expanded easily.
    """
    recs = []

    for p in patterns:
        p_lower = p.lower()

        if "inflammation" in p_lower or "infectious" in p_lower:
            recs.append("Consider monitoring fever, hydration, and consult a clinician if symptoms persist.")

        elif "cardio" in p_lower or "lipid" in p_lower or "cholesterol" in p_lower:
            recs.append("Increase dietary fiber, reduce saturated fats, and maintain regular exercise.")

        elif "anemia" in p_lower or "hemoglobin" in p_lower:
            recs.append("Include iron-rich foods and check B12/folate levels if fatigue persists.")

        elif "renal" in p_lower or "creatinine" in p_lower:
            recs.append("Maintain hydration and monitor kidney function if abnormalities persist.")

        elif "liver" in p_lower or "hepatic" in p_lower:
            recs.append("Avoid alcohol and hepatotoxic substances, monitor SGPT/SGOT if elevated.")

        else:
            recs.append("Monitor symptoms and consult a healthcare professional if abnormalities persist.")

    return recs


def generate_recommendations(patterns):
    """
    Main recommendation generator for Milestone 3.
    Uses rule-based system first.
    """
    if not patterns or len(patterns) == 0:
        return ["No abnormal patterns detected — maintain healthy lifestyle."]

    return rule_based_recommendations(patterns)
