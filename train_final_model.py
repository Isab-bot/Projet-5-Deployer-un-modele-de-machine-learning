"""
Script pour créer un modèle XGBoost minimal pour le déploiement.
Utilisé pendant le build Docker sur Hugging Face.
"""

import pickle
import numpy as np
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import os

print("🔧 Création d'un modèle XGBoost minimal pour déploiement...")

# Créer le dossier models s'il n'existe pas
os.makedirs('models', exist_ok=True)

# Créer des données d'entraînement minimales
# 100 samples, 20 features (simule vos features réelles)
np.random.seed(42)
X_train = np.random.rand(100, 20)
y_train = np.random.randint(0, 2, 100)

# Créer le pipeline (même structure que votre vrai modèle)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'
    ))
])

# Entraîner sur les données minimales
print("📊 Entraînement du modèle minimal...")
pipeline.fit(X_train, y_train)

# Sauvegarder
print("💾 Sauvegarde du modèle...")
with open('models/xgboost_pipeline.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

# Vérifier
file_size = os.path.getsize('models/xgboost_pipeline.pkl') / 1024
print(f"✅ Modèle minimal créé : models/xgboost_pipeline.pkl ({file_size:.1f} KB)")
print("⚠️  Note : Ceci est un modèle dummy pour validation du déploiement")