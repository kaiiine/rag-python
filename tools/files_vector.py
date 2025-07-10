from config import CHUNK_SIZE, CHUNK_OVERLAP
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tools.cleaning_text import cleaning
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
import json
import os
import uuid


def json_type(file_path):
    """
    Remplie chromadb avec des fichiers JSON
    """
    text_splitter= RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    with open(file_path, "r", encoding="utf-8") as f:
        entries=json.load(f)
        if not isinstance(entries, list):  
            return []
        all_chunks=[]
        for i, entry in enumerate(entries):
            text=entry.get("content", "")
            filename=entry.get("filename", "unknown")

            clean_text=cleaning(text)

            if not clean_text.strip():
                continue 

            doc=Document(
                page_content=clean_text,
                metadata={
                    "filename": filename,
                    "json_file": os.path.basename(file_path),
                    "entry_index": i,
                    "id": str(uuid.uuid4())
                }
            )
            chunk=text_splitter.split_documents([doc])
            for chunks in chunk:
                chunks.metadata["id"]=str(uuid.uuid4())
            all_chunks.extend(chunk)  
        return all_chunks  
            