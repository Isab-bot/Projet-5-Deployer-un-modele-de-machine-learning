import pickle
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

print("="*80)
print("🚀 ENTRAÎNEMENT DU MODÈLE XGBOOST FINAL")
print("="*80)

# =============================================================================
# 1. CHARGEMENT DES DONNÉES
# =============================================================================

print("\n📂 Chargement du dataset...")
with open('01_classe.pkl', 'rb') as f:
    df = pickle.load(f)

print(f"✅ Dataset chargé : {len(df)} lignes, {len(df.columns)} colonnes")

# =============================================================================
# 2. PRÉPARATION DES DONNÉES
# =============================================================================

print("\n🔧 Préparation des données...")

# Supprimer la colonne id_employe
df_modelisation = df.drop(columns=['id_employe'])

# Encodage de la cible
df_modelisation['démission'] = df_modelisation['démission'].map({'Non': 0, 'Oui': 1})

# Séparation X et y
X = df_modelisation.drop(columns=['démission'])
y = df_modelisation['démission']

print(f"✅ Features : {len(X.columns)} colonnes")
print(f"✅ Target : {y.value_counts().to_dict()}")

# Liste des 29 features du modèle Light 100%
feature_names = [
    'poste', 'heure_supplementaires', 'frequence_deplacement', 'age',
    'statut_marital', 'annees_experience_totale', 'niveau_education',
    'departement', 'participation_pee', 'annees_dans_l_entreprise',
    'genre', 'annes_sous_responsable_actuel', 'satisfaction',
    'experiences_precedentes', 'domaine_etude', 'distance_domicile_travail',
    'pro_perso', 'satisfaction_equilibre_pro_perso', 'revenu_mensuel',
    'revenu_log', 'satisfaction_nature_travail', 'note_evaluation_precedente',
    'nb_formations_suivies', 'annees_depuis_la_derniere_promotion',
    'satisfaction_environnement', 'variation_evaluation', 'reconnaissance',
    'augmentation_salaire_precedent', 'satisfaction_equipe'
]

# Vérifier que toutes les features existent
missing_features = [f for f in feature_names if f not in X.columns]
if missing_features:
    print(f"⚠️  Features manquantes : {missing_features}")
    print("   On utilise toutes les features disponibles à la place.")
    feature_names = X.columns.tolist()

X = X[feature_names]

print(f"✅ Features sélectionnées : {len(feature_names)}")

# =============================================================================
# 3. PREPROCESSING
# =============================================================================

print("\n🔄 Configuration du preprocessing...")

# Identifier les variables catégorielles
variables_objects = [
    col for col in X.select_dtypes(include=["object"]).columns
]

print(f"✅ Variables catégorielles : {len(variables_objects)}")

# Créer le preprocessor
preprocessor_cat = ColumnTransformer(
    transformers=[
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False), variables_objects),
    ],
    remainder="passthrough"
)

# =============================================================================
# 4. SÉPARATION TRAIN/TEST
# =============================================================================

print("\n✂️  Séparation des données...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    stratify=y, 
    test_size=0.2, 
    random_state=42
)

print(f"✅ Train : {len(X_train)} lignes")
print(f"✅ Test  : {len(X_test)} lignes")

# =============================================================================
# 5. CALCUL DU SCALE_POS_WEIGHT
# =============================================================================

scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
print(f"\n⚖️  Scale_pos_weight : {scale_pos_weight:.2f}")

# =============================================================================
# 6. CRÉATION DU MODÈLE XGBOOST
# =============================================================================

print("\n🤖 Création du modèle XGBoost...")

xgb_model = XGBClassifier(
    enable_categorical=True,
    random_state=42,
    n_jobs=-1,
    tree_method='hist',
    scale_pos_weight=scale_pos_weight,
    # Hyperparamètres optimaux
    colsample_bytree=0.8,
    learning_rate=0.05,
    max_depth=3,
    min_child_weight=5,
    n_estimators=100,
    subsample=0.8
)

# Pipeline complet
pipeline_final = Pipeline([
    ('preprocessor', preprocessor_cat),
    ('classifier', xgb_model)
])

print("✅ Pipeline créé")

# =============================================================================
# 7. ENTRAÎNEMENT
# =============================================================================

print("\n🔄 Entraînement du modèle...")

pipeline_final.fit(X_train, y_train)

print("✅ Modèle entraîné avec succès !")

# =============================================================================
# 8. ÉVALUATION RAPIDE
# =============================================================================

print("\n📊 Évaluation rapide sur le jeu de test...")

from sklearn.metrics import classification_report, roc_auc_score

optimal_threshold = 0.090

y_proba_test = pipeline_final.predict_proba(X_test)[:, 1]
y_pred_test = (y_proba_test >= optimal_threshold).astype(int)

print(f"\n   Seuil utilisé : {optimal_threshold}")
print("\n" + classification_report(y_test, y_pred_test, target_names=['Reste', 'Démission']))

roc_auc = roc_auc_score(y_test, y_proba_test)
print(f"   ROC-AUC : {roc_auc:.4f}")

# =============================================================================
# 9. SAUVEGARDE
# =============================================================================

print("\n💾 Sauvegarde des fichiers...")

# Sauvegarder le pipeline complet
joblib.dump(pipeline_final, 'xgboost_model.pkl')
print("✅ xgboost_model.pkl sauvegardé")

# Sauvegarder le preprocessor séparément (au cas où)
joblib.dump(preprocessor_cat, 'preprocessor.pkl')
print("✅ preprocessor.pkl sauvegardé")

# Sauvegarder la liste des features
joblib.dump(feature_names, 'feature_names.pkl')
print("✅ feature_names.pkl sauvegardé")

# Sauvegarder la configuration
config = {
    'optimal_threshold': optimal_threshold,
    'scale_pos_weight': scale_pos_weight,
    'n_features': len(feature_names),
    'feature_names': feature_names,
    'hyperparameters': {
        'colsample_bytree': 0.8,
        'learning_rate': 0.05,
        'max_depth': 3,
        'min_child_weight': 5,
        'n_estimators': 100,
        'subsample': 0.8
    },
    'model_type': 'XGBoost',
    'model_version': 'Light_100%',
    'f2_score': 0.6818
}

with open('model_config.json', 'w') as f:
    json.dump(config, f, indent=4)
print("✅ model_config.json sauvegardé")

# =============================================================================
# 10. RÉCAPITULATIF
# =============================================================================

print("\n" + "="*80)
print("✅ ENTRAÎNEMENT TERMINÉ")
print("="*80)
print("\n📁 Fichiers créés :")
print("   • xgboost_model.pkl      (Pipeline complet)")
print("   • preprocessor.pkl       (OneHotEncoder)")
print("   • feature_names.pkl      (Liste des 29 features)")
print("   • model_config.json      (Configuration et métadonnées)")
print("\n🎯 Prochaine étape : Intégrer le modèle dans l'API FastAPI")
print("="*80)