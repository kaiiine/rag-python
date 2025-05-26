# 🧪 Projet RAG Prof de Chimie avec LangChain + Ollama

Ce projet est un système de questions/réponses (RAG : Retrieval-Augmented Generation) en français, destiné à répondre de manière rigoureuse à des questions de chimie en se basant uniquement sur des documents fournis (PDF, CSV, JSON).

Le système utilise :
- 🧠 [LangChain](https://www.langchain.com/)
- 🔍 [ChromaDB](https://www.trychroma.com/)
- 🤖 [Ollama](https://ollama.com/) pour les modèles LLM & embeddings

---

## 📁 Structure du projet

```
.
├── csv/                          # Contient les fichiers CSV à indexer
├── json/                         # Contient les fichiers JSON à indexer
├── pdf/                          # Contient les fichiers PDF à indexer
├── chrome_langchain_db/         # Dossier de la base vectorielle Chroma (généré automatiquement)
├── build_vector_db_pdf.py       # Script pour indexer les fichiers PDF
├── build_vector_db_csv.py       # Script pour indexer les fichiers CSV
├── build_vector_db_json.py      # Script pour indexer les fichiers JSON
├── main.py                      # Script principal : lance le chatbot
├── vector.py                    # Contient le `retriever` utilisé par le chatbot
├── requirements.txt             # Liste des dépendances Python
├── README.md                    # Ce fichier
└── venv/                        # Environnement virtuel Python (recommandé)
```

---

## 🚀 Mise en route

### 1. Prérequis

- Python 3.10 ou supérieur
- Ollama installé avec les modèles suivants :
  - `llama3.2:latest` (ou `llama2`, `mistral`, etc.)
  - `mxbai-embed-large` pour les embeddings
- `virtualenv` recommandé

---

## ⚙️ Installation d'Ollama et des modèles

### A. Installer Ollama

1. Rendez-vous sur [https://ollama.com](https://ollama.com) et téléchargez le binaire pour votre système d’exploitation.
2. Installez-le selon les instructions (Linux, macOS, Windows).
3. Vérifiez l'installation avec :

```bash
ollama --version
```

### B. Télécharger les modèles nécessaires

Une fois Ollama installé, lancez les commandes suivantes :

```bash
ollama run llama3.2
```

```bash
ollama run mxbai-embed-large
```

Cela téléchargera les modèles localement et les rendra utilisables par votre projet.

> Remarque : les noms de modèles doivent correspondre à ceux utilisés dans les scripts Python (`llama3.2:latest`, `mxbai-embed-large`).

---

## 📦 Installation du projet

### a. Créez un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate      # Sur Windows : venv\Scripts\activate
```

### b. Installez les dépendances

```bash
pip install -r requirements.txt
```

---

## 🧱 Construction de la base de données vectorielle

### A. À partir de fichiers PDF

1. Placez vos fichiers `.pdf` dans le dossier `pdf/`
2. Lancez :

```bash
python build_vector_db_pdf.py
```

### B. À partir de fichiers CSV

1. Placez votre fichier `.csv` dans le dossier `csv/`
2. Lancez :

```bash
python build_vector_db_csv.py
```

### C. À partir de fichiers JSON

1. Placez vos fichiers `.json` dans le dossier `json/`
2. Lancez :

```bash
python build_vector_db_json.py
```

---

## 💬 Utilisation du chatbot

Une fois la base construite :

```bash
python main.py
```

Vous pouvez alors poser des questions en français basées sur les documents fournis.

---

## 🧠 Comportement du chatbot

Le prompt impose des règles strictes :

- Répond **uniquement** si l'information est **présente explicitement** dans les documents.
- Citer les numéros de pages : `(p. 2)`
- Répondre en **français clair, pédagogique et rigoureux**
- Si l'information est absente :  
  `« Je ne trouve pas cette information dans les documents fournis. »`

---

## 📌 Exemple d'utilisation

```
------------------------------------------
Enter your question (q to quit): Quelle est la différence entre un acide et une base ?
```

Réponse possible :
```
Un acide est défini comme une espèce chimique capable de donner un proton (p. 2), tandis qu'une base peut capter ce proton (p. 3).
```

---

## ✨ Remerciements

- [LangChain](https://www.langchain.com/)
- [Ollama](https://ollama.com/)
- [ChromaDB](https://www.trychroma.com/)
