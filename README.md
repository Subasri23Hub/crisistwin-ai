# CrisisTwin

CrisisTwin is a Streamlit app that simulates business crisis response plans using Gemini.

## Features
- Professional blue-and-white Streamlit UI
- Crisis analysis with hidden advanced prompting
- Structured executive output
- Optional document upload for grounding
- Gemini embeddings for semantic retrieval
- Incident history tracking

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Secrets
Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_key_here"
```
