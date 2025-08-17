#!/usr/bin/env python3
"""
Complete undo - move everything back from new directories to original
"""

import os
import shutil
from pathlib import Path

vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")

# Move remaining files from new dirs back to original structure
moves = [
    ("World/*", "02_Worldbuilding"),
    ("Adventures/*", "01_Adventures"),
    ("Characters/*", "07_Player_Resources"),
    ("Resources/*", "04_Resources"),
    ("System/*", "00_System"),
    ("Archive/*", "08_Archive"),
    ("Rules/*", "05_Rules"),
]

for source_pattern, target in moves:
    source_dir = vault_path / source_pattern.replace("/*", "")
    target_dir = vault_path / target
    
    if source_dir.exists() and source_dir.is_dir():
        target_dir.mkdir(exist_ok=True)
        
        # Move all contents
        for item in source_dir.iterdir():
            if item.name.startswith('.'):
                continue
            
            dest = target_dir / item.name
            if not dest.exists():
                try:
                    shutil.move(str(item), str(dest))
                    print(f"✓ Moved {item.name} to {target}")
                except Exception as e:
                    print(f"⚠️ Could not move {item.name}: {e}")

# Remove new directories if empty
new_dirs = ["Adventures", "World", "Rules", "Resources", "Characters", "System", "Archive"]
for dir_name in new_dirs:
    dir_path = vault_path / dir_name
    if dir_path.exists():
        try:
            if not list(dir_path.iterdir()):
                dir_path.rmdir()
                print(f"✓ Removed empty {dir_name}")
        except:
            pass

print("\n✅ Complete undo finished - original structure restored")