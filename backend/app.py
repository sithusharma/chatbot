from fastapi import FastAPI, Query
from retrieval_service import retrieve_best_matches

app = FastAPI()

@app.get("/search")
def search_hr(query: str):
    results = retrieve_best_matches(query)
    return {"matches": results}