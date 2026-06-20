import streamlit as st
import os
import json

from data_handling import load_chunks, save_chunks
from main import (initialize_rag,generate_response,evaluate_pipeline)
from vector_store import build_index

with st.sidebar:
        st.header("Project Information:")

        st.subheader("RAG Pipeline")

        st.subheader("Embedding Model")
        st.write("all-MiniLM-L6-v2")

        st.subheader("Vector Store")
        st.write("FAISS")

        st.subheader("Answer Generation LLM Model")
        st.write("Gemini-2.5-flash")


tab1, tab2 = st.tabs(
    ["Live Uploads", "Evaluation and Failure Detection"]
)

with tab1:
    st.header("Upload a Pdf")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )
    
    if uploaded_file is not None:
        save_path = os.path.join("uploads", uploaded_file.name)

        os.makedirs("uploads", exist_ok=True)  #create a folder to save .
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Uploaded: {uploaded_file.name}")
        chunks, string_chunks = initialize_rag(
                [save_path],
                [uploaded_file.name],
            )
        st.session_state.chunks = chunks
        st.session_state.string_chunks = string_chunks
        st.success("Processing completed!")

        query = st.text_input("Ask a question")
        bool = st.button("Get Answer")
        if query and not bool:
            st.write("Please click the 'Get Answer' button to retrieve the answer.")

        elif (bool and not query):

            st.write("Please enter a question to get an answer.")

        elif bool and query:

            response = generate_response(
                query,
                st.session_state.chunks,
                st.session_state.string_chunks,
            )
            
            st.subheader("Retrieval Statistics")

            st.write(f"Number of Retrieved Chunks: {len(response['retrieved_chunks'])}")
            st.write(F"Top Similarity Score: {max(response['retrieval_scores']):.4f}")
            st.write(f"Average Similarity Score: {sum(response['retrieval_scores']) / len(response['retrieval_scores']):.4f}")
            st.write(f"Unique Sources Retrieved: {len(set([chunk['source'] for chunk in response['retrieved_chunks']]))}")


            st.subheader("Answer")

            st.write(response["answer"])

            st.subheader("Sources")

            for source, page in response["citations"]:
                st.write(f"📖 {source} (page {page})")

            st.subheader("Retrieved Chunks")

            for i in range(len(response["retrieved_chunks"])):
                with st.expander(f"Chunk {i + 1}"):
                    st.write(f"Similarity Score: {response['retrieval_scores'][i]:.4f}")
                    st.write(f"Source: {response['retrieved_chunks'][i]['source']}")
                    st.write(f"Page: {response['retrieved_chunks'][i]['page']}")
                    st.write(f"Text: {response['retrieved_chunks'][i]['text']}")

            st.metric(label="Retrieval Confidence Score", value=f"{sum(response['retrieval_scores']) / len(response['retrieval_scores']):.4f}")

with tab2:
    st.header("Using Default database")

    st.write("Using books like Atomic Habits and Four Thousand Weeks.")

    st.warning("Proceeding with a previously present data of Books Atomic Habits and Four Thousand Weeks.")
    # file_paths = [
    #     "../data/4k weeks.pdf",
    #     "../data/Atomic habits.pdf",
    #     "../data/Web App Development Plan.pdf",
    # ]

    # source_names = [
    #     "Four Thousand Weeks",
    #     "Atomic Habits",
    #     "Web Development Plan",
    # ]
    with st.spinner("Extracting pdf to Chunks"):
        chunks = load_chunks("../data/chunks.jsonl") 
        string_chunks = [
                    str(chunk)
                    for chunk in chunks
                ]

    st.session_state.chunks = chunks
    st.session_state.string_chunks = string_chunks

    with open("../data/Queries.json", "r") as f:
        eval_data = json.load(f)

    queries = eval_data["queries"]

    selected_question = st.selectbox(
        "Choose an evaluation query",
        queries,
        format_func=lambda q: q["question"]
    )

    if selected_question:
        # response = evaluate_pipeline(
        #     selected_question,
        #     st.session_state.chunks,
        #     st.session_state.string_chunks
        # )

        # save_chunks([response],"../data/evaluation_results.jsonl")

        response = load_chunks("../data/evaluation_results.jsonl")
        response = response[0]

        if response:
            st.subheader("Retrieval Statistics")
            st.write(f"Number of Retrieved Chunks: {len(response['similarity_scores'])}")
            st.write(f"Unique Sources Retrieved: {len(response['sources'])}")

            st.subheader("Answer")
            st.write(response["answers"][0])

            st.subheader("Sources")
            for source, page in response["sources"][0]:
                st.write(f"📖 {source} (page {page})")
            
            st.subheader("Retrival Metrics")
            st.write(f"Top Similarity Score: {max(response['similarity_scores']):.4f}")
            st.write(f"Retrieval Confidence Score: {sum(response['similarity_scores']):.4f}")
            st.write(f"Source Accuracy score: {sum(response['source_scores']):.4f}")
            st.write(f"Hit@5 score: {sum(response['citation_scores']):.4f}")
            
            st.subheader("Retrieval chunk Decision")
            st.write(F"Decision of Failure Decision tree: {response['decisions'][0]}")

        else:
            st.write("Select a query to see the evaluation results.")

        
        



