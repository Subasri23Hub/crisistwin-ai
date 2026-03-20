import streamlit as st
from utils.parser import extract_text_from_pdf, extract_text_from_txt
from utils.chunking import chunk_text
from utils.retrieval import retrieve_relevant_chunks
from utils.simulator import run_document_intelligence

# -----------------------------
# Page Styling
# -----------------------------
st.markdown("""
<style>
/* Main page background */
.main {
    background-color: #ffffff;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Paragraphs / labels / captions */
html, body, [class*="css"], label, p, div, span {
    color: #000000 !important;
}

/* Blue button */
.stButton > button {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.7rem 1rem !important;
    width: 100%;
}

.stButton > button:hover {
    background-color: #1d4ed8 !important;
    color: white !important;
}

.stButton > button:active {
    background-color: #1e40af !important;
    color: white !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #f8fbff;
    border: 1px solid #dbeafe;
    padding: 14px;
    border-radius: 12px;
}

/* Input box */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    color: #000000 !important;
}

/* Clean cards */
.custom-card {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 16px;
    box-shadow: 0 2px 10px rgba(37, 99, 235, 0.06);
}

/* Small blue section label */
.section-label {
    color: #2563eb !important;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

/* Success message polish */
[data-testid="stAlert"] {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.title("📄 Document Intelligence")
st.caption("Upload a document and receive a clean AI-generated analysis with summary, insights, risks, and recommendations.")

# -----------------------------
# Inputs
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"]
)

focus_area = st.text_input(
    "Optional focus area",
    placeholder="Example: compliance risks, audit readiness, cybersecurity exposure"
)

analyze_btn = st.button("Analyze Document")

# -----------------------------
# Processing
# -----------------------------
if analyze_btn:
    if not uploaded_file:
        st.warning("Please upload a document first.")
        st.stop()

    with st.spinner("Reading document..."):
        if uploaded_file.name.lower().endswith(".pdf"):
            full_text = extract_text_from_pdf(uploaded_file)
        else:
            full_text = extract_text_from_txt(uploaded_file)

    if not full_text or not full_text.strip():
        st.error("No readable text was found in the uploaded document.")
        st.stop()

    with st.spinner("Analyzing document..."):
        chunks = chunk_text(full_text)

        query = (
            focus_area.strip()
            if focus_area.strip()
            else "Summarize this document and identify key insights, risks, and recommendations"
        )

        top_chunks = retrieve_relevant_chunks(query, chunks, top_k=5)
        retrieved_context = "\n\n".join([chunk for chunk, _ in top_chunks])

        result = run_document_intelligence(
            document_text=retrieved_context,
            focus_area=focus_area.strip()
        )

    # -----------------------------
    # Output
    # -----------------------------
    st.success("Analysis completed successfully.")

    st.markdown(
        f"""
        <div class="custom-card">
            <div class="section-label">Document Summary</div>
            <div>{result.get("summary", "No summary available.")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        insights_html = "".join(
            [f"<li>{item}</li>" for item in result.get("insights", [])]
        ) or "<li>No insights identified.</li>"

        risks_html = "".join(
            [f"<li>{item}</li>" for item in result.get("risks", [])]
        ) or "<li>No risks identified.</li>"

        st.markdown(
            f"""
            <div class="custom-card">
                <div class="section-label">Key Insights</div>
                <ul>{insights_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="custom-card">
                <div class="section-label">Risks Identified</div>
                <ul>{risks_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        recommendations_html = "".join(
            [f"<li>{item}</li>" for item in result.get("recommendations", [])]
        ) or "<li>No recommendations available.</li>"

        st.markdown(
            f"""
            <div class="custom-card">
                <div class="section-label">Recommendations</div>
                <ul>{recommendations_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )