from flask import Flask, request, jsonify
from backend.scrapeData import fetch_supplement_posts
from backend.embeddings import convert_to_embeddings
import pickle
import os

app = Flask(__name__)

# Directory for storing embeddings
EMBEDDINGS_FILE = "data/embeddings.pkl"

@app.route("/fetch_and_embed", methods=["GET"])
def fetch_and_embed():
    """Fetch posts from Reddit, convert them to embeddings, and store them."""
    posts = fetch_supplement_posts(limit=10)  # Fetch posts
    
    texts = [post["title"] + " " + post["body"] for post in posts]  # Combine title & body
    
    embeddings = convert_to_embeddings(texts)  # Convert to embeddings
    
    # Save embeddings
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(embeddings, f)

    return jsonify({"message": "Embeddings stored successfully", "count": len(embeddings)})

if __name__ == "__main__":
    app.run(debug=True)
