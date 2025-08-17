#!/usr/bin/env python3
"""
Master automation controller for vault maintenance
Run this to execute all maintenance tasks
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_script(script_name):
    """Run a Python script and capture output"""
    script_path = Path("_SCRIPTS") / script_name
    if script_path.exists():
        print(f"\n▶ Running {script_name}...")
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            print(result.stdout)
            if result.stderr:
                print(f"  ⚠ Warnings: {result.stderr}")
            return True
        except subprocess.TimeoutExpired:
            print(f"  ⚠ {script_name} timed out")
            return False
        except Exception as e:
            print(f"  ❌ Error running {script_name}: {e}")
            return False
    else:
        print(f"  ❌ Script not found: {script_path}")
        return False

def main():
    print("=" * 60)
    print("VAULT AUTOMATION SUITE")
    print(f"Running: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # List of scripts to run
    scripts = [
        ("auto_organizer.py", "Organization Check"),
        ("link_checker.py", "Link Validation"),
        ("auto_backup.py", "Critical File Backup"),
        ("session_prep.py", "Session Preparation")
    ]
    
    results = []
    for script, description in scripts:
        print(f"\n📋 {description}")
        success = run_script(script)
        results.append((description, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("AUTOMATION COMPLETE")
    print("=" * 60)
    print("\nResults:")
    for task, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {task}")
    
    # Log results
    log_file = Path("09_Performance/automation_log.txt")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        f.write(f"\n{datetime.now().isoformat()}\n")
        for task, success in results:
            f.write(f"  {'SUCCESS' if success else 'FAILED'}: {task}\n")
    
    print(f"\nLog saved to: {log_file}")

if __name__ == "__main__":
    main()
