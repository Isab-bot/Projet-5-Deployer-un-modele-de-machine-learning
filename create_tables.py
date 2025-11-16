from database import engine, Base
from models import TrainingData, Prediction

print("Création des tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables créées avec succès !")