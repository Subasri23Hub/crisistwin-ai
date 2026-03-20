from __future__ import annotations

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from utils.embeddings import embed_text, embed_texts


def retrieve_relevant_chunks(query: str, chunks: list[str], top_k: int = 5) -> list[tuple[str, float]]:
    if not chunks:
        return []

    query_vector = np.array(embed_text(query)).reshape(1, -1)
    chunk_vectors = np.array(embed_texts(chunks))

    similarities = cosine_similarity(query_vector, chunk_vectors)[0]
    ranked = sorted(
        zip(chunks, similarities),
        key=lambda pair: pair[1],
        reverse=True,
    )

    return [(chunk, float(score)) for chunk, score in ranked[:top_k]]
