#!/usr/bin/env python3
"""
EMERGENCY: Undo vault reorganization and restore original structure
"""

import os
import shutil
from pathlib import Path

class UndoReorganization:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.restored_count = 0
        
    def restore_original_structure(self):
        """Restore the original numbered directory structure"""
        print("🔧 UNDOING REORGANIZATION - RESTORING ORIGINAL STRUCTURE...")
        
        # Recreate original numbered directories
        original_dirs = [
            "00_Indexes",
            "00_System", 
            "01_Adventures",
            "02_Worldbuilding",
            "03_People",
            "03_Mechanics",
            "04_Resources",
            "05_Player_Characters",
            "05_Rules",
            "06_Sessions",
            "07_Player_Resources",
            "08_Archive",
            "09_Performance",
            "12_Research",
            "_INDEXES",
            "_METADATA",
            "MASTER_GUIDES"
        ]
        
        for dir_name in original_dirs:
            (self.vault_path / dir_name).mkdir(exist_ok=True)
            print(f"  ✓ Restored {dir_name}")
            
        # Move files back from flattened structure to original locations
        restore_mappings = {
            "System/Indexes": "00_Indexes",
            "System/Automation": "00_System/Automation",
            "System/Canvas_Templates": "00_System/Canvas_Templates",
            "System/Analytics": "09_Performance",
            "System/Metadata": "_METADATA",
            "System/Guides": "MASTER_GUIDES",
            "World/NPCs": "03_People",
            "World/Stubs": "02_Worldbuilding/Stubs",
            "World/Lore": "02_Worldbuilding/Lore",
            "World/Places": "02_Worldbuilding/Places",
            "World/Groups": "02_Worldbuilding/Groups",
            "World/People": "02_Worldbuilding/People",
            "World/Items": "02_Worldbuilding/Items",
            "Adventures/Sessions": "06_Sessions",
            "Resources/Tools": "04_Resources/Tools",
            "Resources/Handouts": "04_Resources/Handouts",
            "Resources/References": "04_Resources/References",
            "Resources/GM_Resources": "04_Resources/GM_Resources",
            "Resources/Assets": "04_Resources/Assets",
            "Resources/Research": "12_Research",
            "Characters/Tools": "07_Player_Resources/Tools",
            "Archive/backups": "08_Archive/backups",
            "Rules": "05_Rules"
        }
        
        for source, target in restore_mappings.items():
            source_path = self.vault_path / source
            target_path = self.vault_path / target
            
            if source_path.exists():
                # Create parent directories if needed
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move all contents back
                if source_path.is_dir():
                    for item in source_path.iterdir():
                        dest = target_path / item.name
                        try:
                            shutil.move(str(item), str(dest))
                            self.restored_count += 1
                        except Exception as e:
                            print(f"    ⚠️ Could not restore {item.name}: {e}")
                            
        print(f"\n✅ Restored {self.restored_count} items to original locations")
        
        # Remove the new directories if empty
        new_dirs = ["Adventures", "World", "Rules", "Resources", "Characters", "System", "Archive"]
        for dir_name in new_dirs:
            dir_path = self.vault_path / dir_name
            if dir_path.exists():
                try:
                    # Only remove if empty
                    if not list(dir_path.iterdir()):
                        dir_path.rmdir()
                        print(f"  ✓ Removed empty {dir_name}")
                except:
                    pass
                    
    def run(self):
        """Execute the undo operation"""
        print("=" * 60)
        print("🚨 EMERGENCY UNDO - RESTORING ORIGINAL STRUCTURE")
        print("=" * 60)
        
        self.restore_original_structure()
        
        print("\n" + "=" * 60)
        print("✅ UNDO COMPLETE - ORIGINAL STRUCTURE RESTORED")
        print("=" * 60)
        print("Your vault has been restored to its original numbered directory structure.")
        print("Please verify that all files are back in their original locations.")

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    undo = UndoReorganization(vault_path)
    undo.run()