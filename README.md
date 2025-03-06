# HR Document Chatbot - Demo Version

**Demo Link:** [https://chatbot-tn7i4fo8guhxz29aazflim.streamlit.app](https://chatbot-tn7i4fo8guhxz29aazflim.streamlit.app)

---

## About This Repo

This repo contains a **demo version** of a chatbot that can answer HR questions by searching through HR documents.

### Important Note
This is **not the original code** used in the actual project for the company.  
The real project used **different technologies** and followed **company security rules**, so that code cannot be shared.  
This demo just shows the **basic idea** using open-source tools.

---

## What This Demo Does

1. Reads HR documents (PDF files).
2. Splits each document into smaller parts (chunks).
3. Creates a **vector embedding** for each chunk using **Azure OpenAI**.
4. Stores those embeddings into **Pinecone**.
5. When you ask a question, the question is also converted into an embedding.
6. The system searches for the most relevant document chunks and returns the answer.

---

## Tech Stack for This Demo

| Layer       | Technology      |
|-------------|------------------|
| Frontend    | Streamlit       |
| Backend     | FastAPI         |
| Embeddings  | Azure OpenAI    |
| Vector DB   | Pinecone        |

---

## How to Run the Demo

1. Put HR PDFs into `data/hr_documents`.
2. Add your `PINECONE_API_KEY` and `OPENAI_API_KEY` into `.env`.
3. Run this to process the documents:
    ```bash
    python embedding_service.py
    ```
4. Start the backend:
    ```bash
    uvicorn app:app --reload
    ```
5. Start the frontend:
    ```bash
    streamlit run app.py
    ```

---

## Original Project (Company Version)

The real system built for the company was much more advanced. It used:

- **Azure CosmosDB** for secure document storage.
- **Azure Cognitive Search** for search functionality.
- **Azure OpenAI** for embeddings.
- **Azure Language Studio** for language processing.
- **Microsoft Bot Framework SDK** for chatbot logic.
- **Node.js** for backend services.

That code is private and cannot be shared because it belongs to the company.

---

## Example Question

If you ask:  
> "What is the sick leave policy?"

The chatbot will search the HR documents and try to find the best answer based on the documents it was given.

---

This demo is just to show the general concept, using open tools so anyone can run it.  
It does **not represent the full system** used at the company.

