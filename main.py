from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import TrainingData, PredictionLog
from schemas import EmployeeResponse, PredictionNewEmployeeRequest, PredictionLogResponse
import json
from typing import List

app = FastAPI(
    title="API de Prédiction de Démission",
    description="API pour prédire les démissions d'employés",
    version="1.0.0"
)

# ========== ENDPOINTS DE TEST ==========

@app.get("/")
def root():
    return {
        "message": "API de Prédiction de Démission",
        "endpoints": {
            "docs": "/docs",
            "training_data": "/training-data",
            "predictions": "/predictions",
            "predict": "/predict"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ========== ENDPOINTS TRAINING DATA ==========

@app.get("/training-data", response_model=List[EmployeeResponse])
def get_training_data(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """Récupérer les données d'entraînement (pagination)"""
    data = db.query(TrainingData).offset(skip).limit(limit).all()
    return data

@app.get("/training-data/count")
def count_training_data(db: Session = Depends(get_db)):
    """Compter le nombre total de données d'entraînement"""
    count = db.query(TrainingData).count()
    return {"total": count}

@app.get("/training-data/{data_id}", response_model=EmployeeResponse)
def get_training_data_by_id(data_id: int, db: Session = Depends(get_db)):
    """Récupérer une donnée d'entraînement spécifique"""
    data = db.query(TrainingData).filter(TrainingData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return data

# ========== ENDPOINTS PREDICTIONS ==========

@app.post("/predict", response_model=PredictionLogResponse)
def make_prediction(
    request: PredictionNewEmployeeRequest, 
    db: Session = Depends(get_db)
):
    """
    Faire une prédiction de démission
    
    Pour l'instant, c'est une prédiction factice.
    Intégration du  vrai modèle ML plus tard.
    """
    
    # TODO: Charger le modèle ML et faire la vraie prédiction
    # Pour l'instant, prédiction aléatoire pour tester
    import random
    prediction_result = random.choice(["Oui", "Non"])
    confidence = round(random.uniform(0.6, 0.99), 2)
    
    # Sauvegarder la prédiction dans la DB
    features_json = json.dumps(request.features)
    
    db_prediction = PredictionLog(
        input_features=features_json,
        prediction_result=prediction_result,
        model_version=request.model_version,
        confidence_score=confidence
    )
    
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction

@app.get("/predictions", response_model=List[PredictionLogResponse])
def get_predictions(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """Récupérer l'historique des prédictions"""
    predictions = db.query(PredictionLog).offset(skip).limit(limit).all()
    return predictions

@app.get("/predictions/count")
def count_predictions(db: Session = Depends(get_db)):
    """Compter le nombre total de prédictions"""
    count = db.query(PredictionLog).count()
    return {"total": count}

@app.get("/predictions/{prediction_id}", response_model=PredictionLogResponse)
def get_prediction_by_id(prediction_id: int, db: Session = Depends(get_db)):
    """Récupérer une prédiction spécifique"""
    prediction = db.query(PredictionLog).filter(PredictionLog.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    return prediction

# ========== STATISTIQUES ==========

@app.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """Statistiques générales"""
    total_training = db.query(TrainingData).count()
    total_predictions = db.query(PredictionLog).count()
    
    # Compter les démissions dans les données d'entraînement
    oui_count = db.query(TrainingData).filter(TrainingData.target == "Oui").count()
    non_count = db.query(TrainingData).filter(TrainingData.target == "Non").count()
    
    return {
        "training_data": {
            "total": total_training,
            "demissions_oui": oui_count,
            "demissions_non": non_count
        },
        "predictions": {
            "total": total_predictions
        }
    }