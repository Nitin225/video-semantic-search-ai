from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open("chunks_with_source.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def generate_answer(query, results):
    # combine context
    expanded = []

    for r in results:
        idx = r.get("idx")
        if idx is None:
            continue

        for i in range(max(0, idx-1), min(len(chunks), idx+2)):
            expanded.append(chunks[i]["text"])

    # remove duplicates (important)
    expanded = list(dict.fromkeys(expanded))

    context = "\n".join(expanded)

    prompt = f"""
You are an intelligent assistant.
Answer the question clearly and briefly using only the context provided below.
If the context does not contain the answer, say:
"I don't have enough information in the provided context."
Do not use outside knowledge.

Context:
{context}

Question: {query}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=220,
        )

        return (
            response.choices[0].message.content.strip()
            or "I don't have enough information in the provided context."
        )

    except Exception as e:
        return f"LLM service error: {e}"