# Standards de Test

## Couverture de Tests

### Objectifs

- **Couverture minimale** : 80% du code
- **Types de tests** : Unitaires + Fonctionnels + Integration
- **Tests actuels** : 51 tests (tous passent)

### Execution des Tests
```bash
# Lancer tous les tests
uv run pytest

# Lancer avec verbosity
uv run pytest -v

# Lancer avec coverage
uv run pytest --cov

# Lancer tests specifiques
uv run pytest tests/test_api.py

# Lancer en mode watch (relance auto)
uv run pytest-watch
```

---

## Structure des Tests

### Organisation des Fichiers
```
tests/
├── test_api.py           # Tests endpoints API
├── test_model.py         # Tests modele ML
├── test_database.py      # Tests base de donnees
├── test_schemas.py       # Tests validation Pydantic
├── conftest.py           # Fixtures pytest
└── __init__.py
```

### Nomenclature

- **Fichiers** : `test_*.py`
- **Fonctions** : `test_*`
- **Classes** : `Test*`

---

## Types de Tests

### Tests Unitaires

**Objectif** : Tester des fonctions isolees

**Exemple :**
```python
def test_load_model():
    """Test du chargement du modele"""
    from model_loader import load_pipeline
    pipeline = load_pipeline()
    assert pipeline is not None
    assert hasattr(pipeline, 'predict')
```

### Tests Fonctionnels

**Objectif** : Tester les endpoints API

**Exemple :**
```python
def test_predict_endpoint(client):
    """Test de l'endpoint /predict"""
    response = client.post(
        "/predict",
        json=valid_employee_data,
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
```

### Tests d'Integration

**Objectif** : Tester l'interaction entre composants

**Exemple :**
```python
def test_prediction_workflow(client, db_session):
    """Test du workflow complet de prediction"""
    # 1. Faire une prediction
    response = client.post("/predict", json=data)
    
    # 2. Verifier que c'est enregistre en DB
    log = db_session.query(PredictionLog).first()
    assert log is not None
    
    # 3. Verifier qu'on peut recuperer l'historique
    history = client.get("/history")
    assert len(history.json()) == 1
```

---

## Fixtures Pytest

### Configuration dans conftest.py
```python
import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine

@pytest.fixture
def client():
    """Client de test FastAPI"""
    return TestClient(app)

@pytest.fixture
def db_session():
    """Session de base de donnees de test"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def valid_employee_data():
    """Donnees employe valides pour tests"""
    return {
        "satisfaction_level": 0.75,
        "last_evaluation": 0.82,
        "number_project": 3,
        "average_montly_hours": 180,
        "time_spend_company": 2,
        "Work_accident": 0,
        "promotion_last_5years": 0,
        "departement": "IT",
        "salary": "medium"
    }
```

---

## Tests de l'API

### Test Health Check
```python
def test_health_check(client):
    """Test de l'endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Test Authentification
```python
def test_predict_without_api_key(client):
    """Test prediction sans API key"""
    response = client.post("/predict", json={})
    assert response.status_code == 401

def test_predict_with_invalid_api_key(client):
    """Test prediction avec API key invalide"""
    response = client.post(
        "/predict",
        json={},
        headers={"X-API-Key": "invalid"}
    )
    assert response.status_code == 401
```

### Test Validation
```python
def test_predict_missing_field(client):
    """Test prediction avec champ manquant"""
    incomplete_data = {"satisfaction_level": 0.5}
    response = client.post(
        "/predict",
        json=incomplete_data,
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 422
```

---

## Tests du Modele

### Test Chargement
```python
def test_model_loading():
    """Test du chargement du pipeline"""
    from model_loader import load_pipeline
    pipeline = load_pipeline()
    assert pipeline is not None
```

### Test Prediction
```python
def test_model_prediction(valid_employee_data):
    """Test de prediction du modele"""
    from model_loader import load_pipeline
    import pandas as pd
    
    pipeline = load_pipeline()
    df = pd.DataFrame([valid_employee_data])
    prediction = pipeline.predict(df)
    
    assert prediction is not None
    assert prediction[0] in [0, 1]
```

### Test Probabilites
```python
def test_model_probabilities(valid_employee_data):
    """Test des probabilites"""
    from model_loader import load_pipeline
    import pandas as pd
    
    pipeline = load_pipeline()
    df = pd.DataFrame([valid_employee_data])
    probas = pipeline.predict_proba(df)
    
    assert probas is not None
    assert len(probas[0]) == 2
    assert 0 <= probas[0][1] <= 1
```

---

## Bonnes Pratiques

### 1. Tests Independants

Chaque test doit pouvoir s'executer independamment.
```python
# BON
def test_feature_a():
    data = create_test_data()
    result = function_a(data)
    assert result == expected

# MAUVAIS (depend de l'ordre d'execution)
global_data = None

def test_setup():
    global global_data
    global_data = create_data()

def test_feature():
    assert function(global_data) == expected
```

### 2. Noms Descriptifs
```python
# BON
def test_predict_returns_high_risk_for_low_satisfaction():
    ...

# MAUVAIS
def test_1():
    ...
```

### 3. AAA Pattern

Arrange - Act - Assert
```python
def test_prediction():
    # Arrange : Preparer les donnees
    employee_data = {...}
    
    # Act : Executer l'action
    response = client.post("/predict", json=employee_data)
    
    # Assert : Verifier le resultat
    assert response.status_code == 200
    assert "prediction" in response.json()
```

### 4. Utiliser Parametrize
```python
import pytest

@pytest.mark.parametrize("satisfaction,expected_risk", [
    (0.1, "HIGH"),
    (0.5, "MEDIUM"),
    (0.9, "LOW")
])
def test_risk_levels(satisfaction, expected_risk):
    data = create_employee_data(satisfaction_level=satisfaction)
    response = client.post("/predict", json=data)
    assert response.json()["risk_level"] == expected_risk
```

---

## Couverture de Code

### Generer un Rapport
```bash
# Rapport console
uv run pytest --cov

# Rapport HTML
uv run pytest --cov --cov-report=html

# Ouvrir le rapport
# Windows :
start htmlcov/index.html
# Mac :
open htmlcov/index.html
```

### Seuil Minimum

Configuration dans `pyproject.toml` :
```toml
[tool.pytest.ini_options]
addopts = "--cov --cov-report=term-missing --cov-fail-under=80"
```

---

## CI/CD Integration

### GitHub Actions
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: uv run pytest --cov --cov-fail-under=80
```

---

## Commandes Utiles
```bash
# Tests avec markers
uv run pytest -m "not slow"

# Tests en parallele
uv run pytest -n auto

# Arreter au premier echec
uv run pytest -x

# Mode verbose + afficher print()
uv run pytest -v -s

# Relancer seulement les tests echoues
uv run pytest --lf
```