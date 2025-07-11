"""
Main entry point for the RAG system
"""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main function
try:
    from src.utils.main import main
    
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"Erreur lors du lancement: {e}")
    print("Assurez-vous que tous les modules sont correctement installés.")
    import traceback
    traceback.print_exc()
    sys.exit(1)
