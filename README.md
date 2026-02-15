🩺 Multi-Model AI Agent for Automated Health Diagnostics

An end-to-end intelligent system that reads medical blood reports (PDF / Image), extracts parameters using OCR, interprets them using rule-based + LLM reasoning, evaluates health risk, generates a clinical summary, and allows users to interact with the report through an AI chatbot.

This project implements a multi-model architecture combining:

OCR (Computer Vision)

Rule-based Clinical Interpretation

LLM Reasoning (Mistral / Gemini)

Retrieval Augmented Generation (RAG)

Conversational Medical Assistant

Automated Report Generation

🚀 Project Objectives

The system automatically:

Reads uploaded medical reports

Extracts blood test parameters

Classifies values as High / Low / Normal

Identifies possible clinical patterns

Calculates patient risk level

Generates medical summary

Produces downloadable PDF report

Provides chatbot to answer patient questions

🧠 AI Architecture (Multi-Model Agent)
User Upload
     ↓
OCR Engine
(pdfplumber + Tesseract)
     ↓
Parser
(RegEx medical extraction)
     ↓
Model 1 → Parameter Interpretation
(Rule Based Medical Ranges)
     ↓
Model 2 → Pattern Detection
(LLM Reasoning + RAG)
     ↓
Model 3 → Risk Assessment & Summary
(LLM + Severity Score)
     ↓
Report Generator
(PDF + Recommendations)
     ↓
Medical Chatbot
(Context Aware AI Assistant)



📂 Project Structure

health_diagnostics/
│
├── app.py                     → Streamlit User Interface
├── ocr.py                     → PDF/Image text extraction
├── parser.py                  → Blood parameter extraction
├── standardize.py             → Model 1 classification logic
├── llm_mistral_engine.py      → Model 2 & 3 reasoning (Mistral)
├── rag_engine.py              → Medical knowledge retrieval
├── report_generator.py        → Final PDF report generator
├── chat_engine.py             → AI chatbot interaction
├── evaluate_system.py         → Accuracy evaluation
├── requirements.txt           → Dependencies
└── reports/                   → Generated reports



🧪 Implemented Models
🔹 Model 1 — Parameter Classification

Determines if values are:

High

Low

Normal

Based on clinical reference ranges.

Example:

| Test       | Value | Range | Status |
| ---------- | ----- | ----- | ------ |
| Hemoglobin | 9.2   | 13–17 | Low    |
| CRP        | 120   | <5    | High   |



Model 2 — Pattern Identification

LLM detects medical patterns from abnormal parameters.

Example Output:

Possible inflammatory process

Possible anemia pattern

Uses:

Mistral-7B-Instruct

One-shot prompting

RAG medical context


Model 3 — Risk Assessment

Computes:

Risk Level (Low / Moderate / High)

Risk Score (0–100)

Clinical Summary

AI Chatbot

Users can ask:

"Why is my CRP high?"
"Is low hemoglobin serious?"
"What does platelet count indicate?"

The chatbot answers using:

Extracted report data

LLM reasoning

Medical safety constraints

Report Generation

The system generates a downloadable medical report including:

Patient details

All parameters

Abnormal findings

Clinical patterns

Risk assessment

Recommendations

Medical disclaimer

⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/<your-username>/Multi-model-health-diagnostics-amogh.git
cd Multi-model-health-diagnostics-amogh


Create Virtual Environment

Windows:

python -m venv .venv
.venv\Scripts\activate


Mac/Linux:

python3 -m venv .venv
source .venv/bin/activate


Install Requirements
pip install -r requirements.txt

4️⃣ Install Tesseract OCR

Download:
https://github.com/UB-Mannheim/tesseract/wiki

After installing → add to PATH

Verify:

tesseract --version

5️⃣ Install Ollama (for Mistral)

Download:
https://ollama.com

Then run:

ollama pull mistral:7b-instruct

▶️ Run Application
streamlit run app.py


Open browser:

http://localhost:8501

📊 Evaluation Metrics

| Metric                  | Target                        |
| ----------------------- | ----------------------------- |
| Extraction Accuracy     | >95%                          |
| Classification Accuracy | >98%                          |
| Pattern Similarity      | High overlap                  |
| Risk Prediction         | Consistent clinical reasoning |


🧩 Technologies Used

Python

Streamlit

Pandas

Regex NLP

Tesseract OCR

pdfplumber

Mistral-7B-Instruct (Ollama)

Gemini API (Chatbot)

Retrieval Augmented Generation

FPDF

⚠️ Medical Disclaimer

This system does NOT diagnose diseases.
It provides informational interpretation only.

Always consult a licensed healthcare professional.

🔮 Future Improvements

Multi-page report understanding

Lab-specific format adaptation

More medical datasets

Deep learning extraction model

Hospital integration API

👨‍💻 Author

Amogh S
AI/ML Developer

📜 License

Educational / Research Use Only

