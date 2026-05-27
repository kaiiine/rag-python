from src.utils.config import EMBEDDING_MODEL_DOWNLOAD, EMBEDDING_PATH
from sentence_transformers import SentenceTransformer
import os
from os.path import exists

try:
    print(f"🔧 Téléchargement du modèle: {EMBEDDING_MODEL_DOWNLOAD}")
    print(f"📁 Dossier de destination: {EMBEDDING_PATH}")
    
    # Créer le dossier parent si nécessaire
    parent_dir = os.path.dirname(EMBEDDING_PATH)
    if not exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
        print(f"📁 Dossier créé: {parent_dir}")
    
    # Télécharger et sauvegarder le modèle
    model = SentenceTransformer(EMBEDDING_MODEL_DOWNLOAD)
    model.save(EMBEDDING_PATH)
    
    print(f"✅ Modèle sauvegardé dans: {EMBEDDING_PATH}")
    
except Exception as e:
    print(f"❌ Erreur lors du téléchargement du modèle d'embedding: {e}")
    raise e


def main():
    """Main function for the installer"""
    print("🔧 Installation du modèle d'embedding...")
    # Le code principal est exécuté au niveau du module


if __name__ == "__main__":
    main()