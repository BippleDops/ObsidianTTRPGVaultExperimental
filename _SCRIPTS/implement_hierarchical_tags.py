#!/usr/bin/env python3
"""
Hierarchical Tag Implementation Script for Vault Standardization
Converts flat tags to hierarchical nested tag system
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict
import shutil
from datetime import datetime
import json

def backup_file(file_path, backup_dir):
    """Create backup of file before modification"""
    relative_path = os.path.relpath(file_path, os.path.dirname(backup_dir))
    backup_path = os.path.join(backup_dir, relative_path)
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copy2(file_path, backup_path)

def load_frontmatter(file_path):
    """Load frontmatter from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            return None, content
        
        end_match = re.search(r'\n---\n', content)
        if not end_match:
            return None, content
        
        frontmatter_content = content[3:end_match.start()]
        body_content = content[end_match.end():]
        
        try:
            frontmatter = yaml.safe_load(frontmatter_content)
            return frontmatter, body_content
        except yaml.YAMLError:
            return None, content
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None, None

def save_frontmatter(file_path, frontmatter, body_content):
    """Save updated frontmatter and body to file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True, sort_keys=True)
            f.write('---\n')
            f.write(body_content)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def create_hierarchical_tag_mappings():
    """Create mappings from flat tags to hierarchical tags"""
    mappings = {
        # Content type mappings
        'content/adventure': ['adventure', 'adventure-hooks', 'adventure-introduction', 'adventure-module', 'adventure-session', 'quest', 'scenario', 'mission'],
        'content/npc': ['npc', 'person', 'character', 'people'],
        'content/location': ['location', 'place', 'site', 'settlement', 'city', 'town', 'village'],
        'content/faction': ['faction', 'group', 'organization', 'guild', 'government', 'criminal'],
        'content/lore': ['lore', 'history', 'legend', 'mythology', 'ancient-lore', 'background'],
        'content/item': ['item', 'equipment', 'weapon', 'armor', 'tool', 'artifact', 'treasure'],
        'content/mechanics': ['mechanics', 'mechanic', 'rules', 'system', 'stats'],
        'content/template': ['template', 'framework', 'structure'],
        
        # World-specific mappings
        'world/aethermoor': ['aethermoor', 'crystal', 'sky', 'aerial', 'wind', 'cloud'],
        'world/aquabyssos': ['aquabyssos', 'depth', 'pressure', 'undersea', 'underwater', 'ocean', 'sea', 'marine'],
        'world/both': ['both', 'universal', 'cross-world', 'inter-dimensional'],
        'world/surface': ['surface', 'land', 'terrestrial', 'continental'],
        
        # Campaign-related mappings
        'campaign/session': ['session', 'session-ready', 'gameplay', 'encounter'],
        'campaign/arc': ['campaign', 'arc', 'storyline', 'plot'],
        'campaign/hook': ['hook', 'lead', 'opportunity', 'rumor'],
        'campaign/objective': ['objective', 'goal', 'mission', 'target'],
        'campaign/consequence': ['consequence', 'result', 'aftermath', 'impact'],
        
        # Status mappings
        'status/complete': ['complete', 'completed', 'finished', 'done'],
        'status/draft': ['draft', 'wip', 'work-in-progress', 'todo'],
        'status/in-progress': ['in-progress', 'active', 'ongoing', 'current'],
        'status/review': ['review', 'needs-review', 'check', 'verify'],
        'status/archived': ['archived', 'old', 'deprecated', 'legacy'],
        'status/stub': ['stub', 'placeholder', 'minimal', 'outline'],
        
        # Importance mappings
        'importance/critical': ['critical', 'vital', 'essential', 'crucial'],
        'importance/major': ['major', 'important', 'significant', 'key'],
        'importance/minor': ['minor', 'secondary', 'supporting', 'peripheral'],
        'importance/core': ['core', 'central', 'primary', 'main'],
        
        # Access control mappings
        'access/public': ['public', 'open', 'player-facing', 'visible'],
        'access/restricted': ['restricted', 'limited', 'controlled', 'private'],
        'access/secret': ['secret', 'hidden', 'classified', 'confidential'],
        'access/dm-only': ['dm-only', 'gm-only', 'spoiler', 'behind-scenes'],
        
        # Mechanics mappings
        'mechanics/combat': ['combat', 'battle', 'fight', 'conflict'],
        'mechanics/social': ['social', 'diplomacy', 'negotiation', 'interaction'],
        'mechanics/exploration': ['exploration', 'discovery', 'investigation', 'search'],
        'mechanics/magic': ['magic', 'spell', 'enchantment', 'mystical'],
        'mechanics/skill': ['skill', 'ability', 'check', 'roll'],
    }
    
    # Create reverse mapping for quick lookup
    flat_to_hierarchical = {}
    for hierarchical_tag, flat_tags in mappings.items():
        for flat_tag in flat_tags:
            if flat_tag not in flat_to_hierarchical:
                flat_to_hierarchical[flat_tag] = []
            flat_to_hierarchical[flat_tag].append(hierarchical_tag)
    
    return flat_to_hierarchical

def convert_tags_to_hierarchical(tags, mappings):
    """Convert flat tags to hierarchical tags"""
    if not tags:
        return []
    
    hierarchical_tags = set()
    unmapped_tags = []
    
    for tag in tags:
        tag_str = str(tag).strip().lower()
        if tag_str in mappings:
            # Add all hierarchical mappings for this tag
            hierarchical_tags.update(mappings[tag_str])
        else:
            # Check for partial matches
            mapped = False
            for flat_pattern, hierarchical_list in mappings.items():
                if flat_pattern in tag_str or tag_str in flat_pattern:
                    hierarchical_tags.update(hierarchical_list)
                    mapped = True
                    break
            
            if not mapped:
                # Keep unmapped tags but try to categorize them
                if any(keyword in tag_str for keyword in ['adventure', 'quest', 'scenario']):
                    hierarchical_tags.add('content/adventure')
                elif any(keyword in tag_str for keyword in ['npc', 'person', 'character']):
                    hierarchical_tags.add('content/npc')
                elif any(keyword in tag_str for keyword in ['location', 'place', 'city']):
                    hierarchical_tags.add('content/location')
                elif any(keyword in tag_str for keyword in ['faction', 'group', 'organization']):
                    hierarchical_tags.add('content/faction')
                elif any(keyword in tag_str for keyword in ['lore', 'history', 'legend']):
                    hierarchical_tags.add('content/lore')
                elif any(keyword in tag_str for keyword in ['item', 'equipment', 'weapon']):
                    hierarchical_tags.add('content/item')
                elif any(keyword in tag_str for keyword in ['mechanic', 'rule', 'system']):
                    hierarchical_tags.add('content/mechanics')
                elif any(keyword in tag_str for keyword in ['aethermoor', 'crystal', 'sky']):
                    hierarchical_tags.add('world/aethermoor')
                elif any(keyword in tag_str for keyword in ['aquabyssos', 'depth', 'underwater']):
                    hierarchical_tags.add('world/aquabyssos')
                elif tag_str in ['both', 'universal']:
                    hierarchical_tags.add('world/both')
                else:
                    # Add as uncategorized with original form preserved
                    unmapped_tags.append(str(tag))
    
    # Combine hierarchical and unmapped tags
    result_tags = list(hierarchical_tags) + unmapped_tags
    return sorted(result_tags)

def process_file(file_path, mappings, backup_dir, dry_run=False):
    """Process a single file to convert its tags"""
    try:
        frontmatter, body_content = load_frontmatter(file_path)
        
        if not frontmatter or 'tags' not in frontmatter:
            return False, "No tags found"
        
        original_tags = frontmatter['tags']
        if not original_tags:
            return False, "Empty tags"
        
        # Convert to hierarchical tags
        new_tags = convert_tags_to_hierarchical(original_tags, mappings)
        
        if new_tags == original_tags:
            return False, "No changes needed"
        
        if dry_run:
            return True, f"Would convert {len(original_tags)} tags to {len(new_tags)} hierarchical tags"
        
        # Backup original file
        backup_file(file_path, backup_dir)
        
        # Update frontmatter
        frontmatter['tags'] = new_tags
        frontmatter['updated'] = datetime.now().isoformat()
        
        # Save updated file
        success = save_frontmatter(file_path, frontmatter, body_content)
        
        if success:
            return True, f"Converted {len(original_tags)} tags to {len(new_tags)} hierarchical tags"
        else:
            return False, "Failed to save file"
            
    except Exception as e:
        return False, f"Error: {e}"

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    backup_dir = os.path.join(vault_path, "backups", f"hierarchical_tags_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    import sys
    dry_run = '--dry-run' in sys.argv
    
    print("Hierarchical Tag Implementation Script")
    print("====================================")
    print(f"Vault path: {vault_path}")
    print(f"Dry run: {dry_run}")
    print()
    
    # Create backup directory
    if not dry_run:
        os.makedirs(backup_dir, exist_ok=True)
        print(f"Backup directory: {backup_dir}")
    
    # Load tag mappings
    mappings = create_hierarchical_tag_mappings()
    print(f"Loaded {len(mappings)} tag mappings")
    
    # Process files
    total_files = 0
    updated_files = 0
    errors = []
    
    for root, dirs, files in os.walk(vault_path):
        # Skip backup and script directories
        if 'backup' in root.lower() or 'script' in root.lower():
            continue
            
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, vault_path)
                
                total_files += 1
                success, message = process_file(file_path, mappings, backup_dir, dry_run)
                
                if success:
                    updated_files += 1
                    if total_files % 100 == 0:
                        print(f"Processed {total_files} files, updated {updated_files}")
                elif "No tags found" not in message and "Empty tags" not in message and "No changes needed" not in message:
                    errors.append(f"{relative_path}: {message}")
    
    print(f"\nProcessing complete!")
    print(f"Total files processed: {total_files}")
    print(f"Files updated: {updated_files}")
    print(f"Files skipped: {total_files - updated_files}")
    
    if errors:
        print(f"\nErrors encountered ({len(errors)}):")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    # Save conversion report
    report_data = {
        'timestamp': datetime.now().isoformat(),
        'dry_run': dry_run,
        'total_files': total_files,
        'updated_files': updated_files,
        'errors': errors,
        'mappings_used': len(mappings)
    }
    
    report_file = os.path.join(vault_path, "scripts", "hierarchical_tags_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nConversion report saved to: {report_file}")
    
    if dry_run:
        print("\nThis was a dry run. No files were actually modified.")
        print("Remove --dry-run flag to perform the actual conversion.")
    else:
        print(f"\nBackup created at: {backup_dir}")
        print("Hierarchical tag conversion complete!")

if __name__ == "__main__":
    main()