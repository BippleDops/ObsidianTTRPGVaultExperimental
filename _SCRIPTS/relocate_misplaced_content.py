#!/usr/bin/env python3
"""
Relocate misplaced content to proper folders based on content analysis
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

def get_file_hash(filepath):
    """Get MD5 hash of file content for duplicate detection"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def analyze_content(filepath):
    """Analyze file content to determine proper category"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            filename = filepath.name.lower()
            
        # Rules/Mechanics indicators
        if any(term in filename or term in content[:500] for term in [
            'saving throw', 'hit point', 'combat', 'initiative', 'armor class',
            'ability score', 'proficiency', 'damage type', 'condition', 'exhaustion',
            'advantage', 'disadvantage', 'spell slot', 'concentration', 'rest',
            'death save', 'stabilizing', 'unconscious', 'dying'
        ]):
            return '05_Rules'
            
        # NPC/Character indicators
        if any(term in filename for term in ['npc', 'character_']) or \
           re.match(r'npc\d{4,}', filename):
            return '03_People'
            
        # Quest/Adventure indicators  
        if any(term in filename for term in ['quest', 'encounter', 'hook', 'chapter']) or \
           'quest -' in filename:
            return '01_Adventures'
            
        # Worldbuilding indicators
        if any(term in filename for term in [
            'loc00', 'location', 'faction', 'lore', 'history', 'culture',
            'organization', 'guild', 'government', 'economy', 'religion'
        ]):
            return '02_Worldbuilding'
            
        # Session indicators
        if 'session' in filename or re.match(r'session[ _]\d+', filename):
            return '06_Sessions'
            
        # Asset indicators
        if filepath.suffix in ['.png', '.jpg', '.jpeg', '.svg', '.webp'] or \
           any(term in str(filepath.parent) for term in ['assets', 'maps', 'handouts']):
            return '04_Resources'
            
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
    
    return None

def relocate_file(source, target_dir, rename_if_exists=True):
    """Move file to target directory, handling duplicates"""
    target_path = target_dir / source.name
    
    if target_path.exists():
        # Check if it's actually the same file
        if get_file_hash(source) == get_file_hash(target_path):
            # True duplicate - archive the source
            return 'duplicate', None
        elif rename_if_exists:
            # Different content, same name - rename
            counter = 1
            stem = source.stem
            suffix = source.suffix
            while target_path.exists():
                target_path = target_dir / f"{stem}_relocated_{counter}{suffix}"
                counter += 1
    
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target_path))
    return 'moved', target_path

def main():
    vault_root = Path.cwd()
    archive_dir = vault_root / "08_Archive" / "duplicates"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    relocations = []
    duplicates = []
    
    # Define proper locations for different content types
    locations = {
        '05_Rules': {
            'subfolders': {
                'combat': ['combat', 'fighting', 'battle', 'initiative'],
                'conditions': ['condition', 'exhaustion', 'status'],
                'magic': ['spell', 'magic', 'cantrip', 'ritual'],
                'abilities': ['ability', 'skill', 'proficiency', 'save'],
                'character': ['character creation', 'level', 'class', 'race']
            }
        },
        '03_People': {
            'subfolders': {
                'NPCs': ['npc'],
                'Factions': ['faction', 'organization', 'guild'],
                'Groups': ['group', 'party', 'team']
            }
        },
        '01_Adventures': {
            'subfolders': {
                'Campaigns': ['campaign', 'chapter'],
                'quests': ['quest'],
                'Encounters': ['encounter'],
                'Hooks': ['hook']
            }
        },
        '02_Worldbuilding': {
            'subfolders': {
                'Locations': ['location', 'loc00', 'place', 'city', 'town'],
                'Lore': ['lore', 'history', 'legend', 'myth'],
                'Items': ['item', 'artifact', 'treasure']
            }
        }
    }
    
    # Check each folder for misplaced content
    folders_to_check = ['01_Adventures', '02_Worldbuilding', '03_People', '04_Resources', '06_Sessions']
    
    for folder in folders_to_check:
        folder_path = vault_root / folder
        if not folder_path.exists():
            continue
            
        print(f"\nChecking {folder} for misplaced content...")
        
        for file in folder_path.rglob('*.md'):
            # Skip if in archive or performance folders
            if any(skip in str(file) for skip in ['08_Archive', '09_Performance', '_SCRIPTS']):
                continue
                
            # Analyze where this file should be
            proper_category = analyze_content(file)
            
            if proper_category and proper_category != folder:
                # File is misplaced
                print(f"  Misplaced: {file.relative_to(vault_root)}")
                print(f"    Should be in: {proper_category}")
                
                # Determine subfolder within category
                target_folder = vault_root / proper_category
                
                # Try to find appropriate subfolder
                if proper_category in locations:
                    file_lower = file.name.lower()
                    for subfolder, keywords in locations[proper_category]['subfolders'].items():
                        if any(kw in file_lower for kw in keywords):
                            target_folder = vault_root / proper_category / subfolder
                            break
                
                # Relocate the file
                status, new_path = relocate_file(file, target_folder)
                
                if status == 'moved':
                    relocations.append((file.relative_to(vault_root), new_path.relative_to(vault_root)))
                elif status == 'duplicate':
                    # Archive the duplicate
                    archive_path = archive_dir / file.relative_to(vault_root)
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), str(archive_path))
                    duplicates.append(file.relative_to(vault_root))
    
    # Special case: Combat/rules files in 03_People
    print("\nChecking for combat/rules files in 03_People...")
    people_path = vault_root / "03_People"
    
    for file in people_path.glob("*Combat*"):
        if file.is_file() and file.suffix == '.md':
            # Check if it's about a combat NPC or combat rules
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'saving throw' in content.lower() or 'hit point' in content.lower():
                # This is rules content
                target = vault_root / "05_Rules" / "combat"
                target.mkdir(parents=True, exist_ok=True)
                
                status, new_path = relocate_file(file, target)
                if status == 'moved':
                    relocations.append((file.relative_to(vault_root), new_path.relative_to(vault_root)))
                    print(f"  Moved combat rules: {file.name} -> 05_Rules/combat/")
    
    # Check for numbered chapter files outside 01_Adventures
    print("\nChecking for chapter files outside Adventures...")
    for file in vault_root.rglob("*Chapter [0-9]*"):
        if any(skip in str(file) for skip in ['08_Archive', '09_Performance', '01_Adventures']):
            continue
            
        if file.is_file() and file.suffix == '.md':
            target = vault_root / "01_Adventures" / "Campaigns"
            target.mkdir(parents=True, exist_ok=True)
            
            status, new_path = relocate_file(file, target)
            if status == 'moved':
                relocations.append((file.relative_to(vault_root), new_path.relative_to(vault_root)))
                print(f"  Moved chapter: {file.name} -> 01_Adventures/Campaigns/")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"RELOCATION SUMMARY")
    print(f"{'='*60}")
    print(f"Files relocated: {len(relocations)}")
    print(f"Duplicates archived: {len(duplicates)}")
    
    if relocations:
        print("\nRelocated files:")
        for old, new in relocations[:10]:  # Show first 10
            print(f"  {old} -> {new}")
        if len(relocations) > 10:
            print(f"  ... and {len(relocations) - 10} more")
    
    if duplicates:
        print("\nArchived duplicates:")
        for dup in duplicates[:10]:  # Show first 10
            print(f"  {dup}")
        if len(duplicates) > 10:
            print(f"  ... and {len(duplicates) - 10} more")
    
    # Create recovery script
    if relocations:
        recovery_script = vault_root / "_SCRIPTS" / "undo_relocations.py"
        with open(recovery_script, 'w') as f:
            f.write("#!/usr/bin/env python3\n")
            f.write("# Script to undo relocations if needed\n")
            f.write("import shutil\nfrom pathlib import Path\n\n")
            f.write("vault_root = Path.cwd()\n")
            f.write("relocations = [\n")
            for old, new in relocations:
                f.write(f"    ('{new}', '{old}'),\n")
            f.write("]\n\n")
            f.write("for current, original in relocations:\n")
            f.write("    current_path = vault_root / current\n")
            f.write("    original_path = vault_root / original\n")
            f.write("    if current_path.exists():\n")
            f.write("        original_path.parent.mkdir(parents=True, exist_ok=True)\n")
            f.write("        shutil.move(str(current_path), str(original_path))\n")
            f.write("        print(f'Restored: {original}')\n")
        
        print(f"\nRecovery script created: {recovery_script.relative_to(vault_root)}")
    
    return len(relocations), len(duplicates)

if __name__ == "__main__":
    main()