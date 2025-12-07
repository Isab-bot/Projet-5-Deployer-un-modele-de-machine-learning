# Architecture Technique

## Stack Technologique

- **API** : FastAPI 0.115.5
- **ML** : XGBoost + scikit-learn
- **Database** : SQLite
- **Deploiement** : Docker + Hugging Face Spaces
- **CI/CD** : GitHub Actions
- **Tests** : pytest (51 tests)

## Composants Principaux

### API Layer

FastAPI avec endpoints REST securises

### Model Layer

Pipeline XGBoost avec preprocessing integre

### Data Layer

SQLite pour l'historique des predictions

### Deployment

Docker + Hugging Face Spaces pour la haute disponibilite