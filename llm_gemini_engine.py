import google.generativeai as genai
import os

# Load API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_gemini_chat(report_df, llm_summary, user_question):
    """
    Context-aware Gemini chatbot for blood report Q&A
    """

    # Build context safely
    abnormal = report_df[report_df["status"].isin(["High", "Low"])]

    context = f"""
REPORT SUMMARY:
{llm_summary}

ABNORMAL PARAMETERS:
"""

    for _, row in abnormal.iterrows():
        context += f"- {row['test_name']}: {row['value']} ({row['status']})\n"

    prompt = f"""
You are a medical explanation assistant.

STRICT RULES:
- DO NOT diagnose diseases
- DO NOT prescribe medication
- DO NOT give treatment advice
- Explain values in simple terms
- Use cautious language ("may indicate", "can be associated with")
- Base answers ONLY on the provided report context

CONTEXT:
{context}

USER QUESTION:
{user_question}

Provide a short, safe explanation.
"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text.strip()
