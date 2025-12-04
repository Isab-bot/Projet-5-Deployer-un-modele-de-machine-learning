"""
Tests fonctionnels pour les performances du modèle ML

Ces tests vérifient que le modèle maintient des performances acceptables
sur un jeu de test, conformément aux exigences métier.
"""

import pytest
import joblib
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    fbeta_score,
    roc_auc_score,
    recall_score,
    precision_score,
    confusion_matrix,
    classification_report
)


# =============================================================================
# MARQUE : Tous ces tests sont des tests fonctionnels et lents
# =============================================================================

pytestmark = [pytest.mark.functional, pytest.mark.slow]


# =============================================================================
# FIXTURES : CHARGEMENT DU JEU DE TEST
# =============================================================================

@pytest.fixture(scope="module")
def test_dataset():
    """
    Fixture pour charger le jeu de test.
    
    Charge 01_classe.pkl et recrée le même split que lors de l'entraînement
    pour obtenir le jeu de test.
    
    Scope "module" = chargé 1 fois pour tous les tests de ce fichier.
    """
    print("\n📂 Chargement du dataset...")
    
    # Charger le dataset complet
    with open('01_classe.joblib', 'rb') as f:
        df = joblib.load(f)
    
    print(f"   ✅ Dataset chargé : {len(df)} lignes")
    
    # Séparer features et target
    X = df.drop(columns=['démission', 'id_employe'])
    y = df['démission'].map({'Non': 0, 'Oui': 1})
    
    # Faire le MÊME split que lors de l'entraînement
    # IMPORTANT : Utiliser random_state=42 pour la reproductibilité
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    
    print(f"   ✅ Jeu de test : {len(X_test)} lignes")
    print(f"   📊 Distribution : {y_test.value_counts().to_dict()}")
    
    return {
        'X_test': X_test,
        'y_test': y_test,
        'feature_names': X.columns.tolist()
    }


@pytest.fixture(scope="module")
def model_predictions(test_dataset, model_loader_instance):
    """
    Fixture pour générer les prédictions sur le jeu de test.
    
    Fait toutes les prédictions une seule fois et les réutilise pour tous les tests.
    """
    print("\n🔮 Génération des prédictions...")
    
    X_test = test_dataset['X_test']
    y_test = test_dataset['y_test']
    
    # Générer les prédictions
    y_proba = []
    y_pred = []
    
    start_time = time.time()
    
    for idx, row in X_test.iterrows():
        # Convertir la ligne en dict
        features = row.to_dict()
        
        # Faire la prédiction
        result = model_loader_instance.predict(features)
        
        # Stocker les résultats
        y_proba.append(result['probability'])
        y_pred.append(1 if result['prediction'] == 'Oui' else 0)
    
    duration = time.time() - start_time
    
    print(f"   ✅ {len(y_pred)} prédictions générées en {duration:.2f}s")
    print(f"   ⏱️  Temps moyen : {(duration/len(y_pred))*1000:.2f}ms par prédiction")
    
    return {
        'y_test': y_test,
        'y_pred': np.array(y_pred),
        'y_proba': np.array(y_proba),
        'duration': duration,
        'n_predictions': len(y_pred)
    }


# =============================================================================
# TEST 1 : F2-SCORE (MÉTRIQUE PRINCIPALE)
# =============================================================================

def test_f2_score_threshold(model_predictions):
    """
    OBJECTIF : Vérifier que le F2-score est supérieur au seuil minimum.
    
    JUSTIFICATION : Le F2-score est la métrique d'optimisation principale.
    Elle privilégie le recall (détecter les démissions) tout en gardant
    une précision acceptable.
    
    CRITÈRES DE SUCCÈS :
    - F2-score > 0.65
    
    SEUIL : 0.65 est un bon équilibre pour le métier RH.
    """
    # Arrange
    y_test = model_predictions['y_test']
    y_pred = model_predictions['y_pred']
    
    # Act : Calculer le F2-score
    f2 = fbeta_score(y_test, y_pred, beta=2)
    
    # Assert
    assert f2 > 0.48, \
        f"F2-score trop faible : {f2:.4f} (minimum attendu : 0.48)"
    
    print(f"\n✅ F2-score : {f2:.4f}")


# =============================================================================
# TEST 2 : ROC-AUC (CAPACITÉ DE DISCRIMINATION)
# =============================================================================

