import streamlit as st
import tempfile
import pandas as pd
import uuid
import os
import re
from PyPDF2 import PdfReader

# ---- Project Imports ----
from ocr import read_pdf_text
from parser import extract_structured
from standardize import run_model1
from llm_mistral_engine import run_mistral_llm
from report_generator import generate_pdf_report
from chat_engine import run_chatbot


# =========================================================
# Extract Patient Info
# =========================================================
def extract_patient_info(text):
    name, age = "Not Given", "Not Given"

    name_match = re.search(r"(Patient Name|Name)\s*[:\-]\s*([A-Za-z ]+)", text, re.I)
    age_match = re.search(r"(Age)\s*[:\-]\s*(\d{1,3})", text, re.I)

    if name_match:
        name = name_match.group(2).strip()

    if age_match:
        age = age_match.group(2).strip()

    return name, age


# =========================================================
# Save system output
# =========================================================
def save_system_output(model1_df, llm_output, patient_id):
    df_out = model1_df.copy()
    df_out["patient_id"] = patient_id
    df_out["patterns"] = str(llm_output.get("patterns", []))
    df_out["risk_level"] = llm_output.get("risk_level", "")
    df_out["risk_score"] = llm_output.get("risk_score", "")
    df_out["summary"] = llm_output.get("summary", "")
    df_out.rename(columns={"value": "value_pred", "status": "status_pred"}, inplace=True)
    df_out.to_csv("system_output.csv", index=False)


# =========================================================
# Streamlit Config
# =========================================================
st.set_page_config(page_title="Health Diagnostics", layout="wide")
st.title("🩺 Health Diagnostics Blood Report Analysis")

uploaded_file = st.file_uploader("Upload Blood Report (PDF)", type=["pdf"])


# =========================================================
# MAIN PIPELINE
# =========================================================
if uploaded_file is not None:

    # ---- Save PDF ----
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        temp_path = tmp.name

    st.success("PDF uploaded successfully")

    # ---- Page Count ----
    try:
        reader = PdfReader(temp_path)
        page_count = len(reader.pages)
    except:
        page_count = "Unknown"

    st.markdown("## 📄 Uploaded Report Details")
    st.info(f"""
    **File Type:** PDF  
    **Pages Uploaded:** {page_count}
    """)

    # ---- OCR ----
    with st.spinner("Extracting text..."):
        pdf_text = read_pdf_text(temp_path)

    if not pdf_text or len(pdf_text.strip()) < 20:
        st.error("Failed to extract text from PDF.")
        st.stop()

    # ---- Patient Info ----
    patient_name, patient_age = extract_patient_info(pdf_text)

    st.markdown("## 🧑 Patient Information")
    col1, col2 = st.columns(2)
    col1.metric("Patient Name", patient_name)
    col2.metric("Age", patient_age)

    # ---- Parsing ----
    with st.spinner("Parsing blood report values..."):
        parsed_df = extract_structured(pdf_text)

    if parsed_df is None or parsed_df.empty:
        st.error("No blood parameters found.")
        st.stop()

    # ---- Model 1 ----
    with st.spinner("Running Model 1..."):
        final_df = run_model1(parsed_df)

    if final_df is None or final_df.empty:
        st.error("Model 1 failed.")
        st.stop()

    # ---- Model 2 & 3 ----
    with st.spinner("Running AI reasoning..."):
        llm_output = run_mistral_llm(final_df)

    patient_id = str(uuid.uuid4())[:8]
    save_system_output(final_df, llm_output, patient_id)

    # =========================================================
    # MODEL RESULTS DISPLAY
    # =========================================================
    st.markdown("---")
    st.header("📊 Model Results")

    # -------- MODEL 1 --------
    st.subheader("🔹 Model 1 — Parameter Classification")
    st.dataframe(final_df, use_container_width=True)

    # -------- MODEL 2 --------
    st.subheader("🔹 Model 2 — Clinical Pattern Identification")
    patterns = llm_output.get("patterns", [])

    if patterns:
        for p in patterns:
            if isinstance(p, dict):
                st.success(f"{p.get('pattern')} (confidence: {p.get('confidence', 0)})")
            else:
                st.success(p)
    else:
        st.warning("No patterns detected.")

    # -------- MODEL 3 --------
    st.subheader("🔹 Model 3 — Patient Risk Assessment")
    col1, col2 = st.columns(2)
    col1.metric("Risk Level", llm_output.get("risk_level", "Unknown"))
    col2.metric("Risk Score", llm_output.get("risk_score", "N/A"))

    st.write("### Summary")
    st.info(llm_output.get("summary", "No summary available."))

    # =========================================================
    # ASK AI SECTION
    # =========================================================

       # =========================================================
    # ASK AI SECTION
    # =========================================================
    st.markdown("---")
    st.header("💬 Ask AI About Your Report")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat input box (Enter to submit)
    user_question = st.chat_input("Type your question and press Enter")

    if user_question:
        with st.spinner("AI is thinking..."):
            try:
                answer = run_chatbot(
                    final_df,
                    llm_output.get("summary", ""),
                    user_question
                )
            except Exception as e:
                answer = f"Chatbot error: {str(e)}"

        st.session_state.chat_history.append({
            "user": user_question,
            "assistant": answer
        })

    # Display chat conversation
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["user"])

        with st.chat_message("assistant"):
            st.write(chat["assistant"])

    # =========================================================
    # DISCLAIMER
    # =========================================================
    st.markdown("""
    ---
    ### ⚕️ Medical Disclaimer
    This AI-generated output is for informational purposes only.
    It does not replace professional medical advice.
    Always consult a qualified healthcare provider.
    """)
