# Architecture

The RAG (Retrieval-Augmented Generation) pipeline is designed to answer questions from uploaded PDF documents while providing retrieval transparency and evaluation metrics.

## Pipeline Overview

```text
PDF Documents
      │
      ▼
Text Extraction
      │
      ▼
Chunking
      │
      ▼
Embedding Generation
      │
      ▼
FAISS Vector Index
      │
      ▼
Top-k Semantic Retrieval
      │
      ▼
LLM-Based Answer Generation
      │
      ▼
Answer + Source Citations
```

---

## Evaluation Framework

In addition to the live question-answering pipeline, the project includes an offline evaluation module for benchmarking retrieval and generation quality.

```text
Retrieved Chunks
      │
      ▼
Evaluation Module
   ├── Chunk Match Score
   ├── Source Match Score
   └── Answer Similarity Score
      │
      ▼
Failure Classification
```

---

## Component Description

### 1. PDF Processing

* Extracts text and metadata from uploaded PDF documents.
* Preserves source information such as document name and page number.

### 2. Chunking

* Splits extracted text into smaller semantic chunks.
* Maintains metadata required for source attribution and evaluation.

### 3. Embedding Generation

* Converts text chunks into dense vector representations.
* Enables semantic search instead of keyword matching.

### 4. FAISS Vector Store

* Stores chunk embeddings for efficient nearest-neighbor retrieval.
* Supports scalable similarity search over large document collections.

### 5. Retrieval

* Retrieves the top-k most relevant chunks for a given user query.
* Returns associated metadata including source document and page references.

### 6. LLM Generation

* Uses retrieved context to generate grounded answers.
* Produces responses with supporting source citations.

### 7. Evaluation Module

The system includes a benchmark dataset containing:

* Expected answers
* Expected source documents
* Expected page numbers

Evaluation metrics include:

* **Chunk Match Score** – Measures whether the correct chunk was retrieved.
* **Source Match Score** – Measures whether the correct source document was retrieved.
* **Answer Similarity Score** – Measures semantic similarity between generated and expected answers.

### 8. Failure Classification

Errors are categorized into:

* Retrieval Failures
* Source Attribution Failures
* Metadata Failures
* Generation Failures

This helps identify whether performance issues originate from retrieval quality, context selection, source tracking, or answer generation.
