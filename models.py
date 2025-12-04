from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)
    features = Column(Text)  # JSON avec features
    target = Column(String, nullable=True)  # "Oui" ou "Non"
    created_at = Column(DateTime, default=datetime.utcnow)

class PredictionLog(Base):
    __tablename__ = "predictions_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien optionnel vers un employé existant (pour endpoint 1)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    
    # Features utilisées pour la prédiction (JSON)
    input_features = Column(Text, nullable=False)
    
    # Résultat de la prédiction
    prediction_result = Column(String, nullable=False)  # "Oui" ou "Non"
    
    # Score de confiance du modèle
    confidence_score = Column(Float, nullable=True)
    
    # Version du modèle utilisé
    model_version = Column(String, default="v1.0")
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)