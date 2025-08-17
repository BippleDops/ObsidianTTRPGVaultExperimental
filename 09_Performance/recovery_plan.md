# Vault Recovery Plan

## Backup Locations

1. **Primary Backup**: `09_Performance/backups/backup_20250815_173537/`
2. **Archive**: `08_Archive/`
3. **Scripts**: `_SCRIPTS/`

## Recovery Procedures

### Campaign/Session Recovery
```bash
python3 _SCRIPTS/EMERGENCY_RECOVERY.py
```

### Broken Link Cleanup
```bash
python3 _SCRIPTS/REMOVE_BROKEN_LINK_FILES.py
```

### Full Restore
```bash
python3 09_Performance/backups/backup_20250815_173537/RESTORE.py
```

## Critical Paths to Protect

- `01_Adventures/Campaigns/`
- `06_Sessions/`
- `03_People/NPCs/`
- `02_Worldbuilding/Locations/`

## Emergency Contacts

- Vault Owner: User
- Last Good Backup: 2025-08-15 17:35
- Recovery Time Objective: < 5 minutes
