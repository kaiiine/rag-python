from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever



model = OllamaLLM(model="llama3.2:latest")
#model=OllamaLLM(model="llama2:7b")

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
Vous êtes le meilleur professeur de chimie.

Règles à respecter :
1. Réponde **uniquement** à partir des informations figurant dans le CONTEXTE ci-dessous.  
2. Si la réponse n’est pas explicitement dans le contexte, répond exactement :  
   « Je ne trouve pas cette information dans les documents fournis. »
3. Pour chaque fait utilisé, **cite la (ou les) page(s)** entre parenthèses, p. ex. : (p. 12) ou (p. 12, 15).
4. Rédige la réponse en français, dans un style clair, pédagogique et concis.

──────────────── CONTEXTE ────────────────
{reviews}
───────────────────────────────────────────

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

    result=chain.invoke({"reviews":reviews, "question": question})
    print(result)
