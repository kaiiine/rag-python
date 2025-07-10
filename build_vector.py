from config import EMBEDDING_MODEL, DB_LOCATION, COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP, DATA_FOLDER
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tools.files_vector import json_type
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
import os


embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embeddings
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

data=[f for f in os.listdir(DATA_FOLDER)] 
documents=[]
for data_file in data:
    file_path=os.path.join(DATA_FOLDER, data_file)
    match file_path:
        case f if f.endswith(".json"):
            chunk=json_type(file_path)
            if chunk:
                documents.extend(chunk)


ids=[doc.metadata["id"] for doc in documents]
print(f"Nombre total de documents après nettoyage : {len(documents)}")
print(f"Ajout de {len(documents)} documents nettoyés à la base de données vectorielle...")
vector_store.add_documents(documents=documents, ids=ids)