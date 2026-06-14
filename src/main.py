import sys
import json
from pdf_Reader import extract_pdf
from chunker import chunk_text
from data_handling import load_chunks,save_chunks,load_queries,query_extraction
from search import search_chunks
from vector_store import build_index,search_semantic
from rag_pipeline import answer_with_context
from evaluation import evaluate_source_score

file_paths = ["../data/4k weeks.pdf","../data/Atomic habits.pdf","../data/Web App Development Plan.pdf"]

sources = [ "Four Thousand Weeks","Atomic Habits", "Web Development Plan"]

texts = extract_pdf(file_paths)

chunks = chunk_text(texts,sources,chunk_size=500)

print("Total Chunks :",len(chunks))

save_chunks(chunks,"..\data\chunks.jsonl")

sys.exit()

chunks = load_chunks("..\data\chunks.jsonl")


queries_data = load_queries("..\data\Queries.json")
# top_k_chunks = search_chunks(query,chunks)
queries = query_extraction(queries_data)
# print("The answer fromchunks of keyword search")
# print(answer_with_context(query=query,retrieved_chunks=top\
# _k_chunks))



#storing semantic meanaing of the chunks
string_chunks = [f"{chunk}" for chunk in chunks]
build_index(string_chunks)

#searching for the similiar vectors to that of a query vector
best_indices = search_semantic(queries)


print("The sources used include : ",)
different_query_chunks =[]
for best_idx in best_indices:
    top_3_chunks = []
    for idx in best_idx:
        top_3_chunks.append(string_chunks[idx])
    different_query_chunks.append(top_3_chunks)

#Retreival evaluation


score_source = evaluate_source_score(queries_data,different_query_chunks)


print("The answer from chunks of embedded search \n",answer_with_context(query=queries,context=different_query_chunks))

