# Makefile pour RAG Python
# Usage: make [target]

.PHONY: help install setup build run clean check test

# Variables
PYTHON := python3
VENV := venv
SRC := src
SCRIPTS := scripts

# Couleurs pour l'affichage
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Cible par défaut
.DEFAULT_GOAL := help

help: ## 📖 Afficher l'aide
	@echo "$(BLUE)🤖 RAG Python - Makefile$(NC)"
	@echo ""
	@echo "$(YELLOW)Commandes disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## 📦 Installer les dépendances
	@echo "$(BLUE)📦 Installation des dépendances...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "$(GREEN)✅ Dépendances installées$(NC)"

install-model: ## 🔽 Télécharger le modèle d'embedding
	@echo "$(BLUE)🔽 Installation du modèle d'embedding...$(NC)"
	PYTHONPATH=. $(PYTHON) $(SCRIPTS)/installer_embedding.py
	@echo "$(GREEN)✅ Modèle d'embedding installé$(NC)"

setup: install install-model ## 🚀 Installation complète (dépendances + modèle)
	@echo "$(GREEN)🎉 Setup terminé!$(NC)"

build: ## 🔧 Construire la base de données vectorielle
	@echo "$(BLUE)🔧 Construction de la base vectorielle...$(NC)"
	@if [ ! -d "data" ] || [ -z "$$(ls -A data 2>/dev/null)" ]; then \
		echo "$(RED)❌ Aucun fichier trouvé dans le dossier data/$(NC)"; \
		echo "$(YELLOW)💡 Ajoutez vos fichiers JSON, PDF ou CSV dans data/ avant de continuer$(NC)"; \
		exit 1; \
	fi
	PYTHONPATH=. $(PYTHON) $(SRC)/data_processing/build_vector.py
	@echo "$(GREEN)✅ Base vectorielle construite$(NC)"

run: ## 🏃 Lancer le chatbot
	@echo "$(BLUE)🏃 Lancement du chatbot RAG...$(NC)"
	PYTHONPATH=. $(PYTHON) main.py

check: ## 🔍 Vérifier l'état du système
	@echo "$(BLUE)🔍 Vérification du système...$(NC)"
	PYTHONPATH=. $(PYTHON) $(SCRIPTS)/health_check.py

clean: ## 🧹 Nettoyer les fichiers temporaires
	@echo "$(BLUE)🧹 Nettoyage...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Nettoyage terminé$(NC)"

clean-all: clean ## 🗑️ Nettoyage complet (cache + models + DB)
	@echo "$(YELLOW)⚠️  Suppression des modèles et base vectorielle...$(NC)"
	rm -rf embedding_models/* 2>/dev/null || true
	rm -rf storage/vector_db/* 2>/dev/null || true
	@echo "$(GREEN)✅ Nettoyage complet terminé$(NC)"

reset: clean-all setup build ## 🔄 Reset complet (tout refaire)
	@echo "$(GREEN)🔄 Reset complet terminé!$(NC)"

dev-setup: ## 🛠️ Setup pour développement
	@echo "$(BLUE)🛠️ Setup développement...$(NC)"
	$(PYTHON) -m pip install black flake8 pytest
	@echo "$(GREEN)✅ Outils de développement installés$(NC)"

format: ## 🎨 Formater le code avec black
	@echo "$(BLUE)🎨 Formatage du code...$(NC)"
	black $(SRC)/ --line-length 88
	@echo "$(GREEN)✅ Code formaté$(NC)"

lint: ## 🔍 Vérifier le code avec flake8
	@echo "$(BLUE)🔍 Vérification du code...$(NC)"
	flake8 $(SRC)/ --max-line-length=88 --extend-ignore=E203,W503
	@echo "$(GREEN)✅ Code vérifié$(NC)"

test: ## 🧪 Lancer les tests (à venir)
	@echo "$(YELLOW)🧪 Tests pas encore implémentés$(NC)"

status: ## 📊 Afficher le statut du projet
	@echo "$(BLUE)📊 Statut du projet:$(NC)"
	@echo ""
	@echo "$(YELLOW)📁 Structure:$(NC)"
	@ls -la | grep "^d" | grep -E "(src|data|scripts|storage|embedding_models)" || echo "  Dossiers manquants"
	@echo ""
	@echo "$(YELLOW)📦 Modèles:$(NC)"
	@if [ -d "embedding_models" ] && [ -n "$$(ls -A embedding_models 2>/dev/null)" ]; then \
		echo "  $(GREEN)✅ Modèle d'embedding présent$(NC)"; \
	else \
		echo "  $(RED)❌ Modèle d'embedding manquant$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)🗄️ Base vectorielle:$(NC)"
	@if [ -d "storage/vector_db" ] && [ -n "$$(ls -A storage/vector_db 2>/dev/null)" ]; then \
		echo "  $(GREEN)✅ Base vectorielle présente$(NC)"; \
	else \
		echo "  $(RED)❌ Base vectorielle manquante$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)📄 Données:$(NC)"
	@if [ -d "data" ] && [ -n "$$(ls -A data 2>/dev/null)" ]; then \
		echo "  $(GREEN)✅ Fichiers de données présents ($(shell ls data 2>/dev/null | wc -l) fichiers)$(NC)"; \
	else \
		echo "  $(RED)❌ Aucun fichier de données$(NC)"; \
	fi

demo: ## 🎬 Workflow complet de démonstration
	@echo "$(BLUE)🎬 Démonstration complète...$(NC)"
	@echo "$(YELLOW)1. Vérification des prérequis...$(NC)"
	make status
	@echo ""
	@echo "$(YELLOW)2. Installation si nécessaire...$(NC)"
	make setup
	@echo ""
	@echo "$(YELLOW)3. Construction de la base...$(NC)"
	make build
	@echo ""
	@echo "$(YELLOW)4. Vérification finale...$(NC)"
	make check
	@echo ""
	@echo "$(GREEN)🎉 Prêt! Lancez 'make run' pour démarrer le chatbot$(NC)"

# Raccourcis pratiques
i: install ## 📦 Raccourci pour install
b: build   ## 🔧 Raccourci pour build  
r: run     ## 🏃 Raccourci pour run
c: check   ## 🔍 Raccourci pour check
s: status  ## 📊 Raccourci pour status
