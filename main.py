import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# =========================
# CONFIG
# =========================
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(
    page_title="Compliance Buddy",
    layout="wide",
    page_icon="🏦"
)

# =========================
# CUSTOM BACKGROUND STYLE
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0B1F3B 0%, #111827 50%, #0F172A 100%);
        color: white;
    }

    .block-container {
        padding-top: 2rem;
    }

    h1, h2, h3 {
        color: white !important;
    }

    /* Card style */
    .card {
        background-color: rgba(255,255,255,0.06);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }

    /* Button styling */
    .stButton button {
        background: #2F6BFF;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        border: none;
    }

    .stTextArea textarea {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# AI FUNCTION
# =========================
SYSTEM_PROMPT = """
You are a senior banking compliance expert.

Return response in:
1. Verdict
2. Reason
3. Regulatory Logic
4. Fix
"""

def ask_ai(question):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=SYSTEM_PROMPT + "\n\nUser:\n" + question,
        config={"max_output_tokens": 100}
    )
    return response.text

# =========================
# SIDEBAR MENU (MODERN)
# =========================
with st.sidebar:
    selected = option_menu(
        menu_title="🏦 Compliance Buddy",
        options=["Dashboard", "Ask Compliance", "Journey Validator"],
        icons=["house", "chat-dots", "diagram-3"],
        default_index=0,
    )

# =========================
# DASHBOARD
# =========================
if selected == "Dashboard":
    st.title("🏦 Compliance Intelligence Platform")

    st.markdown("""
    <div class="card">
    Welcome to <b>Compliance Copilot</b> — an AI system for validating banking journeys against RBI regulations.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">📊 Risk Analysis<br>Real-time compliance checks</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">📜 RBI Rules<br>Guideline-based reasoning</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">⚡ Fast Decisions<br>LLM-powered validation</div>', unsafe_allow_html=True)

# =========================
# ASK COMPLIANCE
# =========================
elif selected == "Ask Compliance":
    st.title("💬 Ask Compliance Question")

    user_input = st.text_area("Enter your question")

    if st.button("Analyze"):
        with st.spinner("Checking compliance rules..."):
            result = ask_ai(user_input)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🧠 Compliance Result")
        st.write(result)
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# JOURNEY VALIDATOR
# =========================
elif selected == "Journey Validator":
    st.title("🧾 Journey Validator")

    journey_type = st.selectbox(
        "Select Journey",
        ["Onboarding", "Remittance", "Loan", "KYC Update"]
    )

    steps = st.text_area("Enter journey steps")

    if st.button("Validate"):
        query = f"""
        Journey Type: {journey_type}
        Steps: {steps}
        """

        with st.spinner("Analyzing compliance risk..."):
            result = ask_ai(query)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📋 Compliance Report")
        st.write(result)
        st.markdown('</div>', unsafe_allow_html=True)
