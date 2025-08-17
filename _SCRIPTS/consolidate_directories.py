#!/usr/bin/env python3
"""
Consolidate duplicate numbered directories and deduplicate content
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime


class DirectoryConsolidator:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.moves = []
        self.duplicates_found = []
        
    def consolidate_directories(self):
        """Main consolidation process"""
        print("🔧 Starting Directory Consolidation")
        print("="*60)
        
        # Define consolidation plan
        consolidations = [
            # Templates go to 07_Templates
            ("05_Templates", "07_Templates", "Templates"),
            
            # Player resources go to 05_Player_Resources  
            ("07_Player_Resources", "05_Player_Resources", "Player Resources"),
            
            # GM Resources stay in 06
            ("06_Session_Management", "06_GM_Resources", "GM Resources"),
            
            # Community/Homebrew go to 10_Homebrew
            ("10_Community", "10_Homebrew", "Homebrew"),
            
            # Media/Professional go to 11_Media
            ("11_Professional", "11_Media", "Media"),
            
            # Archive consolidation - 12_Archive content goes to 08_Archive
            ("12_Archive", "08_Archive", "Archive"),
            
            # Research consolidation - 08_Research goes to 12_Research (bigger dir)
            ("08_Research", "12_Research", "Research")
        ]
        
        for source, target, desc in consolidations:
            self.merge_directories(source, target, desc)
            
        # After consolidation, deduplicate within each directory
        self.deduplicate_consolidated_dirs()
        
        # Clean up empty directories
        self.remove_empty_dirs()
        
        return self.generate_report()
    
    def merge_directories(self, source_name: str, target_name: str, description: str):
        """Merge source directory into target"""
        source = self.vault_path / source_name
        target = self.vault_path / target_name
        
        if not source.exists():
            print(f"  ⚠️ {source_name} doesn't exist, skipping")
            return
            
        if not target.exists():
            print(f"  📁 Creating {target_name}")
            target.mkdir(parents=True, exist_ok=True)
            
        # Count files
        source_files = list(source.rglob("*"))
        file_count = sum(1 for f in source_files if f.is_file())
        
        if file_count == 0:
            print(f"  📭 {source_name} is empty, will remove")
            self.moves.append((source_name, "DELETED", "Empty directory"))
            return
            
        print(f"\n📦 Consolidating {description}: {source_name} → {target_name}")
        print(f"  Files to move: {file_count}")
        
        # Move all content
        moved = 0
        for item in source_files:
            if item.is_file():
                # Calculate relative path
                rel_path = item.relative_to(source)
                new_path = target / rel_path
                
                # Create parent directories
                new_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Check for duplicates
                if new_path.exists():
                    if self.files_identical(item, new_path):
                        print(f"    🔄 Duplicate found: {rel_path}")
                        self.duplicates_found.append(str(rel_path))
                        item.unlink()  # Remove duplicate
                    else:
                        # Files differ, rename
                        new_name = new_path.stem + "_merged" + new_path.suffix
                        new_path = new_path.parent / new_name
                        shutil.move(str(item), str(new_path))
                        moved += 1
                        print(f"    ➡️ Renamed: {rel_path} → {new_name}")
                else:
                    shutil.move(str(item), str(new_path))
                    moved += 1
                    
        print(f"  ✅ Moved {moved} files, skipped {len(self.duplicates_found)} duplicates")
        self.moves.append((source_name, target_name, f"{moved} files"))
        
    def files_identical(self, file1: Path, file2: Path) -> bool:
        """Check if two files are identical"""
        try:
            # Quick size check
            if file1.stat().st_size != file2.stat().st_size:
                return False
                
            # Content hash check
            hash1 = hashlib.md5(file1.read_bytes()).hexdigest()
            hash2 = hashlib.md5(file2.read_bytes()).hexdigest()
            return hash1 == hash2
        except:
            return False
            
    def deduplicate_consolidated_dirs(self):
        """Remove duplicates within consolidated directories"""
        print("\n🔍 Deduplicating consolidated directories...")
        
        target_dirs = [
            "05_Player_Resources",
            "06_GM_Resources", 
            "07_Templates",
            "08_Archive",
            "10_Homebrew",
            "11_Media",
            "12_Research"
        ]
        
        total_removed = 0
        
        for dir_name in target_dirs:
            dir_path = self.vault_path / dir_name
            if not dir_path.exists():
                continue
                
            # Find all files
            files = list(dir_path.rglob("*.md"))
            
            # Group by content hash
            hash_map = {}
            for file in files:
                try:
                    content = file.read_text(encoding='utf-8')
                    # Normalize for comparison
                    normalized = ' '.join(content.split())
                    content_hash = hashlib.md5(normalized.encode()).hexdigest()
                    
                    if content_hash not in hash_map:
                        hash_map[content_hash] = []
                    hash_map[content_hash].append(file)
                except:
                    continue
                    
            # Remove duplicates (keep first occurrence)
            for content_hash, file_list in hash_map.items():
                if len(file_list) > 1:
                    # Keep the shortest filename (usually the original)
                    file_list.sort(key=lambda x: len(str(x)))
                    keep = file_list[0]
                    
                    for duplicate in file_list[1:]:
                        print(f"    🗑️ Removing duplicate: {duplicate.relative_to(self.vault_path)}")
                        duplicate.unlink()
                        total_removed += 1
                        
        print(f"  ✅ Removed {total_removed} duplicate files")
        
    def remove_empty_dirs(self):
        """Remove empty directories after consolidation"""
        print("\n🧹 Cleaning up empty directories...")
        
        dirs_to_check = [
            "05_Templates",
            "06_Session_Management",
            "07_Player_Resources", 
            "10_Community",
            "11_Professional",
            "12_Archive",
            "08_Research"
        ]
        
        removed = []
        for dir_name in dirs_to_check:
            dir_path = self.vault_path / dir_name
            if dir_path.exists():
                # Check if truly empty (no files in any subdirs)
                files = list(dir_path.rglob("*"))
                if not any(f.is_file() for f in files):
                    shutil.rmtree(dir_path)
                    removed.append(dir_name)
                    print(f"  🗑️ Removed empty directory: {dir_name}")
                    
        print(f"  ✅ Removed {len(removed)} empty directories")
        
    def generate_report(self) -> Dict:
        """Generate consolidation report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "consolidations": self.moves,
            "duplicates_removed": len(self.duplicates_found),
            "duplicate_files": self.duplicates_found
        }
        
        # Save report
        report_path = self.vault_path / "reports" / f"consolidation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print("\n" + "="*60)
        print("📊 CONSOLIDATION COMPLETE")
        print("="*60)
        print(f"Directories consolidated: {len([m for m in self.moves if m[1] != 'DELETED'])}")
        print(f"Empty directories removed: {len([m for m in self.moves if m[1] == 'DELETED'])}")
        print(f"Duplicate files removed: {len(self.duplicates_found)}")
        print(f"\n📄 Report saved to: {report_path}")
        
        return report


def main():
    consolidator = DirectoryConsolidator()
    consolidator.consolidate_directories()


if __name__ == "__main__":
    main()