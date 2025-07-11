# config.py

## Installer
EMBEDDING_MODEL_DOWNLOAD="thenlper/gte-small"

## LLM
LLM_MODEL = "mistral:7b-instruct-q4_K_M"
LLM_TEMPERATURE = 0.0
LLM_STREAM=True

## Embedding
EMBEDDING_PATH = "./embedding_models/" + EMBEDDING_MODEL_DOWNLOAD.split("/")[1]

## Chroma_db
COLLECTION_NAME = "lawyer_courses"
DB_LOCATION = "./chrome_langchain_db"

## Chunk Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 75

## DATA
DATA_FOLDER="./data"

## Prompt
PROMPT_FILE = "./prompts/legal_chatbot_prompt.txt"
