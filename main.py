import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Compliance Buddy",
    layout="wide",
    page_icon="🏦"
)

# Safe API init (prevents crashes)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    client = None

# =========================
# FUTURISTIC UI STYLING
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #0B1F3B, #050A1A);
    color: #E8EEF9;
    font-family: 'Inter', sans-serif;
}

/* Glass card */
.glass {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 18px;
    border-radius: 16px;
    backdrop-filter: blur(14px);
    box-shadow: 0 4px 30px rgba(0,0,0,0.3);
}

/* Neon button feel */
.stButton button {
    background: linear-gradient(90deg, #2F6BFF, #6EE7FF);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    border: none;
    font-weight: 600;
    transition: 0.3s ease;
}

.stButton button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(47,107,255,0.5);
}

/* Inputs */
textarea, input {
    border-radius: 10px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(10,15,30,0.9);
}

/* Headings */
h1, h2, h3 {
    color: #E8EEF9 !important;
}

.small-text {
    font-size: 13px;
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)

# =========================
# ERROR SAFE AI FUNCTION
# =========================
SYSTEM_PROMPT = """
You are a senior RBI banking compliance expert.

Always respond in:
1. Verdict
2. Reason
3. Regulatory Reference
4. Suggested Fix

Be precise and avoid long explanations.
"""

def ask_ai(question):
    if client is None:
        return "⚠️ System error: AI client not initialized. Check API key."

    if not question or len(question.strip()) < 5:
        return "⚠️ Please enter a meaningful compliance question."

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=SYSTEM_PROMPT + "\n\nUser:\n" + question,
            config={"max_output_tokens": 350}
        )
        return response.text

    except Exception as e:
        return f"""
⚠️ System Error Occurred

Possible reasons:
- API rate limit exceeded
- Network issue
- Invalid request format

Technical detail:
{str(e)}
"""

# =========================
# NAVIGATION
# =========================
with st.sidebar:
    selected = option_menu(
        "🏦 Compliance Buddy",
        ["Dashboard", "Ask Compliance", "Journey Validator"],
        icons=["house", "chat", "diagram-3"],
        default_index=0
    )

# =========================
# DASHBOARD
# =========================
if selected == "Dashboard":
    st.title("🏦 Compliance Intelligence Platform")

    st.markdown("""
    <div class="glass">
    <b>Welcome to Compliance Copilot</b><br><br>
    A futuristic AI system designed to validate banking journeys against RBI compliance rules in real time.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.markdown('<div class="glass">⚡ Fast Analysis<br><span class="small-text">Instant compliance reasoning</span></div>', unsafe_allow_html=True)
    col2.markdown('<div class="glass">📜 RBI Knowledge<br><span class="small-text">Rule-based intelligence layer</span></div>', unsafe_allow_html=True)
    col3.markdown('<div class="glass">🛡 Risk Detection<br><span class="small-text">Detect non-compliant flows</span></div>', unsafe_allow_html=True)

# =========================
# ASK COMPLIANCE
# =========================
elif selected == "Ask Compliance":
    st.title("💬 Compliance Intelligence Assistant")

    st.markdown('<div class="glass">Ask any RBI / banking compliance question below</div>', unsafe_allow_html=True)

    user_input = st.text_area("Enter your question", placeholder="e.g. Is Aadhaar OTP mandatory for onboarding?")

    if st.button("Analyze Compliance"):
        with st.spinner("Analyzing RBI regulations..."):
            result = ask_ai(user_input)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 🧠 AI Compliance Output")
        st.write(result)
        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# JOURNEY VALIDATOR
# =========================
elif selected == "Journey Validator":
    st.title("🧾 Journey Risk Engine")

    st.markdown('<div class="glass">Validate your banking journey against regulatory rules</div>', unsafe_allow_html=True)

    journey_type = st.selectbox(
        "Journey Type",
        ["Onboarding", "Remittance", "Loan", "KYC Update"]
    )

    steps = st.text_area(
        "Journey Steps",
        placeholder="OTP → Aadhaar → PAN → Debit Card Verification"
    )

    if st.button("Run Compliance Check"):
        query = f"""
        Journey Type: {journey_type}
        Steps: {steps}
        """

        with st.spinner("Running compliance engine..."):
            result = ask_ai(query)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### 📋 Compliance Report")
        st.write(result)
        st.markdown('</div>', unsafe_allow_html=True)
