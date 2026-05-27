from src.utils.config import PROMPT_FILE, get_llm
from langchain_core.prompts import ChatPromptTemplate
from src.core.vector_store import retriever
from typing import List, Generator
from langchain_core.documents import Document
import sys


class RAGChatbot:

    def __init__(self):
        self.model = get_llm()
        self.prompt_template = self._load_prompt(prompt_file=PROMPT_FILE)
        self.chain = self.prompt_template | self.model

    def _load_prompt(self, prompt_file: str) -> ChatPromptTemplate:
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                template = f.read()
            return ChatPromptTemplate.from_template(template)
        except FileNotFoundError:
            print(f"Error: Prompt file '{prompt_file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading prompt: {e}")
            sys.exit(1)

    def _format_documents(self, documents: List[Document]) -> str:
        if not documents:
            return "AUCUN DOCUMENT PERTINENT TROUVÉ"
        formatted = ""
        for i, doc in enumerate(documents):
            page_num = doc.metadata.get("page_number", doc.metadata.get("entry_index", "N/A"))
            filename = doc.metadata.get("filename") or doc.metadata.get("source_pdf", "Inconnu")
            formatted += f"Document {i+1} (Source: {filename}, Page/Section: {page_num}):\n{doc.page_content}\n\n"
        return formatted

    def retrieve(self, question: str) -> List[Document]:
        """Retrieve relevant documents for a question."""
        try:
            return retriever.invoke(question)
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la récupération des documents: {e}") from e

    def stream(self, question: str, documents: List[Document]) -> Generator[str, None, None]:
        """Stream the LLM response given pre-retrieved documents."""
        formatted = self._format_documents(documents)
        try:
            for chunk in self.chain.stream({"reviews": formatted, "question": question}):
                yield chunk.content
        except Exception as e:
            yield f"Erreur lors de la génération de la réponse: {e}"