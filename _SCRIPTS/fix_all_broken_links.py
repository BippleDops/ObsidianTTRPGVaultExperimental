#!/usr/bin/env python3
"""
Find and fix all broken wikilinks - either create notes or remove references
"""

import re
from pathlib import Path
from datetime import datetime
import json
from collections import defaultdict
from typing import Set, Dict, List, Tuple

class BrokenLinkFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.all_notes = set()
        self.broken_links = defaultdict(list)
        self.fixed_links = []
        self.created_notes = []
        self.removed_links = []
        
    def scan_existing_notes(self):
        """Build index of all existing notes"""
        print("📚 Scanning existing notes...")
        
        for md_file in self.vault_path.rglob("*.md"):
            if "08_Archive" not in str(md_file):
                # Store both full path and just the name
                self.all_notes.add(md_file.stem.lower())
                relative_path = md_file.relative_to(self.vault_path)
                self.all_notes.add(str(relative_path).replace('.md', '').lower())
                
        print(f"   Found {len(self.all_notes)} existing notes")
        
    def find_broken_links(self):
        """Find all broken wikilinks in the vault"""
        print("\n🔍 Finding broken wikilinks...")
        
        checked = 0
        
        for md_file in self.vault_path.rglob("*.md"):
            if "08_Archive" in str(md_file):
                continue
                
            checked += 1
            
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Find all wikilinks [[...]]
                wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
                
                for link in wikilinks:
                    # Remove any pipe aliases
                    link_target = link.split('|')[0].strip()
                    
                    # Check if link exists
                    if link_target.lower() not in self.all_notes:
                        self.broken_links[link_target].append(str(md_file.relative_to(self.vault_path)))
                        
                if checked % 100 == 0:
                    print(f"   Checked {checked} files...")
                    
            except Exception as e:
                print(f"   Error checking {md_file}: {e}")
                
        print(f"   ✅ Found {len(self.broken_links)} unique broken links")
        
    def categorize_broken_links(self) -> Tuple[Dict, Dict]:
        """Categorize broken links into those to create vs remove"""
        to_create = {}
        to_remove = {}
        
        for link, files in self.broken_links.items():
            link_lower = link.lower()
            
            # Determine if we should create or remove
            should_create = False
            
            # Create if it's a commonly referenced concept
            if any(keyword in link_lower for keyword in [
                'npc', 'location', 'quest', 'item', 'spell',
                'faction', 'campaign', 'session', 'player',
                'character', 'place', 'group', 'organization',
                'city', 'town', 'dungeon', 'temple', 'guild'
            ]):
                should_create = True
                
            # Create if referenced multiple times
            if len(files) >= 2:
                should_create = True
                
            # Don't create if it's likely a typo or fragment
            if len(link) < 3 or link.count(' ') > 5:
                should_create = False
                
            # Don't create if it's a date or number
            if re.match(r'^[\d\-\/]+$', link):
                should_create = False
                
            if should_create:
                to_create[link] = files
            else:
                to_remove[link] = files
                
        return to_create, to_remove
        
    def create_missing_notes(self, to_create: Dict):
        """Create placeholder notes for valid broken links"""
        print("\n📝 Creating missing notes...")
        
        for link, referencing_files in to_create.items():
            # Determine appropriate location
            if 'npc' in link.lower() or 'character' in link.lower():
                folder = "02_Worldbuilding/People"
                note_type = "npc"
            elif any(word in link.lower() for word in ['location', 'place', 'city', 'town']):
                folder = "02_Worldbuilding/Places"
                note_type = "location"
            elif any(word in link.lower() for word in ['faction', 'group', 'guild', 'organization']):
                folder = "02_Worldbuilding/Groups"
                note_type = "faction"
            elif 'quest' in link.lower():
                folder = "01_Adventures"
                note_type = "quest"
            elif 'item' in link.lower():
                folder = "02_Worldbuilding/Items"
                note_type = "item"
            elif 'session' in link.lower():
                folder = "01_Adventures"
                note_type = "session"
            else:
                folder = "02_Worldbuilding/Lore"
                note_type = "lore"
                
            # Create the note
            note_path = self.vault_path / folder / f"{link}.md"
            
            # Skip if already exists
            if note_path.exists():
                continue
                
            # Ensure folder exists
            note_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create content
            content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: {note_type}
