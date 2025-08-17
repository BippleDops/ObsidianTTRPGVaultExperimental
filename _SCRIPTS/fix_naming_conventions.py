#!/usr/bin/env python3
"""
Fix naming conventions and clean up weird JSON files
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime

def clean_filename(filename):
    """Clean up weird filename patterns"""
    # Remove multiple underscores
    filename = re.sub(r'_{2,}', '_', filename)
    
    # Fix chapter/combat/rules patterns
    filename = re.sub(r'(\d+)_combat_dropping_to_0_hit_points', r'combat_rules_\1_dropping_to_0_hp', filename)
    filename = re.sub(r'(\d+)_chapter_(\d+)_playing_the_game', r'rules_chapter_\1_\2_playing', filename)
    
    # Remove weird character metadata suffixes
    filename = re.sub(r'_character(_v\d+)?_metadata\.json$', '_metadata.json', filename)
    
    # Fix assets paths in names
    filename = re.sub(r'assets_locations_location_city_', '', filename)
    filename = re.sub(r'assets_art_', '', filename)
    filename = re.sub(r'assets_portraits_portrait_npc_', '', filename)
    filename = re.sub(r'_svg$', '', filename)
    filename = re.sub(r'_png$', '', filename)
    
    # Convert to title case for readability
    parts = filename.replace('.json', '').replace('.md', '').split('_')
    # Keep certain words lowercase
    lowercase_words = ['of', 'the', 'and', 'or', 'in', 'to', 'a', 'an']
    
    cleaned_parts = []
    for i, part in enumerate(parts):
        if i == 0 or part.lower() not in lowercase_words:
            cleaned_parts.append(part.capitalize())
        else:
            cleaned_parts.append(part.lower())
    
    # Rejoin and add extension back
    if filename.endswith('.json'):
        return '_'.join(cleaned_parts) + '.json'
    elif filename.endswith('.md'):
        return '_'.join(cleaned_parts) + '.md'
    else:
        return '_'.join(cleaned_parts)

def should_be_index_or_list(filepath):
    """Determine if a file should have Index or List in its name"""
    filename = filepath.name.lower()
    
    # Check filename patterns
    if any(pattern in filename for pattern in ['all_', 'complete_', 'master_', 'catalog_', 'full_']):
        return 'List'
    
    if 'index' in filename:
        return 'Index'
    
    # Check content for markdown files
    if filepath.suffix == '.md':
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()[:1000].lower()  # Check first 1000 chars
                
            # Look for list patterns
            if content.count('\n- ') > 5 or content.count('\n* ') > 5 or content.count('\n1. ') > 3:
                return 'List'
            
            # Look for index patterns
            if '## index' in content or '# index' in content or 'table of contents' in content:
                return 'Index'
                
        except Exception:
            pass
    
    return None

def relocate_weird_json(filepath, vault_root):
    """Determine where weird JSON files should go"""
    filename = filepath.name.lower()
    
    # Rules/combat JSON metadata should go to archive
    if any(term in filename for term in ['chapter', 'combat', 'hit_point', 'saving_throw', 
                                          'stabilizing', 'death', 'rules']):
        return vault_root / '08_Archive' / 'removed_metadata_json'
    
    # Character metadata that's actually about NPCs
    if 'character_metadata' in filename and filepath.parent.name == '03_People':
        # These are probably misnamed - check if there's an actual NPC file
        base_name = filename.replace('_character_metadata.json', '').replace('_metadata.json', '')
        npc_file = filepath.parent / f"{base_name}.md"
        if not npc_file.exists():
            # No corresponding NPC file, archive it
            return vault_root / '08_Archive' / 'orphaned_metadata'
    
    # Token and portrait JSON files should stay with their images
    if filename.startswith(('token_', 'portrait_')):
        # Check if there's a corresponding image
        for ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp']:
            image_name = filename.replace('.json', ext)
            image_path = filepath.parent / image_name
            if image_path.exists():
                return None  # Keep it where it is
        # No image found, archive it
        return vault_root / '08_Archive' / 'orphaned_metadata'
    
    return None

def main():
    vault_root = Path.cwd()
    
    renames = []
    relocations = []
    archives = []
    
    # Process all files
    for filepath in vault_root.rglob('*'):
        # Skip archives, backups, git
        if any(skip in str(filepath) for skip in ['08_Archive', '09_Performance', '.git', '_SCRIPTS']):
            continue
            
        if not filepath.is_file():
            continue
        
        # Handle JSON files
        if filepath.suffix == '.json':
            # Check if it should be relocated
            new_location = relocate_weird_json(filepath, vault_root)
            if new_location:
                relocations.append((filepath, new_location / filepath.name))
                continue
            
            # Clean the filename
            old_name = filepath.name
            new_name = clean_filename(old_name)
            
            if old_name != new_name:
                new_path = filepath.parent / new_name
                renames.append((filepath, new_path))
        
        # Handle markdown files
        elif filepath.suffix == '.md':
            old_name = filepath.name
            
            # Check if it should have Index or List
            list_type = should_be_index_or_list(filepath)
            if list_type and list_type not in old_name:
                # Add List or Index to the name
                name_without_ext = old_name.replace('.md', '')
                new_name = f"{name_without_ext}_{list_type}.md"
                new_path = filepath.parent / new_name
                renames.append((filepath, new_path))
            
            # Also check for "All " prefix that should be "List"
            elif old_name.startswith('All '):
                new_name = old_name.replace('All ', '') .replace('.md', '_List.md')
                new_path = filepath.parent / new_name
                renames.append((filepath, new_path))
    
    # Special case: Remove weird JSON files from 03_People
    people_dir = vault_root / '03_People'
    if people_dir.exists():
        for json_file in people_dir.glob('*.json'):
            filename = json_file.name.lower()
            
            # These are definitely wrong and should be archived
            if any(term in filename for term in [
                'chapter', 'combat', 'hit_point', 'saving_throw',
                'stabilizing', 'death', 'playing_the_game'
            ]):
                archive_path = vault_root / '08_Archive' / 'removed_rules_json'
                target = archive_path / json_file.name
                # Check if not already in relocations
                if not any(src == json_file for src, _ in relocations):
                    archives.append((json_file, target))
    
    # Execute renames
    print(f"Found {len(renames)} files to rename")
    print(f"Found {len(relocations)} files to relocate")
    print(f"Found {len(archives)} files to archive")
    
    # Perform archives first
    if archives:
        archive_dir = vault_root / '08_Archive' / 'removed_rules_json'
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        for source, target in archives:
            if source.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                print(f"Archiving: {source.name}")
                shutil.move(str(source), str(target))
    
    # Perform relocations
    for source, target in relocations:
        if source.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            print(f"Relocating: {source.relative_to(vault_root)} -> {target.relative_to(vault_root)}")
            shutil.move(str(source), str(target))
    
    # Perform renames
    for source, target in renames:
        if source.exists() and not target.exists():
            print(f"Renaming: {source.name} -> {target.name}")
            source.rename(target)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"NAMING CONVENTION FIXES")
    print(f"{'='*60}")
    print(f"Files renamed: {len(renames)}")
    print(f"Files relocated: {len(relocations)}")
    print(f"Files archived: {len(archives)}")
    
    # Show some examples
    if renames:
        print("\nExample renames:")
        for old, new in renames[:5]:
            print(f"  {old.name} -> {new.name}")
    
    return len(renames) + len(relocations) + len(archives)

if __name__ == "__main__":
    main()