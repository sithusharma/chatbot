import os
import openai
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Connect to the existing index
index = pc.Index("hr-docs")

def embed_text(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def retrieve_best_matches(query):
    query_embedding = embed_text(query)
    results = index.query(vector=query_embedding, top_k=5, include_metadata=True)

    matched_chunks = [match['metadata']['text'] for match in results['matches']]

    # Combine chunks into a coherent response using a prompt
    response = generate_polished_response(query, matched_chunks)
    return response

def generate_polished_response(query, chunks):
    combined_context = "\n".join(chunks)

    prompt = f"""
    You are an HR assistant. Answer the following query using the context provided from the HR documents.
    Query: {query}

    Context:
    {combined_context}

    Provide a clear, friendly, and professional response based on this information.
    """

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful HR assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion['choices'][0]['message']['content'].strip()