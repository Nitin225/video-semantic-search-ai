import os
import faiss
import numpy as np

# Existing workflow 

def create_faiss_index():
    embeddings = np.load("embeddings.npy")

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    faiss.write_index(index, "faiss.index")

    print("Index saved!")

# Incremental workflow

def append_faiss(new_embeddings):

    if len(new_embeddings) == 0:
        return

    new_embeddings = np.asarray(new_embeddings, dtype=np.float32)

    if os.path.exists("faiss.index"):
        index = faiss.read_index("faiss.index")
    else:
        # First-ever upload: no index exists yet, create one
        dim = new_embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)

    index.add(new_embeddings)

    faiss.write_index(index, "faiss.index")

    print("FAISS index updated successfully!")


if __name__ == "__main__":
    create_faiss_index()