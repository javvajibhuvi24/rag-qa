import numpy as np
THRESHOLD = 0.60
from sentence_transformers import SentenceTransformer

from chunking import load_chunks

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
chunks = load_chunks("data", max_chars=100)
vectors = model.encode([c["text"] for c in chunks], normalize_embeddings=True)


def search(query: str, k: int = 3):
    q = model.encode([query], normalize_embeddings=True)[0]
    scores = vectors @ q
    top = np.argsort(scores)[::-1][:k]
    return [(float(scores[i]), chunks[i]) for i in top]

def retrieve(query: str, k: int = 3):
    results = search(query, k)
    if results[0][0] < THRESHOLD:
        return []
    return results

if __name__ == "__main__":
    questions = [
        "What documents do I need for a loan?",
        "How can I pay back early?",
        "What happens if I miss a payment?",
        "What is the capital of France?",
    ]
    for question in questions:
        print(f"\nQ: {question}")
        results = retrieve(question)
        if not results:
            print("  I don't have that information.")
        for score, c in results:
            print(f"  {score:.2f} [{c['source']}] {c['text'][:120]}")