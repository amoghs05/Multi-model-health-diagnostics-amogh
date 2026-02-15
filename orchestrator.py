# orchestrator.py

import uuid
from ocr import read_pdf_text
from parser import extract_structured
from standardize import run_model1
from llm_mistral_engine import run_mistral_llm
from report_generator import generate_pdf_report

class MultiModelOrchestrator:

    def __init__(self):
        pass

    def run_pipeline(self, pdf_path):
        """
        Complete end-to-end workflow.
        Returns patient_id, model1_df, llm_output, pdf_report_path
        """

        # 1. Generate patient ID
        patient_id = str(uuid.uuid4())[:8]

        # 2. OCR / Text extraction
        text = read_pdf_text(pdf_path)
        if not text or len(text.strip()) < 20:
            raise ValueError("OCR failed or text extraction insufficient")

        # 3. Parsing
        parsed_df = extract_structured(text)
        if parsed_df is None or parsed_df.empty:
            raise ValueError("No blood parameters parsed from report")

        # 4. Model-1 Classification
        model1_df = run_model1(parsed_df)
        if model1_df is None or model1_df.empty:
            raise ValueError("Model 1 classification failed")

        # 5. Model-2 & Model-3 (LLM)
        llm_output = run_mistral_llm(model1_df)

        # 6. Generate PDF Report
        report_path = f"reports/{patient_id}_report.pdf"
        generate_pdf_report(patient_id, model1_df, llm_output, report_path)

        return patient_id, model1_df, llm_output, report_path
    
        # Edge Case: Empty PDF
        if os.path.getsize(pdf_path) == 0:
            raise ValueError("Uploaded PDF is empty or corrupted")

        # Edge Case: No abnormal values
        if llm_output.get("risk_level") == "Low":
            print("Info: No significant abnormalities detected.")

