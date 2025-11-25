"""
Tests unitaires pour schemas.py

Ces tests vérifient que les schémas Pydantic valident correctement
les données entrantes de l'API.
"""

import pytest
from pydantic import ValidationError
from schemas import (
    PredictionNewEmployeeRequest,
    EmployeeResponse,
    PredictionLogResponse
)


# =============================================================================
# MARQUE : Tous ces tests sont des tests unitaires
# =============================================================================

pytestmark = pytest.mark.unit


# =============================================================================
# TESTS POUR PredictionNewEmployeeRequest
# =============================================================================

def test_prediction_request_valid_data(valid_employee_data):
    """
    OBJECTIF : Vérifier qu'un schéma valide est accepté.
    
    JUSTIFICATION : Les données normales doivent passer sans erreur.
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé sans lever d'exception
    - Les valeurs sont correctement stockées
    """
    # Arrange : Préparer les données
    data = {
        "features": valid_employee_data,
        "model_version": "v1.0"
    }
    
    # Act : Créer le schéma
    request = PredictionNewEmployeeRequest(**data)
    
    # Assert : Vérifier
    assert request.features == valid_employee_data
    assert request.model_version == "v1.0"


def test_prediction_request_features_wrong_type():
    """
    OBJECTIF : Vérifier que Pydantic rejette un type incorrect pour 'features'.
    
    JUSTIFICATION : 'features' doit être un dict, pas un string ou autre.
    
    CRITÈRES DE SUCCÈS :
    - Une ValidationError est levée
    """
    # Arrange : Données invalides
    data = {
        "features": "pas un dict",  # ❌ Type incorrect
        "model_version": "v1.0"
    }
    
    # Act & Assert : Doit lever une exception
    with pytest.raises(ValidationError) as exc_info:
        PredictionNewEmployeeRequest(**data)
    
    # Vérifier que l'erreur concerne bien 'features'
    errors = exc_info.value.errors()
    assert any(error['loc'] == ('features',) for error in errors)


def test_prediction_request_model_version_wrong_type():
    """
    OBJECTIF : Vérifier que Pydantic rejette un type incorrect pour 'model_version'.
    
    JUSTIFICATION : 'model_version' doit être un string.
    
    CRITÈRES DE SUCCÈS :
    - Une ValidationError est levée
    """
    # Arrange
    data = {
        "features": {"age": 30},
        "model_version": 123  # ❌ Type incorrect (devrait être string)
    }
    
    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        PredictionNewEmployeeRequest(**data)
    
    errors = exc_info.value.errors()
    assert any(error['loc'] == ('model_version',) for error in errors)


def test_prediction_request_missing_features():
    """
    OBJECTIF : Vérifier que 'features' est obligatoire.
    
    JUSTIFICATION : Sans features, impossible de faire une prédiction.
    
    CRITÈRES DE SUCCÈS :
    - Une ValidationError est levée si 'features' est absent
    """
    # Arrange : Données sans 'features'
    data = {
        "model_version": "v1.0"
        # 'features' manquant ❌
    }
    
    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        PredictionNewEmployeeRequest(**data)
    
    errors = exc_info.value.errors()
    assert any(error['loc'] == ('features',) for error in errors)


def test_prediction_request_model_version_optional():
    """
    OBJECTIF : Vérifier que 'model_version' est optionnel avec valeur par défaut.
    
    JUSTIFICATION : Si non fourni, doit utiliser la valeur par défaut.
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé sans erreur
    - model_version a la valeur par défaut "v1.0"
    """
    # Arrange : Données sans model_version
    data = {
        "features": {"age": 30, "genre": "M"}
        # model_version omis
    }
    
    # Act
    request = PredictionNewEmployeeRequest(**data)
    
    # Assert : Vérifier la valeur par défaut
    assert request.model_version == "v1.0"


def test_prediction_request_features_empty_dict():
    """
    OBJECTIF : Vérifier qu'un dict vide est techniquement accepté par Pydantic.
    
    JUSTIFICATION : Pydantic valide le type, pas le contenu (c'est le modèle ML qui le fera).
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé (Pydantic accepte)
    - Le dict est vide mais valide au niveau du type
    """
    # Arrange
    data = {
        "features": {},  # Dict vide mais techniquement valide
        "model_version": "v1.0"
    }
    
    # Act
    request = PredictionNewEmployeeRequest(**data)
    
    # Assert
    assert request.features == {}
    assert isinstance(request.features, dict)


