import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = None

index = None
chunks = []


def get_embedding_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def reload_index():
    global index, chunks

    if not os.path.exists("faiss.index") or not os.path.exists("chunks_with_source.json"):
        index = None
        chunks = []
        return

    index = faiss.read_index("faiss.index")

    with open("chunks_with_source.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)


reload_index()


def search(query, k=6):

    if index is None or not chunks:
        return []

    k = min(k, len(chunks))

    query_embedding = (
        get_embedding_model()
        .encode([query], convert_to_numpy=True)
        .astype(np.float32)
    )

    D, I = index.search(query_embedding, k)

    results = []

    for idx in I[0]:

        if idx < 0 or idx >= len(chunks):
            continue

        chunk = chunks[idx].copy()
        chunk["idx"] = idx

        results.append(chunk)

    return results