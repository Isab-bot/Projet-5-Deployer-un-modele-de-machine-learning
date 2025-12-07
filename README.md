# Projet 5 - Déployer un Modèle de Machine Learning

![CI Tests](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning/actions/workflows/ci.yml/badge.svg)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Space-yellow)](https://huggingface.co/spaces/Fox6768/API_demission_prediction)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-green)](https://fastapi.tiangolo.com/)

## 🎯 Objectif du Projet

Système de prédiction de démissions d'employés utilisant un modèle XGBoost déployé en production via une API REST sécurisée.

**Formation :** IA Engineer  
**Contexte :** Projet 5 - Déploiement d'un modèle de Machine Learning

---

## 🚀 API en Production

**URL Production :** [https://Fox6768-api-demission-prediction.hf.space](https://Fox6768-api-demission-prediction.hf.space)

**Documentation Interactive (Swagger) :** [https://Fox6768-api-demission-prediction.hf.space/docs](https://Fox6768-api-demission-prediction.hf.space/docs)

**Documentation Complète :** [Lien vers GitHub Pages] *(à ajouter après déploiement)*

---

## 📊 Performances du Modèle

| Métrique | Score | Signification |
|----------|-------|---------------|
| **F2-Score** | 0.6818 | Métrique principale (privilégie le Recall) |
| **Precision** | 0.8214 | 82% des alertes sont correctes |
| **Recall** | 0.9474 | 95% des démissions sont détectées |
| **ROC-AUC** | 0.9326 | Excellent pouvoir discriminant |

---

## 🛠️ Stack Technique

- **API :** FastAPI 0.115.5
- **ML :** XGBoost + scikit-learn
- **Database :** SQLite
- **Déploiement :** Docker + Hugging Face Spaces
- **CI/CD :** GitHub Actions
- **Tests :** pytest (51 tests automatiques, 100% passants)
- **Documentation :** MkDocs

---

## ⚡ Installation Locale

### Prérequis

- Python 3.13+
- UV (gestionnaire de dépendances)
- Git

### Étapes
```bash
# Cloner le repository
git clone https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning.git
cd Projet-5-Deployer-un-modele-de-machine-learning

# Installer les dépendances
uv sync

# Lancer l'API
uv run uvicorn main:app --reload
```

L'API sera accessible sur `http://127.0.0.1:8000`

**Documentation détaillée :** Voir [Guide d'Installation](docs/getting-started/installation.md)

---

## 📖 Utilisation

### Exemple de Prédiction
```bash
curl -X POST "https://Fox6768-api-demission-prediction.hf.space/predict" \
  -H "X-API-Key: votre_cle" \
  -H "Content-Type: application/json" \
  -d '{
    "satisfaction_level": 0.38,
    "last_evaluation": 0.53,
    "number_project": 2,
    "average_montly_hours": 157,
    "time_spend_company": 3,
    "Work_accident": 0,
    "promotion_last_5years": 0,
    "departement": "sales",
    "salary": "low"
  }'
```

**Plus d'exemples :** Voir [Documentation Utilisateur](docs/user-guide/examples.md)

---

## 🧪 Tests
```bash
# Lancer tous les tests
uv run pytest

# Avec coverage
uv run pytest --cov
```

**Résultat :** 51/51 tests passants ✅

---

## 📁 Structure du Projet
```
.
├── main.py                    # API FastAPI
├── model_loader.py            # Chargement du modèle
├── models.py                  # Modèles SQLAlchemy
├── schemas.py                 # Schémas Pydantic
├── database.py                # Configuration base de données
├── tests/                     # Tests automatiques
├── docs/                      # Documentation MkDocs
├── pipeline_xgboost_optimised.joblib  # Modèle ML
└── pyproject.toml             # Configuration projet
```

---

## 🔗 Liens Utiles

- **API Production :** [https://Fox6768-api-demission-prediction.hf.space](https://Fox6768-api-demission-prediction.hf.space)
- **Swagger UI :** [/docs](https://Fox6768-api-demission-prediction.hf.space/docs)
- **Hugging Face Space :** [Fox6768/API_demission_prediction](https://huggingface.co/spaces/Fox6768/API_demission_prediction)
- **CI/CD Pipeline :** [GitHub Actions](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning/actions)

---

## 📝 Licence

Projet développé dans le cadre d'une formation IA Engineer.

---

## 👤 Auteur

**I.R.** - En formation IA Engineer

**Contact :** Voir [page Contact](docs/about/contact.md)
