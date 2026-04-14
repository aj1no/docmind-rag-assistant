import os
import glob
import tiktoken
from typing import List, Dict, Any
from .config import settings

def count_tokens(text: str) -> int:
    """Helper to accurately count tokens for the given text."""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except Exception:
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    return len(encoding.encode(text))

def chunk_text(text: str, document_name: str, max_tokens: int = settings.chunk_size) -> List[Dict[str, Any]]:
    """
    Splits text into conceptual chunks based on a maximum token boundary.
    We split initially by paragraph (double newline) to preserve context boundaries.
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        # Prevent oversized single paragraphs from breaking the counting constraint by splitting them further if needed
        # (For this example, we assume paragraphs fit the token limit, which is safe for our markdown)
        tokens_para = count_tokens(para)
        if count_tokens(current_chunk) + tokens_para > max_tokens and current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": {"document": document_name}
            })
            current_chunk = para + "\n\n"
        else:
            current_chunk += para + "\n\n"
            
    if current_chunk.strip():
        chunks.append({
            "text": current_chunk.strip(),
            "metadata": {"document": document_name}
        })
        
    return chunks

def load_and_chunk_documents() -> List[Dict[str, Any]]:
    """
    Reads all markdown files in the configured docs directory and chunks them.
    Returns a unified list of chunk dictionaries.
    """
    docs_path = os.path.join(settings.docs_dir, "*.md")
    all_chunks = []
    
    for file_path in glob.glob(docs_path):
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Append document text into manageable chunks attached with metadata
            doc_chunks = chunk_text(content, document_name=filename)
            # Hydrate text inside metadata for simplified downstream storage in vector store mapping
            for chunk in doc_chunks:
                chunk["metadata"]["text"] = chunk["text"]
            all_chunks.extend(doc_chunks)
            
    return all_chunks
