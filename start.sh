#!/bin/bash
# =============================================================================
# SCRIPT D'INITIALISATION RAG - 100% LOCAL
# =============================================================================

echo "🚀 Initialisation du système RAG..."

# 1. Vérifier si les modèles d'embedding existent
if [ ! -d "/app/embedding_models/gte-small" ]; then
    echo "📥 Téléchargement des modèles d'embedding (première fois)..."
    python -m scripts.installer_embedding
else
    echo "✅ Modèles d'embedding déjà présents"
fi

# 2. Vérifier si la base vectorielle existe
if [ ! -f "/app/storage/vector_db/chroma.sqlite3" ]; then
    echo "🔧 Construction de la base de données vectorielle..."
    if [ -n "$(ls -A /app/data 2>/dev/null)" ]; then
        python -m src.data_processing.build_vector
    else
        echo "⚠️  Aucun fichier de données trouvé dans /app/data"
        echo "   Placez vos fichiers PDF/JSON dans le dossier data/"
    fi
else
    echo "✅ Base de données vectorielle déjà construite"
fi

# 3. Lancer l'application principale
echo "🎯 Lancement de l'application RAG..."
exec python main.py
