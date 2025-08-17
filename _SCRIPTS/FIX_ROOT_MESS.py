#!/usr/bin/env python3
"""
EMERGENCY FIX: Remove all the crap I added to root and those bad directories
"""

import os
import shutil
from pathlib import Path

vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")

print("🔧 FIXING ROOT DIRECTORY MESS...")
print("=" * 60)

# Directories that should NOT exist (I created these by mistake)
bad_directories = [
    "Audio",
    "Export", 
    "MASTER_GUIDES",
    "Player_Characters",
    "reports",
    "Resources",  # Should be 04_Resources
    "World",  # Should be 02_Worldbuilding
    "World_Simulation"
]

# Remove these bad directories
for dir_name in bad_directories:
    dir_path = vault_path / dir_name
    if dir_path.exists():
        try:
            shutil.rmtree(dir_path)
            print(f"✓ Removed bad directory: {dir_name}")
        except Exception as e:
            print(f"⚠️ Could not remove {dir_name}: {e}")

# Move any .md files from root to appropriate places
root_files = list(vault_path.glob("*.md"))
if root_files:
    print(f"\nFound {len(root_files)} .md files in root that shouldn't be there")
    
    # Move them to 08_Archive/root_cleanup
    archive_dir = vault_path / "08_Archive" / "root_cleanup"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    for file_path in root_files:
        try:
            dest = archive_dir / file_path.name
            shutil.move(str(file_path), str(dest))
            print(f"✓ Moved {file_path.name} to Archive/root_cleanup")
        except Exception as e:
            print(f"⚠️ Could not move {file_path.name}: {e}")

# Also remove any other non-hidden files in root that shouldn't be there
for item in vault_path.iterdir():
    if item.is_file() and not item.name.startswith('.'):
        # Only keep .gitignore
        if item.name != '.gitignore':
            try:
                dest = archive_dir / item.name
                shutil.move(str(item), str(dest))
                print(f"✓ Moved root file {item.name} to Archive")
            except:
                pass

print("\n✅ ROOT DIRECTORY CLEANED!")