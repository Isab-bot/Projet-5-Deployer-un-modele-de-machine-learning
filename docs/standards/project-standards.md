# Standards du Projet

## Conventions de Code

- PEP 8 pour Python
- Type hints obligatoires
- Docstrings pour toutes les fonctions

## Structure des Fichiers

\\\
projet/
├── main.py           # API FastAPI
├── models.py         # Modeles SQLAlchemy
├── schemas.py        # Schemas Pydantic
├── model_loader.py   # Chargement modele
├── tests/            # Tests pytest
└── docs/             # Documentation MkDocs
\\\

## Git Workflow

- Branch main protegee
- Pull requests obligatoires
- Tests automatiques avant merge