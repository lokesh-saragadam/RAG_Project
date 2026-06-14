import faiss
import numpy as np
from embedder import get_embedding

def build_index(chunks):
    embedded_vectors = get_embedding(chunks)
    dimension = embedded_vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Add the vectors to the index
    # Note: FAISS requires float32 arrays
    index.add(embedded_vectors.astype("float32"))
    print(f"Total vectors indexed: {index.ntotal}")

    ##indexing completed.
    # Save the index to a local file
    faiss.write_index(index, "my_faiss_index.index")


def search_semantic(queries):
    best_match_indices = []
    for query in queries:
        # To load it back later (e.g., in a separate run or script):
        index = faiss.read_index("my_faiss_index.index")

        # 1. Vectorize the user query and reshape it into a 2D array [1, 384]
        query_vector = get_embedding([query]).astype("float32")

        # 2. Search the index
        # k=3 means we want the top 3 closest match
        # 'distances' contains the similarity scores, 'indices' contains the position tracking numbers
        distances, indices = index.search(query_vector, k=3)

        # 3. Retrieve the matching text using the returned index reference
        best_match_idx = indices[0]
        similarity_score = distances[0]

        print(f"\nUser Query: {query}")
        print(f"Matched Document Index: {best_match_idx}")
    # print(f"Similarity Score (Dot Product): {similarity_score:.4f}")
        best_match_indices.append(best_match_idx)
    return best_match_indices


