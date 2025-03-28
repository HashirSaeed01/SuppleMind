from sentence_transformers import SentenceTransformer

# Load MiniLM embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def convert_to_embeddings(texts):
    """
    Converts a list of texts into embeddings.
    
    Args:
        texts (list of str): List of text documents.
        
    Returns:
        list: Corresponding embeddings.
    """
    return model.encode(texts, convert_to_numpy=True)  # Convert text to embeddings
