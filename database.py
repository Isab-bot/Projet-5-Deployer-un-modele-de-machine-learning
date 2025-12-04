from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException, status  
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__) 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hr_analytics.db")  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance pour FastAPI
def get_db():
    """Fournit une session de base de données avec gestion d'erreurs."""
    db = SessionLocal()
    try:
        # Tester la connexion
        db.execute(text("SELECT 1"))
        yield db
    except OperationalError as e:
        logger.error(f"❌ Impossible de se connecter à la base de données : {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de données non accessible"
        )
    finally:
        db.close()
