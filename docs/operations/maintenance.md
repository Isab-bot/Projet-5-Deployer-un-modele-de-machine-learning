# Protocole de Maintenance

## Monitoring Quotidien

### Verifications a Effectuer

**Chaque matin (10 minutes) :**

1. **Verifier les logs d'erreur**
```bash
   # Logs des dernieres 24h
   grep "ERROR" logs/api.log | tail -50
```

2. **Controler les temps de reponse**
   - Ouvrir https://Fox6768-api-demission-prediction.hf.space/health
   - Temps de reponse doit etre < 200ms

3. **Surveiller l'utilisation**
```bash
   # Nombre de predictions aujourd'hui
   sqlite3 hr_analytics.db "SELECT COUNT(*) FROM predictions WHERE DATE(timestamp) = DATE('now')"
```

4. **Verifier l'espace disque**
```bash
   df -h
```

---

## Retraining Mensuel

### Calendrier

- **Frequence** : 1er de chaque mois
- **Duree estimee** : 2-3 heures
- **Responsable** : Data Scientist

### Processus Complet

**1. Collecter nouvelles donnees**
```bash
# Exporter les predictions du mois
sqlite3 hr_analytics.db <<EOF
.mode csv
.output predictions_$(date +%Y%m).csv
SELECT * FROM predictions WHERE timestamp >= datetime('now', '-1 month');
EOF
```

**2. Valider la qualite des donnees**

- Verifier absence de valeurs manquantes
- Verifier coherence des donnees
- Identifier anomalies

**3. Reentrainer le modele**
```bash
# Lancer script de retraining
uv run python train_final_model.py
```

**4. Evaluer performances**
```python
# Comparer avec modele actuel
# F2-Score doit etre >= modele actuel
# Recall doit etre >= 90%
```

**5. Deployer si meilleur**
```bash
# Backup ancien modele
cp pipeline_xgboost_optimised.joblib pipeline_xgboost_backup_$(date +%Y%m%d).joblib

# Deployer nouveau modele
# (automatique via GitHub Actions)
git add pipeline_xgboost_optimised.joblib
git commit -m "feat: update model $(date +%Y-%m-%d)"
git push
```

---

## Backup Hebdomadaire

### Automatisation

**Script de backup (Linux/Mac) :**
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup base de donnees
cp hr_analytics.db "$BACKUP_DIR/hr_analytics_$DATE.db"

# Backup modele
cp pipeline_xgboost_optimised.joblib "$BACKUP_DIR/model_$DATE.joblib"

# Nettoyer backups > 30 jours
find "$BACKUP_DIR" -name "*.db" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.joblib" -mtime +30 -delete

echo "Backup complete : $DATE"
```

**Cron job (chaque dimanche a 2h) :**
```bash
0 2 * * 0 /path/to/backup.sh
```

**Script PowerShell (Windows) :**
```powershell
# backup.ps1
$BackupDir = "C:\Backups"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"

Copy-Item "hr_analytics.db" "$BackupDir\hr_analytics_$Date.db"
Copy-Item "pipeline_xgboost_optimised.joblib" "$BackupDir\model_$Date.joblib"

# Nettoyer > 30 jours
Get-ChildItem $BackupDir -Filter "*.db" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
Get-ChildItem $BackupDir -Filter "*.joblib" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
```

---

## Alertes Automatiques

### Configuration

**1. Temps de reponse > 2s**
```python
# monitoring.py
import requests
import time

start = time.time()
response = requests.get("https://Fox6768-api-demission-prediction.hf.space/health")
duration = time.time() - start

if duration > 2.0:
    send_alert(f"ALERTE: Temps de reponse eleve ({duration:.2f}s)")
```

**2. Taux d'erreur > 5%**
```python
# Calculer taux d'erreur sur dernieres 100 requetes
error_rate = calculate_error_rate(last_100_requests)

if error_rate > 0.05:
    send_alert(f"ALERTE: Taux d'erreur eleve ({error_rate*100:.1f}%)")
```

**3. Stockage > 80%**
```bash
# disk_monitor.sh
USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ $USAGE -gt 80 ]; then
    echo "ALERTE: Espace disque > 80% ($USAGE%)"
fi
```

---

## Incidents Courants

### 1. API ne repond pas

**Diagnostic :**
```bash
# Verifier si processus tourne
ps aux | grep uvicorn

# Verifier logs
tail -f logs/api.log
```

**Solution :**
```bash
# Redemarrer API
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Predictions incorrectes

**Diagnostic :**
- Verifier version du modele
- Comparer avec predictions attendues
- Analyser feature importance

**Solution :**
- Reentrainer modele si necessaire
- Rollback vers version precedente

### 3. Base de donnees corrompue

**Diagnostic :**
```bash
sqlite3 hr_analytics.db "PRAGMA integrity_check;"
```

**Solution :**
```bash
# Restaurer depuis backup
cp /backups/hr_analytics_latest.db hr_analytics.db
```

---

## Checklist Mensuelle

- [ ] Retraining du modele
- [ ] Verification backups
- [ ] Analyse des logs d'erreur
- [ ] Revue des metriques de performance
- [ ] Mise a jour dependencies (si necessaire)
- [ ] Test de restauration backup
- [ ] Documentation des incidents

---

## Contacts Urgence

| Role | Contact | Disponibilite |
|------|---------|---------------|
| Admin Systeme | admin@company.com | 24/7 |
| Data Scientist | ds@company.com | Lun-Ven 9h-18h |
| DevOps | devops@company.com | 24/7 |

---

## Historique Maintenance

| Date | Action | Responsable | Resultat |
|------|--------|-------------|----------|
| 2024-12-01 | Retraining modele | I.R. | F2=0.68 (stable) |
| 2024-11-15 | Backup DB | Auto | OK |
| 2024-11-01 | Update deps | I.R. | OK |

---

## Documentation Complementaire

- [Monitoring](monitoring.md) - Metriques et dashboards
- [Retraining](retraining.md) - Processus detaille
- [Rollback](rollback.md) - Procedures d'urgence