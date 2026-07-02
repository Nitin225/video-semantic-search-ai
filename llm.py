from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def load_chunks():
    with open("chunks_with_source.json", "r", encoding="utf-8") as f:
        return json.load(f)


def generate_answer(query, results):

    # Always use the latest chunks
    chunks = load_chunks()

    expanded = []

    for r in results:
        idx = r.get("idx")

        if idx is None:
            continue

        # Take two chunks before and after
        for i in range(max(0, idx - 4), min(len(chunks), idx + 5)):
            expanded.append(chunks[i]["text"])

    # Remove duplicates
    expanded = list(dict.fromkeys(expanded))

    context = "\n".join(expanded)

    prompt = f"""
You are an intelligent assistant.
Answer ONLY using the provided context.
Guidelines:
- Keep the answer concise (3–6 sentences).
- Explain the concept clearly.
- Combine relevant information from multiple context snippets.
- Do not repeat information.
- Do not use outside knowledge.
- Do not invent facts.
If the answer is not available in the context, reply exactly:
"I don't have enough information in the provided context."

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            max_tokens=256,
        )

        return (
            response.choices[0].message.content.strip()
            or "I don't have enough information in the provided context."
        )

    except Exception as e:
        return f"LLM service error: {e}"