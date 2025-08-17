#!/usr/bin/env python3
"""
Quick vault reorganizer - focuses on the most critical fixes
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class QuickVaultReorganizer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.files_moved = 0
        self.dirs_removed = 0
        
    def run(self):
        """Main execution"""
        print("=" * 80)
        print("🚀 QUICK VAULT REORGANIZER")
        print("=" * 80)
        
        # Priority 1: Fix the most problematic nested directories
        print("\n🔧 Fixing critical nested directories...")
        self.fix_critical_nesting()
        
        # Priority 2: Remove empty directories
        print("\n🧹 Removing empty directories...")
        self.cleanup_empty()
        
        # Report
        print("\n" + "=" * 80)
        print(f"✅ QUICK FIX COMPLETE")
        print(f"   • Files moved: {self.files_moved}")
        print(f"   • Directories removed: {self.dirs_removed}")
        
    def fix_critical_nesting(self):
        """Fix the most critical nested directory issues"""
        
        # Critical paths to fix
        critical_fixes = [
            ("01_Adventures/02_Worldbuilding", "02_Worldbuilding"),
            ("02_Worldbuilding/Lore/02_Worldbuilding", "02_Worldbuilding/Lore"),
            ("02_Worldbuilding/Lore/01_Adventures", "01_Adventures"),
            ("02_Worldbuilding/Places/02_Worldbuilding", "02_Worldbuilding/Places"),
            ("02_Worldbuilding/Groups/02_Worldbuilding", "02_Worldbuilding/Groups"),
            ("02_Worldbuilding/People/02_Worldbuilding", "02_Worldbuilding/People"),
            ("02_Worldbuilding/People/01_Adventures", "01_Adventures"),
            ("02_Worldbuilding/Items/02_Worldbuilding", "02_Worldbuilding/Items"),
        ]
        
        for source_path, dest_path in critical_fixes:
            source_dir = self.vault_path / source_path
            dest_dir = self.vault_path / dest_path
            
            if not source_dir.exists():
                continue
                
            print(f"   Moving {source_path} → {dest_path}")
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Move all files
            try:
                for item in source_dir.glob("*"):
                    if item.is_file():
                        dest_file = dest_dir / item.name
                        # Handle duplicates
                        if dest_file.exists():
                            base = dest_file.stem
                            ext = dest_file.suffix
                            counter = 1
                            while dest_file.exists():
                                dest_file = dest_dir / f"{base}_{counter}{ext}"
                                counter += 1
                        
                        shutil.move(str(item), str(dest_file))
                        self.files_moved += 1
                        
                # Try to remove empty source directory
                if source_dir.exists() and not any(source_dir.iterdir()):
                    shutil.rmtree(source_dir)
                    self.dirs_removed += 1
                    
            except Exception as e:
                print(f"   ⚠️ Error processing {source_path}: {e}")
                
    def cleanup_empty(self):
        """Remove empty directories"""
        
        # Walk bottom-up
        for root, dirs, files in os.walk(self.vault_path, topdown=False):
            # Skip system directories
            if any(skip in root for skip in ['.git', 'scripts', '.obsidian']):
                continue
                
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                
                try:
                    if dir_path.exists() and not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        self.dirs_removed += 1
                except:
                    pass

def main():
    reorganizer = QuickVaultReorganizer()
    reorganizer.run()

if __name__ == "__main__":
    main()