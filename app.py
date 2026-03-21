import os
import logging
import json
import streamlit as st
from query import search
from llm import generate_answer



with open("chunks_with_source.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

os.environ["STREAMLIT_SUPPRESS_CONFIG_WARNINGS"] = "true"
logging.getLogger("transformers").setLevel(logging.ERROR)

st.title("Video Q&A System")

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

    st.subheader("Results:")

    with st.expander("Sources"):
        for r in results:
            st.write(f"{r['text']}")
            st.write(f"Source: {r['source']}")
            st.write(f"{r['start']} - {r['end']}")
            st.write("---")
        

    with st.spinner("Thinking... "):
        try:
            answer = generate_answer(query, results)
        except Exception as e:
            st.error(f"Answer generation failed: {e}")
            answer = ""

    st.subheader("Answer")
    if answer and answer.strip():
        st.write(answer)
    else:
        st.info("Could not generate an answer right now. Please try again.")
