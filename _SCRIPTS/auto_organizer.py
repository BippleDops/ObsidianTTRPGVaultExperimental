#!/usr/bin/env python3
"""
Auto-organizer for TTRPG Vault
Runs safe organization tasks automatically
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

def organize_new_files():
    """Move new files to appropriate folders based on content"""
    inbox = Path("00_Inbox")
    if not inbox.exists():
        inbox.mkdir()
    
    # Check for files in root that should be organized
    for file in Path(".").glob("*.md"):
        if file.name.startswith("NPC"):
            target = Path("03_People") / file.name
            print(f"  Moving {file} to People folder")
            # shutil.move(file, target)  # Commented for safety
        elif "quest" in file.name.lower():
            target = Path("01_Adventures") / file.name
            print(f"  Moving {file} to Adventures folder")
            # shutil.move(file, target)  # Commented for safety
    
    print("Organization check complete")

def clean_empty_folders():
    """Remove empty folders"""
    empty_dirs = []
    for root, dirs, files in os.walk("."):
        if not dirs and not files and "Archive" not in root:
            empty_dirs.append(root)
    
    print(f"Found {len(empty_dirs)} empty directories")
    # for dir in empty_dirs:
    #     os.rmdir(dir)  # Commented for safety

if __name__ == "__main__":
    print("Running auto-organization...")
    organize_new_files()
    clean_empty_folders()
    print("Auto-organization complete!")
