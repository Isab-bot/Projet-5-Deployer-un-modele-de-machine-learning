import pickle
import json
import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models import TrainingData
import joblib

print("📂 Chargement du dataset...")

# Charger le fichier pickle
with open('01_classe.joblib', 'rb') as f:
    df = joblib.load(f)

print(f"✅ Dataset chargé : {len(df)} lignes, {len(df.columns)} colonnes")
print(f"Colonnes : {df.columns.tolist()}")

# Connexion à la base de données
db = SessionLocal()

print("\n📥 Importation dans PostgreSQL...")

# Compteur pour suivre la progression
count = 0

for index, row in df.iterrows():
    # Extraire la target (démission)
    target_value = str(row['démission']) if pd.notna(row['démission']) else None
    
    # Créer un dictionnaire avec toutes les features SAUF démission
    features_dict = row.drop('démission').to_dict()
    
    # Convertir les valeurs NaN en None pour JSON
    features_dict = {k: (None if pd.isna(v) else v) for k, v in features_dict.items()}
    
    # Convertir en JSON
    features_json = json.dumps(features_dict)
    
    # Créer l'entrée dans la DB
    db_entry = TrainingData(
        identifier=f"RECORD_{index}",  # Identifiant auto-généré
        features=features_json,
        target=target_value
    )
    
    db.add(db_entry)
    count += 1
    
    # Commit par batch de 100 pour optimiser
    if count % 100 == 0:
        db.commit()
        print(f"  → {count}/{len(df)} lignes importées...")

# Commit final
db.commit()
db.close()

print(f"\n✅ Importation terminée ! {count} lignes ajoutées à la table 'training_data'")