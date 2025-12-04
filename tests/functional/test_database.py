"""
Tests fonctionnels pour les opérations de base de données

Ces tests vérifient que les opérations CRUD (Create, Read, Update, Delete)
et l'intégrité des données fonctionnent correctement.
"""

import pytest
import json
from datetime import datetime
from models import Employee, PredictionLog


# =============================================================================
# MARQUE : Tous ces tests sont des tests fonctionnels
# =============================================================================

pytestmark = pytest.mark.functional


# =============================================================================
# TEST 1 : CRÉER UN EMPLOYÉ
# =============================================================================

def test_create_employee(db_session):
    """
    OBJECTIF : Vérifier qu'on peut créer un employé dans la table employees.
    
    JUSTIFICATION : Test de base pour vérifier que la table existe et
    que les opérations d'insertion fonctionnent.
    
    CRITÈRES DE SUCCÈS :
    - L'employé est créé sans erreur
    - Un ID est auto-généré
    - Les données sont bien stockées
    """
    # Arrange : Préparer les données
    employee_features = {
        "age": 30,
        "genre": "M",
        "statut_marital": "Célibataire"
    }
    
    # Act : Créer l'employé
    employee = Employee(
        features=json.dumps(employee_features),
        target="Non"
    )
    db_session.add(employee)
    db_session.commit()
    
    # Assert : Vérifier
    assert employee.id is not None, "L'ID devrait être auto-généré"
    assert employee.target == "Non"
    
    print(f"\n✅ Employé créé avec ID : {employee.id}")


# =============================================================================
# TEST 2 : CRÉER UN LOG DE PRÉDICTION
# =============================================================================

def test_create_prediction_log(db_session):
    """
    OBJECTIF : Vérifier qu'on peut créer un log dans predictions_logs.
    
    JUSTIFICATION : Vérifie que la table de logs fonctionne et que tous
    les champs sont correctement stockés.
    
    CRITÈRES DE SUCCÈS :
    - Le log est créé sans erreur
    - Un ID est auto-généré
    - Le timestamp est auto-généré
    - Toutes les données sont stockées
    """
    # Arrange
    log_features = {"age": 35, "genre": "F"}
    
    # Act : Créer le log
    log = PredictionLog(
        employee_id=None,
        input_features=json.dumps(log_features),
        prediction_result="Non",
        confidence_score=0.75,
        model_version="v1.0"
    )
    db_session.add(log)
    db_session.commit()
    
    # Assert : Vérifier
    assert log.id is not None, "L'ID devrait être auto-généré"
    assert log.created_at is not None, "Le timestamp devrait être auto-généré"
    assert log.prediction_result == "Non"
    assert log.confidence_score == 0.75
    
    # Vérifier que le timestamp est récent (moins de 1 minute)
    time_diff = datetime.utcnow() - log.created_at
    assert time_diff.total_seconds() < 60, "Le timestamp devrait être récent"
    
    print(f"\n✅ Log créé avec ID : {log.id}")


# =============================================================================
# TEST 3 : RELATION EMPLOYÉ → LOGS (FOREIGN KEY)
# =============================================================================

def test_employee_has_logs(db_session):
    """
    OBJECTIF : Vérifier qu'un employé peut avoir plusieurs logs associés.
    
    JUSTIFICATION : Teste la relation entre employees et predictions_logs.
    Un employé doit pouvoir avoir un historique de prédictions.
    
    CRITÈRES DE SUCCÈS :
    - Un employé peut avoir plusieurs logs
    - La foreign key fonctionne
    - On peut récupérer tous les logs d'un employé
    """
    # Arrange : Créer un employé
    employee = Employee(
        features='{"age": 40}',
        target="Non"
    )
    db_session.add(employee)
    db_session.commit()
    
    employee_id = employee.id
    
    # Act : Créer 3 logs pour cet employé
    for i in range(3):
        log = PredictionLog(
            employee_id=employee_id,
            input_features=f'{{"age": 40, "iteration": {i}}}',
            prediction_result="Non" if i % 2 == 0 else "Oui",
            confidence_score=0.5 + (i * 0.1)
        )
        db_session.add(log)
    db_session.commit()
    
    # Assert : Récupérer tous les logs de cet employé
    logs = db_session.query(PredictionLog)\
        .filter(PredictionLog.employee_id == employee_id)\
        .all()
    
    assert len(logs) == 3, f"Attendu 3 logs, trouvé {len(logs)}"
    
    # Vérifier que tous les logs sont bien liés à cet employé
    for log in logs:
        assert log.employee_id == employee_id
    
    print(f"\n✅ Employé {employee_id} a {len(logs)} logs associés")


