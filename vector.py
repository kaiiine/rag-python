from config import COLLECTION_NAME, DB_LOCATION, EMBEDDING_PATH
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_PATH)

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embeddings,
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 7}
    )
