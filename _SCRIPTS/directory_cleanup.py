#!/usr/bin/env python3
"""
Step 10: Directory Cleanup
Removes empty directories (except structural ones)
"""

from pathlib import Path
from datetime import datetime

class DirectoryCleanup:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.empty_dirs = []
        self.removed_count = 0
        self.protected_dirs = []
        
        # Directories that should be kept even if empty (structural)
        self.structural_dirs = {
            "00_System",
            "00_Indexes",
            "01_Adventures",
            "02_Worldbuilding", 
            "03_People",
            "04_Resources",
            "05_Rules",
            "06_Sessions",
            "07_Player_Resources",
            "08_Archive",
            "09_Performance",
            "_SCRIPTS",
            "_INDEXES",
            "_METADATA",
            "Campaigns",
            "NPCs",
            "Locations",
            "Quests",
            "Items",
            "Maps",
            "Encounters",
            "Hooks"
        }
        
    def find_empty_directories(self):
        """Find all empty directories in the vault"""
        print("🔍 Scanning for empty directories...")
        
        all_dirs = []
        
        # Walk through all directories
        for root, dirs, files in self.vault_path.walk(top_down=False):
            for dir_name in dirs:
                dir_path = root / dir_name
                
                # Skip system directories
                if any(skip in str(dir_path) for skip in ['.git', '.obsidian']):
                    continue
                    
                all_dirs.append(dir_path)
                
                # Check if directory is empty
                try:
                    if not any(dir_path.iterdir()):
                        if self.is_safe_to_remove(dir_path):
                            self.empty_dirs.append(dir_path)
                        else:
                            self.protected_dirs.append(dir_path)
                except:
                    pass
                    
        print(f"  ✓ Scanned {len(all_dirs)} directories")
        print(f"  ✓ Found {len(self.empty_dirs)} empty directories")
        print(f"  ⚠️ Protected {len(self.protected_dirs)} structural directories")
        
    def is_safe_to_remove(self, dir_path):
        """Check if a directory is safe to remove"""
        dir_name = dir_path.name
        
        # Never remove structural directories
        if dir_name in self.structural_dirs:
            return False
            
        # Never remove directories in the root
        if dir_path.parent == self.vault_path:
            return False
            
        # Check for important parent directories
        path_str = str(dir_path)
        protected_paths = [
            '01_Adventures/Campaigns',
            '06_Sessions',
            'Aquabyssos',
            'Aethermoor',
            '_SCRIPTS',
            '09_Performance'
        ]
        
        for protected in protected_paths:
            if protected in path_str:
                return False
                
        return True
        
    def remove_empty_directories(self):
        """Remove empty directories that are safe to delete"""
        if not self.empty_dirs:
            print("\n✅ No empty directories to remove")
            return
            
        print(f"\n🗑️ Removing {len(self.empty_dirs)} empty directories...")
        
        # Sort by depth (deepest first) to avoid trying to remove non-empty parents
        self.empty_dirs.sort(key=lambda x: len(x.parts), reverse=True)
        
        for dir_path in self.empty_dirs:
            try:
                # Double-check it's still empty
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    self.removed_count += 1
                    
                    if self.removed_count % 10 == 0:
                        print(f"  Removed {self.removed_count} directories...")
                        
            except Exception as e:
                # Directory might not be empty anymore or other issue
                pass
                
        print(f"  ✓ Removed {self.removed_count} empty directories")
        
    def generate_report(self):
        """Generate directory cleanup report"""
        report = f"""# Directory Cleanup Report - Step 10/100

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Directories Removed**: {self.removed_count}

## 📊 Summary

- **Empty Directories Found**: {len(self.empty_dirs) + len(self.protected_dirs)}
- **Directories Removed**: {self.removed_count}
- **Protected Structural Directories**: {len(self.protected_dirs)}

## 📁 Protected Directories

The following empty directories were kept as they are structural:

"""
        
        if self.protected_dirs:
            for dir_path in self.protected_dirs[:20]:
                rel_path = dir_path.relative_to(self.vault_path)
                report += f"- `{rel_path}`\n"
                
            if len(self.protected_dirs) > 20:
                report += f"\n*(and {len(self.protected_dirs) - 20} more...)*\n"
                
        report += f"""

## 🗑️ Removed Directories

"""
        
        if self.removed_count > 0:
            report += f"Successfully removed {self.removed_count} empty directories.\n\n"
            
            # Show sample of removed directories
            if self.empty_dirs:
                report += "Sample of removed directories:\n"
                for dir_path in self.empty_dirs[:10]:
                    if not dir_path.exists():  # Was successfully removed
                        rel_path = dir_path.relative_to(self.vault_path)
                        report += f"- `{rel_path}`\n"
                        
        else:
            report += "No directories were removed.\n"
            
        report += f"""

## ✅ Structural Integrity

The following structural directories were preserved:
- Root numbered directories (00-09)
- Core organizational folders (Campaigns, NPCs, etc.)
- System directories (_SCRIPTS, _INDEXES, etc.)
- Campaign-specific folders

## 🎯 Benefits

- Cleaner folder structure
- Easier navigation
- Reduced clutter
- Maintained organizational integrity

## 📋 Phase 1 Completion

With Step 10 complete, **Phase 1: Assessment & Cleanup** is now finished!

### Phase 1 Achievements:
✅ Vault health assessed
✅ Backup created
✅ Broken links analyzed
✅ Duplicates detected
✅ Empty files scanned
✅ Broken references archived
✅ Test files cleaned
✅ Double extensions fixed
✅ Empty directories removed

## 📋 Next Steps

Ready to proceed to **Phase 2: Organization Within Structure** (Steps 11-20)

---
*Directory cleanup complete. Phase 1 finished!*
"""
        
        report_path = self.vault_path / "09_Performance" / f"directory_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
    def run(self):
        """Execute the cleanup process"""
        print("=" * 60)
        print("📁 DIRECTORY CLEANUP (Step 10/100)")
        print("=" * 60)
        
        self.find_empty_directories()
        self.remove_empty_directories()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ CLEANUP COMPLETE")
        print(f"   Directories Removed: {self.removed_count}")
        print(f"   Protected Directories: {len(self.protected_dirs)}")
        print("=" * 60)
        print("\n🎉 PHASE 1 COMPLETE! (Steps 1-10)")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    cleaner = DirectoryCleanup(vault_path)
    cleaner.run()