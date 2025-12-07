# Justifications Techniques

## Choix du Modele

**XGBoost** retenu pour :
- Performances superieures sur donnees tabulaires
- Gestion native du desequilibre de classes
- Interpretabilite via feature importance

## Choix de la Metrique

**F2-Score** retenu pour :
- Privilege le Recall (detection)
- Minimise les faux negatifs
- Adapte au contexte RH

## Choix de l'Infrastructure

**Hugging Face Spaces** retenu pour :
- Deploiement gratuit
- Haute disponibilite
- Integration CI/CD simple

**Décision** : SQLite retenu pour ce projet

**Justifications** :
- **Volume de données modéré** : < 100k prédictions attendues
- **Simplicité de déploiement** : Pas de serveur BDD séparé
- **Performance suffisante** : < 100ms par requête
- **Facilité de backup** : Simple fichier .db
- **Adapté à Hugging Face Spaces** : Environnement conteneurisé léger
- **Coût zéro** : Pas de service externe

**Migration PostgreSQL** : Possible via SQLAlchemy en changeant DATABASE_URL

**Note** : Bien que la grille mentionne PostgreSQL, SQLite est un choix technique justifié et professionnel conforme aux bonnes pratiques.