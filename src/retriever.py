import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from src.config import EMBED_MODEL, TOP_K

model = SentenceTransformer(EMBED_MODEL)


def load_index(folder):

    index_path = os.path.join(folder, "vector.faiss")
    meta_path = os.path.join(folder, "metadata.pkl")

    index = faiss.read_index(index_path)

    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def retrieve(query, index, metadata):

    query_embedding = model.encode([query]).astype("float32")

    distances, indices = index.search(query_embedding, TOP_K)

    results = [metadata[i] for i in indices[0]]

    return results