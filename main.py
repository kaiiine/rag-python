"""
Main entry point for the RAG system
"""
import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


if __name__ == "__main__":
    try:
        # Vérifie si on est dans un environnement interactif
        if sys.stdin.isatty():
            from src.utils.main import main
            print("Mode interactif détecté, lancement du chatbot...")
            main()
        else:
            print("Mode non-interactif : serveur en attente...")
            # Dans un conteneur, on peut attendre indéfiniment ou servir une API
            import time
            while True:
                print("🤖 RAG Server running... (Press Ctrl+C to stop)")
                time.sleep(60)
    except KeyboardInterrupt:
        print("\n👋 Programme interrompu. Au revoir!")
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        print("Assurez-vous que tous les modules sont correctement installés.")
        import traceback
        traceback.print_exc()
        sys.exit(1)
