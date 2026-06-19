import streamlit as st

from main import (initialize_rag,generate_response,retrieve_context)

if "chunks" not in st.session_state:

    file_paths = [
        "../data/4k weeks.pdf",
        "../data/Atomic habits.pdf",
        "../data/Web App Development Plan.pdf",
    ]

    source_names = [
        "Four Thousand Weeks",
        "Atomic Habits",
        "Web Development Plan",
    ]

    chunks, string_chunks = initialize_rag(
        file_paths,
        source_names,
    )

    st.session_state.chunks = chunks
    st.session_state.string_chunks = string_chunks

query = st.text_input("Ask a question")

if st.button("Get Answer") and query:

    response = generate_response(
        query,
        st.session_state.chunks,
        st.session_state.string_chunks,
    )

    st.write(response["answer"])

    st.subheader("Sources")

    for source, page in response["citations"]:
        st.write(f"📖 {source} — Page {page}")

elif (st.button("Get Answer") and not query):

    st.write("Please enter a question to get an answer.")