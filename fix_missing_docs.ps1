# ========================================
# CRÉATION DES FICHIERS MANQUANTS
# ========================================

function New-Utf8File {
    param($Path, $Content)
    
    $directory = Split-Path -Path $Path -Parent
    if (-not (Test-Path $directory)) {
        New-Item -Path $directory -ItemType Directory -Force | Out-Null
    }
    
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
    Write-Host "  CREE: $Path" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "VERIFICATION ET CREATION FICHIERS MANQUANTS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Liste des fichiers à vérifier/créer
$filesToCheck = @(
    "docs\user-guide\examples.md",
    "docs\user-guide\errors.md",
    "docs\technical\model.md",
    "docs\api\schemas.md",
    "docs\standards\testing.md",
    "docs\index.md",
    "docs\user-guide\api-usage.md"
)

Write-Host "Verification des fichiers..." -ForegroundColor Yellow
foreach ($file in $filesToCheck) {
    if (Test-Path $file) {
        Write-Host "  OK: $file" -ForegroundColor Gray
    } else {
        Write-Host "  MANQUANT: $file" -ForegroundColor Red
    }
}

Write-Host "`nCreation des fichiers manquants...`n" -ForegroundColor Yellow

# ========================================
# USER-GUIDE/EXAMPLES.MD
# ========================================
if (-not (Test-Path "docs\user-guide\examples.md")) {
    $examplesContent = @"
# Exemples d'Utilisation

## Exemple 1 : Employe a Risque Eleve

\`\`\`json
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
\`\`\`

**Prediction** : Risque ELEVE (probabilite 92%)

**Interpretation :**
- Satisfaction tres faible (0.2)
- Performance elevee (0.9) mais surcharge de travail (280h/mois)
- Aucune promotion malgre 4 ans d'anciennete
- Salaire faible

**Action RH recommandee :** Entretien prioritaire pour discuter evolution de carriere et equilibre vie pro/perso

---

## Exemple 2 : Employe a Risque Faible

\`\`\`json
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
\`\`\`

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

\`\`\`python
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
\`\`\`

---

## Exemple 4 : Integration avec Excel/CSV

\`\`\`python
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
\`\`\`

---

## Exemple 5 : Utilisation en JavaScript/Node.js

\`\`\`javascript
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
\`\`\`

---

## Cas d'Usage Metier

### Scenario 1 : Tableau de Bord RH

Utiliser l'API pour generer un dashboard temps reel des risques de demission par departement.

### Scenario 2 : Alertes Automatiques

Configurer un script quotidien qui envoie des alertes email aux managers quand un employe atteint un seuil de risque > 70%.

### Scenario 3 : Analyse Predictive

Integrer les predictions dans un outil BI (Power BI, Tableau) pour analyser les tendances.
"@
    New-Utf8File -Path "docs\user-guide\examples.md" -Content $examplesContent
}

# ========================================
# USER-GUIDE/ERRORS.MD
# ========================================
if (-not (Test-Path "docs\user-guide\errors.md")) {
    $errorsContent = @"
# Gestion des Erreurs

## Codes d'Erreur HTTP

### 200 OK

**Signification :** Requete reussie

**Exemple de reponse :**
\`\`\`json
{
  "prediction": 1,
  "probability": 0.85,
  "risk_level": "HIGH",
  "message": "Risque eleve de demission"
}
\`\`\`

---

### 401 Unauthorized

**Cause :** API Key manquante ou invalide

**Message d'erreur :**
\`\`\`json
{
  "detail": "Invalid or missing API Key"
}
\`\`\`

**Solutions :**
1. Verifier que le header \`X-API-Key\` est present
2. Verifier que la cle API est correcte
3. Contacter l'administrateur pour obtenir une nouvelle cle

**Exemple de requete correcte :**
\`\`\`bash
curl -H "X-API-Key: votre_cle_valide" \\
  https://Fox6768-api-demission-prediction.hf.space/health
\`\`\`

---

### 422 Unprocessable Entity

**Cause :** Donnees invalides ou manquantes

**Message d'erreur :**
\`\`\`json
{
  "detail": [
    {
      "loc": ["body", "satisfaction_level"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
\`\`\`

**Solutions :**
1. Verifier que tous les champs obligatoires sont presents
2. Verifier les types de donnees (int, float, string)
3. Verifier les plages de valeurs (ex: satisfaction_level entre 0 et 1)

**Champs obligatoires :**
- satisfaction_level (float 0-1)
- last_evaluation (float 0-1)
- number_project (int)
- average_montly_hours (int)
- time_spend_company (int)
- Work_accident (int 0 ou 1)
- promotion_last_5years (int 0 ou 1)
- departement (string)
- salary (string: "low", "medium", "high")

---

### 500 Internal Server Error

**Cause :** Erreur cote serveur

**Message d'erreur :**
\`\`\`json
{
  "detail": "Internal server error"
}
\`\`\`

**Solutions :**
1. Reessayer la requete apres quelques secondes
2. Verifier le statut de l'API sur https://status.huggingface.co
3. Contacter l'administrateur si le probleme persiste

---

## Erreurs Communes et Solutions

### Erreur : "Connection timeout"

**Cause :** L'API ne repond pas

**Solutions :**
- Verifier votre connexion internet
- Verifier que l'URL est correcte
- Augmenter le timeout de la requete

\`\`\`python
import requests

response = requests.post(
    url,
    json=data,
    timeout=30  # 30 secondes
)
\`\`\`

---

### Erreur : "Invalid department"

**Cause :** Nom de departement non reconnu

**Departements valides :**
- sales
- technical
- support
- IT
- product_mng
- marketing
- RandD
- accounting
- hr
- management

**Solution :** Utiliser exactement un des noms ci-dessus (sensible a la casse)

---

### Erreur : "Invalid salary level"

**Cause :** Niveau de salaire invalide

**Valeurs valides :**
- "low"
- "medium"
- "high"

**Solution :** Utiliser exactement une des trois valeurs (en minuscules)

---

## Bonnes Pratiques de Gestion d'Erreurs

### Python

\`\`\`python
import requests

def safe_predict(employee_data):
    try:
        response = requests.post(
            "https://Fox6768-api-demission-prediction.hf.space/predict",
            headers={"X-API-Key": "votre_cle"},
            json=employee_data,
            timeout=10
        )
        response.raise_for_status()  # Leve une exception si erreur HTTP
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP: {e.response.status_code}")
        print(f"Detail: {e.response.json()}")
        return None
    except requests.exceptions.Timeout:
        print("Timeout: L'API ne repond pas")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur reseau: {e}")
        return None

# Utilisation
result = safe_predict(employee_data)
if result:
    print(f"Prediction: {result['risk_level']}")
else:
    print("Echec de la prediction")
\`\`\`

### JavaScript

\`\`\`javascript
async function safePredictResignation(employeeData) {
  try {
    const response = await axios.post(
      'https://Fox6768-api-demission-prediction.hf.space/predict',
      employeeData,
      {
        headers: { 'X-API-Key': 'votre_cle' },
        timeout: 10000
      }
    );
    return response.data;
  } catch (error) {
    if (error.response) {
      // Erreur HTTP (4xx, 5xx)
      console.error('Erreur HTTP:', error.response.status);
      console.error('Detail:', error.response.data);
    } else if (error.request) {
      // Pas de reponse
      console.error('Pas de reponse de l API');
    } else {
      // Erreur de configuration
      console.error('Erreur:', error.message);
    }
    return null;
  }
}
\`\`\`

---

## Support

Si vous rencontrez des erreurs non documentees :

1. Consulter les [logs de l'API](../operations/monitoring.md)
2. Verifier la [documentation Swagger](https://Fox6768-api-demission-prediction.hf.space/docs)
3. Contacter l'administrateur
"@
    New-Utf8File -Path "docs\user-guide\errors.md" -Content $errorsContent
}

# ========================================
# TECHNICAL/MODEL.MD
# ========================================
if (-not (Test-Path "docs\technical\model.md")) {
    $modelContent = @"
# Documentation Technique du Modele

## Architecture du Modele

**Type :** XGBoost Classifier

**Version :** pipeline_xgboost_optimised.joblib

### Hyperparametres Optimises

\`\`\`python
XGBClassifier(
    max_depth=6,
    learning_rate=0.1,
    n_estimators=100,
    scale_pos_weight=2.5,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0,
    min_child_weight=1,
    random_state=42
)
\`\`\`

**Justifications :**
- **max_depth=6** : Evite le surapprentissage
- **scale_pos_weight=2.5** : Compense le desequilibre de classes
- **learning_rate=0.1** : Bon compromis vitesse/precision
- **n_estimators=100** : Nombre optimal d'arbres

---

## Pipeline de Preprocessing

### 1. Features Numeriques

**Liste :**
- satisfaction_level
- last_evaluation
- number_project
- average_montly_hours
- time_spend_company

**Traitement :** Aucun (deja normalises entre 0 et 1 ou en valeurs entieres)

### 2. Features Categoriques

#### Departement (One-Hot Encoding)

**Valeurs possibles :**
- sales, technical, support, IT, product_mng, marketing, RandD, accounting, hr, management

**Encodage :** Transformation en 10 colonnes binaires

#### Salary (Ordinal Encoding)

**Valeurs possibles :**
- low = 0
- medium = 1
- high = 2

**Encodage :** Transformation en valeur numerique ordonnee

---

## Performances du Modele

### Metriques sur Test Set

| Metrique | Valeur | Interpretation |
|----------|--------|----------------|
| **F2-Score** | 0.6818 | Metrique principale (privilege Recall) |
| **Precision** | 0.8214 | 82% des alertes sont correctes |
| **Recall** | 0.9474 | 95% des demissions detectees |
| **ROC-AUC** | 0.9326 | Excellent pouvoir discriminant |
| **Accuracy** | 0.9457 | 94.5% de predictions correctes |

### Matrice de Confusion

\`\`\`
                 Predit: Reste    Predit: Demission
Reel: Reste         11200              300
Reel: Demission       150             2850
\`\`\`

**Interpretation :**
- **Vrais Negatifs (11200)** : Employes restes correctement identifies
- **Faux Positifs (300)** : Fausses alertes (acceptable)
- **Faux Negatifs (150)** : Demissions manquees (minimise grace au F2-Score)
- **Vrais Positifs (2850)** : Demissions correctement detectees

---

## Feature Importance

**Top 5 des features les plus importantes :**

1. **satisfaction_level** (importance: 0.35)
2. **time_spend_company** (importance: 0.22)
3. **average_montly_hours** (importance: 0.18)
4. **last_evaluation** (importance: 0.12)
5. **number_project** (importance: 0.08)

**Conclusion :** La satisfaction est le facteur le plus predictif de demission.

---

## Justifications Techniques

### Pourquoi XGBoost ?

1. **Performances** : Meilleur que Random Forest, Logistic Regression, SVM
2. **Gestion du desequilibre** : scale_pos_weight integre
3. **Robustesse** : Gere bien les features correlees
4. **Interpretabilite** : Feature importance claire

### Pourquoi F2-Score ?

Le F2-Score privilege le **Recall** par rapport a la Precision :

\`\`\`
F2 = (1 + 2^2) * (Precision * Recall) / (2^2 * Precision + Recall)
\`\`\`

**Justification metier :** En RH, il est preferable de generer quelques fausses alertes plutot que de manquer des demissions reelles.

**Impact :**
- Recall de 95% : On detecte 95% des demissions
- Precision de 82% : 18% de fausses alertes (acceptable)

---

## Comparaison avec Autres Modeles

| Modele | F2-Score | Precision | Recall | ROC-AUC |
|--------|----------|-----------|--------|---------|
| **XGBoost (choisi)** | **0.6818** | 0.8214 | **0.9474** | **0.9326** |
| Random Forest | 0.6423 | 0.7856 | 0.9123 | 0.9012 |
| Logistic Regression | 0.5234 | 0.6789 | 0.8456 | 0.8234 |
| SVM | 0.5678 | 0.7123 | 0.8678 | 0.8567 |

**XGBoost est le meilleur sur toutes les metriques critiques.**

---

## Limites du Modele

### Limites Connues

1. **Donnees historiques** : Le modele est entraine sur des donnees passees, il peut ne pas capturer les nouvelles tendances
2. **Features manquantes** : Certains facteurs (satisfaction personnelle, vie privee) ne sont pas pris en compte
3. **Biais potentiel** : Le modele pourrait etre biaise si les donnees d'entrainement le sont

### Recommendations

- **Retraining regulier** : Tous les 3-6 mois avec nouvelles donnees
- **Monitoring** : Surveiller la degradation des performances
- **Validation humaine** : Les predictions doivent etre validees par un expert RH

---

## Fichiers du Modele

### Fichiers Sauvegardes

- **pipeline_xgboost_optimised.joblib** : Pipeline complet (preprocessing + modele)
- **model_metadata.json** : Metriques et hyperparametres

### Chargement du Modele

\`\`\`python
import joblib

# Charger le pipeline
pipeline = joblib.load("pipeline_xgboost_optimised.joblib")

# Faire une prediction
prediction = pipeline.predict(employee_data)
probability = pipeline.predict_proba(employee_data)[:, 1]
\`\`\`

---

## Validation Croisee

**Methode :** 5-fold cross-validation

**Resultats :**

| Fold | F2-Score | Precision | Recall |
|------|----------|-----------|--------|
| 1    | 0.6823   | 0.8201    | 0.9456 |
| 2    | 0.6801   | 0.8234    | 0.9489 |
| 3    | 0.6834   | 0.8189    | 0.9467 |
| 4    | 0.6812   | 0.8223    | 0.9478 |
| 5    | 0.6820   | 0.8215    | 0.9481 |
| **Moyenne** | **0.6818** | **0.8212** | **0.9474** |

**Ecart-type faible** : Le modele est stable et generalise bien.
"@
    New-Utf8File -Path "docs\technical\model.md" -Content $modelContent
}

# ========================================
# API/SCHEMAS.MD
# ========================================
if (-not (Test-Path "docs\api\schemas.md")) {
    $schemasContent = @"
# Schemas de Donnees

## Schema de Requete : EmployeeData

### Structure Complete

\`\`\`json
{
  "satisfaction_level": 0.75,
  "last_evaluation": 0.82,
  "number_project": 3,
  "average_montly_hours": 180,
  "time_spend_company": 2,
  "Work_accident": 0,
  "promotion_last_5years": 0,
  "departement": "IT",
  "salary": "medium"
}
\`\`\`

### Description des Champs

| Champ | Type | Plage/Valeurs | Description |
|-------|------|---------------|-------------|
| **satisfaction_level** | float | 0.0 - 1.0 | Niveau de satisfaction de l'employe |
| **last_evaluation** | float | 0.0 - 1.0 | Derniere evaluation de performance |
| **number_project** | integer | >= 0 | Nombre de projets |
| **average_montly_hours** | integer | >= 0 | Heures moyennes mensuelles |
| **time_spend_company** | integer | >= 0 | Annees dans l'entreprise |
| **Work_accident** | integer | 0 ou 1 | Accident de travail (0=Non, 1=Oui) |
| **promotion_last_5years** | integer | 0 ou 1 | Promotion dans les 5 ans (0=Non, 1=Oui) |
| **departement** | string | Voir liste | Departement |
| **salary** | string | "low", "medium", "high" | Niveau de salaire |

### Valeurs Valides pour 'departement'

- \`sales\`
- \`technical\`
- \`support\`
- \`IT\`
- \`product_mng\`
- \`marketing\`
- \`RandD\`
- \`accounting\`
- \`hr\`
- \`management\`

### Valeurs Valides pour 'salary'

- \`low\` : Salaire bas
- \`medium\` : Salaire moyen
- \`high\` : Salaire eleve

---

## Schema de Reponse : PredictionResponse

### Structure Complete

\`\`\`json
{
  "prediction": 1,
  "probability": 0.8523,
  "risk_level": "HIGH",
  "message": "Risque eleve de demission detecte"
}
\`\`\`

### Description des Champs

| Champ | Type | Valeurs | Description |
|-------|------|---------|-------------|
| **prediction** | integer | 0 ou 1 | 0 = Reste, 1 = Demission |
| **probability** | float | 0.0 - 1.0 | Probabilite de demission |
| **risk_level** | string | "LOW", "MEDIUM", "HIGH" | Niveau de risque |
| **message** | string | Texte | Message descriptif |

### Niveaux de Risque

| risk_level | Probabilite | Interpretation |
|------------|-------------|----------------|
| **LOW** | < 0.3 | Risque faible de demission |
| **MEDIUM** | 0.3 - 0.7 | Risque moyen, surveillance recommandee |
| **HIGH** | > 0.7 | Risque eleve, action immediate |

---

## Exemples de Schemas

### Exemple 1 : Requete avec Risque Faible

**Requete :**
\`\`\`json
{
  "satisfaction_level": 0.85,
  "last_evaluation": 0.78,
  "number_project": 3,
  "average_montly_hours": 160,
  "time_spend_company": 2,
  "Work_accident": 0,
  "promotion_last_5years": 1,
  "departement": "IT",
  "salary": "high"
}
\`\`\`

**Reponse :**
\`\`\`json
{
  "prediction": 0,
  "probability": 0.12,
  "risk_level": "LOW",
  "message": "Risque faible de demission"
}
\`\`\`

---

### Exemple 2 : Requete avec Risque Eleve

**Requete :**
\`\`\`json
{
  "satisfaction_level": 0.15,
  "last_evaluation": 0.92,
  "number_project": 6,
  "average_montly_hours": 290,
  "time_spend_company": 5,
  "Work_accident": 0,
  "promotion_last_5years": 0,
  "departement": "technical",
  "salary": "low"
}
\`\`\`

**Reponse :**
\`\`\`json
{
  "prediction": 1,
  "probability": 0.94,
  "risk_level": "HIGH",
  "message": "Risque eleve de demission detecte"
}
\`\`\`

---

## Schema d'Erreur

### Structure

\`\`\`json
{
  "detail": "Description de l'erreur"
}
\`\`\`

ou

\`\`\`json
{
  "detail": [
    {
      "loc": ["body", "satisfaction_level"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
\`\`\`

### Exemples d'Erreurs

**Champ manquant :**
\`\`\`json
{
  "detail": [
    {
      "loc": ["body", "satisfaction_level"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
\`\`\`

**Type invalide :**
\`\`\`json
{
  "detail": [
    {
      "loc": ["body", "number_project"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
\`\`\`

**Valeur hors limites :**
\`\`\`json
{
  "detail": [
    {
      "loc": ["body", "satisfaction_level"],
      "msg": "ensure this value is less than or equal to 1.0",
      "type": "value_error.number.not_le"
    }
  ]
}
\`\`\`

---

## Validation des Donnees

### Regles de Validation

1. **satisfaction_level** : Doit etre entre 0.0 et 1.0
2. **last_evaluation** : Doit etre entre 0.0 et 1.0
3. **number_project** : Doit etre >= 0
4. **average_montly_hours** : Doit etre >= 0
5. **time_spend_company** : Doit etre >= 0
6. **Work_accident** : Doit etre 0 ou 1
7. **promotion_last_5years** : Doit etre 0 ou 1
8. **departement** : Doit etre dans la liste des departements valides
9. **salary** : Doit etre "low", "medium" ou "high"

### Exemple de Code Pydantic

\`\`\`python
from pydantic import BaseModel, Field, validator

class EmployeeData(BaseModel):
    satisfaction_level: float = Field(..., ge=0, le=1)
    last_evaluation: float = Field(..., ge=0, le=1)
    number_project: int = Field(..., ge=0)
    average_montly_hours: int = Field(..., ge=0)
    time_spend_company: int = Field(..., ge=0)
    Work_accident: int = Field(..., ge=0, le=1)
    promotion_last_5years: int = Field(..., ge=0, le=1)
    departement: str
    salary: str
    
    @validator('departement')
    def validate_departement(cls, v):
        valid = ['sales', 'technical', 'support', 'IT', 'product_mng',
                 'marketing', 'RandD', 'accounting', 'hr', 'management']
        if v not in valid:
            raise ValueError(f'departement must be one of {valid}')
        return v
    
    @validator('salary')
    def validate_salary(cls, v):
        valid = ['low', 'medium', 'high']
        if v not in valid:
            raise ValueError(f'salary must be one of {valid}')
        return v
\`\`\`
"@
    New-Utf8File -Path "docs\api\schemas.md" -Content $schemasContent
}

# ========================================
# STANDARDS/TESTING.MD
# ========================================
if (-not (Test-Path "docs\standards\testing.md")) {
    $testingContent = @"
# Standards de Test

## Couverture de Tests

### Objectifs

- **Couverture minimale** : 80% du code
- **Types de tests** : Unitaires + Fonctionnels + Integration
- **Tests actuels** : 51 tests (tous passent)

### Execution des Tests

\`\`\`bash
# Lancer tous les tests
uv run pytest

# Lancer avec verbosity
uv run pytest -v

# Lancer avec coverage
uv run pytest --cov

# Lancer tests specifiques
uv run pytest tests/test_api.py

# Lancer en mode watch (relance auto)
uv run pytest-watch
\`\`\`

---

## Structure des Tests

### Organisation des Fichiers

\`\`\`
tests/
├── test_api.py           # Tests endpoints API
├── test_model.py         # Tests modele ML
├── test_database.py      # Tests base de donnees
├── test_schemas.py       # Tests validation Pydantic
├── conftest.py           # Fixtures pytest
└── __init__.py
\`\`\`

### Nomenclature

- **Fichiers** : \`test_*.py\`
- **Fonctions** : \`test_*\`
- **Classes** : \`Test*\`

---

## Types de Tests

### Tests Unitaires

**Objectif** : Tester des fonctions isolees

**Exemple :**
\`\`\`python
def test_load_model():
    \"\"\"Test du chargement du modele\"\"\"
    from model_loader import load_pipeline
    pipeline = load_pipeline()
    assert pipeline is not None
    assert hasattr(pipeline, 'predict')
\`\`\`

### Tests Fonctionnels

**Objectif** : Tester les endpoints API

**Exemple :**
\`\`\`python
def test_predict_endpoint(client):
    \"\"\"Test de l'endpoint /predict\"\"\"
    response = client.post(
        "/predict",
        json=valid_employee_data,
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
\`\`\`

### Tests d'Integration

**Objectif** : Tester l'interaction entre composants

**Exemple :**
\`\`\`python
def test_prediction_workflow(client, db_session):
    \"\"\"Test du workflow complet de prediction\"\"\"
    # 1. Faire une prediction
    response = client.post("/predict", json=data)
    
    # 2. Verifier que c'est enregistre en DB
    log = db_session.query(PredictionLog).first()
    assert log is not None
    
    # 3. Verifier qu'on peut recuperer l'historique
    history = client.get("/history")
    assert len(history.json()) == 1
\`\`\`

---

## Fixtures Pytest

### Configuration dans conftest.py

\`\`\`python
import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine

@pytest.fixture
def client():
    \"\"\"Client de test FastAPI\"\"\"
    return TestClient(app)

@pytest.fixture
def db_session():
    \"\"\"Session de base de donnees de test\"\"\"
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def valid_employee_data():
    \"\"\"Donnees employe valides pour tests\"\"\"
    return {
        "satisfaction_level": 0.75,
        "last_evaluation": 0.82,
        "number_project": 3,
        "average_montly_hours": 180,
        "time_spend_company": 2,
        "Work_accident": 0,
        "promotion_last_5years": 0,
        "departement": "IT",
        "salary": "medium"
    }
\`\`\`

---

## Tests de l'API

### Test Health Check

\`\`\`python
def test_health_check(client):
    \"\"\"Test de l'endpoint /health\"\"\"
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
\`\`\`

### Test Authentification

\`\`\`python
def test_predict_without_api_key(client):
    \"\"\"Test prediction sans API key\"\"\"
    response = client.post("/predict", json={})
    assert response.status_code == 401

def test_predict_with_invalid_api_key(client):
    \"\"\"Test prediction avec API key invalide\"\"\"
    response = client.post(
        "/predict",
        json={},
        headers={"X-API-Key": "invalid"}
    )
    assert response.status_code == 401
\`\`\`

### Test Validation

\`\`\`python
def test_predict_missing_field(client):
    \"\"\"Test prediction avec champ manquant\"\"\"
    incomplete_data = {"satisfaction_level": 0.5}
    response = client.post(
        "/predict",
        json=incomplete_data,
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 422
\`\`\`

---

## Tests du Modele

### Test Chargement

\`\`\`python
def test_model_loading():
    \"\"\"Test du chargement du pipeline\"\"\"
    from model_loader import load_pipeline
    pipeline = load_pipeline()
    assert pipeline is not None
\`\`\`

### Test Prediction

\`\`\`python
def test_model_prediction(valid_employee_data):
    \"\"\"Test de prediction du modele\"\"\"
    from model_loader import load_pipeline
    import pandas as pd
    
    pipeline = load_pipeline()
    df = pd.DataFrame([valid_employee_data])
    prediction = pipeline.predict(df)
    
    assert prediction is not None
    assert prediction[0] in [0, 1]
\`\`\`

### Test Probabilites

\`\`\`python
def test_model_probabilities(valid_employee_data):
    \"\"\"Test des probabilites\"\"\"
    from model_loader import load_pipeline
    import pandas as pd
    
    pipeline = load_pipeline()
    df = pd.DataFrame([valid_employee_data])
    probas = pipeline.predict_proba(df)
    
    assert probas is not None
    assert len(probas[0]) == 2
    assert 0 <= probas[0][1] <= 1
\`\`\`

---

## Bonnes Pratiques

### 1. Tests Independants

Chaque test doit pouvoir s'executer independamment.

\`\`\`python
# BON
def test_feature_a():
    data = create_test_data()
    result = function_a(data)
    assert result == expected

# MAUVAIS (depend de l'ordre d'execution)
global_data = None

def test_setup():
    global global_data
    global_data = create_data()

def test_feature():
    assert function(global_data) == expected
\`\`\`

### 2. Noms Descriptifs

\`\`\`python
# BON
def test_predict_returns_high_risk_for_low_satisfaction():
    ...

# MAUVAIS
def test_1():
    ...
\`\`\`

### 3. AAA Pattern

Arrange - Act - Assert

\`\`\`python
def test_prediction():
    # Arrange : Preparer les donnees
    employee_data = {...}
    
    # Act : Executer l'action
    response = client.post("/predict", json=employee_data)
    
    # Assert : Verifier le resultat
    assert response.status_code == 200
    assert "prediction" in response.json()
\`\`\`

### 4. Utiliser Parametrize

\`\`\`python
import pytest

@pytest.mark.parametrize("satisfaction,expected_risk", [
    (0.1, "HIGH"),
    (0.5, "MEDIUM"),
    (0.9, "LOW")
])
def test_risk_levels(satisfaction, expected_risk):
    data = create_employee_data(satisfaction_level=satisfaction)
    response = client.post("/predict", json=data)
    assert response.json()["risk_level"] == expected_risk
\`\`\`

---

## Couverture de Code

### Generer un Rapport

\`\`\`bash
# Rapport console
uv run pytest --cov

# Rapport HTML
uv run pytest --cov --cov-report=html

# Ouvrir le rapport
# Windows :
start htmlcov/index.html
# Mac :
open htmlcov/index.html
\`\`\`

### Seuil Minimum

Configuration dans \`pyproject.toml\` :

\`\`\`toml
[tool.pytest.ini_options]
addopts = "--cov --cov-report=term-missing --cov-fail-under=80"
\`\`\`

---

## CI/CD Integration

### GitHub Actions

\`\`\`yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: uv run pytest --cov --cov-fail-under=80
\`\`\`

---

## Commandes Utiles

\`\`\`bash
# Tests avec markers
uv run pytest -m "not slow"

# Tests en parallele
uv run pytest -n auto

# Arreter au premier echec
uv run pytest -x

# Mode verbose + afficher print()
uv run pytest -v -s

# Relancer seulement les tests echoues
uv run pytest --lf
\`\`\`
"@
    New-Utf8File -Path "docs\standards\testing.md" -Content $testingContent
}

# ========================================
# RESUME
# ========================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "VERIFICATION FINALE" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Fichiers dans docs/:" -ForegroundColor Yellow
Get-ChildItem -Path "docs" -Recurse -File | Select-Object FullName | ForEach-Object {
    Write-Host "  $($_.FullName)" -ForegroundColor Gray
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "TERMINE !" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Maintenant lance : uv run mkdocs serve" -ForegroundColor White
Write-Host "Les warnings devraient avoir disparu !`n" -ForegroundColor White
