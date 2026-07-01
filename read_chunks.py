import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Shared helper

def _load_chunks(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Existing workflow 

def read_chunks():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    all_chunks = []

    for file in os.listdir("json_files"):
        if not file.endswith(".json"):
            continue

        json_path = os.path.join("json_files", file)

        all_chunks.extend(_load_chunks(json_path))

    print("Total chunks:", len(all_chunks))

    texts = [chunk["text"] for chunk in all_chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    np.save("embeddings.npy", embeddings)

    with open("chunks_with_source.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4, ensure_ascii=False)

    print("Embeddings created successfully!")

# New workflow

def embed_chunks(json_path):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    new_chunks = _load_chunks(json_path)

    texts = [chunk["text"] for chunk in new_chunks]

    new_embeddings = model.encode(
        texts,
        show_progress_bar=False
    )

    return new_chunks, new_embeddings

# Metadata update
def append_chunks(new_chunks):

    if not new_chunks:
        return

    metadata_path = "chunks_with_source.json"

    if os.path.exists(metadata_path):

        with open(metadata_path, "r", encoding="utf-8") as f:
            old_chunks = json.load(f)

    else:
        old_chunks = []

    old_chunks.extend(new_chunks)

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(
            old_chunks,
            f,
            indent=4,
            ensure_ascii=False
        )


if __name__ == "__main__":
    read_chunks()