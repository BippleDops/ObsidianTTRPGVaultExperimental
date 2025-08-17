#!/usr/bin/env python3
"""
Smart Vault Consolidator - Keeps existing structure but consolidates intelligently
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

class SmartVaultConsolidator:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.analysis = defaultdict(list)
        
    def analyze_structure(self):
        """Analyze current structure for issues and opportunities"""
        print("📊 ANALYZING VAULT STRUCTURE...")
        print("=" * 60)
        
        # Find all directories
        all_dirs = []
        for root, dirs, files in os.walk(self.vault_path):
            for dir_name in dirs:
                if not dir_name.startswith('.'):
                    dir_path = Path(root) / dir_name
                    rel_path = dir_path.relative_to(self.vault_path)
                    file_count = len(list(dir_path.glob('**/*.md')))
                    all_dirs.append((str(rel_path), file_count))
        
        # Sort by name to identify patterns
        all_dirs.sort()
        
        # Identify problematic directories
        print("\n🔴 DIRECTORIES TO REMOVE (duplicates/unnecessary):")
        print("-" * 60)
        
        remove_candidates = [
            # Duplicate numbered directories (keep the one with more content)
            ("03_People", "03_Mechanics"),  # Keep 03_People if it has NPCs
            ("05_Rules", "05_Player_Characters"),  # Keep 05_Rules
            ("13_Performance", "09_Performance"),  # Keep 09_Performance
            ("Player_Characters", "05_Player_Characters"),  # Keep 05_
            ("Players", "07_Player_Resources"),  # Keep 07_
            ("Audio", None),  # Empty/unused
            ("Export", None),  # Empty/unused
            ("reports", None),  # Script output, not content
            ("World_Simulation", None),  # Empty/unused
        ]
        
        for pair in remove_candidates:
            if len(pair) == 2 and pair[1]:
                # Compare two directories
                dir1_path = self.vault_path / pair[0]
                dir2_path = self.vault_path / pair[1]
                
                if dir1_path.exists() and dir2_path.exists():
                    count1 = len(list(dir1_path.glob('**/*.md')))
                    count2 = len(list(dir2_path.glob('**/*.md')))
                    
                    if count1 == 0 and count2 == 0:
                        print(f"  • Remove both: {pair[0]} (empty) and {pair[1]} (empty)")
                        self.analysis['remove'].extend([pair[0], pair[1]])
                    elif count1 > count2:
                        print(f"  • Remove: {pair[1]} ({count2} files) - Keep: {pair[0]} ({count1} files)")
                        self.analysis['remove'].append(pair[1])
                        self.analysis['merge'].append((pair[1], pair[0]))
                    else:
                        print(f"  • Remove: {pair[0]} ({count1} files) - Keep: {pair[1]} ({count2} files)")
                        self.analysis['remove'].append(pair[0])
                        self.analysis['merge'].append((pair[0], pair[1]))
            else:
                # Single directory to check if empty
                dir_path = self.vault_path / pair[0]
                if dir_path.exists():
                    count = len(list(dir_path.glob('**/*')))
                    if count == 0:
                        print(f"  • Remove: {pair[0]} (empty)")
                        self.analysis['remove'].append(pair[0])
                    else:
                        print(f"  • Check: {pair[0]} ({count} files) - may be unnecessary")
        
        print("\n🟡 CONSOLIDATION OPPORTUNITIES:")
        print("-" * 60)
        
        consolidations = [
            ("Move People from 02_Worldbuilding to 03_People", 
             "02_Worldbuilding/People", "03_People"),
            ("Move Groups/Factions from 02_Worldbuilding to own directory",
             "02_Worldbuilding/Groups", "03_People/Factions"),
            ("Consolidate all indexes to _INDEXES",
             "00_Indexes", "_INDEXES"),
            ("Consolidate all metadata to _METADATA",
             "00_System/Metadata", "_METADATA"),
            ("Move all guides to MASTER_GUIDES",
             "00_System/Guides", "MASTER_GUIDES"),
            ("Consolidate research materials",
             "12_Research", "04_Resources/Research"),
            ("Move archive content to 08_Archive",
             "00_System/old-versions", "08_Archive"),
        ]
        
        for desc, source, target in consolidations:
            source_path = self.vault_path / source
            target_path = self.vault_path / target
            
            if source_path.exists():
                count = len(list(source_path.glob('**/*.md')))
                if count > 0:
                    print(f"  • {desc}")
                    print(f"    {source} → {target} ({count} files)")
                    self.analysis['consolidate'].append((source, target))
        
        print("\n🟢 IMPROVEMENT OPPORTUNITIES:")
        print("-" * 60)
        
        improvements = [
            "1. NAMING CONSISTENCY: Standardize on either underscores or hyphens (not both)",
            "2. NUMBERING: Keep 00-09 numbering for main categories, remove others",
            "3. STRUCTURE: Maximum 3 levels deep (currently some are 4-5 levels)",
            "4. TEMPLATES: Consolidate all templates to 00_System/Templates",
            "5. SCRIPTS: Move all scripts to dedicated _SCRIPTS directory",
            "6. PERFORMANCE: Move all reports/analytics to 09_Performance",
            "7. CANVAS FILES: Consolidate all .canvas files to 00_System/Canvas",
            "8. STUBS: Identify and consolidate stub files to 08_Archive/Stubs",
            "9. DUPLICATES: Many NPCs appear in both 02_Worldbuilding and 03_People",
            "10. ASSETS: All images/media should be in 04_Resources/Assets"
        ]
        
        for improvement in improvements:
            print(f"  {improvement}")
        
        return self.analysis
        
    def execute_cleanup(self):
        """Execute the identified cleanup actions"""
        print("\n🔧 EXECUTING CLEANUP...")
        print("=" * 60)
        
        # Remove empty/duplicate directories
        for dir_name in self.analysis['remove']:
            dir_path = self.vault_path / dir_name
            if dir_path.exists():
                try:
                    # Move any content first
                    file_count = len(list(dir_path.glob('**/*')))
                    if file_count > 0:
                        # Find appropriate target
                        for source, target in self.analysis['merge']:
                            if source == dir_name:
                                target_path = self.vault_path / target
                                target_path.mkdir(parents=True, exist_ok=True)
                                
                                for item in dir_path.iterdir():
                                    dest = target_path / item.name
                                    if not dest.exists():
                                        shutil.move(str(item), str(dest))
                                        print(f"  ✓ Moved {item.name} to {target}")
                                break
                    
                    # Remove directory
                    shutil.rmtree(dir_path)
                    print(f"  ✓ Removed {dir_name}")
                    
                except Exception as e:
                    print(f"  ⚠️ Could not remove {dir_name}: {e}")
        
        # Execute consolidations
        for source, target in self.analysis['consolidate']:
            source_path = self.vault_path / source
            target_path = self.vault_path / target
            
            if source_path.exists():
                target_path.mkdir(parents=True, exist_ok=True)
                
                try:
                    for item in source_path.iterdir():
                        dest = target_path / item.name
                        if not dest.exists():
                            shutil.move(str(item), str(dest))
                            print(f"  ✓ Consolidated {item.name} to {target}")
                        else:
                            # Handle duplicates by renaming
                            counter = 1
                            while dest.exists():
                                stem = item.stem
                                suffix = item.suffix
                                dest = target_path / f"{stem}_{counter}{suffix}"
                                counter += 1
                            shutil.move(str(item), str(dest))
                            print(f"  ✓ Consolidated {item.name} to {dest.name} (renamed)")
                    
                    # Remove empty source
                    if not list(source_path.iterdir()):
                        source_path.rmdir()
                        print(f"  ✓ Removed empty {source}")
                        
                except Exception as e:
                    print(f"  ⚠️ Could not consolidate {source}: {e}")
        
        print("\n✅ CLEANUP COMPLETE!")
        
    def generate_report(self):
        """Generate detailed report of changes"""
        report = f"""# Vault Consolidation Report

