# Base de Données

## Architecture SQLite

Le projet utilise SQLite avec 2 tables principales :
- `employees` : Données d'entraînement (1470 employés historiques)
- `predictions_logs` : Historique des prédictions effectuées par l'API

---

## Table 1 : employees

Table contenant les données d'entraînement du modèle (employés historiques).

### Structure

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identifiant unique |
| identifier | VARCHAR | UNIQUE, INDEX | Identifiant métier (ex: RECORD_0) |
| features | TEXT (JSON) | NOT NULL | Caractéristiques employé en JSON |
| target | VARCHAR | NULLABLE | Démission réelle : "Oui" ou "Non" |
| created_at | DATETIME | DEFAULT NOW | Date de création |

### Schéma SQL
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identifier VARCHAR UNIQUE NOT NULL,
    features TEXT NOT NULL,
    target VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_employees_identifier ON employees(identifier);
```

### Exemple de données
```json
{
    "id": 1,
    "identifier": "RECORD_0",
    "features": {
        "satisfaction_level": 0.38,
        "last_evaluation": 0.53,
        "number_project": 2,
        "average_montly_hours": 157,
        "time_spend_company": 3,
        "Work_accident": 0,
        "promotion_last_5years": 0,
        "departement": "sales",
        "salary": "low"
    },
    "target": "Oui",
    "created_at": "2025-12-07T10:30:00"
}
```

---

## Table 2 : predictions_logs

Table loggant toutes les prédictions effectuées par l'API pour traçabilité.

### Structure

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identifiant unique du log |
| employee_id | INTEGER | FOREIGN KEY, NULLABLE | Lien vers employé existant (si applicable) |
| input_features | TEXT (JSON) | NOT NULL | Features utilisées pour prédiction |
| prediction_result | VARCHAR | NOT NULL | Résultat : "Oui" ou "Non" |
| confidence_score | FLOAT | NULLABLE | Score de confiance (0.0 - 1.0) |
| model_version | VARCHAR | DEFAULT "v1.0" | Version du modèle ML utilisé |
| created_at | DATETIME | DEFAULT NOW | Timestamp de la prédiction |

### Schéma SQL
```sql
CREATE TABLE predictions_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    input_features TEXT NOT NULL,
    prediction_result VARCHAR NOT NULL,
    confidence_score REAL,
    model_version VARCHAR DEFAULT 'v1.0',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE INDEX idx_predictions_employee_id ON predictions_logs(employee_id);
CREATE INDEX idx_predictions_created_at ON predictions_logs(created_at);
```

### Exemple de log
```json
{
    "id": 42,
    "employee_id": 1,
    "input_features": {
        "satisfaction_level": 0.38,
        "departement": "sales",
        ...
    },
    "prediction_result": "Oui",
    "confidence_score": 0.87,
    "model_version": "v1.0",
    "created_at": "2025-12-07T14:23:15"
}
```

---

## Relations
```
employees (1) ←------ (0..N) predictions_logs
     ↑                           ↓
     └─── employee_id (FK) ──────┘
```

**Relation :**
- Un employé peut avoir zéro ou plusieurs prédictions loggées
- Une prédiction peut (optionnellement) référencer un employé existant
- `employee_id` nullable permet de logger aussi les prédictions pour nouveaux employés

---

## Requêtes Communes

### Historique complet des prédictions
```sql
SELECT * FROM predictions_logs 
ORDER BY created_at DESC;
```

### Prédictions des 7 derniers jours
```sql
SELECT * FROM predictions_logs 
WHERE created_at >= datetime('now', '-7 days')
ORDER BY created_at DESC;
```

### Statistiques globales
```sql
SELECT 
  COUNT(*) as total_predictions,
  SUM(CASE WHEN prediction_result = 'Oui' THEN 1 ELSE 0 END) as high_risk_count,
  AVG(confidence_score) as avg_confidence
FROM predictions_logs;
```

### Statistiques par département
```sql
SELECT 
  json_extract(input_features, '$.departement') as departement,
  COUNT(*) as total,
  SUM(CASE WHEN prediction_result = 'Oui' THEN 1 ELSE 0 END) as demissions_predites,
  AVG(confidence_score) as confiance_moyenne
