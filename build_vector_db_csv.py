from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader 
import uuid

dataframe=pd.read_csv("csv/data.csv")
embeddings=OllamaEmbeddings(model="mxbai-embed-large")

db_location="./chrome_langchain_db"

vector_store=Chroma(
    collection_name="legal_rules",
    persist_directory=db_location,
    embedding_function=embeddings,
)




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
    


vector_store.add_documents(documents=documents, ids=ids)

retriever=vector_store.as_retriever(
    search_kwargs={
        "k":5
        }
)
