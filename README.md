# RAG-Based Video Q&A System

A local Retrieval-Augmented Generation (RAG) application that answers user questions from video content using transcript retrieval and LLM-based response generation.

## Project Summary
This project converts videos into searchable knowledge and serves grounded answers through a Streamlit interface.  
It combines speech-to-text, semantic retrieval, and local LLM inference in an end-to-end pipeline.

## Key Highlights
- Built an end-to-end RAG workflow: video -> transcript -> embeddings -> retrieval -> answer generation
- Implemented timestamped chunking for traceable source context
- Added FAISS-based semantic search for fast relevant context retrieval
- Integrated local Ollama model for private, offline-friendly inference
- Included fail-safe handling for retrieval errors, empty context, and model timeout scenarios

## Tech Stack
- `Python`
- `Streamlit`
- `OpenAI Whisper`
- `SentenceTransformers` (`all-MiniLM-L6-v2`)
- `FAISS`
- `Ollama` (`llama3:8b`)

## System Architecture
1. `process_videos.py` - extracts audio from video files
2. `speech_to_text.py` - transcribes audio and creates timestamped chunks
3. `read_chunks.py` - builds embeddings and merged metadata file
4. `faiss_index.py` - creates FAISS index from embeddings
5. `query.py` - retrieves top-k relevant chunks
6. `llm.py` - generates grounded answers from retrieved context
7. `app.py` - Streamlit UI for question-answer interaction

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run
Place your input video files inside the `videos/` folder before running the pipeline.

```bash
python process_videos.py
python speech_to_text.py
python read_chunks.py
python faiss_index.py
streamlit run app.py
```

> Note: Transcription and chunk generation can take significant time on CPU (depends on video length and hardware). This is expected for first-time processing.

## Ollama Setup
Make sure Ollama is running locally and the model is available:
```bash
ollama pull llama3:8b
```

Optional environment variables:
- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
- `OLLAMA_MODEL` (default: `llama3:8b`)

## Results
- Built a complete local RAG pipeline for video-based Q&A with source-grounded responses.
- Improved reliability through guarded retrieval and LLM timeout/error handling.
- Added transparent source traces using timestamped transcript chunks in the UI.

## Current Limitations
- Processing can be slow on CPU for long videos (transcription + embedding generation).
- Pipeline is batch-based; it does not yet support background/asynchronous ingestion.
- Retrieval is basic top-k semantic search without reranking or hybrid keyword search.

## Future Improvements
- Automated evaluation (Recall@k, groundedness/faithfulness checks)
- Dockerized deployment
- Caching and async processing for faster response times
