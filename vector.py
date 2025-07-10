from config import COLLECTION_NAME, DB_LOCATION, EMBEDDING_MODEL
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

#embeddings = OllamaEmbeddings(model="mxbai-embed-large")
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embeddings,
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 7}
    )
