# aegismind/config/settings.py
"""
Global configuration for AegisMind
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment"""
    
    # API Keys
    groq_api_key: str
    
    # Model Configuration
    groq_model: str = "llama-3.3-70b-versatile"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # RAG Settings
    chunk_size: int = 500
    chunk_overlap: int = 50
    retrieval_k: int = 3
    
    # Memory Settings
    memory_db_path: str = "data/memory.db"
    max_short_term_messages: int = 10
    
    # Paths
    data_dir: Path = Path("data")
    documents_dir: Path = Path("data/documents")
    embeddings_dir: Path = Path("data/embeddings")
    
    # Agent Configuration
    max_agent_iterations: int = 5
    agent_timeout: int = 30
    
    # Voice Settings (Optional)
    enable_voice: bool = False
    whisper_model: str = "base"
    tts_model: str = "tts_models/en/ljspeech/tacotron2-DDC"
    
    # MCP Settings (Optional)
    enable_mcp: bool = False
    mcp_server_url: Optional[str] = None
    
    class Config:
        env_file = ".env"  # tells to read from .env file 
        
        env_file_encoding = "utf-8"

# Create directories
def init_directories(settings: Settings):
    """Initialize required directories"""
    settings.data_dir.mkdir(exist_ok=True)
    settings.documents_dir.mkdir(exist_ok=True)
    settings.embeddings_dir.mkdir(exist_ok=True)

# Singleton instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get or create settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
        init_directories(_settings)
    return _settings