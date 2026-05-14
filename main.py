import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Compliance Copilot",
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
.stApp {
    background: linear-gradient(135deg, #0A0F1E, #1A1F3C);
    color: #E8EEF9;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Top bar */
header[data-testid="stHeader"] {
    background: rgba(20,25,45,0.9);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding: 0.8rem 2rem;
}
header[data-testid="stHeader"]::after {
    content: "🚀 Compliance Copilot | RBI Governance AI";
    color: #E8EEF9;
    font-weight: 600;
    font-size: 16px;
    text-shadow: 0 0 8px rgba(0,224,255,0.4);
}

/* Glass cards */
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

/* Neon buttons */
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
</style>
""", unsafe_allow_html=True)

# =========================
# ERROR SAFE AI FUNCTION
# =========================
SYSTEM_PROMPT = """<Improved prompt above>"""

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
        return f"⚠️ System Error: {str(e)}"

# =========================
# NAVIGATION
# =========================
with st.sidebar:
    selected = option_menu(
        "🚀 Compliance Copilot",
        ["Dashboard", "Ask Compliance", "Journey Validator", "RBI Circular Explorer"],
        icons=["house", "chat", "diagram-3", "book"],
        default_index=0
    )

# =========================
# DASHBOARD
# =========================
if selected == "Dashboard":
    st.title("📊 RBI Governance Dashboard")

    st.markdown("""
    <div class="glass">
    <b>Welcome to Compliance Copilot</b><br>
    Governance Health: <span style="color:#00E0FF">Stable</span><br>
    2 new RBI circulars detected in last 24h.
    </div>
    """, unsafe_allow_html=True)

    st.button("Review Changes")

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="glass">Compliance Health<br><b>97.8%</b></div>', unsafe_allow_html=True)
    col2.markdown('<div class="glass">Journeys Validated<br><b>1,284 (+12%)</b></div>', unsafe_allow_html=True)
    col3.markdown('<div class="glass">Active Risks<br><b>9</b></div>', unsafe_allow_html=True)
    col4.markdown('<div class="glass">AI Response Time<br><b>1.8s (p95)</b></div>', unsafe_allow_html=True)

# =========================
# ASK COMPLIANCE
# =========================
elif selected == "Ask Compliance":
    st.title("💬 Ask Compliance")

    user_input = st.text_area("Enter your compliance query", placeholder="e.g. Is Video KYC mandatory?")
    if st.button("Analyze"):
        with st.spinner("Consulting RBI Master Directions..."):
            result = ask_ai(user_input)
        st.markdown('<div class="glass">### 🧠 AI Compliance Output</div>', unsafe_allow_html=True)
        st.write(result)

# =========================
# JOURNEY VALIDATOR
# =========================
elif selected == "Journey Validator":
    st.title("🧾 Journey Risk Engine")

    journey_type = st.selectbox("Journey Type", ["Onboarding", "Remittance", "Loan", "KYC Update"])
    risk_appetite = st.radio("Risk Appetite", ["Conservative", "Balanced", "Aggressive"])
    steps = st.text_area("Journey Steps", placeholder="Mobile → OTP → Aadhaar → Video KYC")

    if st.button("Validate Compliance Flow"):
        query = f"Journey Type: {journey_type}\nRisk Appetite: {risk_appetite}\nSteps: {steps}"
        with st.spinner("Running compliance engine..."):
            result = ask_ai(query)
        st.markdown('<div class="glass">### 📋 Compliance Report</div>', unsafe_allow_html=True)
        st.write(result)

# =========================
# RBI CIRCULAR EXPLORER
# =========================
elif selected == "RBI Circular Explorer":
    st.title("📚 RBI Circular Explorer")
    st.markdown('<div class="glass">Search and explore RBI circulars & master directions</div>', unsafe_allow_html=True)
    search_query = st.text_input("Search regulations...", placeholder="e.g. Digital Lending Master Directions")
    if st.button("Search"):
        st.info("🔍 Regulatory search feature coming soon...")
