#!/usr/bin/env python3
"""
Targeted removal of fake filepath-based files
Focus on removing only clearly fake files
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def identify_fake_files():
    """Identify only clearly fake files"""
    fake_files = []
    
    # Very specific patterns for fake files
    fake_name_patterns = [
        # Filepath-based NPCs in 03_People
        r'^00_Indexes_',
        r'^01_Adventures_',
        r'^02_Worldbuilding_',
        r'^03_People_',
        r'^04_Resources_',
        r'^05_Rules_',
        r'^06_Sessions_',
        r'^07_Player_',
        
        # Chapter files in wrong places
        r'^\d{2} Chapter \d+',
        r'^Chapter \d+ ',
        
        # Clear system paths
        r'^Users_',
        r'^Library_',
        r'^Applications_',
        r'^System_',
        r'^private_',
        r'^var_',
        r'^tmp_',
        
        # File extension mistakes
        r'\.png\.md$',
        r'\.jpg\.md$',
        r'\.svg\.md$',
        r'\.json\.md$',
        
        # Step/phase files
        r'^step_\d+',
        r'^phase_\d+',
    ]
    
    # Check specific directories
    directories_to_check = [
        Path("03_People"),  # Most problematic
        Path("02_Worldbuilding"),
        Path("01_Adventures")
    ]
    
    for dir_path in directories_to_check:
        if not dir_path.exists():
            continue
            
        for file_path in dir_path.rglob("*.md"):
            filename = file_path.name
            
            # Check against patterns
            for pattern in fake_name_patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    # Double-check it's not a real file
                    if not any(keep in filename.lower() for keep in ['aquabyssos', 'aethermoor', 'session', 'campaign']):
                        fake_files.append(file_path)
                        break
            
            # Also check for "Chapter X" files in People folder
            if "03_People" in str(file_path):
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if 'Chapter' in content and 'Playing the Game' in content:
                        fake_files.append(file_path)
                    elif 'stabilizing a Character' in filename:
                        fake_files.append(file_path)
                    elif '00_Indexes/Master_Index has established' in content:
                        fake_files.append(file_path)
                except:
                    pass
    
    return list(set(fake_files))  # Remove duplicates

def main():
    print("=" * 60)
    print("TARGETED FAKE FILE REMOVAL")
    print("=" * 60)
    
    # Find fake files
    fake_files = identify_fake_files()
    
    print(f"\nFound {len(fake_files)} clearly fake files\n")
    
    if fake_files:
        # Group by directory
        by_dir = {}
        for f in fake_files:
            dir_name = f.parent.name
            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(f)
        
        # Show samples
        for dir_name, files in by_dir.items():
            print(f"\n{dir_name}: {len(files)} fake files")
            for f in files[:5]:
                print(f"  - {f.name}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
        
        # Create detailed list
        list_path = Path("09_Performance/fake_files_to_remove.txt")
        list_path.parent.mkdir(parents=True, exist_ok=True)
        with open(list_path, 'w') as f:
            f.write(f"Fake Files to Remove\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Total: {len(fake_files)}\n\n")
            for fake_file in sorted(fake_files):
                f.write(f"{fake_file}\n")
        
        print(f"\nFull list saved to: {list_path}")
        
        # Archive them
        print("\n" + "=" * 60)
        confirm = input("Archive these fake files? (yes/no): ")
        
        if confirm.lower() == 'yes':
            archive_dir = Path("08_Archive") / f"fake_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            archived = 0
            errors = 0
            
            for fake_file in fake_files:
                try:
                    # Create subdirectory in archive
                    sub_dir = archive_dir / fake_file.parent.name
                    sub_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    target = sub_dir / fake_file.name
                    shutil.move(str(fake_file), str(target))
                    archived += 1
                except Exception as e:
                    print(f"  Error archiving {fake_file.name}: {e}")
                    errors += 1
            
            print(f"\n✅ Archived {archived} fake files")
            if errors:
                print(f"⚠️  {errors} errors occurred")
            print(f"📁 Archive location: {archive_dir}")
        else:
            print("No files were removed.")
    else:
        print("✅ No fake files found!")

if __name__ == "__main__":
    main()