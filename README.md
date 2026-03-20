# CrisisTwin — AI Crisis Decision Simulator

> An AI-powered decision support system designed to simulate, analyze, and respond to real-world business crises using advanced prompt engineering and Retrieval-Augmented Generation (RAG).

> Live Application : https://crisistwin-ai-seg5sosyr4my6j3ysj7pw3.streamlit.app/

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [AI Techniques Used](#ai-techniques-used)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Deployment](#deployment)
- [Use Cases](#use-cases)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

CrisisTwin generates structured, executive-level insights to support strategic decision-making during critical business situations. It combines role prompting, chain-of-thought reasoning, and RAG pipelines to deliver actionable crisis response plans.

---

## Key Features

### Crisis Simulator

- Input any business crisis scenario
- Generates a structured response plan covering:
  - Executive Summary
  - Crisis Type and Severity
  - Stakeholders Impacted
  - Risks Identified
  - Immediate Actions
  - 24h / 7d / 30d Action Plan
  - Communication Draft
  - Recovery Strategy

### Document Intelligence

- Upload PDFs or plain text files
- AI automatically extracts:
  - Summary
  - Key Insights
  - Risks
  - Recommendations

### RAG Pipeline

- Text chunking
- Embeddings generation
- Semantic similarity search
- Context-aware AI responses

### Incident History

- Stores all past simulations
- Enables tracking and review over time

---

## AI Techniques Used

- Role Prompting
- Chain-of-Thought Prompting (hidden reasoning)
- Step-by-Step Prompting
- Structured Output Prompting (JSON)
- Retrieval-Augmented Generation (RAG)
- Embeddings and Similarity Search

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| UI Framework | Streamlit |
| AI Model | Google Gemini API |
| Numerical Computing | NumPy |
| Data Processing | Pandas |
| ML Utilities | Scikit-learn |
| PDF Parsing | PyPDF2 |

---

## Project Structure

```
crisistwin/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── secrets.toml
├── pages/
│   ├── 1_Crisis_Simulator.py
│   ├── 2_Document_Intelligence.py
│   └── 3_Incident_History.py
├── utils/
│   ├── gemini_client.py
│   ├── prompt_builder.py
│   ├── schemas.py
│   ├── parser.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retrieval.py
│   └── simulator.py
├── data/
└── outputs/
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/crisistwin-ai.git
cd crisistwin-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create the file `.streamlit/secrets.toml` and add the following:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

### 4. Run the Application

```bash
streamlit run app.py
```

---

## Deployment

To deploy on Streamlit Cloud:

1. Push the project to a GitHub repository
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Select your repository
4. Add `GEMINI_API_KEY` under **Secrets**
5. Click **Deploy**

---

## Use Cases

- Business crisis management
- Risk analysis and compliance
- Audit preparation
- Strategic decision-making
- AI-powered consulting tools

---

## Future Improvements

- Real-time alerts integration
- Multi-agent simulation
- Dashboard analytics
- Voice-enabled interaction

---

## Author

**Subasri B**

---

> If you find this project useful, consider starring it on GitHub.
