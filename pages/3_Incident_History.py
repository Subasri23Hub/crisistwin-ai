import json
import streamlit as st

from utils.simulator import load_history

st.set_page_config(page_title="Incident History", page_icon="🕘", layout="wide")


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

st.title("🕘 Incident History")
st.caption("Review past crisis simulations generated in the app.")

st.markdown(
    """
    <div class="soft-card">
        <h3 style="margin-bottom:0.25rem;">Saved analysis history</h3>
        <p style="margin-bottom:0;">
            Each generated crisis response is stored locally in the outputs folder so you can review previous scenarios.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

history = load_history()

top1, top2 = st.columns(2)
top1.metric("Saved Incidents", len(history))
top2.metric("Storage", "Local JSON")

if not history:
    st.info("No incident history found yet. Generate a crisis response from the simulator page first.")
else:
    for idx, item in enumerate(history, start=1):
        result = item.get("result", {})
        title = f"{idx}. {item.get('industry', '—')} • {result.get('crisis_type', 'Unknown')} • {item.get('timestamp', '')}"
        with st.expander(title):
            st.markdown("**Company**")
            st.write(item.get("company_name") or "Not provided")

            st.markdown("**Scenario**")
            st.write(item.get("scenario", ""))

            c1, c2, c3 = st.columns(3)
            c1.metric("Severity Hint", item.get("severity_hint", "—"))
            c2.metric("Final Severity", result.get("severity", "—"))
            c3.metric("Confidence", result.get("confidence", "—"))

            st.markdown("**Executive Summary**")
            st.write(result.get("executive_summary", ""))

            st.markdown("**Immediate Actions**")
            for action in result.get("immediate_actions", []):
                st.markdown(f"- {action}")

            st.download_button(
                label=f"Download incident {idx} JSON",
                data=json.dumps(item, indent=2, ensure_ascii=False),
                file_name=f"incident_{idx}.json",
                mime="application/json",
                key=f"download_incident_{idx}",
            )
