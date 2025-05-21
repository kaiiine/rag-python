from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import uuid

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location="./chrome_langchain_db"

vector_store = Chroma(
    collection_name="chemistry_courses",
    persist_directory=db_location,
    embedding_function=embeddings,
)

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

pdf_folder = "./pdfs"
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
            chunk.metadata["source_pdf"] = pdf_file
            chunk.metadata["page_number"] = cpt
            chunk.metadata["id"] = str(uuid.uuid4())
            documents.append(chunk)
        cpt+=1

ids = [doc.metadata["id"] for doc in documents]
vector_store.add_documents(documents=documents, ids=ids)