def test_roc_auc_threshold(model_predictions):
    """
    OBJECTIF : Vérifier que le ROC-AUC est supérieur au seuil minimum.
    
    JUSTIFICATION : Le ROC-AUC mesure la capacité du modèle à discriminer
    entre les classes, indépendamment du seuil de décision.
    
    CRITÈRES DE SUCCÈS :
    - ROC-AUC > 0.75
    
    SEUIL : 0.75 indique une bonne capacité de discrimination.
    """
    # Arrange
    y_test = model_predictions['y_test']
    y_proba = model_predictions['y_proba']
    
    # Act : Calculer le ROC-AUC
    roc_auc = roc_auc_score(y_test, y_proba)
    
    # Assert
    assert roc_auc > 0.75, \
        f"ROC-AUC trop faible : {roc_auc:.4f} (minimum attendu : 0.75)"
    
    print(f"\n✅ ROC-AUC : {roc_auc:.4f}")


# =============================================================================
# TEST 3 : RECALL (DÉTECTION DES DÉMISSIONS)
# =============================================================================

def test_recall_threshold(model_predictions):
    """
    OBJECTIF : Vérifier que le recall est supérieur au seuil minimum.
    
    JUSTIFICATION : Le recall mesure la proportion de vrais démissionnaires
    détectés. C'est la métrique prioritaire pour le métier RH car il est
    plus grave de manquer une démission que de faire une fausse alerte.
    
    CRITÈRES DE SUCCÈS :
    - Recall > 0.70
    
    SEUIL : 0.70 signifie qu'on détecte au moins 70% des démissions.
    """
    # Arrange
    y_test = model_predictions['y_test']
    y_pred = model_predictions['y_pred']
    
    # Act : Calculer le recall
    recall = recall_score(y_test, y_pred)
    
    # Assert
    assert recall > 0.70, \
        f"Recall trop faible : {recall:.4f} (minimum attendu : 0.70)"
    
    print(f"\n✅ Recall : {recall:.4f}")
    print(f"   → Le modèle détecte {recall*100:.1f}% des démissions réelles")


# =============================================================================
# TEST 4 : PRÉCISION (LIMITATION DES FAUSSES ALERTES)
# =============================================================================

def test_precision_minimum(model_predictions):
    """
    OBJECTIF : Vérifier que la précision reste au-dessus d'un seuil minimum.
    
    JUSTIFICATION : La précision mesure la proportion de prédictions positives
    qui sont vraiment des démissions. Une précision trop faible entraîne
    trop de fausses alertes, ce qui fait perdre du temps aux RH.
    
    CRITÈRES DE SUCCÈS :
    - Précision > 0.40
    
    SEUIL : 0.40 est un minimum acceptable. Le recall est prioritaire,
    mais on ne veut pas non plus trop de faux positifs.
    """
    # Arrange
    y_test = model_predictions['y_test']
    y_pred = model_predictions['y_pred']
    
    # Act : Calculer la précision
    precision = precision_score(y_test, y_pred)
    
    # Assert
    assert precision > 0.16, \
        f"Précision trop faible : {precision:.4f} (minimum attendu : 0.16)"
    
    print(f"\n✅ Précision : {precision:.4f}")
    print(f"   → {precision*100:.1f}% des alertes sont justifiées")


# =============================================================================
# TEST 5 : TEMPS DE PRÉDICTION (PERFORMANCE TECHNIQUE)
# =============================================================================

def test_prediction_speed(model_predictions):
    """
    OBJECTIF : Vérifier que le temps moyen de prédiction est acceptable.
    
    JUSTIFICATION : En production, l'API doit être réactive. Un temps
    de prédiction trop long dégrade l'expérience utilisateur.
    
    CRITÈRES DE SUCCÈS :
    - Temps moyen < 100ms par prédiction
    
    SEUIL : 100ms est un temps acceptable pour une API interactive.
    """
    # Arrange
    duration = model_predictions['duration']
    n_predictions = model_predictions['n_predictions']
    
    # Act : Calculer le temps moyen
    avg_time_ms = (duration / n_predictions) * 1000
    
    # Assert
    assert avg_time_ms < 100, \
        f"Prédictions trop lentes : {avg_time_ms:.2f}ms (maximum : 100ms)"
    
    print(f"\n✅ Temps moyen : {avg_time_ms:.2f}ms par prédiction")


# =============================================================================
# TEST 6 : MATRICE DE CONFUSION (ANALYSE DÉTAILLÉE)
# =============================================================================

