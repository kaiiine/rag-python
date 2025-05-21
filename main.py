from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import time


model = OllamaLLM(model="llama3.2:latest", temperature=0.0, stream=True)
#model=OllamaLLM(model="llama2:7b")
#model=OllamaLLM(model="mistral:latest", temperature=0.0, stream=True)

old_template = """
You're the best chemistry teacher ever.

You must answer the following question (in french) **only** using the provided reviews. 
If the answer is not in the reviews, say: "I cannot find this document in the document provided."

Here are the reviews (you have to give the page number where you find information):
{reviews}

Question:
{question}
"""

template = """
Vous êtes un professeur de chimie très rigoureux. Vous ne devez répondre que si l'information est **STRICTEMENT présente dans le CONTEXTE**.

Règles impératives :
1. Citez toujours les numéros de page entre parenthèses (p. 2) pour chaque élément cité.
2. Utilisez uniquement les informations ci-dessous (CONTEXT).
3. Ne faites AUCUNE supposition ou déduction hors contexte.
4. Si l'information n'est pas clairement écrite dans le contexte, répondez uniquement :  
   « Je ne trouve pas cette information dans les documents fournis. »
5. Écrivez en français clair, détailé et pédagogique.

──────────── CONTEXTE ────────────
{reviews}
──────────────────────────────────

Question :
{question}

Réponse :

"""


prompt=ChatPromptTemplate.from_template(template)
chain=prompt | model

while True:
    print("\n\n------------------------------------------")
    question=input("Enter your question (q to quit): ")
    if question == "q":
        break
    
    reviews=retriever.invoke(question)

    results=chain.invoke({"reviews":reviews, "question": question})
    for result in results:
        print(result, end="", flush=True)
        time.sleep(0.02) 
