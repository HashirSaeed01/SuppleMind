from backend.scrapeData import fetch_supplement_posts
from backend.embeddings import convert_to_embeddings
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import pickle
import os

# Directory for storing embeddings
EMBEDDINGS_FILE = "data/embeddings.pkl"

# Connect to Qdrant (Cloud or Local)
qdrant_client = QdrantClient(
    url="https://9b7c1600-4f16-4ab5-a09a-e04ecaf893ad.europe-west3-0.gcp.cloud.qdrant.io:6333",  
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.7OPV3YEszm7HEVW36Q3D97_UWWnQdOhVG03CzHpNJ8c"  # Replace with actual API Key
)

# Ensure the collection exists
qdrant_client.recreate_collection(
    collection_name="supplements",
    vectors_config={"size": 384, "distance": "Cosine"}
)

def fetch_and_embed():
    """Fetch posts from Reddit, convert them to embeddings, store locally and in Qdrant."""
    posts = fetch_supplement_posts(limit=10)  # Fetch posts
    texts = [post["title"] + " " + post["body"] for post in posts]  # Combine title & body
    
    # Print the text before conversion
    for i, text in enumerate(texts):
        print(f"\nText {i + 1}:\n{text}\n{'-'*50}")

    embeddings = convert_to_embeddings(texts)  # Convert to embeddings

    # Save embeddings locally
    os.makedirs("data", exist_ok=True)
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(embeddings, f)

    print(f"Embeddings stored locally. Count: {len(embeddings)}")

    # Insert embeddings into Qdrant
    points = [
        PointStruct(id=i, vector=emb, payload={"category": "supplement", "text": texts[i]}) 
        for i, emb in enumerate(embeddings)
    ]
    
    qdrant_client.upsert(collection_name="supplements", points=points)
    print("Embeddings inserted into Qdrant")

def search_zinc():
    """Search for zinc-related posts."""
    query = "What are the benefits of zinc?"
    query_embedding = convert_to_embeddings([query])[0]

    results = qdrant_client.search(
        collection_name="supplements",
        query_vector=query_embedding,
        limit=5
    )

    print("\nTop 5 matching posts for 'zinc':")
    for res in results:
        print(f"Score: {res.score} | Text: {res.payload['text']}")

if __name__ == "__main__":
    fetch_and_embed()
    search_zinc()
