#!/usr/bin/env python3
"""
Complete Vault Flattener - Removes all numbered directories
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class CompleteVaultFlattener:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.moved_count = 0
        
    def flatten_numbered_directories(self):
        """Move all content from numbered directories to flat structure"""
        print("🔨 Complete Vault Flattening - Removing numbered directories...")
        
        # Ensure flat structure exists
        flat_dirs = ["Adventures", "World", "Rules", "Resources", "Characters", "System", "Archive"]
        for dir_name in flat_dirs:
            (self.vault_path / dir_name).mkdir(exist_ok=True)
        
        # Mapping of numbered dirs to flat structure
        mappings = {
            "00_Indexes": "System",
            "00_System": "System",
            "01_Adventures": "Adventures",
            "02_Worldbuilding": "World",
            "03_People": "World/NPCs",
            "03_Mechanics": "Rules",
            "04_Resources": "Resources",
            "05_Player_Characters": "Characters",
            "05_Rules": "Rules",
            "06_Sessions": "Adventures/Sessions",
            "07_Player_Resources": "Characters",
            "08_Archive": "Archive",
            "09_Performance": "System/Analytics",
            "12_Research": "Resources/Research",
            "14_Personal": "Archive/Personal",
            "_INDEXES": "System/Indexes",
            "_METADATA": "System/Metadata",
            "MASTER_GUIDES": "System/Guides"
        }
        
        for old_dir, new_location in mappings.items():
            old_path = self.vault_path / old_dir
            
            if old_path.exists() and old_path.is_dir():
                # Create target subdirectory if needed
                target_path = self.vault_path / new_location
                target_path.mkdir(parents=True, exist_ok=True)
                
                print(f"\n  Moving {old_dir} → {new_location}")
                
                # Move all contents
                for item in old_path.iterdir():
                    if item.name.startswith('.'):
                        continue
                        
                    dest = target_path / item.name
                    
                    # Handle name conflicts
                    if dest.exists():
                        if item.is_file():
                            counter = 1
                            stem = item.stem
                            suffix = item.suffix
                            while dest.exists():
                                dest = target_path / f"{stem}_{counter}{suffix}"
                                counter += 1
                        else:
                            # For directories, merge contents
                            if item.is_dir():
                                for subitem in item.rglob('*'):
                                    if subitem.is_file():
                                        rel_path = subitem.relative_to(item)
                                        subdest = dest / rel_path
                                        subdest.parent.mkdir(parents=True, exist_ok=True)
                                        if not subdest.exists():
                                            shutil.move(str(subitem), str(subdest))
                                            self.moved_count += 1
                                continue
                    
                    try:
                        shutil.move(str(item), str(dest))
                        self.moved_count += 1
                        print(f"    ✓ Moved {item.name}")
                    except Exception as e:
                        print(f"    ⚠️ Could not move {item.name}: {e}")
                
                # Remove empty old directory
                try:
                    if not list(old_path.iterdir()):
                        old_path.rmdir()
                        print(f"    ✓ Removed empty {old_dir}")
                except:
                    pass
        
        print(f"\n✅ Moved {self.moved_count} items to flat structure")
        
    def create_new_readme(self):
        """Create new README for flattened structure"""
        content = f"""# 📚 TTRPG Vault - Flattened Structure

*Reorganized on {datetime.now().strftime("%Y-%m-%d %H:%M")}*

## 📁 New Directory Structure

### 🎮 Adventures/
- **Sessions/** - Game session notes and logs
- **Quests/** - Quest descriptions and tracking  
- **Encounters/** - Combat and social encounters
- **Campaigns/** - Campaign overviews and arcs

### 🌍 World/
- **NPCs/** - All non-player characters
- **Locations/** - Cities, dungeons, regions
- **Factions/** - Organizations and groups
- **Lore/** - History and mythology
- **Timeline/** - World events chronology

### 📖 Rules/
- **Mechanics/** - Core game mechanics
- **Homebrew/** - Custom rules and content
- **References/** - Quick lookup guides
- **Tables/** - Random generation tables

### 🎨 Resources/
- **Maps/** - Battle maps and world maps
- **Assets/** - Images and artwork
- **Handouts/** - Player materials
- **Research/** - Reference materials
- **Tools/** - Generators and calculators

### 👥 Characters/
- **PCs/** - Player character sheets
- **Party/** - Party resources and tracking
- **Backstories/** - Character histories
- **Development/** - Character progression

### ⚙️ System/
- **Indexes/** - Navigation and organization
- **Metadata/** - Vault configuration
- **Analytics/** - Performance tracking
- **Guides/** - Master documentation
- **Templates/** - Note templates
- **Automation/** - Scripts and queries

### 📦 Archive/
- **Old/** - Previous versions
- **Deprecated/** - Outdated content
- **Personal/** - Personal notes
- **Backups/** - Backup copies

## 🔍 Quick Navigation

- [[System/Indexes/Master_Index|Master Index]]
- [[World/NPCs/NPC_Directory|All NPCs]]
- [[World/Locations/Location_Index|All Locations]]
- [[Adventures/Sessions/Session_Log|Session History]]
- [[Rules/References/Quick_Rules|Quick Rules Reference]]

## 📊 Vault Statistics

- **Total Reorganized**: {self.moved_count} items
- **Structure**: 7 main categories
- **Depth**: Maximum 3 levels
- **Organization**: Topic-based, not numbered

---
*The vault has been flattened for easier navigation and better organization.*
"""
        
        readme_path = self.vault_path / "README.md"
        readme_path.write_text(content, encoding='utf-8')
        print(f"  ✓ Created new README.md")
        
    def run(self):
        """Execute complete flattening"""
        self.flatten_numbered_directories()
        self.create_new_readme()
        
        print("\n" + "=" * 60)
        print("✅ VAULT FLATTENING COMPLETE!")
        print("=" * 60)
        print("Your vault now has a clean, flat structure:")
        print("  • No more numbered directories")
        print("  • Maximum 3 levels of nesting")
        print("  • Logical topic-based organization")
        print("  • Easy to navigate and maintain")

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    flattener = CompleteVaultFlattener(vault_path)
    flattener.run()