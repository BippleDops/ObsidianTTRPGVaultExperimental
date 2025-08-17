#!/usr/bin/env python3
"""
Remove weird/broken files from the vault based on patterns identified in CLAUDE.md
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def main():
    vault_root = Path.cwd()
    archive_dir = vault_root / "08_Archive" / "removed_weird_files"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    removed_count = 0
    files_to_remove = []
    
    # Pattern 1: Files starting with problematic characters (excluding archive and git)
    for pattern in ["#*", "$*", "%*", "<*"]:
        for file in vault_root.rglob(pattern):
            if "08_Archive" not in str(file) and ".git" not in str(file):
                files_to_remove.append(file)
    
    # Pattern 2: .png.json and similar files (keep actual .json files)
    for ext in [".png.json", ".svg.json", ".jpg.json"]:
        for file in vault_root.rglob(f"*{ext}"):
            if "08_Archive" not in str(file):
                files_to_remove.append(file)
    
    # Pattern 3: Files with (category) in name outside proper locations
    for file in vault_root.rglob("*(*).md"):
        if "08_Archive" not in str(file) and "09_Performance" not in str(file):
            # Check if it's a misplaced categorization file
            if any(cat in file.name for cat in ["(02_Worldbuilding)", "(03_People)", "(01_Adventures)"]):
                files_to_remove.append(file)
    
    # Remove duplicates from list
    files_to_remove = list(set(files_to_remove))
    
    print(f"Found {len(files_to_remove)} problematic files to remove")
    
    for file in files_to_remove:
        if file.exists():
            # Create archive path
            rel_path = file.relative_to(vault_root)
            archive_path = archive_dir / rel_path
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move to archive
            print(f"Archiving: {rel_path}")
            shutil.move(str(file), str(archive_path))
            removed_count += 1
    
    print(f"\nArchived {removed_count} files to {archive_dir}")
    
    # Also check for orphaned .json files that should be metadata
    json_count = 0
    for json_file in vault_root.rglob("*.json"):
        if ("08_Archive" not in str(json_file) and 
            ".git" not in str(json_file) and
            ".obsidian" not in str(json_file) and
            "_SCRIPTS" not in str(json_file) and
            "_METADATA" not in str(json_file)):
            
            # Check if it's a metadata file for an image
            base_name = json_file.stem
            parent = json_file.parent
            
            # Look for corresponding image
            image_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.webp']
            has_image = any((parent / f"{base_name}{ext}").exists() for ext in image_extensions)
            
            if has_image:
                json_count += 1
                print(f"Found metadata JSON (keeping): {json_file.relative_to(vault_root)}")
            else:
                # Check if it's a weird .png.json type file
                if any(ext in str(json_file) for ext in ['.png.json', '.svg.json', '.jpg.json']):
                    print(f"Found orphaned weird JSON: {json_file.relative_to(vault_root)}")
    
    print(f"\nFound {json_count} legitimate metadata JSON files (kept)")
    
    return removed_count

if __name__ == "__main__":
    main()