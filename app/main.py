from fastapi import FastAPI
from app.routes import ingest, query

app = FastAPI(title="AiRA RAG")

app.include_router(ingest.router, prefix="/ingest")
app.include_router(query.router, prefix="/query")
