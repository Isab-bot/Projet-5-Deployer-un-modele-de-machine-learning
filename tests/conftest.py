import pytest
import json
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ORDRE IMPORTANT : D'abord Base, puis les modèles
from database import Base, get_db
from main import app
from model_loader import model_loader
from models import TrainingData, PredictionLog

# =============================================================================
# CONFIGURATION DE LA BASE DE DONNÉES DE TEST
# =============================================================================

# IMPORTANT : Utiliser StaticPool pour partager la connexion
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ← AJOUT IMPORTANT pour partager la connexion
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture(scope="module")  # ← scope="module" au lieu de "function"
def db_session():
    """
    Fixture pour une session de base de données de test.
    
    Scope "module" = même DB pour tous les tests du module.
    """
    # Créer toutes les tables
    Base.metadata.create_all(bind=test_engine)
    
    print(f"\n📋 Tables créées : {Base.metadata.tables.keys()}")
    
    # Créer UNE session partagée
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="module")
def client(db_session):
    """
    Fixture pour le client de test FastAPI.
    Configure la base de données ET l'API Key pour les tests.
    """
    def override_get_db():
        yield db_session

    # Override de la base de données
    app.dependency_overrides[get_db] = override_get_db
    
    # ✅ Définir l'API Key pour les tests
    os.environ["API_KEY"] = "test-api-key-for-ci"

    with TestClient(app) as test_client:
        yield test_client
    
    # Nettoyer les overrides
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def valid_employee_data():
    """Fixture pour les données d'un employé valide."""
    with open('tests/data/valid_employee.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="session")
def invalid_employee_data():
    """Fixture pour les données d'un employé invalide."""
    with open('tests/data/invalid_employee.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="session")
def edge_cases_data():
    """Fixture pour les cas limites."""
    with open('tests/data/edge_cases.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope="session")
def model_loader_instance():
    """
    Fixture pour l'instance du model_loader.
    """
    from model_loader import ModelLoader
    
    loader = ModelLoader()
    loader.load_model()
    
    return loader


# =============================================================================
# CONFIGURATION GLOBALE DE PYTEST
# =============================================================================

def pytest_configure(config):
    """Configuration globale de pytest."""
    config.addinivalue_line(
        "markers", "unit: Tests unitaires (rapides)"
    )
    config.addinivalue_line(
        "markers", "functional: Tests fonctionnels (plus lents)"
    )
    config.addinivalue_line(
        "markers", "slow: Tests lents (performance, DB)"
    )