# =============================================================================
# TEST 4 : LOG SANS EMPLOYÉ (employee_id = NULL)
# =============================================================================

def test_prediction_log_without_employee(db_session):
    """
    OBJECTIF : Vérifier qu'on peut créer un log sans employee_id.
    
    JUSTIFICATION : Pour les nouveaux employés (endpoint /predict/new_employee),
    on doit pouvoir créer un log sans avoir l'employé en base.
    
    CRITÈRES DE SUCCÈS :
    - Le log est créé avec employee_id = NULL
    - Aucune erreur de contrainte de foreign key
    """
    # Act : Créer un log sans employé
    log = PredictionLog(
        employee_id=None,  # ← NULL
        input_features='{"age": 25, "genre": "F"}',
        prediction_result="Oui",
        confidence_score=0.85,
        model_version="v1.0"
    )
    db_session.add(log)
    db_session.commit()
    
    # Assert : Vérifier
    assert log.id is not None
    assert log.employee_id is None, "employee_id devrait être NULL"
    
    print(f"\n✅ Log créé sans employé (ID : {log.id})")


# =============================================================================
# TEST 5 : RÉCUPÉRER UN EMPLOYÉ PAR ID
# =============================================================================

def test_retrieve_employee_by_id(db_session):
    """
    OBJECTIF : Vérifier qu'on peut récupérer un employé par son ID.
    
    JUSTIFICATION : Simule l'endpoint /predict/from_id/{id}.
    Les données doivent être correctement persistées et récupérables.
    
    CRITÈRES DE SUCCÈS :
    - L'employé est trouvé par son ID
    - Les données récupérées sont exactes
    """
    # Arrange : Créer un employé
    original_features = '{"age": 45, "genre": "M", "departement": "IT"}'
    employee = Employee(
        features=original_features,
        target="Non"
    )
    db_session.add(employee)
    db_session.commit()
    
    employee_id = employee.id
    
    # Act : Récupérer l'employé par ID
    retrieved = db_session.query(Employee)\
        .filter(Employee.id == employee_id)\
        .first()
    
    # Assert : Vérifier
    assert retrieved is not None, f"Employé {employee_id} non trouvé"
    assert retrieved.id == employee_id
    assert retrieved.features == original_features
    assert retrieved.target == "Non"
    
    print(f"\n✅ Employé {employee_id} récupéré avec succès")


# =============================================================================
# TEST 6 : RÉCUPÉRER TOUS LES LOGS D'UN EMPLOYÉ
# =============================================================================

def test_get_all_logs_for_employee(db_session):
    """
    OBJECTIF : Vérifier qu'on peut récupérer l'historique complet d'un employé.
    
    JUSTIFICATION : Cas d'usage réel pour un dashboard RH montrant
    l'évolution des prédictions pour un employé.
    
    CRITÈRES DE SUCCÈS :
    - Tous les logs de l'employé sont récupérés
    - Les logs d'autres employés ne sont pas inclus
    - L'ordre peut être contrôlé (par date)
    """
    # Arrange : Créer 2 employés
    emp1 = Employee(features='{"age": 30}', target="Non")
    emp2 = Employee(features='{"age": 40}', target="Oui")
    db_session.add_all([emp1, emp2])
    db_session.commit()
    
    # Créer 3 logs pour emp1 et 2 logs pour emp2
    for i in range(3):
        log = PredictionLog(
            employee_id=emp1.id,
            input_features=f'{{"iteration": {i}}}',
            prediction_result="Non",
            confidence_score=0.5
        )
        db_session.add(log)
    
    for i in range(2):
        log = PredictionLog(
            employee_id=emp2.id,
            input_features=f'{{"iteration": {i}}}',
            prediction_result="Oui",
            confidence_score=0.8
        )
        db_session.add(log)
    
    db_session.commit()
    
    # Act : Récupérer les logs de emp1 uniquement
    logs_emp1 = db_session.query(PredictionLog)\
        .filter(PredictionLog.employee_id == emp1.id)\
        .order_by(PredictionLog.created_at.desc())\
        .all()
    
    # Assert : Vérifier
    assert len(logs_emp1) == 3, f"Attendu 3 logs pour emp1, trouvé {len(logs_emp1)}"
    
    # Vérifier qu'aucun log d'emp2 n'est inclus
    for log in logs_emp1:
        assert log.employee_id == emp1.id
    
    print(f"\n✅ Historique de l'employé {emp1.id} : {len(logs_emp1)} logs")


