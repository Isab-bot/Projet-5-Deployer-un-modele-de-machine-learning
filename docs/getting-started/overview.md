# Vue d'Ensemble

## Objectif du Projet

Le systeme de prediction de demissions permet aux equipes RH d'identifier proactivement les employes a risque de demission.

## Approche Machine Learning

- **Modele** : XGBoost Classifier
- **Metrique principale** : F2-Score (privilege le Recall)
- **Performances** : 95% de detection des demissions

## Architecture Globale

1. **API FastAPI** : Interface REST securisee
2. **Modele XGBoost** : Predictions en temps reel
3. **Base de donnees SQLite** : Historique des predictions
4. **Deploiement Hugging Face** : Haute disponibilite

## Cas d'Usage

### Pour les RH

- Identifier les employes a risque
- Planifier des entretiens preventifs
- Suivre l'evolution du risque

### Pour les Managers

- Consulter les alertes de leur equipe
- Analyser les facteurs de risque
- Prendre des mesures correctives