from config import LLM_MODEL, LLM_TEMPERATURE, LLM_STREAM
from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever


model = OllamaLLM(model=LLM_MODEL, temperature=LLM_TEMPERATURE, stream=LLM_STREAM)

# Loading the prompt template
with open("prompt.txt", "r", encoding="utf-8") as f:
    template = f.read()

prompt=ChatPromptTemplate.from_template(template)
chain=prompt | model

while True:
    print("\n\n------------------------------------------")
    question=input("Enter your question (q to quit): ")
    if question == "q":
        break
    
    reviews=retriever.invoke(question)

    # Formater les documents pour le prompt pour qu'ils comprenne tmieux
    formatted_reviews = ""
    for i, doc in enumerate(reviews):
        page_num = doc.metadata.get('page_number', 'N/A')
        formatted_reviews += f"Document {i+1} (page {page_num}):\n{doc.page_content}\n\n"

    #results=chain.invoke({"reviews":formatted_reviews, "question": question})
    for chunk in chain.stream({"reviews": formatted_reviews, "question": question}):
        print(chunk, end="", flush=True)
