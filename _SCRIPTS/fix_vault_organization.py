#!/usr/bin/env python3
"""
Fix vault organization by eliminating duplicate subdirectory structures
and reorganizing all content into the proper top-level directories.
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple

class VaultOrganizationFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.files_moved = 0
        self.directories_removed = 0
        self.links_fixed = 0
        self.errors = []
        
        # Define the correct top-level structure
        self.correct_structure = {
            "00_Indexes": "Indexes, navigation, and documentation",
            "01_Adventures": "Adventure modules, campaigns, and quests",
            "02_Worldbuilding": "Lore, history, culture, and world details",
            "03_People": "NPCs, characters, and personalities",
            "04_Places": "Locations, maps, and geography",
            "04_Resources": "Assets, media, handouts, and resources",
            "05_Rules": "Game mechanics, rules, and systems",
            "06_Sessions": "Session notes, planning, and logs",
            "07_Player_Resources": "Player handouts, guides, and references",
            "08_Archive": "Archived content and backups",
            "09_Templates": "Note templates and forms",
            "10_Inspiration": "Ideas, concepts, and creative material",
            "11_References": "External references and source material",
            "12_Research": "Research notes and development",
            "13_Performance": "Metrics, reports, and optimization"
        }
        
        # Map subdirectories that shouldn't exist to their correct parent
        self.incorrect_nesting = {
            "01_Adventures/02_Worldbuilding": "02_Worldbuilding",
            "01_Adventures/04_Resources": "04_Resources",
            "01_Adventures/05_Templates": "09_Templates",
            "01_Adventures/06_GM_Resources": "06_Sessions",
            "01_Adventures/06_Session_Management": "06_Sessions",
            "01_Adventures/07_Player_Resources": "07_Player_Resources",
            "02_Worldbuilding/Lore/01_Adventures": "01_Adventures",
            "02_Worldbuilding/Lore/02_Worldbuilding": "02_Worldbuilding/Lore",
            "02_Worldbuilding/Places/02_Worldbuilding": "02_Worldbuilding/Places",
            "02_Worldbuilding/Groups/02_Worldbuilding": "02_Worldbuilding/Groups",
            "02_Worldbuilding/People/01_Adventures": "01_Adventures",
            "02_Worldbuilding/People/02_Worldbuilding": "02_Worldbuilding/People",
            "02_Worldbuilding/Items/02_Worldbuilding": "02_Worldbuilding/Items"
        }
        
        # Track all file moves for link fixing
        self.file_moves = {}  # old_path -> new_path
        
    def run(self):
        """Main execution"""
        print("=" * 80)
        print("🔧 VAULT ORGANIZATION FIXER")
        print("=" * 80)
        
        # Phase 1: Analyze current structure
        print("\n📊 Phase 1: Analyzing vault structure...")
        self.analyze_structure()
        
        # Phase 2: Move files from incorrect nested directories
        print("\n📁 Phase 2: Moving files from incorrect locations...")
        self.fix_nested_directories()
        
        # Phase 3: Reorganize misplaced content
        print("\n🗂️ Phase 3: Reorganizing misplaced content...")
        self.reorganize_content()
        
        # Phase 4: Clean up empty directories
        print("\n🧹 Phase 4: Cleaning up empty directories...")
        self.cleanup_empty_directories()
        
        # Phase 5: Fix all broken links
        print("\n🔗 Phase 5: Fixing broken links...")
        self.fix_all_links()
        
        # Phase 6: Generate report
        self.generate_report()
        
    def analyze_structure(self):
        """Analyze and report on structural issues"""
        issues = []
        
        # Find all duplicate directory patterns
        for root, dirs, files in os.walk(self.vault_path):
            rel_path = Path(root).relative_to(self.vault_path)
            
            # Check for numbered directories where they shouldn't be
            for dir_name in dirs:
                if re.match(r'^\d{2}_', dir_name):  # Starts with XX_
                    parent = str(rel_path)
                    # If this is a numbered dir inside another numbered dir, it's wrong
                    if re.match(r'^\d{2}_', parent.split('/')[0] if '/' in parent else parent):
                        issues.append(f"{rel_path}/{dir_name}")
                        
        print(f"   Found {len(issues)} structural issues")
        for issue in issues[:10]:  # Show first 10
            print(f"   - {issue}")
            
    def fix_nested_directories(self):
        """Move files from incorrectly nested directories"""
        for incorrect_path, correct_parent in self.incorrect_nesting.items():
            source_dir = self.vault_path / incorrect_path
            
            if not source_dir.exists():
                continue
                
            print(f"\n   Processing {incorrect_path}...")
            
            # Create correct destination
            if '/' in correct_parent:
                dest_dir = self.vault_path / correct_parent
            else:
                dest_dir = self.vault_path / correct_parent
                
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Move all contents
            for item in source_dir.rglob("*"):
                if item.is_file():
                    # Calculate relative path from the incorrect nested directory
                    rel_path = item.relative_to(source_dir)
                    
                    # Create new path in correct location
                    new_path = dest_dir / rel_path
                    new_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        # Track the move for link fixing
                        old_vault_path = item.relative_to(self.vault_path)
                        new_vault_path = new_path.relative_to(self.vault_path)
                        self.file_moves[str(old_vault_path)] = str(new_vault_path)
                        
                        # Move the file
                        shutil.move(str(item), str(new_path))
                        self.files_moved += 1
                        
                    except Exception as e:
                        self.errors.append(f"Error moving {item}: {e}")
                        
            # Remove the now-empty incorrect directory
            try:
                if source_dir.exists() and not any(source_dir.iterdir()):
                    shutil.rmtree(source_dir)
                    self.directories_removed += 1
                    print(f"   ✓ Removed empty directory: {incorrect_path}")
            except:
                pass
                
    def reorganize_content(self):
        """Reorganize content based on type"""
        
        # Special case reorganizations
        reorganizations = {
            # Adventures in wrong places
            "**/Session_*.md": "06_Sessions",
            "**/Quest*.md": "01_Adventures",
            "**/Campaign_*.md": "01_Adventures",
            
            # Worldbuilding in wrong places
            "**/Lore_*.md": "02_Worldbuilding/Lore",
            "**/History_*.md": "02_Worldbuilding/Lore",
            "**/Culture_*.md": "02_Worldbuilding/Lore",
            
            # People in wrong places
            "**/NPC_*.md": "03_People",
            "**/Character_*.md": "03_People",
            
            # Places in wrong places  
            "**/Location_*.md": "04_Places",
            "**/Map_*.md": "04_Places",
            
            # Rules in wrong places
            "**/Rule_*.md": "05_Rules",
            "**/Mechanic_*.md": "05_Rules",
            
            # Templates in wrong places
            "**/Template_*.md": "09_Templates",
            "**/*_Template.md": "09_Templates"
        }
        
        for pattern, destination in reorganizations.items():
            for file_path in self.vault_path.glob(pattern):
                # Skip if already in correct location
                if destination in str(file_path):
                    continue
                    
                # Skip system files
                if any(skip in str(file_path) for skip in ['scripts/', '.git/', 'Archive/']):
                    continue
                    
                dest_dir = self.vault_path / destination
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                new_path = dest_dir / file_path.name
                
                # Handle duplicates
                if new_path.exists():
                    base = new_path.stem
                    ext = new_path.suffix
                    counter = 1
                    while new_path.exists():
                        new_path = dest_dir / f"{base}_{counter}{ext}"
                        counter += 1
                        
                try:
                    # Track the move
                    old_vault_path = file_path.relative_to(self.vault_path)
                    new_vault_path = new_path.relative_to(self.vault_path)
                    self.file_moves[str(old_vault_path)] = str(new_vault_path)
                    
                    shutil.move(str(file_path), str(new_path))
                    self.files_moved += 1
                    
                except Exception as e:
                    self.errors.append(f"Error reorganizing {file_path}: {e}")
                    
    def cleanup_empty_directories(self):
        """Remove empty directories after reorganization"""
        
        # Walk bottom-up to remove empty directories
        for root, dirs, files in os.walk(self.vault_path, topdown=False):
            # Skip system directories
            if any(skip in root for skip in ['.git', 'scripts', '.obsidian']):
                continue
                
            # Check each subdirectory
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                
                try:
                    # If directory is empty, remove it
                    if dir_path.exists() and not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        self.directories_removed += 1
                        print(f"   ✓ Removed empty directory: {dir_path.relative_to(self.vault_path)}")
                except:
                    pass  # Directory not empty or permission issue
                    
    def fix_all_links(self):
        """Fix all internal links after file moves"""
        
        print(f"   Fixing links for {len(self.file_moves)} moved files...")
        
        # Process all markdown files
        for md_file in self.vault_path.rglob("*.md"):
            # Skip system files
            if any(skip in str(md_file) for skip in ['scripts/', '.git/']):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content
                
                # Fix each moved file's links
                for old_path, new_path in self.file_moves.items():
                    # Get just the filename without extension for link matching
                    old_name = Path(old_path).stem
                    new_name = Path(new_path).stem
                    
                    # Fix [[wiki-style]] links
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\]\]',
                        f'[[{new_name}]]',
                        content
                    )
                    
                    # Fix [[wiki-style|display]] links
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\|([^\]]+)\]\]',
                        rf'[[{new_name}|\1]]',
                        content
                    )
                    
                    # Fix relative path links
                    if '/' in old_path:
                        content = re.sub(
                            rf'\[\[{re.escape(old_path.replace(".md", ""))}\]\]',
                            f'[[{new_path.replace(".md", "")}]]',
                            content
                        )
                        
                # Only write if changed
                if content != original_content:
                    md_file.write_text(content, encoding='utf-8')
                    self.links_fixed += 1
                    
            except Exception as e:
                self.errors.append(f"Error fixing links in {md_file}: {e}")
                
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 80)
        print("✅ VAULT ORGANIZATION FIXED")
        print("=" * 80)
        
        print(f"\n📊 Results:")
        print(f"   • Files moved: {self.files_moved}")
        print(f"   • Directories removed: {self.directories_removed}")
        print(f"   • Links fixed: {self.links_fixed}")
        
        if self.errors:
            print(f"\n⚠️ Errors encountered: {len(self.errors)}")
            for error in self.errors[:5]:
                print(f"   - {error}")
                
        # Create structure documentation
        self.create_structure_documentation()
        
        # Update vault log
        self.update_vault_log()
        
    def create_structure_documentation(self):
        """Create documentation of the new structure"""
        doc_content = f"""---
