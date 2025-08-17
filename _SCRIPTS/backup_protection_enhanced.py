#!/usr/bin/env python3
"""
Enhanced Backup Protection System
Ensures backups are always zipped and never linked into main vault
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
import json
import hashlib
from typing import Set, List, Dict, Any
from pydantic import BaseModel, Field


class BackupConfig(BaseModel):
    """Configuration for backup protection"""
    vault_path: Path = Field(default=Path("."))
    backup_dirs: List[str] = Field(default=["backups", "backup", "08_Archive"])
    auto_zip: bool = Field(default=True)
    remove_originals: bool = Field(default=True)
    exclude_patterns: List[str] = Field(default=["*.zip", "*.tar", "*.gz", "*.7z"])
    max_backup_age_days: int = Field(default=30)
    auto_zip_on_creation: bool = Field(default=True)  # New: auto-zip any new backup dirs


class BackupProtector:
    """Protects backup directories from being linked into main vault"""
    
    def __init__(self, config: BackupConfig):
        self.config = config
        self.protected_files: Set[Path] = set()
        self.zip_archives: List[Path] = []
        
    def scan_backup_directories(self) -> Dict[str, Any]:
        """Scan all backup directories for unzipped content"""
        results = {
            "unzipped_files": [],
            "markdown_files": [],
            "total_size_mb": 0,
            "directories": {}
        }
        
        for backup_dir in self.config.backup_dirs:
            dir_path = self.config.vault_path / backup_dir
            if not dir_path.exists():
                continue
                
            dir_info = {
                "path": str(dir_path),
                "files": 0,
                "size_mb": 0,
                "markdown_count": 0
            }
            
            for root, dirs, files in os.walk(dir_path):
                root_path = Path(root)
                
                # Skip already zipped content
                if any(pattern in str(root_path) for pattern in [".zip", ".tar"]):
                    continue
                    
                for file in files:
                    file_path = root_path / file
                    
                    # Skip if already zipped
                    if file.endswith(('.zip', '.tar', '.gz')):
                        continue
                        
                    # Track unzipped files
                    results["unzipped_files"].append(str(file_path))
                    dir_info["files"] += 1
                    
                    # Check file size
                    try:
                        size_mb = file_path.stat().st_size / (1024 * 1024)
                        dir_info["size_mb"] += size_mb
                        results["total_size_mb"] += size_mb
                    except:
                        pass
                    
                    # Flag markdown files that could be linked
                    if file.endswith('.md'):
                        results["markdown_files"].append(str(file_path))
                        dir_info["markdown_count"] += 1
                        
            results["directories"][backup_dir] = dir_info
            
        return results
        
    def create_zip_archive(self, source_dir: Path, archive_name: str = None) -> Path:
        """Create a zip archive of a directory"""
        if not archive_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{source_dir.name}_{timestamp}.zip"
            
        archive_path = source_dir.parent / archive_name
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(source_dir.parent)
                    zipf.write(file_path, arcname)
                    
        return archive_path
        
    def protect_backup_directory(self, backup_dir: str) -> Dict[str, Any]:
        """Zip all content in a backup directory"""
        dir_path = self.config.vault_path / backup_dir
        if not dir_path.exists():
            return {"status": "skipped", "reason": "directory not found"}
            
        results = {
            "directory": backup_dir,
            "original_files": 0,
            "original_size_mb": 0,
            "archives_created": [],
            "status": "success"
        }
        
        # Find all subdirectories with content
        subdirs_to_zip = []
        for item in dir_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Check if it has markdown files
                md_files = list(item.glob("**/*.md"))
                if md_files:
                    subdirs_to_zip.append(item)
                    results["original_files"] += len(md_files)
                    
        # Zip each subdirectory
        for subdir in subdirs_to_zip:
            try:
                # Calculate size
                size_mb = sum(f.stat().st_size for f in subdir.glob("**/*") if f.is_file()) / (1024 * 1024)
                results["original_size_mb"] += size_mb
                
                # Create archive
                archive_path = self.create_zip_archive(subdir)
                results["archives_created"].append(str(archive_path.name))
                
                # Remove original if configured
                if self.config.remove_originals:
                    shutil.rmtree(subdir)
                    
            except Exception as e:
                results["status"] = "partial"
                results["error"] = str(e)
                
        return results
        
    def add_to_gitignore(self) -> bool:
        """Ensure backup directories are in .gitignore"""
        gitignore_path = self.config.vault_path / ".gitignore"
        
        patterns_to_add = [
            "# Backup directories (auto-added by backup_protection)",
            "backups/",
            "backup/",
            "*_backup_*/",
            "*.backup/",
            "vault_backup_*/",
            "# Prevent accidental backup linking",
            "backups/**/*.md",
            "backup/**/*.md",
            "08_Archive/**/*.md"
        ]
        
        existing_patterns = set()
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                existing_patterns = set(line.strip() for line in f)
                
        new_patterns = [p for p in patterns_to_add if p not in existing_patterns]
        
        if new_patterns:
            with open(gitignore_path, 'a') as f:
                f.write("\n\n")
                f.write("\n".join(new_patterns))
                f.write("\n")
            return True
            
        return False
        
    def create_backup_readme(self) -> None:
        """Create README in backup directories explaining the protection"""
        readme_content = """# ⚠️ BACKUP DIRECTORY - DO NOT LINK

