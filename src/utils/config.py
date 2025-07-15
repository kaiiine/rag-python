"""
Configuration file for the RAG system
"""
import os
from pathlib import Path

# Base paths - depuis src/utils/, on remonte de 2 niveaux pour atteindre la racine
PROJECT_ROOT = Path(__file__).parent.parent.parent
os.chdir(PROJECT_ROOT)  # S'assurer qu'on travaille depuis la racine

## Installer
EMBEDDING_MODEL_DOWNLOAD="thenlper/gte-small"

## LLM
LLM_MODEL = "mistral:7b-instruct-q4_K_M"
LLM_TEMPERATURE = 0.0
LLM_STREAM=True
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

## Embedding
EMBEDDING_PATH = str(PROJECT_ROOT / "embedding_models" / EMBEDDING_MODEL_DOWNLOAD.split("/")[1])

## Chroma_db
COLLECTION_NAME = "lawyer_courses"
DB_LOCATION = str(PROJECT_ROOT / "storage" / "vector_db")

## Chunk Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 75

## DATA
DATA_FOLDER = str(PROJECT_ROOT / "data")

## Prompt
PROMPT_FILE = str(PROJECT_ROOT / "prompts" / "legal_chatbot_prompt.txt")

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        PROJECT_ROOT / "embedding_models",
        PROJECT_ROOT / "storage" / "vector_db", 
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "prompts",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
