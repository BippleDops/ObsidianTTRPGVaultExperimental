#!/usr/bin/env python3
"""
Safe Recovery Script - Recovers deleted files from git history
Only recovers, never deletes
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import json


class SafeRecovery:
    """Safely recover deleted files from git"""
    
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.deleted_files = []
        self.recovery_log = []
        
    def find_deleted_files(self) -> List[str]:
        """Find all deleted files in git status"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.vault_path
            )
            
            for line in result.stdout.split("\n"):
                if line.startswith(" D ") or line.startswith("D  "):
                    file_path = line[3:].strip().strip('"')
                    self.deleted_files.append(file_path)
                        
            return self.deleted_files
        except Exception as e:
            print(f"Error finding deleted files: {e}")
            return []
    
    def categorize_deleted_files(self) -> Dict[str, List[str]]:
        """Categorize deleted files by type and importance"""
        categories = {
            "critical_indexes": [],
            "worldbuilding": [],
            "adventures": [],
            "mechanics": [],
            "resources": [],
            "templates": [],
            "other": []
        }
        
        for file_path in self.deleted_files:
            path_lower = file_path.lower()
            
            # Critical index files
            if "index" in path_lower or "hub" in path_lower:
                categories["critical_indexes"].append(file_path)
            # Worldbuilding content
            elif "02_worldbuilding" in path_lower:
                categories["worldbuilding"].append(file_path)
            # Adventures
            elif "01_adventures" in path_lower:
                categories["adventures"].append(file_path)
            # Mechanics
            elif "03_mechanics" in path_lower:
                categories["mechanics"].append(file_path)
            # Resources
            elif "04_resources" in path_lower or "05_" in path_lower or "06_" in path_lower:
                categories["resources"].append(file_path)
            # Templates
            elif "template" in path_lower or "07_" in path_lower:
                categories["templates"].append(file_path)
            else:
                categories["other"].append(file_path)
                
        return categories
    
    def recover_files(self, file_list: List[str], batch_size: int = 50) -> Dict[str, bool]:
        """Recover specific files from git history in batches"""
        recovery_status = {}
        
        # Process in batches to avoid command line length limits
        for i in range(0, len(file_list), batch_size):
            batch = file_list[i:i+batch_size]
            
            try:
                # Recover from the last commit before deletion
                cmd = ["git", "checkout", "HEAD~1", "--"] + batch
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=self.vault_path
                )
                
                if result.returncode == 0:
                    for file_path in batch:
                        recovery_status[file_path] = True
                        self.recovery_log.append({
                            "file": file_path,
                            "status": "recovered",
                            "timestamp": datetime.now().isoformat()
                        })
                    print(f"✅ Recovered batch of {len(batch)} files")
                else:
                    for file_path in batch:
                        recovery_status[file_path] = False
                    print(f"❌ Failed to recover batch: {result.stderr}")
                    
            except Exception as e:
                for file_path in batch:
                    recovery_status[file_path] = False
                print(f"❌ Error recovering batch: {e}")
                
        return recovery_status
    
    def run_recovery(self) -> Dict[str, Any]:
        """Run the full recovery process"""
        print("🔄 Safe Recovery Process Starting")
        print("="*60)
        
        # Find deleted files
        print("\n📋 Finding deleted files...")
        deleted = self.find_deleted_files()
        print(f"  Found {len(deleted)} deleted files")
        
        # Categorize files
        print("\n📊 Categorizing files...")
        categories = self.categorize_deleted_files()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_deleted": len(deleted),
            "categories": {k: len(v) for k, v in categories.items()},
            "recovery_results": {}
        }
        
        # Show category counts
        for category, files in categories.items():
            if files:
                print(f"  {category}: {len(files)} files")
        
        # Recover critical files first
        if categories["critical_indexes"]:
            print(f"\n🔴 Recovering {len(categories['critical_indexes'])} critical index files...")
            results = self.recover_files(categories["critical_indexes"])
            report["recovery_results"]["critical_indexes"] = sum(1 for v in results.values() if v)
        
        # Recover worldbuilding
        if categories["worldbuilding"]:
            print(f"\n🌍 Recovering {len(categories['worldbuilding'])} worldbuilding files...")
            results = self.recover_files(categories["worldbuilding"])
            report["recovery_results"]["worldbuilding"] = sum(1 for v in results.values() if v)
        
        # Recover adventures
        if categories["adventures"]:
            print(f"\n⚔️ Recovering {len(categories['adventures'])} adventure files...")
            results = self.recover_files(categories["adventures"])
            report["recovery_results"]["adventures"] = sum(1 for v in results.values() if v)
        
        # Recover mechanics
        if categories["mechanics"]:
            print(f"\n⚙️ Recovering {len(categories['mechanics'])} mechanics files...")
            results = self.recover_files(categories["mechanics"])
            report["recovery_results"]["mechanics"] = sum(1 for v in results.values() if v)
        
        # Recover resources
        if categories["resources"]:
            print(f"\n📚 Recovering {len(categories['resources'])} resource files...")
            results = self.recover_files(categories["resources"])
            report["recovery_results"]["resources"] = sum(1 for v in results.values() if v)
        
        # Save recovery log
        log_path = self.vault_path / "reports" / f"recovery_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_path.parent.mkdir(exist_ok=True)
        
        with open(log_path, 'w') as f:
            json.dump({
                "report": report,
                "detailed_log": self.recovery_log
            }, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 RECOVERY SUMMARY")
        print("="*60)
        
        total_recovered = sum(report["recovery_results"].values())
        print(f"\n✅ Successfully recovered {total_recovered} files")
        
        for category, count in report["recovery_results"].items():
            print(f"  • {category}: {count} files")
        
        print(f"\n📄 Recovery log saved to: {log_path}")
        print("\n🎯 Recovery complete! No files were deleted.")
        
        return report


def main():
    """Main execution"""
    recovery = SafeRecovery()
    recovery.run_recovery()


if __name__ == "__main__":
    main()