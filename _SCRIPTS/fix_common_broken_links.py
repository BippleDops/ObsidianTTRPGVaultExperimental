#!/usr/bin/env python3
"""
Fix the most common broken links by creating missing files or updating references
"""

import os
import json
import re
from pathlib import Path
from collections import Counter

def create_stub_file(file_path, title, file_type="Generic"):
    """Create a stub file with basic metadata"""
    content = f"""---
tags:
- aquabyssos
- {file_type.lower()}
type: {file_type}
world: Aquabyssos
status: stub
created: 2025-08-12
updated: 2025-08-12
---

# {title}

*This is a stub file created to resolve broken links. Content needed.*

## Overview

[Content to be added]

## Related Concepts

- [[02_Worldbuilding/Lore/Master Index]]

## References

[Add references here]
"""
    
    os.makedirs(file_path.parent, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_broken_links():
    vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")
    
    # Load broken links analysis
    with open(vault_path / "broken_links_analysis.json", 'r') as f:
        data = json.load(f)
    
    # Count most common broken links
    all_broken_links = []
    for file_path, broken_links in data['broken_links'].items():
        all_broken_links.extend(broken_links)
    
    # Filter out empty links
    all_broken_links = [link for link in all_broken_links if link.strip()]
    
    link_counts = Counter(all_broken_links)
    
    print("Most common broken links:")
    for link, count in link_counts.most_common(20):
        print(f"  {link}: {count} occurrences")
    
    # Fix specific common issues
    fixes_made = 0
    
    # 1. Create Shadow Corruption file
    shadow_corruption_path = vault_path / "02_Worldbuilding/Lore/Shadow Corruption.md"
    if not shadow_corruption_path.exists():
        create_stub_file(shadow_corruption_path, "Shadow Corruption", "Lore")
        print(f"Created: {shadow_corruption_path}")
        fixes_made += 1
    
    # 2. Create common missing files based on frequency
    common_missing_files = [
        ("02_Worldbuilding/Places/Aquabyssos", "02_Worldbuilding/Places/Aquabyssos.md", "Place"),
        ("Master Artificer Chaos-Crystal", "02_Worldbuilding/People/Master Artificer Chaos-Crystal.md", "Person"),
        ("Ethics Coordinator Elena Compassion", "02_Worldbuilding/People/Ethics Coordinator Elena Compassion.md", "Person"),
        ("Investigator Supreme Lucian Brightwater", "02_Worldbuilding/People/Investigator Supreme Lucian Brightwater.md", "Person"),
        ("Guild Master Shellforge", "02_Worldbuilding/People/Guild Master Shellforge.md", "Person"),
        ("Void Touched Cult", "02_Worldbuilding/Groups/Void Touched Cult.md", "Group"),
        ("The Observatory Between", "02_Worldbuilding/Places/The Observatory Between.md", "Place"),
    ]
    
    for link_name, file_path_str, file_type in common_missing_files:
        file_path = vault_path / file_path_str
        if not file_path.exists() and link_name in link_counts:
            create_stub_file(file_path, link_name, file_type)
            print(f"Created: {file_path}")
            fixes_made += 1
    
    # 3. Fix empty links in specific files
    files_with_empty_links = [
        "Campaign_Quick_Reference_Sheets.md",
        "Master_Lore_Index.md",
        "METADATA_STANDARDS.md"
    ]
    
    for filename in files_with_empty_links:
        file_path = vault_path / filename
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove empty WikiLinks
                original_content = content
                content = re.sub(r'\[\[\s*\]\]', '', content)
                content = re.sub(r'\[\[\s*\|\s*\]\]', '', content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed empty links in: {filename}")
                    fixes_made += 1
                    
            except Exception as e:
                print(f"Error fixing {filename}: {e}")
    
    print(f"\nTotal fixes made: {fixes_made}")
    return fixes_made

if __name__ == "__main__":
    fix_broken_links()