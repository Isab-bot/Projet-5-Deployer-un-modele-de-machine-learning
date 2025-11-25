"""
Tests unitaires pour model_loader.py

Ces tests vérifient que la fonction predict() fonctionne correctement
de manière isolée (sans dépendances externes).
"""

import pytest
import time
from model_loader import model_loader


# =============================================================================
# REMARQUE : Tous ces tests sont des tests unitaires
# =============================================================================

pytestmark = pytest.mark.unit


# =============================================================================
# TEST 1 : FORMAT DE SORTIE CORRECT
# =============================================================================

def test_predict_returns_correct_format(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier que predict() retourne un dictionnaire avec les bonnes clés.
    
    JUSTIFICATION : L'API s'attend à recevoir ces clés précises.
    Si le format change, l'API crashera.
    
    CRITÈRES DE SUCCÈS :
    - Le résultat contient 'prediction'
    - Le résultat contient 'confidence_score'
    - Le résultat contient 'threshold_used'
    """
    # Act : Appeler la fonction
    result = model_loader_instance.predict(valid_employee_data)
    
    # Assert : Vérifier le format
    assert isinstance(result, dict), "Le résultat doit être un dictionnaire"
    assert 'prediction' in result, "La clé 'prediction' est manquante"
    assert 'confidence_score' in result, "La clé 'confidence_score' est manquante"
    assert 'threshold_used' in result, "La clé 'threshold_used' est manquante"


# =============================================================================
# TEST 2 : VALEURS COHÉRENTES
# =============================================================================

def test_predict_values_are_valid(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier que les valeurs retournées sont cohérentes.
    
    JUSTIFICATION : Éviter les bugs comme score > 1, prédiction invalide, etc.
    
    CRITÈRES DE SUCCÈS :
    - prediction est 'Oui' ou 'Non'
    - confidence_score est entre 0 et 1
    - threshold_used correspond au seuil configuré (0.090)
    """
    # Act
    result = model_loader_instance.predict(valid_employee_data)
    
    # Assert : Vérifier les valeurs
    assert result['prediction'] in ['Oui', 'Non'], \
        f"Prédiction invalide : {result['prediction']}"
    
    assert 0 <= result['confidence_score'] <= 1, \
        f"Score hors limites : {result['confidence_score']}"
    
    assert result['threshold_used'] == 0.090, \
        f"Seuil incorrect : {result['threshold_used']}"


# =============================================================================
# TEST 3 : REPRODUCTIBILITÉ
# =============================================================================

def test_predict_is_reproducible(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier que deux prédictions identiques donnent le même résultat.
    
    JUSTIFICATION : Exigence de reproductibilité dans le cahier des charges.
    Les utilisateurs doivent obtenir les mêmes résultats avec les mêmes données.
    
    CRITÈRES DE SUCCÈS :
    - Deux appels successifs retournent exactement le même résultat
    """
    # Act : Faire deux prédictions
    result1 = model_loader_instance.predict(valid_employee_data)
    result2 = model_loader_instance.predict(valid_employee_data)
    
    # Assert : Vérifier qu'elles sont identiques
    assert result1['prediction'] == result2['prediction'], \
        "Les prédictions diffèrent"
    
    assert result1['confidence_score'] == result2['confidence_score'], \
        "Les scores de confiance diffèrent"


# =============================================================================
# TEST 4 : GESTION DES VALEURS MANQUANTES
# =============================================================================

def test_predict_handles_missing_values(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier que le modèle gère les valeurs None sans crasher.
    
    JUSTIFICATION : En production, certaines données peuvent être manquantes.
    Le modèle doit être robuste face à ces situations.
    
    CRITÈRES DE SUCCÈS :
    - Le modèle ne crashe pas (pas d'exception levée)
    - Une prédiction est retournée (peut être moins fiable)
    """
    # Arrange : Créer des données avec valeurs manquantes
    data_with_none = valid_employee_data.copy()
    data_with_none['age'] = None
    data_with_none['revenu_mensuel'] = None
    
    # Act : Faire une prédiction (ne doit pas crasher)
    try:
        result = model_loader_instance.predict(data_with_none)
        
        # Assert : Vérifier qu'un résultat est retourné
        assert result is not None, "Aucun résultat retourné"
        assert 'prediction' in result, "Format de sortie incorrect"
        
    except Exception as e:
        pytest.fail(f"Le modèle a crashé avec des valeurs None : {e}")


# =============================================================================
# TEST 5 : GESTION DES VALEURS EXTRÊMES
# =============================================================================

def test_predict_handles_extreme_values(edge_cases_data, model_loader_instance):
    """
    OBJECTIF : Vérifier que le modèle gère les cas limites sans crasher.
    
    JUSTIFICATION : Les données réelles peuvent contenir des valeurs extrêmes
    (âge très élevé, salaire très élevé, etc.).
    
    CRITÈRES DE SUCCÈS :
    - Le modèle traite tous les cas limites sans erreur
    - Une prédiction est retournée pour chaque cas
    """
    # Act & Assert : Tester chaque cas limite
    for case in edge_cases_data:
        description = case['description']
        data = case['data']
        
        try:
            result = model_loader_instance.predict(data)
            
            # Vérifier qu'un résultat est retourné
            assert result is not None, f"Échec pour : {description}"
            assert 'prediction' in result, f"Format incorrect pour : {description}"
            
        except Exception as e:
            pytest.fail(f"Échec pour '{description}' : {e}")


# =============================================================================
# TEST 6 : TEMPS DE RÉPONSE (PERFORMANCE)
# =============================================================================

def test_predict_performance(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier qu'une prédiction prend moins d'1 seconde.
    
    JUSTIFICATION : L'API doit être réactive pour une bonne expérience utilisateur.
    Un temps de réponse > 1s serait inacceptable en production.
    
    CRITÈRES DE SUCCÈS :
    - Temps d'exécution < 1 seconde
    """
    # Act : Mesurer le temps d'exécution
    start = time.time()
    result = model_loader_instance.predict(valid_employee_data)
    duration = time.time() - start
    
    # Assert : Vérifier le temps
    assert duration < 1.0, \
        f"Prédiction trop lente : {duration:.3f}s (limite : 1.0s)"
    
    # Info : Afficher le temps même si le test passe
    print(f"\n⏱️  Temps de prédiction : {duration*1000:.2f}ms")


# =============================================================================
# TEST 7 : COHÉRENCE PRÉDICTION / SCORE
# =============================================================================

def test_predict_prediction_matches_threshold(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier la cohérence entre la prédiction et le score de confiance.
    
    JUSTIFICATION : Si score > seuil → prédiction doit être 'Oui'.
    Si score < seuil → prédiction doit être 'Non'.
    
    CRITÈRES DE SUCCÈS :
    - La logique de seuillage est correcte
    """
    # Act
    result = model_loader_instance.predict(valid_employee_data)
    
    threshold = result['threshold_used']
    score = result['confidence_score']
    prediction = result['prediction']
    
    # Assert : Vérifier la cohérence
    if score >= threshold:
        assert prediction == 'Oui', \
            f"Score {score} >= seuil {threshold} mais prédiction = {prediction}"
    else:
        assert prediction == 'Non', \
            f"Score {score} < seuil {threshold} mais prédiction = {prediction}"


# =============================================================================
# TEST 8 : TYPE DES VALEURS RETOURNÉES
# =============================================================================

def test_predict_return_types(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier que les types de données retournés sont corrects.
    
    JUSTIFICATION : Éviter les erreurs de type lors de la sérialisation JSON.
    
    CRITÈRES DE SUCCÈS :
    - prediction est un string
    - confidence_score est un float
    - threshold_used est un float
    """
    # Act
    result = model_loader_instance.predict(valid_employee_data)
    
    # Assert : Vérifier les types
    assert isinstance(result['prediction'], str), \
        f"prediction doit être un string, reçu : {type(result['prediction'])}"
    
    assert isinstance(result['confidence_score'], (float, int)), \
        f"confidence_score doit être un float, reçu : {type(result['confidence_score'])}"
    
    assert isinstance(result['threshold_used'], (float, int)), \
        f"threshold_used doit être un float, reçu : {type(result['threshold_used'])}"


# =============================================================================
# TEST 9 : STABILITÉ SUR PLUSIEURS PRÉDICTIONS
# =============================================================================

def test_predict_stability_multiple_calls(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier que le modèle reste stable après plusieurs appels.
    
    JUSTIFICATION : En production, le modèle sera appelé des milliers de fois.
    Il ne doit pas dégrader ses performances ou changer de comportement.
    
    CRITÈRES DE SUCCÈS :
    - 100 prédictions successives donnent toutes le même résultat
    """
    # Act : Faire 100 prédictions
    results = [model_loader_instance.predict(valid_employee_data) for _ in range(100)]
    
    # Assert : Vérifier qu'elles sont toutes identiques
    first_result = results[0]
    
    for i, result in enumerate(results[1:], start=2):
        assert result['prediction'] == first_result['prediction'], \
            f"Prédiction {i} diffère de la première"
        
        assert result['confidence_score'] == first_result['confidence_score'], \
            f"Score {i} diffère du premier"


# =============================================================================
# TEST 10 : CHARGE DE TRAVAIL (BATCH)
# =============================================================================

def test_predict_batch_performance(valid_employee_data, model_loader_instance):
    """
    OBJECTIF : Vérifier que 100 prédictions peuvent être faites en < 10s.
    
    JUSTIFICATION : En production, l'API peut recevoir plusieurs requêtes simultanées.
    
    CRITÈRES DE SUCCÈS :
    - 100 prédictions en moins de 10 secondes (moyenne < 100ms par prédiction)
    """
    # Act : Faire 100 prédictions
    start = time.time()
    
    for _ in range(100):
        model_loader_instance.predict(valid_employee_data)
    
    duration = time.time() - start
    
    # Assert : Vérifier le temps total
    assert duration < 10.0, \
        f"100 prédictions trop lentes : {duration:.2f}s (limite : 10s)"
    
    # Info : Afficher les statistiques
    avg_time = (duration / 100) * 1000
    print(f"\n⏱️  100 prédictions en {duration:.2f}s (moyenne : {avg_time:.2f}ms)")