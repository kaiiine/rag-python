from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

dataframe=pd.read_csv("data.csv")
embeddings=OllamaEmbeddings(model="mxbai-embed-large")

db_location="./chrome_langchain_db"
add_documents= not os.path.exists(db_location)

if add_documents:
    documents=[]
    ids=[]
    
    for i, row in dataframe.iterrows():
        document=Document(
            page_content=row["Thématique"] + " " + row["Réglementation"],
            metadata={
                "obligatoire": row["Obligatoire"],
                "source": row["Source"]
            },
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)
        
vector_store=Chroma(
    collection_name="legal_rules",
    persist_directory=db_location,
    embedding_function=embeddings,
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)
    
    retriever=vector_store.as_retriever(
        search_kwargs={
            "k":5
            }
    )
else:
    print("******************************")
    retriever=vector_store.as_retriever(
        search_kwargs={
            "k":5
            }
    )