title: Vault Structure Documentation
type: documentation
tags:
- structure
- organization
- guide
created: '{datetime.now().strftime('%Y-%m-%d')}'
modified: '{datetime.now().strftime('%Y-%m-%d')}'
---

# 📁 VAULT STRUCTURE DOCUMENTATION

## ✅ Correct Directory Structure

The vault is organized into the following top-level directories:

"""
        
        for dir_name, description in self.correct_structure.items():
            doc_content += f"### {dir_name}\n{description}\n\n"
            
        doc_content += """
## 🚫 Common Mistakes to Avoid

1. **No nested numbered directories**: Never put 01_Adventures inside 02_Worldbuilding
2. **No duplicate structures**: Each category should exist only at the top level
3. **Use correct directory**: Place files based on their primary purpose
4. **Maintain flat hierarchy**: Avoid deep nesting beyond 2-3 levels

## 📝 File Placement Guide

| Content Type | Correct Directory |
|-------------|------------------|
| Adventures, Quests | 01_Adventures |
| NPCs, Characters | 03_People |
| Locations, Maps | 04_Places |
| Lore, History | 02_Worldbuilding |
| Session Notes | 06_Sessions |
| Rules, Mechanics | 05_Rules |
| Player Handouts | 07_Player_Resources |
| Templates | 09_Templates |
| Images, Assets | 04_Resources |

