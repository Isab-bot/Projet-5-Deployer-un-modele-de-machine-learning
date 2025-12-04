# Image de base Python 3.13
FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY . .

# Créer le dossier models s'il n'existe pas
RUN mkdir -p models

# Entraîner le modèle au build (si nécessaire)
# Ou copier un modèle pré-entraîné
# Le modèle pré-entraîné est déjà copié avec COPY . .
# RUN python train_final_model.py

# Exposer le port 7860 (standard Hugging Face)
EXPOSE 7860

# Variables d'environnement par défaut
ENV DATABASE_URL=sqlite:///./hr_analytics.db
ENV API_KEY=changeme

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]


