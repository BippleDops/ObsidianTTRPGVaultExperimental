#!/usr/bin/env python3
"""
Intelligent File Categorizer - Reviews files against their neighbors to detect miscategorization
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict
import random

class IntelligentFileCategorizer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.miscategorized = []
        self.moves = []
        self.analyzed = 0
        
        # Define content patterns for each category
        self.category_patterns = {
            'npc': {
                'must_have': [r'\brace\b', r'\bclass\b', r'\bpersonality\b', r'\bNPC\b', r'\bcharacter\b', 
                              r'\balignment\b', r'\bAC\b', r'\bHP\b', r'\bSTR\b', r'\bDEX\b'],
                'must_not': [r'\bdistrict\b', r'\bbuilding\b', r'\blocation\b', r'\blandmark\b', 
                            r'\bspell\b', r'\bitem\b', r'\bquest\b', r'\badventure\b'],
                'target_dir': '03_People'
            },
            'location': {
                'must_have': [r'\blocation\b', r'\bdistrict\b', r'\bbuilding\b', r'\blandmark\b', 
                              r'\bregion\b', r'\bcity\b', r'\btown\b', r'\benvironment\b', r'\barea\b'],
                'must_not': [r'\bNPC\b', r'\bpersonality\b', r'\bclass\b', r'\brace\b', 
                            r'\balignment\b', r'\bSTR\b', r'\bDEX\b'],
                'target_dir': '02_Worldbuilding/Locations'
            },
            'item': {
                'must_have': [r'\bitem\b', r'\bweapon\b', r'\barmor\b', r'\bpotion\b', r'\bartifact\b',
                              r'\bmagic item\b', r'\brarity\b', r'\battunement\b', r'\bproperties\b'],
                'must_not': [r'\bNPC\b', r'\blocation\b', r'\bdistrict\b', r'\bpersonality\b'],
                'target_dir': '04_Resources/Items'
            },
            'quest': {
                'must_have': [r'\bquest\b', r'\badventure\b', r'\bmission\b', r'\bobjective\b', 
                              r'\breward\b', r'\bhook\b', r'\bchallenge\b'],
                'must_not': [r'\bNPC\b', r'\blocation\b', r'\bitem\b', r'\bspell\b'],
                'target_dir': '01_Adventures/Quests'
            },
            'spell': {
                'must_have': [r'\bspell\b', r'\bcantrip\b', r'\britual\b', r'\bspell level\b',
                              r'\bcomponents\b', r'\bduration\b', r'\brange\b', r'\bcasting time\b'],
                'must_not': [r'\bNPC\b', r'\blocation\b', r'\bitem\b', r'\bquest\b'],
                'target_dir': '05_Rules/Spells'
            },
            'rule': {
                'must_have': [r'\brule\b', r'\bmechanic\b', r'\bDC\b', r'\bcheck\b', r'\bmodifier\b',
                              r'\badvantage\b', r'\bdisadvantage\b', r'\bcondition\b'],
                'must_not': [r'\bNPC\b', r'\blocation\b', r'\bquest\b'],
                'target_dir': '05_Rules/Mechanics'
            },
            'lore': {
                'must_have': [r'\bhistory\b', r'\blore\b', r'\blegend\b', r'\bmyth\b', r'\bprophecy\b',
                              r'\bancient\b', r'\btradition\b', r'\bculture\b'],
                'must_not': [r'\bNPC\b', r'\bquest\b', r'\bspell\b', r'\bitem\b'],
                'target_dir': '02_Worldbuilding/Lore'
            },
            'faction': {
                'must_have': [r'\bfaction\b', r'\bguild\b', r'\borganization\b', r'\bcouncil\b',
                              r'\bbrotherhood\b', r'\border\b', r'\bconsortium\b', r'\balliance\b'],
                'must_not': [r'\bNPC\b', r'\blocation\b', r'\bitem\b', r'\bspell\b'],
                'target_dir': '02_Worldbuilding/Factions'
            },
            'session': {
                'must_have': [r'\bsession\b', r'\bcampaign\b', r'\bepisode\b', r'\bplayer\b', r'\bparty\b'],
                'must_not': [r'\bNPC\b', r'\blocation\b', r'\bitem\b', r'\bspell\b'],
                'target_dir': '06_Sessions'
            }
        }
        
    def analyze_content(self, file_path):
        """Analyze file content to determine its true category"""
        try:
            content = file_path.read_text(encoding='utf-8').lower()
            
            # Skip if file is too small
            if len(content) < 50:
                return None
                
            # Check tags first
            if 'tags:' in content:
                for category, patterns in self.category_patterns.items():
                    if category in content[:500]:  # Check in frontmatter
                        return category
                        
            # Score each category based on pattern matches
            scores = {}
            for category, patterns in self.category_patterns.items():
                score = 0
                
                # Check must_have patterns
                for pattern in patterns['must_have']:
                    if re.search(pattern, content):
                        score += 10
                        
                # Check must_not patterns (negative score)
                for pattern in patterns['must_not']:
                    if re.search(pattern, content):
                        score -= 5
                        
                scores[category] = score
                
            # Return category with highest score (if positive)
            best_category = max(scores, key=scores.get)
            if scores[best_category] > 0:
                return best_category
                
            return None
            
        except Exception as e:
            return None
            
    def analyze_directory(self, directory, expected_category=None):
        """Analyze all files in a directory for miscategorization"""
        print(f"\n📁 Analyzing: {directory.name}")
        
        if not directory.exists():
            return
            
        md_files = list(directory.glob("*.md"))[:500]  # Limit to 500 files per directory
        
        # Sample files to understand directory's primary content
        sample_size = min(20, len(md_files))
        if sample_size == 0:
            return
            
        sample_files = random.sample(md_files, sample_size)
        category_counts = defaultdict(int)
        
        # Determine what most files in this directory actually are
        for file_path in sample_files:
            category = self.analyze_content(file_path)
            if category:
                category_counts[category] += 1
                
        # Determine primary category of directory
        if category_counts:
            primary_category = max(category_counts, key=category_counts.get)
            print(f"  Primary content type: {primary_category} ({category_counts[primary_category]}/{sample_size} samples)")
        else:
            primary_category = expected_category
            
        # Now check all files against expected category
        miscategorized_count = 0
        for file_path in md_files:
            self.analyzed += 1
            
            # Skip system files
            if any(skip in file_path.name.lower() for skip in ['index', 'moc', 'template', 'dashboard']):
                continue
                
            actual_category = self.analyze_content(file_path)
            
            # If file doesn't match expected category, mark for moving
            if actual_category and expected_category:
                if actual_category != expected_category:
                    target_dir = self.vault_path / self.category_patterns[actual_category]['target_dir']
                    self.miscategorized.append({
                        'file': file_path,
                        'current_category': expected_category,
                        'actual_category': actual_category,
                        'target_dir': target_dir
                    })
                    miscategorized_count += 1
                    
            if self.analyzed % 100 == 0:
                print(f"  Progress: {self.analyzed} files analyzed, {len(self.miscategorized)} miscategorized")
                
        if miscategorized_count > 0:
            print(f"  ⚠️ Found {miscategorized_count} miscategorized files")
            
    def review_vault(self):
        """Review entire vault for miscategorized files"""
        print("=" * 60)
        print("🔍 INTELLIGENT FILE CATEGORIZATION REVIEW")
        print("=" * 60)
        
        # Check NPCs folder
        npc_dirs = [
            self.vault_path / "03_People",
            self.vault_path / "02_Worldbuilding" / "People",
            self.vault_path / "01_Adventures" / "NPCs"
        ]
        
        for npc_dir in npc_dirs:
            if npc_dir.exists():
                self.analyze_directory(npc_dir, 'npc')
                
        # Check Locations folder
        location_dirs = [
            self.vault_path / "02_Worldbuilding" / "Locations",
            self.vault_path / "02_Worldbuilding" / "Places",
            self.vault_path / "04_Resources" / "Locations"
        ]
        
        for loc_dir in location_dirs:
            if loc_dir.exists():
                self.analyze_directory(loc_dir, 'location')
                
        # Check Items folder
        item_dirs = [
            self.vault_path / "04_Resources" / "Items",
            self.vault_path / "02_Worldbuilding" / "Items"
        ]
        
        for item_dir in item_dirs:
            if item_dir.exists():
                self.analyze_directory(item_dir, 'item')
                
        # Check Quests folder
        quest_dirs = [
            self.vault_path / "01_Adventures" / "Quests",
            self.vault_path / "01_Adventures"
        ]
        
        for quest_dir in quest_dirs:
            if quest_dir.exists():
                self.analyze_directory(quest_dir, 'quest')
                
        # Check Rules folder
        rules_dir = self.vault_path / "05_Rules"
        if rules_dir.exists():
            self.analyze_directory(rules_dir, 'rule')
            
        # Check Lore folder
        lore_dirs = [
            self.vault_path / "02_Worldbuilding" / "Lore",
            self.vault_path / "02_Worldbuilding" / "History"
        ]
        
        for lore_dir in lore_dirs:
            if lore_dir.exists():
                self.analyze_directory(lore_dir, 'lore')
                
    def move_miscategorized_files(self):
        """Move miscategorized files to their correct locations"""
        print(f"\n📦 Moving {len(self.miscategorized)} miscategorized files...")
        
        moved_count = 0
        for item in self.miscategorized[:100]:  # Limit to 100 moves per run
            try:
                source = item['file']
                target_dir = item['target_dir']
                
                # Create target directory if needed
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Generate new path
                target_path = target_dir / source.name
                
                # Handle duplicates
                if target_path.exists():
                    base = target_path.stem
                    suffix = target_path.suffix
                    counter = 1
                    while target_path.exists():
                        target_path = target_dir / f"{base}_{counter}{suffix}"
                        counter += 1
                        
                # Move file
                shutil.move(str(source), str(target_path))
                moved_count += 1
                
                self.moves.append({
                    'from': str(source.relative_to(self.vault_path)),
                    'to': str(target_path.relative_to(self.vault_path)),
                    'category': item['actual_category']
                })
                
                if moved_count % 10 == 0:
                    print(f"  Moved {moved_count} files...")
                    
            except Exception as e:
                print(f"  Error moving {source.name}: {e}")
                
        print(f"  ✓ Moved {moved_count} files to correct categories")
        
    def generate_report(self):
        """Generate categorization report"""
        from datetime import datetime
        
        report_content = f"""# Intelligent File Categorization Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Files Analyzed**: {self.analyzed}
