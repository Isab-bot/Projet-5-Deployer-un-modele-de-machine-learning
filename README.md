 ---
title: API Prédiction Démission
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🎯 API de Prédiction de Démission - Projet 5

![CI Tests](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning/actions/workflows/ci.yml/badge.svg)

API REST pour prédire les démissions d'employés à l'aide d'un modèle XGBoost.

---

## 📊 Description

Cette API permet de :
- ✅ Prédire si un employé va démissionner
- ✅ Consulter l'historique des prédictions
- ✅ Analyser les facteurs de risque de démission

**Modèle utilisé :** XGBoost avec optimisation du seuil (F2-Score)

---

## 🔐 Authentification

L'API est protégée par API Key. 

**Pour utiliser l'API, ajoutez ce header à vos requêtes :**
```http
X-API-Key: votre-cle-api
```

**Exemple avec curl :**
```bash
curl -X POST https://votre-space.hf.space/predict/from_id/1 \
  -H "X-API-Key: votre-cle-api"
```

---

## 📡 Endpoints Disponibles

### **🔓 Endpoints Publics (sans authentification)**

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Informations sur l'API |
| `/health` | GET | Status de l'API |
| `/docs` | GET | Documentation Swagger interactive |

### **🔒 Endpoints Protégés (API Key requise)**

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/predict/from_id/{employee_id}` | POST | Prédiction pour un employé existant |
| `/predict/new_employee` | POST | Prédiction pour un nouvel employé |
| `/predict/log/{log_id}` | GET | Récupérer une prédiction passée |
| `/predictions/logs` | GET | Liste des prédictions |

---

## 🚀 Utilisation

### **Exemple 1 : Prédiction depuis un ID**
```bash
curl -X POST "https://votre-space.hf.space/predict/from_id/1" \
  -H "X-API-Key: votre-cle-api"
```

**Réponse :**
```json
{
  "log_id": 123,
  "employee_id": 1,
  "prediction": "Non",
  "confidence_score": 0.85,
  "features": {...},
  "timestamp": "2024-12-02T10:30:00"
}
```

### **Exemple 2 : Prédiction pour un nouvel employé**
```bash
curl -X POST "https://votre-space.hf.space/predict/new_employee" \
  -H "X-API-Key: votre-cle-api" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "age": 35,
      "anciennete": 5,
      "satisfaction": 0.7,
      ...
    }
  }'
```

---

## 🛠️ Technologies

| Technologie | Usage |
|-------------|-------|
| **FastAPI** | Framework API REST |
| **XGBoost** | Modèle de Machine Learning |
| **SQLAlchemy** | ORM pour la base de données |
| **SQLite** | Base de données |
| **Docker** | Containerisation |
| **GitHub Actions** | CI/CD (tests automatiques) |
| **Hugging Face Spaces** | Déploiement cloud |

---

## 📈 Performance du Modèle

| Métrique | Valeur |
|----------|--------|
| **F2-Score** | > 0.80 |
| **Recall** | > 0.85 |
| **ROC-AUC** | > 0.75 |
| **Précision** | > 0.50 |

Le modèle privilégie le **Recall** (détecter toutes les démissions potentielles) plutôt que la précision.

---

## 🧪 Tests

✅ **51 tests automatiques** lancés à chaque commit via GitHub Actions
```bash
# Lancer les tests localement
pytest tests/ -v
```

---

## 💻 Installation Locale (Développement)

### **Prérequis**
- Python 3.13
- UV (gestionnaire de dépendances)

### **Étapes**
```bash
# 1. Cloner le repository
git clone https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning.git
cd Projet-5-Deployer-un-modele-de-machine-learning

# 2. Installer les dépendances
uv sync

# 3. Créer le fichier .env
echo "DATABASE_URL=sqlite:///./hr_analytics.db" > .env
echo "API_KEY=votre-cle-de-dev" >> .env

# 4. Créer les tables
uv run python create_tables.py

# 5. Importer les données (si nécessaire)
uv run python import_data.py

# 6. Entraîner le modèle
uv run python train_final_model.py

# 7. Lancer l'API
uv run uvicorn main:app --reload
```

L'API sera accessible sur http://localhost:8000

---

## 🐳 Docker

### **Build local**
```bash
docker build -t api-demission .
docker run -p 7860:7860 -e API_KEY=votre-cle api-demission
```

### **Variables d'environnement**
- `DATABASE_URL` : Chemin de la base de données (défaut : `sqlite:///./hr_analytics.db`)
- `API_KEY` : Clé d'authentification (à configurer dans les secrets)

---

## 📚 Documentation

- **Swagger UI** : `/docs` (documentation interactive)
- **ReDoc** : `/redoc` (documentation alternative)

---

## 👨‍💻 Auteur

I. R. 
Projet 5 - Formation IA Engineer

---

## 📄 Licence

Ce projet est développé dans le cadre d'une formation.

---

## 🔗 Liens

- [GitHub Repository](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning)
- [CI/CD Pipeline](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning/actions)
- [Hugging Face Space](https://huggingface.co/spaces/Isab-bot/api-demission)