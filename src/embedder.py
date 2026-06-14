from sentence_transformers import SentenceTransformer

# # Load the pre-trained model
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# # Save the model to a local folder named 'local_minilm_model'
# embedding_model.save("local_minilm_model")
# print("Model saved successfully!")

# # Load instantly from your local disk (Works completely offline!)
embedding_model = SentenceTransformer("./local_minilm_model")

def get_embedding(chunks):
    # Generate the embeddings (returns a NumPy array or PyTorch tensor)
    embeddings = embedding_model.encode(chunks)

    return embeddings
