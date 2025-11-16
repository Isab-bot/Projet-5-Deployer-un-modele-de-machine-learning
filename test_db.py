from database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("✅ Connexion réussie à PostgreSQL!")
        print(result.fetchone())
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")