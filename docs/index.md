# Bienvenue dans la Documentation

Bienvenue dans la documentation complete du **Systeme de Prediction de Demissions d'Employes**.

Cette plateforme utilise un modele de Machine Learning (XGBoost) pour identifier les employes a risque de demission, permettant aux equipes RH d'agir de maniere preventive.

## API en Production

**URL :** [https://Fox6768-api-demission-prediction.hf.space](https://Fox6768-api-demission-prediction.hf.space)

**Documentation Interactive (Swagger) :** [/docs](https://Fox6768-api-demission-prediction.hf.space/docs)

## Performances du Modele

| Metrique | Score | Signification |
|----------|-------|---------------|
| **F2-Score** | 0.6818 | Metrique principale (privilegie Recall) |
| **Precision** | 0.8214 | 82% des alertes sont correctes |
| **Recall** | 0.9474 | 95% des demissions sont detectees |
| **ROC-AUC** | 0.9326 | Excellent pouvoir discriminant |

## Demarrage Rapide

### Pour Utilisateurs de l'API

1. Obtenir une API Key (contact administrateur)
2. Tester l'API via [Swagger UI](https://Fox6768-api-demission-prediction.hf.space/docs)
3. Consulter les [exemples pratiques](user-guide/examples.md)

### Pour Developpeurs

1. Cloner le repository
2. Installer les dependances
3. Lancer l'API localement

Consulte le [Guide d'Installation](getting-started/installation.md)

## Liens Rapides

- [GitHub Repository](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning)
- [Hugging Face Space](https://huggingface.co/spaces/Fox6768/API_demission_prediction)
- [Documentation API](api/endpoints.md)
- [Guide Utilisateur](user-guide/api-usage.md)