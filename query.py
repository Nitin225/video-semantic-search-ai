import faiss
import json
from sentence_transformers import SentenceTransformer

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

def search(query, k=4):
    if not chunks:
        return []

    k = min(k, len(chunks))
    if k <= 0:
        return []

    query_embedding = model.encode([query])

    D, I = index.search(query_embedding, k)

    results = []

    for idx in I[0]:
        if idx < 0 or idx >= len(chunks):
            continue

        chunk = chunks[idx].copy()
        chunk["idx"] = idx
        results.append(chunk)

    return results