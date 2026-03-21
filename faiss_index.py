import faiss
import numpy as np

embeddings = np.load("embeddings.npy")
dim = embeddings.shape[1]

index = faiss.IndexFlatL2(dim)
index.add(embeddings)

faiss.write_index(index, "faiss.index")
print("Index saved!")