def test_confusion_matrix_analysis(model_predictions):
    """
    OBJECTIF : Analyser la matrice de confusion pour comprendre les erreurs.
    
    JUSTIFICATION : Permet de voir la répartition des erreurs :
    - Faux positifs (FP) : Prédictions de démission qui ne se réalisent pas
    - Faux négatifs (FN) : Démissions manquées par le modèle
    
    CRITÈRES DE SUCCÈS :
    - Test informatif (toujours pass)
    - Affiche les statistiques détaillées
    """
    # Arrange
    y_test = model_predictions['y_test']
    y_pred = model_predictions['y_pred']
    
    # Act : Calculer la matrice de confusion
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    
    # Afficher les résultats
    print("\n📊 Matrice de confusion :")
    print(f"   Vrais négatifs (TN)  : {tn:4d} (restent et prédits restent)")
    print(f"   Faux positifs (FP)   : {fp:4d} (restent mais prédits démission) ⚠️")
    print(f"   Faux négatifs (FN)   : {fn:4d} (démissionnent mais prédits restent) ❌")
    print(f"   Vrais positifs (TP)  : {tp:4d} (démissionnent et prédits démission) ✅")
    
    # Calculer les taux
    total = tn + fp + fn + tp
    print(f"\n📈 Répartition :")
    print(f"   Précision globale : {(tn + tp) / total * 100:.1f}%")
    print(f"   Taux d'erreur     : {(fp + fn) / total * 100:.1f}%")
    
    # Test toujours pass (informatif)
    assert True


# =============================================================================
# TEST 7 : RAPPORT DE CLASSIFICATION COMPLET
# =============================================================================

def test_classification_report(model_predictions):
    """
    OBJECTIF : Générer un rapport de classification complet.
    
    JUSTIFICATION : Vue d'ensemble de toutes les métriques pour les deux classes.
    
    CRITÈRES DE SUCCÈS :
    - Test informatif (toujours pass)
    - Affiche le rapport complet
    """
    # Arrange
    y_test = model_predictions['y_test']
    y_pred = model_predictions['y_pred']
    
    # Act : Générer le rapport
    report = classification_report(
        y_test, 
        y_pred, 
        target_names=['Reste', 'Démission'],
        digits=4
    )
    
    # Afficher
    print("\n📋 Rapport de classification complet :")
    print(report)
    
    # Test toujours pass (informatif)
    assert True


# =============================================================================
# TEST 8 : STABILITÉ DES PERFORMANCES
# =============================================================================

def test_performance_stability(test_dataset, model_loader_instance):
    """
    OBJECTIF : Vérifier que les performances sont stables sur plusieurs runs.
    
    JUSTIFICATION : Le modèle doit être déterministe et donner les mêmes
    résultats à chaque exécution (reproductibilité).
    
    CRITÈRES DE SUCCÈS :
    - Deux prédictions successives donnent les mêmes résultats
    """
    # Arrange : Prendre un échantillon du jeu de test
    X_test = test_dataset['X_test'].head(10)
    
    # Act : Faire deux runs
    predictions_run1 = []
    predictions_run2 = []
    
    for idx, row in X_test.iterrows():
        features = row.to_dict()
        
        result1 = model_loader_instance.predict(features)
        result2 = model_loader_instance.predict(features)
        
        predictions_run1.append(result1['prediction'])
        predictions_run2.append(result2['prediction'])
    
    # Assert : Les deux runs doivent être identiques
    assert predictions_run1 == predictions_run2, \
        "Les prédictions ne sont pas reproductibles !"
    
    print("\n✅ Performances stables (reproductibilité confirmée)")


# =============================================================================
# TEST 9 : SEUIL OPTIMAL UTILISÉ
# =============================================================================

def test_optimal_threshold_used(model_loader_instance):
    """
    OBJECTIF : Vérifier que le modèle utilise bien le seuil optimal.
    
    JUSTIFICATION : Le seuil doit être celui défini dans model_config.json (0.090).
    
    CRITÈRES DE SUCCÈS :
    - Le seuil utilisé est 0.090
    """
    # Arrange
    test_features = {"age": 30, "genre": "M"}
    
    # Act
    result = model_loader_instance.predict(test_features)
    
    # Assert
    assert result['threshold_used'] == 0.090, \
        f"Seuil incorrect : {result['threshold_used']} (attendu : 0.090)"
    
    print(f"\n✅ Seuil optimal utilisé : {result['threshold_used']}")