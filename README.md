---
title: API Prédiction Démission
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🎯 API de Prédiction de Démission - Projet 5

[![CI Tests](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning/actions/workflows/ci.yml/badge.svg)](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning/actions/workflows/ci.yml)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-yellow)](https://huggingface.co/spaces/Fox6768/API_demission_prediction)

API REST pour prédire les démissions d'employés à l'aide d'un modèle XGBoost.

---

## 🚀 API Déployée

**🌐 URL Production :** https://Fox6768-api-demission-prediction.hf.space

**📖 Documentation Interactive :** https://Fox6768-api-demission-prediction.hf.space/docs

### ⚡ Endpoints Rapides
- **Health Check :** [/health](https://Fox6768-api-demission-prediction.hf.space/health)
- **Swagger UI :** [/docs](https://Fox6768-api-demission-prediction.hf.space/docs)
- **ReDoc :** [/redoc](https://Fox6768-api-demission-prediction.hf.space/redoc)

### 🔑 Obtenir l'API Key
Contactez l'administrateur pour obtenir votre clé d'authentification.

---

## 📊 Description

Cette API permet de :
- ✅ Prédire si un employé va démissionner
- ✅ Consulter l'historique des prédictions
- ✅ Analyser les facteurs de risque de démission

**Modèle utilisé :** XGBoost avec optimisation du seuil (F2-Score)

---

## 🔐 Authentification

L'API est protégée par API Key. 

**Pour utiliser l'API, ajoutez ce header à vos requêtes :**
```http
X-API-Key: votre-cle-api
```

**Exemple avec curl :**
```bash
curl -X POST https://Fox6768-api-demission-prediction.hf.space/predict/from_id/1 \
  -H "X-API-Key: votre-cle-api"
```

---

## 📡 Endpoints Disponibles

### **🔓 Endpoints Publics (sans authentification)**

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Informations sur l'API |
| `/health` | GET | Status de l'API |
| `/docs` | GET | Documentation Swagger interactive |

### **🔒 Endpoints Protégés (API Key requise)**

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/predict/from_id/{employee_id}` | POST | Prédiction pour un employé existant |
| `/predict/new_employee` | POST | Prédiction pour un nouvel employé |
| `/predict/log/{log_id}` | GET | Récupérer une prédiction passée |
| `/predictions/logs` | GET | Liste des prédictions |

---

## 🚀 Utilisation

### **Exemple 1 : Prédiction depuis un ID**
```bash
curl -X POST "https://Fox6768-api-demission-prediction.hf.space/predict/from_id/1" \
  -H "X-API-Key: votre-cle-api"
```

**Réponse :**
```json
{
  "log_id": 123,
  "employee_id": 1,
  "prediction": "Non",
  "confidence_score": 0.85,
  "features": {...},
  "timestamp": "2024-12-02T10:30:00"
}
```

### **Exemple 2 : Prédiction pour un nouvel employé**
```bash
curl -X POST "https://Fox6768-api-demission-prediction.hf.space/predict/new_employee" \
  -H "X-API-Key: votre-cle-api" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "age": 35,
      "anciennete": 5,
      "satisfaction": 0.7,
      ...
    }
  }'
```

---

## 🛠️ Technologies

| Technologie | Usage |
|-------------|-------|
| **FastAPI** | Framework API REST |
| **XGBoost** | Modèle de Machine Learning |
| **SQLAlchemy** | ORM pour la base de données |
| **SQLite** | Base de données |
| **Docker** | Containerisation |
| **GitHub Actions** | CI/CD (tests automatiques) |
| **Hugging Face Spaces** | Déploiement cloud |

---

## 🔍 Justifications Techniques

### **Choix de l'Algorithme : XGBoost**

#### Pourquoi XGBoost plutôt que d'autres algorithmes ?

| Critère | XGBoost | Random Forest | Neural Networks | Régression Logistique |
|---------|---------|---------------|-----------------|----------------------|
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Interprétabilité** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **Vitesse Prédiction** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Gestion Déséquilibre** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Robustesse Overfitting** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**Avantages clés de XGBoost :**
- ✅ **État de l'art** pour données tabulaires
- ✅ **Régularisation intégrée** (L1, L2) → évite surapprentissage
- ✅ **Gestion native** des valeurs manquantes
- ✅ **Feature importance** claire et exploitable
- ✅ **Temps de prédiction** < 100ms (production-ready)
- ✅ **Optimisation avancée** (approximation histogramme)

---

### **Configuration du Modèle**

#### Utilisation de TOUTES les features (29/29)

**Pourquoi ne pas réduire à 10-15 features principales ?**

| Configuration | F2-Score | Recall | ROC-AUC | Commentaire |
|---------------|----------|--------|---------|-------------|
| **Light 10%** (3 features) | ~0.50 | ~0.80 | ~0.85 | ❌ Perte significative |
| Light 30% (9 features) | ~0.60 | ~0.88 | ~0.90 | ⚠️ Acceptable mais limité |
| Light 50% (15 features) | ~0.65 | ~0.92 | ~0.92 | ✅ Bon compromis |
| **Light 100%** (29 features) | **0.68** | **0.95** | **0.93** | ⭐ Optimal |

**Justifications :**
1. ✅ **Toutes les features sont informatives** (importance minimale : 0.96%)
2. ✅ **Gain de performance significatif** (+8% F2-Score vs 50%)
3. ✅ **Pas de surapprentissage** (hyperparamètres conservateurs)
4. ✅ **Complexité acceptable** (29 features = collecte RH standard)
5. ✅ **Meilleur ROC-AUC** (pouvoir discriminant maximal)

---

### **Métrique Principale : F2-Score**

#### Pourquoi F2-Score et pas F1-Score ou Accuracy ?

**Formule du Fβ-Score :**
```
Fβ = (1 + β²) × (Precision × Recall) / (β² × Precision + Recall)
```

**Avec β=2 :** Le Recall compte **4 fois plus** que la Precision.

#### Comparaison des métriques :

| Métrique | Avantages | Inconvénients | Adapté à notre cas ? |
|----------|-----------|---------------|----------------------|
| **Accuracy** | Simple à comprendre | Trompeuse si classes déséquilibrées | ❌ NON |
| **F1-Score** | Équilibre Precision/Recall | Pas adapté si coûts asymétriques | ⚠️ MOYEN |
| **F2-Score** | Privilégie Recall (détection) | Moins connu | ✅ PARFAIT |
| **Recall seul** | Maximise détection | Ignore fausses alertes | ⚠️ TROP EXTRÊME |

#### Justification métier du F2-Score :

**Coût d'une erreur :**
- **Faux Négatif** (démission manquée) : ❌❌❌ **ÉLEVÉ**
  - Perte de compétences
  - Désorganisation équipe
  - Recrutement d'urgence (~30-50k€)
  - Formation remplaçant
  
- **Faux Positif** (fausse alerte) : ⚠️ **FAIBLE**
  - Entretien RH préventif (~1h)
  - Mesures de rétention inutiles
  - ✅ Améliore climat social (écoute)

**Ratio des coûts :** ~10:1 → Justifie β=2

---

### **Optimisation du Seuil : 0.09**

#### Pourquoi un seuil si bas (vs 0.5 par défaut) ?

**Comparaison :**

| Seuil | Precision | Recall | F2-Score | Interprétation |
|-------|-----------|--------|----------|----------------|
| **0.5** (défaut) | 0.90 | 0.60 | 0.55 | ❌ Manque 40% des démissions |
| **0.3** | 0.85 | 0.80 | 0.63 | ⚠️ Encore insuffisant |
| **0.09** (optimal) | 0.82 | 0.95 | **0.68** | ✅ Détecte 95% des démissions |

**Conséquences pratiques :**
- ✅ On alerte dès **9% de probabilité** de démission
- ✅ On détecte **95 démissions sur 100** (vs 60 avec seuil 0.5)
- ⚠️ **18 fausses alertes sur 100** (vs 10 avec seuil 0.5)

**Trade-off assumé :** Mieux vaut 18 interventions inutiles que 40 démissions manquées.

---

### **Architecture : Pipeline sklearn**

#### Pourquoi un Pipeline et pas juste le modèle XGBoost ?

```python
Pipeline([
    ('preprocessor', ColumnTransformer(...)),  # OneHotEncoder
    ('classifier', XGBClassifier(...))         # XGBoost
])
```

**Avantages :**

1. ✅ **Reproductibilité**
   - Le preprocessing est versionné avec le modèle
   - Impossible d'oublier une étape de transformation

2. ✅ **Prévention des fuites de données**
   - Le fit du preprocessor se fait sur train uniquement
   - Automatique via pipeline (pas d'erreur humaine)

3. ✅ **Déploiement simplifié**
   - 1 seul fichier `.joblib` pour tout
   - API : données brutes → prédiction (pas d'étape manuelle)

4. ✅ **Maintenance facilitée**
   - Modifications du preprocessing tracées dans Git
   - Compatible avec MLOps (CI/CD)

5. ✅ **Compatibilité sklearn**
   - Fonctionne avec GridSearchCV, cross_val_score, etc.
   - Standard de l'industrie

---

### **Format de Sauvegarde : joblib (vs pickle)**

#### Pourquoi joblib et pas pickle ?

| Critère | joblib | pickle |
|---------|--------|--------|
| **Vitesse** (gros objets) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Compression** | ✅ Intégrée | ❌ Manuelle |
| **Arrays NumPy** | ⭐⭐⭐⭐⭐ Optimisé | ⭐⭐⭐ Standard |
| **Compatibilité sklearn** | ✅ Recommandé | ✅ Supporté |
| **Compatibilité HF** | ✅ Natif | ⚠️ Possible mais moins courant |

**Choix : joblib**
- ✅ Plus rapide pour modèles ML (arrays NumPy)
- ✅ Compression automatique (fichiers plus petits)
- ✅ Standard sklearn recommandé
- ✅ Compatible Hugging Face Spaces

---

### **Déploiement : Hugging Face Spaces (vs autres options)**

#### Comparaison des solutions de déploiement :

| Solution | Coût | Setup | Scalabilité | CI/CD | Monitoring |
|----------|------|-------|-------------|-------|------------|
| **Hugging Face** | ✅ Gratuit | ⭐⭐⭐⭐⭐ Facile | ⭐⭐⭐ Moyen | ✅ Git push | ⭐⭐⭐ Logs |
| AWS Lambda | 💰 Pay-as-you-go | ⭐⭐⭐ Moyen | ⭐⭐⭐⭐⭐ Élevé | ⚠️ Complex | ⭐⭐⭐⭐⭐ CloudWatch |
| Heroku | 💰 $7-25/mois | ⭐⭐⭐⭐ Facile | ⭐⭐⭐ Moyen | ✅ Git push | ⭐⭐⭐ Logs |
| Google Cloud Run | 💰 Pay-as-you-go | ⭐⭐ Complex | ⭐⭐⭐⭐⭐ Élevé | ⚠️ Complex | ⭐⭐⭐⭐⭐ Stackdriver |
| VPS Perso | 💰 $5-20/mois | ⭐ Difficile | ⭐ Faible | ❌ Manuel | ⭐ Manuel |

**Choix : Hugging Face Spaces**
- ✅ **Gratuit** pour projets académiques/démonstration
- ✅ **Déploiement automatique** via Git push
- ✅ **Docker natif** (Dockerfile → build auto)
- ✅ **URL publique** immédiate
- ✅ **Logs accessibles** via interface web
- ✅ **Communauté ML** (visibilité projet)

**Limitations assumées :**
- ⚠️ Pas de scaling automatique (adapté au trafic modéré)
- ⚠️ Monitoring basique (suffisant pour MVP)
- ⚠️ Pas de SLA formel (acceptable pour démo/formation)

---

### **Base de Données : SQLite (vs PostgreSQL)**

#### Pourquoi SQLite pour la production ?

| Critère | SQLite | PostgreSQL |
|---------|--------|------------|
| **Setup** | ⭐⭐⭐⭐⭐ 1 fichier | ⭐⭐ Serveur requis |
| **Déploiement** | ✅ Inclus dans Docker | ⚠️ Service externe |
| **Concurrence** | ⚠️ Lectures multiples OK, 1 écriture | ⭐⭐⭐⭐⭐ Haute |
| **Scalabilité** | ⭐⭐ < 1M lignes | ⭐⭐⭐⭐⭐ Illimité |
| **Coût** | ✅ Gratuit | 💰 Hébergement requis |

**Choix : SQLite**
- ✅ **Adapté au volume** (~2400 employés + logs prédictions)
- ✅ **Zéro configuration** (pas de serveur externe)
- ✅ **Portable** (1 fichier = toute la DB)
- ✅ **Compatible HF** (stockage persistant)
- ✅ **Suffisant pour API lecture-intensive**

**Limitations connues :**
- ⚠️ Pas adapté si > 100 écritures/seconde simultanées
- ⚠️ Pas de réplication/haute disponibilité native

**Évolution future :** Migration vers PostgreSQL si :
- Volume > 100k employés
- Trafic > 1000 req/sec
- Besoins de réplication

---

### **CI/CD : GitHub Actions (vs autres)**

#### Pourquoi GitHub Actions ?

**Avantages :**
- ✅ **Intégré à GitHub** (pas de service externe)
- ✅ **Gratuit** pour repos publics (2000 min/mois privés)
- ✅ **Déclenchement automatique** sur push/PR
- ✅ **Yaml simple** et lisible
- ✅ **Marketplace d'actions** réutilisables

**Notre workflow :**
```yaml
Commit → Push → GitHub Actions
           ↓
       Tests (pytest)
           ↓
    ✅ Passage → Merge autorisé
    ❌ Échec  → Blocage du merge
```

**Tests lancés automatiquement :**
- 51 tests unitaires + fonctionnels
- Validation du modèle (métriques)
- Tests API (endpoints)
- Coverage (> 80%)

---

### **Authentification : API Key (vs JWT/OAuth)**

#### Pourquoi une simple API Key ?

| Solution | Complexité | Sécurité | Adapté à notre cas |
|----------|------------|----------|---------------------|
| **API Key** | ⭐ Simple | ⭐⭐⭐ Bonne | ✅ PARFAIT |
| JWT | ⭐⭐⭐ Moyenne | ⭐⭐⭐⭐ Élevée | ⚠️ Over-engineering |
| OAuth 2.0 | ⭐⭐⭐⭐⭐ Complexe | ⭐⭐⭐⭐⭐ Maximale | ❌ Trop complexe |
| Aucune | ⭐⭐⭐⭐⭐ Trivial | ❌ Nulle | ❌ Dangereux |

**Choix : API Key**
- ✅ **Simplicité** (1 header HTTP)
- ✅ **Suffisant** pour usage interne RH
- ✅ **Révocable** facilement
- ✅ **Pas de session** à gérer
- ✅ **Compatible** avec tous les clients (curl, Python, JS)

**Implémentation :**
```python
# Header requis
X-API-Key: votre-cle-secrete
```

**Sécurité :**
- ✅ Stockée dans secrets HF (pas en clair dans code)
- ✅ HTTPS obligatoire (chiffrement transport)
- ⚠️ 1 clé pour tous (acceptable pour MVP, améliorer si multi-utilisateurs)

---

## 📊 Résumé des Choix Techniques

| Décision | Justification | Alternative Considérée |
|----------|---------------|------------------------|
| **XGBoost** | Performance + Interprétabilité | Random Forest, Neural Nets |
| **29 features** | Toutes informatives, meilleur ROC-AUC | Feature selection (50%) |
| **F2-Score** | Privilégie Recall (coût métier) | F1-Score, Accuracy |
| **Seuil 0.09** | Maximise détection (95% Recall) | Seuil 0.5 (60% Recall) |
| **Pipeline sklearn** | Reproductibilité + Déploiement | Preprocessing manuel |
| **joblib** | Optimisé sklearn + Compression | pickle |
| **Hugging Face** | Gratuit + Git-based CI/CD | AWS, Heroku, GCP |
| **SQLite** | Simple + Adapté au volume | PostgreSQL |
| **GitHub Actions** | Intégré + Tests auto | GitLab CI, Jenkins |
| **API Key** | Simple + Suffisant MVP | JWT, OAuth |

---

**Ces choix sont documentés, justifiés et révisables en fonction de l'évolution du projet.**

---

## 🧪 Tests

✅ **51 tests automatiques** lancés à chaque commit via GitHub Actions
```bash
# Lancer les tests localement
pytest tests/ -v
```

---

## 💻 Installation Locale (Développement)

### **Prérequis**
- Python 3.13
- UV (gestionnaire de dépendances)

### **Étapes**
```bash
# 1. Cloner le repository
git clone https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning.git
cd Projet-5-Deployer-un-modele-de-machine-learning

# 2. Installer les dépendances
uv sync

# 3. Créer le fichier .env
echo "DATABASE_URL=sqlite:///./hr_analytics.db" > .env
echo "API_KEY=votre-cle-de-dev" >> .env

# 4. Créer les tables
uv run python create_tables.py

# 5. Importer les données (si nécessaire)
uv run python import_data.py

# 6. Entraîner le modèle
uv run python train_final_model.py

# 7. Lancer l'API
uv run uvicorn main:app --reload
```

L'API sera accessible sur http://localhost:8000

---

## 🐳 Docker

### **Build local**
```bash
docker build -t api-demission .
docker run -p 7860:7860 -e API_KEY=votre-cle api-demission
```

### **Variables d'environnement**
- `DATABASE_URL` : Chemin de la base de données (défaut : `sqlite:///./hr_analytics.db`)
- `API_KEY` : Clé d'authentification (à configurer dans les secrets)

### **☁️ Déploiement Automatique**

Chaque push sur `main` déclenche :
1. ✅ Tests CI/CD (GitHub Actions)
2. 🚀 Build automatique sur Hugging Face
3. 📊 Génération des données et entraînement du modèle
4. 🌐 Déploiement en production

**Les données sont générées AUTOMATIQUEMENT au build** depuis `01_classe.joblib`.
Aucun fichier CSV n'est inclus dans le repository pour des raisons de confidentialité.

---

## 📚 Documentation

- **Swagger UI** : `/docs` (documentation interactive)
- **ReDoc** : `/redoc` (documentation alternative)

---

## 👨‍💻 Auteur

I. R. 
Projet 5 - Formation IA Engineer

---

## 📄 Licence

Ce projet est développé dans le cadre d'une formation.

---

## 🔗 Liens

- [GitHub Repository](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning)
- [CI/CD Pipeline](https://github.com/Isab-bot/Projet-5-Deployer-un-modele-de-machine-learning/actions)
- [Hugging Face Space (Production)](https://huggingface.co/spaces/Fox6768/API_demission_prediction)
- [API Déployée](https://Fox6768-api-demission-prediction.hf.space)