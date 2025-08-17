#!/usr/bin/env python3
"""
SAFE SCRIPT RUNNER - Protect the vault from dangerous operations
Run other scripts through this wrapper for safety checks and backups
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib
import json

class SafeScriptRunner:
    def __init__(self):
        self.vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")
        self.safety_backup_dir = self.vault_path / "safety_backups"
        self.dangerous_scripts = []
        self.safe_scripts = []
        
    def analyze_script(self, script_path):
        """Analyze a script for dangerous operations"""
        script_path = Path(script_path)
        if not script_path.exists():
            return {"safe": False, "reason": "Script not found"}
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        dangers = []
        warnings = []
        
        # Check for dangerous operations
        dangerous_patterns = {
            'shutil.rmtree': 'DELETES ENTIRE DIRECTORY TREES',
            'os.remove': 'DELETES FILES',
            'os.rmdir': 'REMOVES DIRECTORIES',
            'os.unlink': 'DELETES FILES',
            'open.*"w"': 'OVERWRITES FILES',
            'shutil.move': 'MOVES FILES (can lose data)',
            '.unlink()': 'DELETES FILES',
            '.rmdir()': 'REMOVES DIRECTORIES',
            'DROP TABLE': 'DELETES DATABASE TABLES',
            'DELETE FROM': 'DELETES DATABASE RECORDS',
        }
        
        for pattern, description in dangerous_patterns.items():
            if pattern in content:
                dangers.append(f"⚠️ {description} - Pattern: {pattern}")
        
        # Check for safety features
        safety_features = {
            'backup': 'Creates backups',
            'dry.run\|dry_run': 'Has dry-run mode',
            'confirm': 'Asks for confirmation',
            'try.*except': 'Has error handling',
            '.exists()': 'Checks file existence',
            'Path.mkdir.*exist_ok': 'Safe directory creation',
        }
        
        safety_score = 0
        for pattern, description in safety_features.items():
            if pattern.replace('\\', '') in content:
                safety_score += 1
                warnings.append(f"✅ {description}")
        
        # Determine safety level
        if len(dangers) == 0:
            safety = "SAFE"
        elif len(dangers) <= 2 and safety_score >= 3:
            safety = "MODERATE"
        else:
            safety = "DANGEROUS"
        
        return {
            "script": script_path.name,
            "safety": safety,
            "dangers": dangers,
            "safety_features": warnings,
            "safety_score": safety_score,
            "danger_count": len(dangers)
        }
    
    def create_safety_backup(self):
        """Create a safety backup before running any script"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"safety_backup_{timestamp}"
        backup_path = self.safety_backup_dir / backup_name
        
        print(f"🛡️ Creating safety backup: {backup_name}")
        
        # Create backup directory
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Backup critical files only (not the entire vault)
        critical_paths = [
            self.vault_path / "README.md",
            self.vault_path / "TODO.md",
            self.vault_path / "CLAUDE.md",
        ]
        
        # Also backup directory structure
        structure_file = backup_path / "directory_structure.txt"
        with open(structure_file, 'w') as f:
            for item in self.vault_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    f.write(f"DIR: {item.name}\n")
                    # Count files in directory
                    file_count = len(list(item.glob("*.md")))
                    f.write(f"  Files: {file_count}\n")
        
        # Copy critical files
        for file_path in critical_paths:
            if file_path.exists():
                shutil.copy2(file_path, backup_path / file_path.name)
        
        # Create vault statistics
        stats = {
            "timestamp": timestamp,
            "total_files": len(list(self.vault_path.rglob("*.md"))),
            "directories": len([d for d in self.vault_path.iterdir() if d.is_dir()]),
            "backup_path": str(backup_path)
        }
        
        with open(backup_path / "vault_stats.json", 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"  ✅ Backup created with {len(critical_paths)} critical files")
        return backup_path
    
    def audit_all_scripts(self):
        """Audit all Python scripts in the scripts directory"""
        scripts_dir = self.vault_path / "scripts"
        
        print("🔍 Script Safety Audit")
        print("=" * 60)
        
        all_scripts = list(scripts_dir.glob("*.py"))
        
        safe = []
        moderate = []
        dangerous = []
        
        for script in all_scripts:
            result = self.analyze_script(script)
            
            if result["safety"] == "SAFE":
                safe.append(result)
            elif result["safety"] == "MODERATE":
                moderate.append(result)
            else:
                dangerous.append(result)
        
        # Print results
        print(f"\n✅ SAFE Scripts ({len(safe)}):")
        for s in safe[:10]:
            print(f"  • {s['script']}")
        if len(safe) > 10:
            print(f"  ... and {len(safe) - 10} more")
        
        print(f"\n⚠️ MODERATE Risk Scripts ({len(moderate)}):")
        for s in moderate:
            print(f"  • {s['script']}")
            for danger in s["dangers"][:2]:
                print(f"    {danger}")
        
        print(f"\n🚨 DANGEROUS Scripts ({len(dangerous)}):")
        for s in dangerous:
            print(f"  • {s['script']}")
            for danger in s["dangers"][:3]:
                print(f"    {danger}")
        
        # Save detailed report
        report = {
            "audit_date": datetime.now().isoformat(),
            "total_scripts": len(all_scripts),
            "safe": len(safe),
            "moderate": len(moderate),
            "dangerous": len(dangerous),
            "dangerous_scripts": [s["script"] for s in dangerous],
            "details": {
                "safe": safe,
                "moderate": moderate,
                "dangerous": dangerous
            }
        }
        
        report_path = self.vault_path / "scripts" / "SCRIPT_SAFETY_AUDIT.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: SCRIPT_SAFETY_AUDIT.json")
        
        return report
    
    def safe_run_script(self, script_name, args=None, dry_run=True):
        """Safely run a script with protections"""
        script_path = self.vault_path / "scripts" / script_name
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_name}")
            return False
        
        # Analyze script
        analysis = self.analyze_script(script_path)
        
        print(f"\n🔍 Script Analysis: {script_name}")
        print(f"Safety Level: {analysis['safety']}")
        
        if analysis["dangers"]:
            print("\n⚠️ Dangerous Operations Detected:")
            for danger in analysis["dangers"]:
                print(f"  {danger}")
        
        if analysis["safety"] == "DANGEROUS":
            print("\n🚨 This script is marked as DANGEROUS!")
            response = input("Do you want to continue? (yes/no): ")
            if response.lower() != "yes":
                print("Aborted.")
                return False
        
        # Create safety backup
        if not dry_run:
            backup_path = self.create_safety_backup()
            print(f"\n💾 Safety backup created at: {backup_path}")
        
        # Run script
        if dry_run:
            print(f"\n🔵 DRY RUN MODE - No changes will be made")
            
        cmd = ["python3", str(script_path)]
        if args:
            cmd.extend(args)
        
        if dry_run and "--dry-run" not in cmd:
            cmd.append("--dry-run")
        
        print(f"\nRunning: {' '.join(cmd)}")
        print("-" * 60)
        
        try:
            result = subprocess.run(cmd, capture_output=False, text=True)
            if result.returncode == 0:
                print("-" * 60)
                print("✅ Script completed successfully")
            else:
                print("-" * 60)
                print(f"⚠️ Script exited with code: {result.returncode}")
        except Exception as e:
            print(f"❌ Error running script: {e}")
            return False
        
        return True