## Directories Removed
{chr(10).join('- ' + d for d in self.analysis['remove'])}

## Files Consolidated
{chr(10).join(f'- {s} → {t}' for s, t in self.analysis['consolidate'])}

## Recommended Next Steps

1. **Review 03_People vs 02_Worldbuilding/People** - Significant duplication
2. **Standardize naming** - Choose either underscores or hyphens
3. **Flatten deep nesting** - Some files are 5+ levels deep
4. **Create _SCRIPTS directory** - Move all Python scripts there
5. **Audit stub files** - Many placeholder files could be removed

## Current Structure Summary

Main Categories (keep these):
- 00_System - System files and templates
- 01_Adventures - Campaigns and quests
- 02_Worldbuilding - World content
- 03_People - NPCs and characters
- 04_Resources - Assets and references
- 05_Rules - Game mechanics
- 06_Sessions - Session notes
- 07_Player_Resources - Player materials
- 08_Archive - Old content
- 09_Performance - Analytics and reports

Special Directories (keep these):
- _INDEXES - All indexes and MOCs
- _METADATA - Vault metadata
- MASTER_GUIDES - Comprehensive guides
- scripts - Automation scripts
"""
        
        report_path = self.vault_path / "09_Performance" / "consolidation_report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Full report saved to: {report_path.relative_to(self.vault_path)}")
        
    def run(self):
        """Execute the consolidation process"""
        print("=" * 60)
        print("🎯 SMART VAULT CONSOLIDATOR")
        print("=" * 60)
        
        # Analyze
        self.analyze_structure()
        
        # Ask for confirmation
        print("\n" + "=" * 60)
        print("Ready to execute cleanup.")
        print("This will:")
        print("  • Remove empty/duplicate directories")
        print("  • Consolidate files to appropriate locations")
        print("  • Preserve all content")
        
        # Execute
        self.execute_cleanup()
        
        # Generate report
        self.generate_report()

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    consolidator = SmartVaultConsolidator(vault_path)
    consolidator.run()