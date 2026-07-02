import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
chunks = []

def reload_index():
    global index, chunks

    index = faiss.read_index("faiss.index")
    with open("chunks_with_source.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

# Load once when module is imported
reload_index()

def search(query, k=6):
    if not chunks:
        return []

    k = min(k, len(chunks))
    if k <= 0:
        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype(np.float32)

    D, I = index.search(query_embedding, k)

    results = []

    for idx in I[0]:
        if idx < 0 or idx >= len(chunks):
            continue

        chunk = chunks[idx].copy()
        chunk["idx"] = idx
        results.append(chunk)

    return results