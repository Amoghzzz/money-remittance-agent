import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# =========================
# CONFIG
# =========================
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(
    page_title="Compliance Buddy",
    layout="wide"
)

# =========================
# SIDEBAR NAVIGATION
# =========================
st.sidebar.title("🏦 Compliance Buddy")

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Ask Compliance", "Journey Validator"]
)

# =========================
# COMMON SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
You are a senior banking compliance expert.

You help Indian bank product teams validate journeys against:
- RBI guidelines
- SEBI guidelines
- KYC/AML rules
- LRS rules
- onboarding compliance
- examples of what fintechs are doing

Always respond in this structure:
1. Verdict (Compliant / Risky / Non-Compliant)
2. Reason
3. RBI/Regulatory Logic
4. Suggested Fix
Be concise and precise.
"""

# =========================
# AI CALL FUNCTION
# =========================
def ask_ai(question):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=SYSTEM_PROMPT + "\n\nUser Query:\n" + question,
        config={
            "max_output_tokens": 100
        }
    )
    return response.text

# =========================
# DASHBOARD
# =========================
if page == "Dashboard":
    st.title("📊 Compliance Copilot Dashboard")

    st.markdown("""
    Welcome to **Compliance Copilot**, an AI assistant for banking teams.

    Use this tool to:
    - Validate onboarding journeys
    - Check RBI compliance rules
    - Reduce regulatory risk in product design
    """)

    st.info("Select a feature from the sidebar to begin.")

# =========================
# ASK COMPLIANCE MODE
# =========================
elif page == "Ask Compliance":
    st.title("💬 Ask Compliance Question")

    user_input = st.text_area("Enter your compliance question")

    if st.button("Check Compliance"):
        if user_input.strip():
            with st.spinner("Analyzing RBI guidelines..."):
                result = ask_ai(user_input)

            st.markdown("### 🧠 AI Compliance Output")
            st.write(result)

# =========================
# JOURNEY VALIDATOR MODE
# =========================
elif page == "Journey Validator":
    st.title("🧾 Journey Compliance Validator")

    journey_type = st.selectbox(
        "Select Journey Type",
        ["Onboarding", "Remittance", "Loan", "KYC Update"]
    )

    steps = st.text_area(
        "Enter journey steps (comma separated)",
        placeholder="OTP, Aadhaar verification, PAN check, Debit card verification"
    )

    if st.button("Validate Journey"):
        query = f"""
        Validate this banking journey:

        Type: {journey_type}
        Steps: {steps}

        Check if this follows RBI compliance rules.
        """

        with st.spinner("Evaluating journey..."):
            result = ask_ai(query)

        st.markdown("### 📋 Compliance Review")
        st.write(result)
