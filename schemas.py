from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schéma pour lire les données d'entraînement
class TrainingDataResponse(BaseModel):
    id: int
    identifier: str
    features: str  # JSON string
    target: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schéma pour créer une prédiction
class PredictionRequest(BaseModel):
    features: dict  # Les  features en dictionnaire
    model_version: Optional[str] = "v1.0"

# Schéma pour la réponse de prédiction
class PredictionResponse(BaseModel):
    id: int
    input_features: str
    prediction_result: str
    model_version: str
    confidence_score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True