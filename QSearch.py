import os
import requests
import json
from langchain.schema import SystemMessage, HumanMessage
from backend.embeddings import convert_to_embeddings
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Initialize Qdrant Client
qdrant_client = QdrantClient(
    url="https://9b7c1600-4f16-4ab5-a09a-e04ecaf893ad.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key=os.getenv("QDRANT_API_KEY")  # Store API key in .env file for security
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

def retrieve_context(query, top_k=5):
    """Retrieve relevant posts for a given query"""
    query_embedding = convert_to_embeddings([query])[0]
    results = qdrant_client.search(
        collection_name="supplements",
        query_vector=query_embedding,
        limit=top_k
    )
    return [res.payload["text"] for res in results]

def query_mistral(prompt):
    """Query the Mistral model hosted on Hugging Face"""
    data = {"inputs": prompt, "parameters": {"max_new_tokens": 100}}

    response = requests.post(HF_MODEL_URL, json=data, headers=headers)

    print("\n=== API Response ===")
    print(f"Status Code: {response.status_code}\n")

    try:
        json_response = response.json()
        formatted_response = json.dumps(json_response, indent=4)  # Pretty print JSON response
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



Response:
---------
Please answer the question using the provided information in a clear and concise manner.
"""

    return query_mistral(prompt)

if __name__ == "__main__":
    user_query = "Is zinc good for the immune system?"
    response = agent_response(user_query)

    print("\n=== Final Agent Response ===\n")
    if "generated_text" in response:
        print(response["generated_text"])
    else:
        print("Error: No valid response received.")



















# User Query:
# ------------
# {query}

# Relevant Information:
# ---------------------
# {context_str}