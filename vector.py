from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

vector_store = Chroma(
    collection_name="chemistry_courses",
    persist_directory="./chrome_langchain_db",
    embedding_function=embeddings,
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
    )
