# API Reference

The DocMind API is organized around REST, uses standard HTTP verbs, and returns JSON-encoded responses.

## Base URL
All API requests must be routed to:
`https://api.docmind.cloud/v1`

---

## Health Check
Check the operational status of the DocMind API.

**GET** `/health`

*Response (200 OK)*
```json
{
  "status": "operational",
  "version": "1.0.4"
}
```

---

## Ingest Documents
Triggers an asynchronous pipeline to read all newly uploaded documents and insert them into the Vector index.

**POST** `/ingest`

*Response (202 Accepted)*
```json
{
  "message": "Ingestion started.",
  "job_id": "job_998877"
}
```

---

## RAG Query (Ask)
Perform a Retrieval-Augmented Generation request. Provide a natural language question, and the API will return an LLM-generated answer strictly scoped to your documentation.

**POST** `/ask`
*Request Body*
```json
{
  "question": "How do I create a new API key?",
  "top_k": 5
}
```

*Response (200 OK)*
```json
{
  "answer": "To create a new API key, log into the DocMind Cloud Dashboard, navigate to Developers > API Keys, and generate a new Secret Key.",
  "sources": [
    {
      "document": "authentication.md",
      "chunk": "To get started, you will need a secret API key. \n1. Log in to your DocMind Cloud Dashboard.\n2. Navigate to Developers > API Keys...",
      "score": 0.89
    }
  ]
}
```
