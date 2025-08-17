# Vault Automation Scripts

## Available Scripts

### 🤖 auto_organizer.py
Organizes new files into appropriate folders

### 🔗 link_checker.py
Checks for broken links and generates reports

### 💾 auto_backup.py
Backs up critical campaign and session files

### 🎲 session_prep.py
Prepares templates and gathers NPCs for sessions

### 🎛️ vault_automation.py
Master controller - runs all automation tasks

## Usage

Run individual scripts:
```bash
python3 _SCRIPTS/script_name.py
```

Run all automation:
```bash
python3 _SCRIPTS/vault_automation.py
```

## Schedule

Recommended automation schedule:
- **Daily**: link_checker.py
- **Before Sessions**: session_prep.py
- **Weekly**: auto_organizer.py, auto_backup.py
- **Monthly**: Full vault_automation.py

## Safety

All scripts are designed to be safe:
- No deletions without confirmation
- Backups before major changes
- Detailed logging
- Timeout protection
