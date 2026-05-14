import streamlit as st
from google import genai
import time
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Compliance Copilot",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# ====================== ULTRA PREMIUM STYLING ======================
st.markdown("""
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
    }

    .glass-hover:hover {
        border-color: #00E0FF;
        box-shadow: 0 20px 50px rgba(0, 224, 255, 0.15);
        transform: translateY(-3px);
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
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0F111D;
        border-right: 1px solid #1E2A5E;
    }

    /* Buttons */
    .stButton button {
        border-radius: 16px;
        font-weight: 600;
        background: linear-gradient(90deg, #00C8FF, #4A9FFF);
        box-shadow: 0 0 25px rgba(0, 200, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 40px rgba(0, 200, 255, 0.5);
    }

    /* Input */
    textarea, input {
        border-radius: 16px !important;
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }

    /* Verdict Badges */
    .verdict-compliant { background: #0A3D1F; color: #4ADE80; padding: 4px 12px; border-radius: 30px; }
    .verdict-risky { background: #4C3F1F; color: #FACC15; padding: 4px 12px; border-radius: 30px; }
    .verdict-non { background: #4C2F2F; color: #F87171; padding: 4px 12px; border-radius: 30px; }

    .chip {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(100,180,255,0.3);
        border-radius: 30px;
        padding: 8px 16px;
        display: inline-block;
        margin: 4px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .chip:hover { background: rgba(0, 224, 255, 0.15); }
</style>
""", unsafe_allow_html=True)

# ====================== API CLIENT ======================
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    client = None

SYSTEM_PROMPT = """
You are Compliance Copilot — an expert RBI compliance AI used by leading Indian banks and fintechs.
Always respond in this exact format:

**Verdict**: Compliant / Risky / Non-Compliant
**Risk Score**: X/10
**Reason**: Clear explanation
**Regulatory Reference**: Specific RBI circulars / Master Directions
**Suggested Fix**: Actionable steps
"""

def ask_ai(query):
    if not client:
        return "AI client not initialized."
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT + "\n\nQuery: " + query,
            config={"temperature": 0.2, "max_output_tokens": 300}
        )
        return response.text
    except Exception as e:
        return f"Analysis failed. Please try again."

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("## 🛡️ Compliance Copilot")
    st.caption("RBI AI Intelligence Platform")

    selected = option_menu(
        None,
        ["Dashboard", "Ask Compliance", "Journey Validator", "RBI Circular Explorer", "Audit Logs"],
        icons=["house", "chat-dots-fill", "diagram-3", "book", "clock-history"],
        default_index=0,
        styles={
            "container": {"padding": "0"},
            "nav-link": {"font-size": "15.5px", "margin": "6px 0"},
            "nav-link-selected": {"background-color": "#1E40AF"}
        }
    )

    st.divider()
    st.success("● Live • RBI Knowledge Base 2026")

# ====================== RIGHT INSIGHT PANEL (Simulated) ======================
def show_right_panel(verdict="", risk=0, references=""):
    with st.expander("📊 AI Insight Panel", expanded=True):
        st.markdown("**Verdict**")
        if "Compliant" in verdict:
            st.markdown(f"<span class='verdict-compliant'>✅ {verdict}</span>", unsafe_allow_html=True)
        elif "Risky" in verdict:
            st.markdown(f"<span class='verdict-risky'>⚠️ {verdict}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='verdict-non'>❌ {verdict}</span>", unsafe_allow_html=True)

        st.progress(risk/10)
        st.caption(f"Risk Score: {risk}/10")

        if references:
            st.markdown("**Key References**")
            st.info(references)

# ====================== MAIN PAGES ======================
if selected == "Dashboard":
    st.markdown('<h1 class="hero-title">Welcome to Compliance Copilot</h1>', unsafe_allow_html=True)
    st.markdown("**Next-generation RBI compliance intelligence for Indian banks & fintechs**")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Compliance Health", "97.8%", "↑2.4%")
    with col2:
        st.metric("Journeys Validated", "1,284", "This month")
    with col3:
        st.metric("Active Risks", "9", "↓3")
    with col4:
        st.metric("Avg Response Time", "1.8s", "AI")

    st.divider()
    st.subheader("Quick Start")
    chips = ["Is Video KYC mandatory for savings accounts above ₹50k?", 
             "PAN-Aadhaar linking rules for remittances", 
             "Latest guidelines on Account Aggregator consent"]
    
    for chip in chips:
        if st.button(chip, key=chip, use_container_width=True):
            st.session_state.query = chip
            st.switch_page("Ask Compliance")  # Approximate

elif selected == "Ask Compliance":
    st.markdown('<h1 class="hero-title">Ask Compliance Copilot</h1>', unsafe_allow_html=True)

    # Example Prompts
    st.markdown("**Example Prompts**")
    examples = [
        "Is Aadhaar OTP mandatory in all onboarding flows?",
        "Can we use Video KYC for Tier-2 city customers?",
        "What are the latest Master Directions on Digital Lending?"
    ]
    cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        with cols[i]:
            if st.button(ex, use_container_width=True, key=f"ex_{i}"):
                st.session_state.query = ex

    query = st.text_area("Your compliance question", 
                        placeholder="Ask anything about RBI regulations...",
                        height=120, key="query_input")

    if st.button("Analyze", type="primary", use_container_width=True):
        with st.spinner("Consulting latest RBI guidelines..."):
            time.sleep(1.2)
            result = ask_ai(query or st.session_state.get("query", ""))

        col_main, col_side = st.columns([3, 1])
        with col_main:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_side:
            show_right_panel("Compliant", 3, "Master Direction on KYC 2024")

elif selected == "Journey Validator":
    st.markdown('<h1 class="hero-title">Journey Risk Engine</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        journey_type = st.selectbox("Journey Type", 
            ["Customer Onboarding", "Loan Disbursement", "Remittance", "KYC Refresh", "High Value Transaction"])
        risk_appetite = st.select_slider("Risk Appetite", ["Low", "Medium", "High"])

    with col2:
        steps = st.text_area("Journey Steps (one per line)", 
            height=280,
            placeholder="1. Mobile + OTP\n2. Aadhaar e-KYC\n3. Video Verification\n4. PAN + Bank Account")

    if st.button("Validate Complete Journey", type="primary", use_container_width=True):
        if steps:
            with st.spinner("Running multi-layer compliance analysis..."):
                time.sleep(1.5)
                result = ask_ai(f"Journey: {journey_type}\nRisk: {risk_appetite}\nSteps:\n{steps}")
            
            st.success("Analysis Complete")
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)

# Placeholder pages
elif selected == "RBI Circular Explorer":
    st.info("RBI Circular Explorer coming soon — Full searchable database with semantic search.")

elif selected == "Audit Logs":
    st.info("Audit Logs & Compliance History coming soon.")

st.caption("🛡️ Compliance Copilot • Enterprise RBI AI Platform")
