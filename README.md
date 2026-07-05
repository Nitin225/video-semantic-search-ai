---
title: Video Semantic Search AI
colorFrom: indigo
colorTo: gray
sdk: docker
app_port: 8501
pinned: false
license: mit
short_description: RAG-based video search.
---

# Video Semantic Search AI

Upload a video, ask a question in plain English, and get an answer — with the exact timestamp it came from.

Built with **Whisper**, **FAISS**, **Sentence Transformers**, and **Groq's Llama 3.1**, wrapped in a simple Streamlit app.

---

## How it works

```
Video → Extract audio → Whisper transcribes → Split into chunks
      → Embed chunks → Store in FAISS → Search relevant chunks
      → Groq Llama 3.1 answers using those chunks → Answer + timestamp
```

In short: it's a mini RAG (Retrieval-Augmented Generation) pipeline, but for video instead of text documents.

---

## Features

- Upload and index videos right from the browser
- Automatic transcription (Whisper)
- Semantic search over transcripts (FAISS)
- Grounded Q&A — answers are based only on your video, not guesswork
- Timestamped sources, so you can jump to the right part of the video
- Incremental indexing — add new videos without re-processing old ones
- Duplicate upload detection
- Live status updates while indexing

---

## Tech stack

| Purpose | Tool |
|---|---|
| UI | Streamlit |
| Speech-to-text | OpenAI Whisper |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector search | FAISS |
| Answer generation | Groq (Llama 3.1) |
| Audio extraction | FFmpeg |

---

## Run it locally

```bash
git clone https://github.com/Nitin225/video-semantic-search-ai.git
cd video-semantic-search-ai
git checkout deploy-version

python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # Mac/Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

Then run:

```bash
streamlit run app.py
```

## Run it with Docker

```bash
docker build -t video-semantic-search .
docker run -p 8501:8501 --env-file .env video-semantic-search
```

Open **http://localhost:8501** in your browser.

---

## Project structure

```
app.py              # Streamlit UI
pipeline.py          # Orchestrates the full indexing pipeline
speech_to_text.py    # Whisper transcription
read_chunks.py        # Splits transcripts into chunks
faiss_index.py        # Builds/updates the FAISS vector index
query.py             # Semantic search over the index
llm.py               # Calls Groq to generate the final answer
process_videos.py     # Video/audio processing helpers
upload_utils.py       # Upload handling & duplicate detection
```

---

## Future improvements

- Hybrid search (keyword + semantic)
- Reranking for better retrieval
- Cloud storage for videos/index
- Multi-user support

---

## License

MIT
