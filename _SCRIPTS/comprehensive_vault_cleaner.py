#!/usr/bin/env python3
"""
Comprehensive vault cleaner - removes ALL fake files and misplaced content
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import json

class VaultCleaner:
    def __init__(self):
        self.fake_files = []
        self.misplaced_files = []
        self.real_npcs = []
        self.real_content = []
        
        # Comprehensive fake patterns
        self.fake_patterns = {
            'filepath_based': [
                r'^\d{2}_[A-Z][a-z]+_',  # 00_System_, 01_Adventures_
                r'^[A-Z][a-z]+_\d{2}_',  # System_00_, Adventures_01_
                r'_Master_Index',  # Master index files
                r'_index_',  # Index files
                r'^Users_',  # Mac user paths
                r'^Library_',  # Mac library paths
                r'^Applications_',  # Mac applications
                r'^System_',  # System paths
                r'^private_',  # Private paths
                r'^var_',  # Var paths
                r'^tmp_',  # Temp paths
                r'^opt_',  # Opt paths
                r'^usr_',  # Usr paths
                r'^bin_',  # Bin paths
                r'^sbin_',  # Sbin paths
                r'^etc_',  # Etc paths
                r'^dev_',  # Dev paths
                r'^proc_',  # Proc paths
            ],
            'broken_links': [
                r'\.png\.md$',  # PNG files as MD
                r'\.jpg\.md$',  # JPG files as MD
                r'\.jpeg\.md$',  # JPEG files as MD
                r'\.gif\.md$',  # GIF files as MD
                r'\.svg\.md$',  # SVG files as MD
                r'\.pdf\.md$',  # PDF files as MD
                r'\.json\.md$',  # JSON files as MD
                r'\.txt\.md$',  # TXT files as MD
                r'\.css\.md$',  # CSS files as MD
                r'\.js\.md$',  # JS files as MD
                r'\.html\.md$',  # HTML files as MD
            ],
            'step_files': [
                r'^step_\d+',  # Step files
                r'^phase_\d+',  # Phase files
                r'step_\d+_\(',  # Step with parentheses
                r'phase_\d+_\(',  # Phase with parentheses
            ],
            'system_generated': [
                r'^#',  # Files starting with #
                r'^\$',  # Files starting with $
                r'^%',  # Files starting with %
                r'^<',  # Files starting with <
                r'^>',  # Files starting with >
                r'^\^',  # Files starting with ^
                r'^~',  # Files starting with ~
                r'^\.\_',  # Mac hidden files
                r'^\_\.',  # More hidden files
            ],
            'duplicate_markers': [
                r'_1\.md$',  # _1.md duplicates
                r'_2\.md$',  # _2.md duplicates
                r'_copy\.md$',  # _copy.md
                r'_Copy\.md$',  # _Copy.md
                r'_backup\.md$',  # _backup.md
                r'_old\.md$',  # _old.md
                r'_temp\.md$',  # _temp.md
                r'_test\.md$',  # _test.md
            ]
        }
        
        # Patterns for content that belongs in specific folders
        self.content_patterns = {
            '05_Rules': [
                r'Chapter \d+.*Playing the Game',
                r'Chapter \d+.*Character Creation',
                r'Chapter \d+.*Combat',
                r'Chapter \d+.*Spellcasting',
                r'Chapter \d+.*Equipment',
                r'stabilizing a Character',
                r'rules.*compendium',
                r'player.*handbook',
                r'dungeon.*master.*guide',
                r'game.*mechanics',
            ],
            '01_Adventures': [
                r'quest.*:',
                r'adventure.*:',
                r'campaign.*:',
                r'encounter.*:',
                r'hook.*:',
                r'mission.*:',
                r'scenario.*:',
            ],
            '02_Worldbuilding': [
                r'location.*:',
                r'city.*:',
                r'town.*:',
                r'region.*:',
                r'kingdom.*:',
                r'continent.*:',
                r'world.*:',
                r'plane.*:',
                r'realm.*:',
            ],
            '03_People': [
                # Only ACTUAL NPCs belong here
                r'^NPC_[A-Za-z]+_[A-Za-z]+',  # Real NPC names
                r'Race:.*Class:',  # NPC stat blocks
                r'Alignment:.*\(Lawful|Neutral|Chaotic\)',
            ]
        }

    def is_fake_file(self, file_path):
        """Comprehensive check if file is fake"""
        filename = file_path.name
        
        # Check all fake patterns
        for category, patterns in self.fake_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    # Special case: preserve real quest/campaign files
                    if any(real in filename.lower() for real in ['quest', 'campaign', 'session', 'encounter', 'aquabyssos', 'aethermoor']):
                        continue
                    return True, category
        
        # Check file content for fake patterns
        if file_path.exists() and file_path.suffix == '.md':
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # Check for path-based fake NPCs
                if '03_People' in str(file_path):
                    # Is this really an NPC or something else?
                    if 'Chapter' in content and 'Playing the Game' in content:
                        return True, 'misplaced_rules'
                    if 'has established themselves as a notable figure' in content and '00_Indexes' in content:
                        return True, 'fake_npc_from_path'
                    if '/Users/' in content and 'Library/Mobile Documents' in content:
                        return True, 'contains_system_paths'
                
                # Generic fake content
                if len(content) < 50 and 'To Be Determined' in content:
                    return True, 'placeholder_content'
                    
            except:
                pass
        
        return False, None

    def check_misplaced_file(self, file_path):
        """Check if file is in wrong directory"""
        if not file_path.exists() or file_path.suffix != '.md':
            return None
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            current_dir = file_path.parent.name
            
            # Check each content pattern
            for correct_dir, patterns in self.content_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        # File matches pattern for different directory
                        if correct_dir != current_dir and correct_dir not in str(file_path):
                            return correct_dir
        except:
            pass
        
        return None

    def scan_vault(self):
        """Scan entire vault for issues"""
        print("Scanning vault for fake and misplaced files...")
        
        for root, dirs, files in os.walk("."):
            # Skip system directories
            if any(skip in root for skip in ['.git', '.obsidian', '09_Performance', '08_Archive', '_SCRIPTS']):
                continue
            
            for file in files:
                if not file.endswith('.md'):
                    continue
                
                file_path = Path(root) / file
                
                # Check if fake
                is_fake, fake_type = self.is_fake_file(file_path)
                if is_fake:
                    self.fake_files.append({
                        'path': file_path,
                        'type': fake_type
                    })
                else:
                    # Check if misplaced
                    correct_dir = self.check_misplaced_file(file_path)
                    if correct_dir:
                        self.misplaced_files.append({
                            'path': file_path,
                            'should_be_in': correct_dir
                        })
                    else:
                        # It's real content in right place
                        if '03_People' in str(file_path):
                            self.real_npcs.append(file_path)
                        else:
                            self.real_content.append(file_path)

    def generate_report(self):
        """Generate detailed report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'fake_files': {
                'total': len(self.fake_files),
                'by_type': {}
            },
            'misplaced_files': {
                'total': len(self.misplaced_files),
                'details': []
            },
            'preserved': {
                'real_npcs': len(self.real_npcs),
                'real_content': len(self.real_content)
            }
        }
        
        # Group fake files by type
        for fake in self.fake_files:
            fake_type = fake['type']
            if fake_type not in report['fake_files']['by_type']:
                report['fake_files']['by_type'][fake_type] = []
            report['fake_files']['by_type'][fake_type].append(str(fake['path']))
        
        # Add misplaced files
        for misplaced in self.misplaced_files:
            report['misplaced_files']['details'].append({
                'file': str(misplaced['path']),
                'should_be_in': misplaced['should_be_in']
            })
        
        # Save report
        report_path = Path("09_Performance/comprehensive_clean_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also create readable report
        readable_path = Path("09_Performance/comprehensive_clean_report.md")
        with open(readable_path, 'w') as f:
            f.write("# Comprehensive Vault Clean Report\n\n")
            f.write(f"Generated: {report['timestamp']}\n\n")
            
            f.write(f"## Summary\n")
            f.write(f"- **Fake Files Found**: {report['fake_files']['total']}\n")
            f.write(f"- **Misplaced Files**: {report['misplaced_files']['total']}\n")
            f.write(f"- **Real NPCs Preserved**: {report['preserved']['real_npcs']}\n")
            f.write(f"- **Real Content Preserved**: {report['preserved']['real_content']}\n\n")
            
            f.write("## Fake Files by Type\n")
            for fake_type, files in report['fake_files']['by_type'].items():
                f.write(f"\n### {fake_type} ({len(files)} files)\n")
                for file in files[:5]:  # Show first 5
                    f.write(f"- {file}\n")
                if len(files) > 5:
                    f.write(f"- ... and {len(files) - 5} more\n")
            
            f.write("\n## Misplaced Files\n")
            for item in report['misplaced_files']['details'][:10]:
                f.write(f"- {item['file']} → should be in {item['should_be_in']}\n")
            if len(report['misplaced_files']['details']) > 10:
                f.write(f"- ... and {len(report['misplaced_files']['details']) - 10} more\n")
        
        print(f"\nReports saved:")
        print(f"  - {report_path}")
        print(f"  - {readable_path}")
        
        return report

    def clean_vault(self, dry_run=True):
        """Clean the vault"""
        if dry_run:
            print("\n🔍 DRY RUN MODE - No files will be moved")
        else:
            print("\n🧹 CLEANING MODE - Files will be archived")
        
        # Archive fake files
        if self.fake_files and not dry_run:
            archive_dir = Path("08_Archive") / f"fake_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            for fake in self.fake_files:
                try:
                    source = fake['path']
                    target = archive_dir / fake['type'] / source.name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(target))
                    print(f"  Archived: {source.name}")
                except Exception as e:
                    print(f"  Error: {e}")
        
        # Move misplaced files
        if self.misplaced_files and not dry_run:
            for misplaced in self.misplaced_files:
                try:
                    source = misplaced['path']
                    target_dir = Path(misplaced['should_be_in'])
                    target_dir.mkdir(parents=True, exist_ok=True)
                    target = target_dir / source.name
                    shutil.move(str(source), str(target))
                    print(f"  Moved: {source.name} → {misplaced['should_be_in']}")
                except Exception as e:
                    print(f"  Error: {e}")

