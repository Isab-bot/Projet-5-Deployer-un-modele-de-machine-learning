# Documentation des Endpoints

## GET /health

**Description** : Verifier l'etat de l'API

**Reponse** :
\\\json
{"status": "healthy"}
\\\

## POST /predict

**Description** : Predire le risque de demission

**Body** : EmployeeData (voir schemas)

**Reponse** : PredictionResponse

## GET /history

**Description** : Historique des predictions

**Headers** : X-API-Key

**Reponse** : Liste de predictions