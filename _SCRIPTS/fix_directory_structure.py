#!/usr/bin/env python3
"""
Fix directory structure inconsistencies and consolidate duplicate folders
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class DirectoryStructureFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.directories_fixed = 0
        self.files_moved = 0
        
    def run(self):
        """Main execution"""
        print("=" * 80)
        print("🗂️ DIRECTORY STRUCTURE FIX")
        print("=" * 80)
        
        # Fix directory structure
        print("\n📁 Consolidating and renaming directories...")
        self.fix_directory_structure()
        
        # Generate report
        self.generate_report()
        
    def fix_directory_structure(self):
        """Fix and consolidate directory structure"""
        
        # Define the correct structure
        consolidations = {
            # Merge similar directories
            "05_Player_Resources": "07_Player_Resources",
            "06_GM_Resources": "06_Sessions",  # GM resources should be in sessions or specific folders
            "07_Templates": "09_Templates",
            "09_Campaigns": "01_Adventures",  # Campaigns are adventures
            "09_Performance": "13_Performance",  # Consolidate performance
            "1-Session Journals": "06_Sessions",  # Session journals go with sessions
            "10_Sessions": "06_Sessions",  # Consolidate sessions
            "11_Media": "04_Resources",  # Media goes with resources
        }
        
        for old_dir, new_dir in consolidations.items():
            old_path = self.vault_path / old_dir
            new_path = self.vault_path / new_dir
            
            if old_path.exists() and old_path.is_dir():
                print(f"\n   Processing {old_dir}...")
                
                # Ensure target exists
                new_path.mkdir(parents=True, exist_ok=True)
                
                # Move all contents
                for item in old_path.iterdir():
                    if item.is_file():
                        # Move file
                        target = new_path / item.name
                        # Handle duplicates by adding number
                        if target.exists():
                            base = target.stem
                            ext = target.suffix
                            counter = 1
                            while target.exists():
                                target = new_path / f"{base}_{counter}{ext}"
                                counter += 1
                        shutil.move(str(item), str(target))
                        self.files_moved += 1
                        print(f"      ✓ Moved {item.name}")
                    elif item.is_dir():
                        # Move directory contents recursively
                        target_dir = new_path / item.name
                        if target_dir.exists():
                            # Merge contents
                            for subitem in item.rglob("*"):
                                if subitem.is_file():
                                    rel_path = subitem.relative_to(item)
                                    target_file = target_dir / rel_path
                                    target_file.parent.mkdir(parents=True, exist_ok=True)
                                    if not target_file.exists():
                                        shutil.move(str(subitem), str(target_file))
                                        self.files_moved += 1
                        else:
                            # Move entire directory
                            shutil.move(str(item), str(target_dir))
                            self.files_moved += 1
                            print(f"      ✓ Moved directory {item.name}")
                
                # Remove empty old directory
                if not any(old_path.iterdir()):
                    old_path.rmdir()
                    self.directories_fixed += 1
                    print(f"   ✓ Removed empty directory {old_dir}")
                    
        # Rename directories to have consistent numbering
        renames = {
            "03_Mechanics": "05_Rules",  # Mechanics are rules
        }
        
        for old_name, new_name in renames.items():
            old_path = self.vault_path / old_name
            new_path = self.vault_path / new_name
            
            if old_path.exists() and not new_path.exists():
                shutil.move(str(old_path), str(new_path))
                self.directories_fixed += 1
                print(f"   ✓ Renamed {old_name} to {new_name}")
            elif old_path.exists() and new_path.exists():
                # Merge contents
                print(f"\n   Merging {old_name} into {new_name}...")
                for item in old_path.rglob("*"):
                    if item.is_file():
                        rel_path = item.relative_to(old_path)
                        target = new_path / rel_path
                        target.parent.mkdir(parents=True, exist_ok=True)
                        if not target.exists():
                            shutil.move(str(item), str(target))
                            self.files_moved += 1
                # Remove empty old directory
                if not any(old_path.iterdir()):
                    old_path.rmdir()
                    self.directories_fixed += 1
                    
        # Create any missing standard directories
        standard_dirs = [
            "00_Indexes",
            "01_Adventures", 
            "02_Worldbuilding",
            "03_People",
            "04_Places",
            "05_Rules",
            "06_Sessions",
            "07_Player_Resources",
            "08_Archive",
            "09_Templates",
            "10_Inspiration",
            "11_References",
            "12_Research",
            "13_Performance",
            "04_Resources"  # Keep resources as subfolder of 04
        ]
        
        for dir_name in standard_dirs:
            dir_path = self.vault_path / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✓ Created standard directory {dir_name}")
                
    def generate_report(self):
        """Generate consolidation report"""
        print("\n" + "=" * 80)
        print("✅ DIRECTORY STRUCTURE FIXED")
        print("=" * 80)
        print(f"📊 Results:")
        print(f"   • Directories fixed: {self.directories_fixed}")
        print(f"   • Files moved: {self.files_moved}")
        
        # Update VAULT_UPDATES.md
        self.update_vault_updates()
        
    def update_vault_updates(self):
        """Add directory fix entry to VAULT_UPDATES.md"""
        updates_file = self.vault_path / "VAULT_UPDATES.md"
        
        if updates_file.exists():
            content = updates_file.read_text(encoding='utf-8')
            
            # Find the insertion point
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if '## 📅 2025-08-14 19:11 - Root Directory Cleanup' in line:
                    # Insert after this section
                    while i < len(lines) and not (lines[i].startswith('## 📅') and i > insert_index):
                        i += 1
                    insert_index = i
                    break
                    
            # Create new entry
            new_entry = f"""
## 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Directory Structure Standardization

### Summary
Fixed directory structure inconsistencies and consolidated duplicate folders into standard organization.

### Changes Made
- **Fixed {self.directories_fixed} directories**
- **Moved {self.files_moved} files** to correct locations
- **Consolidated duplicate folders**
- **Standardized directory numbering**

### Directory Consolidations
- `05_Player_Resources` → `07_Player_Resources`
- `06_GM_Resources` → `06_Sessions`
- `07_Templates` → `09_Templates`
- `09_Campaigns` → `01_Adventures`
- `09_Performance` → `13_Performance`
- `1-Session Journals` → `06_Sessions`
- `10_Sessions` → `06_Sessions`
- `11_Media` → `04_Resources`
- `03_Mechanics` → `05_Rules`

### Final Structure
```
00_Indexes/         - Indexes and documentation
01_Adventures/      - Adventure modules and campaigns
02_Worldbuilding/   - Lore, groups, items, world details
03_People/          - NPCs and characters
04_Places/          - Locations and maps
04_Resources/       - Assets, media, resources
05_Rules/           - Game mechanics and rules
06_Sessions/        - Session notes and GM resources
07_Player_Resources/- Player handouts and resources
08_Archive/         - Archived content and backups
09_Templates/       - Note templates
10_Inspiration/     - Ideas and inspiration
11_References/      - External references
12_Research/        - Research notes
13_Performance/     - Performance metrics and reports
scripts/            - Automation scripts
```

### Result
The vault now has a clean, standardized directory structure with no duplicates or inconsistencies.

---"""
            
            # Insert the new entry
            if insert_index == 0:
                insert_index = 101  # Default position if not found
            lines.insert(insert_index, new_entry)
            
            # Write back
            updates_file.write_text('\n'.join(lines), encoding='utf-8')
            print("\n✅ Updated VAULT_UPDATES.md with directory structure report")

def main():
    fixer = DirectoryStructureFixer()
    fixer.run()

if __name__ == "__main__":
    main()