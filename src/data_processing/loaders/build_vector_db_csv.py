from langchain_core.documents import Document
import pandas as pd
from src.utils.config import get_vector_store
import uuid

dataframe=pd.read_csv("../csv/data.csv")

vector_store=get_vector_store()




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
    


BATCH_SIZE = 5000
for i in range(0, len(documents), BATCH_SIZE):
    vector_store.add_documents(documents=documents[i:i + BATCH_SIZE], ids=ids[i:i + BATCH_SIZE])

retriever=vector_store.as_retriever(
    search_kwargs={
        "k":5
        }
)
