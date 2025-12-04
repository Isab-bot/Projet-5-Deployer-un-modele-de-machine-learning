import json
import pandas as pd
import os
import joblib
from database import SessionLocal, engine
from models import Base, Employee

# Supprimer l'ancienne base si elle existe
DB_PATH = "hr_analytics.db"
if os.path.exists(DB_PATH):
    print(f"🗑️  Suppression de l'ancienne base : {DB_PATH}")
    os.remove(DB_PATH)

# Recréer les tables
print("📋 Création des tables...")
Base.metadata.create_all(bind=engine)

print("📂 Chargement du dataset...")

# Charger le fichier joblib
with open('01_classe.joblib', 'rb') as f:
    df = joblib.load(f)

print(f"✅ Dataset chargé : {len(df)} lignes, {len(df.columns)} colonnes")
print(f"Colonnes : {df.columns.tolist()}")

# Connexion à la base de données
db = SessionLocal()

print("\n📥 Importation dans la base de données...")

count = 0

try:
    for index, row in df.iterrows():
        target_value = str(row['démission']) if pd.notna(row['démission']) else None
        features_dict = row.drop('démission').to_dict()
        features_dict = {k: (None if pd.isna(v) else v) for k, v in features_dict.items()}
        features_json = json.dumps(features_dict)
        
        db_entry = Employee(
            identifier=f"RECORD_{index}",
            features=features_json,
            target=target_value
        )
        
        db.add(db_entry)
        count += 1
        
        if count % 100 == 0:
            db.commit()
            print(f"  → {count}/{len(df)} lignes importées...")
    
    db.commit()
    print(f"\n✅ {count} lignes ajoutées à la table 'employees'")

except Exception as e:
    db.rollback()
    print(f"❌ Erreur : {e}")
    raise

finally:
    db.close()