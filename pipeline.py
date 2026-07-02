import os

from upload_utils import save_uploaded_video
from process_videos import process_videos
from speech_to_text import speech_to_text
from read_chunks import embed_chunks, append_chunks
from faiss_index import append_faiss
from query import reload_index


def run_incremental_pipeline(uploaded_file, status_callback=None):

    def update_status(message):
        if status_callback:
            status_callback(message)

    try:

        # Duplicate upload check
        video_name = os.path.splitext(uploaded_file.name)[0]
        json_file = os.path.join("json_files", f"{video_name}.json")

        if os.path.exists(json_file):
            return False, "This video has already been indexed."

        # Step 1
        update_status("📤 Saving uploaded video...")
        video_path = save_uploaded_video(uploaded_file)

        # Step 2
        update_status("🎵 Extracting audio...")
        audio_path = process_videos(video_path)

        if audio_path is None:
            return False, "Audio extraction failed."

        # Step 3
        update_status("🎙️ Converting speech to text...")
        json_path = speech_to_text(audio_path)

        if json_path is None:
            return False, "Transcription failed."

        # Step 4
        update_status("🧠 Creating embeddings...")
        new_chunks, new_embeddings = embed_chunks(json_path)

        # Step 5
        update_status("📚 Updating knowledge base...")
        append_chunks(new_chunks)
        append_faiss(new_embeddings)

        # Step 6
        update_status("🔄 Refreshing search index...")
        reload_index()

        update_status("✅ Video indexed successfully.")

        return True, "Video processed and indexed successfully."

    except Exception as e:
        return False, str(e)