from upload_utils import save_uploaded_video
from process_videos import process_videos
from speech_to_text import speech_to_text
from read_chunks import embed_chunks, append_chunks
from faiss_index import append_faiss
from query import reload_index


def run_incremental_pipeline(uploaded_file):

    try:

        # Step 1
        video_path = save_uploaded_video(uploaded_file)

        # Step 2
        audio_path = process_videos(video_path)

        if audio_path is None:
            return False, "Audio extraction failed."

        # Step 3
        json_path = speech_to_text(audio_path)

        if json_path is None:
            return False, "Transcription failed."

        # Step 4
        new_chunks, new_embeddings = embed_chunks(json_path)

        # Step 5
        append_chunks(new_chunks)

        # Step 6
        append_faiss(new_embeddings)
        
        # reload index
        reload_index()

        return True, "Video processed and indexed successfully."

    except Exception as e:

        return False, str(e)