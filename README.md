# HR Document Chatbot

This project is a full example of building a chatbot that can answer HR questions by searching across uploaded HR documents. It works by:

1. Reading HR documents (PDFs)
2. Splitting them into smaller text chunks
3. Creating embeddings for each chunk using Azure OpenAI
4. Storing those embeddings in Pinecone
5. When a user asks a question, the query is embedded and matched against the document embeddings

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- Embeddings: Azure OpenAI
- Vector Database: Pinecone

## Setup
1. Place PDFs into `data/hr_documents`
2. Set `PINECONE_API_KEY` and `OPENAI_API_KEY` as environment variables
3. Run preprocessing: `python embedding_service.py`
4. Start backend: `uvicorn app:app --reload`
5. Start frontend: `streamlit run app.py`

## Example
Ask: "What is the leave policy?"
The chatbot will search the HR documents for relevant answers.