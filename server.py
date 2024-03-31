import os
import signal
from threading import Thread

import uvicorn
from fastapi import FastAPI, Request

from search import BM25SearchEngine


app = FastAPI()
search_engine = BM25SearchEngine("document_index.json")


@app.post("/add_document")
async def receive_message(request: Request):
    data = await request.json()
    url = data.get("url", "").strip()
    title = data.get("title", "").strip()
    text = data.get("text", "").strip()

    if not all([url, title, text]):
        return {"status": "error", "message": "All fields must be provided"}

    print(f"Adding document: {url[:50]}")
    search_engine.add_document(url, title, text)
    return {"status": "success"}


@app.get("/search")
def search(query: str):
    query = query.strip()
    if not query:
        return {"status": "error", "message": "Query must be provided"}

    print(f"Searching for: {query}")
    results = search_engine.search(query)
    return {"status": "success", "results": results}


@app.post("/delete_document")
async def delete_document(request: Request):
    data = await request.json()
    url = data.get("url", "").strip()

    if not url:
        raise {"status": "error", "message": "URL must be provided"}

    print(f"Deleting document: {url[:50]}")
    search_engine.delete_documnet(url)
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
