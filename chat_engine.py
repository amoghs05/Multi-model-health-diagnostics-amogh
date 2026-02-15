import google.generativeai as genai
import os

# Configure API key
genai.configure(api_key=os.getenv("AIzaSyDpXQzI5IWJnQgJgE9U0dW1FEIOrGLt4vo"))

def run_chatbot(model1_df, summary_text, user_question):

    model = genai.GenerativeModel("models/gemini-2.5-flash")

    context = f"""
You are a medical AI assistant.
Do NOT diagnose.
Do NOT prescribe.
Explain lab results clearly.

Model 1 Results:
{model1_df.to_string()}

Clinical Summary:
{summary_text}

User Question:
{user_question}
"""

    response = model.generate_content(context)

    return response.text
