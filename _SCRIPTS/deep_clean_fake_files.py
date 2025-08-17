#!/usr/bin/env python3
"""
Deep clean script to remove fake filepath-based entries
while preserving real D&D content
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# Patterns that indicate fake filepath-based files
FAKE_PATTERNS = [
    # Filepath patterns
    r'^\d+_[A-Z][a-z]+_', # Like "00_Indexes_", "01_Adventures_"
    r'^step_\d+', # Step files
    r'^phase_\d+', # Phase files
    r'_index\.md$', # Index files that aren't real
    r'^\d+_\d+_', # Double number prefixes
    r'^Users_', # Filepath remnants
    r'^var_folders', # System paths
    r'^tmp_', # Temp files
    r'^Applications_', # Mac app paths
    r'^System_', # System paths
    r'^Library_', # Library paths
    r'^private_', # Private paths
    r'\.png\.md$', # Image files turned to MD
    r'\.jpg\.md$', # Image files turned to MD
    r'\.svg\.md$', # SVG files turned to MD
    r'\.json\.md$', # JSON files turned to MD
    r'^NPC\d+_.*_CLI_', # CLI generated NPCs
    r'_\(.*\)\.md$', # Files with parenthetical categories
    r'^#', # Files starting with #
    r'^\$', # Files starting with $
    r'^%', # Files starting with %
    r'^<', # Files starting with <
]

# Content patterns that indicate fake files
FAKE_CONTENT_PATTERNS = [
    r'/Users/[^/]+/Library/Mobile Documents', # Mac paths
    r'00_Indexes/Master_Index has established', # Fake NPC from path
    r'01_Adventures/Campaigns has established', # Fake NPC from path
    r'02_Worldbuilding/Locations has established', # Fake NPC from path
    r'03_People/NPCs has established', # Fake NPC from path
    r'04_Resources/Assets has established', # Fake NPC from path
    r'05_Rules/Mechanics has established', # Fake NPC from path
    r'Based on \*\*Commoner\*\* \(MM p\.345\) with modifications', # Generic template
    r'This NPC can serve multiple roles:', # Generic placeholder
    r'To be developed', # Placeholder content
    r'To Be Determined', # Placeholder content
]

# Real D&D content patterns to PRESERVE
REAL_PATTERNS = [
    r'aquabyssos', # Campaign name
    r'aethermoor', # Campaign name
    r'session', # Session notes
    r'quest', # Quest content
    r'encounter', # Encounters
    r'campaign', # Campaigns
    r'player', # Player content
    r'^NPC_[A-Za-z]+_[A-Za-z]+\.md$', # Real NPC names like NPC_John_Smith.md
    r'handbook', # Handbooks
    r'guide', # Guides
    r'rules', # Rules
    r'spell', # Spells
    r'item', # Items
    r'monster', # Monsters
    r'class', # Classes
    r'race', # Races
]

def is_fake_file(file_path):
    """Determine if a file is fake based on name and content"""
    filename = file_path.name
    
    # Check filename patterns
    for pattern in FAKE_PATTERNS:
        if re.search(pattern, filename, re.IGNORECASE):
            # But preserve if it matches a real pattern
            for real_pattern in REAL_PATTERNS:
                if re.search(real_pattern, filename, re.IGNORECASE):
                    return False
            return True
    
    # Check content if file exists
    if file_path.exists() and file_path.suffix == '.md':
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Check for fake content patterns
            for pattern in FAKE_CONTENT_PATTERNS:
                if re.search(pattern, content):
                    return True
            
            # Check for suspiciously generic content
            if len(content) < 100:  # Very short files
                if not any(re.search(p, content, re.IGNORECASE) for p in REAL_PATTERNS):
                    return True
            
            # Check if it's just a path-based NPC
            if '00_Indexes' in filename or '01_Adventures' in filename:
                if 'has established themselves' in content:
                    return True
                    
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return False

def scan_directory(base_path):
    """Scan directory for fake files"""
    fake_files = []
    real_files = []
    
    for root, dirs, files in os.walk(base_path):
        # Skip certain directories
        if any(skip in root for skip in ['.git', '.obsidian', '09_Performance', '08_Archive']):
            continue
        
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                
                if is_fake_file(file_path):
                    fake_files.append(file_path)
                else:
                    # Double-check real files for safety
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        # If it's a real D&D file, preserve it
                        if any(re.search(p, content, re.IGNORECASE) for p in ['spell', 'monster', 'quest', 'campaign', 'session', 'player', 'npc', 'encounter']):
                            real_files.append(file_path)
                    except:
                        pass
    
    return fake_files, real_files

def archive_files(files, archive_name):
    """Archive files instead of deleting"""
    if not files:
        return
    
    archive_dir = Path("08_Archive") / f"fake_files_{archive_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    for file_path in files:
        try:
            relative_path = file_path.relative_to(Path.cwd())
            target = archive_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(target))
            print(f"  Archived: {file_path.name}")
        except Exception as e:
            print(f"  Error archiving {file_path}: {e}")
    
    return archive_dir

def main():
    print("=" * 60)
    print("DEEP CLEAN: REMOVING FAKE FILEPATH FILES")
    print("=" * 60)
    
    # Directories to clean
    directories = [
        "00_System",
        "01_Adventures", 
        "02_Worldbuilding",
        "03_People",
        "04_Resources",
        "05_Rules",
        "06_Sessions",
        "07_Player_Resources"
    ]
    
    all_fake = []
    all_real = []
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"\nScanning {dir_name}...")
            fake, real = scan_directory(dir_path)
            all_fake.extend(fake)
            all_real.extend(real)
            print(f"  Found {len(fake)} fake files, {len(real)} real files")
    
    print("\n" + "=" * 60)
    print(f"SCAN COMPLETE")
    print(f"Total fake files found: {len(all_fake)}")
    print(f"Total real files preserved: {len(all_real)}")
    
    if all_fake:
        print("\nSample fake files to be removed:")
        for f in all_fake[:10]:
            print(f"  - {f}")
        
        # Create report
        report_path = Path("09_Performance/fake_files_found.txt")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(f"Fake Files Found: {datetime.now().isoformat()}\n")
            f.write(f"Total: {len(all_fake)}\n\n")
            for fake_file in all_fake:
                f.write(f"{fake_file}\n")
        
        print(f"\nFull list saved to: {report_path}")
        
        # Archive fake files
        response = input("\nArchive these fake files? (yes/no): ")
        if response.lower() == 'yes':
            archive_dir = archive_files(all_fake, "deep_clean")
            print(f"\n✓ Archived {len(all_fake)} files to: {archive_dir}")
        else:
            print("No files were removed.")
    else:
        print("\n✓ No fake files found!")
    
    print("\n✓ Deep clean complete!")

if __name__ == "__main__":
    main()