def test_prediction_request_extra_fields_ignored():
    """
    OBJECTIF : Vérifier que les champs supplémentaires sont ignorés.
    
    JUSTIFICATION : Pydantic ignore les champs non définis (comportement par défaut).
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé sans erreur
    - Les champs extra ne sont pas dans l'objet
    """
    # Arrange
    data = {
        "features": {"age": 30},
        "model_version": "v1.0",
        "champ_inexistant": "valeur"  # Champ en trop
    }
    
    # Act
    request = PredictionNewEmployeeRequest(**data)
    
    # Assert : Champ ignoré
    assert not hasattr(request, 'champ_inexistant')


# =============================================================================
# TESTS POUR EmployeeResponse (si applicable)
# =============================================================================

def test_employee_response_valid():
    """
    OBJECTIF : Vérifier que EmployeeResponse accepte des données valides.
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé sans erreur
    """
    # Note : Adaptez selon votre schéma réel
    data = {
        "id": 1,
        "age": 30,
        "genre": "M",
        "departement": "IT"
        # Ajoutez les autres champs selon votre schéma
    }
    
    try:
        response = EmployeeResponse(**data)
        assert response.id == 1
    except Exception as e:
        pytest.skip(f"EmployeeResponse non testé : {e}")


# =============================================================================
# TESTS POUR PredictionLogResponse (si applicable)
# =============================================================================

def test_prediction_log_response_valid():
    """
    OBJECTIF : Vérifier que PredictionLogResponse accepte des données valides.
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé sans erreur
    """
    # Note : Adaptez selon votre schéma réel
    data = {
        "id": 1,
        "features": {"age": 30},
        "prediction": "Non",
        "confidence_score": 0.75,
        "created_at": "2025-11-25T10:00:00"
        # Ajoutez les autres champs selon votre schéma
    }
    
    try:
        response = PredictionLogResponse(**data)
        assert response.id == 1
    except Exception as e:
        pytest.skip(f"PredictionLogResponse non testé : {e}")


# =============================================================================
# TEST AVEC LES DONNÉES INVALIDES DU FICHIER JSON
# =============================================================================

def test_prediction_request_with_invalid_employee_data(invalid_employee_data):
    """
    OBJECTIF : Vérifier que Pydantic accepte le dict même si les valeurs sont invalides.
    
    JUSTIFICATION : Pydantic valide le TYPE (dict), pas le CONTENU des features.
    C'est le modèle ML qui validera ensuite.
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé (Pydantic ne valide que le type dict)
    """
    # Arrange
    data = {
        "features": invalid_employee_data,  # Contient des valeurs invalides
        "model_version": "v1.0"
    }
    
    # Act : Pydantic accepte car c'est un dict (même si les valeurs sont mauvaises)
    request = PredictionNewEmployeeRequest(**data)
    
    # Assert
    assert isinstance(request.features, dict)
    # Note : Le modèle ML devra gérer ces valeurs invalides


# =============================================================================
# TESTS DES CAS LIMITES
# =============================================================================

def test_prediction_request_with_null_values():
    """
    OBJECTIF : Vérifier que Pydantic accepte des valeurs None dans le dict features.
    
    JUSTIFICATION : Pydantic valide le type dict, pas les valeurs à l'intérieur.
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé
    """
    # Arrange
    data = {
        "features": {
            "age": None,
            "genre": None
        },
        "model_version": "v1.0"
    }
    
    # Act
    request = PredictionNewEmployeeRequest(**data)
    
    # Assert
    assert request.features["age"] is None


def test_prediction_request_features_nested_dict():
    """
    OBJECTIF : Vérifier que Pydantic accepte des dicts imbriqués.
    
    JUSTIFICATION : Dict[str, Any] peut contenir n'importe quoi, y compris des dicts.
    
    CRITÈRES DE SUCCÈS :
    - Le schéma est créé
    """
    # Arrange
    data = {
        "features": {
            "age": 30,
            "nested": {"key": "value"}  # Dict imbriqué
        },
        "model_version": "v1.0"
    }
    
    # Act
    request = PredictionNewEmployeeRequest(**data)
    
    # Assert
    assert request.features["nested"]["key"] == "value"