status: placeholder
tags:
- placeholder
- needs-content
- {note_type}
---

# {link}

> *This is a placeholder note created automatically because it was referenced in other notes.*

## Description

*[To be filled in]*

## Details

*[To be filled in]*

## Connections

### Referenced In
"""
            
            # Add references
            for ref_file in referencing_files[:10]:  # Max 10 references
                content += f"- [[{ref_file.replace('.md', '')}]]\n"
                
            content += """
## Notes

*This placeholder was created because this concept was referenced but didn't have its own note. Please add appropriate content.*

## Related
- *[Add related links]*

---
*Placeholder generated: """ + datetime.now().strftime('%Y-%m-%d') + "*"
            
            # Write the note
            note_path.write_text(content, encoding='utf-8')
            self.created_notes.append(str(note_path.relative_to(self.vault_path)))
            
        print(f"   ✅ Created {len(self.created_notes)} placeholder notes")
        
    def remove_invalid_links(self, to_remove: Dict):
        """Remove or fix invalid wikilinks"""
        print("\n🗑️ Removing invalid links...")
        
        files_modified = set()
        
        for link, referencing_files in to_remove.items():
            for ref_file in referencing_files:
                file_path = self.vault_path / ref_file
                
                if not file_path.exists():
                    continue
                    
                try:
                    content = file_path.read_text(encoding='utf-8')
                    original = content
                    
                    # Remove the broken link, keeping any display text
                    # [[broken|display]] becomes display
                    # [[broken]] becomes broken (as plain text)
                    pattern = r'\[\[' + re.escape(link) + r'(?:\|([^\]]+))?\]\]'
                    
                    def replace_link(match):
                        display_text = match.group(1)
                        return display_text if display_text else link
                        
                    content = re.sub(pattern, replace_link, content)
                    
                    if content != original:
                        file_path.write_text(content, encoding='utf-8')
                        files_modified.add(ref_file)
                        self.removed_links.append(f"{link} from {ref_file}")
                        
                except Exception as e:
                    print(f"   Error fixing {ref_file}: {e}")
                    
        print(f"   ✅ Removed {len(self.removed_links)} invalid links from {len(files_modified)} files")
        
    def generate_report(self):
        """Generate comprehensive report"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_broken_links": len(self.broken_links),
                "notes_created": len(self.created_notes),
                "links_removed": len(self.removed_links),
                "unique_broken_links": list(self.broken_links.keys())[:100]  # First 100
            },
            "created_notes": self.created_notes[:50],  # First 50
            "removed_links": self.removed_links[:50],  # First 50
            "top_broken_links": sorted(
                [(link, len(files)) for link, files in self.broken_links.items()],
                key=lambda x: x[1],
                reverse=True
            )[:20]  # Top 20 most referenced
        }
        
        report_path = self.vault_path / "13_Performance" / f"broken_links_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report_path
        
    def run_full_fix(self):
        """Execute complete broken link fix"""
        print("="*60)
        print("🔗 BROKEN LINK COMPREHENSIVE FIX")
        print("="*60)
        
        # Step 1: Scan vault
        self.scan_existing_notes()
        
        # Step 2: Find broken links
        self.find_broken_links()
        
        if not self.broken_links:
            print("\n✅ No broken links found!")
            return
            
        # Step 3: Categorize
        to_create, to_remove = self.categorize_broken_links()
        
        print(f"\n📊 Analysis:")
        print(f"   • Links to create notes for: {len(to_create)}")
        print(f"   • Links to remove: {len(to_remove)}")
        
        # Step 4: Create missing notes
        if to_create:
            self.create_missing_notes(to_create)
            
        # Step 5: Remove invalid links
        if to_remove:
            self.remove_invalid_links(to_remove)
            
        # Step 6: Generate report
        report_path = self.generate_report()
        
        print("\n" + "="*60)
        print("✅ BROKEN LINK FIX COMPLETE!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Total broken links found: {len(self.broken_links)}")
        print(f"   • Placeholder notes created: {len(self.created_notes)}")
        print(f"   • Invalid links removed: {len(self.removed_links)}")
        print(f"\n📄 Full report: {report_path.name}")

def main():
    fixer = BrokenLinkFixer()
    fixer.run_full_fix()

if __name__ == "__main__":
    main()