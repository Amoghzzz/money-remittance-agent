import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def ask_agent(question):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=question,
	config={"max_output_tokens":100}
    )
    return response.text


st.title("💬 Remittance Rejection Agent")

user_input = st.text_input("Hello there! How can I help you today")

SYSTEM_PROMPT = """
You are a senior banking compliance assistant for international remittances.

Your job:
- Identify rejection reasons
- Map to RBI/LRS/compliance rules
- Give short, precise and brief answers
- Always suggest next action

Keep responses under 8 lines.
"""

contents = SYSTEM_PROMPT + "\n\nUser: " + user_input

if user_input:
    result = ask_agent(contents)
    st.write(result)
