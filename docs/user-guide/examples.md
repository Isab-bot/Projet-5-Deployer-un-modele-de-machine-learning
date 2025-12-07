# Exemples d'Utilisation

## Exemple 1 : Employe a Risque Eleve
```json
{
  "satisfaction_level": 0.2,
  "last_evaluation": 0.9,
  "number_project": 5,
  "average_montly_hours": 280,
  "time_spend_company": 4,
  "Work_accident": 0,
  "promotion_last_5years": 0,
  "departement": "technical",
  "salary": "low"
}
```

**Prediction** : Risque ELEVE (probabilite 92%)

**Interpretation :**
- Satisfaction tres faible (0.2)
- Performance elevee (0.9) mais surcharge de travail (280h/mois)
- Aucune promotion malgre 4 ans d'anciennete
- Salaire faible

**Action RH recommandee :** Entretien prioritaire pour discuter evolution de carriere et equilibre vie pro/perso

---

## Exemple 2 : Employe a Risque Faible
```json
{
  "satisfaction_level": 0.8,
  "last_evaluation": 0.75,
  "number_project": 3,
  "average_montly_hours": 160,
  "time_spend_company": 2,
  "Work_accident": 0,
  "promotion_last_5years": 1,
  "departement": "management",
  "salary": "high"
}
```

**Prediction** : Risque FAIBLE (probabilite 8%)

**Interpretation :**
- Tres satisfait (0.8)
- Bonne evaluation (0.75)
- Charge de travail normale (160h)
- Promotion recente
- Salaire eleve

**Action RH recommandee :** Suivi de routine, employe engage

---

## Exemple 3 : Batch de Predictions (Python)
```python
import requests
import pandas as pd

# Liste d'employes
employees = [
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
    },
    {
        "satisfaction_level": 0.92,
        "last_evaluation": 0.85,
        "number_project": 4,
        "average_montly_hours": 200,
        "time_spend_company": 5,
        "Work_accident": 0,
        "promotion_last_5years": 1,
        "departement": "technical",
        "salary": "high"
    }
]

# API endpoint
url = "https://Fox6768-api-demission-prediction.hf.space/predict"
headers = {"X-API-Key": "votre_cle_api"}

# Boucle de predictions
results = []
for emp in employees:
    response = requests.post(url, headers=headers, json=emp)
    if response.status_code == 200:
        results.append(response.json())
        print(f"Employe {emp['departement']}: {response.json()['risk_level']}")
    else:
        print(f"Erreur: {response.status_code}")

# Sauvegarde en CSV
df = pd.DataFrame(results)
df.to_csv("predictions_batch.csv", index=False)
```

---

## Exemple 4 : Integration avec Excel/CSV
```python
import pandas as pd
import requests

# Charger fichier CSV avec donnees employes
df = pd.read_csv("employes.csv")

# Fonction de prediction
def predict_employee(row):
    data = {
        "satisfaction_level": row["satisfaction_level"],
        "last_evaluation": row["last_evaluation"],
        "number_project": row["number_project"],
        "average_montly_hours": row["average_montly_hours"],
        "time_spend_company": row["time_spend_company"],
        "Work_accident": row["Work_accident"],
        "promotion_last_5years": row["promotion_last_5years"],
        "departement": row["departement"],
        "salary": row["salary"]
    }
    
    response = requests.post(
        "https://Fox6768-api-demission-prediction.hf.space/predict",
        headers={"X-API-Key": "votre_cle"},
        json=data
    )
    return response.json()

# Appliquer predictions
df["prediction"] = df.apply(lambda row: predict_employee(row)["prediction"], axis=1)
df["probability"] = df.apply(lambda row: predict_employee(row)["probability"], axis=1)
df["risk_level"] = df.apply(lambda row: predict_employee(row)["risk_level"], axis=1)

# Sauvegarder resultats
df.to_csv("employes_avec_predictions.csv", index=False)
print(f"Predictions terminees pour {len(df)} employes")
```

---

## Exemple 5 : Utilisation en JavaScript/Node.js
```javascript
const axios = require('axios');

async function predictResignation(employeeData) {
  try {
    const response = await axios.post(
      'https://Fox6768-api-demission-prediction.hf.space/predict',
      employeeData,
      {
        headers: {
          'X-API-Key': 'votre_cle_api',
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log('Prediction:', response.data);
    return response.data;
  } catch (error) {
    console.error('Erreur:', error.response?.data || error.message);
  }
}

// Exemple d'utilisation
const employee = {
  satisfaction_level: 0.45,
  last_evaluation: 0.68,
  number_project: 3,
  average_montly_hours: 180,
  time_spend_company: 2,
  Work_accident: 0,
  promotion_last_5years: 0,
  departement: 'IT',
  salary: 'medium'
};

predictResignation(employee);
```

---

## Cas d'Usage Metier

### Scenario 1 : Tableau de Bord RH

Utiliser l'API pour generer un dashboard temps reel des risques de demission par departement.

### Scenario 2 : Alertes Automatiques

Configurer un script quotidien qui envoie des alertes email aux managers quand un employe atteint un seuil de risque > 70%.

### Scenario 3 : Analyse Predictive

Integrer les predictions dans un outil BI (Power BI, Tableau) pour analyser les tendances.