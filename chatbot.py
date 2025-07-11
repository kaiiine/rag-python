from config import LLM_MODEL, LLM_TEMPERATURE, LLM_STREAM, PROMPT_FILE
from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from typing import List, Generator
from langchain_core.documents import Document
import sys

class RAGChatbot:

    def __init__(self):
        self.model=OllamaLLM(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            stream=LLM_STREAM
        )
        self.prompt_template=self._load_prompt(prompt_file=PROMPT_FILE)
        self.chain=self.prompt_template | self.model

    def _load_prompt(self, prompt_file:str) -> ChatPromptTemplate:
        try:
            with open(prompt_file, 'r', encoding="utf-8") as f:
                template=f.read()
            return ChatPromptTemplate.from_template(template)
        except FileNotFoundError:
            print(f"Error: Prompt file '{prompt_file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading prompt: {e}")
            sys.exit(1)

    def _retriever_documents(self, question:str):
        try:
            return retriever.invoke(question)
        except Exception as e:
            print(f"Erreur lors de la récupération des documents: {e}")
            return []
        
    def _format_documents(self, documents: List[Document]) -> str:
        if not documents:
            return "Aucun document pertinent trouvé."
        
        formatted_reviews=""
        for i, doc in enumerate(documents):
            page_num=doc.metadata.get('page_number', doc.metadata.get('entry_index', 'N/A'))
            filename=doc.metadata.get('filename', 'Inconnu')
            formatted_reviews+=f"Document {i+1} (Source: {filename}, Page/Section: {page_num}):\n{doc.page_content}\n\n"
        
        return formatted_reviews
    
    def ask_question(self, question:str, show_debug: bool = False) -> Generator[str, None, None]:
       
        if question.lower() == "/debug":
            show_debug= not show_debug
            if show_debug:
                yield "Mode debug activé. Posez votre question."
            else:
                yield "Mode debug désactivé. Posez votre question."
            return

        documents=self._retriever_documents(question)

        if show_debug:
            print(f"DEBUG: {len(documents)} documents trouvés")
            for i, doc in enumerate(documents):
                filename=doc.metadata.get('filename', 'Inconnu')
                preview=doc.page_content[:100].replace('\n',  ' ')
                print(f"Doc {i+1}: {filename} - {preview}...")
            print()

        formatted_reviews=self._format_documents(documents)

        try:
            for chunk in self.chain.stream({
                "reviews": formatted_reviews,
                "question": question
            }):
                yield chunk
        except Exception as e:
            yield f"Erreur lors de la génération de la réponse: {e}"

    def chat_loop(self, show_debug: bool = False):
        print("🤖 Chatbot RAG démarré!")
        print("Tapez 'q' ou 'quit' pour quitter")
        print("Tapez '/debug' pour activer/désactiver le mode debug")

        while True:
            print("\n" + "="*75)
            question=input("❓ Votre question: ").strip()

            if question.lower() in ['q', 'quit', 'exit']:
                print("👋 Au revoir!")
                break

            if not question:
                print("⚠️ Veuillez poser une question.")
                continue
            
            print("🔍 Recherche de documents pertinents...", end="\r" ,flush=True)
            print(" " * 60, end="\r")  
            print("📝 Génération de la réponse...", flush=True)
            try:
                for chunk in self.ask_question(question, show_debug):
                    print(chunk, end='', flush=True)

            except KeyboardInterrupt:
                print("\n⏹️  Opération interrompue par l'utilisateur.")
            except Exception as e:
                print(f"\n❌ Erreur: {e}")