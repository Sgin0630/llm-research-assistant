from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.generation.llm_chain import HEPAssistant

app = FastAPI(title="HEP arXiv Assistant API", version="1.0.0")

# Shared assistant instance (retriever injected at startup in production)
_assistant = HEPAssistant()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")
    answer, sources = _assistant.chat(request.query, top_k=request.top_k)
    return QueryResponse(answer=answer, sources=sources)


@app.post("/ingest")
def ingest():
    """Trigger arXiv paper harvesting and index building (placeholder)."""
    return {"status": "ingestion triggered", "message": "Run the harvester manually via src/ingest/arxiv_harvester.py"}