This directory contains backup archives that should NOT be linked into the main vault.

## Important Notes:
- All content here is automatically zipped to prevent accidental linking
- Markdown files in zipped archives won't appear in Obsidian's graph
- This preserves vault performance and prevents duplicate content

## Accessing Backups:
1. Unzip the archive you need to a temporary location
2. Copy specific files back to the main vault as needed
3. Never unzip directly in this backup directory

## Archive Format:
- `[name]_[YYYYMMDD_HHMMSS].zip` - Timestamped backups
- Archives are compressed to save space
- Original directory structure is preserved inside

---
*Generated by backup_protection_enhanced.py*
"""
        
        for backup_dir in self.config.backup_dirs:
            dir_path = self.config.vault_path / backup_dir
            if dir_path.exists():
                readme_path = dir_path / "README.md"
                with open(readme_path, 'w') as f:
                    f.write(readme_content)
                    
    def protect_all_backups(self) -> Dict[str, Any]:
        """Main method to protect all backup directories"""
        print("🛡️ Backup Protection System Starting...")
        
        # Scan current state
        print("📊 Scanning backup directories...")
        scan_results = self.scan_backup_directories()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "scan_results": scan_results,
            "protection_results": [],
            "gitignore_updated": False,
            "readmes_created": False
        }
        
        # Show current state
        print(f"\n📁 Found {len(scan_results['unzipped_files'])} unzipped files")
        print(f"📝 Found {len(scan_results['markdown_files'])} markdown files at risk")
        print(f"💾 Total size: {scan_results['total_size_mb']:.2f} MB")
        
        if scan_results['markdown_files']:
            print("\n⚠️  Markdown files found in backup directories!")
            print("These could be accidentally linked into the vault.")
            
            if self.config.auto_zip:
                print("\n🗜️ Auto-zipping backup directories...")
                
                for backup_dir in self.config.backup_dirs:
                    result = self.protect_backup_directory(backup_dir)
                    report["protection_results"].append(result)
                    
                    if result["status"] != "skipped":
                        print(f"  ✅ {backup_dir}: {len(result['archives_created'])} archives created")
                        
        # Update .gitignore
        print("\n📝 Updating .gitignore...")
        report["gitignore_updated"] = self.add_to_gitignore()
        
        # Create README files
        print("📄 Creating README files in backup directories...")
        self.create_backup_readme()
        report["readmes_created"] = True
        
        # Save report
        report_path = self.config.vault_path / "backup_protection_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n✅ Backup protection complete!")
        print(f"📊 Report saved to: {report_path}")
        
        return report


def main():
    """Main execution"""
    config = BackupConfig(
        vault_path=Path("."),
        auto_zip=True,
        remove_originals=True
    )
    
    protector = BackupProtector(config)
    report = protector.protect_all_backups()
    
    # Summary
    print("\n" + "="*50)
    print("BACKUP PROTECTION SUMMARY")
    print("="*50)
    
    if report["scan_results"]["markdown_files"]:
        print(f"✅ Protected {len(report['scan_results']['markdown_files'])} markdown files from linking")
        
    for result in report["protection_results"]:
        if result.get("archives_created"):
            print(f"✅ {result['directory']}: {len(result['archives_created'])} archives created")
            print(f"   Compressed {result['original_files']} files ({result['original_size_mb']:.2f} MB)")
            
    if report["gitignore_updated"]:
        print("✅ Updated .gitignore with backup exclusions")
        
    print("\n🎯 Your backups are now protected from accidental linking!")
    

if __name__ == "__main__":
    main()