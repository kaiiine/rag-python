from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import uuid
import re

#embeddings = OllamaEmbeddings(model="mxbai-embed-large")
embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-small")

def clean_text(text):
    """
    Nettoie le texte extrait du PDF pour améliorer la qualité des embeddings
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Supprimer les caractères de contrôle et les caractères non imprimables
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Normaliser les espaces multiples en un seul espace
    text = re.sub(r'\s+', ' ', text)
    
    # Supprimer les tirets de césure en fin de ligne
    text = re.sub(r'-\s*\n\s*', '', text)
    
    # Supprimer les sauts de ligne multiples
    text = re.sub(r'\n\s*\n', '\n', text)
    if re.match(r'^\s*\d+\s*$', text.strip()):
        return ""
    
    # Supprimer les en-têtes et pieds de page récurrents (ajustable selon vos PDFs)
    text = re.sub(r'^\s*page\s+\d+.*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Supprimer les URLs et emails pour éviter le bruit
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    
    # Nettoyer les caractères spéciaux répétés
    text = re.sub(r'[^\w\s\.,;:!?()[\]{}"\'-]+', ' ', text)
    
    # Supprimer les espaces en début et fin
    text = text.strip()
    
    # Retourner vide si le texte est trop court après nettoyage
    if len(text) < 10:
        return ""
    
    return text

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
            # Nettoyer le contenu du chunk
            cleaned_content = clean_text(chunk.page_content)
            
            # Ignorer les chunks vides après nettoyage
            if not cleaned_content:
                continue
                
            # Mettre à jour le contenu du chunk avec le texte nettoyé
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