**Miscategorized Found**: {len(self.miscategorized)}
**Files Moved**: {len(self.moves)}

## Summary

Analyzed files across the vault to detect miscategorization based on content patterns.
Files were evaluated against their neighbors and moved to appropriate categories.

## Categories Checked

- **NPCs**: Characters with stats, personality, alignment
- **Locations**: Places, buildings, districts, regions
- **Items**: Weapons, armor, artifacts, potions
- **Quests**: Adventures, missions, objectives
- **Spells**: Magic spells with components and levels
- **Rules**: Game mechanics and conditions
- **Lore**: History, legends, myths, traditions
- **Factions**: Organizations, guilds, councils
- **Sessions**: Campaign notes and player content

## Miscategorized Files Found

### By Current Location
"""
        
        # Group by current location
        by_location = defaultdict(list)
        for item in self.miscategorized[:50]:  # Show first 50
            current = str(item['file'].parent.relative_to(self.vault_path))
            by_location[current].append(item)
            
        for location, items in by_location.items():
            report_content += f"\n**{location}** ({len(items)} files)\n"
            for item in items[:5]:  # Show first 5 per location
                report_content += f"- {item['file'].name} → should be '{item['actual_category']}'\n"
            if len(items) > 5:
                report_content += f"- ... and {len(items)-5} more\n"
                
        report_content += f"""

