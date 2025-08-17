#!/usr/bin/env python3
"""
Fix duplicate directories and update all links systematically
"""
import os
import shutil
import re
from pathlib import Path
from collections import defaultdict

class DirectoryAndLinkFixer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.moved_files = {}
        self.link_updates = 0
        
    def fix_duplicate_directories(self):
        """Fix the duplicate directory structures"""
        print("\n📁 Fixing duplicate directories...")
        
        # Map of wrong locations to correct locations
        directory_fixes = {
            '02_Worldbuilding/Groups/04_Resources': '04_Resources',
            '02_Worldbuilding/Items/04_Resources': '04_Resources',
            '02_Worldbuilding/Lore/04_Resources': '04_Resources',
            '02_Worldbuilding/Groups/05_Templates': '09_Templates',
            '02_Worldbuilding/Items/05_Templates': '09_Templates',
            '02_Worldbuilding/Groups/07_Player_Resources': '07_Player_Resources',
            '02_Worldbuilding/Items/07_Player_Resources': '07_Player_Resources',
            '05_Templates': '09_Templates',
            '09_Performance': '13_Performance',
            '10_Performance': '13_Performance',
            '01_Adventures/02_Worldbuilding': '02_Worldbuilding',
            '01_Adventures/03_People': '03_People',
            '01_Adventures/04_Places': '04_Places',
        }
        
        for wrong_dir, correct_dir in directory_fixes.items():
            wrong_path = self.vault_path / wrong_dir
            correct_path = self.vault_path / correct_dir
            
            if wrong_path.exists():
                # Ensure correct directory exists
                correct_path.mkdir(parents=True, exist_ok=True)
                
                # Move all contents
                for item in wrong_path.iterdir():
                    target = correct_path / item.name
                    
                    # Handle duplicates
                    if target.exists():
                        # Add number suffix for duplicates
                        counter = 1
                        while target.exists():
                            if item.is_file():
                                stem = item.stem
                                suffix = item.suffix
                                target = correct_path / f"{stem}_{counter}{suffix}"
                            else:
                                target = correct_path / f"{item.name}_{counter}"
                            counter += 1
                    
                    try:
                        shutil.move(str(item), str(target))
                        self.moved_files[str(item.relative_to(self.vault_path))] = str(target.relative_to(self.vault_path))
                        print(f"   ✓ Moved: {item.name} to {correct_dir}")
                    except Exception as e:
                        print(f"   ✗ Error moving {item}: {e}")
                
                # Remove empty directory
                try:
                    wrong_path.rmdir()
                    print(f"   ✓ Removed empty directory: {wrong_dir}")
                except:
                    pass
                    
    def update_all_links(self):
        """Update every link in every file one by one"""
        print("\n🔗 Updating all links systematically...")
        
        # Get all markdown files
        md_files = list(self.vault_path.rglob("*.md"))
        total_files = len(md_files)
        
        for idx, md_file in enumerate(md_files, 1):
            if any(skip in str(md_file) for skip in ['scripts/', '.obsidian/', 'backups/']):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Update links for moved files
                for old_path, new_path in self.moved_files.items():
                    old_name = Path(old_path).stem
                    new_name = Path(new_path).stem
                    
                    # Update wikilinks [[name]]
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\]\]',
                        f'[[{new_name}]]',
                        content
                    )
                    
                    # Update wikilinks with display text [[name|display]]
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\|([^\]]+)\]\]',
                        rf'[[{new_name}|\1]]',
                        content
                    )
                    
                    # Update markdown links [text](path)
                    content = re.sub(
                        rf'\[([^\]]+)\]\({re.escape(old_path)}(#[^)]+)?\)',
                        rf'[\1]({new_path}\2)',
                        content
                    )
                
                # Fix common broken link patterns
                # Fix links with underscores that should be spaces
                content = re.sub(r'\[\[([^_\]]+)_([^_\]]+)\]\]', r'[[\1 \2]]', content)
                
                # Fix links with hyphens that should be spaces
                content = re.sub(r'\[\[([^-\]]+)-([^-\]]+)\]\]', r'[[\1 \2]]', content)
                
                if content != original_content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.link_updates += 1
                    
                # Progress indicator
                if idx % 100 == 0:
                    print(f"   Processing: {idx}/{total_files} files...")
                    
            except Exception as e:
                print(f"   ✗ Error updating {md_file}: {e}")
        
        print(f"   ✓ Updated links in {self.link_updates} files")
        
    def eliminate_placeholders(self):
        """Remove all placeholder content"""
        print("\n🔄 Eliminating placeholder content...")
        
        placeholder_count = 0
        
        for md_file in self.vault_path.rglob("*.md"):
            if any(skip in str(md_file) for skip in ['scripts/', '.obsidian/', 'VAULT_', 'README']):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Remove TODO markers
                content = re.sub(r'TODO:?\s*[^\n]*\n?', '', content)
                content = re.sub(r'<!--\s*TODO[^>]*-->', '', content)
                
                # Remove placeholder text
                content = re.sub(r'\[placeholder\]', '', content, flags=re.IGNORECASE)
                content = re.sub(r'<!--\s*placeholder\s*-->', '', content, flags=re.IGNORECASE)
                content = re.sub(r'\bplaceholder\b', '', content, flags=re.IGNORECASE)
                
                # Remove TBD markers
                content = re.sub(r'\bTBD\b', '', content)
                content = re.sub(r'\bFIXME:?\s*[^\n]*\n?', '', content)
                
                # Clean up multiple blank lines
                content = re.sub(r'\n\n\n+', '\n\n', content)
                
                if content != original_content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    placeholder_count += 1
                    
            except Exception as e:
                print(f"   ✗ Error processing {md_file}: {e}")
                
        print(f"   ✓ Removed placeholders from {placeholder_count} files")
        
    def run(self):
        """Execute all fixes"""
        print("=" * 80)
        print("🔧 DIRECTORY AND LINK FIXING")
        print("=" * 80)
        
        self.fix_duplicate_directories()
        self.update_all_links()
        self.eliminate_placeholders()
        
        print("\n✅ Complete!")
        print(f"   - Moved {len(self.moved_files)} files to correct directories")
        print(f"   - Updated links in {self.link_updates} files")
        
        return True

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    fixer = DirectoryAndLinkFixer(vault_path)
    fixer.run()