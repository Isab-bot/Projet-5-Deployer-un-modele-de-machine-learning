from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from database import get_db
from models import Employee, PredictionLog
from schemas import (
    EmployeeResponse, 
    PredictionFromIdRequest, 
    PredictionNewEmployeeRequest,
    PredictionLogResponse,
    PredictionDetailedResponse
)
import json
from typing import List
from datetime import datetime
from model_loader import model_loader
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# =============================================================================
# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
# =============================================================================

# Charger les variables depuis .env
load_dotenv()

# Récupérer l'API Key depuis .env
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("⚠️ API_KEY non définie dans le fichier .env")

# Définir le header de sécurité pour l'API Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# =============================================================================
# FONCTION DE VALIDATION DE L'API KEY
# =============================================================================

def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Vérifie que l'API Key est valide.
    
    Args:
        api_key: La clé API fournie dans le header X-API-Key
        
    Raises:
        HTTPException 401: Si la clé est absente ou invalide
        
    Returns:
        str: La clé API validée
    """
    # Vérifier si la clé est présente
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="❌ API Key manquante. Ajoutez le header 'X-API-Key' à votre requête."
        )
    
    # Vérifier si la clé est valide
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="❌ API Key invalide. Vérifiez votre clé d'authentification."
        )
    
    return api_key

# =============================================================================
# INITIALISATION DE L'APPLICATION
# =============================================================================

app = FastAPI(
    title="API de Prédiction de Démission",
    description="API pour prédire les démissions d'employés avec XGBoost",
    version="2.0.0"
)

@app.on_event("startup")
def startup_event():
    """Charger le modèle ML au démarrage de l'application"""
    model_loader.load_model()

# =============================================================================
# ENDPOINTS DE BASE (PUBLICS - SANS AUTHENTIFICATION)
# =============================================================================

@app.get("/")
def root():
    """
    🏠 Endpoint racine - PUBLIC
    
    Affiche les informations de base de l'API.
    Aucune authentification requise.
    """
    return {
        "message": "API de Prédiction de Démission - XGBoost",
        "version": "2.0.0",
        "model": "XGBoost Light 100%",
        "security": "🔒 Endpoints protégés par API Key (header X-API-Key)",
        "endpoints": {
            "documentation": "/docs",
            "health": "/health",
            "employees": "/employees",
            "predict_from_id": "/predict/from_id/{employee_id} 🔒",
            "predict_new_employee": "/predict/new_employee 🔒",
            "get_prediction_log": "/predict/log/{log_id} 🔒",
            "statistics": "/stats"
        }
    }

@app.get("/health")
def health_check():
    """
    ❤️ Endpoint de santé - PUBLIC
    
    Vérifie que l'API fonctionne correctement.
    Aucune authentification requise.
    """
    return {
        "status": "healthy",
        "model_loaded": model_loader.pipeline is not None,
        "timestamp": datetime.utcnow().isoformat()
    }

# =============================================================================
# ENDPOINTS EMPLOYEES (PUBLICS - CONSULTABLES SANS AUTHENTIFICATION)
# =============================================================================

@app.get("/employees", response_model=List[EmployeeResponse])
def get_employees(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """
    📋 Récupérer les employés (pagination) - PUBLIC
    
    Aucune authentification requise pour consulter la liste.
    """
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees

@app.get("/employees/count")
def count_employees(db: Session = Depends(get_db)):
    """
    🔢 Compter le nombre total d'employés - PUBLIC
    
    Aucune authentification requise.
    """
    count = db.query(Employee).count()
    return {"total": count}

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    """
    👤 Récupérer un employé spécifique - PUBLIC
    
    Aucune authentification requise pour consulter.
    """
    try:
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employé avec l'ID {employee_id} non trouvé"
            )
        return employee
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'employé {employee_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération de l'employé"
        )

# =============================================================================
# ENDPOINT 1 : PRÉDICTION À PARTIR D'UN ID EXISTANT 🔒 PROTÉGÉ
# =============================================================================

@app.post("/predict/from_id/{employee_id}", response_model=PredictionDetailedResponse)
def predict_from_employee_id(
    employee_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)  # 🔒 AUTHENTIFICATION REQUISE
):
    """
    🎯 ENDPOINT 1 : Prédiction à partir d'un employé existant - 🔒 PROTÉGÉ
    
    ⚠️ Requiert une API Key valide dans le header X-API-Key
    
    - Récupère les features de l'employé depuis la DB
    - Fait une prédiction avec le modèle
    - Loggue la prédiction dans predictions_logs
    """
    try:
        # Vérifier que le modèle est chargé
        if model_loader.pipeline is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Le modèle n'est pas chargé. Veuillez réessayer dans quelques instants."
            )
        
        # 1. Récupérer l'employé
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employé {employee_id} non trouvé"
            )
        
        # 2. Décoder les features (JSON → dict)
        features = json.loads(employee.features)
        
        # 3. Faire la prédiction
        prediction_result = model_loader.predict(features)
        
        # 4. Logger dans predictions_logs
        features_json = json.dumps(features)
        
        log_entry = PredictionLog(
            employee_id=employee_id,
            input_features=features_json,
            prediction_result=prediction_result['prediction'],
            confidence_score=prediction_result['confidence_score'],
            model_version="XGBoost_Light_100%"
        )
        
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        
        # 5. Retourner la réponse détaillée
        return PredictionDetailedResponse(
            log_id=log_entry.id,
            employee_id=employee_id,
            features=features,
            prediction=prediction_result['prediction'],
            confidence_score=prediction_result['confidence_score'],
            model_version="XGBoost_Light_100%",
            timestamp=log_entry.created_at
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction pour l'employé {employee_id}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction : {str(e)}"
        )

