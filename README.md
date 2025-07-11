# RAG Python - Système de Chatbot RAG

Un système de chatbot intelligent utilisant la technologie RAG (Retrieval Augmented Generation) avec Langchain, ChromaDB et des modèles d'embedding modernes.

## 🎯 Fonctionnalités

- **Chatbot conversationnel** avec recherche sémantique dans vos documents
- **Support multi-formats** : JSON, PDF, CSV
- **Embedding moderne** avec thenlper/gte-small
- **Interface en streaming** pour des réponses en temps réel
- **Mode debug** pour analyser les documents récupérés
- **Architecture modulaire** et extensible

## 🏗️ Architecture

```
rag-python/
├── src/                              # Code source principal
│   ├── core/                         # Logique métier
│   │   ├── chatbot.py               # Chatbot RAG principal
│   │   └── vector_store.py          # Gestion base vectorielle
│   ├── data_processing/             # Traitement des données
│   │   ├── loaders/                 # Chargeurs de fichiers
│   │   │   ├── files_vector.py      # Chargeur JSON
│   │   │   ├── build_vector_db_*.py # Chargeurs spécialisés
│   │   ├── processors/              # Processeurs de texte
│   │   │   └── cleaning_text.py     # Nettoyage de texte
│   │   └── build_vector.py          # Construction DB vectorielle
│   └── utils/                       # Configuration et utilitaires
│       ├── config.py                # Configuration centralisée
│       └── main.py                  # Point d'entrée principal
├── data/                            # Données sources
├── embedding_models/                # Modèles d'embedding
├── storage/                         # Stockage persistant
│   └── vector_db/                   # Base de données vectorielle
├── prompts/                         # Templates de prompts
└── scripts/                         # Scripts utilitaires
    ├── installer_embedding.py       # Installation modèles
    └── health_check.py              # Vérification système
```

## 🚀 Installation et démarrage rapide

### Méthode simple avec Makefile (recommandée)

```bash
# Installation complète
make setup

# Construction de la base vectorielle (ajoutez vos fichiers dans data/ avant)
make build

# Lancement du chatbot
make run
```

### Méthode manuelle

### 1. Prérequis
- Python 3.10+
- Ollama installé avec le modèle mistral:7b-instruct-q4_K_M

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3. Installation du modèle d'embedding
```bash
python3 scripts/installer_embedding.py
```

### 4. Préparation des données
Placez vos fichiers dans le dossier `data/` :
- **JSON** : Format `{"content": "texte", "filename": "nom"}`
- **PDF** : Documents PDF standard
- **CSV** : Fichiers avec colonnes de contenu

### 5. Construction de la base vectorielle
```bash
PYTHONPATH=. python3 src/data_processing/build_vector.py
```

### 6. Lancement du chatbot
```bash
PYTHONPATH=. python3 main.py
```

## 🔧 Utilisation

### Commandes Makefile

```bash
make help          # 📖 Afficher l'aide
make setup         # 🚀 Installation complète
make build         # 🔧 Construire la base vectorielle
make run           # 🏃 Lancer le chatbot
make check         # 🔍 Vérifier le système
make status        # 📊 Statut du projet
make clean         # 🧹 Nettoyer les fichiers temporaires
make demo          # 🎬 Workflow complet de démonstration
```

### Interface du chatbot
```
🤖 Chatbot RAG démarré!
Tapez 'q' ou 'quit' pour quitter
Tapez '/debug' pour activer/désactiver le mode debug

===========================================================================
❓ Votre question: Que dit le document sur les polymères ?
```

### Commandes disponibles
- **`/debug`** : Active/désactive le mode debug pour voir les documents récupérés
- **`q`, `quit`, `exit`** : Quitter le chatbot

### Mode debug
Quand activé, affiche :
- Nombre de documents trouvés
- Aperçu des documents pertinents
- Sources et métadonnées

## ⚙️ Configuration

Modifiez `src/utils/config.py` pour personnaliser :

```python
# Modèle LLM
LLM_MODEL = "mistral:7b-instruct-q4_K_M"
LLM_TEMPERATURE = 0.0

# Modèle d'embedding
EMBEDDING_MODEL_DOWNLOAD = "thenlper/gte-small"

# Paramètres de chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 75

# Chemins des données
DATA_FOLDER = "data/"
```

## 📁 Formats de fichiers supportés

### JSON
Structure attendue :
```json
[
  {
    "content": "Votre contenu textuel ici",
    "filename": "nom_du_document"
  }
]
```

### PDF
- Extraction automatique du texte
- Métadonnées de page conservées
- Nettoyage automatique du contenu

### CSV
- Colonne `content` pour le texte principal
- Colonne `filename` optionnelle pour les noms

## 🛠️ Scripts utilitaires

### Vérification du système
```bash
python3 scripts/health_check.py
```
Vérifie que tous les composants sont correctement installés.

### Installation des modèles
```bash
python3 scripts/installer_embedding.py
```
Télécharge et installe le modèle d'embedding.

## 🔍 Dépannage

### Problèmes courants

**❌ Modèle d'embedding manquant**
```bash
make install-model
```

**❌ Erreur d'import de modules**
```bash
make install
```

**❌ Base vectorielle vide**
```bash
# Vérifiez que des fichiers sont dans data/
make status
# Reconstruisez la base
make build
```

**❌ Ollama non disponible**
```bash
# Installez Ollama et le modèle
ollama pull mistral:7b-instruct-q4_K_M
```

### Logs et debug
- Utilisez `/debug` dans le chatbot pour voir les documents récupérés
- Vérifiez les chemins dans `src/utils/config.py`
- Lancez `make check` pour un diagnostic complet
- Utilisez `make status` pour voir l'état du projet

## 🚀 Développement

### Ajouter un nouveau format de fichier
1. Créer un loader dans `src/data_processing/loaders/`
2. L'importer dans `build_vector.py`
3. Ajouter la logique de détection du format

### Personnaliser le nettoyage de texte
Modifier `src/data_processing/processors/cleaning_text.py`

### Changer le modèle d'embedding
Modifier `EMBEDDING_MODEL_DOWNLOAD` dans `src/utils/config.py`

### Structure des tests
```bash
# À venir
tests/
├── test_core/
├── test_data_processing/
└── fixtures/
```

## 📝 Technologies utilisées

- **LangChain** : Framework pour applications LLM
- **ChromaDB** : Base de données vectorielle
- **Sentence Transformers** : Modèles d'embedding
- **Ollama** : Serveur de modèles LLM local
- **HuggingFace** : Hub de modèles et transformers

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajoute nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙋‍♂️ Support

Pour toute question ou problème :
1. Vérifiez la section dépannage
2. Lancez `python3 scripts/health_check.py`
3. Consultez les logs d'erreur
4. Ouvrez une issue sur GitHub

---

**Fait avec ❤️ en Python**