## Files Moved

### Movement Summary
"""
        
        # Group moves by category
        by_category = defaultdict(list)
        for move in self.moves:
            by_category[move['category']].append(move)
            
        for category, moves in by_category.items():
            report_content += f"\n**{category.title()}** ({len(moves)} files)\n"
            for move in moves[:3]:  # Show first 3 per category
                report_content += f"- {move['from']} → {move['to']}\n"
            if len(moves) > 3:
                report_content += f"- ... and {len(moves)-3} more\n"
                
        report_content += f"""

## Recommendations

1. **Review Moved Files**: Check the moved files to ensure correct categorization
2. **Update Links**: Run a link checker to update any broken links
3. **Tag Consistency**: Consider adding proper tags to all files
4. **Regular Review**: Run this categorization check monthly
5. **Manual Verification**: Spot-check categorizations for accuracy

## Result

✅ Successfully analyzed {self.analyzed} files
✅ Identified {len(self.miscategorized)} miscategorized files
✅ Moved {len(self.moves)} files to correct locations
"""
        
        report_path = self.vault_path / "09_Performance" / f"categorization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report_content, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
    def run(self):
        """Execute the categorization review and correction"""
        self.review_vault()
        
        if self.miscategorized:
            print(f"\n⚠️ Found {len(self.miscategorized)} miscategorized files")
            self.move_miscategorized_files()
        else:
            print("\n✅ No miscategorized files found!")
            
        self.generate_report()
        
        print("\n" + "=" * 60)
        print(f"✅ CATEGORIZATION COMPLETE")
        print(f"   Files Analyzed: {self.analyzed}")
        print(f"   Miscategorized: {len(self.miscategorized)}")
        print(f"   Files Moved: {len(self.moves)}")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    categorizer = IntelligentFileCategorizer(vault_path)
    categorizer.run()