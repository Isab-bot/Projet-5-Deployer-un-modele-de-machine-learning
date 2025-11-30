import joblib
import json
from typing import Dict, Any
import numpy as np
import pandas as pd
import logging
from pathlib import Path
import pickle 

logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self, model_path: str = "models/xgboost_pipeline.pkl"):
        self.model_path = Path(model_path)
        self.pipeline = None
        self.config = None
        self.feature_names = None
        self.optimal_threshold = None
        
    def load_model(self):
        """Charge le modèle avec gestion d'erreurs."""
        try:
            # Vérifier que le fichier existe
            if not self.model_path.exists():
                raise FileNotFoundError(
                    f"❌ Modèle non trouvé : {self.model_path}\n"
                    f"💡 Assurez-vous d'avoir exécuté 'python train_final_model.py'"
                )
            
            # Charger le modèle
            with open(self.model_path, 'rb') as f:
                saved_data = pickle.load(f)
            
            self.pipeline = saved_data['pipeline']
            self.config = saved_data['config']
            self.feature_names = saved_data['feature_names']
            self.optimal_threshold = saved_data['optimal_threshold']
            
            logger.info(f"✅ Modèle chargé : {len(self.feature_names)} features")
            
        except FileNotFoundError as e:
            logger.error(str(e))
            raise
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle : {e}")
            raise RuntimeError(
                f"Impossible de charger le modèle depuis {self.model_path}. "
                f"Erreur : {e}"
            )
        
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
        proba = self.pipeline.predict_proba(df)[0, 1]
        
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