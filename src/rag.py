import os
from typing import Tuple, List

from google import genai
from google.genai import types

from .config import settings
from .schemas import Source
from .embeddings import get_embedding
from .vector_store import vector_store

def generate_answer(question: str, top_k: int) -> Tuple[str, List[Source]]:
    """
    Completes a Retrieval-Augmented Generation request via Google Gemini Cloud.
    It embeds the question, retrieves semantic data, formats a stringent prompt,
    and streams to Google AI Studio.
    """
    # 1. Embed user query
    query_vector = get_embedding(question)

    # 2. Retrieve relevant DocMind context chunks
    results = vector_store.search(query_vector, top_k=top_k)
    
    if not results:
        # Graceful degradation if no index exists or no similarity found
        return "I could not find any relevant documentation to answer your question.", []
    
    # 3. Format Context
    context_text = ""
    sources = []
    
    for res in results:
        context_text += f"---\nSource Document: {res['document']}\nExcerpt:\n{res['text']}\n---\n\n"
        sources.append(Source(
            document=res['document'],
            chunk=res['text'],
            score=round(res['score'], 4)
        ))

    # 4. Construct stringent anti-hallucination Prompt
    system_prompt = (
        "You are DocMind Assistant, an expert AI embedded within the DocMind Cloud SaaS platform documentation. "
        "Your task is to answer user questions purely based on the provided technical documentation context. "
        "CRITICAL RULES:\n"
        "1. Never invent or hallucinate answers. If the information is not present within the provided context, state explicitly that you do not know.\n"
        "2. Do not use outside knowledge.\n"
        "3. Provide direct, professional answers.\n"
        "4. Quote or explicitly reference the exact provided documents when elaborating."
    )
    
    user_prompt = f"Context:\n{context_text}\n\nQuestion: {question}"
    
    # 5. Call Gemini 
    api_key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Code cannot proceed with generation.")

    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model=settings.llm_model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.0
        )
    )
    
    answer = response.text
    
    return answer, sources
