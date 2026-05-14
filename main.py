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

# ======================
# ULTRA PREMIUM STYLING
# ======================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

    .stApp {
        background: #0A0B12;
        color: #F0F4FF;
    }

    .main .block-container {
        padding-top: 1.5rem;
        max-width: 1400px;
    }

    /* Glassmorphism */
    .glass {
        background: rgba(20, 25, 45, 0.65);
        border: 1px solid rgba(100, 180, 255, 0.18);
        border-radius: 20px;
        backdrop-filter: blur(24px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.35);
        padding: 24px;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.025em;
    }

    .hero-title {
        font-size: 3.1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #60E0FF, #A0B8FF, #C8A8FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: #0F111D;
        border-right: 1px solid #1E2A5E;
    }

    /* Custom Metric styling */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
