import pandas as pd

def create_ground_truth_template(system_csv="system_output.csv", output_csv="ground_truth.csv"):
    sys_df = pd.read_csv(system_csv)

    gt_df = pd.DataFrame()
    gt_df["patient_id"] = sys_df["patient_id"]
    gt_df["test_name"] = sys_df["test_name"]
    gt_df["value_true"] = ""
    gt_df["status_true"] = ""
    gt_df["patterns_true"] = ""
    gt_df["risk_level_true"] = ""

    gt_df.to_csv(output_csv, index=False)
    print(f"📝 Ground truth template created: {output_csv}")

if __name__ == "__main__":
    create_ground_truth_template()
