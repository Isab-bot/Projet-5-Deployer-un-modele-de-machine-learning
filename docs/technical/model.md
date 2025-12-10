# Documentation du Modèle

Documentation technique complète du modèle de prédiction de démissions.

---

## 🎯 Vue d'Ensemble

**Type de modèle :** XGBoost Classifier  
**Objectif :** Prédire si un employé va démissionner (classification binaire)  
**Version actuelle :** v1.0  
**Date d'entraînement :** Décembre 2024  

---

## 📊 Performances du Modèle

### Métriques Principales

| Métrique | Score | Interprétation |
|----------|-------|----------------|
| **F2-Score** | 0.6818 | Métrique principale (privilégie le Recall) |
| **Precision** | 0.8214 | 82% des prédictions "démission" sont correctes |
| **Recall** | 0.9474 | 95% des vraies démissions sont détectées |
| **ROC-AUC** | 0.9326 | Excellent pouvoir discriminant |
| **Accuracy** | 0.9586 | 96% de prédictions correctes globalement |

### Interprétation Business

✅ **Recall 95%** : Le modèle détecte 95% des démissions réelles  
→ Peu de faux négatifs (employés à risque non détectés)

✅ **Precision 82%** : 82% des alertes sont justifiées  
→ Quelques faux positifs (employés alertés qui ne démissionnent pas)

**Compromis optimisé pour les RH :** Mieux vaut avoir quelques fausses alertes que de manquer des démissions réelles.

---

## 🔍 Caractéristiques (Features)

### Features d'Entrée

| Feature | Type | Plage | Description |
|---------|------|-------|-------------|
| `satisfaction_level` | Float | 0.0 - 1.0 | Niveau de satisfaction (0=faible, 1=élevé) |
| `last_evaluation` | Float | 0.0 - 1.0 | Dernière évaluation de performance |
| `number_project` | Integer | 1 - 10 | Nombre de projets assignés |
| `average_montly_hours` | Integer | 80 - 350 | Heures mensuelles moyennes |
| `time_spend_company` | Integer | 1 - 10 | Années d'ancienneté |
| `Work_accident` | Binary | 0 ou 1 | A eu un accident de travail |
| `promotion_last_5years` | Binary | 0 ou 1 | A été promu dans les 5 dernières années |
| `departement` | Categorical | 10 valeurs | Département (sales, IT, support, etc.) |
| `salary` | Categorical | low/medium/high | Niveau de salaire |

### Importance des Features

**Top 5 des features les plus influentes :**

1. **satisfaction_level** (35%) - Feature la plus importante
2. **time_spend_company** (20%)
3. **average_montly_hours** (15%)
4. **last_evaluation** (12%)
5. **number_project** (8%)

---

## ⚙️ Architecture du Modèle

### Algorithme : XGBoost

**XGBoost (eXtreme Gradient Boosting)** est un algorithme de boosting performant.

**Principe :**
- Ensemble d'arbres de décision
- Chaque arbre corrige les erreurs du précédent
- Agrégation des prédictions

**Avantages pour ce cas d'usage :**
- ✅ Gère bien les données déséquilibrées
- ✅ Robuste aux outliers
- ✅ Interprétable (importance des features)
- ✅ Rapide en prédiction (< 100ms)

---

### Hyperparamètres

**Hyperparamètres optimisés (via Optuna) :**
```python
{
    'n_estimators': 150,
    'max_depth': 6,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'min_child_weight': 1,
    'gamma': 0,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'scale_pos_weight': 3.5  # Gestion déséquilibre
}
```

**Justification `scale_pos_weight` :**
- Gère le déséquilibre des classes (plus de "Non" que de "Oui")
- Augmente le poids des exemples positifs (démissions)

---

## 🔧 Pipeline de Prétraitement

### Étapes du Pipeline
```
Données brutes → Preprocessing → Modèle → Prédiction
```

**1. Gestion des valeurs manquantes**
- Aucune valeur manquante dans le dataset d'entraînement
- Validation stricte via Pydantic en production

**2. Encodage des variables catégorielles**
- `departement` : One-Hot Encoding (10 colonnes)
- `salary` : Ordinal Encoding (low=0, medium=1, high=2)

**3. Normalisation**
- Features numériques : StandardScaler
- Centrage et réduction (moyenne=0, écart-type=1)

**4. Équilibrage des classes**
- Utilisation de `scale_pos_weight` dans XGBoost
- Pas de SMOTE/undersampling pour préserver les données réelles

