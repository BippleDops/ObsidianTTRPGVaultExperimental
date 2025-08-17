#!/usr/bin/env python3
"""
Anomalous Files Cleanup Script
Safely removes or archives problematic files following established patterns.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

class AnomalousCleanup:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.archive_path = self.vault_path / '08_Archive' / 'anomalous_cleanup'
        self.removed_count = 0
        self.archived_count = 0
        
        # Patterns to remove (known bad)
        self.remove_patterns = [
            (r'^step_\d+\s*\(phase_\d+\)\.md$', 'step_X (phase_Y) files'),
            (r'\.png\.md$', 'PNG.md files'),
            (r'\.svg\.md$', 'SVG.md files'),
            (r'\.json\.md$', 'JSON.md files'),
            (r'^#.*\.md$', 'files starting with #'),
            (r'^\$.*\.md$', 'files starting with $'),
            (r'^%.*\.md$', 'files starting with %'),
            (r'^<.*\.md$', 'files starting with <'),
            (r'.*\s+\(\w+\)\.md$', 'files with (category) suffix'),
            (r'.*_\d+\.md$', 'duplicate marker files'),
            (r'.*_Quick_Ref\.md$', 'Quick_Ref duplicates')
        ]
        
        # Patterns to archive (might have content)
        self.archive_patterns = [
            (r'.*conflicted.*', 'conflicted files'),
            (r'.*\.bak$', 'backup files'),
            (r'.*\.tmp$', 'temporary files'),
            (r'.*~$', 'editor backup files')
        ]
        
    def scan_for_anomalies(self) -> Tuple[List[Path], List[Path]]:
        """Scan vault for anomalous files"""
        to_remove = []
        to_archive = []
        
        for root, dirs, files in os.walk(self.vault_path):
            # Skip system directories
            if any(skip in root for skip in ['.git', '.obsidian', '08_Archive']):
                continue
                
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                
                # Check remove patterns
                for pattern, description in self.remove_patterns:
                    if re.match(pattern, file):
                        to_remove.append(file_path)
                        break
                        
                # Check archive patterns
                for pattern, description in self.archive_patterns:
                    if re.match(pattern, file):
                        to_archive.append(file_path)
                        break
                        
        return to_remove, to_archive
        
    def verify_safe_to_remove(self, file_path: Path) -> bool:
        """Verify file is safe to remove"""
        try:
            # Check file size (if > 1KB, might have real content)
            if file_path.stat().st_size > 1024:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for substantial content
                lines = [l.strip() for l in content.split('\n') if l.strip()]
                
                # If file has more than frontmatter + title, archive instead
                if len(lines) > 10:
                    return False
                    
                # Check for important keywords
                important = ['quest', 'session', 'player', 'campaign', 'important']
                content_lower = content.lower()
                if any(keyword in content_lower for keyword in important):
                    return False
                    
            return True
            
        except:
            # If can't read, archive to be safe
            return False
            
    def archive_file(self, file_path: Path):
        """Archive a file instead of deleting"""
        timestamp = datetime.now().strftime('%Y%m%d')
        archive_folder = self.archive_path / timestamp
        archive_folder.mkdir(parents=True, exist_ok=True)
        
        relative = file_path.relative_to(self.vault_path)
        dest = archive_folder / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(file_path), str(dest))
        self.archived_count += 1
        
        # Create archive log
        log_path = archive_folder / 'archive_log.txt'
        with open(log_path, 'a') as f:
            f.write(f"{datetime.now()}: Archived {relative}\n")
            
    def remove_file(self, file_path: Path):
        """Remove a file permanently"""
        try:
            os.remove(file_path)
            self.removed_count += 1
        except Exception as e:
            print(f"  Error removing {file_path}: {e}")
            
    def cleanup(self, dry_run: bool = False):
        """Execute cleanup"""
        print("=" * 50)
        print("ANOMALOUS FILES CLEANUP")
        print("=" * 50)
        
        # Scan for anomalies
        print("\nScanning for anomalous files...")
        to_remove, to_archive = self.scan_for_anomalies()
        
        print(f"\nFound:")
        print(f"  Files to remove: {len(to_remove)}")
        print(f"  Files to archive: {len(to_archive)}")
        
        if dry_run:
            print("\n🔍 DRY RUN MODE - No files will be modified")
            
            if to_remove:
                print("\nFiles that would be removed:")
                for f in to_remove[:20]:
                    print(f"  ❌ {f.relative_to(self.vault_path)}")
                if len(to_remove) > 20:
                    print(f"  ... and {len(to_remove) - 20} more")
                    
            if to_archive:
                print("\nFiles that would be archived:")
                for f in to_archive[:20]:
                    print(f"  📦 {f.relative_to(self.vault_path)}")
                if len(to_archive) > 20:
                    print(f"  ... and {len(to_archive) - 20} more")
                    
            return
            
        # Process files for removal
        if to_remove:
            print("\n🗑️  Processing files for removal...")
            for file_path in to_remove:
                if self.verify_safe_to_remove(file_path):
                    self.remove_file(file_path)
                    print(f"  ✓ Removed: {file_path.name}")
                else:
                    # Has content, archive instead
                    self.archive_file(file_path)
                    print(f"  📦 Archived (has content): {file_path.name}")
                    
        # Archive files
        if to_archive:
            print("\n📦 Archiving files...")
            for file_path in to_archive:
                if file_path.exists():  # Might have been removed already
                    self.archive_file(file_path)
                    print(f"  ✓ Archived: {file_path.name}")
                    
        # Summary
        print("\n" + "=" * 50)
        print("CLEANUP COMPLETE")
        print("=" * 50)
        print(f"Files removed: {self.removed_count}")
        print(f"Files archived: {self.archived_count}")
        
        if self.archived_count > 0:
            print(f"\nArchive location: {self.archive_path}")
            
            # Create recovery script
            recovery_script = self.archive_path / 'RECOVERY.py'
            with open(recovery_script, 'w') as f:
                f.write("""#!/usr/bin/env python3
# Recovery script for archived files
import shutil
from pathlib import Path

archive_path = Path(__file__).parent
vault_path = archive_path.parents[2]

def recover_all():
    for timestamp_dir in archive_path.iterdir():
        if timestamp_dir.is_dir() and timestamp_dir.name.isdigit():
            for root, dirs, files in os.walk(timestamp_dir):
                for file in files:
                    if file == 'archive_log.txt' or file == 'RECOVERY.py':
                        continue
                    source = Path(root) / file
                    relative = source.relative_to(timestamp_dir)
                    dest = vault_path / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
                    print(f"Recovered: {relative}")

if __name__ == "__main__":
    response = input("Recover all archived files? (y/n): ")
    if response.lower() == 'y':
        recover_all()
""")
            print(f"Recovery script created: {recovery_script}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean up anomalous files')
    parser.add_argument('--vault',
                       default="/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVaultExperimental",
                       help='Path to vault')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview without making changes')
    
    args = parser.parse_args()
    
    cleanup = AnomalousCleanup(args.vault)
    cleanup.cleanup(dry_run=args.dry_run)

if __name__ == "__main__":
    main()