# Démarrage Rapide

Commencez à utiliser l'API de prédiction de démissions en 5 minutes ! 🚀

---

## 🎯 Objectif

Faire votre **première prédiction** en moins de 5 minutes.

---

## ✅ Prérequis

- Un terminal (PowerShell, bash, ou équivalent)
- `curl` installé (ou Python avec `requests`)

---

## 🚀 Option 1 : Test Immédiat (Sans Installation)

### Étape 1 : Tester l'API en Production
```bash
# Health check
curl https://Fox6768-api-demission-prediction.hf.space/health
```

**Réponse attendue :**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_status": "connected"
}
```

---

### Étape 2 : Faire une Prédiction Simple

**⚠️ Note :** Les endpoints de prédiction nécessitent une API Key (contactez l'administrateur).

**Pour tester sans API Key, utilisez la documentation interactive :**

👉 **[Ouvrir Swagger UI](https://Fox6768-api-demission-prediction.hf.space/docs)**

1. Cliquez sur `POST /predict/new_employee`
2. Cliquez sur "Try it out"
3. Utilisez cet exemple de données :
```json
{
  "satisfaction_level": 0.38,
  "last_evaluation": 0.53,
  "number_project": 2,
  "average_montly_hours": 157,
  "time_spend_company": 3,
  "Work_accident": 0,
  "promotion_last_5years": 0,
  "departement": "sales",
  "salary": "low"
}
```

4. Cliquez sur "Execute"

**Résultat attendu :**
```json
{
  "employee_id": null,
  "prediction": "Oui",
  "confidence_score": 0.87,
  "log_id": 42
}
```

---

## 💻 Option 2 : Installation Locale

### Étape 1 : Cloner le Projet
```bash
git clone https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning.git
cd Projet-5-Deployer-un-modele-de-machine-learning
```

---

### Étape 2 : Installer les Dépendances
```bash
# Installer UV (si pas déjà fait)
pip install uv

# Installer les dépendances du projet
uv sync
```

---

### Étape 3 : Configurer l'Environnement

**Créer un fichier `.env` :**
```bash
# Windows PowerShell
New-Item -Path .env -ItemType File

# Linux/Mac
touch .env
```

**Ajouter ce contenu dans `.env` :**
```bash
API_KEY=votre-cle-de-test-12345
DATABASE_URL=sqlite:///./hr_analytics.db
```

---

### Étape 4 : Initialiser la Base de Données
```bash
uv run python import_data.py
```

**Résultat attendu :**
```
🗑️  Suppression de l'ancienne base : hr_analytics.db
📋 Création des tables...
📂 Chargement du dataset...
✅ Dataset chargé : 2363 lignes, 10 colonnes
📥 Importation dans la base de données...
  → 100/2363 lignes importées...
  → 200/2363 lignes importées...
  ...
✅ 2363 lignes ajoutées à la table 'employees'
```

---

### Étape 5 : Lancer l'API
```bash
uv run uvicorn main:app --reload
```

**Résultat attendu :**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

---

### Étape 6 : Tester Localement

**Ouvrir dans le navigateur :**

👉 **http://127.0.0.1:8000/docs**

**Ou avec curl :**
```bash
curl http://127.0.0.1:8000/health
```

---

## 🐍 Option 3 : Script Python

**Créer un fichier `test_api.py` :**
```python
import requests
import json

# Configuration
API_URL = "https://Fox6768-api-demission-prediction.hf.space"
API_KEY = "VOTRE_CLE_API"  # Remplacer par votre clé

# Headers
headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Données employé
employee_data = {
    "satisfaction_level": 0.38,
    "last_evaluation": 0.53,
    "number_project": 2,
    "average_montly_hours": 157,
    "time_spend_company": 3,
    "Work_accident": 0,
    "promotion_last_5years": 0,
    "departement": "sales",
    "salary": "low"
}

# Faire la prédiction
response = requests.post(
    f"{API_URL}/predict/new_employee",
    headers=headers,
    json=employee_data
)

# Afficher le résultat
if response.status_code == 200:
    result = response.json()
    print(f"✅ Prédiction : {result['prediction']}")
    print(f"📊 Confiance : {result['confidence_score']:.2%}")
    print(f"📝 Log ID : {result['log_id']}")
else:
    print(f"❌ Erreur : {response.status_code}")
    print(response.text)
```

**Exécuter :**
```bash
python test_api.py
```

---

## 📊 Interpréter les Résultats

| Prédiction | Signification | Action RH |
|------------|---------------|-----------|
| **"Oui"** | Risque élevé de démission | Entretien, plan de rétention |
| **"Non"** | Risque faible de démission | Suivi normal |

**Score de confiance :**
- **> 0.8** : Prédiction très fiable
- **0.5 - 0.8** : Prédiction fiable
- **< 0.5** : Prédiction peu fiable

---

## 🎓 Prochaines Étapes

1. **Explorer la documentation complète :** [Lien](https://isab-bot.github.io/Projet-5-Deployer-un-modele-de-machine-learning/)
2. **Voir plus d'exemples :** [Guide Utilisateur](../user-guide/examples.md)
3. **Comprendre l'API :** [Référence API](../api/endpoints.md)
4. **Configurer l'authentification :** [Guide Auth](../user-guide/authentication.md)
---

## ❓ Besoin d'Aide ?

- **Documentation complète :** https://isab-bot.github.io/Projet-5-Deployer-un-modele-de-machine-learning/
- **API Swagger :** https://Fox6768-api-demission-prediction.hf.space/docs

---

**✅ Félicitations ! Vous venez de faire votre première prédiction ! 🎉**