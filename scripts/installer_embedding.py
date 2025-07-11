from src.utils.config import EMBEDDING_MODEL_DOWNLOAD, EMBEDDING_PATH
from sentence_transformers import SentenceTransformer
import os
from os.path import exists

try:
    if not exists(EMBEDDING_PATH):
        os.makedirs(EMBEDDING_PATH)
        save_path = EMBEDDING_PATH

    # Download and save the sentence-transformers model
    model = SentenceTransformer(EMBEDDING_MODEL_DOWNLOAD)
    model.save(save_path)
except Exception as e:
    print(f"Erreur lors du téléchargement du modèle d'embedding: {e}")
    raise e
else:
    print(f"Modèle d'embedding téléchargé et sauvegardé dans {save_path}")
    print("Vous pouvez maintenant utiliser ce modèle pour l'indexation et la recherche de documents.")


def main():
    """Main function for the installer"""
    print("🔧 Installation du modèle d'embedding...")
    # Le code principal est exécuté au niveau du module


if __name__ == "__main__":
    main()