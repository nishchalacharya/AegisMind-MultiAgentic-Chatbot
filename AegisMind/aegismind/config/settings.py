# config/settings.py
"""
Global configuration for AegisMind
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment"""
    
    # API Keys
    groq_api_key: str = Field(..., description="Groq API key")
    
    # Model Configuration
    groq_model: str = Field(
        default="llama-3.3-70b-versatile",
        description="Groq model to use"
    )
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model"
    )
    
    # RAG Settings
    chunk_size: int = Field(default=500, description="Text chunk size")
    chunk_overlap: int = Field(default=50, description="Chunk overlap")
    retrieval_k: int = Field(default=3, description="Number of chunks to retrieve")
    
    # Memory Settings
    memory_db_path: str = Field(
        default="data/memory.db",
        description="Path to memory database"
    )
    max_short_term_messages: int = Field(
        default=10,
        description="Max messages in short-term memory"
    )
    
    # Paths
    data_dir: Path = Field(default=Path("data"), description="Data directory")
    documents_dir: Path = Field(
        default=Path("data/documents"),
        description="Documents directory"
    )
    embeddings_dir: Path = Field(
        default=Path("data/embeddings"),
        description="Embeddings directory"
    )
    
    # Agent Configuration
    max_agent_iterations: int = Field(
        default=5,
        description="Max agent iterations"
    )
    agent_timeout: int = Field(default=30, description="Agent timeout in seconds")
    
    # Voice Settings (Optional)
    enable_voice: bool = Field(default=False, description="Enable voice features")
    whisper_model: str = Field(default="base", description="Whisper model size")
    
    # MCP Settings (Optional)
    enable_mcp: bool = Field(default=False, description="Enable MCP tools")
    mcp_server_url: Optional[str] = Field(
        default=None,
        description="MCP server URL"
    )
    
    # New style configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

# Create directories
def init_directories(settings: Settings):
    """Initialize required directories"""
    settings.data_dir.mkdir(exist_ok=True)
    settings.documents_dir.mkdir(exist_ok=True, parents=True)
    settings.embeddings_dir.mkdir(exist_ok=True, parents=True)

# Singleton instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get or create settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
        init_directories(_settings)
    return _settings