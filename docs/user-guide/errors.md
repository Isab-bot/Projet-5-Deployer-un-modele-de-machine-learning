# Gestion des Erreurs

## Codes d'Erreur HTTP

### 200 OK

**Signification :** Requete reussie

**Exemple de reponse :**
```json
{
  "prediction": 1,
  "probability": 0.85,
  "risk_level": "HIGH",
  "message": "Risque eleve de demission"
}
```

---

### 401 Unauthorized

**Cause :** API Key manquante ou invalide

**Message d'erreur :**
```json
{
  "detail": "Invalid or missing API Key"
}
```

**Solutions :**
1. Verifier que le header `X-API-Key` est present
2. Verifier que la cle API est correcte
3. Contacter l'administrateur pour obtenir une nouvelle cle

**Exemple de requete correcte :**
```bash
curl -H "X-API-Key: votre_cle_valide" \
  https://Fox6768-api-demission-prediction.hf.space/health
```

---

### 422 Unprocessable Entity

**Cause :** Donnees invalides ou manquantes

**Message d'erreur :**
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
```json
{
  "detail": "Internal server error"
}
```

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
```python
import requests

response = requests.post(
    url,
    json=data,
    timeout=30  # 30 secondes
)
```

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
```python
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
```

### JavaScript
```javascript
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
```

---

## Support

Si vous rencontrez des erreurs non documentees :

1. Consulter les [logs de l'API](../operations/monitoring.md)
2. Verifier la [documentation Swagger](https://Fox6768-api-demission-prediction.hf.space/docs)
3. Contacter l'administrateur