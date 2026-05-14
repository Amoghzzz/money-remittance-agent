import streamlit as st
from google import genai
from streamlit_option_menu import option_menu

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Compliance Copilot",
    layout="wide",
    page_icon="🛡️"
)

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# =========================
# PREMIUM DARK UI THEME
# =========================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top left, #0B1220, #05070F);
    color: #E8EEF9;
}

/* glass card */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(120,160,255,0.15);
    border-radius: 16px;
    padding: 18px;
    backdrop-filter: blur(18px);
}

/* sidebar */
section[data-testid="stSidebar"] {
    background: #0A0F1C;
    border-right: 1px solid #1B2A4A;
}

/* buttons */
.stButton button {
    background: linear-gradient(90deg, #2F6BFF, #5EEAD4);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

/* inputs */
textarea {
    border-radius: 12px !important;
}

/* headings */
h1, h2, h3 {
    color: #E8EEF9 !important;
}

.small {
    font-size: 12px;
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (NO DASHBOARD)
# =========================
with st.sidebar:
    st.title("🛡️ Compliance Copilot")

    selected = option_menu(
        None,
        ["Ask Compliance", "Journey Validator", "RBI Explorer"],
        icons=["chat-dots", "diagram-3", "book"],
        default_index=0
    )

    st.markdown("---")
    st.caption("AI Governance Engine v2.0")

# =========================
# AI FUNCTION
# =========================
SYSTEM_PROMPT = """
You are an RBI compliance expert.

Return:
1. Verdict
2. Reason
3. RBI reference
4. Fix
Keep it structured and concise.
"""

def ask_ai(q):
    try:
        res = client.models.generate_content(
            model="models/gemini-1.5-flash-001",
            contents=SYSTEM_PROMPT + "\n\n" + q,
            config={"max_output_tokens": 350}
        )
        return res.text
    except Exception as e:
        return f"System Error: {str(e)}"

# =========================
# MAIN UI (INSPIRED BY YOUR IMAGE)
# =========================

st.title("AI Compliance Workspace")

col_main, col_right = st.columns([2.2, 1])

# =========================
# LEFT MAIN WORKSPACE
# =========================
with col_main:

    if selected == "Ask Compliance":

        st.markdown("### 💬 Ask Compliance Intelligence")

        query = st.text_area(
            " ",
            placeholder="Ask about RBI rules, onboarding flows, KYC, remittance compliance..."
        )

        if st.button("Analyze"):
            with st.spinner("Analyzing RBI regulations..."):
                result = ask_ai(query)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🧠 Compliance Output")
            st.write(result)
            st.markdown('</div>', unsafe_allow_html=True)

    elif selected == "Journey Validator":

        st.markdown("### 🧾 Journey Risk Engine")

        journey_type = st.selectbox(
            "Journey Type",
            ["Onboarding", "Remittance", "Loan", "KYC Update"]
        )

        steps = st.text_area(
            "Journey Steps",
            placeholder="OTP → Aadhaar → PAN → Video KYC"
        )

        if st.button("Validate Journey"):
            q = f"""
            Validate this journey:
            Type: {journey_type}
            Steps: {steps}
            """

            with st.spinner("Running compliance engine..."):
                result = ask_ai(q)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📋 Compliance Result")
            st.write(result)
            st.markdown('</div>', unsafe_allow_html=True)

    else:

        st.markdown("### 📚 RBI Explorer")
        st.info("Semantic RBI circular search coming soon (RAG layer).")

# =========================
# RIGHT PANEL (LIKE YOUR IMAGE)
# =========================
with col_right:

    st.markdown("### 🧠 AI Insights")

    st.markdown("""
    <div class="card">
    <b>Risk Score</b><br>
    3/10 (Low Risk)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <b>Active References</b><br><br>
    RBI/2023-24/104<br>
    KYC-MD-2016
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <b style='color:#ff6b6b'>Critical Insight</b><br>
    Missing geo-tagging in V-CIP flow may violate RBI Section 18.
    </div>
    """, unsafe_allow_html=True)
