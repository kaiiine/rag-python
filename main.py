from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are a legal assistant specialized in Junior-Enterprises.

You must answer the following question **only** using the provided reviews. 
If the answer is not in the reviews, say: "Je ne trouve pas cette information dans les documents fournis."

Here are the reviews:
{reviews}

Question:
{question}
"""


prompt=ChatPromptTemplate.from_template(template)
chain=prompt | model

while True:
    print("\n\n------------------------------------------")
    question=input("Enter your question (q to quit): ")
    if question == "q":
        break
    
    reviews=retriever.invoke(question)

    result=chain.invoke({"reviews":reviews, "question": question})
    print(result)
