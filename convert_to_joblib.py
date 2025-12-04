"""
Script pour convertir 01_classe.pkl en 01_classe.joblib
"""
import pickle
import joblib

print("🔄 Conversion de 01_classe.pkl → 01_classe.joblib...")

# Charger le fichier pickle
with open('01_classe.pkl', 'rb') as f:
    data = pickle.load(f)

# Sauvegarder en joblib
joblib.dump(data, '01_classe.joblib')

print("✅ Conversion terminée !")
print(f"📊 Taille : {len(data)} lignes")