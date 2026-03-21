import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# load model
model = SentenceTransformer('all-MiniLM-L6-v2')

all_chunks = []

# load all json files
for file in os.listdir("json_files"):
    if not file.endswith(".json"):
        continue

    with open(f"json_files/{file}", "r", encoding="utf-8") as f:
        data = json.load(f)   # list of chunks
        all_chunks.extend(data)

print("Total chunks:", len(all_chunks))

# extract text
texts = [chunk["text"] for chunk in all_chunks]

# generate embeddings 
embeddings = model.encode(texts, show_progress_bar=True)

# save embeddings
np.save("embeddings.npy", embeddings)

# save metadata 
with open("chunks_with_source.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=4, ensure_ascii=False)

print("Embeddings created successfully!")