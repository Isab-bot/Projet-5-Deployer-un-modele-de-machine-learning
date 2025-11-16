from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from database import Base
from datetime import datetime

class TrainingData(Base):
    __tablename__ = "training_data"
    
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)  # colonne d'identifiant
    features = Column(Text)  # JSON avec features
    target = Column(String, nullable=True)  # Variable à prédire ()
    created_at = Column(DateTime, default=datetime.utcnow)

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    input_features = Column(Text)  # JSON des features envoyées
    prediction_result = Column(Float)
    model_version = Column(String, default="v1.0")
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)