# Authentification

## 🔐 Vue d'ensemble

L'API utilise une **authentification par API Key** via header HTTP pour sécuriser les endpoints de prédiction.

---

## 🔑 Obtenir votre Clé API

### En développement local

Créez un fichier `.env` à la racine du projet :
```bash
API_KEY=votre-cle-secrete-123456
```

### En production

Contactez l'administrateur pour obtenir votre clé API personnelle.

---

## 📡 Utiliser votre Clé

### Avec curl
```bash
curl -X POST "https://Fox6768-api-demission-prediction.hf.space/predict/new_employee" \
  -H "X-API-Key: VOTRE_CLE_API" \
  -H "Content-Type: application/json" \
  -d '{
    "satisfaction_level": 0.75,
    "last_evaluation": 0.86,
    "number_project": 5,
    "average_montly_hours": 200,
    "time_spend_company": 4,
    "Work_accident": 0,
    "promotion_last_5years": 0,
    "departement": "IT",
    "salary": "medium"
  }'
```

### Avec Python
```python
import requests
import os
from dotenv import load_dotenv

# Charger la clé depuis .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

url = "https://Fox6768-api-demission-prediction.hf.space/predict/new_employee"
headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}
data = {
    "satisfaction_level": 0.75,
    "last_evaluation": 0.86,
    "number_project": 5,
    "average_montly_hours": 200,
    "time_spend_company": 4,
    "Work_accident": 0,
    "promotion_last_5years": 0,
    "departement": "IT",
    "salary": "medium"
}

response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    print("Prédiction :", response.json())
else:
    print("Erreur :", response.status_code, response.text)
```

### Avec JavaScript
```javascript
const API_KEY = "VOTRE_CLE_API";
const url = "https://Fox6768-api-demission-prediction.hf.space/predict/new_employee";

fetch(url, {
  method: 'POST',
  headers: {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    satisfaction_level: 0.75,
    last_evaluation: 0.86,
    number_project: 5,
    average_montly_hours: 200,
    time_spend_company: 4,
    Work_accident: 0,
    promotion_last_5years: 0,
    departement: "IT",
    salary: "medium"
  })
})
.then(response => response.json())
.then(data => console.log("Prédiction :", data))
.catch(error => console.error("Erreur :", error));
```

---

## 🌐 Endpoints

### ✅ Endpoints PUBLICS (sans API Key)

| Endpoint | Description |
|----------|-------------|
| `GET /` | Page d'accueil |
| `GET /health` | Vérifier le statut de l'API |
| `GET /docs` | Documentation Swagger |

### 🔒 Endpoints PROTÉGÉS (API Key requise)

| Endpoint | Description |
|----------|-------------|
| `POST /predict/from_id/{id}` | Prédire depuis un employé existant |
| `POST /predict/new_employee` | Prédire pour un nouvel employé |
| `GET /predict/log/{id}` | Récupérer un log de prédiction |
| `GET /employees` | Liste des employés |
| `GET /employees/{id}` | Détails d'un employé |
| `GET /predictions/logs` | Historique des prédictions |
| `GET /stats` | Statistiques globales |

---

## ⚠️ Erreurs Courantes

### Erreur 401 - API Key manquante

**Message :**
```json
{
  "detail": "❌ API Key manquante. Ajoutez le header 'X-API-Key' à votre requête."
}
```

**Solution :** Ajoutez le header `X-API-Key` avec votre clé.

---

### Erreur 401 - API Key invalide

**Message :**
```json
{
  "detail": "❌ API Key invalide. Vérifiez votre clé d'authentification."
}
```

**Solutions possibles :**
- Vérifiez l'orthographe de la clé (pas d'espace, copie complète)
- Vérifiez que le fichier `.env` est bien chargé
- Contactez l'administrateur pour vérifier la validité de votre clé

---

## 🔒 Bonnes Pratiques

### ✅ À FAIRE

- **Stocker la clé dans `.env`** (jamais dans le code)
- **Ajouter `.env` au `.gitignore`**
- **Utiliser des variables d'environnement** pour la production
- **Ne pas partager votre clé** publiquement

### ❌ À ÉVITER

- ❌ Hard-coder la clé dans le code source
- ❌ Commiter le fichier `.env` sur Git
- ❌ Partager la clé dans des messages publics
- ❌ Utiliser la même clé pour tous les environnements

---

## 📝 Fichier .env

**Créez un fichier `.env` à la racine du projet :**
```bash
# API Key
API_KEY=votre-cle-secrete-ici

# Base de données (si nécessaire)
DATABASE_URL=sqlite:///./hr_analytics.db
```

**Générer une clé sécurisée :**
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🛡️ Sécurité

L'API utilise HTTPS en production (Hugging Face Spaces), ce qui chiffre automatiquement les communications, y compris l'API Key transmise dans le header.

**Configuration du fichier `.gitignore` :**
```gitignore
# Fichiers secrets
.env
*.env

# Base de données locale
*.db
hr_analytics.db
```

---

## 📞 Besoin d'Aide ?

**Problèmes d'authentification :**
- Erreur 401 persistante → Vérifiez votre clé
- Clé perdue → Contactez l'administrateur
- Clé compromise → Signalez immédiatement

**Documentation complète :** [API Endpoints](../api/endpoints.md)