FROM predictions_logs
GROUP BY departement
ORDER BY demissions_predites DESC;
```

### Prédictions pour un employé spécifique
```sql
SELECT 
  p.*,
  e.identifier,
  e.target as demission_reelle
FROM predictions_logs p
LEFT JOIN employees e ON p.employee_id = e.id
WHERE p.employee_id = 1
ORDER BY p.created_at DESC;
```

---

## Gestion de la Base

### Emplacement
```
./hr_analytics.db
```

### Backup
```bash
# Backup manuel
cp hr_analytics.db hr_analytics_backup_$(date +%Y%m%d).db

# Backup automatique (cron)
0 2 * * * cp /path/to/hr_analytics.db /path/to/backups/hr_analytics_$(date +\%Y\%m\%d).db
```

### Nettoyage
```sql
-- Supprimer logs > 1 an
DELETE FROM predictions_logs 
WHERE created_at < datetime('now', '-1 year');

-- Vacuum pour récupérer espace
VACUUM;
```

---

## Accès Programmatique

### Python (SQLAlchemy)
```python
from database import SessionLocal
from models import Employee, PredictionLog
import json

# Créer une session
db = SessionLocal()

# Récupérer un employé
employee = db.query(Employee).filter(Employee.id == 1).first()
print(f"Employé : {employee.identifier}, Target : {employee.target}")

# Logger une prédiction
new_log = PredictionLog(
    employee_id=1,
    input_features=json.dumps({"satisfaction_level": 0.75, ...}),
    prediction_result="Oui",
    confidence_score=0.87,
    model_version="v1.0"
)
db.add(new_log)
db.commit()

# Récupérer l'historique
logs = db.query(PredictionLog).order_by(PredictionLog.created_at.desc()).limit(10).all()
for log in logs:
    print(f"Log {log.id}: {log.prediction_result} (confiance: {log.confidence_score})")

db.close()
```

---

## Monitoring

### Taille de la base
```bash
# Linux/Mac
du -h hr_analytics.db

# Windows PowerShell
(Get-Item hr_analytics.db).Length / 1MB
```

### Nombre d'entrées
```sql
SELECT 
  (SELECT COUNT(*) FROM employees) as total_employees,
  (SELECT COUNT(*) FROM predictions_logs) as total_predictions;
```

### Croissance journalière
```sql
SELECT 
  DATE(created_at) as date,
  COUNT(*) as predictions_count
FROM predictions_logs
WHERE created_at >= datetime('now', '-30 days')
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

## Sécurité

### Permissions
```bash
# Restreindre accès (Linux/Mac)
chmod 600 hr_analytics.db

# Propriétaire uniquement
chown api_user:api_group hr_analytics.db
```

### Sauvegarde Chiffrée
```bash
# Backup chiffré avec OpenSSL
sqlite3 hr_analytics.db ".backup hr_analytics_backup.db"
openssl enc -aes-256-cbc -salt -in hr_analytics_backup.db -out hr_analytics_backup.db.enc
rm hr_analytics_backup.db
```

---

## Maintenance

### Optimisation
```sql
-- Analyser les statistiques
ANALYZE;

-- Reconstruire index
REINDEX;

-- Compacter la base
VACUUM;
```

### Vérification Intégrité
```bash
sqlite3 hr_analytics.db "PRAGMA integrity_check;"
```

---

## Migration vers PostgreSQL

Si besoin de migrer plus tard (volume croissant) :
```python
from sqlalchemy import create_engine
from models import Base, Employee, PredictionLog

# Source SQLite
sqlite_engine = create_engine('sqlite:///hr_analytics.db')

# Destination PostgreSQL
pg_engine = create_engine('postgresql://user:pass@localhost/hr_analytics')

# Créer tables PostgreSQL
Base.metadata.create_all(bind=pg_engine)

# Migrer données (exemple simplifié)
from sqlalchemy.orm import sessionmaker

SQLiteSession = sessionmaker(bind=sqlite_engine)
PgSession = sessionmaker(bind=pg_engine)

sqlite_session = SQLiteSession()
pg_session = PgSession()

# Migrer employees
employees = sqlite_session.query(Employee).all()
for emp in employees:
    pg_session.merge(emp)

# Migrer predictions_logs
logs = sqlite_session.query(PredictionLog).all()
for log in logs:
    pg_session.merge(log)

pg_session.commit()
```