import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API configuration
    api_title: str = "DocMind API"
    api_version: str = "1.0.0"
    
    # Environment limits
    max_top_k: int = 10
    
    # RAG Settings
    chunk_size: int = 600
    chunk_overlap: int = 100
    
    # LLM & Google Gemini
    gemini_api_key: str = ""
    llm_model: str = "gemini-2.5-flash"
    
    # Sentence Transformers config
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Directory paths
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir: str = os.path.join(base_dir, "docs")

    class Config:
        env_file = ".env"

# Initialize global settings
settings = Settings()