---

## 📈 Entraînement

### Dataset

**Source :** `01_classe.joblib` (2363 employés historiques)

**Répartition :**
- **Train set :** 70% (1654 employés)
- **Validation set :** 15% (355 employés)
- **Test set :** 15% (354 employés)

**Distribution des classes :**
- **Démissions (Oui) :** 24% (567 employés)
- **Rétention (Non) :** 76% (1796 employés)

---

### Processus d'Optimisation

**Méthode :** Recherche d'hyperparamètres avec Optuna

**Métrique d'optimisation :** F2-Score  
**Raison :** Privilégie le Recall (détecter un maximum de démissions)

**Nombre d'essais :** 100 combinaisons testées

---

## 🚀 Déploiement

### Format du Modèle

**Fichier :** `pipeline_xgboost_optimised.joblib`  
**Taille :** ~5 MB  
**Format :** Joblib (sklearn/xgboost compatible)

**Contenu :**
```python
{
    'preprocessor': ColumnTransformer,  # Preprocessing pipeline
    'model': XGBClassifier,             # Modèle XGBoost entraîné
    'feature_names': list,              # Noms des features
    'threshold': float                  # Seuil optimal (si applicable)
}
```

---

### Chargement en Production

**Fichier :** `model_loader.py`
```python
import joblib

# Chargement
pipeline = joblib.load('pipeline_xgboost_optimised.joblib')

# Prédiction
prediction = pipeline.predict(features)
proba = pipeline.predict_proba(features)
```

**Performance :**
- Chargement : ~100ms (au démarrage)
- Prédiction : < 50ms par employé

---

## 🎯 Utilisation du Modèle

### Cas d'Usage

**1. Prédiction individuelle**
```python
employee_data = {
    "satisfaction_level": 0.38,
    "last_evaluation": 0.53,
    ...
}
prediction = model.predict([employee_data])
```

**2. Batch de prédictions**
```python
employees_df = pd.DataFrame([...])  # Plusieurs employés
predictions = model.predict(employees_df)
```

**3. Score de confiance**
```python
proba = model.predict_proba(employee_data)
confidence = proba[0][1]  # Probabilité de démission
```

---

## 🔄 Maintenance et Amélioration

### Monitoring

**Métriques à suivre en production :**
- Distribution des prédictions (% Oui vs Non)
- Temps de réponse de l'API
- Drift des features (satisfaction moyenne, heures moyennes)

### Réentraînement

**Déclencheurs pour réentraîner :**
- ✅ Nouvelles données disponibles (démissions réelles vs prédictions)
- ✅ Dégradation des performances (baisse du F2-score)
- ✅ Changements organisationnels majeurs

**Fréquence recommandée :** Trimestriel

---

## 🛡️ Limites et Biais

### Limites Connues

⚠️ **Données historiques :** Le modèle apprend du passé, peut ne pas capter les nouvelles tendances

⚠️ **Features manquantes :** Pas d'info sur salaire exact, relations interpersonnelles, contexte familial

⚠️ **Faux positifs :** ~18% des alertes sont incorrectes (employés prédits démission mais qui restent)

### Biais Potentiels

⚠️ **Biais temporel :** Entraîné sur données passées, peut être moins précis sur nouvelles cohortes

⚠️ **Biais départements :** Performance peut varier selon les départements (moins de données pour certains)

**Recommandation :** Combiner prédictions avec jugement RH expert

---

## 📚 Ressources

**Code source :**
- Entraînement : `train_final_model.py`
- Chargement : `model_loader.py`
- Tests : `tests/functional/test_model_performance.py`

**Documentation externe :**
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [Scikit-learn Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)

---

## 🔍 FAQ Technique

**Q : Pourquoi F2-Score et pas F1 ?**  
**R :** F2 privilégie le Recall (2x plus important que Precision). Pour les RH, mieux vaut avoir quelques fausses alertes que rater des vraies démissions.

**Q : Le modèle peut-il expliquer ses prédictions ?**  
**R :** Oui, via l'importance des features. Pour une prédiction individuelle, SHAP values pourraient être ajoutées (amélioration future).

**Q : Quelle est la durée de vie du modèle ?**  
**R :** Recommandé de réentraîner tous les 3-6 mois avec nouvelles données.

**Q : Le modèle gère-t-il les nouvelles valeurs de features ?**  
**R :** Non, il faut réentraîner si nouvelles catégories (ex: nouveau département). Les valeurs numériques hors plage sont gérées par le StandardScaler.