#!/usr/bin/env python3
"""
Tag Analysis Script for Vault Standardization
Analyzes current tag usage to design hierarchical tag system
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict, Counter
import json

def extract_frontmatter_tags(file_path):
    """Extract tags from YAML frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has frontmatter
        if not content.startswith('---'):
            return []
        
        # Find end of frontmatter
        end_match = re.search(r'\n---\n', content)
        if not end_match:
            return []
        
        frontmatter_content = content[3:end_match.start()]
        
        try:
            frontmatter = yaml.safe_load(frontmatter_content)
            if frontmatter and 'tags' in frontmatter:
                tags = frontmatter['tags']
                if isinstance(tags, list):
                    return [str(tag).strip() for tag in tags if tag]
                elif isinstance(tags, str):
                    return [tags.strip()]
        except yaml.YAMLError:
            pass
        
        return []
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def analyze_vault_tags(vault_path):
    """Analyze all tags in the vault"""
    all_tags = []
    tag_file_mapping = defaultdict(list)
    file_type_tags = defaultdict(list)
    
    # Walk through all markdown files
    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, vault_path)
                
                tags = extract_frontmatter_tags(file_path)
                if tags:
                    all_tags.extend(tags)
                    for tag in tags:
                        tag_file_mapping[tag].append(relative_path)
                    
                    # Categorize by directory structure
                    if relative_path.startswith('01_Adventures'):
                        file_type_tags['adventure'].extend(tags)
                    elif relative_path.startswith('02_Worldbuilding'):
                        if 'People' in relative_path:
                            file_type_tags['npc'].extend(tags)
                        elif 'Places' in relative_path:
                            file_type_tags['location'].extend(tags)
                        elif 'Groups' in relative_path:
                            file_type_tags['faction'].extend(tags)
                        elif 'Lore' in relative_path:
                            file_type_tags['lore'].extend(tags)
                        elif 'Items' in relative_path:
                            file_type_tags['item'].extend(tags)
                    elif relative_path.startswith('03_Mechanics'):
                        file_type_tags['mechanics'].extend(tags)
                    elif relative_path.startswith('05_Templates'):
                        file_type_tags['template'].extend(tags)
    
    return all_tags, tag_file_mapping, file_type_tags

def categorize_tags(all_tags):
    """Categorize tags into logical hierarchies"""
    categories = {
        'content': [],
        'world': [],
        'campaign': [],
        'status': [],
        'importance': [],
        'access': [],
        'mechanics': [],
        'uncategorized': []
    }
    
    # Content type patterns
    content_patterns = [
        'adventure', 'npc', 'location', 'faction', 'lore', 'item', 'mechanics', 'template',
        'person', 'place', 'group', 'government', 'criminal', 'organization'
    ]
    
    # World-related patterns
    world_patterns = [
        'aethermoor', 'aquabyssos', 'both', 'universal', 'crystal', 'depth', 'pressure',
        'undersea', 'underwater', 'sky', 'aerial', 'mountain', 'ocean', 'sea', 'surface'
    ]
    
    # Campaign-related patterns
    campaign_patterns = [
        'session', 'campaign', 'quest', 'mission', 'scenario', 'encounter', 'combat',
        'social', 'exploration', 'investigation', 'puzzle', 'mystery'
    ]
    
    # Status patterns
    status_patterns = [
        'complete', 'draft', 'in-progress', 'review', 'published', 'archived', 'deprecated',
        'stub', 'active', 'inactive', 'finished', 'todo', 'wip', 'needs-review'
    ]
    
    # Importance patterns
    importance_patterns = [
        'major', 'minor', 'critical', 'important', 'key', 'primary', 'secondary',
        'central', 'essential', 'vital', 'core', 'main', 'supporting'
    ]
    
    # Access patterns
    access_patterns = [
        'public', 'player-facing', 'dm-only', 'secret', 'hidden', 'restricted',
        'spoiler', 'confidential', 'open', 'classified'
    ]
    
    # Mechanics patterns
    mechanics_patterns = [
        'stats', 'rules', 'system', 'mechanics', 'dice', 'roll', 'check', 'save',
        'skill', 'ability', 'spell', 'magic', 'combat', 'equipment', 'weapon',
        'armor', 'tool', 'vehicle'
    ]
    
    for tag in set(all_tags):
        tag_lower = tag.lower()
        categorized = False
        
        # Check each category
        if any(pattern in tag_lower for pattern in content_patterns):
            categories['content'].append(tag)
            categorized = True
        elif any(pattern in tag_lower for pattern in world_patterns):
            categories['world'].append(tag)
            categorized = True
        elif any(pattern in tag_lower for pattern in campaign_patterns):
            categories['campaign'].append(tag)
            categorized = True
        elif any(pattern in tag_lower for pattern in status_patterns):
            categories['status'].append(tag)
            categorized = True
        elif any(pattern in tag_lower for pattern in importance_patterns):
            categories['importance'].append(tag)
            categorized = True
        elif any(pattern in tag_lower for pattern in access_patterns):
            categories['access'].append(tag)
            categorized = True
        elif any(pattern in tag_lower for pattern in mechanics_patterns):
            categories['mechanics'].append(tag)
            categorized = True
        
        if not categorized:
            categories['uncategorized'].append(tag)
    
    return categories

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    print("Analyzing current tag usage in vault...")
    all_tags, tag_file_mapping, file_type_tags = analyze_vault_tags(vault_path)
    
    print(f"\nTotal tags found: {len(all_tags)}")
    print(f"Unique tags: {len(set(all_tags))}")
    
    # Count frequency
    tag_counts = Counter(all_tags)
    print(f"\nMost common tags:")
    for tag, count in tag_counts.most_common(20):
        print(f"  {tag}: {count} files")
    
    # Categorize tags
    print(f"\nCategorizing tags...")
    categories = categorize_tags(all_tags)
    
    for category, tags in categories.items():
        if tags:
            print(f"\n{category.upper()} tags ({len(tags)}):")
            for tag in sorted(set(tags))[:10]:  # Show first 10
                print(f"  - {tag}")
            if len(set(tags)) > 10:
                print(f"  ... and {len(set(tags)) - 10} more")
    
    # Analyze by file type
    print(f"\nTags by content type:")
    for content_type, tags in file_type_tags.items():
        if tags:
            unique_tags = set(tags)
            print(f"  {content_type}: {len(unique_tags)} unique tags")
            common_tags = Counter(tags).most_common(5)
            for tag, count in common_tags:
                print(f"    {tag}: {count}")
    
    # Save detailed analysis
    analysis_file = os.path.join(vault_path, "scripts", "tag_analysis_results.json")
    analysis_data = {
        'total_tags': len(all_tags),
        'unique_tags': len(set(all_tags)),
        'tag_counts': dict(tag_counts.most_common(50)),
        'categories': {k: list(set(v)) for k, v in categories.items()},
        'file_type_tags': {k: dict(Counter(v).most_common(10)) for k, v in file_type_tags.items()},
        'sample_files_per_tag': {tag: files[:5] for tag, files in tag_file_mapping.items() if len(files) >= 2}
    }
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed analysis saved to: {analysis_file}")
    
    # Print recommendations
    print(f"\nHierarchical Tag Recommendations:")
    print(f"1. content/ - Content type classification")
    print(f"2. world/ - World-specific tags") 
    print(f"3. campaign/ - Campaign and session tags")
    print(f"4. status/ - Content status and completion")
    print(f"5. importance/ - Priority and significance")
    print(f"6. access/ - Visibility and access control")
    print(f"7. mechanics/ - Game mechanics and rules")

if __name__ == "__main__":
    main()