# =============================================================================
# ENDPOINT 2 : PRÉDICTION POUR UN NOUVEL EMPLOYÉ 🔒 PROTÉGÉ
# =============================================================================

@app.post("/predict/new_employee", response_model=PredictionDetailedResponse)
def predict_new_employee(
    request: PredictionNewEmployeeRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)  # 🔒 AUTHENTIFICATION REQUISE
):
    """
    🎯 ENDPOINT 2 : Prédiction pour un nouvel employé - 🔒 PROTÉGÉ
    
    ⚠️ Requiert une API Key valide dans le header X-API-Key
    
    - Reçoit les features en JSON
    - Fait une prédiction avec le modèle
    - Loggue la prédiction dans predictions_logs
    """
    try:
        # Vérifier que le modèle est chargé
        if model_loader.pipeline is None:  # ✅ CORRECTION : pipeline au lieu de model
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Le modèle n'est pas chargé. Veuillez réessayer dans quelques instants."
            )
        
        # 1. Faire la prédiction
        prediction_result = model_loader.predict(request.features)
        
        # 2. Logger dans predictions_logs
        features_json = json.dumps(request.features)
        
        log_entry = PredictionLog(
            employee_id=None,  # Pas d'ID car nouvel employé
            input_features=features_json,
            prediction_result=prediction_result['prediction'],
            confidence_score=prediction_result['confidence_score'],
            model_version=request.model_version
        )
        
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        
        # 3. Retourner la réponse détaillée
        return PredictionDetailedResponse(
            log_id=log_entry.id,
            employee_id=None,
            features=request.features,
            prediction=prediction_result['prediction'],
            confidence_score=prediction_result['confidence_score'],
            model_version=request.model_version,
            timestamp=log_entry.created_at
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction pour un nouvel employé: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction : {str(e)}"
        )

# =============================================================================
# ENDPOINT 3 : RÉCUPÉRER UNE PRÉDICTION VIA LOG_ID 🔒 PROTÉGÉ
# =============================================================================

@app.get("/predict/log/{log_id}", response_model=PredictionDetailedResponse)
def get_prediction_log(
    log_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)  # 🔒 AUTHENTIFICATION REQUISE
):
    """
    🎯 ENDPOINT 3 : Récupérer une prédiction passée - 🔒 PROTÉGÉ
    
    ⚠️ Requiert une API Key valide dans le header X-API-Key
    
    - Récupère un log de prédiction par son ID
    - Retourne les features + la prédiction + timestamp
    """
    try:
        # 1. Récupérer le log
        log_entry = db.query(PredictionLog).filter(PredictionLog.id == log_id).first()
        if not log_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Log {log_id} non trouvé"
            )
        
        # 2. Décoder les features
        features = json.loads(log_entry.input_features)
        
        # 3. Retourner la réponse
        return PredictionDetailedResponse(
            log_id=log_entry.id,
            employee_id=log_entry.employee_id,
            features=features,
            prediction=log_entry.prediction_result,
            confidence_score=log_entry.confidence_score,
            model_version=log_entry.model_version,
            timestamp=log_entry.created_at
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du log {log_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la récupération du log"
        )

# =============================================================================
# ENDPOINTS POUR LISTER LES LOGS 🔒 PROTÉGÉ
# =============================================================================

@app.get("/predictions/logs", response_model=List[PredictionLogResponse])
def get_prediction_logs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)  # 🔒 AUTHENTIFICATION REQUISE
):
    """
    📜 Récupérer l'historique des prédictions - 🔒 PROTÉGÉ
    
    ⚠️ Requiert une API Key valide dans le header X-API-Key
    """
    logs = db.query(PredictionLog).order_by(PredictionLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs

@app.get("/predictions/logs/count")
def count_prediction_logs(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)  # 🔒 AUTHENTIFICATION REQUISE
):
    """
    🔢 Compter le nombre total de prédictions loguées - 🔒 PROTÉGÉ
    
    ⚠️ Requiert une API Key valide dans le header X-API-Key
    """
    count = db.query(PredictionLog).count()
    return {"total": count}

# =============================================================================
# STATISTIQUES (PUBLIC)
# =============================================================================

@app.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """
    📊 Statistiques générales - PUBLIC
    
    Aucune authentification requise pour consulter les stats.
    """
    total_employees = db.query(Employee).count()
    total_predictions = db.query(PredictionLog).count()
    
    # Compter les démissions dans les données d'entraînement
    oui_count = db.query(Employee).filter(Employee.target == "Oui").count()
    non_count = db.query(Employee).filter(Employee.target == "Non").count()
    
    # Compter les prédictions
    pred_oui = db.query(PredictionLog).filter(PredictionLog.prediction_result == "Oui").count()
    pred_non = db.query(PredictionLog).filter(PredictionLog.prediction_result == "Non").count()
    
    return {
        "employees": {
            "total": total_employees,
            "demissions_oui": oui_count,
            "demissions_non": non_count
        },
        "predictions": {
            "total": total_predictions,
            "predicted_oui": pred_oui,
            "predicted_non": pred_non
        },
        "model": {
            "type": "XGBoost",
            "version": "Light_100%",
            "threshold": model_loader.optimal_threshold if model_loader.pipeline else None  # ✅ CORRECTION
        }
    }