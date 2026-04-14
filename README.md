# DocMind — AI Documentation Assistant (RAG)

DocMind Cloud is a fictional SaaS platform providing robust internal documentation management, semantic index building, and AI-driven answering. This repository implements the **Retrieval-Augmented Generation (RAG)** backend powering DocMind Cloud.

## The Problem
Technical documentation scales poorly. When internal wikis or developer docs exceed a certain size, traditional keyword search becomes a bottleneck. Engineers and support staff waste time scanning through lengthy pages. 

DocMind solves this by utilizing vector embeddings to understand the *semantics* of the query, retrieving exactly what is relevant, and utilizing an LLM to synthesize an immediate, strictly context-scoped answer.

## Stripe Inspiration
The documentation schema located within `docs/` is heavily inspired by Stripe's approach to API documentation—separated cleanly by concept (Authentication, Billing, Workspaces, etc.), emphasizing clarity, strict limits, and developer-friendly examples. It mirrors how a true enterprise SaaS handles user-facing documentation.

## RAG Architecture
1. **Ingestion**: Parses Markdown files from `docs/`.
2. **Chunking**: Splits text into 400–800 token boundary subsets while preserving metadata.
3. **Embeddings**: Utilizes the local, lightweight `sentence-transformers` model (`all-MiniLM-L6-v2`) to convert text into high-dimensional vectors.
4. **Vector Store**: Rebuilds a local, in-memory `FAISS` index for instantaneous semantic similarity matching.
5. **Generation**: Dispatches an API call to **Google Vertex AI / AI Studio (`gemini-2.5-flash`)**. The system prompt is engineered to *prevent hallucination* by strictly binding the LLM to the retrieved chunks, ensuring it cites documents appropriately.

## Technologies Used
- **Python**: Core Language
- **FastAPI / Uvicorn**: High-performance REST interface
- **FAISS**: Local Vector Storage Engine
- **Sentence-Transformers**: Open-source Embedding models
- **Google Gemini SDK**: For generation (`gemini-2.5-flash`)
- **Vanilla JS/HTML/CSS**: Highly customized, responsive single page application frontend with Glassmorphism UI.
- **Tiktoken**: Precise token counting

## How to Run

1. **Clone & Setup Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
    pip install -r requirements.txt
    ```

2. **Configure Variables**
    Copy `.env.example` to `.env` and insert your API keys:
    ```bash
    cp .env.example .env
    # Edit .env and supply your GEMINI_API_KEY
    ```

3. **Start the API Server**
    ```bash
    uvicorn src.main:app --reload
    ```
    The server will boot up at `http://localhost:8000`.

## Real World Examples

### Step 1: Ingest the documentation
Index the provided document base so the Vector store learns the data.

```bash
curl -X POST http://localhost:8000/ingest
```

### Step 2: Ask a Question
Query the RAG pipeline about DocMind's billing limits.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What happens if I downgrade my plan and have too many documents?",
    "top_k": 3
  }'
```

**Expected Response**:
```json
{
  "answer": "If you downgrade from Pro to Developer and your workspace already exceeds the 50 document limit, your API access will be restricted to read-only until you delete the excess data.",
  "sources": [
    {
      "document": "billing.md",
      "chunk": "Note: If you downgrade from Pro to Developer and your workspace already exceeds the 50 document limit, your API access will be restricted to read-only until you delete excess data.",
      "score": 1.09
    }
  ]
}
```
