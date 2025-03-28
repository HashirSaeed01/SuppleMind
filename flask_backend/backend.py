import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import importlib.util

# This would normally import from your backend modules
# Placeholder for actual imports - you'll need to adjust these paths
try:
    from backend.embeddings import convert_to_embeddings
    from qdrant_client import QdrantClient
    from dotenv import load_dotenv
except ImportError:
    print("Backend modules not found. Running in demo mode with mock responses.")

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Try to load environment variables and initialize clients
# If this fails, we'll use mock responses
try:
    # Load .env file
    load_dotenv()

    # Initialize Qdrant Client
    qdrant_client = QdrantClient(
        url="https://9b7c1600-4f16-4ab5-a09a-e04ecaf893ad.europe-west3-0.gcp.cloud.qdrant.io:6333",
        api_key=os.getenv("QDRANT_API_KEY")
    )

    # Hugging Face API Key
    HF_API_KEY = os.getenv("HF_API_KEY")

    # Hugging Face API URL for Mistral-7B
    HF_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

    # Set headers
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    backend_available = True
except Exception as e:
    print(f"Error initializing backend: {e}")
    backend_available = False

def retrieve_context(query, top_k=5):
    """Retrieve relevant posts for a given query"""
    if not backend_available:
        # Return mock data if backend is not available
        return ["Mock context 1 about " + query, "Mock context 2 about " + query]
        
    query_embedding = convert_to_embeddings([query])[0]
    results = qdrant_client.search(
        collection_name="supplements",
        query_vector=query_embedding,
        limit=top_k
    )
    return [res.payload["text"] for res in results]

def query_mistral(prompt):
    """Query the Mistral model hosted on Hugging Face"""
    if not backend_available:
        # Return mock response if backend is not available
        return {"generated_text": f"This is a mock response for: {prompt}"}
        
    data = {"inputs": prompt, "parameters": {"max_new_tokens": 100}}

    response = requests.post(HF_MODEL_URL, json=data, headers=headers)

    print("\n=== API Response ===")
    print(f"Status Code: {response.status_code}\n")

    try:
        json_response = response.json()
        formatted_response = json.dumps(json_response, indent=4)
        print(f"Response:\n{formatted_response}\n")
        return json_response
    except requests.exceptions.JSONDecodeError:
        print(f"Error: Response was not JSON - {response.text}\n")
        return {"error": response.text}

def agent_response(query):
    """Generate a response based on retrieved Reddit discussions"""
    context = retrieve_context(query)
    context_str = "\n".join(context)

    prompt = f"""You are a helpful assistant that provides supplement information based on Reddit discussions.

# User Query:
# ------------
# {query}

# Relevant Information:
# ---------------------
# {context_str}

Response:
---------
Please answer the question using the provided information in a clear and concise manner.
"""

    response = query_mistral(prompt)
    
    if not backend_available:
        # Generate more realistic mock responses for demo purposes
        if "zinc" in query.lower():
            return {
                "generated_text": "Based on Reddit discussions, zinc appears to be beneficial for immune system support. Many users report fewer colds and faster recovery when taking zinc supplements."
            }
        elif "vitamin d" in query.lower():
            return {
                "generated_text": "Reddit discussions show strong support for Vitamin D supplementation, particularly for immune health and mood regulation."
            }
        elif "magnesium" in query.lower():
            return {
                "generated_text": "Magnesium is frequently discussed on Reddit for its benefits for sleep quality, muscle relaxation, and anxiety reduction."
            }
        else:
            return {
                "generated_text": "Based on discussions from Reddit, there isn't enough specific information about this supplement query in our database."
            }
    
    return response
@app.route('/api/supplement-info', methods=['POST'])
def get_supplement_info():
    data = request.json

    if not isinstance(data, dict):  # Ensure data is a dictionary
        return {"error": "Invalid JSON format"}, 400
    
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    response = agent_response(query)
    print("DEBUG: Response from agent_response →", response)  # Debugging
    
    # Ensure response is a list and has at least one element
    if isinstance(response, list) and response:
        answer = response[0].get("generated_text", "No response generated")
    else:
        answer = "No response generated"
    
    # Format response to match frontend expectations
    result = {
        "answer": answer,
        "sources": [f"Source from Reddit: Discussion about {query.split()[0]}"]
    }
    
    return jsonify(result)











if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)