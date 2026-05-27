"""
Configuration file for the RAG system
"""
import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Base paths - depuis src/utils/, on remonte de 2 niveaux pour atteindre la racine
PROJECT_ROOT = Path(__file__).parent.parent.parent
os.chdir(PROJECT_ROOT)  # S'assurer qu'on travaille depuis la racine

## Installer
EMBEDDING_MODEL_DOWNLOAD_OLD="thenlper/gte-small"
EMBEDDING_MODEL_DOWNLOAD="BAAI/bge-m3"
EMBEDDING_MODEL = "BAAI/bge-m3"

## LLM
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.0

## Embedding
EMBEDDING_PATH = str(PROJECT_ROOT / "embedding_models" / EMBEDDING_MODEL_DOWNLOAD.split("/")[1])

## Chroma_db
COLLECTION_NAME = "lawyer_courses"
DB_LOCATION = str(PROJECT_ROOT / "storage" / "vector_db")

## Retriever Settings
SIMILARITY_THRESHOLD = 0.3  

## Chunk Settings
CHUNK_SIZE = 1000 
CHUNK_OVERLAP = 200 

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

@lru_cache(maxsize=1)
def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
    )

@lru_cache(maxsize=1)
def get_embedding() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=DB_LOCATION,
        embedding_function=get_embedding()
    )