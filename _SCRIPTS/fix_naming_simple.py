#!/usr/bin/env python3
"""
Simple version: Clean up weird JSON files and fix basic naming issues
"""

import os
import shutil
from pathlib import Path

def main():
    vault_root = Path.cwd()
    archive_dir = vault_root / "08_Archive" / "removed_weird_json"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    archived = 0
    renamed = 0
    
    # 1. Archive weird JSON files from 03_People
    people_dir = vault_root / "03_People"
    if people_dir.exists():
        for json_file in people_dir.glob("*.json"):
            filename = json_file.name.lower()
            
            # These definitely don't belong in People folder
            if any(term in filename for term in [
                'chapter', 'combat', 'hit_point', 'saving_throw',
                'stabilizing', 'death', 'playing_the_game', 'rules'
            ]):
                target = archive_dir / json_file.name
                print(f"Archiving rules JSON: {json_file.name}")
                shutil.move(str(json_file), str(target))
                archived += 1
    
    # 2. Find and rename files that should have "List" or "Index" suffix
    for md_file in vault_root.rglob("*.md"):
        # Skip archives and backups
        if any(skip in str(md_file) for skip in ['08_Archive', '09_Performance', '.git', '_SCRIPTS']):
            continue
            
        filename = md_file.name
        
        # Files starting with "All " should be lists
        if filename.startswith("All ") and "_List" not in filename:
            new_name = filename.replace("All ", "").replace(".md", "_List.md")
            new_path = md_file.parent / new_name
            if not new_path.exists():
                print(f"Renaming to list: {filename} -> {new_name}")
                md_file.rename(new_path)
                renamed += 1
        
        # Files with catalog/complete/master should have List
        elif any(term in filename.lower() for term in ['catalog', 'complete_', 'master_list']):
            if '_List' not in filename and '_Index' not in filename:
                new_name = filename.replace('.md', '_List.md')
                new_path = md_file.parent / new_name
                if not new_path.exists():
                    print(f"Adding List suffix: {filename} -> {new_name}")
                    md_file.rename(new_path)
                    renamed += 1
    
    # 3. Archive orphaned metadata JSON files (no corresponding image)
    for json_file in vault_root.rglob("*.json"):
        # Skip archives and system files
        if any(skip in str(json_file) for skip in ['08_Archive', '09_Performance', '.git', '_SCRIPTS', '.obsidian', '_METADATA']):
            continue
            
        filename = json_file.name
        
        # Check token and portrait JSON files
        if filename.startswith(('token_', 'portrait_')):
            # Look for corresponding image
            has_image = False
            base_name = filename.replace('.json', '')
            
            for ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp']:
                image_path = json_file.parent / f"{base_name}{ext}"
                if image_path.exists():
                    has_image = True
                    break
            
            if not has_image:
                # No image, archive the JSON
                target = archive_dir / json_file.name
                print(f"Archiving orphaned JSON: {json_file.relative_to(vault_root)}")
                shutil.move(str(json_file), str(target))
                archived += 1
    
    print(f"\n{'='*60}")
    print(f"CLEANUP SUMMARY")
    print(f"{'='*60}")
    print(f"Files archived: {archived}")
    print(f"Files renamed: {renamed}")
    print(f"Total changes: {archived + renamed}")
    
    return archived + renamed

if __name__ == "__main__":
    main()