# config.py


## LLM
LLM_MODEL = "mistral:7b-instruct-q4_K_M"
LLM_TEMPERATURE = 0.0
LLM_STREAM=True

## Chroma_db
COLLECTION_NAME = "lawyer_courses"
DB_LOCATION = "./chrome_langchain_db"
EMBEDDING_MODEL = "./embedding_model/gte-small"

## Folders
PDF_FOLDER=".pdf"
JSON_FOLDER="./json"
CSV_FOLDER="./csv"
DATA_FOLDER="./data"

## Chunk Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 75

