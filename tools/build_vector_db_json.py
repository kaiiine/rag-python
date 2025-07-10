from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import uuid
import json
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

#embeddings = OllamaEmbeddings(model="mxbai-embed-large")
embeddings=HuggingFaceEmbeddings(model="thenlper/gte-small")
db_location = "./chrome_langchain_db"

vector_store = Chroma(
    collection_name="json_documents",
    persist_directory=db_location,
    embedding_function=embeddings,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

json_folder = "./json"
json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
documents = []
for json_file in json_files:
    file_path = os.path.join(json_folder, json_file)
    
    with open(file_path, "r", encoding="utf-8") as f:
        entries = json.load(f)
        
        if not isinstance(entries, list):
            continue 
        
        for i, entry in enumerate(entries):
            text = entry.get("content", "")
            filename = entry.get("filename", "unknown")

            if not text.strip():
                continue  # skip si vide

            doc = Document(
                page_content=text,
                metadata={
                    "filename": filename,
                    "json_file": json_file,
                    "entry_index": i,
                    "id": str(uuid.uuid4())
                }
            )

            chunks = text_splitter.split_documents([doc])
            for chunk in chunks:
                chunk.metadata["id"] = str(uuid.uuid4())  
                documents.append(chunk)

ids = [doc.metadata["id"] for doc in documents]
vector_store.add_documents(documents=documents, ids=ids)

print("fini")