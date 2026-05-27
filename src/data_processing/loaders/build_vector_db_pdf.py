from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.data_processing.processors.cleaning_text import cleaning
import os
from src.utils.config import get_vector_store, get_embedding
import uuid

#embeddings = OllamaEmbeddings(model="mxbai-embed-large")
embeddings = get_embedding()

vector_store = get_vector_store()

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=75
)

pdf_folder = "./data"
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

BATCH_SIZE = 5000
for i in range(0, len(documents), BATCH_SIZE):
    batch_docs = documents[i:i + BATCH_SIZE]
    batch_ids = ids[i:i + BATCH_SIZE]
    vector_store.add_documents(documents=batch_docs, ids=batch_ids)
    print(f"  Batch {i // BATCH_SIZE + 1} / {-(-len(documents) // BATCH_SIZE)} ajouté ({len(batch_docs)} docs)")

print("Base de données vectorielle créée avec succès !")