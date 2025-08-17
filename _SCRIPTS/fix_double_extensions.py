#!/usr/bin/env python3
"""
Step 9: Fix Double Extensions
Removes .md.md, .png.md and similar double extension files
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

class DoubleExtensionFixer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.archive_dir = self.vault_path / "08_Archive" / "double_extensions"
        self.double_extension_files = []
        self.fixed_count = 0
        self.archived_count = 0
        
    def find_double_extensions(self):
        """Find all files with double extensions"""
        print("🔍 Searching for double extension files...")
        
        patterns = [
            (r"\.md\.md$", ".md.md files"),
            (r"\.png\.md$", ".png.md files"),
            (r"\.jpg\.md$", ".jpg.md files"),
            (r"\.jpeg\.md$", ".jpeg.md files"),
            (r"\.svg\.md$", ".svg.md files"),
            (r"\.gif\.md$", ".gif.md files"),
            (r"\.pdf\.md$", ".pdf.md files"),
            (r"\.json\.md$", ".json.md files"),
            (r"\.txt\.md$", ".txt.md files"),
            (r"\.csv\.md$", ".csv.md files"),
            (r"\.xml\.md$", ".xml.md files"),
            (r"\.html\.md$", ".html.md files"),
        ]
        
        categories = {}
        
        for pattern, category in patterns:
            files = list(self.vault_path.glob(f"**/*{pattern[1:-1]}"))
            
            # Filter out system directories
            files = [f for f in files 
                    if not any(skip in str(f) for skip in ['.obsidian', '.git', '_SCRIPTS', '09_Performance', '08_Archive'])]
            
            if files:
                self.double_extension_files.extend(files)
                categories[category] = len(files)
                
        # Remove duplicates
        self.double_extension_files = list(set(self.double_extension_files))
        
        print(f"  ✓ Found {len(self.double_extension_files)} double extension files")
        
        # Show breakdown
        if categories:
            print("\n  Types found:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"    - {category}: {count}")
                
    def determine_action(self, file_path):
        """Determine whether to fix or archive the file"""
        filename = file_path.name
        
        # For .md.md files, we can safely rename
        if filename.endswith('.md.md'):
            return 'rename'
            
        # For image/document extensions, these shouldn't be .md files
        if any(filename.endswith(ext) for ext in ['.png.md', '.jpg.md', '.jpeg.md', '.svg.md', '.gif.md', '.pdf.md']):
            # Check if the file has markdown content or is just a reference
            try:
                content = file_path.read_text(encoding='utf-8')
                # If it has substantial markdown content, it might be intentional
                if len(content) > 100 and '#' in content:
                    return 'keep'
                else:
                    return 'archive'
            except:
                return 'archive'
                
        # For other double extensions, archive to be safe
        return 'archive'
        
    def fix_files(self):
        """Fix or archive double extension files"""
        if not self.double_extension_files:
            print("\n✅ No double extension files found")
            return
            
        print(f"\n🔧 Processing {len(self.double_extension_files)} double extension files...")
        
        # Create archive directory if needed
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        renamed = []
        archived = []
        kept = []
        
        for file_path in self.double_extension_files:
            action = self.determine_action(file_path)
            
            try:
                if action == 'rename':
                    # Remove one .md extension
                    new_name = file_path.stem  # Removes last .md
                    new_path = file_path.parent / f"{new_name}"
                    
                    # Check if target exists
                    if not new_path.exists():
                        file_path.rename(new_path)
                        renamed.append((file_path, new_path))
                        self.fixed_count += 1
                    else:
                        # Archive if can't rename
                        self.archive_file(file_path)
                        archived.append(file_path)
                        
                elif action == 'archive':
                    self.archive_file(file_path)
                    archived.append(file_path)
                    
                elif action == 'keep':
                    kept.append(file_path)
                    
            except Exception as e:
                print(f"  Error processing {file_path.name}: {e}")
                
        print(f"\n  Results:")
        print(f"    ✓ Renamed: {len(renamed)} files")
        print(f"    📦 Archived: {len(archived)} files")
        print(f"    ✅ Kept: {len(kept)} files")
        
    def archive_file(self, file_path):
        """Archive a single file"""
        relative_path = file_path.relative_to(self.vault_path)
        target_path = self.archive_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(file_path), str(target_path))
        self.archived_count += 1
        
    def generate_report(self):
        """Generate double extension fix report"""
        report = f"""# Double Extension Fix Report - Step 9/100

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Files Processed**: {len(self.double_extension_files)}
**Files Fixed**: {self.fixed_count}
**Files Archived**: {self.archived_count}

## 📊 Summary

- **Double Extensions Found**: {len(self.double_extension_files)}
- **Files Renamed**: {self.fixed_count}
- **Files Archived**: {self.archived_count}
- **Archive Location**: `08_Archive/double_extensions/`

## 🔧 Actions Taken

### Files Renamed:
- .md.md → .md (removed duplicate extension)

### Files Archived:
- .png.md files (image references)
- .jpg.md files (image references)
- .svg.md files (image references)
- .pdf.md files (document references)
- Other non-markdown double extensions

## 📁 File Types Processed

| Extension | Action | Reason |
|-----------|--------|--------|
| .md.md | Renamed | Duplicate markdown extension |
| .png.md | Archived | Image file incorrectly as markdown |
| .jpg.md | Archived | Image file incorrectly as markdown |
| .svg.md | Archived | Image file incorrectly as markdown |
| .pdf.md | Archived | PDF file incorrectly as markdown |
| .json.md | Archived | Data file incorrectly as markdown |

## 🔄 Recovery

Archived files can be recovered from:
`08_Archive/double_extensions/`

## ✅ Vault Improvement

- Cleaner file structure
- Correct file extensions
- No more confusion with double extensions
- Proper file type identification

## 📋 Next Steps

Ready to proceed to Step 10: Directory Cleanup

---
*Double extension fix complete.*
"""
        
        report_path = self.vault_path / "09_Performance" / f"double_extension_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
    def run(self):
        """Execute the fix process"""
        print("=" * 60)
        print("🔧 FIX DOUBLE EXTENSIONS (Step 9/100)")
        print("=" * 60)
        
        self.find_double_extensions()
        self.fix_files()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ FIX COMPLETE")
        print(f"   Files Fixed: {self.fixed_count}")
        print(f"   Files Archived: {self.archived_count}")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    fixer = DoubleExtensionFixer(vault_path)
    fixer.run()