import json
import pickle
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from src.config import EMBED_MODEL


def build_index(output_folder):

    data_path = os.path.join(output_folder, "final_summary.json")
    index_file = os.path.join(output_folder, "vector.indexing")
    meta_file = os.path.join(output_folder, "metadata.pkl")

    print("📥 Loading structured JSON...")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    metadata = []

    for item in data:

        text_block = f"""
Question asked by: {item['summary']['asked_by']}
Ministry: {item['summary']['ministry']}
Category: {item['summary']['category']}

Question Summary:
{item['summary']['question_summary']}

Answer Summary:
{item['summary']['answer_summary']}

Overall Summary:
{item['summary']['overall_summary']}
"""

        documents.append(text_block)
        metadata.append(item)

    print("🧠 Creating embeddings...")

    model = SentenceTransformer(EMBED_MODEL)
    embeddings = model.encode(documents).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, index_file)

    with open(meta_file, "wb") as f:
        pickle.dump(metadata, f)

    print("✅ Vector index built successfully!")
    print(f"📁 Saved index → {index_file}")