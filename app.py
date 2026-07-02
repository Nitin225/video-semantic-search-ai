import os
import logging
import streamlit as st

from pipeline import run_incremental_pipeline
from query import search
from llm import generate_answer

os.environ["STREAMLIT_SUPPRESS_CONFIG_WARNINGS"] = "true"
logging.getLogger("transformers").setLevel(logging.ERROR)

st.set_page_config(
    page_title="Video Semantic Search AI",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

#  Main UI

st.title(" Video Semantic Search AI")

uploaded_file = st.file_uploader(
    "Choose a video",
    type=["mp4"],
)

st.write(uploaded_file)

st.stop()

st.caption(
    "Upload videos, build a searchable knowledge base, and ask natural language questions."
)

# Upload Section 

st.header(" Upload & Index Video")

uploaded_file = st.file_uploader(
    "Choose a video",
    type=["mp4", "mkv", "avi", "mov", "webm"],
)

if uploaded_file is not None:

    st.info(f"Selected file: **{uploaded_file.name}**")

    if st.button(" Index Video", use_container_width=True):

        status_box = st.empty()

        def update_status(message):
            status_box.info(message)

        success, message = run_incremental_pipeline(
            uploaded_file,
            status_callback=update_status
        )

        status_box.empty()

        if success:
            st.success(message)
        else:
            st.warning(message)

st.divider()

# Question Answering

st.header(" Ask Questions")

query = st.text_input(
    "Ask anything about the indexed videos..."
)

if query.strip():

    try:
        results = search(query)

    except Exception as e:
        st.error(f"Search failed: {e}")
        st.stop()

    if not results:
        st.warning("No relevant context found.")
        st.stop()

    with st.spinner("Generating answer..."):

        try:
            answer = generate_answer(query, results)

        except Exception as e:
            st.error(f"Answer generation failed: {e}")
            answer = ""

    st.subheader(" Answer")

    if answer.strip():
        st.markdown(answer)
    else:
        st.info("Could not generate an answer.")

    st.divider()

    with st.expander(" Retrieved Sources"):

        for i, r in enumerate(results, start=1):

            st.markdown(f"**Source {i}**")

            st.caption(
                f"📄 {r['source']} | ⏱ {r['start']:.2f}s – {r['end']:.2f}s"
            )

            st.write(r["text"])

            if i != len(results):
                st.divider()

st.divider()

#  About

with st.expander(" About This Project"):

    st.markdown("""
### Tech Stack

- **Speech-to-Text:** Whisper Small
- **Embeddings:** all-MiniLM-L6-v2
- **Vector Search:** FAISS
- **LLM:** Llama 3.1 8B (Groq)

### Features

- Semantic search over video transcripts
- Incremental video indexing
- Automatic transcript chunking
- Duplicate upload detection
- Grounded question answering using RAG
""")