# Base de Donnees

## Schema SQLite

### Table : predictions

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER | Cle primaire auto-incrementee |
| employee_data | JSON | Donnees employe (format JSON) |
| prediction | INTEGER | Prediction (0 = Reste, 1 = Demission) |
| probability | FLOAT | Probabilite de demission (0.0 - 1.0) |
| timestamp | DATETIME | Date et heure de la prediction |

### Structure Complete
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_data TEXT NOT NULL,
    prediction INTEGER NOT NULL,
    probability REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Requetes Communes

### Historique complet
```sql
SELECT * FROM predictions 
ORDER BY timestamp DESC;
```

### Predictions des 7 derniers jours
```sql
SELECT * FROM predictions 
WHERE timestamp >= datetime('now', '-7 days')
ORDER BY timestamp DESC;
```

### Statistiques globales
```sql
SELECT 
  COUNT(*) as total_predictions,
  SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as high_risk_count,
  AVG(probability) as avg_probability
FROM predictions;
```

### Statistiques par departement
```sql
SELECT 
  json_extract(employee_data, '$.departement') as departement,
  COUNT(*) as total,
  SUM(prediction) as demissions_predites,
  AVG(probability) as probabilite_moyenne
FROM predictions
GROUP BY departement
ORDER BY demissions_predites DESC;
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
-- Supprimer predictions > 1 an
DELETE FROM predictions 
WHERE timestamp < datetime('now', '-1 year');

-- Vacuum pour recuperer espace
VACUUM;
```

---

## Acces Programmatique

### Python
```python
import sqlite3
import json
from datetime import datetime

# Connexion
conn = sqlite3.connect('hr_analytics.db')
cursor = conn.cursor()

# Inserer une prediction
employee_data = {
    "satisfaction_level": 0.75,
    "departement": "IT",
    # ...
}

cursor.execute("""
    INSERT INTO predictions (employee_data, prediction, probability)
    VALUES (?, ?, ?)
""", (json.dumps(employee_data), 1, 0.85))

conn.commit()

# Recuperer l'historique
cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 10")
results = cursor.fetchall()

for row in results:
    print(f"ID: {row[0]}, Prediction: {row[2]}, Probabilite: {row[3]}")

conn.close()
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

### Nombre d'entrees
```sql
SELECT COUNT(*) FROM predictions;
```

### Croissance journaliere
```sql
SELECT 
  DATE(timestamp) as date,
  COUNT(*) as predictions_count
FROM predictions
WHERE timestamp >= datetime('now', '-30 days')
GROUP BY DATE(timestamp)
ORDER BY date DESC;
```

---

## Securite

### Permissions
```bash
# Restreindre acces (Linux/Mac)
chmod 600 hr_analytics.db

# Proprietaire uniquement
chown api_user:api_group hr_analytics.db
```

### Sauvegarde Chiffree
```bash
# Backup chiffre avec OpenSSL
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

-- Reconstruire index (si necessaire)
REINDEX;

-- Compacter la base
VACUUM;
```

### Verification Integrite
```bash
# Verifier integrite
sqlite3 hr_analytics.db "PRAGMA integrity_check;"
```

---

## Migration

Si besoin de migrer vers PostgreSQL ou MySQL plus tard :
```python
import sqlite3
import psycopg2
import json

# SQLite source
sqlite_conn = sqlite3.connect('hr_analytics.db')
sqlite_cursor = sqlite_conn.cursor()

# PostgreSQL destination
pg_conn = psycopg2.connect("dbname=hr_analytics user=postgres")
pg_cursor = pg_conn.cursor()

# Migrer donnees
sqlite_cursor.execute("SELECT * FROM predictions")
for row in sqlite_cursor.fetchall():
    pg_cursor.execute("""
        INSERT INTO predictions (id, employee_data, prediction, probability, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """, row)

pg_conn.commit()
```