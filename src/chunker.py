import sys
import json
from pdf_Reader import extract_pdf

def build_pages(texts, sources):
    pages = []

    for source, document in zip(sources, texts):
        for page_num, page_text in enumerate(document, start=1):
            pages.append({
                "source": source,
                "page": page_num,
                "text": page_text
            })

    return pages

from bisect import bisect_right

def chunk_text(texts, sources, chunk_size=500, overlap=100):
    chunks = []
    step = chunk_size - overlap

    for document, source in zip(texts, sources):

        all_words = []
        page_boundaries = []

        current_word_idx = 0

        for page_num, page_text in enumerate(document, start=1):
            page_boundaries.append((current_word_idx, page_num))

            words = page_text.split()

            all_words.extend(words)
            current_word_idx += len(words)

        boundary_indices = [idx for idx, _ in page_boundaries]

        for start in range(0, len(all_words), step):

            end = min(start + chunk_size, len(all_words))
            chunk_words = all_words[start:end]

            if not chunk_words:
                break

            # Find page containing start word
            pos = bisect_right(boundary_indices, start) - 1
            start_page = page_boundaries[pos][1]

            chunks.append({
                "text": " ".join(chunk_words),
                "page": start_page,
                "source": source
            })

    return chunks

