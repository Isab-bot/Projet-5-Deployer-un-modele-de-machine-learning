# Installation Locale

Ce guide vous explique comment installer et executer l'API en local pour le developpement ou les tests.

## Prerequis

### Logiciels Requis

- **Python** 3.13+ ([Telecharger](https://www.python.org/downloads/))
- **UV** (gestionnaire de dependances) ([Installation](https://docs.astral.sh/uv/getting-started/installation/))
- **Git** ([Telecharger](https://git-scm.com/downloads))

### Verification

\\\ash
# Verifier Python
python --version
# Attendu : Python 3.13.x

# Verifier UV
uv --version
# Attendu : uv 0.x.x

# Verifier Git
git --version
# Attendu : git version 2.x.x
\\\

!!! tip "Alternative a UV"
    Si vous n'avez pas UV, vous pouvez utiliser pip classique, mais UV est recommande pour sa rapidite.

---

## Installation Rapide (5 minutes)

### Etape 1 : Cloner le Repository

\\\ash
# Cloner le projet
git clone https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning.git

# Entrer dans le dossier
cd Projet-5-Deployer-un-modele-de-machine-learning
\\\

### Etape 2 : Installer les Dependances

=== "Avec UV (Recommande)"

    \\\ash
    # Creer environnement virtuel + installer dependances
    uv sync

    # Verifier installation
    uv run python --version
    \\\

=== "Avec pip"

    \\\ash
    # Creer environnement virtuel
    python -m venv .venv

    # Activer environnement
    # Sur Windows :
    .venv\Scripts\activate
    # Sur Mac/Linux :
    source .venv/bin/activate

    # Installer dependances
    pip install -e .
    \\\

### Etape 3 : Configuration Environnement

\\\ash
# Creer fichier .env
echo "DATABASE_URL=sqlite:///./hr_analytics.db" > .env
echo "API_KEY=dev-secret-key12345" >> .env
\\\

!!! warning "Securite"
    Ne JAMAIS commit le fichier \.env\ dans Git. Il est deja dans \.gitignore\.

### Etape 4 : Initialiser la Base de Donnees

\\\ash
# Creer les tables
uv run python create_tables.py

# Importer les donnees (optionnel si fichier 01_classe.joblib present)
uv run python import_data.py
\\\

**Sortie attendue :**

\\\
Table 'employees' creee
Table 'prediction_logs' creee
2363 employes importes
\\\

### Etape 5 : Entrainer le Modele (si necessaire)

!!! info "Modele pre-entraine"
    Le repository contient deja \pipeline_xgboost_optimised.joblib\. Cette etape n'est necessaire que si vous voulez reentrainer.

\\\ash
# Entrainer le modele
uv run python train_final_model.py
\\\

**Duree :** ~30 secondes

**Sortie :** \pipeline_xgboost_optimised.joblib\ cree

### Etape 6 : Lancer l'API

\\\ash
# Demarrer le serveur de developpement
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
\\\

**Sortie attendue :**

\\\
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO: Started reloader process
INFO: Started server process
INFO: Waiting for application startup.
INFO: Application startup complete.
\\\

### Etape 7 : Tester l'API

**Ouvrir dans le navigateur :**

\\\
http://localhost:8000/docs
\\\

Vous devriez voir l'interface Swagger avec tous les endpoints !

---

## Verification de l'Installation

### Test Manuel

\\\ash
# Test 1 : Health Check
curl http://localhost:8000/health
# Attendu : {"status":"healthy", ...}
\\\

\\\ash
# Test 2 : Prediction (necessite API Key)
curl -X POST "http://localhost:8000/predict/from_id/1" \\
  -H "X-API-Key: dev-secret-key12345"
# Attendu : {"log_id": ..., "prediction": "Oui", ...}
\\\

### Tests Automatiques

\\\ash
# Lancer tous les tests
uv run pytest tests/ -v
# Attendu : 51 tests passent
\\\

---

## Structure du Projet

Apres installation, votre structure sera :

\\\
Projet-5-Deployer-un-modele-de-machine-learning/
├── .venv/                                # Environnement virtuel (cree)
├── .env                                  # Variables d'environnement (cree)
├── hr_analytics.db                       # Base SQLite (creee)
├── pipeline_xgboost_optimised.joblib     # Modele ML
├── 01_classe.joblib                      # Donnees brutes
├── main.py                               # API FastAPI
├── model_loader.py                       # Chargement modele
├── database.py                           # Configuration DB
├── models.py                             # Modeles SQLAlchemy
├── schemas.py                            # Schemas Pydantic
├── tests/                                # Tests automatiques
├── docs/                                 # Documentation MkDocs
└── pyproject.toml                        # Configuration projet
\\\

---

## Configuration Avancee

### Variables d'Environnement

Le fichier \.env\ supporte les variables suivantes :

\\\ash
# Base de donnees (defaut : SQLite local)
DATABASE_URL=sqlite:///./hr_analytics.db

# API Key pour authentification
API_KEY=votre-cle-secrete

# Mode debug (optionnel)
DEBUG=true

# Port API (optionnel, defaut : 8000)
PORT=8000
\\\

### Configuration du Modele

Pour modifier les hyperparametres du modele, editer \	rain_final_model.py\ :

\\\python
# Exemple : augmenter le nombre d'arbres
xgb_classifier = XGBClassifier(
    n_estimators=200,  # Au lieu de 100
    max_depth=3,
    learning_rate=0.05,
    ...
)
\\\

---

## Installation avec Docker (Alternative)

### Prerequis Docker

- Docker Desktop installe ([Telecharger](https://www.docker.com/products/docker-desktop))

### Build et Run

\\\ash
# Build l'image
docker build -t api-demission .

# Lancer le container
docker run -p 7860:7860 \\
  -e API_KEY=dev-secret-key12345 \\
  api-demission
\\\

**Acces :** http://localhost:7860

### Avec Docker Compose

\\\ash
# Lancer avec docker-compose
docker-compose up
\\\

**Configuration :** Voir \docker-compose.yml\

---

## Resolution de Problemes

### Erreur : "Module not found"

\\\ash
# Reinstaller dependances
uv sync --force

# OU avec pip
pip install -e . --force-reinstall
\\\

### Erreur : "Database locked"

\\\ash
# Supprimer et recreer la DB
rm hr_analytics.db
uv run python create_tables.py
uv run python import_data.py
\\\

### Erreur : "Port 8000 already in use"

\\\ash
# Trouver le processus
# Windows :
netstat -ano | findstr :8000
# Mac/Linux :
lsof -i :8000

# Tuer le processus OU utiliser un autre port
uv run uvicorn main:app --port 8001
\\\

### Erreur : "API Key invalid"

Verifier que :

1. Le fichier \.env\ existe
2. La variable \API_KEY\ est definie
3. Vous utilisez le header \X-API-Key\ dans vos requetes

---

## Etapes Suivantes

Maintenant que l'installation est terminee :

1. **[Premier Test](quickstart.md)** : Testez votre premiere prediction
2. **[Guide Utilisateur](../user-guide/api-usage.md)** : Apprenez a utiliser l'API
3. **[Documentation Technique](../technical/architecture.md)** : Comprenez l'architecture

---

## Conseils pour le Developpement

### Hot Reload

Le flag \--reload\ d'Uvicorn recharge automatiquement l'API quand vous modifiez le code :

\\\ash
uv run uvicorn main:app --reload
\\\

### Logs Detailles

\\\ash
# Activer logs DEBUG
uv run uvicorn main:app --reload --log-level debug
\\\

### Tests Continus

\\\ash
# Relancer tests automatiquement a chaque modification
uv run pytest-watch
\\\

---

**Installation terminee !**

Passez au [guide de demarrage rapide](quickstart.md)