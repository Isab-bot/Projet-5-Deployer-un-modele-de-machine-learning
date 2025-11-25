 ##Installation et configuration

### 1. Cloner le repository
git clone 
cd deployer_un_modele

### 2. Installer les dépendances
uv sync

### 3. Créer les tables PostgreSQL
uv run python create_tables.py

### 4. Importer les données
uv run python import_data.py

### 5. Entraîner le modèle
uv run python train_final_model.py

### 6. Lancer l'API
uv run uvicorn main:app --reload