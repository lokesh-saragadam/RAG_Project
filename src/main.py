import sys
import json
from pdf_Reader import extract_pdf
from chunker import chunk_text
from data_handling import load_chunks,save_chunks,load_queries,query_extraction
from search import search_chunks
from vector_store import build_index,search_semantic
from rag_pipeline import answer_with_context
from evaluation import evaluate_source_score

##Create and Save Chunks

# file_paths = ["../data/4k weeks.pdf","../data/Atomic habits.pdf","../data/Web App Development Plan.pdf"]

# sources = [ "Four Thousand Weeks","Atomic Habits", "Web Development Plan"]

# texts = extract_pdf(file_paths)

# chunks = chunk_text(texts,sources,chunk_size=500)

# print("Total Chunks :",len(chunks))

# save_chunks(chunks,"..\data\chunks.jsonl")

# sys.exit()

##Loading the Chunks

chunks = load_chunks("..\data\chunks.jsonl")

queries_data = load_queries("..\data\Queries.json")

queries = query_extraction(queries_data[:10])

#storing semantic meanaing of the chunks
string_chunks = [f"{chunk}" for chunk in chunks]
build_index(string_chunks)

#searching for the similiar vectors to that of a query vector
best_indices,similiarity_scores = search_semantic(queries,k=5)

print("The sources used include : ",)
different_query_chunks =[]
retrieval_chunk_idx = []
for best_idx,sim_scores in zip(best_indices,similiarity_scores):
    top_k_chunks_stringified = []
    top_k_chunks = []
    for id,score in zip(best_idx,sim_scores):
        top_k_chunks_stringified.append(string_chunks[id])
        top_k_chunks.append(chunks[id])
        print("",chunks[id]["chunk_id"],"\n",chunks[id]["page"],"\n",chunks[id]["source"],"\n",f"{score:.3f} \n")
    different_query_chunks.extend(top_k_chunks_stringified)
    retrieval_chunk_idx.append(top_k_chunks)


#Retreival evaluation
score_source = evaluate_source_score(queries_data,retrieval_chunk_idx) #retreival accuracy.

print("The answer from chunks of embedded search \n",answer_with_context(query=queries,context=different_query_chunks))

print("Source matches are : ",score_source)
