import streamlit as st

st.set_page_config(page_title="Upload Test")

st.title("Upload Test")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["mp4", "mkv", "avi", "mov", "webm"]
)

st.write(uploaded_file)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Test"):
        st.success("Button clicked!")