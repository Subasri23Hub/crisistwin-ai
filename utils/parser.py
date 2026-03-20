from __future__ import annotations

import io
import fitz
import pandas as pd


def extract_text_from_pdf(file) -> str:
    file.seek(0)
    pdf_bytes = file.read()
    text_parts = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page_number, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(f"[Page {page_number}]\n{page_text.strip()}")
    return "\n\n".join(text_parts)


def extract_text_from_txt(file) -> str:
    file.seek(0)
    return file.read().decode("utf-8", errors="ignore")


def extract_text_from_csv(file) -> str:
    file.seek(0)
    df = pd.read_csv(io.BytesIO(file.read()))
    if df.empty:
        return ""
    preview_rows = []
    for _, row in df.head(50).iterrows():
        preview_rows.append(" | ".join(f"{col}: {row[col]}" for col in df.columns))
    return "\n".join(preview_rows)


def extract_text_from_file(file) -> str:
    name = file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    if name.endswith(".txt"):
        return extract_text_from_txt(file)
    if name.endswith(".csv"):
        return extract_text_from_csv(file)
    return ""
