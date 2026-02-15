# evaluate_system.py

import pandas as pd
from sklearn.metrics import accuracy_score
from ast import literal_eval
import numpy as np


def create_ground_truth_template(system_csv="system_output.csv", output_csv="ground_truth.csv"):
    sys_df = pd.read_csv(system_csv)

    gt_df = pd.DataFrame()
    gt_df["patient_id"] = sys_df["patient_id"]
    gt_df["test_name"] = sys_df["test_name"]
    gt_df["value_true"] = sys_df.get("value_pred", "")
    gt_df["status_true"] = sys_df.get("status_pred", "")
    gt_df["patterns_true"] = sys_df.get("patterns", "")
    gt_df["risk_level_true"] = sys_df.get("risk_level", "")

    gt_df.to_csv(output_csv, index=False)
    print(f"📝 Ground truth template created: {output_csv}")


# ---------------------------------------------------------
# MODEL 1 - Value & Status Evaluation
# ---------------------------------------------------------
def evaluate_extraction(sys_df, gt_df):
    merged = sys_df.merge(gt_df, on=["patient_id", "test_name"], how="inner")

    merged["correct_value"] = (
        merged["value_pred"].astype(str) == merged["value_true"].astype(str)
    )
    merged["correct_status"] = (
        merged["status_pred"].astype(str) == merged["status_true"].astype(str)
    )

    value_accuracy = merged["correct_value"].mean()
    status_accuracy = merged["correct_status"].mean()

    return value_accuracy, status_accuracy


# ---------------------------------------------------------
# Jaccard Similarity Helper
# ---------------------------------------------------------
def jaccard_similarity(list1, list2):
    set1, set2 = set(list1), set(list2)
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0
    return float(len(set1 & set2)) / len(set1 | set2)


# ---------------------------------------------------------
# MODEL 2 - Pattern Evaluation
# ---------------------------------------------------------
def evaluate_patterns(sys_df, gt_df):
    merged = sys_df.merge(gt_df, on=["patient_id", "test_name"], how="inner")
    scores = []

    for _, row in merged.iterrows():
        sys_raw = row.get("patterns", "[]")
        gt_raw = row.get("patterns_true", "[]")

        # Convert to Python list safely
        def safe_parse(x):
            if pd.isna(x) or x == "" or x == "nan":
                return []
            try:
                return literal_eval(str(x))
            except:
                return []

        sys_patterns = safe_parse(sys_raw)
        gt_patterns = safe_parse(gt_raw)

        # Convert to lowercase strings for matching
        sys_patterns = [str(x).lower() for x in sys_patterns]
        gt_patterns = [str(x).lower() for x in gt_patterns]

        scores.append(jaccard_similarity(sys_patterns, gt_patterns))

    return float(np.mean(scores)) if scores else 0.0


# ---------------------------------------------------------
# MODEL 3 - Risk Level Evaluation
# ---------------------------------------------------------
def evaluate_risk(sys_df, gt_df):
    merged = sys_df.merge(gt_df, on=["patient_id", "test_name"], how="inner")

    if "risk_level" not in merged.columns or "risk_level_true" not in merged.columns:
        print("⚠️ Risk level fields missing, returning 0 accuracy.")
        return 0.0

    return accuracy_score(merged["risk_level_true"], merged["risk_level"])


# ---------------------------------------------------------
# RUN FULL EVALUATION PIPELINE
# ---------------------------------------------------------
def run_evaluation(system_csv, ground_truth_csv):
    sys_df = pd.read_csv(system_csv)
    gt_df = pd.read_csv(ground_truth_csv)

    print("=== MODEL 1 EVALUATION ===")
    val_acc, status_acc = evaluate_extraction(sys_df, gt_df)
    print(f"Value Extraction Accuracy: {val_acc:.2f}")
    print(f"Status Classification Accuracy: {status_acc:.2f}")

    print("\n=== MODEL 2 EVALUATION ===")
    pattern_score = evaluate_patterns(sys_df, gt_df)
    print(f"Pattern Similarity (Jaccard): {pattern_score:.2f}")

    print("\n=== MODEL 3 EVALUATION ===")
    risk_acc = evaluate_risk(sys_df, gt_df)
    print(f"Risk Level Accuracy: {risk_acc:.2f}")

    return {
        "value_accuracy": val_acc,
        "status_accuracy": status_acc,
        "pattern_similarity": pattern_score,
        "risk_accuracy": risk_acc
    }


if __name__ == "__main__":
    create_ground_truth_template()   # Generates template only once
    run_evaluation("system_output.csv", "ground_truth.csv")
