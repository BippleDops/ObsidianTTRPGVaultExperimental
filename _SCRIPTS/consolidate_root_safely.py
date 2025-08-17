#!/usr/bin/env python3
"""
Safely consolidate and organize root directory files
WITHOUT accidentally moving to backups folder
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def safe_consolidate():
    """Consolidate root files safely"""
    vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")
    
    # Define categories and their target locations
    # IMPORTANT: None of these go to backups!
    file_moves = {
        # Documentation - Keep in proper documentation folder
        "09_Documentation": [
            "CORDELIA_VAULT_USER_MANUAL.md",
            "GM_QUICK_REFERENCE.md", 
            "PLAYER_HANDBOOK.md",
            "TECHNICAL_DOCUMENTATION.md",
            "VIDEO_TUTORIAL_SCRIPTS.md",
            "INTERACTIVE_TUTORIAL_SYSTEM.md",
            "EXAMPLE_CAMPAIGN_SETUP.md"
        ],
        
        # Campaign Management Tools - Active use
        "06_GM_Resources/Campaign_Management": [
            "Campaign_Dashboard.md",
            "Campaign_Relationship_Matrix.md",
            "MASTER_VAULT_DASHBOARD.md",
            "D&D_SOURCEBOOK_INTEGRATION_DASHBOARD.md"
        ],
        
        # Master Indexes - Keep accessible
        "00_Indexes": [
            "Master_Campaign_Index.md",
            "Master_Groups_Index.md",
            "Master_Lore_Index.md",
            "Master_People_Index.md",
            "Master_Places_Index.md",
            "Vault_Navigation_Hub.md"
        ],
        
        # Archive completed project reports
        "08_Archive/Project_Reports": [
            "PHASE_1_COMPLETION_REPORT.md",
            "Phase_3_Content_Enhancement_Complete.md",
            "Phase_4_Advanced_Automation_Complete.md",
            "PHASE_5_AUTONOMOUS_REPORT.md",
            "PHASE_5_EXCELLENCE_250_STEP_PLAN.md",
            "PHASE_5_EXCELLENCE_CERTIFICATION.md",
            "SPRINT_1_IMPLEMENTATION_REPORT.md",
            "SPRINT_2_IMPLEMENTATION_REPORT.md",
            "SPRINT_3_IMPLEMENTATION_REPORT.md",
            "SPRINT_4_IMPLEMENTATION_REPORT.md",
            "PARALLEL_DEPLOYMENT_SUMMARY.md",
            "wikilink_standardization_report.md",
            "VAULT_COMPLETION_SUMMARY.md",
            "FINAL_VAULT_AUDIT_REPORT.md",
            "ROOT_CONSOLIDATION.md"
        ],
        
        # Archive planning documents
        "08_Archive/Planning": [
            "100_NEXT_LEVEL_IMPROVEMENTS.md",
            "500_STEP_VAULT_COMPLETION_PLAN.md",
            "AGILE_IMPLEMENTATION_GLIDE_PATH.md"
        ]
    }
    
    # Files to keep in root (essential only)
    keep_in_root = [
        "README.md",  # Vault overview
        "CLAUDE.md",  # AI configuration (if exists)
        "TODO.md"     # Current tasks (if exists)
    ]
    
    moved_files = []
    errors = []
    
    print("🔄 Safely Consolidating Root Directory")
    print("=" * 50)
    
    for target_dir, files in file_moves.items():
        target_path = vault_path / target_dir
        
        # Create target directory if needed
        target_path.mkdir(parents=True, exist_ok=True)
        
        for filename in files:
            source = vault_path / filename
            if source.exists():
                try:
                    destination = target_path / filename
                    
                    # Check if already exists at destination
                    if destination.exists():
                        # Rename with timestamp to avoid overwriting
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        new_name = f"{filename.replace('.md', '')}_{timestamp}.md"
                        destination = target_path / new_name
                    
                    # Move the file
                    shutil.move(str(source), str(destination))
                    moved_files.append(f"{filename} → {target_dir}/")
                    print(f"  ✅ Moved: {filename} → {target_dir}/")
                    
                except Exception as e:
                    errors.append(f"Error moving {filename}: {e}")
                    print(f"  ❌ Error: {filename} - {e}")
    
    print("\n" + "=" * 50)
    print(f"✅ Successfully moved {len(moved_files)} files")
    
    if errors:
        print(f"\n⚠️ {len(errors)} errors occurred:")
        for error in errors:
            print(f"  - {error}")
    
    return moved_files

def check_for_duplicates():
    """Check for duplicate or similar files"""
    vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")
    
    print("\n📋 Checking for Duplicates")
    print("-" * 50)
    
    # Look for files with similar names
    duplicates = []
    
    # Check for "Master Campaign Index.md" vs "Master_Campaign_Index.md"
    if (vault_path / "Master Campaign Index.md").exists():
        duplicates.append("Master Campaign Index.md (duplicate of Master_Campaign_Index.md)")
    
    # Check for "Link Integrity Report.md" (might be incomplete name)
    if (vault_path / "Link Integrity Report.md").exists():
        duplicates.append("Link Integrity Report.md")
        
    if duplicates:
        print("Found potential duplicates/issues:")
        for dup in duplicates:
            print(f"  ⚠️ {dup}")
    else:
        print("  ✅ No duplicates found")
    
    return duplicates

def consolidate_duplicates():
    """Merge duplicate index files"""
    vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")
    
    print("\n🔧 Consolidating Duplicates")
    print("-" * 50)
    
    # Handle "Master Campaign Index.md" vs "Master_Campaign_Index.md"
    old_file = vault_path / "Master Campaign Index.md"
    new_file = vault_path / "Master_Campaign_Index.md"
    
    if old_file.exists() and new_file.exists():
        # Read both files
        with open(old_file, 'r') as f:
            old_content = f.read()
        with open(new_file, 'r') as f:
            new_content = f.read()
        
        # If they're different, merge them
        if old_content != new_content:
            # Append old content to new file as a section
            with open(new_file, 'a') as f:
                f.write("\n\n---\n## Previous Version Content\n")
                f.write(old_content)
            print(f"  ✅ Merged content from 'Master Campaign Index.md' into 'Master_Campaign_Index.md'")
        
        # Archive the old file
        archive_path = vault_path / "08_Archive" / "Duplicates"
        archive_path.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old_file), str(archive_path / old_file.name))
        print(f"  ✅ Archived duplicate: {old_file.name}")
    
    # Handle "Link Integrity Report.md" 
    link_file = vault_path / "Link Integrity Report.md"
    if link_file.exists():
        # This appears to be an incomplete filename - move to reports
        reports_path = vault_path / "reports"
        reports_path.mkdir(exist_ok=True)
        shutil.move(str(link_file), str(reports_path / "Link_Integrity_Report.md"))
        print(f"  ✅ Moved 'Link Integrity Report.md' to reports/")

def verify_root_clean():
    """Verify root directory is clean"""
    vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")
    
    print("\n✅ Final Root Directory Status")
    print("-" * 50)
    
    md_files = list(vault_path.glob("*.md"))
    
    print(f"Files remaining in root: {len(md_files)}")
    for f in md_files:
        print(f"  - {f.name}")
    
    # Check nothing went to backups
    backup_path = vault_path / "backups"
    if backup_path.exists():
        new_files = list(backup_path.glob("*.md"))
        if new_files:
            print(f"\n⚠️ WARNING: {len(new_files)} files found in backups/")
            print("These should be reviewed and moved to proper locations!")
        else:
            print("\n✅ Backups folder clean - no files accidentally moved there")

def main():
    print("🧹 Root Directory Consolidation (Safe Mode)")
    print("=" * 50)
    print("This script will NOT move files to backups folder")
    print("All files will go to appropriate active directories")
    print("=" * 50)
    
    # Check for duplicates first
    duplicates = check_for_duplicates()
    
    if duplicates:
        # Handle duplicates
        consolidate_duplicates()
    
    # Move files to proper locations
    moved = safe_consolidate()
    
    # Verify final state
    verify_root_clean()
    
    print("\n" + "=" * 50)
    print("✨ Root Consolidation Complete!")
    print(f"Files organized: {len(moved)}")
    print("No files moved to backups folder ✅")
    print("Root directory now contains only essential files")

if __name__ == "__main__":
    main()