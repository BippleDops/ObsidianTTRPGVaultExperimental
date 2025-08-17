#!/usr/bin/env python3
"""
Final cleanup - consolidate 13_Performance to 09_Performance and organize scripts
"""

import os
import shutil
from pathlib import Path

vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")

print("🧹 FINAL CLEANUP...")
print("=" * 60)

# 1. Consolidate 13_Performance into 09_Performance
perf_13 = vault_path / "13_Performance"
perf_09 = vault_path / "09_Performance"

if perf_13.exists() and perf_09.exists():
    print("Consolidating 13_Performance → 09_Performance...")
    
    # Move all content from 13 to 09
    for item in perf_13.iterdir():
        dest = perf_09 / item.name
        if not dest.exists():
            try:
                shutil.move(str(item), str(dest))
                print(f"  ✓ Moved {item.name}")
            except Exception as e:
                # If file exists, rename it
                counter = 1
                new_dest = perf_09 / f"{item.stem}_{counter}{item.suffix}"
                while new_dest.exists():
                    counter += 1
                    new_dest = perf_09 / f"{item.stem}_{counter}{item.suffix}"
                try:
                    shutil.move(str(item), str(new_dest))
                    print(f"  ✓ Moved {item.name} as {new_dest.name}")
                except:
                    pass
    
    # Remove empty 13_Performance
    try:
        perf_13.rmdir()
        print("✓ Removed empty 13_Performance")
    except:
        print("⚠️ Could not remove 13_Performance - may have remaining files")

# 2. Create _SCRIPTS directory and move all Python scripts
scripts_dir = vault_path / "_SCRIPTS"
scripts_dir.mkdir(exist_ok=True)

current_scripts = vault_path / "scripts"
if current_scripts.exists():
    print("\nOrganizing scripts...")
    
    # Move all .py files from scripts/ to _SCRIPTS/
    py_files = list(current_scripts.glob("*.py"))
    print(f"  Found {len(py_files)} Python scripts")
    
    for script in py_files:
        dest = scripts_dir / script.name
        if not dest.exists():
            try:
                shutil.move(str(script), str(dest))
            except:
                pass
    
    # Remove empty scripts directory
    try:
        if not list(current_scripts.iterdir()):
            current_scripts.rmdir()
            print("  ✓ Moved all scripts to _SCRIPTS")
            print("  ✓ Removed empty scripts directory")
    except:
        pass

# 3. Check for any remaining issues
print("\n=== FINAL STRUCTURE CHECK ===")
all_dirs = sorted([d.name for d in vault_path.iterdir() if d.is_dir() and not d.name.startswith('.')])

proper_dirs = [
    "_INDEXES",
    "_METADATA", 
    "_SCRIPTS",
    "00_System",
    "01_Adventures",
    "02_Worldbuilding",
    "03_People",
    "04_Resources",
    "05_Rules",
    "06_Sessions",
    "07_Player_Resources",
    "08_Archive",
    "09_Performance",
    "12_Research"  # Optional - could be moved to 04_Resources/Research
]

print("Current directories:")
for d in all_dirs:
    if d in proper_dirs:
        print(f"  ✅ {d}")
    else:
        print(f"  ❌ {d} (should be removed or consolidated)")

print("\n✅ CLEANUP COMPLETE!")