import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


index = faiss.read_index("faiss.index")

with open("chunks_with_source.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


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

