#!/usr/bin/env python3
"""
Clean file names that include path patterns
"""

import os
import re
from pathlib import Path

class FileNameCleaner:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.cleaned = 0
        self.deleted = 0
        
    def clean_path_patterns(self):
        """Remove files with path patterns in names"""
        print("🧹 Cleaning files with path patterns in names...")
        
        patterns = [
            r"_03_Mechanics_",
            r"_02_Worldbuilding_", 
            r"_04_Resources_",
            r"_05_Rules_",
            r"_06_Sessions_",
            r"vault_backup_\d+_"
        ]
        
        for pattern in patterns:
            files = list(self.vault_path.glob(f"**/*{pattern.replace('_', '')}*"))
            
            for file_path in files:
                if file_path.is_file():
                    # These are likely duplicates or unnecessary files
                    try:
                        os.remove(file_path)
                        self.deleted += 1
                        print(f"  ✗ Deleted: {file_path.name}")
                    except:
                        pass
                        
    def remove_quick_ref_duplicates(self):
        """Remove Quick_Ref duplicates"""
        print("📋 Removing Quick Reference duplicates...")
        
        quick_ref_dir = self.vault_path / "03_People" / "Quick_Reference"
        if quick_ref_dir.exists():
            for file_path in quick_ref_dir.glob("*_Quick_Ref.md"):
                try:
                    os.remove(file_path)
                    self.deleted += 1
                except:
                    pass
                    
    def clean_portrait_metadata(self):
        """Remove unnecessary portrait metadata files"""
        print("🖼️ Cleaning portrait metadata...")
        
        for file_path in self.vault_path.glob("**/portrait_*_meta.json"):
            try:
                os.remove(file_path)
                self.deleted += 1
            except:
                pass
                
        for file_path in self.vault_path.glob("**/token_*_meta.json"):
            try:
                os.remove(file_path)
                self.deleted += 1
            except:
                pass
                
    def run(self):
        """Execute cleaning"""
        print("=" * 60)
        print("🧹 FILE NAME CLEANER")
        print("=" * 60)
        
        self.clean_path_patterns()
        self.remove_quick_ref_duplicates()
        self.clean_portrait_metadata()
        
        print("\n" + "=" * 60)
        print(f"✅ COMPLETE")
        print(f"   Files Deleted: {self.deleted}")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    cleaner = FileNameCleaner(vault_path)
    cleaner.run()