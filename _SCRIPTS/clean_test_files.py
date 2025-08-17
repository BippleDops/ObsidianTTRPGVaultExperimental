#!/usr/bin/env python3
"""
Step 8: Clean Test Files
Removes obvious test and temporary files
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

class TestFileCleaner:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.archive_dir = self.vault_path / "08_Archive" / "test_files"
        self.test_files = []
        self.archived_count = 0
        
    def identify_test_files(self):
        """Identify test and temporary files"""
        print("🔍 Identifying test and temporary files...")
        
        # Patterns that indicate test/temp files
        test_patterns = [
            (r"^test[_\-]", "Test prefix"),
            (r"^temp[_\-]", "Temp prefix"),
            (r"^tmp[_\-]", "Tmp prefix"),
            (r"^sample[_\-]", "Sample prefix"),
            (r"^example[_\-]", "Example prefix"),
            (r"^demo[_\-]", "Demo prefix"),
            (r"^draft[_\-]", "Draft prefix"),
            (r"_test\.md$", "Test suffix"),
            (r"_temp\.md$", "Temp suffix"),
            (r"_tmp\.md$", "Tmp suffix"),
            (r"_draft\.md$", "Draft suffix"),
            (r"_backup\.md$", "Backup suffix"),
            (r"_old\.md$", "Old suffix"),
            (r"_copy\.md$", "Copy suffix"),
            (r"_duplicate\.md$", "Duplicate suffix"),
            (r"^untitled", "Untitled files"),
            (r"^new_file", "New file defaults"),
            (r"^document_\d+\.md$", "Generic documents"),
            (r"\.backup\.", "Backup files"),
            (r"~$", "Backup files (tilde)"),
        ]
        
        categories = {}
        
        for md_file in self.vault_path.glob("**/*.md"):
            # Skip system folders
            if any(skip in str(md_file) for skip in ['.obsidian', '.git', '_SCRIPTS', '09_Performance', '08_Archive']):
                continue
                
            filename = md_file.name.lower()
            
            # Check each pattern
            for pattern, category in test_patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    # Double-check it's not important content
                    if not self.is_protected_file(md_file):
                        self.test_files.append(md_file)
                        categories[category] = categories.get(category, 0) + 1
                        break
                        
        # Remove duplicates
        self.test_files = list(set(self.test_files))
        
        print(f"  ✓ Found {len(self.test_files)} test/temp files")
        
        # Show breakdown by category
        if categories:
            print("\n  Categories found:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"    - {category}: {count}")
                
    def is_protected_file(self, file_path):
        """Check if file is in a protected location"""
        protected_terms = [
            'Campaigns',
            '06_Sessions', 
            'Aquabyssos',
            'Aethermoor',
            'player',
            'character',
            'important',
            'main'
        ]
        
        path_str = str(file_path).lower()
        for term in protected_terms:
            if term.lower() in path_str:
                return True
                
        # Also check content for important markers
        try:
            content = file_path.read_text(encoding='utf-8')
            if len(content) > 500:  # Substantial content
                return True
            if any(marker in content.lower() for marker in ['campaign', 'session', 'player', 'important']):
                return True
        except:
            pass
            
        return False
        
    def verify_test_files(self):
        """Verify files are truly test/temp before removal"""
        print("\n🔍 Verifying test files...")
        
        verified = []
        excluded = []
        
        for file_path in self.test_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Check various indicators
                if len(content.strip()) < 200:  # Very short
                    verified.append(file_path)
                elif any(indicator in content.lower() for indicator in ['test', 'temp', 'todo', 'placeholder', 'example']):
                    verified.append(file_path)
                elif file_path.stat().st_size < 500:  # Small file
                    verified.append(file_path)
                else:
                    # Might have real content
                    excluded.append(file_path)
                    
            except:
                verified.append(file_path)
                
        # Update list
        self.test_files = verified
        
        print(f"  ✓ Verified {len(self.test_files)} files for cleaning")
        if excluded:
            print(f"  ⚠️ Excluded {len(excluded)} files with potential content")
            
    def archive_test_files(self):
        """Archive test files instead of deleting"""
        if not self.test_files:
            print("\n✅ No test files to clean")
            return
            
        print(f"\n🗑️ Archiving {len(self.test_files)} test/temp files...")
        
        # Create archive directory
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path in self.test_files:
            try:
                # Create target path preserving structure
                relative_path = file_path.relative_to(self.vault_path)
                target_path = self.archive_dir / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file
                shutil.move(str(file_path), str(target_path))
                self.archived_count += 1
                
                if self.archived_count % 50 == 0:
                    print(f"  Archived {self.archived_count} files...")
                    
            except Exception as e:
                print(f"  Error archiving {file_path.name}: {e}")
                
        print(f"  ✓ Archived {self.archived_count} test files")
        
    def generate_report(self):
        """Generate test file cleaning report"""
        report = f"""# Test File Cleaning Report - Step 8/100

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Files Cleaned**: {self.archived_count}
**Archive Location**: 08_Archive/test_files/

## 📊 Summary

- **Test Files Identified**: {len(self.test_files)}
- **Files Archived**: {self.archived_count}
- **Space Freed**: ~{(self.archived_count * 500) / 1024 / 1024:.2f} MB (estimated)

## 🗑️ Types of Files Cleaned

### Prefixes Removed:
- test_*
- temp_*
- tmp_*
- sample_*
- example_*
- demo_*
- draft_*
- untitled*

### Suffixes Removed:
- *_test.md
- *_temp.md
- *_tmp.md
- *_draft.md
- *_backup.md
- *_old.md
- *_copy.md
- *_duplicate.md

## ✅ Protected Content

The following were NOT touched:
- Files in campaign directories
- Files in session directories
- Files with substantial content (>500 bytes)
- Files containing important keywords

## 🔄 Recovery

All archived files can be recovered from:
`08_Archive/test_files/`

Files maintain their original directory structure.

## 📋 Next Steps

Ready to proceed to Step 9: Fix Double Extensions

---
*Cleaning complete. {self.archived_count} test files archived.*
"""
        
        report_path = self.vault_path / "09_Performance" / f"test_file_cleaning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
    def run(self):
        """Execute the cleaning process"""
        print("=" * 60)
        print("🧹 CLEAN TEST FILES (Step 8/100)")
        print("=" * 60)
        
        self.identify_test_files()
        
        if self.test_files:
            self.verify_test_files()
            self.archive_test_files()
            
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ CLEANING COMPLETE")
        print(f"   Files Cleaned: {self.archived_count}")
        print(f"   Location: 08_Archive/test_files/")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    cleaner = TestFileCleaner(vault_path)
    cleaner.run()