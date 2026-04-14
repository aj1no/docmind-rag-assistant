from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .schemas import AskRequest, AskResponse, IngestResponse, HealthResponse
from .vector_store import vector_store
from .ingest import run_ingestion
from .rag import generate_answer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Attempt to load existing vector index on boot
    loaded = vector_store.load_if_exists()
    if loaded:
        print(f"Loaded existing FAISS index with {vector_store.index.ntotal} vectors.")
    else:
        print("No FAISS index found. Please hit /ingest to build the Vector store.")
        vector_store.init_index()
    yield

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="DocMind Cloud backend API supporting semantic RAG.",
    lifespan=lifespan
)

# Standard permissive CORS rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="operational",
        version=settings.api_version
    )

@app.post("/ingest", response_model=IngestResponse)
def ingest_documents():
    """
    Kicks off the process of parsing documents, chunking, embedding, and indexing.
    Note: In a true production environment, this should be executed asynchronously via a task queue (like Celery).
    """
    try:
        total_indexed = run_ingestion()
        return IngestResponse(
            message="Ingestion completed successfully.",
            chunks_indexed=total_indexed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """
    Accepts a natural language question and optionally overrides top_k context limits.
    Returns the AI generated answer along with rigorously tracked sources.
    """
    # Enforce safe upper bound on top_k
    top_k = min(request.top_k, settings.max_top_k)
    
    try:
        answer, sources = generate_answer(request.question, top_k)
        return AskResponse(
            answer=answer,
            sources=sources
        )
    except ValueError as ve:
        # Expected value errors (e.g., Missing API key)
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
