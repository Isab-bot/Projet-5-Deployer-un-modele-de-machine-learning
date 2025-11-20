from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

# ========== SCHÉMAS POUR EMPLOYEES ==========

class EmployeeResponse(BaseModel):
    """Schéma pour lire un employé"""
    id: int
    identifier: str
    features: str  # JSON string
    target: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== SCHÉMAS POUR PREDICTIONS ==========

class PredictionFromIdRequest(BaseModel):
    """Endpoint 1 : Prédiction à partir d'un ID existant"""
    employee_id: int

class PredictionNewEmployeeRequest(BaseModel):
    """Endpoint 2 : Prédiction pour un nouvel employé"""
    features: dict = Field(..., description="Dictionnaire avec les features")
    model_version: Optional[str] = "v1.0"

class PredictionLogResponse(BaseModel):
    """Réponse d'une prédiction (pour tous les endpoints)"""
    id: int
    employee_id: Optional[int]
    input_features: str  # JSON
    prediction_result: str  # "Oui" ou "Non"
    confidence_score: Optional[float]
    model_version: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionDetailedResponse(BaseModel):
    """Réponse détaillée avec features décodées"""
    log_id: int
    employee_id: Optional[int]
    features: Dict[str, Any]
    prediction: str
    confidence_score: Optional[float]
    model_version: str
    timestamp: datetime
    