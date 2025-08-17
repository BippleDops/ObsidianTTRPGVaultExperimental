#!/usr/bin/env python3
"""
Fast Vault Flattener - Optimized for large vaults
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class FastVaultFlattener:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.moves_log = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Simple flat structure - just 7 main folders
        self.flat_structure = {
            "Adventures": [],
            "World": [],
            "Rules": [],
            "Resources": [],
            "Characters": [],
            "System": [],
            "Archive": []
        }
        
    def quick_flatten(self):
        """Quick flattening based on directory patterns"""
        print("🚀 Fast Vault Flattening Started...")
        
        # Create main directories
        for main_dir in self.flat_structure.keys():
            (self.vault_path / main_dir).mkdir(exist_ok=True)
        
        # Mapping rules for quick reorganization
        mapping = {
            "Adventures": ["**/01_Adventures/**/*.md", "**/Sessions/**/*.md", "**/Quests/**/*.md"],
            "World": ["**/02_Worldbuilding/**/*.md", "**/NPCs/**/*.md", "**/Locations/**/*.md"],
            "Rules": ["**/03_Mechanics/**/*.md", "**/Rules/**/*.md", "**/Combat/**/*.md"],
            "Resources": ["**/04_Resources/**/*", "**/Maps/**/*", "**/Assets/**/*"],
            "Characters": ["**/05_Player_Characters/**/*.md", "**/07_Player_Resources/**/*.md"],
            "System": ["**/00_System/**/*.md", "**/00_Indexes/**/*.md", "**/Templates/**/*.md"],
        }
        
        for target_dir, patterns in mapping.items():
            target_path = self.vault_path / target_dir
            moved = 0
            
            for pattern in patterns:
                try:
                    for file_path in list(self.vault_path.glob(pattern))[:100]:  # Process in batches
                        if file_path.is_file() and not file_path.is_relative_to(target_path):
                            dest = target_path / file_path.name
                            if not dest.exists():
                                shutil.move(str(file_path), str(dest))
                                moved += 1
                                if moved >= 100:
                                    break
                except Exception as e:
                    continue
                    
            print(f"  ✓ Moved {moved} files to {target_dir}")
        
        # Quick cleanup of empty directories
        for root, dirs, files in os.walk(self.vault_path, topdown=False):
            if not files and not dirs and Path(root) != self.vault_path:
                try:
                    os.rmdir(root)
                except:
                    pass
        
        print("✅ Fast flattening complete!")
        
        # Create simple index
        self.create_simple_index()
        
    def create_simple_index(self):
        """Create a simple navigation index"""
        index_content = f"""---
tags: [index, flattened]
created: {datetime.now().strftime("%Y-%m-%d")}
---

# 📁 Flattened Vault Structure

Your vault has been reorganized into a simpler, flatter structure:

## 🎮 [[Adventures]]
All campaigns, sessions, quests, and encounters

## 🌍 [[World]]  
NPCs, locations, factions, and lore

## 📖 [[Rules]]
Game mechanics, homebrew, and references

## 🎨 [[Resources]]
Maps, assets, handouts, and tables

## 👥 [[Characters]]
Player characters and party resources

## ⚙️ [[System]]
Templates, automation, and vault management

## 📦 [[Archive]]
Old versions and deprecated content

---
*Vault flattened for better organization*
"""
        
        index_path = self.vault_path / "README.md"
        index_path.write_text(index_content, encoding='utf-8')
        print(f"  ✓ Created index at {index_path.name}")

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    flattener = FastVaultFlattener(vault_path)
    flattener.quick_flatten()