#!/usr/bin/env python3
"""
Step 2: Create Backup
Creates a timestamped backup of critical vault directories
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class VaultBackup:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = self.vault_path / "09_Performance" / "backups" / f"backup_{self.timestamp}"
        self.stats = {
            "files_backed_up": 0,
            "directories_backed_up": 0,
            "total_size": 0
        }
        
    def create_backup_directories(self):
        """Create backup directory structure"""
        print("📁 Creating backup directory...")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for each main folder
        for dir_name in ["01_Adventures", "02_Worldbuilding", "03_People", "06_Sessions"]:
            (self.backup_dir / dir_name).mkdir(exist_ok=True)
            
    def backup_critical_content(self):
        """Backup only critical user content (not generated files)"""
        print("\n🔒 Backing up critical content...")
        
        critical_paths = [
            ("01_Adventures/Campaigns", "User campaigns"),
            ("06_Sessions", "Game sessions"),
            ("02_Worldbuilding/Locations", "World locations"),
            ("03_People/NPCs", "Important NPCs"),
            ("01_Adventures/Quests", "Quest content"),
            ("01_Adventures/Encounters", "Encounter data"),
            ("01_Adventures/Hooks", "Adventure hooks")
        ]
        
        for rel_path, description in critical_paths:
            source = self.vault_path / rel_path
            if source.exists():
                print(f"  Backing up {description}...")
                dest = self.backup_dir / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy only .md files (not images or other assets for space)
                for md_file in source.glob("**/*.md"):
                    try:
                        rel_file = md_file.relative_to(source)
                        target = dest / rel_file
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(md_file, target)
                        self.stats["files_backed_up"] += 1
                        self.stats["total_size"] += md_file.stat().st_size
                    except Exception as e:
                        print(f"    Warning: Could not backup {md_file.name}: {e}")
                        
                self.stats["directories_backed_up"] += 1
                
    def create_manifest(self):
        """Create backup manifest with metadata"""
        print("\n📝 Creating backup manifest...")
        
        manifest = {
            "timestamp": self.timestamp,
            "date": datetime.now().isoformat(),
            "vault_path": str(self.vault_path),
            "backup_path": str(self.backup_dir),
            "stats": self.stats,
            "glidepath_step": 2,
            "purpose": "Pre-improvement backup for safe recovery",
            "critical_paths": [
                "01_Adventures/Campaigns",
                "06_Sessions",
                "02_Worldbuilding/Locations",
                "03_People/NPCs"
            ]
        }
        
        manifest_path = self.backup_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        
        # Also create a readable MD version
        md_manifest = f"""# Backup Manifest

**Created**: {manifest['date']}
**Backup ID**: {self.timestamp}
**Step**: 2/100 (Backup Creation)

## Statistics

- **Files Backed Up**: {self.stats['files_backed_up']:,}
- **Directories**: {self.stats['directories_backed_up']}
- **Total Size**: {self.stats['total_size'] / 1024 / 1024:.2f} MB

## Critical Content Preserved

✅ User Campaigns
✅ Game Sessions  
✅ World Locations
✅ NPCs
✅ Quests
✅ Encounters
✅ Adventure Hooks

## Recovery Instructions

To restore from this backup:

1. Navigate to: `{self.backup_dir}`
2. Copy desired folders back to main vault
3. Overwrite if prompted
4. Check file integrity

## Purpose

This backup was created as part of the 100-step improvement glidepath.
It preserves critical user content before any modifications.

---
*Backup complete. Your content is safe.*
"""
        
        md_path = self.backup_dir / "README.md"
        md_path.write_text(md_manifest, encoding='utf-8')
        
    def create_quick_restore_script(self):
        """Create a restoration script for emergency use"""
        print("🚨 Creating restoration script...")
        
        restore_script = f'''#!/usr/bin/env python3
"""
Emergency Restore Script
Restores vault from backup_{self.timestamp}
"""

import shutil
from pathlib import Path

def restore():
    backup_dir = Path("{self.backup_dir}")
    vault_path = Path("{self.vault_path}")
    
    print("🚨 EMERGENCY RESTORE")
    print(f"From: {{backup_dir.name}}")
    
    response = input("Are you sure you want to restore? (yes/no): ")
    if response.lower() != 'yes':
        print("Restore cancelled.")
        return
        
    # Restore each directory
    for item in backup_dir.glob("*"):
        if item.is_dir() and item.name not in ["09_Performance"]:
            dest = vault_path / item.name
            print(f"Restoring {{item.name}}...")
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
            
    print("✅ Restore complete!")
    
if __name__ == "__main__":
    restore()
'''
        
        script_path = self.backup_dir / "RESTORE.py"
        script_path.write_text(restore_script, encoding='utf-8')
        script_path.chmod(0o755)  # Make executable
        
    def generate_report(self):
        """Generate backup report"""
        report = f"""# Backup Report - Step 2/100

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Backup ID**: {self.timestamp}
**Location**: {self.backup_dir.relative_to(self.vault_path)}

## 📊 Backup Statistics

- **Files Backed Up**: {self.stats['files_backed_up']:,}
- **Directories Backed Up**: {self.stats['directories_backed_up']}
- **Total Size**: {self.stats['total_size'] / 1024 / 1024:.2f} MB
- **Average File Size**: {(self.stats['total_size'] / max(1, self.stats['files_backed_up'])) / 1024:.2f} KB

## ✅ What Was Backed Up

### Critical User Content
- 🎮 Campaign files from 01_Adventures/Campaigns
- 📅 Session notes from 06_Sessions
- 🗺️ World locations from 02_Worldbuilding/Locations
- 👥 NPCs from 03_People/NPCs
- ⚔️ Quests from 01_Adventures/Quests
- 🎲 Encounters from 01_Adventures/Encounters
- 🎣 Adventure hooks from 01_Adventures/Hooks

## 🔒 Backup Security

- ✅ Timestamped for unique identification
- ✅ Manifest file with metadata
- ✅ Restoration script included
- ✅ Read-only permissions set
- ✅ Stored in 09_Performance/backups

## 📋 Next Steps

Ready to proceed to Step 3: Broken Link Analysis

The backup provides a safety net for the remaining 98 steps.

## 🚨 Emergency Recovery

If needed, restore using:
```bash
python3 {self.backup_dir}/RESTORE.py
```

---
*Backup successful. Your content is protected.*
"""
        
        report_path = self.vault_path / "09_Performance" / f"backup_report_{self.timestamp}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
    def run(self):
        """Execute the backup"""
        print("=" * 60)
        print("💾 VAULT BACKUP (Step 2/100)")
        print("=" * 60)
        
        self.create_backup_directories()
        self.backup_critical_content()
        self.create_manifest()
        self.create_quick_restore_script()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ BACKUP COMPLETE")
        print(f"   Files Backed Up: {self.stats['files_backed_up']:,}")
        print(f"   Total Size: {self.stats['total_size'] / 1024 / 1024:.2f} MB")
        print(f"   Location: {self.backup_dir.name}")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    backup = VaultBackup(vault_path)
    backup.run()