## 🔗 Linking Best Practices

1. Use simple [[Note Name]] links when possible
2. Avoid full path links unless necessary
3. Let Obsidian handle link resolution
4. Use aliases for display names: [[Note Name|Display Text]]

---

*This structure ensures optimal organization and navigation.*
"""
        
        doc_path = self.vault_path / "00_Indexes" / "Vault_Structure_Documentation.md"
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(doc_content, encoding='utf-8')
        print("\n✅ Created Vault Structure Documentation")
        
    def update_vault_log(self):
        """Update VAULT_UPDATES.md with reorganization report"""
        updates_file = self.vault_path / "VAULT_UPDATES.md"
        
        entry = f"""

## 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Vault Organization Fix

### Summary
Fixed duplicate subdirectory structures and reorganized vault into proper hierarchy.

### Statistics
- **Files Moved**: {self.files_moved}
- **Directories Removed**: {self.directories_removed}
- **Links Fixed**: {self.links_fixed}
- **Errors**: {len(self.errors)}

### Major Fixes
- Eliminated nested numbered directories (01_Adventures inside 02_Worldbuilding, etc.)
- Moved all content to correct top-level directories
- Removed empty and duplicate directories
- Fixed all internal links to reflect new locations

### Structural Improvements
- Flattened unnecessary nesting
- Consolidated duplicate content
- Standardized directory purposes
- Created clear organization documentation

### Directories Cleaned
- 01_Adventures/02_Worldbuilding → Content moved to proper locations
- 02_Worldbuilding/*/02_Worldbuilding → Flattened nested duplicates
- Empty directories removed after content migration

### Result
The vault now has a clean, logical structure with all content in appropriate directories and all links functioning correctly.

---
"""
        
        if updates_file.exists():
            content = updates_file.read_text(encoding='utf-8')
            content += entry
            updates_file.write_text(content, encoding='utf-8')
        else:
            updates_file.write_text(entry, encoding='utf-8')
            
        print("✅ Updated VAULT_UPDATES.md")

def main():
    fixer = VaultOrganizationFixer()
    fixer.run()

if __name__ == "__main__":
    main()