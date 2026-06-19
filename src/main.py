import json

from pdf_Reader import extract_pdf
from chunker import chunk_text
from data_handling import save_chunks,load_queries,query_extraction
from vector_store import build_index,search_semantic,similiarity_score
from rag_pipeline import generate_answers
from evaluation import  evaluate_scores,decision_tree

# INITIALIZATION

def initialize_rag( file_paths,source_names,chunk_size=400,overlap=50):
    """
    Run in the begingning to create and save chunks, and build the FAISS index.
    Returns:
        chunks,string_chunks
    """
    texts = extract_pdf(file_paths)

    chunks = chunk_text(texts,source_names,chunk_size=chunk_size,overlap=overlap)

    save_chunks(chunks,"../data/chunks.jsonl")

    string_chunks = [
        str(chunk)
        for chunk in chunks
    ]

    build_index(string_chunks)

    print(f"Total Chunks: {len(chunks)}")

    return chunks, string_chunks

# RETRIEVAL

def retrieve_context(query,chunks,string_chunks,k=5):
    """
    Retrieve top-k chunks for a single user query.
    Returns:
        retrieved_context,citations,retrieved_chunks
    """

    best_indices, similarity_scores = search_semantic(
        [query],
        k=k,
    )

    retrieved_context = []

    retrieved_chunks = []

    citations = []

    for idx in best_indices[0]:

        retrieved_context.append(string_chunks[idx])

        retrieved_chunks.append(chunks[idx])

        citations.append((chunks[idx]["source"],chunks[idx]["page"]))

    citations = list(set(citations))

    return (retrieved_context,citations,retrieved_chunks,similarity_scores[0])


# ANSWER GENERATION

def generate_response(query,chunks,string_chunks,k=5,):
    """
    End-to-end RAG query.
    """
    (contexts,citations,retrieved_chunks,retrieval_scores)=retrieve_context(query,chunks,string_chunks,k=k)

    result = generate_answers(contexts=contexts,queries=[query],)

    answer = result["answers"][0]["answer"]

    return {
        "query": query,
        "answer": answer,
        "citations": citations,
        "retrieved_chunks": retrieved_chunks,
        "retrieval_scores": retrieval_scores,
    }


# EVALUATION

def evaluate_pipeline(query_file,chunks,string_chunks,k=5,):
    """
    Used only for benchmarking.
    """

    queries_data = load_queries(query_file)

    queries = query_extraction(queries_data)

    retrieval_chunk_idx = []

    sources = []

    all_contexts = []

    best_indices, _ = search_semantic(queries,k=k,)

    for best_idx in best_indices:

        curr_chunks = []

        curr_sources = []

        for idx in best_idx:

            curr_chunks.append(chunks[idx])

            curr_sources.append((chunks[idx]["source"],chunks[idx]["page"]))

            all_contexts.append(string_chunks[idx])

        retrieval_chunk_idx.append(curr_chunks)

        sources.append(list(set(curr_sources)))

    source_scores, citation_scores = (evaluate_scores(queries_data,retrieval_chunk_idx))

    result = generate_answers(contexts=all_contexts,queries=queries)

    answers = [item["answer"]for item in result["answers"]]

    sim_scores = similiarity_score(queries,answers,)

    decisions = decision_tree(
        sim_scores=sim_scores,
        source_scores=source_scores,
        cit_scores=citation_scores,
    )

    return {
        "answers": answers,
        "sources": sources,
        "similarity_scores": sim_scores,
        "source_scores": source_scores,
        "citation_scores": citation_scores,
        "decisions": decisions,
    }