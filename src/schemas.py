from pydantic import BaseModel, Field
from typing import List, Optional

class Source(BaseModel):
    document: str = Field(description="The source filename")
    chunk: str = Field(description="The specific text chunk used")
    score: float = Field(description="The distance or similarity score")

class AskRequest(BaseModel):
    question: str = Field(..., description="The user's query about the documentation")
    top_k: int = Field(5, description="Number of context chunks to retrieve", le=20)

class AskResponse(BaseModel):
    answer: str = Field(..., description="The generated LLM answer")
    sources: List[Source] = Field(description="List of supporting documents and excerpts")

class IngestResponse(BaseModel):
    message: str = Field(description="Status message")
    chunks_indexed: int = Field(description="Total chunks processed and stored")
    
class HealthResponse(BaseModel):
    status: str
    version: str
