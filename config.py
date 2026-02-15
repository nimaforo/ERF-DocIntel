"""
Configuration module for document intelligence project.
Loads environment variables and sets up project-wide constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"
CHAT_HISTORY_DIR = DATA_DIR / "chat_history"
UPLOADS_DIR = PROJECT_ROOT / "uploads"
SUMMARIES_DIR = PROJECT_ROOT / "summaries"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Ensure data directories exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, CHROMA_DB_DIR, CHAT_HISTORY_DIR, UPLOADS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Output Files
CHUNKS_FILE = PROJECT_ROOT / "chunks.json"
EXTRACTION_FILE = PROJECT_ROOT / "extraction.json"
INGESTION_REPORT = PROJECT_ROOT / "ingestion_report.md"
PROMPT_EXPERIMENTS = PROJECT_ROOT / "prompt_experiments.md"

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

# Local Model Configuration (Ollama)
USE_LOCAL_MODEL = os.getenv("USE_LOCAL_MODEL", "true").lower() == "true"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "qwen2.5:latest")

# Model Selection: "openai", "anthropic", or "local"
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "local" if USE_LOCAL_MODEL else "openai")

# Convert 'local' to 'ollama' for agent initialization
def get_llm_provider():
    """Get the LLM provider, converting 'local' to 'ollama'."""
    provider = MODEL_PROVIDER
    if provider == "local":
        return "ollama"
    return provider

# Tesseract Configuration
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")

# LLM Settings
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "2000"))

# Document Processing Settings
SUPPORTED_FORMATS = [".pdf", ".docx"]
OCR_LANGUAGE = "eng"
OCR_DPI = 300

# Chunking Settings
MIN_CHUNK_SIZE = 100  # minimum tokens per chunk
MAX_CHUNK_SIZE = 3000  # maximum tokens per chunk

# Ensure directories exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, SUMMARIES_DIR, PROMPTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
