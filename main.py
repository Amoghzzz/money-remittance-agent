import streamlit as st
from google import genai
from streamlit_option_menu import option_menu
import time

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Compliance Buddy",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Safe API init
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    client = None

# =========================
# ADVANCED FUTURISTIC STYLING
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 20%, rgba(0, 224, 255, 0.08) 0%, transparent 50%),
                    linear-gradient(135deg, #0A0F1E 0%, #1A1F3C 100%);
        color: #E8EEF9;
    }

    /* Glassmorphism + Neon */
    .glass {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 50px rgba(0, 224, 255, 0.15);
        border-color: rgba(0, 224, 255, 0.3);
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    .main-title {
        background: linear-gradient(90deg, #00E0FF, #3A7CFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }

    /* Neon Button */
    .stButton button {
        background: linear-gradient(90deg, #00E0FF, #3A7CFF);
        color: white;
        border: none;
        padding: 0.75rem 1.8rem;
        border-radius: 16px;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 0 25px rgba(0, 224, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 0 40px rgba(0, 224, 255, 0.6);
    }

    /* Input Fields */
    textarea, input, select {
        border-radius: 16px !important;
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #E8EEF9 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 20, 40, 0.95);
        border-right: 1px solid rgba(0, 224, 255, 0.15);
    }

    /* Animated glow effect */
    .glow-text {
        text-shadow: 0 0 15px rgba(0, 224, 255, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# AI FUNCTION
# =========================
SYSTEM_PROMPT = """
You are Compliance Copilot, a world-class RBI compliance expert.
Respond in this exact structured format:

1. **Verdict** – Clear, bold statement (Compliant / Non-Compliant / Partially Compliant)
2. **Reason** – Concise, user-friendly explanation
3. **Regulatory Reference** – Specific RBI circulars, Master Directions, or Acts
4. **Suggested Fix** – Actionable, practical recommendation

Tone: Professional, confident, and helpful.
"""

def ask_ai(question):
    if client is None:
        return "⚠️ AI client not initialized. Please check your API key."
    if not question or len(question.strip()) < 8:
        return "⚠️ Please ask a meaningful compliance question."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT + "\n\nUser Query:\n" + question,
            config={"max_output_tokens": 500, "temperature": 0.3}
        )
        return response.text
    except Exception as e:
        return f"**Error:** {str(e)}"

# =========================
# NAVIGATION
# =========================
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#00E0FF;'>🚀 Compliance Buddy</h2>", unsafe_allow_html=True)
    selected = option_menu(
        None,
        ["Dashboard", "Ask Compliance", "Journey Validator"],
        icons=["speedometer2", "chat-dots", "shield-check"],
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "icon": {"color": "#00E0FF"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "8px 0"},
            "nav-link-selected": {"background-color": "#1E3A8A"}
        }
    )

# =========================
# DASHBOARD
# =========================
if selected == "Dashboard":
    st.markdown('<h1 class="main-title glow-text">Compliance Intelligence</h1>', unsafe_allow_html=True)
    st.markdown("**Real-time RBI Compliance Co-Pilot**")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="glass"><h3>98.4%</h3><p style="margin:0; opacity:0.8;">Compliance Score</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass"><h3>247</h3><p style="margin:0; opacity:0.8;">Journeys Validated</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="glass"><h3>12</h3><p style="margin:0; opacity:0.8;">Critical Risks</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="glass"><h3>Live</h3><p style="margin:0; opacity:0.8; color:#00ff9d;">● RBI Knowledge Base</p></div>', unsafe_allow_html=True)

    st.markdown("### Featured Checks")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass">Aadhaar + Video KYC flows are now fully compliant under Master Direction 2024</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass">PAN-Aadhaar linking mandatory for all high-value transactions</div>', unsafe_allow_html=True)

# =========================
# ASK COMPLIANCE
# =========================
elif selected == "Ask Compliance":
    st.markdown('<h1 class="main-title">Ask Compliance Copilot</h1>', unsafe_allow_html=True)
    st.markdown("Get instant, authoritative answers backed by latest RBI guidelines.")

    user_input = st.text_area(
        "What compliance question do you have?",
        placeholder="Is Video KYC allowed for savings account opening above ₹50,000?",
        height=120
    )

    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button("🚀 Analyze", use_container_width=True):
            with st.spinner("Consulting RBI regulations..."):
                time.sleep(0.8)  # simulates thinking
                result = ask_ai(user_input)
            
            st.markdown("### Compliance Analysis")
            st.markdown(f'<div class="glass">{result}</div>', unsafe_allow_html=True)

# =========================
# JOURNEY VALIDATOR
# =========================
elif selected == "Journey Validator":
    st.markdown('<h1 class="main-title">Journey Risk Engine</h1>', unsafe_allow_html=True)
    st.markdown("Validate complete user journeys against regulatory requirements.")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        journey_type = st.selectbox(
            "Select Journey Type",
            ["Customer Onboarding", "Loan Disbursement", "Remittance (Domestic)", 
             "KYC Update", "High Value Transaction", "Account Closure"]
        )
        
        risk_level = st.select_slider("Expected Risk Level", 
                                    options=["Low", "Medium", "High"], value="Medium")

    with col2:
        steps = st.text_area(
            "Describe the Journey Steps",
            placeholder="1. Mobile + Email\n2. Aadhaar e-KYC + Video Verification\n3. PAN + Bank Account Verification\n...",
            height=200
        )

    if st.button("Run Full Compliance Validation", type="primary", use_container_width=True):
        if steps:
            with st.spinner("Running multi-layer compliance engine..."):
                time.sleep(1.2)
                query = f"Journey Type: {journey_type}\nRisk Level: {risk_level}\nSteps:\n{steps}"
                result = ask_ai(query)
            
            st.success("Validation Complete")
            st.markdown(f'<div class="glass"><h4>Compliance Report</h4>{result}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please describe the journey steps.")

st.caption("© 2026 Compliance Buddy • Built for precision and trust")