# =============================================================================
# TEST 7 : INTÉGRITÉ DES DONNÉES (CONTRAINTES)
# =============================================================================

def test_prediction_log_requires_input_features(db_session):
    """
    OBJECTIF : Vérifier que les contraintes de la DB fonctionnent.
    
    JUSTIFICATION : Les champs obligatoires doivent être respectés.
    input_features est un champ NOT NULL.
    
    CRITÈRES DE SUCCÈS :
    - Créer un log sans input_features doit échouer
    - Une exception est levée
    """
    # Act : Essayer de créer un log sans input_features
    log = PredictionLog(
        employee_id=None,
        # input_features manquant ← Devrait échouer
        prediction_result="Non",
        confidence_score=0.75
    )
    
    # Assert : Devrait lever une exception
    with pytest.raises(Exception):  # IntegrityError ou autre
        db_session.add(log)
        db_session.commit()
    
    # Rollback pour nettoyer
    db_session.rollback()
    
    print("\n✅ Contrainte respectée : input_features est obligatoire")


# =============================================================================
# TEST 8 : VÉRIFIER QUE LES DONNÉES JSON SONT BIEN STOCKÉES
# =============================================================================

def test_json_data_integrity(db_session):
    """
    OBJECTIF : Vérifier que les données JSON sont correctement stockées et récupérées.
    
    JUSTIFICATION : Les features sont stockées en JSON. Il faut vérifier
    qu'elles ne sont pas corrompues lors du stockage/récupération.
    
    CRITÈRES DE SUCCÈS :
    - Les données JSON sont identiques après stockage/récupération
    - Les caractères spéciaux sont préservés
    """
    # Arrange : Données avec caractères spéciaux
    original_features = {
        "nom": "Dupont",
        "prenom": "François",
        "ville": "Sélestat",
        "age": 35
    }
    
    # Act : Créer un log
    log = PredictionLog(
        employee_id=None,
        input_features=json.dumps(original_features, ensure_ascii=False),
        prediction_result="Non",
        confidence_score=0.7
    )
    db_session.add(log)
    db_session.commit()
    
    log_id = log.id
    
    # Récupérer le log
    retrieved_log = db_session.query(PredictionLog)\
        .filter(PredictionLog.id == log_id)\
        .first()
    
    # Assert : Vérifier que le JSON est identique
    retrieved_features = json.loads(retrieved_log.input_features)
    
    assert retrieved_features == original_features, \
        "Les données JSON diffèrent après stockage/récupération"
    
    assert retrieved_features["nom"] == "Dupont"
    assert retrieved_features["prenom"] == "François"
    assert retrieved_features["ville"] == "Sélestat"
    
    print("\n✅ Données JSON préservées (y compris caractères spéciaux)")


# =============================================================================
# TEST 9 : COMPTER LES ENREGISTREMENTS
# =============================================================================

def test_count_records(db_session):
    """
    OBJECTIF : Vérifier qu'on peut compter les enregistrements.
    
    JUSTIFICATION : Opération courante pour des statistiques.
    
    CRITÈRES DE SUCCÈS :
    - Le comptage fonctionne correctement
    """
    # Arrange : Créer 5 logs
    for i in range(5):
        log = PredictionLog(
            employee_id=None,
            input_features=f'{{"iteration": {i}}}',
            prediction_result="Non",
            confidence_score=0.5
        )
        db_session.add(log)
    db_session.commit()
    
    # Act : Compter
    count = db_session.query(PredictionLog).count()
    
    # Assert : Vérifier
    assert count >= 5, f"Attendu au moins 5 logs, trouvé {count}"
    
    print(f"\n✅ Nombre total de logs : {count}")