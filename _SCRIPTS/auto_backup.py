#!/usr/bin/env python3
"""
Automated backup script for critical vault files
"""
import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def backup_critical_files():
    """Backup campaigns, sessions, and important NPCs"""
    backup_dir = Path("08_Archive/automated_backups") / datetime.now().strftime("%Y%m%d")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    critical_paths = [
        "06_Sessions",
        "01_Adventures/Campaigns",
        "00_System/Templates"
    ]
    
    files_backed_up = 0
    
    for path_str in critical_paths:
        path = Path(path_str)
        if path.exists():
            for file in path.rglob("*.md"):
                relative = file.relative_to(path)
                target = backup_dir / path_str / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
                files_backed_up += 1
    
    # Create manifest
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "files_backed_up": files_backed_up,
        "backup_location": str(backup_dir)
    }
    
    with open(backup_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Backup complete: {files_backed_up} files backed up to {backup_dir}")
    return backup_dir

if __name__ == "__main__":
    backup_critical_files()
