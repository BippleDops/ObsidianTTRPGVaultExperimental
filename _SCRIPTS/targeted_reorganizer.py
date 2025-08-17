#!/usr/bin/env python3
"""
Targeted Reorganizer - Handles specific miscategorization issues
"""

import os
import shutil
from pathlib import Path
import re

class TargetedReorganizer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.moved = 0
        self.report = []
        
    def move_module_content(self):
        """Move D&D module content to appropriate location"""
        print("📚 Moving D&D module content...")
        
        # Create modules directory
        modules_dir = self.vault_path / "04_Resources" / "Modules"
        modules_dir.mkdir(parents=True, exist_ok=True)
        
        # Find module files in wrong places
        quests_dir = self.vault_path / "01_Adventures" / "Quests"
        if quests_dir.exists():
            for file_path in quests_dir.glob("*chapter*.md"):
                try:
                    # Move to modules
                    target = modules_dir / file_path.name
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        self.moved += 1
                        self.report.append(f"Moved module: {file_path.name}")
                except:
                    pass
                    
        print(f"  ✓ Moved {self.moved} module files")
        
    def separate_npcs_from_quests(self):
        """Move NPCs that are in the Quests folder"""
        print("🎭 Separating NPCs from Quests...")
        
        quests_dir = self.vault_path / "01_Adventures" / "Quests"
        npcs_dir = self.vault_path / "03_People"
        
        if not quests_dir.exists():
            return
            
        count = 0
        for file_path in list(quests_dir.glob("*.md"))[:200]:
            try:
                content = file_path.read_text(encoding='utf-8').lower()
                
                # Check if it's actually an NPC
                npc_indicators = ['personality', 'alignment', 'str', 'dex', 'con', 'race', 'class']
                quest_indicators = ['objective', 'reward', 'quest', 'adventure', 'mission']
                
                npc_score = sum(1 for ind in npc_indicators if ind in content)
                quest_score = sum(1 for ind in quest_indicators if ind in content)
                
                if npc_score > quest_score and npc_score > 2:
                    # It's an NPC, move it
                    target = npcs_dir / file_path.name
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        count += 1
                        self.moved += 1
                        
            except:
                pass
                
        print(f"  ✓ Moved {count} NPCs out of Quests folder")
        
    def organize_images(self):
        """Move images to proper Resources folder"""
        print("🖼️ Organizing images...")
        
        images_dir = self.vault_path / "04_Resources" / "Assets" / "Images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        count = 0
        # Find images scattered around
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.svg']:
            for file_path in self.vault_path.glob(f"**/{ext}"):
                # Skip if already in Resources
                if "04_Resources" in str(file_path):
                    continue
                    
                # Skip .obsidian folder
                if ".obsidian" in str(file_path):
                    continue
                    
                try:
                    # Determine subfolder based on name
                    name_lower = file_path.name.lower()
                    if 'portrait' in name_lower or 'npc' in name_lower:
                        target_dir = self.vault_path / "04_Resources" / "Assets" / "Portraits"
                    elif 'map' in name_lower or 'battle' in name_lower:
                        target_dir = self.vault_path / "04_Resources" / "Assets" / "Maps"
                    elif 'token' in name_lower:
                        target_dir = self.vault_path / "04_Resources" / "Assets" / "Tokens"
                    elif 'symbol' in name_lower or 'heraldry' in name_lower:
                        target_dir = self.vault_path / "04_Resources" / "Assets" / "Symbols"
                    else:
                        target_dir = images_dir
                        
                    target_dir.mkdir(parents=True, exist_ok=True)
                    target = target_dir / file_path.name
                    
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        count += 1
                        self.moved += 1
                        
                except:
                    pass
                    
        print(f"  ✓ Organized {count} images")
        
    def clean_empty_files(self):
        """Remove empty or stub files"""
        print("🗑️ Cleaning empty files...")
        
        count = 0
        for file_path in self.vault_path.glob("**/*.md"):
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Remove if essentially empty
                if len(content.strip()) < 10:
                    os.remove(file_path)
                    count += 1
                    self.moved += 1
                    
            except:
                pass
                
        print(f"  ✓ Removed {count} empty files")
        
    def consolidate_duplicates(self):
        """Find and consolidate duplicate content"""
        print("🔄 Consolidating duplicates...")
        
        # Track files by name stem
        file_groups = {}
        
        for file_path in self.vault_path.glob("**/*.md"):
            if ".obsidian" in str(file_path) or "_SCRIPTS" in str(file_path):
                continue
                
            stem = file_path.stem.lower()
            # Remove numbers and common suffixes
            stem = re.sub(r'[_\-]\d+$', '', stem)
            stem = re.sub(r'_copy$', '', stem)
            stem = re.sub(r'_\d$', '', stem)
            
            if stem not in file_groups:
                file_groups[stem] = []
            file_groups[stem].append(file_path)
            
        # Archive duplicates
        archive_dir = self.vault_path / "08_Archive" / "duplicates"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        count = 0
        for stem, files in file_groups.items():
            if len(files) > 1:
                # Keep the largest file
                files.sort(key=lambda x: x.stat().st_size, reverse=True)
                
                for duplicate in files[1:]:
                    try:
                        target = archive_dir / duplicate.name
                        if not target.exists():
                            shutil.move(str(duplicate), str(target))
                            count += 1
                            self.moved += 1
                    except:
                        pass
                        
        print(f"  ✓ Archived {count} duplicate files")
        
    def create_proper_structure(self):
        """Ensure proper directory structure exists"""
        print("📁 Creating proper structure...")
        
        structure = {
            "01_Adventures": ["Campaigns", "Quests", "Encounters", "Hooks"],
            "02_Worldbuilding": ["Locations", "Factions", "Lore", "Timeline", "Politics"],
            "03_People": ["PCs", "NPCs", "Monsters", "Groups"],
            "04_Resources": ["Assets/Maps", "Assets/Portraits", "Assets/Tokens", "Assets/Handouts", 
                           "Tables", "Modules", "References"],
            "05_Rules": ["Core", "Homebrew", "Spells", "Items", "Conditions"],
            "06_Sessions": ["Notes", "Prep", "Recaps", "Planning"],
            "07_Player_Resources": ["Handouts", "Maps", "Rules", "Lore"],
            "08_Archive": ["Old_Sessions", "Retired_NPCs", "Completed_Quests", "duplicates"],
            "09_Performance": ["Reports", "Analytics", "Logs"]
        }
        
        for main_dir, subdirs in structure.items():
            for subdir in subdirs:
                full_path = self.vault_path / main_dir / subdir
                full_path.mkdir(parents=True, exist_ok=True)
                
        print("  ✓ Directory structure verified")
        
    def generate_report(self):
        """Generate reorganization report"""
        from datetime import datetime
        
        report_content = f"""# Targeted Reorganization Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Total Operations**: {self.moved}

## Actions Taken

### 📚 Module Content
Moved D&D module chapters to proper Resources/Modules folder

### 🎭 NPCs Separation  
Separated NPCs from Quests folder to 03_People

### 🖼️ Image Organization
Organized images into proper Assets subfolders

### 🗑️ Cleanup
Removed empty and stub files

### 🔄 Duplicate Consolidation
Archived duplicate files to 08_Archive/duplicates

### 📁 Structure Creation
Ensured proper directory structure exists

## Summary

✅ Successfully reorganized {self.moved} items
✅ Improved vault organization
✅ Separated content by type
✅ Cleaned up duplicates and empty files

## Recommendations

1. Review 08_Archive/duplicates for any needed content
2. Check 04_Resources/Modules for module organization
3. Verify NPCs are properly categorized in 03_People
4. Update any broken links from moved files
5. Consider adding tags to prevent future miscategorization

## Note on Archive Folders

- **08_Archive**: For old/completed content
- **09_Performance**: For reports and analytics only

These folders should not contain active game content.
"""
        
        report_path = self.vault_path / "09_Performance" / f"targeted_reorg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report_content, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
    def run(self):
        """Execute targeted reorganization"""
        print("=" * 60)
        print("🎯 TARGETED REORGANIZATION")
        print("=" * 60)
        
        self.create_proper_structure()
        self.move_module_content()
        self.separate_npcs_from_quests()
        self.organize_images()
        self.clean_empty_files()
        self.consolidate_duplicates()
        
        self.generate_report()
        
        print("\n" + "=" * 60)
        print(f"✅ REORGANIZATION COMPLETE")
        print(f"   Total Operations: {self.moved}")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    reorganizer = TargetedReorganizer(vault_path)
    reorganizer.run()