"""
Tests fonctionnels pour les endpoints de l'API

Ces tests vérifient que l'API fonctionne correctement de bout en bout :
requête HTTP → traitement → base de données → modèle → réponse JSON.
"""

import pytest
from sqlalchemy.orm import Session
from models import Employee, PredictionLog


    
# =============================================================================
# RE
# MARQUE : Tous ces tests sont des tests fonctionnels
# =============================================================================

pytestmark = pytest.mark.functional

def test_root(client):
    """Test de l'endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_health_check(client):
    """Test du health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"



def test_count_employees(client, setup_test_data):
    """Test comptage employés"""
    response = client.get("/employees/count")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert data["total"] >= 1



def test_get_prediction_logs(client):
    """Test récupération logs de prédictions"""
    response = client.get("/predictions/logs?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_predict_from_id_not_found(client):
    """Test prédiction avec ID inexistant"""
    response = client.post("/predict/from_id/99999")
    assert response.status_code == 404


def test_predict_new_employee_invalid_data(client):
    """Test prédiction avec données invalides"""
    response = client.post("/predict/new_employee", json={"features": "invalid"})
    assert response.status_code == 422


def test_get_prediction_log_not_found(client):
    """Test récupération log inexistant"""
    response = client.get("/predict/log/99999")
    assert response.status_code == 404



# =============================================================================
# SETUP : Ajouter des données de test dans la DB
# =============================================================================

@pytest.fixture(scope="function")
def setup_test_data(db_session):
    """
    Fixture pour ajouter des données de test dans la base.
    
    Crée un employé de test avec ID=1 pour tester l'endpoint /predict/from_id/
    """
    import json
    
    # Charger les données valides
    with open('tests/data/valid_employee.json', 'r', encoding='utf-8') as f:
        features = json.load(f)
    
    # Créer un employé de test
    employee = Employee(
        id=1,
        features=json.dumps(features),
        target="Non"
    )
    
    db_session.add(employee)
    db_session.commit()
    
    yield employee
    
    # Cleanup : supprimer après le test
    db_session.query(Employee).delete()
    db_session.query(PredictionLog).delete()
    db_session.commit()


# =============================================================================
# ENDPOINT 1 : POST /predict/from_id/{employee_id}
# =============================================================================

def test_predict_from_id_success(client, setup_test_data):
    """
    OBJECTIF : Tester une prédiction depuis un employé existant.
    
    JUSTIFICATION : Cas d'usage principal de l'endpoint.
    
    CRITÈRES DE SUCCÈS :
    - Status code 200
    - Réponse contient les clés attendues
    - Un log est créé en base de données
    """
    # Act : Appeler l'endpoint
    response = client.post("/predict/from_id/1")
    
    # Assert : Vérifier la réponse
    assert response.status_code == 200, f"Code inattendu : {response.status_code}"
    
    data = response.json()
    
    # Vérifier la structure de la réponse
    assert 'log_id' in data, "Clé 'log_id' manquante dans la réponse"
    assert 'employee_id' in data, "Clé 'employee_id' manquante"
    assert 'prediction' in data, "Clé 'prediction' manquante"
    assert 'confidence_score' in data, "Clé 'confidence_score' manquante"
    assert 'timestamp' in data, "Clé 'timestamp' manquante"
    
    # Vérifier les valeurs
    assert data['employee_id'] == 1
    assert data['prediction'] in ['Oui', 'Non']
    assert 0 <= data['confidence_score'] <= 1


def test_predict_from_id_not_found(client):
    """
    OBJECTIF : Tester avec un ID d'employé inexistant.
    
    JUSTIFICATION : L'API doit gérer les erreurs correctement.
    
    CRITÈRES DE SUCCÈS :
    - Status code 404
    - Message d'erreur approprié
    """
    # Act : Appeler avec un ID qui n'existe pas
    response = client.post("/predict/from_id/99999")
    
    # Assert
    assert response.status_code == 404, f"Code attendu : 404, reçu : {response.status_code}"
    
    data = response.json()
    assert 'detail' in data, "Message d'erreur manquant"


def test_predict_from_id_creates_log(client, setup_test_data, db_session):
    """
    OBJECTIF : Vérifier qu'un log de prédiction est créé en base de données.
    
    JUSTIFICATION : Exigence de traçabilité des prédictions.
    
    CRITÈRES DE SUCCÈS :
    - Un log existe en DB après l'appel
    - Le log contient les bonnes informations
    """
    # Arrange : Compter les logs avant
    logs_before = db_session.query(PredictionLog).count()
    
    # Act : Faire une prédiction
    response = client.post("/predict/from_id/1")
    assert response.status_code == 200
    
    # Assert : Vérifier qu'un log a été créé
    logs_after = db_session.query(PredictionLog).count()
    assert logs_after == logs_before + 1, "Aucun log créé"
    
    # Vérifier le contenu du log
    log = db_session.query(PredictionLog).order_by(PredictionLog.id.desc()).first()
    assert log is not None
    assert log.employee_id == 1
    assert log.prediction_result in ['Oui', 'Non']


# =============================================================================
# ENDPOINT 2 : POST /predict/new_employee
# =============================================================================

def test_predict_new_employee_success(client, valid_employee_data):
    """
    OBJECTIF : Tester une prédiction pour un nouvel employé.
    
    JUSTIFICATION : Cas d'usage principal pour les nouveaux employés.
    
    CRITÈRES DE SUCCÈS :
    - Status code 200
    - Réponse contient les clés attendues
    - employee_id est null (pas en base)
    """
    # Arrange : Préparer la requête
    payload = {
        "features": valid_employee_data,
        "model_version": "v1.0"
    }
    
    # Act : Appeler l'endpoint
    response = client.post("/predict/new_employee", json=payload)
    
    # Assert : Vérifier la réponse
    assert response.status_code == 200, f"Code inattendu : {response.status_code}"
    
    data = response.json()
    
    # Vérifier la structure
    assert 'log_id' in data
    assert 'employee_id' in data
    assert 'prediction' in data
    assert 'confidence_score' in data
    
    # employee_id doit être null (nouvel employé)
    assert data['employee_id'] is None
    assert data['prediction'] in ['Oui', 'Non']


def test_predict_new_employee_invalid_data(client):
    """
    OBJECTIF : Tester avec des données invalides.
    
    JUSTIFICATION : L'API doit rejeter les données mal formées.
    
    CRITÈRES DE SUCCÈS :
    - Status code 422 (Validation Error)
    """
    # Arrange : Données invalides
    payload = {
        "features": "pas un dict",  # ❌ Type incorrect
        "model_version": "v1.0"
    }
    
    # Act
    response = client.post("/predict/new_employee", json=payload)
    
    # Assert
    assert response.status_code == 422, f"Code attendu : 422, reçu : {response.status_code}"


def test_predict_new_employee_creates_log(client, valid_employee_data, db_session):
    """
    OBJECTIF : Vérifier qu'un log est créé pour un nouvel employé.
    
    JUSTIFICATION : Toutes les prédictions doivent être loggées.
    
    CRITÈRES DE SUCCÈS :
    - Un log est créé en DB
    - employee_id est null dans le log
    """
    # Arrange
    payload = {
        "features": valid_employee_data,
        "model_version": "v1.0"
    }
    logs_before = db_session.query(PredictionLog).count()
    
    # Act
    response = client.post("/predict/new_employee", json=payload)
    assert response.status_code == 200
    
    # Assert
    logs_after = db_session.query(PredictionLog).count()
    assert logs_after == logs_before + 1
    
    # Vérifier le log
    log = db_session.query(PredictionLog).order_by(PredictionLog.id.desc()).first()
    assert log.employee_id is None  # Nouvel employé


def test_predict_new_employee_empty_features(client):
    """
    OBJECTIF : Tester avec un dict de features vide.
    
    JUSTIFICATION : Le modèle doit gérer les features manquantes.
    
    CRITÈRES DE SUCCÈS :
    - Status code 200 ou 400 (selon votre implémentation)
    - Si 200 : une prédiction est quand même retournée (avec valeurs par défaut)
    """
    # Arrange
    payload = {
        "features": {},  # Dict vide
        "model_version": "v1.0"
    }
    
    # Act
    response = client.post("/predict/new_employee", json=payload)
    
    # Assert : Le comportement dépend de votre implémentation
    # Option 1 : Le modèle accepte et utilise des valeurs par défaut
    # Option 2 : Le modèle rejette avec une erreur
    assert response.status_code in [200, 400, 422]


# =============================================================================
# ENDPOINT 3 : GET /predict/log/{log_id}
# =============================================================================

def test_get_prediction_log_success(client, setup_test_data, db_session):
    """
    OBJECTIF : Récupérer un log de prédiction existant.
    
    JUSTIFICATION : Les utilisateurs doivent pouvoir consulter l'historique.
    
    CRITÈRES DE SUCCÈS :
    - Status code 200
    - Réponse contient toutes les informations du log
    """
    # Arrange : Créer une prédiction d'abord
    response_predict = client.post("/predict/from_id/1")
    assert response_predict.status_code == 200
    log_id = response_predict.json()['log_id']
    
    # Act : Récupérer le log
    response = client.get(f"/predict/log/{log_id}")
    
    # Assert
    assert response.status_code == 200
    
    data = response.json()
    assert 'log_id' in data
    assert 'features' in data
    assert 'prediction' in data
    assert 'confidence_score' in data
    assert data['log_id'] == log_id


def test_get_prediction_log_not_found(client):
    """
    OBJECTIF : Tester avec un log_id inexistant.
    
    JUSTIFICATION : L'API doit gérer les erreurs correctement.
    
    CRITÈRES DE SUCCÈS :
    - Status code 404
    """
    # Act : Chercher un log qui n'existe pas
    response = client.get("/predict/log/99999")
    
    # Assert
    assert response.status_code == 404


def test_get_prediction_log_content(client, setup_test_data):
    """
    OBJECTIF : Vérifier que le contenu du log est correct.
    
    JUSTIFICATION : Le log doit contenir exactement ce qui a été prédit.
    
    CRITÈRES DE SUCCÈS :
    - Les features récupérées correspondent aux features d'origine
    - La prédiction est cohérente
    """
    # Arrange : Faire une prédiction
    response_predict = client.post("/predict/from_id/1")
    predicted_result = response_predict.json()['prediction']
    log_id = response_predict.json()['log_id']
    
    # Act : Récupérer le log
    response = client.get(f"/predict/log/{log_id}")
    
    # Assert
    data = response.json()
    assert data['prediction'] == predicted_result
    assert 'features' in data
    # Vérifier que les features sont bien un dict/objet
    assert isinstance(data['features'], (dict, str))


# =============================================================================
# TESTS DE PERFORMANCE
# =============================================================================

def test_api_response_time(client, setup_test_data):
    """
    OBJECTIF : Vérifier que l'API répond en moins de 2 secondes.
    
    JUSTIFICATION : L'API doit être réactive en production.
    
    CRITÈRES DE SUCCÈS :
    - Temps de réponse < 2 secondes
    """
    import time
    
    # Act : Mesurer le temps de réponse
    start = time.time()
    response = client.post("/predict/from_id/1")
    duration = time.time() - start
    
    # Assert
    assert response.status_code == 200
    assert duration < 2.0, f"API trop lente : {duration:.2f}s"
    
    print(f"\n⏱️  Temps de réponse API : {duration*1000:.2f}ms")


# =============================================================================
# TESTS D'INTÉGRATION (WORKFLOW COMPLET)
# =============================================================================

def test_full_prediction_workflow(client, valid_employee_data, db_session):
    """
    OBJECTIF : Tester un workflow complet de bout en bout.
    
    JUSTIFICATION : Vérifier que tous les composants fonctionnent ensemble.
    
    WORKFLOW :
    1. Créer une prédiction pour un nouvel employé
    2. Récupérer le log
    3. Vérifier la cohérence des données
    
    CRITÈRES DE SUCCÈS :
    - Chaque étape fonctionne
    - Les données sont cohérentes à chaque étape
    """
    # Étape 1 : Faire une prédiction
    payload = {
        "features": valid_employee_data,
        "model_version": "v1.0"
    }
    response1 = client.post("/predict/new_employee", json=payload)
    assert response1.status_code == 200
    
    prediction_data = response1.json()
    log_id = prediction_data['log_id']
    predicted_result = prediction_data['prediction']
    
    # Étape 2 : Récupérer le log
    response2 = client.get(f"/predict/log/{log_id}")
    assert response2.status_code == 200
    
    log_data = response2.json()
    
    # Étape 3 : Vérifier la cohérence
    assert log_data['log_id'] == log_id
    assert log_data['prediction'] == predicted_result
    
    # Étape 4 : Vérifier en base de données
    log_in_db = db_session.query(PredictionLog).filter(PredictionLog.id == log_id).first()
    assert log_in_db is not None
    assert log_in_db.prediction_result == predicted_result
    
    print(f"\n✅ Workflow complet testé : prédiction '{predicted_result}' loggée avec ID {log_id}")

def test_predict_new_employee_success(client, valid_employee_data):
    """
    OBJECTIF : Tester une prédiction pour un nouvel employé.
    
    JUSTIFICATION : Cas d'usage principal pour les nouveaux employés.
    
    CRITÈRES DE SUCCÈS :
    - Status code 200
    - Réponse contient les clés attendues
    - employee_id est null (pas en base)
    """
    # Arrange : Préparer la requête
    payload = {
        "features": valid_employee_data,
        "model_version": "v1.0"
    }
    
    # Act : Appeler l'endpoint
    response = client.post("/predict/new_employee", json=payload)
    
    # Assert : Vérifier la réponse
    assert response.status_code == 200, f"Code inattendu : {response.status_code}"
    
    data = response.json()
    
    
    # Vérifier la structure
    assert 'log_id' in data
    assert 'employee_id' in data
    assert 'prediction' in data  
    assert 'confidence_score' in data
    
    # employee_id doit être null (nouvel employé)
    assert data['employee_id'] is None
    assert data['prediction'] in ['Oui', 'Non']  

def test_api_docs_accessible(client):
    """Test que la documentation Swagger est accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_api_redoc_accessible(client):
    """Test que ReDoc est accessible"""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_json(client):
    """Test que le schéma OpenAPI est accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data

#=============================================================================
# TESTS D'AUTHENTIFICATION
# =============================================================================



def test_predict_from_id_with_valid_api_key(client, setup_test_data):
    """Test prédiction avec bonne API Key"""
    response = client.post(
        "/predict/from_id/1",
        headers={"X-API-Key": "test-api-key-12345"}
    )
    assert response.status_code == 200


# =============================================================================
# TESTS ENDPOINTS PROTÉGÉS
# =============================================================================




def test_get_employee_by_id_not_found(client):
    """Test GET /employees/{id} avec ID inexistant"""
    response = client.get(
        "/employees/99999",
        headers={"X-API-Key": "test-api-key-12345"}
    )
    assert response.status_code == 404



def test_get_statistics_with_auth(client, setup_test_data):
    """Test GET /stats avec authentification"""
    response = client.get(
        "/stats",
        headers={"X-API-Key": "test-api-key-12345"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "employees" in data
    assert "predictions" in data
    assert "model" in data    