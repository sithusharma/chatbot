import os
import json
import fitz  # PyMuPDF
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import openai

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("❌ Missing API keys. Check your .env file.")

# Set OpenAI key
openai.api_key = OPENAI_API_KEY

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Index name and expected dimension
INDEX_NAME = "hr-docs"
EMBEDDING_DIMENSION = 1536

# Always recreate index to ensure correct config
existing_indexes = [index.name for index in pc.list_indexes()]

if INDEX_NAME in existing_indexes:
    print(f"🔄 Deleting existing index '{INDEX_NAME}' to ensure correct config...")
    pc.delete_index(INDEX_NAME)

print(f"✅ Creating index '{INDEX_NAME}' with dimension={EMBEDDING_DIMENSION}")
pc.create_index(
    name=INDEX_NAME,
    dimension=EMBEDDING_DIMENSION,
    metric='cosine',
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)

# Connect to the new index
index = pc.Index(INDEX_NAME)

def embed_text(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response['data'][0]['embedding']

    if len(embedding) != EMBEDDING_DIMENSION:
        raise ValueError(f"❌ Embedding dimension mismatch: expected {EMBEDDING_DIMENSION}, got {len(embedding)}")

    return embedding

def preprocess_and_store():
    chunks = []

    # Locate HR documents folder
    documents_dir = os.path.join(os.path.dirname(__file__), "../data/hr_documents")
    print(f"📂 Looking for HR documents in: {os.path.abspath(documents_dir)}")

    if not os.path.exists(documents_dir):
        raise FileNotFoundError(f"❌ Folder not found: {documents_dir}")

    files = [f for f in os.listdir(documents_dir) if f.endswith(".pdf")]

    if not files:
        raise FileNotFoundError(f"❌ No PDFs found in: {documents_dir}")

    for file_name in files:
        print(f"📄 Processing file: {file_name}")
        with fitz.open(os.path.join(documents_dir, file_name)) as doc:
            full_text = "".join(page.get_text() for page in doc)

            # Chunk the text into 500-character pieces
            for i in range(0, len(full_text), 500):
                chunk_text = full_text[i:i+500]
                embedding = embed_text(chunk_text)

                chunks.append({
                    "id": f"{file_name}-chunk-{i//500}",
                    "values": embedding,
                    "metadata": {"text": chunk_text}
                })

    # Save locally (optional for debugging)
    processed_path = os.path.join(os.path.dirname(__file__), "../data/processed_chunks.json")
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    # Upload to Pinecone
    print(f"⬆️ Uploading {len(chunks)} chunks to Pinecone...")
    index.upsert(vectors=chunks)
    print("✅ Upload complete.")

if __name__ == "__main__":
    preprocess_and_store()
