from fpdf import FPDF
from datetime import datetime
import os

def generate_pdf_report(patient_id, model1_df, llm_output, output_path):

    # Ensure reports folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Health Diagnostics AI Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Patient ID: {patient_id}", ln=True)
    pdf.cell(0, 8, f"Generated Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Extracted Lab Parameters:", ln=True)
    pdf.set_font("Arial", size=10)

    for _, row in model1_df.iterrows():
        pdf.cell(0, 6, f"{row['test_name']}: {row['value']} ({row['status']})", ln=True)

    pdf.ln(3)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Detected Patterns:", ln=True)
    pdf.set_font("Arial", size=10)

    for p in llm_output.get("patterns", []):
        pdf.cell(0, 6, f"- {p['pattern']} (confidence={p['confidence']})", ln=True)

    pdf.ln(3)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Risk Assessment:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, f"Risk Level: {llm_output.get('risk_level')}", ln=True)
    pdf.cell(0, 6, f"Risk Score: {llm_output.get('risk_score')}", ln=True)
    pdf.multi_cell(0, 6, f"Summary: {llm_output.get('summary')}")
    pdf.ln(3)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Recommendations:", ln=True)
    pdf.set_font("Arial", size=10)
    for rec in llm_output.get("recommendations", []):
        pdf.multi_cell(0, 6, f"- {rec}")

    pdf.ln(2)
    pdf.set_font("Arial", "I", 8)
    pdf.multi_cell(0, 5,
        "Disclaimer: This AI-generated report is for informational purposes only and "
        "should not be used for diagnosis or treatment. Always consult qualified medical professionals."
    )

    pdf.output(output_path)
    return output_path
