from process_videos import process_videos
from speech_to_text import speech_to_text
from read_chunks import read_chunks
from faiss_index import create_faiss_index


def run_pipeline():
    print("=" * 60)
    print("Step 1/4 : Extracting Audio")
    process_videos()

    print("=" * 60)
    print("Step 2/4 : Transcribing")
    speech_to_text()

    print("=" * 60)
    print("Step 3/4 : Creating Embeddings")
    read_chunks()

    print("=" * 60)
    print("Step 4/4 : Building FAISS Index")
    create_faiss_index()

    print("=" * 60)
    print("Pipeline Completed Successfully!")