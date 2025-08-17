#!/usr/bin/env python3
"""
Fix broken links according to user specifications
"""

import re
import os
from pathlib import Path
from collections import defaultdict

def fix_links_in_content(content, filepath):
    """Fix broken links in content according to rules"""
    changes_made = False
    original_content = content
    
    # 1. Remove meta placeholders
    meta_placeholders = [
        r'\[\[Related_Content\]\]',
        r'\[\[SYSTEM_STATUS\]\]',
        r'\[\[NPC Motivations\]\]',
        r'\[\[Diplomacy Rules\]\]',
        r'\[\[Political Factions\]\]'
    ]
    
    for placeholder in meta_placeholders:
        if re.search(placeholder, content):
            content = re.sub(placeholder, '', content)
            changes_made = True
    
    # 2. Remove step references
    step_pattern = r'\[\[step_\d+\]\]'
    if re.search(step_pattern, content):
        content = re.sub(step_pattern, '', content)
        changes_made = True
    
    # 3. Fix location links - simplify paths
    location_fixes = [
        (r'\[\[02_Worldbuilding/Places/Aquabyssos\]\]', '[[Aquabyssos]]'),
        (r'\[\[02_Worldbuilding/Places/Aethermoor\]\]', '[[Aethermoor]]'),
        (r'\[\[02_Worldbuilding/Places/Crystalhaven\]\]', '[[Crystalhaven]]'),
        (r'\[\[02_Worldbuilding/Places/Port Meridian\]\]', '[[Port Meridian]]'),
        (r'\[\[02_Worldbuilding/Places/Abyssos Prime\]\]', '[[Abyssos Prime]]'),
        (r'\[\[02_Worldbuilding/Places/The Sunken Library of Thalassius\]\]', '[[The Sunken Library of Thalassius]]'),
        (r'\[\[02_Worldbuilding/Places/Parliament of Echoes\]\]', '[[Parliament of Echoes]]'),
        (r'\[\[02_Worldbuilding/Places/The Hadal Depths\]\]', '[[The Hadal Depths]]'),
        (r'\[\[02_Worldbuilding/Places/Port Meridian - Merchant Quarter\]\]', '[[Port Meridian - Merchant Quarter]]'),
    ]
    
    for old_link, new_link in location_fixes:
        if re.search(re.escape(old_link), content):
            content = content.replace(old_link, new_link)
            changes_made = True
    
    # 4. Fix people/character links
    people_fixes = [
        (r'\[\[02_Worldbuilding/People/Vex Shadowthorn\]\]', '[[Vex Shadowthorn]]'),
        (r'\[\[02_Worldbuilding/People/Crystal Wardens\]\]', '[[Crystal Wardens]]'),
        (r'\[\[02_Worldbuilding/People/Queen Seraphina Lumengarde\]\]', '[[Queen Seraphina Lumengarde]]'),
        (r'\[\[02_Worldbuilding/People/The Crimson Sage\]\]', '[[The Crimson Sage]]'),
    ]
    
    for old_link, new_link in people_fixes:
        if re.search(re.escape(old_link), content):
            content = content.replace(old_link, new_link)
            changes_made = True
    
    # 5. Fix lore links
    lore_fixes = [
        (r'\[\[02_Worldbuilding/Lore/The Deep Mother\]\]', '[[The Deep Mother]]'),
        (r'\[\[02_Worldbuilding/Lore/Deep Mother\]\]', '[[Deep Mother]]'),
        (r'\[\[02_Worldbuilding/Lore/The Seven Shards\]\]', '[[The Seven Shards]]'),
        (r'\[\[02_Worldbuilding/Lore/The Convergence Point\]\]', '[[The Convergence Point]]'),
        (r'\[\[02_Worldbuilding/Lore/Crystal Forest\]\]', '[[Crystal Forest]]'),
        (r'\[\[02_Worldbuilding/Lore/The Crimson Hand\]\]', '[[The Crimson Hand]]'),
    ]
    
    for old_link, new_link in lore_fixes:
        if re.search(re.escape(old_link), content):
            content = content.replace(old_link, new_link)
            changes_made = True
    
    # 6. Fix quest links
    quest_fixes = [
        (r'\[\[02_Worldbuilding/Quests/Aquabyssos\]\]', '[[Aquabyssos]]'),
        (r'\[\[02_Worldbuilding/Quests/The Whispering Expanse\]\]', '[[The Whispering Expanse]]'),
    ]
    
    for old_link, new_link in quest_fixes:
        if re.search(re.escape(old_link), content):
            content = content.replace(old_link, new_link)
            changes_made = True
    
    # 7. Fix group links
    group_fixes = [
        (r'\[\[02_Worldbuilding/Groups/Silverscale Consortium\]\]', '[[Silverscale Consortium]]'),
    ]
    
    for old_link, new_link in group_fixes:
        if re.search(re.escape(old_link), content):
            content = content.replace(old_link, new_link)
            changes_made = True
    
    # 8. Fix system links to proper rules pages
    system_fixes = [
        (r'\[\[classes\]\]', '[[05_Rules/Character Classes]]'),
        (r'\[\[conditions\]\]', '[[05_Rules/Conditions]]'),
        (r'\[\[spells\]\]', '[[05_Rules/Spells]]'),
    ]
    
    for old_link, new_link in system_fixes:
        if re.search(old_link, content, re.IGNORECASE):
            content = re.sub(old_link, new_link, content, flags=re.IGNORECASE)
            changes_made = True
    
    # 9. Clean up multiple blank lines created by removals
    if changes_made:
        # Replace 3+ newlines with 2
        content = re.sub(r'\n{3,}', '\n\n', content)
        # Clean up spaces before/after removed links
        content = re.sub(r'  +', ' ', content)
        content = re.sub(r' \n', '\n', content)
    
    return content, changes_made

