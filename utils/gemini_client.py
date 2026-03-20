import streamlit as st
from google import genai

GENERATION_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"


@st.cache_resource(show_spinner=False)
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing in .streamlit/secrets.toml")
    return genai.Client(api_key=api_key)
