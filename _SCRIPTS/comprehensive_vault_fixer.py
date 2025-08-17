#!/usr/bin/env python3
"""
Comprehensive vault fixer - handles backups, organization, and link repair
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class ComprehensiveVaultFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.backups_moved = 0
        self.links_fixed = 0
        self.files_organized = 0
        self.broken_links = defaultdict(list)
        
    def run(self):
        """Main execution"""
        print("=" * 80)
        print("🔧 COMPREHENSIVE VAULT FIXER")
        print("=" * 80)
        
        # Step 1: Move backup directories to Archive
        print("\n📦 Step 1: Moving backup directories to Archive...")
        self.move_backups_to_archive()
        
        # Step 2: Scan for broken links
        print("\n🔍 Step 2: Scanning for broken links...")
        self.scan_broken_links()
        
        # Step 3: Fix broken links
        print("\n🔗 Step 3: Fixing broken links...")
        self.fix_broken_links()
        
        # Step 4: Final organization check
        print("\n📁 Step 4: Final organization check...")
        self.final_organization()
        
        # Report
        self.generate_report()
        
    def move_backups_to_archive(self):
        """Move all backup directories to Archive"""
        archive_dir = self.vault_path / "08_Archive" / "Vault_Backups"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all backup directories
        backup_patterns = ["vault_backup_*", "backup_*", "*_backup", "*_bak"]
        
        for pattern in backup_patterns:
            for backup_dir in self.vault_path.rglob(pattern):
                if backup_dir.is_dir():
                    # Skip if already in Archive
                    if "08_Archive" in str(backup_dir):
                        continue
                        
                    dest = archive_dir / backup_dir.name
                    
                    # Handle duplicates
                    if dest.exists():
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest = archive_dir / f"{backup_dir.name}_{timestamp}"
                        
                    try:
                        print(f"   Moving {backup_dir.name} to Archive...")
                        shutil.move(str(backup_dir), str(dest))
                        self.backups_moved += 1
                    except Exception as e:
                        print(f"   ⚠️ Error moving {backup_dir}: {e}")
                        
    def scan_broken_links(self):
        """Scan all files for broken links"""
        all_note_names = set()
        all_note_paths = {}
        
        # First, collect all existing note names and paths
        for md_file in self.vault_path.rglob("*.md"):
            # Skip non-content files
            if any(skip in str(md_file) for skip in ['scripts/', '.git/', 'Archive/']):
                continue
                
            note_name = md_file.stem
            all_note_names.add(note_name)
            all_note_paths[note_name] = md_file
            
        # Now scan for links and check if they exist
        for md_file in self.vault_path.rglob("*.md"):
            # Skip non-content files
            if any(skip in str(md_file) for skip in ['scripts/', '.git/', 'Archive/']):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Find all [[wiki-style]] links
                wiki_links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                
                for link in wiki_links:
                    # Clean the link
                    link_name = link.strip()
                    
                    # Remove any path components
                    if '/' in link_name:
                        link_name = link_name.split('/')[-1]
                        
                    # Remove .md extension if present
                    link_name = link_name.replace('.md', '')
                    
                    # Check if this note exists
                    if link_name not in all_note_names:
                        self.broken_links[str(md_file)].append(link_name)
                        
            except Exception as e:
                print(f"   ⚠️ Error scanning {md_file}: {e}")
                
        print(f"   Found {sum(len(v) for v in self.broken_links.values())} broken links in {len(self.broken_links)} files")
        
    def fix_broken_links(self):
        """Attempt to fix broken links"""
        
        # Create a mapping of potential fixes
        all_notes = {}
        for md_file in self.vault_path.rglob("*.md"):
            if any(skip in str(md_file) for skip in ['scripts/', '.git/', 'Archive/']):
                continue
            note_name = md_file.stem
            all_notes[note_name.lower()] = note_name
            
        # Fix broken links
        for file_path, broken_links in self.broken_links.items():
            if not broken_links:
                continue
                
            file_obj = Path(file_path)
            try:
                content = file_obj.read_text(encoding='utf-8')
                original_content = content
                
                for broken_link in broken_links:
                    # Try to find a close match
                    broken_lower = broken_link.lower()
                    
                    # Direct match (case-insensitive)
                    if broken_lower in all_notes:
                        correct_name = all_notes[broken_lower]
                        content = content.replace(f'[[{broken_link}]]', f'[[{correct_name}]]')
                        content = content.replace(f'[[{broken_link}|', f'[[{correct_name}|')
                        self.links_fixed += 1
                        continue
                        
                    # Try removing common prefixes
                    for prefix in ['Item_', 'NPC_', 'Location_', 'Quest_', 'Session_']:
                        if broken_link.startswith(prefix):
                            clean_name = broken_link[len(prefix):]
                            if clean_name.lower() in all_notes:
                                correct_name = all_notes[clean_name.lower()]
                                content = content.replace(f'[[{broken_link}]]', f'[[{correct_name}]]')
                                self.links_fixed += 1
                                break
                                
                # Write back if changed
                if content != original_content:
                    file_obj.write_text(content, encoding='utf-8')
                    
            except Exception as e:
                print(f"   ⚠️ Error fixing links in {file_path}: {e}")
                
    def final_organization(self):
        """Final organization pass"""
        
        # Move any stray session files to 06_Sessions
        for session_file in self.vault_path.rglob("Session*.md"):
            if "06_Sessions" not in str(session_file):
                dest_dir = self.vault_path / "06_Sessions"
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                try:
                    dest_file = dest_dir / session_file.name
                    if not dest_file.exists():
                        shutil.move(str(session_file), str(dest_file))
                        self.files_organized += 1
                except:
                    pass
                    
        # Move any stray templates to 09_Templates
        for template_file in self.vault_path.rglob("*Template*.md"):
            if "09_Templates" not in str(template_file) and "scripts" not in str(template_file):
                dest_dir = self.vault_path / "09_Templates"
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                try:
                    dest_file = dest_dir / template_file.name
                    if not dest_file.exists():
                        shutil.move(str(template_file), str(dest_file))
                        self.files_organized += 1
                except:
                    pass
                    
    def generate_report(self):
        """Generate final report"""
        print("\n" + "=" * 80)
        print("✅ COMPREHENSIVE FIX COMPLETE")
        print("=" * 80)
        
        print(f"\n📊 Results:")
        print(f"   • Backups moved to Archive: {self.backups_moved}")
        print(f"   • Broken links fixed: {self.links_fixed}")
        print(f"   • Files organized: {self.files_organized}")
        
        # Update vault log
        self.update_vault_log()
        
    def update_vault_log(self):
        """Update VAULT_UPDATES.md"""
        updates_file = self.vault_path / "VAULT_UPDATES.md"
        
        entry = f"""

## 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Comprehensive Vault Fix

### Summary
Comprehensive organization fix including backup archival and link repair.

### Statistics
- **Backups Archived**: {self.backups_moved}
- **Broken Links Fixed**: {self.links_fixed}
- **Files Organized**: {self.files_organized}

### Actions Taken
- Moved all backup directories to 08_Archive/Vault_Backups
- Scanned and fixed broken internal links
- Organized stray session and template files
- Case-insensitive link matching for fixes

### Result
Vault is now properly organized with functioning links and archived backups.

---
"""
        
        if updates_file.exists():
            content = updates_file.read_text(encoding='utf-8')
            content += entry
            updates_file.write_text(content, encoding='utf-8')
            
        print("\n✅ Updated VAULT_UPDATES.md")

def main():
    fixer = ComprehensiveVaultFixer()
    fixer.run()

if __name__ == "__main__":
    main()