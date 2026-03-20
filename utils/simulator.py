import json
import os
import re
from utils.gemini_client import get_client
from utils.prompt_builder import (
    build_crisis_prompt,
    build_document_intelligence_prompt
)

# -----------------------------
# Crisis Simulation
# -----------------------------
def run_crisis_simulation(
    company_name: str,
    industry: str,
    scenario: str,
    severity_hint: str,
    retrieved_context: str = ""
):
    client = get_client()

    prompt = build_crisis_prompt(
        company_name=company_name,
        industry=industry,
        scenario=scenario,
        severity_hint=severity_hint,
        retrieved_context=retrieved_context
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw_text = response.text.strip()

    # 🔥 Fix: remove ```json formatting
    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    # 🔥 Safe JSON extraction
    try:
        parsed = json.loads(raw_text)
    except Exception:
        json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
        else:
            parsed = {
                "executive_summary": raw_text,
                "crisis_type": "Unknown",
                "severity": severity_hint if severity_hint else "Unknown",
                "stakeholders": [],
                "top_risks": [],
                "immediate_actions": [],
                "response_24h": [],
                "response_7d": [],
                "response_30d": [],
                "communication_draft": "",
                "recovery_strategy": [],
                "confidence": "Low - Invalid JSON response"
            }

    return {
        "executive_summary": parsed.get("executive_summary", ""),
        "crisis_type": parsed.get("crisis_type", ""),
        "severity": parsed.get("severity", ""),
        "stakeholders": parsed.get("stakeholders", []),
        "top_risks": parsed.get("top_risks", []),
        "immediate_actions": parsed.get("immediate_actions", []),
        "response_24h": parsed.get("response_24h", []),
        "response_7d": parsed.get("response_7d", []),
        "response_30d": parsed.get("response_30d", []),
        "communication_draft": parsed.get("communication_draft", ""),
        "recovery_strategy": parsed.get("recovery_strategy", []),
        "confidence": parsed.get("confidence", "")
    }


# -----------------------------
# Document Intelligence
# -----------------------------
def run_document_intelligence(document_text: str, focus_area: str = ""):
    client = get_client()

    prompt = build_document_intelligence_prompt(
        document_text=document_text,
        focus_area=focus_area
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw_text = response.text.strip()

    # 🔥 Fix: remove ```json formatting
    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    # 🔥 Safe JSON extraction
    try:
        parsed = json.loads(raw_text)
    except Exception:
        json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
        else:
            parsed = {
                "summary": raw_text,
                "insights": [],
                "risks": [],
                "recommendations": []
            }

    return {
        "summary": parsed.get("summary", ""),
        "insights": parsed.get("insights", []),
        "risks": parsed.get("risks", []),
        "recommendations": parsed.get("recommendations", [])
    }


# -----------------------------
# Download Feature
# -----------------------------
def build_download_payload(result: dict) -> str:
    return json.dumps(result, indent=4)


# -----------------------------
# History Feature
# -----------------------------
HISTORY_FILE = "outputs/history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_to_history(result: dict):
    history = load_history()
    history.append(result)

    os.makedirs("outputs", exist_ok=True)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)