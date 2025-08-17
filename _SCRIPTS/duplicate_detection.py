#!/usr/bin/env python3
"""
Step 4: Duplicate Detection
Finds true duplicates by comparing content, not just names
"""

import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class DuplicateDetector:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.file_hashes = defaultdict(list)
        self.name_duplicates = defaultdict(list)
        self.stats = {
            "files_scanned": 0,
            "content_duplicates": 0,
            "name_duplicates": 0,
            "total_duplicate_size": 0
        }
        
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of file content"""
        try:
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except:
            return None
            
    def scan_for_content_duplicates(self):
        """Find files with identical content"""
        print("\n🔍 Scanning for content duplicates...")
        
        files_to_check = list(self.vault_path.glob("**/*.md"))
        files_to_check = [f for f in files_to_check 
                         if not any(skip in str(f) for skip in ['.obsidian', '.git', '_SCRIPTS', '09_Performance'])]
        
        total = len(files_to_check)
        for i, file_path in enumerate(files_to_check):
            if i % 1000 == 0:
                print(f"  Progress: {i}/{total} files...")
                
            file_hash = self.calculate_file_hash(file_path)
            if file_hash:
                self.file_hashes[file_hash].append(file_path)
                self.stats["files_scanned"] += 1
                
        # Count duplicates
        for hash_value, files in self.file_hashes.items():
            if len(files) > 1:
                self.stats["content_duplicates"] += len(files) - 1
                for f in files[1:]:
                    self.stats["total_duplicate_size"] += f.stat().st_size
                    
        print(f"  ✓ Found {self.stats['content_duplicates']} content duplicates")
        
    def scan_for_name_duplicates(self):
        """Find files with similar names"""
        print("\n📝 Scanning for name duplicates...")
        
        for file_path in self.vault_path.glob("**/*.md"):
            if any(skip in str(file_path) for skip in ['.obsidian', '.git', '_SCRIPTS']):
                continue
                
            base_name = file_path.stem.lower()
            # Remove common suffixes that indicate duplicates
            for suffix in ['_1', '_2', '_copy', '_duplicate', '_backup', '_old', '_new']:
                if base_name.endswith(suffix):
                    base_name = base_name[:-len(suffix)]
                    
            self.name_duplicates[base_name].append(file_path)
            
        # Count name duplicates
        for name, files in self.name_duplicates.items():
            if len(files) > 1:
                self.stats["name_duplicates"] += len(files) - 1
                
        print(f"  ✓ Found {self.stats['name_duplicates']} potential name duplicates")
        
    def identify_safe_duplicates(self):
        """Identify duplicates that are safe to remove"""
        safe_to_remove = []
        
        for hash_value, files in self.file_hashes.items():
            if len(files) > 1:
                # Sort by path depth (keep files in main directories)
                sorted_files = sorted(files, key=lambda x: len(x.parts))
                
                # Keep the first one, mark others for removal
                for duplicate in sorted_files[1:]:
                    # Don't remove from critical directories
                    if not any(critical in str(duplicate) for critical in 
                              ['01_Adventures/Campaigns', '06_Sessions', 'Aquabyssos', 'Aethermoor']):
                        safe_to_remove.append(duplicate)
                        
        return safe_to_remove
        
    def generate_report(self):
        """Generate duplicate detection report"""
        report = f"""# Duplicate Detection Report - Step 4/100

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Vault Path**: {self.vault_path}

## 📊 Statistics

- **Files Scanned**: {self.stats['files_scanned']:,}
- **Content Duplicates**: {self.stats['content_duplicates']:,}
- **Name Duplicates**: {self.stats['name_duplicates']:,}
- **Wasted Space**: {self.stats['total_duplicate_size'] / 1024 / 1024:.2f} MB

## 🔄 Content Duplicates (Identical Files)

"""
        
        # Show top duplicate groups
        duplicate_groups = [(h, f) for h, f in self.file_hashes.items() if len(f) > 1]
        duplicate_groups.sort(key=lambda x: len(x[1]), reverse=True)
        
        for i, (hash_val, files) in enumerate(duplicate_groups[:10]):
            report += f"\n### Duplicate Group {i+1}\n"
            report += f"**{len(files)} identical files:**\n\n"
            
            for file_path in files[:5]:
                rel_path = file_path.relative_to(self.vault_path)
                size = file_path.stat().st_size
                report += f"- `{rel_path}` ({size} bytes)\n"
                
            if len(files) > 5:
                report += f"- *(and {len(files) - 5} more...)*\n"
                
        if len(duplicate_groups) > 10:
            report += f"\n*{len(duplicate_groups) - 10} more duplicate groups found.*\n"
            
        report += f"""

## 📝 Name Duplicates (Similar Names)

"""
        
        # Show files with similar names
        name_groups = [(n, f) for n, f in self.name_duplicates.items() if len(f) > 1]
        name_groups.sort(key=lambda x: len(x[1]), reverse=True)
        
        for i, (name, files) in enumerate(name_groups[:10]):
            report += f"\n### Similar: {name}\n"
            
            for file_path in files[:3]:
                rel_path = file_path.relative_to(self.vault_path)
                report += f"- `{rel_path}`\n"
                
            if len(files) > 3:
                report += f"- *(and {len(files) - 3} more...)*\n"
                
        report += f"""

## 🎯 Safe Removal Candidates

Based on analysis, the following types of duplicates could be safely archived:

1. Files in archive folders that exist elsewhere
2. Files with _copy, _backup, _old suffixes
3. Identical files where one is in a deeper subdirectory
4. Test files and temporary files

## ⚠️ Protected Content

The following will NOT be touched:
- ✅ Campaign files in 01_Adventures/Campaigns
- ✅ Session files in 06_Sessions
- ✅ Aquabyssos campaign content
- ✅ Aethermoor campaign content

## 📋 Recommendations

1. Archive obvious duplicates (_copy, _backup files)
2. Review content duplicates for consolidation
3. Check name duplicates for potential merging
4. Keep original files in primary locations

## ✅ Next Steps

Ready to proceed to Step 5: Empty File Scan

---
*Analysis complete. No files were modified.*
"""
        
        # Save safe removal candidates list
        safe_list = self.identify_safe_duplicates()
        if safe_list:
            safe_report = "# Safe Duplicate Removal List\n\n"
            for file_path in safe_list[:100]:
                safe_report += f"- {file_path.relative_to(self.vault_path)}\n"
                
            safe_path = self.vault_path / "09_Performance" / f"safe_duplicates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            safe_path.write_text(safe_report, encoding='utf-8')
        
        report_path = self.vault_path / "09_Performance" / f"duplicate_detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
    def run(self):
        """Execute the duplicate detection"""
        print("=" * 60)
        print("🔍 DUPLICATE DETECTION (Step 4/100)")
        print("=" * 60)
        
        self.scan_for_content_duplicates()
        self.scan_for_name_duplicates()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ DETECTION COMPLETE")
        print(f"   Files Scanned: {self.stats['files_scanned']:,}")
        print(f"   Content Duplicates: {self.stats['content_duplicates']:,}")
        print(f"   Name Duplicates: {self.stats['name_duplicates']:,}")
        print(f"   Wasted Space: {self.stats['total_duplicate_size'] / 1024 / 1024:.2f} MB")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    detector = DuplicateDetector(vault_path)
    detector.run()