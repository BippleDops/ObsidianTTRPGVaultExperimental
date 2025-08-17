#!/usr/bin/env python3
"""
Cleanup and Organization Script
Organizes backup files and creates proper structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def cleanup_vault_structure(vault_root: str):
    """Clean up backup files and organize vault structure"""
    
    print("🧹 Starting vault cleanup and organization...")
    
    # Create proper backup directory
    backup_dir = os.path.join(vault_root, "08_Archive", "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Move scattered backup files
    backup_files_moved = 0
    
    # Find and move .backup files
    for root, dirs, files in os.walk(vault_root):
        for file in files:
            if file.endswith('.backup'):
                source = os.path.join(root, file)
                dest = os.path.join(backup_dir, file)
                
                try:
                    if not os.path.exists(dest):
                        shutil.move(source, dest)
                        backup_files_moved += 1
                        print(f"  📁 Moved {file} to archive")
                except Exception as e:
                    print(f"  ⚠️  Could not move {file}: {e}")
    
    # Consolidate vault_backup directories
    vault_backup_dirs = []
    for item in os.listdir(vault_root):
        if item.startswith('vault_backup_'):
            vault_backup_dirs.append(item)
    
    if vault_backup_dirs:
        print(f"🗂️  Found {len(vault_backup_dirs)} vault backup directories")
        
        # Move to archive
        for backup_dir_name in vault_backup_dirs:
            source = os.path.join(vault_root, backup_dir_name)
            dest = os.path.join(backup_dir, backup_dir_name)
            
            try:
                if not os.path.exists(dest):
                    shutil.move(source, dest)
                    print(f"  📁 Moved {backup_dir_name} to archive")
            except Exception as e:
                print(f"  ⚠️  Could not move {backup_dir_name}: {e}")
    
    print(f"✅ Cleanup complete! Moved {backup_files_moved} backup files to archive")

if __name__ == "__main__":
    vault_root = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    cleanup_vault_structure(vault_root)