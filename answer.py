from google import genai

from retrieve import retrieve

MODEL = "gemini-3.5-flash-lite"
client = genai.Client()  # reads GEMINI_API_KEY from the environment


def generate(prompt: str) -> str:
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text


def answer(question: str) -> str:
    results = retrieve(question)
    if not results:
        return "I don't have that information."
    context = "\n".join(f"- {c['text']}" for _, c in results)
    prompt = (
        "Answer the question using ONLY the context below. "
        "If the context does not contain the answer, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    return generate(prompt)


if __name__ == "__main__":
    for q in [
        "What documents do I need for a loan?",
        "How can I pay back early?",
        "What is the capital of France?",
    ]:
        print(f"\nQ: {q}\nA: {answer(q)}")