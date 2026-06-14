import numpy as np
from chunker import chunk_text


def search_chunks(query,chunks,k=5):
    maxscore = []
    query_l = query.lower().split()
    for chunk in chunks:
        chunk = chunk.lower().split()
        score = 0
        for qword in query_l:
            if qword in chunk:
                score+=1
        maxscore.append(score)
    top_k_ind = np.argsort(maxscore)[-k:][::-1]
    top_k_chunks = []
    print("The selcted indices include: ",top_k_ind)
    for ind in top_k_ind:
        top_k_chunks.append(chunks[ind])
    return top_k_chunks
        
    