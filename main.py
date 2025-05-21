from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever



model = OllamaLLM(model="llama3.2:latest")
#model=OllamaLLM(model="llama2:7b")

template = """
You're the ebst chemistry teacher ever.

You must answer the following question (in french) **only** using the provided reviews. 
If the answer is not in the reviews, say: "I cannot find this document in the document provided."

Here are the reviews (you have to give the pages where you find information):
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
