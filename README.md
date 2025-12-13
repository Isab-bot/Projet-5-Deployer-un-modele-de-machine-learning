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

**Documentation Complète :** [https://isab-bot.github.io/Projet-5-Deployer-un-modele-de-machine-learning/](https://isab-bot.github.io/Projet-5-Deployer-un-modele-de-machine-learning/)

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


## 🚀 Déploiement

### Environnements

| Environnement | URL | Configuration |
|---------------|-----|---------------|
| **Production** | [HF Spaces](https://Fox6768-api-demission-prediction.hf.space) | Secrets HF Spaces |
| **Développement** | `http://127.0.0.1:8000` | Fichier `.env` local |

### Configuration des Environnements

#### Développement Local

1. Créer un fichier `.env` :
```bash
API_KEY=votre-cle-dev
DATABASE_URL=sqlite:///./hr_analytics.db
ENVIRONMENT=development
```

2. Lancer l'API :
```bash
uv run uvicorn main:app --reload
```

#### Production (Hugging Face Spaces)

**Configuration automatique via :**
- **Secrets HF Spaces :** `API_KEY` défini dans Settings → Variables and secrets
- **Dockerfile :** Build et déploiement automatiques
- **HTTPS :** Activé par défaut

**Déploiement automatique :**
```bash
git push  # Push vers GitHub
git push space main  # Déploiement vers HF Spaces
```

### Pipeline CI/CD

**GitHub Actions :** Exécute automatiquement les tests à chaque push
```yaml
# .github/workflows/ci.yml
- Tests unitaires et fonctionnels (61 tests)
- Validation de la couverture (>80%)
- Vérification du build
```

**Badge :** ![CI Tests](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning/actions/workflows/ci.yml/badge.svg)

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

## 🔐 Authentification

L'API utilise une **authentification par API Key** via header HTTP `X-API-Key`.

### Endpoints Publics (sans authentification)

- `GET /` - Page d'accueil
- `GET /health` - Health check
- `GET /docs` - Documentation Swagger

### Endpoints Protégés (API Key requise)

- `POST /predict/*` - Endpoints de prédiction
- `GET /employees/*` - Consultation des employés
- `GET /predictions/*` - Historique des prédictions
- `GET /stats` - Statistiques

### Exemple d'utilisation
```bash
curl -X POST "https://Fox6768-api-demission-prediction.hf.space/predict/new_employee" \
  -H "X-API-Key: VOTRE_CLE_API" \
  -H "Content-Type: application/json" \
  -d '{
    "satisfaction_level": 0.75,
    "last_evaluation": 0.86,
    "number_project": 5,
    ...
  }'
```

**Documentation complète :** [Guide d'Authentification](https://isab-bot.github.io/Projet-5-Deployer-un-modele-de-machine-learning/user-guide/authentication/)

**Bonnes pratiques :**
- ✅ Stocker la clé dans un fichier `.env`
- ✅ Ajouter `.env` au `.gitignore`
- ❌ Ne jamais commiter la clé sur Git

---

**Plus d'exemples :** Voir [Documentation Utilisateur](docs/user-guide/examples.md)



## 📊 Processus de Traitement et Stockage des Données

### Pipeline de Données
```
01_classe.joblib → import_data.py → SQLite (employees) → API → predictions_logs
     (1470)            ↓                                    ↓
                  Validation                           Logging
                  Transformation                       Traçabilité
```

### Workflow Complet

1. **Source de données** : `01_classe.joblib` (1470 employés historiques)
2. **Import initial** : Script `import_data.py`
   - Charge le fichier joblib
   - Transforme en format JSON (features)
   - Insert dans table `employees`
3. **Stockage principal** : Base SQLite `hr_analytics.db`
   - Table `employees` : Données d'entraînement (lecture seule)
   - Table `predictions_logs` : Historique des prédictions (écriture continue)
4. **Logging des prédictions** : Automatique via API
   - Chaque prédiction → Nouvelle entrée dans `predictions_logs`
   - Traçabilité complète (input, output, timestamp, modèle version)

### Gestion des Données

**Backup :**
```bash
# Backup automatique quotidien (recommandé)
cp hr_analytics.db backups/hr_analytics_$(date +%Y%m%d).db
```

**Nettoyage :**
```sql
-- Supprimer les logs de plus d'un an
DELETE FROM predictions_logs WHERE created_at < datetime('now', '-1 year');
VACUUM;
```

**Monitoring :**
- Taille de la base : `(Get-Item hr_analytics.db).Length / 1MB`
- Nombre de prédictions : `SELECT COUNT(*) FROM predictions_logs;`
- Croissance journalière : Voir `docs/operations/monitoring.md`

**Documentation complète :** [Base de Données](https://isab-bot.github.io/Projet-5-Deployer-un-modele-de-machine-learning/technical/database/)

---
## 📈 Besoins Analytiques et Tableaux de Bord

### Cas d'Usage Analytiques

L'API permet d'alimenter des outils d'analyse et de visualisation pour suivre les tendances de démissions.

### KPIs Principaux

| Indicateur | Requête SQL | Utilité |
|------------|-------------|---------|
| **Taux de prédictions "Oui"** | `SELECT COUNT(*) WHERE prediction_result='Oui'` | Identifier les périodes à risque |
| **Prédictions par département** | `GROUP BY departement` | Cibler les départements critiques |
| **Score de confiance moyen** | `AVG(confidence_score)` | Évaluer la fiabilité du modèle |
| **Volume de prédictions** | `COUNT(*) GROUP BY DATE(created_at)` | Suivre l'utilisation de l'API |

### Requêtes pour Dashboards

#### 1. Top 5 Départements à Risque
```sql
SELECT 
  json_extract(input_features, '$.departement') as departement,
  COUNT(*) as total_predictions,
  SUM(CASE WHEN prediction_result = 'Oui' THEN 1 ELSE 0 END) as demissions_predites,
  ROUND(100.0 * SUM(CASE WHEN prediction_result = 'Oui' THEN 1 ELSE 0 END) / COUNT(*), 2) as taux_risque
FROM predictions_logs
WHERE created_at >= datetime('now', '-30 days')
GROUP BY departement
ORDER BY demissions_predites DESC
LIMIT 5;
```

#### 2. Évolution Hebdomadaire
```sql
SELECT 
  strftime('%Y-W%W', created_at) as semaine,
  COUNT(*) as predictions_totales,
  SUM(CASE WHEN prediction_result = 'Oui' THEN 1 ELSE 0 END) as risque_eleve,
  AVG(confidence_score) as confiance_moyenne
FROM predictions_logs
WHERE created_at >= datetime('now', '-12 weeks')
GROUP BY semaine
ORDER BY semaine;
```

#### 3. Distribution des Scores de Confiance
```sql
SELECT 
  CASE 
    WHEN confidence_score < 0.5 THEN 'Faible (<0.5)'
    WHEN confidence_score < 0.7 THEN 'Moyen (0.5-0.7)'
    ELSE 'Élevé (>0.7)'
  END as niveau_confiance,
  COUNT(*) as nombre_predictions
FROM predictions_logs
GROUP BY niveau_confiance;
```

### Intégration avec Outils BI

#### Power BI / Tableau

Connexion directe à `hr_analytics.db` ou export CSV :
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('hr_analytics.db')
df = pd.read_sql_query("SELECT * FROM predictions_logs", conn)
df.to_csv("export_predictions.csv", index=False)
```

#### Excel / Google Sheets

Export manuel via requêtes SQL ou via l'API :
```bash
# Export des 30 derniers jours
sqlite3 hr_analytics.db <<EOF
.mode csv
.output predictions_30j.csv
SELECT * FROM predictions_logs WHERE created_at >= datetime('now', '-30 days');
.quit
EOF
```

### Métriques de Performance

Pour évaluer le modèle en production :

- **Taux de faux positifs** : Comparer prédictions vs démissions réelles
- **Taux d'utilisation API** : Nombre de requêtes par jour
- **Temps de réponse** : Latence moyenne des prédictions
- **Satisfaction utilisateurs** : Feedback sur la pertinence

**Documentation complète :** [Monitoring et Statistiques](https://isab-bot.github.io/Projet-5-Deployer-un-modele-de-machine-learning/operations/monitoring/)

## 🧪 Tests
```bash
# Lancer tous les tests
uv run pytest

# Avec coverage
uv run pytest --cov
```

**Résultat :** 51/51 tests passants ✅

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
