import streamlit as st
from google import genai
from streamlit_option_menu import option_menu
import time

st.set_page_config(
    page_title="Compliance Buddy • RBI AI Co-Pilot",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# API Init
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    client = None

# ====================== ULTRA PREMIUM STYLING ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

    .stApp {
        background: #0A0A0F;
        color: #F0F4FF;
    }

    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Glass Cards */
    .glass {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(100, 200, 255, 0.15);
        border-radius: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.4s ease;
    }
    .glass:hover {
        border-color: rgba(0, 224, 255, 0.4);
        box-shadow: 0 20px 50px rgba(0, 224, 255, 0.15);
        transform: translateY(-4px);
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.03em;
    }

    .hero-title {
        font-size: 3.2rem;
        background: linear-gradient(90deg, #00E0FF, #4A9FFF, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111118;
        border-right: 1px solid #1E2A5E;
    }
    .sidebar .stMarkdown h2 {
        color: #00E0FF;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #00C4FF, #4A9FFF);
        color: white;
        border-radius: 16px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 0 25px rgba(0, 196, 255, 0.4);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 40px rgba(0, 196, 255, 0.6);
    }

    /* Inputs */
    textarea, input {
        border-radius: 16px !important;
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }

    .metric-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("## 🛡️ Compliance Buddy")
    st.caption("RBI AI Compliance Co-Pilot")
    
    selected = option_menu(
        None,
        ["Dashboard", "Ask Copilot", "Journey Validator"],
        icons=["house", "robot", "map"],
        default_index=0,
        styles={
            "container": {"padding": "10px"},
            "nav-link": {"font-size": "15px", "margin": "8px 0"},
            "nav-link-selected": {"background-color": "#1E40AF"}
        }
    )

    st.divider()
    st.markdown("**Status**")
    st.success("● Connected to latest RBI guidelines")

# ====================== DASHBOARD ======================
if selected == "Dashboard":
    st.markdown('<h1 class="hero-title">Compliance Intelligence Platform</h1>', unsafe_allow_html=True)
    st.markdown("**Real-time RBI compliance guidance powered by Gemini**")

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="glass metric-card"><h2>98.7%</h2><p>Overall Compliance Health</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass metric-card"><h2>312</h2><p>Journeys Validated</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="glass metric-card"><h2>7</h2><p>Critical Risks Detected</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="glass metric-card"><h2>Live</h2><p>RBI Knowledge Base Updated</p></div>', unsafe_allow_html=True)

    st.divider()

    st.subheader("Quick Compliance Checks")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="glass">Is Video KYC mandatory for high-value onboarding?</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass">PAN-Aadhaar linking rules for remittances</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="glass">Latest Master Direction on Digital Lending</div>', unsafe_allow_html=True)

# ====================== ASK COPILOT ======================
elif selected == "Ask Copilot":
    st.markdown('<h1 class="hero-title">Ask Compliance Copilot</h1>', unsafe_allow_html=True)
    st.markdown("Instant, authoritative answers with regulatory references")

    question = st.text_area(
        "Ask any RBI / Banking compliance question",
        placeholder="Is Aadhaar Video KYC allowed for Tier-1 city customers opening savings accounts above ₹1 lakh?",
        height=140
    )

    if st.button("Get Compliance Analysis", use_container_width=True):
        if client and question.strip():
            with st.spinner("Analyzing latest RBI guidelines..."):
                time.sleep(1)
                # (Your ask_ai function here)
                result = "Your AI response will appear here..."
                st.markdown(f'<div class="glass">{result}</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter a question")

# ====================== JOURNEY VALIDATOR ======================
elif selected == "Journey Validator":
    st.markdown('<h1 class="hero-title">Journey Risk Engine</h1>', unsafe_allow_html=True)
    st.markdown("Validate complete customer journeys against RBI regulations")

    col_left, col_right = st.columns([1, 1.6])
    
    with col_left:
        journey = st.selectbox(
            "Journey Type",
            ["Customer Onboarding", "Loan Application", "Remittance", 
             "KYC Refresh", "High-Value Transaction", "Account Closure"]
        )
        risk = st.select_slider("Risk Appetite", ["Low", "Medium", "High"], value="Medium")

    with col_right:
        steps = st.text_area(
            "Journey Steps (one per line)",
            placeholder="1. Mobile number + OTP\n2. Aadhaar e-KYC\n3. Video verification\n4. PAN & Bank account linking",
            height=220
        )

    if st.button("Validate Full Journey", type="primary", use_container_width=True):
        if steps:
            with st.spinner("Running deep compliance analysis..."):
                time.sleep(1.5)
                query = f"Journey: {journey}\nRisk: {risk}\nSteps:\n{steps}"
                # result = ask_ai(query)
                st.success("✅ Analysis Complete")
                st.markdown('<div class="glass">Detailed compliance report will appear here</div>', unsafe_allow_html=True)
        else:
            st.warning("Please describe the journey steps")

st.caption("🛡️ Compliance Buddy v2.0 • Designed for precision, trust & clarity")
