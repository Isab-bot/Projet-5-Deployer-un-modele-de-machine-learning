# Utilisation de l'API

## Authentification

Toutes les requetes necessitent une API Key dans le header :

\\\
X-API-Key: votre_cle_api
\\\

## Endpoints Disponibles

### GET /health

Verifier l'etat de l'API

\\\ash
curl https://Fox6768-api-demission-prediction.hf.space/health
\\\

### POST /predict

Predire le risque de demission

\\\ash
curl -X POST "https://Fox6768-api-demission-prediction.hf.space/predict" \\
  -H "X-API-Key: votre_cle" \\
  -H "Content-Type: application/json" \\
  -d @employee_data.json
\\\

### GET /history

Consulter l'historique des predictions

\\\ash
curl -H "X-API-Key: votre_cle" \\
  https://Fox6768-api-demission-prediction.hf.space/history
\\\

## Formats de Donnees

Voir [Schemas API](../api/schemas.md) pour les details complets.

## Codes de Reponse

- **200** : Succes
- **401** : API Key invalide
- **422** : Donnees invalides
- **500** : Erreur serveur