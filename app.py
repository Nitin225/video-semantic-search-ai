import os
import logging
import streamlit as st
from pipeline import run_incremental_pipeline
from query import search
from llm import generate_answer

os.environ["STREAMLIT_SUPPRESS_CONFIG_WARNINGS"] = "true"
logging.getLogger("transformers").setLevel(logging.ERROR)

st.title(" Video Semantic Search")

st.caption(
    "Upload a video, build a searchable knowledge base, and ask questions about its content."
)

# Upload Section

st.header("Upload & Index")

uploaded_file = st.file_uploader(
    "Choose a video",
    type=["mp4", "mkv", "avi", "mov", "webm"],
)

if uploaded_file is not None:

    if st.button("Index Video"):

        with st.spinner("Processing video... This may take a few minutes."):
            
            success, message = run_incremental_pipeline(uploaded_file)

        if success:
            st.success(message)
        else:
            st.error(message)

st.divider()

# Question Answering

st.header(" Ask Questions")

query = st.text_input("Ask a question:")

if query:

    try:
        results = search(query)

    except Exception as e:
        st.error(f"Search failed: {e}")
        st.stop()

    if not results:
        st.warning("No relevant context found. Try a more specific question.")
        st.stop()

    with st.expander(" Sources"):

        for r in results:

            st.write(r["text"])

            st.caption(
                f"Source: {r['source']} | {r['start']:.2f}s - {r['end']:.2f}s"
            )

            st.divider()

    with st.spinner("Generating answer..."):

        try:
            answer = generate_answer(query, results)

        except Exception as e:
            st.error(f"Answer generation failed: {e}")
            answer = ""

    st.subheader("Answer")

    if answer.strip():
        st.write(answer)

    else:
        st.info("Could not generate an answer right now.")