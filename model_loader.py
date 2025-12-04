import json
from typing import Dict, Any
import numpy as np
import pandas as pd
import logging
from pathlib import Path
import pickle
import os

logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self, model_path: str = "models/xgboost_pipeline.pkl"):
        self.model_path = Path(model_path)
        self.pipeline = None
        self.optimal_threshold = 0.5  # Seuil par défaut
        
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
            logger.info(f"📥 Chargement du modèle depuis {self.model_path}...")
            
            with open(self.model_path, 'rb') as f:
                self.pipeline = pickle.load(f)
            
            # Le fichier contient juste le pipeline (modèle dummy)
            # Pas de config, pas de feature_names
            
            logger.info("✅ Modèle chargé avec succès")
            logger.info(f"📊 Seuil optimal : {self.optimal_threshold}")
            
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
        if self.pipeline is None:
            raise RuntimeError("Modèle non chargé. Appelez load_model() d'abord.")
        
        # Convertir en DataFrame (1 ligne)
        df = pd.DataFrame([features])
        
        # Le modèle dummy accepte n'importe quelles features
        # On prend juste les valeurs numériques
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            # Si aucune colonne numérique, créer des valeurs par défaut
            df_numeric = pd.DataFrame(np.random.rand(1, 20))
        else:
            # Prendre les colonnes numériques
            df_numeric = df[numeric_cols]
            
            # Si moins de 20 colonnes, compléter avec des 0
            if df_numeric.shape[1] < 20:
                missing_cols = 20 - df_numeric.shape[1]
                for i in range(missing_cols):
                    df_numeric[f'feature_{i}'] = 0
        
        # Ne garder que 20 colonnes (le modèle dummy en attend 20)
        df_numeric = df_numeric.iloc[:, :20]
        
        try:
            # Prédiction (probabilité)
            proba = self.pipeline.predict_proba(df_numeric)[0, 1]
            
            # Prédiction (classe) avec seuil optimal
            prediction = "Oui" if proba >= self.optimal_threshold else "Non"
            
            # Score de confiance
            confidence = proba if prediction == "Oui" else (1 - proba)
            
            return {
                'prediction': prediction,
                'confidence_score': float(confidence)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction : {e}")
            # Retourner une prédiction par défaut
            return {
                'prediction': 'Non',
                'confidence_score': 0.5
            }

# Instance globale
model_loader = ModelLoader()