def main():
    vault_root = Path.cwd()
    
    # Statistics
    files_modified = 0
    links_fixed = defaultdict(int)
    
    # 1. Delete template files
    template_files = [
        vault_root / "01_Adventures/Campaigns/{{campaign}}.md",
        vault_root / "02_Worldbuilding/Lore/{{campaign}}.md", 
        vault_root / "02_Worldbuilding/Lore/Maintenance_Schedule_{{year}}.md"
    ]
    
    print("Deleting template files...")
    for template_file in template_files:
        if template_file.exists():
            print(f"  Deleting: {template_file.name}")
            template_file.unlink()
    
    # 2. Fix broken links in all markdown files
    print("\nFixing broken links in markdown files...")
    
    for md_file in vault_root.rglob("*.md"):
        # Skip archives and scripts
        if any(skip in str(md_file) for skip in ['08_Archive', '09_Performance', '.git', '_SCRIPTS']):
            continue
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix links
            new_content, changed = fix_links_in_content(content, md_file)
            
            if changed:
                # Write back
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_modified += 1
                
                # Count what was fixed
                if 'Related_Content' in content:
                    links_fixed['meta_placeholders'] += content.count('[[Related_Content]]')
                if 'SYSTEM_STATUS' in content:
                    links_fixed['meta_placeholders'] += content.count('[[SYSTEM_STATUS]]')
                if 'step_' in content:
                    links_fixed['step_references'] += len(re.findall(r'\[\[step_\d+\]\]', content))
                if '02_Worldbuilding/Places/' in content:
                    links_fixed['location_paths'] += content.count('02_Worldbuilding/Places/')
                if '[[classes]]' in content.lower():
                    links_fixed['system_links'] += content.lower().count('[[classes]]')
                if '[[conditions]]' in content.lower():
                    links_fixed['system_links'] += content.lower().count('[[conditions]]')
                if '[[spells]]' in content.lower():
                    links_fixed['system_links'] += content.lower().count('[[spells]]')
                
                if files_modified % 100 == 0:
                    print(f"  Modified {files_modified} files...")
                    
        except Exception as e:
            print(f"  Error processing {md_file}: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("FIX BROKEN LINKS SUMMARY")
    print("="*60)
    print(f"Template files deleted: {len([f for f in template_files if not f.exists()])}")
    print(f"Files modified: {files_modified}")
    print("\nLinks fixed by category:")
    for category, count in links_fixed.items():
        print(f"  {category}: {count}")
    print("="*60)
    
    return files_modified

if __name__ == "__main__":
    main()