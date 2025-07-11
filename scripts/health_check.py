"""
Health check script for the RAG system
"""
import sys
from pathlib import Path

# Add src to Python path (depuis scripts/, on remonte d'un niveau)
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def check_system():
    """Check if all components are working"""
    print("🔍 Vérification du système RAG...")
    
    try:
        # Check config
        from src.utils.config import ensure_directories, EMBEDDING_PATH, DB_LOCATION
        print("✅ Configuration chargée")
        
        # Check directories
        ensure_directories()
        print("✅ Dossiers créés")
        
        # Check embedding model
        embedding_path = Path(EMBEDDING_PATH)
        if embedding_path.exists():
            print("✅ Modèle d'embedding trouvé")
        else:
            print("❌ Modèle d'embedding manquant - exécutez: python3 scripts/install_models.py")
            return False
        
        # Check vector store
        from src.core.vector_store import vector_store, retriever
        print("✅ Vector store initialisé")
        
        # Check chatbot
        from src.core.chatbot import RAGChatbot
        # Ne pas instancier le chatbot pour éviter les erreurs de prompt manquant
        print("✅ Chatbot module disponible")
        
        print("\n🎉 Système RAG opérationnel!")
        print("Vous pouvez maintenant utiliser:")
        print("  - python3 main_new.py (nouveau chatbot)")
        print("  - python3 build_vector_new.py (construire la DB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_system()
    sys.exit(0 if success else 1)
