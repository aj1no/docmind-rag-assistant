from .chunking import load_and_chunk_documents
from .embeddings import get_embeddings
from .vector_store import vector_store

def run_ingestion() -> int:
    """
    Executes the comprehensive pipeline to read markdown files, split them into chunks,
    generate vector embeddings, and save the resulting FAISS index to disk.
    Returns the total number of ingested chunk nodes.
    """
    # 1. Parse and chunk Markdown files
    chunks = load_and_chunk_documents()
    if not chunks:
        return 0

    # 2. Re-initialize vector store index (start fresh for simplicity of this RAG iteration)
    vector_store.init_index()

    # 3. Generate embeddings mapped to string texts
    texts = [c["text"] for c in chunks]
    embeddings = get_embeddings(texts)

    # 4. Insert vectors alongside metadata into FAISS
    vector_store.add_embeddings(embeddings, chunks)

    # 5. Persist index
    vector_store.save()

    return len(chunks)
