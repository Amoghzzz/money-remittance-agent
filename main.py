import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Compliance Buddy",
    layout="wide",
    page_icon="🚀"
)

# Safe API init
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
    background: linear-gradient(135deg, #0A0F1E, #1A1F3C);
    color: #E8EEF9;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Glass card */
.glass {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(16px);
    box-shadow: 0 6px 40px rgba(0,0,0,0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.glass:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 50px rgba(0,0,0,0.6);
}

/* Neon button */
.stButton button {
    background: linear-gradient(90deg, #3A7CFF, #00E0FF);
    color: white;
    border-radius: 12px;
    padding: 0.7rem 1.2rem;
    border: none;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: 0.3s ease;
}
.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0,224,255,0.7);
}

/* Inputs */
textarea, input, select {
    border-radius: 12px !important;
    background: rgba(255,255,255,0.05) !important;
    color: #E8EEF9 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15,20,40,0.95);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Headings */
h1, h2, h3 {
    color: #E8EEF9 !important;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(0,224,255,0.4);
}

/* Small text */
.small-text {
    font-size: 13px;
    opacity: 0.75;
    letter-spacing: 0.3px;
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
        "🚀 Compliance Buddy",
        ["Dashboard", "Ask Compliance", "Journey Validator"],
        icons=["house", "chat", "diagram-3"],
        default_index=0
    )

# =========================
# DASHBOARD
# =========================
if selected == "Dashboard":
    st.title("🚀 Compliance Intelligence Platform")

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
