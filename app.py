import streamlit as st

st.set_page_config(
    page_title="CrisisTwin",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

GLOBAL_CSS = """
<style>
:root {
    --primary: #0b5ed7;
    --primary-dark: #084298;
    --primary-soft: #eaf2ff;
    --border: #d7e6ff;
    --text: #000000;
    --muted: #23395d;
    --card-bg: #ffffff;
    --page-bg: #ffffff;
}
html, body, [class*="css"] {
    color: var(--text) !important;
}
.stApp {
    background: var(--page-bg);
}
.block-container {
    padding-top: 1.6rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}
h1, h2, h3, h4, h5, h6, p, label, div, span {
    color: var(--text) !important;
}
.hero-card {
    background: linear-gradient(135deg, #ffffff 0%, #f6faff 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 26px 28px;
    box-shadow: 0 10px 28px rgba(11, 94, 215, 0.08);
}
.section-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 10px 24px rgba(11, 94, 215, 0.06);
    margin-bottom: 16px;
}
.kpi-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 5px solid var(--primary);
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 10px 20px rgba(11, 94, 215, 0.06);
}
.badge {
    display: inline-block;
    background: var(--primary-soft);
    color: var(--primary-dark) !important;
    border: 1px solid var(--border);
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.88rem;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 8px;
}
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1rem 0 1.2rem;
}
div[data-testid="stSidebar"] {
    background: #f8fbff;
    border-right: 1px solid var(--border);
}
div[data-testid="stSidebar"] * {
    color: #000000 !important;
}
div[data-testid="stMetricValue"] {
    color: var(--primary-dark) !important;
}
div[data-testid="stMetricLabel"] {
    color: #334155 !important;
    font-weight: 600;
}
.stButton > button {
    background: var(--primary) !important;
    color: #ffffff !important;
    border: 1px solid var(--primary) !important;
    border-radius: 12px !important;
    padding: 0.7rem 1rem !important;
    font-weight: 700 !important;
    width: 100%;
    box-shadow: 0 8px 18px rgba(11, 94, 215, 0.18);
}
.stButton > button:hover {
    background: var(--primary-dark) !important;
    border-color: var(--primary-dark) !important;
}
.stDownloadButton > button {
    background: #ffffff !important;
    color: var(--primary-dark) !important;
    border: 1px solid var(--primary) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-testid="stTextArea"] textarea,
div[data-testid="stFileUploader"] section {
    border-radius: 12px !important;
    border-color: #b8d1ff !important;
}
.stTextInput input, .stTextArea textarea {
    color: #000000 !important;
}
.stAlert {
    border-radius: 14px !important;
}
div[data-testid="stExpander"] details {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    background: #ffffff !important;
}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## CrisisTwin")
    st.markdown("AI Decision Simulator for Business Crisis Management")
    st.markdown("---")
    st.markdown("### Navigation")
    st.markdown("- Home")
    st.markdown("- Crisis Simulator")
    st.markdown("- Document Intelligence")
    st.markdown("- Incident History")
    st.markdown("---")
    st.info("Professional, evidence-aware crisis planning powered by Gemini.")

st.markdown(
    """
    <div class="hero-card">
        <h1 style="margin-bottom:0.4rem;">🚨 CrisisTwin</h1>
        <p style="font-size:1.05rem; margin-bottom:1rem;">
            A professional AI decision simulator that turns a business crisis scenario into an executive-ready response plan.
        </p>
        <span class="badge">Executive Summary</span>
        <span class="badge">Risk Assessment</span>
        <span class="badge">Stakeholder Mapping</span>
        <span class="badge">Response Plan</span>
        <span class="badge">Communication Draft</span>
        <span class="badge">Document Grounding</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="kpi-card">
            <h3 style="margin-bottom:0.25rem;">1. Enter the scenario</h3>
            <p>Describe the crisis, choose the industry, and give an initial severity estimate.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="kpi-card">
            <h3 style="margin-bottom:0.25rem;">2. Add supporting files</h3>
            <p>Optionally upload SOPs, policies, incident notes, or reports for grounded analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="kpi-card">
            <h3 style="margin-bottom:0.25rem;">3. Get a response plan</h3>
            <p>Receive a clean executive output covering risks, actions, communication, and recovery.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### What the app produces")
left, right = st.columns([1.25, 1])
with left:
    st.markdown(
        """
        <div class="section-card">
            <h4>Core output</h4>
            <p>
                CrisisTwin returns an executive summary, crisis classification, severity, impacted stakeholders,
                top risks, immediate actions, 24-hour / 7-day / 30-day response plans, a communication draft,
                and a recovery strategy.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        """
        <div class="section-card">
            <h4>Behind the scenes</h4>
            <p>
                The backend uses advanced prompting and optional semantic retrieval from uploaded files,
                while the user sees only a polished decision dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Suggested scenarios")
examples = [
    "A pharma company discovers data integrity issues in batch records 48 hours before an FDA inspection.",
    "A technology company suffers a ransomware attack that halts customer-facing services.",
    "A food manufacturer identifies possible contamination in a distributed product lot.",
    "A retail brand faces viral backlash after an employee misconduct incident.",
]
for example in examples:
    st.markdown(
        f"""
        <div class="section-card" style="padding:14px 18px;">
            <p style="margin:0;"><strong>Example:</strong> {example}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.success("Open the Crisis Simulator page from the sidebar to start.")
