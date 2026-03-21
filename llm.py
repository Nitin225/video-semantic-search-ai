import requests
import json
import os


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
        response = requests.post(
        os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/api/generate",
        json={
            "model": os.getenv("OLLAMA_MODEL", "llama3:8b"),
            "prompt": prompt,
            "stream": True,
            "options": {
                    "temperature": 0.2,
                    "num_predict": 220
                }
            },
            stream=True,
            timeout=(10, 300),  # connect timeout, read timeout
        )
        response.raise_for_status()

        answer = ""
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            answer += data.get("response", "")
        return answer.strip() or "I don't have enough information in the provided context."

    except requests.exceptions.Timeout:
        return "Model response timed out. Please try again or ask a shorter question."
    except requests.exceptions.RequestException as e:
        return f"LLM service error: {e}"