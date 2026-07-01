import faiss
import numpy as np


def create_faiss_index():
    embeddings = np.load("embeddings.npy")
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, "faiss.index")
    print("Index saved!")


if __name__ == "__main__":
    create_faiss_index()