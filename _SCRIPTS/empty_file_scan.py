#!/usr/bin/env python3
"""
Step 5: Empty File Scan
Identifies stub files under 50 characters
"""

from pathlib import Path
from datetime import datetime
from collections import defaultdict

class EmptyFileScanner:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.empty_files = []  # 0 bytes
        self.tiny_files = []   # 1-10 bytes
        self.stub_files = []   # 11-50 bytes
        self.small_files = []  # 51-100 bytes
        self.stats = defaultdict(int)
        
    def scan_files(self):
        """Scan all files and categorize by size"""
        print("\n📂 Scanning all markdown files...")
        
        files_to_check = list(self.vault_path.glob("**/*.md"))
        files_to_check = [f for f in files_to_check 
                         if not any(skip in str(f) for skip in ['.obsidian', '.git', '_SCRIPTS', '09_Performance'])]
        
        total = len(files_to_check)
        print(f"  Found {total:,} files to check")
        
        for i, file_path in enumerate(files_to_check):
            if i % 5000 == 0 and i > 0:
                print(f"  Progress: {i}/{total} files...")
                
            try:
                size = file_path.stat().st_size
                self.stats["total_files"] += 1
                
                if size == 0:
                    self.empty_files.append(file_path)
                    self.stats["empty"] += 1
                elif size <= 10:
                    self.tiny_files.append(file_path)
                    self.stats["tiny"] += 1
                elif size <= 50:
                    self.stub_files.append(file_path)
                    self.stats["stub"] += 1
                elif size <= 100:
                    self.small_files.append(file_path)
                    self.stats["small"] += 1
                else:
                    self.stats["normal"] += 1
                    
            except Exception as e:
                self.stats["errors"] += 1
                
        print(f"  ✓ Scanned {total:,} files")
        
    def analyze_stub_content(self):
        """Analyze content of stub files to determine if they're truly empty"""
        print("\n🔍 Analyzing stub file content...")
        
        truly_empty = []
        just_title = []
        minimal_content = []
        
        for file_path in self.stub_files[:100]:  # Sample first 100
            try:
                content = file_path.read_text(encoding='utf-8').strip()
                lines = content.split('\n')
                
                if not content:
                    truly_empty.append(file_path)
                elif len(lines) == 1 and lines[0].startswith('#'):
                    just_title.append(file_path)
                else:
                    minimal_content.append(file_path)
                    
            except:
                pass
                
        return truly_empty, just_title, minimal_content
        
    def check_protected_files(self):
        """Identify which empty files are in protected directories"""
        protected = []
        safe_to_remove = []
        
        all_empty = self.empty_files + self.tiny_files
        
        for file_path in all_empty:
            path_str = str(file_path)
            
            # Check if in protected directory
            if any(protected_dir in path_str for protected_dir in 
                  ['01_Adventures/Campaigns', '06_Sessions', 'Aquabyssos', 'Aethermoor']):
                protected.append(file_path)
            else:
                safe_to_remove.append(file_path)
                
        return protected, safe_to_remove
        
    def generate_report(self):
        """Generate empty file scan report"""
        protected, safe = self.check_protected_files()
        truly_empty, just_title, minimal = self.analyze_stub_content()
        
        report = f"""# Empty File Scan Report - Step 5/100

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Vault Path**: {self.vault_path}

## 📊 File Size Distribution

| Category | Size | Count | Percentage |
|----------|------|-------|------------|
| Empty | 0 bytes | {self.stats['empty']:,} | {self.stats['empty']/max(1,self.stats['total_files'])*100:.1f}% |
| Tiny | 1-10 bytes | {self.stats['tiny']:,} | {self.stats['tiny']/max(1,self.stats['total_files'])*100:.1f}% |
| Stub | 11-50 bytes | {self.stats['stub']:,} | {self.stats['stub']/max(1,self.stats['total_files'])*100:.1f}% |
| Small | 51-100 bytes | {self.stats['small']:,} | {self.stats['small']/max(1,self.stats['total_files'])*100:.1f}% |
| Normal | >100 bytes | {self.stats['normal']:,} | {self.stats['normal']/max(1,self.stats['total_files'])*100:.1f}% |

**Total Files**: {self.stats['total_files']:,}

## 🗑️ Empty Files (0 bytes)

**Found**: {len(self.empty_files)} completely empty files

"""
        
        # Show sample of empty files
        if self.empty_files:
            report += "### Sample Empty Files:\n"
            for file_path in self.empty_files[:10]:
                rel_path = file_path.relative_to(self.vault_path)
                report += f"- `{rel_path}`\n"
                
            if len(self.empty_files) > 10:
                report += f"\n*(and {len(self.empty_files) - 10} more...)*\n"
                
        report += f"""

## 📄 Tiny Files (1-10 bytes)

**Found**: {len(self.tiny_files)} tiny files

"""
        
        if self.tiny_files:
            report += "### Sample Tiny Files:\n"
            for file_path in self.tiny_files[:10]:
                rel_path = file_path.relative_to(self.vault_path)
                try:
                    content = file_path.read_text(encoding='utf-8').strip()
                    report += f"- `{rel_path}` - Content: '{content[:20]}...'\n"
                except:
                    report += f"- `{rel_path}` - (unreadable)\n"
                    
        report += f"""

## 📝 Stub Files (11-50 bytes)

**Found**: {len(self.stub_files)} stub files

### Content Analysis (sample of 100):
- **Truly Empty**: {len(truly_empty)} files
- **Just Title**: {len(just_title)} files  
- **Minimal Content**: {len(minimal)} files

"""
        
        report += f"""

## 🔒 Protection Analysis

### Protected Files (in critical directories):
- **Protected Empty/Tiny Files**: {len(protected)}
- **Safe to Remove**: {len(safe)}

Protected directories:
- ✅ 01_Adventures/Campaigns
- ✅ 06_Sessions
- ✅ Aquabyssos content
- ✅ Aethermoor content

## 🎯 Removal Candidates

Based on analysis, these files are safe to remove:

1. **Completely Empty** (0 bytes): {len([f for f in self.empty_files if f in safe])} files
2. **Effectively Empty** (1-10 bytes): {len([f for f in self.tiny_files if f in safe])} files
3. **Just Titles** (no content): {len([f for f in just_title if f in safe])} files

**Total Safe to Remove**: {len(safe)} files

## ⚠️ Recommendations

1. Remove truly empty files (0 bytes) - no content to lose
2. Review tiny files (1-10 bytes) before removal
3. Keep stub files that might be placeholders
4. Never remove from protected directories
5. Archive instead of delete for safety

## ✅ Next Steps

Ready to proceed to Step 6: Remove Empty Files

This step will safely remove only truly empty files from non-critical directories.

---
*Scan complete. No files were modified.*
"""
        
        # Save list of safe removal candidates
        if safe:
            removal_list = "# Empty Files Safe for Removal\n\n"
            removal_list += f"**Total**: {len(safe)} files\n\n"
            
            for file_path in safe[:200]:
                rel_path = file_path.relative_to(self.vault_path)
                size = file_path.stat().st_size
                removal_list += f"- `{rel_path}` ({size} bytes)\n"
                
            if len(safe) > 200:
                removal_list += f"\n*(and {len(safe) - 200} more...)*\n"
                
            list_path = self.vault_path / "09_Performance" / f"empty_files_removal_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            list_path.write_text(removal_list, encoding='utf-8')
            
        report_path = self.vault_path / "09_Performance" / f"empty_file_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
    def run(self):
        """Execute the empty file scan"""
        print("=" * 60)
        print("📂 EMPTY FILE SCAN (Step 5/100)")
        print("=" * 60)
        
        self.scan_files()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ SCAN COMPLETE")
        print(f"   Empty Files (0 bytes): {self.stats['empty']:,}")
        print(f"   Tiny Files (1-10 bytes): {self.stats['tiny']:,}")
        print(f"   Stub Files (11-50 bytes): {self.stats['stub']:,}")
        print(f"   Small Files (51-100 bytes): {self.stats['small']:,}")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    scanner = EmptyFileScanner(vault_path)
    scanner.run()