def main():
    print("=" * 60)
    print("COMPREHENSIVE VAULT CLEANER")
    print("=" * 60)
    
    cleaner = VaultCleaner()
    
    # Scan the vault
    cleaner.scan_vault()
    
    # Generate report
    report = cleaner.generate_report()
    
    # Print summary
    print(f"\n📊 SCAN RESULTS:")
    print(f"  Fake files found: {len(cleaner.fake_files)}")
    print(f"  Misplaced files: {len(cleaner.misplaced_files)}")
    print(f"  Real NPCs preserved: {len(cleaner.real_npcs)}")
    print(f"  Real content preserved: {len(cleaner.real_content)}")
    
    if cleaner.fake_files:
        print(f"\n🗑️  Sample fake files to remove:")
        for fake in cleaner.fake_files[:5]:
            print(f"  - {fake['path'].name} ({fake['type']})")
    
    if cleaner.misplaced_files:
        print(f"\n📁 Sample misplaced files:")
        for misplaced in cleaner.misplaced_files[:5]:
            print(f"  - {misplaced['path'].name} → {misplaced['should_be_in']}")
    
    # Ask to proceed
    if cleaner.fake_files or cleaner.misplaced_files:
        print("\n" + "=" * 60)
        print("OPTIONS:")
        print("1. Dry run (preview only)")
        print("2. Clean vault (archive fake, move misplaced)")
        print("3. Exit without changes")
        
        choice = input("\nChoice (1/2/3): ")
        
        if choice == '1':
            cleaner.clean_vault(dry_run=True)
        elif choice == '2':
            confirm = input("⚠️  This will move files. Are you sure? (yes/no): ")
            if confirm.lower() == 'yes':
                cleaner.clean_vault(dry_run=False)
                print("\n✅ Vault cleaned!")
            else:
                print("Cancelled.")
        else:
            print("No changes made.")
    else:
        print("\n✅ Vault is clean - no fake or misplaced files found!")

if __name__ == "__main__":
    main()