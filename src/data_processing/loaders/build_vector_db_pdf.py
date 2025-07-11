from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.data_processing.processors.cleaning_text import cleaning
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import uuid

#embeddings = OllamaEmbeddings(model="mxbai-embed-large")
embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-small")

db_location="./chrome_langchain_db"

vector_store = Chroma(
    collection_name="chemistry_courses",
    persist_directory=db_location,
    embedding_function=embeddings,
)

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=75
)

pdf_folder = "./pdf"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

documents = []
cpt=0
for pdf_file in pdf_files:
    doc_path=os.path.join(pdf_folder, pdf_file)
    loader = PyPDFLoader(doc_path)
    pages = loader.load() 
    
    for page in pages:
        chunks=text_splitter.split_documents([page])
        for chunk in chunks:
            cleaned_content = cleaning(chunk.page_content)

            if not cleaned_content:
                continue
                
            chunk.page_content = cleaned_content
            
            chunk.metadata["source_pdf"] = pdf_file
            chunk.metadata["page_number"] = cpt
            chunk.metadata["id"] = str(uuid.uuid4())
            documents.append(chunk)
        cpt+=1

ids = [doc.metadata["id"] for doc in documents]
print(f"Nombre total de documents après nettoyage : {len(documents)}")
print(f"Ajout de {len(documents)} documents nettoyés à la base de données vectorielle...")
vector_store.add_documents(documents=documents, ids=ids)
print("Base de données vectorielle créée avec succès !")