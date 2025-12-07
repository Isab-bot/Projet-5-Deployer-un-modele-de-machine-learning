# Schemas de Donnees

## Schema de Requete : EmployeeData

### Structure Complete
```json
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
```

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

- `sales`
- `technical`
- `support`
- `IT`
- `product_mng`
- `marketing`
- `RandD`
- `accounting`
- `hr`
- `management`

### Valeurs Valides pour 'salary'

- `low` : Salaire bas
- `medium` : Salaire moyen
- `high` : Salaire eleve

---

## Schema de Reponse : PredictionResponse

### Structure Complete
```json
{
  "prediction": 1,
  "probability": 0.8523,
  "risk_level": "HIGH",
  "message": "Risque eleve de demission detecte"
}
```

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
```json
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
```

**Reponse :**
```json
{
  "prediction": 0,
  "probability": 0.12,
  "risk_level": "LOW",
  "message": "Risque faible de demission"
}
```

---

### Exemple 2 : Requete avec Risque Eleve

**Requete :**
```json
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
```

**Reponse :**
```json
{
  "prediction": 1,
  "probability": 0.94,
  "risk_level": "HIGH",
  "message": "Risque eleve de demission detecte"
}
```

---

## Schema d'Erreur

### Structure
```json
{
  "detail": "Description de l'erreur"
}
```

ou
```json
{
  "detail": [
    {
      "loc": ["body", "satisfaction_level"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Exemples d'Erreurs

**Champ manquant :**
```json
{
  "detail": [
    {
      "loc": ["body", "satisfaction_level"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Type invalide :**
```json
{
  "detail": [
    {
      "loc": ["body", "number_project"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

**Valeur hors limites :**
```json
{
  "detail": [
    {
      "loc": ["body", "satisfaction_level"],
      "msg": "ensure this value is less than or equal to 1.0",
      "type": "value_error.number.not_le"
    }
  ]
}
```

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
```python
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
```