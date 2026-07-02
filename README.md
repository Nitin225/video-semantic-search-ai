---
title: Video Semantic Search AI
emoji: 🎥
colorFrom: indigo
colorTo: gray
sdk: docker
app_port: 8501
pinned: false
license: mit
short_description: RAG-based video search.
---


#  Video Semantic Search AI

An AI-powered Retrieval-Augmented Generation (RAG) application that enables semantic search and question answering over uploaded videos using Whisper, FAISS, Sentence Transformers, and Groq Llama 3.1.

---
##  Features

-  Upload and index videos through the web interface
-  Automatic speech-to-text transcription using Whisper
-  Semantic transcript chunking for better retrieval
-  FAISS-based semantic search
-  Grounded question answering using Groq Llama 3.1
-  Timestamped source attribution
-  Incremental video indexing
-  Duplicate upload detection
-  Live indexing status updates

---

##  Tech Stack

- Python
- Streamlit
- OpenAI Whisper
- Sentence Transformers (all-MiniLM-L6-v2)
- FAISS
- Groq API
- FFmpeg

---

##  Architecture

```text
Video Upload
      │
      ▼
Audio Extraction
      │
      ▼
Whisper Transcription
      │
      ▼
Semantic Chunking
      │
      ▼
Embeddings
      │
      ▼
FAISS
      │
      ▼
Semantic Retrieval
      │
      ▼
Groq Llama 3.1
      │
      ▼
Answer + Sources
```

---

##  Setup

```bash
git clone <repository-url>

cd <repository>

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

Run:

```bash
streamlit run app.py
```

---

##  Project Structure

```text
app.py
pipeline.py
speech_to_text.py
read_chunks.py
faiss_index.py
query.py
llm.py
process_videos.py
upload_utils.py
```

---

##  Future Improvements

- Hybrid Search
- Reranking
- Docker Deployment
- Cloud Storage
- Multi-user Support
