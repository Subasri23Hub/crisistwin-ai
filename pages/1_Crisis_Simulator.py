import streamlit as st

from utils.chunking import chunk_text
from utils.parser import extract_text_from_file
from utils.retrieval import retrieve_relevant_chunks
from utils.simulator import (
    run_crisis_simulation,
    build_download_payload,
    save_to_history
)

st.set_page_config(page_title="Crisis Simulator", page_icon="🚨", layout="wide")

GLOBAL_CSS = """
<style>
:root {
    --primary: #0b5ed7;
    --primary-dark: #084298;
    --primary-soft: #eaf2ff;
    --border: #d7e6ff;
    --text: #000000;
    --card-bg: #ffffff;
}
html, body, [class*="css"] {
    color: var(--text) !important;
}
.stApp { background: #ffffff; }
.block-container { padding-top: 1.2rem; max-width: 1200px; }
h1, h2, h3, h4, h5, h6, p, label, div, span { color: #000000 !important; }
.card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 10px 24px rgba(11, 94, 215, 0.06);
    margin-bottom: 16px;
}
.soft-card {
    background: linear-gradient(135deg, #ffffff 0%, #f6faff 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 10px 24px rgba(11, 94, 215, 0.07);
    margin-bottom: 16px;
}
.stButton > button {
    background: var(--primary) !important;
    color: #ffffff !important;
    border: 1px solid var(--primary) !important;
    border-radius: 12px !important;
    padding: 0.72rem 1rem !important;
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
div[data-testid="stSidebar"] {
    background: #f8fbff;
    border-right: 1px solid var(--border);
}
div[data-testid="stSidebar"] * { color: #000000 !important; }
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-testid="stTextArea"] textarea,
div[data-testid="stFileUploader"] section {
    border-radius: 12px !important;
    border-color: #b8d1ff !important;
}
.stTextInput input, .stTextArea textarea { color: #000000 !important; }
div[data-testid="stMetricValue"] { color: var(--primary-dark) !important; }
div[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 600; }
div[data-testid="stExpander"] details {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    background: #ffffff !important;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.title("🚨 Crisis Simulator")
st.caption("Create an executive-ready response plan for a business crisis scenario.")

with st.sidebar:
    st.markdown("### Quick guide")
    st.markdown("1. Enter scenario details")
    st.markdown("2. Upload optional evidence")
    st.markdown("3. Generate response plan")

st.markdown(
    """
    <div class="soft-card">
        <h3 style="margin-bottom:0.25rem;">Professional decision support</h3>
        <p style="margin-bottom:0;">
            Enter a crisis scenario and receive a structured business response plan covering severity,
            stakeholders, risks, actions, communication, and recovery.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        company_name = st.text_input("Company Name", placeholder="Example: NovaBiologics")
        industry = st.selectbox(
            "Industry",
            [
                "Pharma",
                "Healthcare",
                "Technology",
                "Retail",
                "Banking",
                "Manufacturing",
                "Logistics",
                "FMCG",
                "Other",
            ],
        )
        scenario = st.text_area(
            "Crisis Description",
            height=230,
            placeholder="Example: A pharma company discovers data integrity issues in electronic batch records 48 hours before an FDA inspection.",
        )

    with right:
        severity_hint = st.selectbox(
            "Initial Severity Estimate",
            ["Low", "Medium", "High", "Critical"],
        )
        uploaded_files = st.file_uploader(
            "Optional Supporting Documents",
            type=["pdf", "txt", "csv"],
            accept_multiple_files=True,
            help="Upload SOPs, audit notes, policy documents, incident logs, or other supporting files.",
        )
        st.markdown(
            """
            <div class="card">
                <h4 style="margin-bottom:0.4rem;">What the output includes</h4>
                <p style="margin-bottom:0;">
                    Executive summary, crisis type, severity, stakeholders, risks, immediate actions,
                    24-hour / 7-day / 30-day plan, communication draft, and recovery strategy.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

if st.button("Generate Crisis Response"):
    if not scenario.strip():
        st.warning("Please enter a crisis description before generating a response.")
        st.stop()

    retrieved_context = ""
    evidence_preview = []

    try:
        if uploaded_files:
            all_text = []
            for file in uploaded_files:
                text = extract_text_from_file(file)
                if text.strip():
                    all_text.append(text)

            combined_text = "\n\n".join(all_text)
            chunks = chunk_text(combined_text, chunk_size=1000, overlap=150)

            if chunks:
                evidence_preview = retrieve_relevant_chunks(scenario, chunks, top_k=5)
                retrieved_context = "\n\n".join(
                    [f"Evidence {idx + 1} (similarity {score:.3f}): {chunk}" for idx, (chunk, score) in enumerate(evidence_preview)]
                )

        with st.spinner("Analyzing scenario and building response plan..."):
            result = run_crisis_simulation(
                company_name=company_name,
                industry=industry,
                scenario=scenario,
                severity_hint=severity_hint,
                retrieved_context=retrieved_context,
            )

            history_entry = {
                "company_name": company_name,
                "industry": industry,
                "scenario": scenario,
                "severity_hint": severity_hint,
                "result": result
            }
            save_to_history(history_entry)

        st.success("Crisis response plan generated successfully.")

        top1, top2, top3 = st.columns(3)
        top1.metric("Crisis Type", result.get("crisis_type", "—"))
        top2.metric("Severity", result.get("severity", "—"))
        top3.metric("Confidence", result.get("confidence", "—"))

        col1, col2 = st.columns([1.25, 0.75], gap="large")

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Executive Summary")
            st.write(result.get("executive_summary", "No summary generated."))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Immediate Actions")
            for item in result.get("immediate_actions", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Response Timeline")
            t1, t2, t3 = st.tabs(["24 Hours", "7 Days", "30 Days"])
            with t1:
                for item in result.get("response_24h", []):
                    st.markdown(f"- {item}")
            with t2:
                for item in result.get("response_7d", []):
                    st.markdown(f"- {item}")
            with t3:
                for item in result.get("response_30d", []):
                    st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Communication Draft")
            st.write(result.get("communication_draft", "No communication draft generated."))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Recovery Strategy")
            for item in result.get("recovery_strategy", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Stakeholders Impacted")
            for item in result.get("stakeholders", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Top Risks")
            for item in result.get("top_risks", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Evidence Used")
            if result.get("evidence_used"):
                for item in result.get("evidence_used", []):
                    st.markdown(f"- {item}")
            else:
                st.write("No supporting evidence was used.")
            st.markdown("</div>", unsafe_allow_html=True)

        payload = build_download_payload({
            "company_name": company_name,
            "industry": industry,
            "scenario": scenario,
            "severity_hint": severity_hint,
            "result": result,
        })

        st.download_button(
            "Download Result (JSON)",
            data=payload,
            file_name="crisistwin_result.json",
            mime="application/json",
        )

        if evidence_preview:
              st.subheader("Retrieved Supporting Context")

        for idx, (chunk, score) in enumerate(evidence_preview, start=1):

        # Convert similarity into label
            if score > 0.75:
               label = "🔵 High Relevance"
            elif score > 0.60:
               label = "🟡 Medium Relevance"
            else:
               label = "⚪ Low Relevance"

            with st.expander(f"Evidence chunk {idx} • {label} • similarity {score:.3f}"):

            # Split into readable bullet points
                 points = chunk.split(". ")

                 st.markdown('<div style="padding:10px;">', unsafe_allow_html=True)

                 for p in points:
                     if p.strip():
                          st.markdown(f"- {p.strip()}")

                 st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Something went wrong: {e}")