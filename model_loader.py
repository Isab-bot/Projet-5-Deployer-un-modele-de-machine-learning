import joblib
import json
from typing import Dict, Any
import numpy as np
import pandas as pd

class ModelLoader:
    """Classe pour charger et utiliser le modèle XGBoost"""
    
    def __init__(self):
        self.model = None
        self.config = None
        self.feature_names = None
        self.optimal_threshold = None
        
    def load(self):
        """Charger tous les fichiers du modèle"""
        print("📦 Chargement du modèle XGBoost...")
        
        # Charger le pipeline (modèle + preprocessor)
        self.model = joblib.load('xgboost_model.pkl')
        print("   ✅ Pipeline chargé")
        
        # Charger la configuration
        with open('model_config.json', 'r') as f:
            self.config = json.load(f)
        print("   ✅ Configuration chargée")
        
        # Charger les noms de features
        self.feature_names = joblib.load('feature_names.pkl')
        print(f"   ✅ {len(self.feature_names)} features chargées")
        
        # Récupérer le seuil optimal
        self.optimal_threshold = self.config['optimal_threshold']
        print(f"   ✅ Seuil optimal : {self.optimal_threshold}")
        
        print("🎉 Modèle prêt !\n")
        
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faire une prédiction à partir d'un dictionnaire de features
        
        Args:
            features: Dictionnaire avec les valeurs des features
            
        Returns:
            Dictionnaire avec prediction, probability, confidence
        """
        
        
        # Convertir en DataFrame (1 ligne)
        df = pd.DataFrame([features])
        
        # S'assurer que toutes les features sont présentes
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = None  # Valeur manquante
        
        # Garder seulement les features du modèle (dans le bon ordre)
        df = df[self.feature_names]
        
        # Prédiction (probabilité)
        proba = self.model.predict_proba(df)[0, 1]
        
        # Prédiction (classe) avec seuil optimal
        prediction = "Oui" if proba >= self.optimal_threshold else "Non"
        
        # Score de confiance
        confidence = proba if prediction == "Oui" else (1 - proba)
        
        return {
            'prediction': prediction,
            'probability': float(proba),
            'confidence_score': float(confidence),
            'threshold_used': self.optimal_threshold
        }

# Instance globale
model_loader = ModelLoader()