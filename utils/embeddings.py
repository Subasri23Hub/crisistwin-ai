from __future__ import annotations

from utils.gemini_client import EMBEDDING_MODEL, get_client


def embed_text(text: str) -> list[float]:
    client = get_client()
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    if hasattr(response, "embeddings") and response.embeddings:
        return list(response.embeddings[0].values)

    if hasattr(response, "embedding") and response.embedding:
        return list(response.embedding.values)

    raise ValueError("Embedding response did not contain vectors.")


def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors = []
    for text in texts:
        vectors.append(embed_text(text))
    return vectors