def main():
    runner = SafeScriptRunner()
    
    if len(sys.argv) == 1:
        # No arguments - run audit
        print("🛡️ SAFE SCRIPT RUNNER")
        print("=" * 60)
        print("Usage:")
        print("  python SAFE_SCRIPT_RUNNER.py audit              # Audit all scripts")
        print("  python SAFE_SCRIPT_RUNNER.py run <script.py>    # Run script safely")
        print("  python SAFE_SCRIPT_RUNNER.py check <script.py>  # Check script safety")
        print("=" * 60)
        print("\nRunning default audit...\n")
        runner.audit_all_scripts()
        
    elif sys.argv[1] == "audit":
        runner.audit_all_scripts()
        
    elif sys.argv[1] == "check" and len(sys.argv) > 2:
        script = sys.argv[2]
        result = runner.analyze_script(runner.vault_path / "scripts" / script)
        print(f"\nScript: {script}")
        print(f"Safety: {result['safety']}")
        print(f"Dangers: {len(result['dangers'])}")
        print(f"Safety Score: {result['safety_score']}")
        
        if result['dangers']:
            print("\nDangerous Operations:")
            for danger in result['dangers']:
                print(f"  {danger}")
                
    elif sys.argv[1] == "run" and len(sys.argv) > 2:
        script = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else None
        
        # Ask for dry run
        response = input("Run in dry-run mode first? (recommended) (y/n): ")
        dry_run = response.lower() != 'n'
        
        runner.safe_run_script(script, args, dry_run)
        
        if dry_run:
            response = input("\nDry run complete. Run for real? (y/n): ")
            if response.lower() == 'y':
                runner.safe_run_script(script, args, False)

if __name__ == "__main__":
    main()