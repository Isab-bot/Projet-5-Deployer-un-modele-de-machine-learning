# Retraining du Modele

## Quand Retrainer ?

- Tous les mois (minimum)
- Si performance < seuil
- Si nouveaux patterns detectes

## Processus

1. Collecter donnees etiquetees
2. Entrainer nouveau modele
3. Evaluer sur test set
4. Comparer a l'ancien modele
5. Deployer si meilleur

## Validation

Le nouveau modele doit avoir :
- F2-Score > modele actuel
- Recall >= 90%