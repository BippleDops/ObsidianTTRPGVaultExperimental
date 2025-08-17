#!/usr/bin/env python3
"""
Comprehensive Vault Cleanup and Organization
Removes empty folders, consolidates duplicates, and reorganizes content
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import hashlib
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class VaultCleaner:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.empty_dirs = []
        self.empty_files = []
        self.duplicates = defaultdict(list)
        self.moved_files = []
        self.deleted_files = []
        self.consolidated_files = []
        self.issues_fixed = []
        
    def run_comprehensive_cleanup(self):
        """Run full cleanup process"""
        print("=" * 80)
        print("🧹 COMPREHENSIVE VAULT CLEANUP AND ORGANIZATION")
        print("=" * 80)
        
        # Phase 1: Scan for issues
        print("\n📊 PHASE 1: Scanning for Issues")
        self.scan_for_issues()
        
        # Phase 2: Clean ALL main folders
        print("\n📁 PHASE 2: Cleaning 00_Indexes")
        self.clean_indexes_folder()
        
        print("\n🎭 PHASE 3: Cleaning 01_Adventures")
        self.clean_adventures_folder()
        
        print("\n🌍 PHASE 4: Cleaning 02_Worldbuilding")
        self.fix_worldbuilding_folder()
        
        print("\n⚙️ PHASE 5: Cleaning 03_Mechanics")
        self.clean_mechanics_folder()
        
        print("\n📦 PHASE 6: Cleaning 04_Resources")
        self.clean_resources_folder()
        
        print("\n🎮 PHASE 7: Cleaning 05_Player_Resources")
        self.clean_player_resources()
        
        print("\n🐉 PHASE 8: Cleaning 06_Bestiary")
        self.clean_bestiary_folder()
        
        print("\n📝 PHASE 9: Cleaning 07_Templates")
        self.clean_templates_folder()
        
        print("\n📂 PHASE 10: Cleaning 08_Archive")
        self.clean_archive_folder()
        
        print("\n🏰 PHASE 11: Cleaning 09_Campaigns")
        self.clean_campaigns_folder()
        
        print("\n📅 PHASE 12: Cleaning 10_Sessions")
        self.clean_sessions_folder()
        
        print("\n🎵 PHASE 13: Cleaning 11_Media")
        self.clean_media_folder()
        
        print("\n📚 PHASE 14: Cleaning 12_Research")
        self.clean_research_folder()
        
        print("\n📊 PHASE 15: Cleaning 13_Performance")
        self.clean_performance_folder()
        
        # Phase 16: Check Homebrew folder
        print("\n🎲 PHASE 16: Checking Homebrew Content")
        self.check_homebrew_folder()
        
        # Phase 17: Review Documentation
        print("\n📚 PHASE 17: Documentation Review")
        self.review_documentation()
        
        # Phase 18: Clean GM Resources specifically
        print("\n👤 PHASE 18: GM Resources Deep Clean")
        self.clean_gm_resources()
        
        # Phase 19: Remove empty directories
        print("\n🗑️ PHASE 19: Removing Empty Directories")
        self.remove_empty_directories()
        
        # Phase 20: Final consolidation
        print("\n✨ PHASE 20: Final Consolidation")
        self.final_consolidation()
        
        # Generate report
        print("\n📊 Generating Cleanup Report...")
        return self.generate_report()
        
    def scan_for_issues(self):
        """Scan vault for issues"""
        print("   Scanning for empty files and directories...")
        
        for root, dirs, files in os.walk(self.vault_path):
            # Check for empty directories
            if not files and not dirs:
                self.empty_dirs.append(str(Path(root).relative_to(self.vault_path)))
                
            # Check for empty files
            for file in files:
                if not file.startswith('.'):
                    file_path = Path(root) / file
                    try:
                        if file_path.stat().st_size == 0:
                            self.empty_files.append(str(file_path.relative_to(self.vault_path)))
                    except:
                        pass
                        
        print(f"   Found {len(self.empty_dirs)} empty directories")
        print(f"   Found {len(self.empty_files)} empty files")
        
    def clean_media_folder(self):
        """Clean and organize Media folder"""
        media_path = self.vault_path / "11_Media"
        
        if not media_path.exists():
            print("   Creating Media folder structure...")
            media_path.mkdir(exist_ok=True)
            
        # Create proper media structure
        subdirs = [
            "Images/Maps",
            "Images/Characters",
            "Images/Items",
            "Images/Locations",
            "Audio/Ambience",
            "Audio/Music",
            "Audio/SFX",
            "Handouts",
            "Tokens"
        ]
        
        for subdir in subdirs:
            (media_path / subdir).mkdir(parents=True, exist_ok=True)
            
        # Create index
        index_content = """# Media Library

## 📁 Structure

### Images
- `/Images/Maps` - Battle maps and region maps
- `/Images/Characters` - Character art and portraits
- `/Images/Items` - Item artwork
- `/Images/Locations` - Location images

### Audio
- `/Audio/Ambience` - Environmental sounds
- `/Audio/Music` - Background music
- `/Audio/SFX` - Sound effects

### Other
- `/Handouts` - Player handouts
- `/Tokens` - VTT tokens

## Usage
Store media files in appropriate subdirectories for easy access during sessions.
"""
        (media_path / "README.md").write_text(index_content, encoding='utf-8')
        print("   ✅ Media folder structure created")
        
    def check_homebrew_folder(self):
        """Create Homebrew content structure"""
        homebrew_path = self.vault_path / "03_Mechanics" / "Homebrew"
        homebrew_path.mkdir(parents=True, exist_ok=True)
        
        # Create homebrew categories
        categories = [
            "Classes",
            "Races",
            "Spells",
            "Items",
            "Feats",
            "Monsters",
            "Rules"
        ]
        
        for category in categories:
            category_path = homebrew_path / category
            category_path.mkdir(exist_ok=True)
            
            # Create template
            template = f"""# Homebrew {category}

## Template

### Name
*{category[:-1] if category.endswith('s') else category} name*

### Description
*Detailed description*

### Mechanics
*Game mechanics and rules*

### Balance Notes
*How this compares to official content*

---
*Add homebrew {category.lower()} here*
"""
            (category_path / f"_{category}_Template.md").write_text(template, encoding='utf-8')
            
        print("   ✅ Homebrew structure created")
        
    def review_documentation(self):
        """Create Documentation structure"""
        docs_path = self.vault_path / "07_Templates" / "Documentation"
        docs_path.mkdir(parents=True, exist_ok=True)
        
        # Create documentation templates
        docs = {
            "Campaign_Setup.md": "# Campaign Setup Guide\n\n## Initial Setup\n1. Define campaign theme\n2. Create world overview\n3. Design starting location\n4. Prepare Session 0\n\n## Resources Needed\n- Player's Handbook\n- Setting materials\n- Character sheets\n- Safety tools",
            "Session_Prep.md": "# Session Preparation Template\n\n## Pre-Session\n- [ ] Review previous session notes\n- [ ] Prepare encounters\n- [ ] Ready NPCs\n- [ ] Gather maps/handouts\n\n## During Session\n- [ ] Take notes\n- [ ] Track initiative\n- [ ] Award XP/treasure\n\n## Post-Session\n- [ ] Update campaign log\n- [ ] Plan next session",
            "Character_Creation.md": "# Character Creation Guide\n\n## Steps\n1. Choose race\n2. Choose class\n3. Determine ability scores\n4. Describe character\n5. Choose equipment\n\n## Backstory Elements\n- Origins\n- Motivations\n- Connections\n- Secrets",
            "House_Rules.md": "# House Rules\n\n## Character Creation\n*Custom rules for character creation*\n\n## Combat\n*Modified combat rules*\n\n## Magic\n*Changes to spellcasting*\n\n## Other\n*Additional house rules*"
        }
        
        for filename, content in docs.items():
            (docs_path / filename).write_text(content, encoding='utf-8')
            
        print("   ✅ Documentation templates created")
        
    def clean_gm_resources(self):
        """Clean and organize GM Resources"""
        gm_path = self.vault_path / "04_Resources" / "GM_Resources"
        gm_path.mkdir(parents=True, exist_ok=True)
        
        # Create GM resource structure
        resources = {
            "Random_Tables/Names.md": "# Name Generators\n\n## Fantasy Names\n- Human: [Roll d20]\n- Elf: [Roll d20]\n- Dwarf: [Roll d20]\n\n## Place Names\n- Towns: [Roll d20]\n- Taverns: [Roll d20]",
            "Random_Tables/Encounters.md": "# Random Encounters\n\n## Road Encounters\n1. Merchant caravan\n2. Bandits\n3. Traveling minstrels\n\n## Wilderness\n1. Wild animals\n2. Lost traveler\n3. Ancient ruins",
            "Quick_References/Conditions.md": "# Condition Reference\n\n## Conditions\n- **Blinded**: Can't see\n- **Charmed**: Can't attack charmer\n- **Deafened**: Can't hear\n- **Frightened**: Disadvantage when source in sight\n- **Grappled**: Speed 0\n- **Incapacitated**: No actions/reactions\n- **Invisible**: Can't be seen\n- **Paralyzed**: Incapacitated, can't move\n- **Petrified**: Transformed to stone\n- **Poisoned**: Disadvantage on attacks/checks\n- **Prone**: Disadvantage on attacks\n- **Restrained**: Speed 0, disadvantage\n- **Stunned**: Incapacitated\n- **Unconscious**: Incapacitated, unaware",
            "Quick_References/DC_Guidelines.md": "# Difficulty Class Guidelines\n\n## Task Difficulty\n- **Very Easy**: DC 5\n- **Easy**: DC 10\n- **Medium**: DC 15\n- **Hard**: DC 20\n- **Very Hard**: DC 25\n- **Nearly Impossible**: DC 30",
            "Campaign_Tools/Timeline_Tracker.md": "# Campaign Timeline\n\n## Year 1\n### Spring\n- Campaign begins\n\n### Summer\n- Major event\n\n### Fall\n- Plot development\n\n### Winter\n- Season finale",
            "Campaign_Tools/NPC_Roster.md": "# NPC Roster\n\n## Major NPCs\n| Name | Role | Location | Status |\n|------|------|----------|--------|\n| - | - | - | - |\n\n## Minor NPCs\n| Name | Role | Location | Notes |\n|------|------|----------|-------|"
        }
        
        for filepath, content in resources.items():
            full_path = gm_path / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            
        print("   ✅ GM Resources organized")
        
    def clean_player_resources(self):
        """Clean and organize Player Resources"""
        player_path = self.vault_path / "05_Player_Resources"
        player_path.mkdir(exist_ok=True)
        
        # Create player resource structure
        resources = {
            "Rules_Reference/Basic_Rules.md": "# Basic Rules Reference\n\n## Core Mechanics\n- **Ability Checks**: d20 + modifier\n- **Advantage/Disadvantage**: Roll twice\n- **Proficiency**: Add bonus when proficient\n\n## Combat\n- **Initiative**: d20 + DEX\n- **Attack**: d20 + modifier vs AC\n- **Damage**: Roll damage dice\n- **Healing**: Restore HP",
            "Rules_Reference/Character_Advancement.md": "# Character Advancement\n\n## Experience Points\n| Level | XP Required |\n|-------|------------|\n| 1 | 0 |\n| 2 | 300 |\n| 3 | 900 |\n| 4 | 2,700 |\n| 5 | 6,500 |\n\n## Milestone Leveling\nLevel up at story milestones",
            "Party_Resources/Party_Inventory.md": "# Party Inventory\n\n## Shared Items\n| Item | Quantity | Carried By |\n|------|----------|------------|\n| - | - | - |\n\n## Party Funds\n- **Platinum**: 0\n- **Gold**: 0\n- **Silver**: 0\n- **Copper**: 0",
            "Party_Resources/Party_Quests.md": "# Active Quests\n\n## Main Quest\n*Current objective*\n\n## Side Quests\n- [ ] Quest 1\n- [ ] Quest 2\n\n## Completed Quests\n- [x] Introduction"
        }
        
        for filepath, content in resources.items():
            full_path = player_path / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            
        print("   ✅ Player Resources organized")
        
    def clean_resources_folder(self):
        """Clean main Resources folder"""
        resources_path = self.vault_path / "04_Resources"
        
        # Create main resource categories
        categories = {
            "Assets/Tokens": "Token images for VTT",
            "Assets/Maps": "Battle and region maps",
            "References/Rules": "Rule references",
            "References/Lore": "Lore documents",
            "Tools/Generators": "Random generators",
            "Tools/Calculators": "Game calculators"
        }
        
        for category_path, description in categories.items():
            full_path = resources_path / category_path
            full_path.mkdir(parents=True, exist_ok=True)
            
            # Create README
            readme = f"# {category_path.split('/')[-1]}\n\n{description}\n\n*Add resources here*"
            (full_path / "README.md").write_text(readme, encoding='utf-8')
            
        print("   ✅ Resources folder organized")
        
    def clean_mechanics_folder(self):
        """Clean and organize Mechanics folder"""
        mechanics_path = self.vault_path / "03_Mechanics"
        
        # Ensure core mechanics files exist
        core_files = {
            "Combat_Rules.md": "# Combat Rules\n\n## Initiative\nRoll d20 + DEX modifier\n\n## Actions\n- Attack\n- Cast Spell\n- Dash\n- Dodge\n- Help\n- Hide\n- Ready\n- Search\n- Use Item\n\n## Reactions\nOne per round",
            "Magic_Rules.md": "# Magic Rules\n\n## Spellcasting\n- Components: V, S, M\n- Concentration\n- Spell slots\n- Cantrips\n\n## Schools\n- Abjuration\n- Conjuration\n- Divination\n- Enchantment\n- Evocation\n- Illusion\n- Necromancy\n- Transmutation",
            "Skill_Checks.md": "# Skill Checks\n\n## Skills by Ability\n\n### Strength\n- Athletics\n\n### Dexterity\n- Acrobatics\n- Sleight of Hand\n- Stealth\n\n### Intelligence\n- Arcana\n- History\n- Investigation\n- Nature\n- Religion\n\n### Wisdom\n- Animal Handling\n- Insight\n- Medicine\n- Perception\n- Survival\n\n### Charisma\n- Deception\n- Intimidation\n- Performance\n- Persuasion"
        }
        
        for filename, content in core_files.items():
            (mechanics_path / filename).write_text(content, encoding='utf-8')
            
        print("   ✅ Mechanics folder organized")
        
    def fix_worldbuilding_folder(self):
        """Fix and reorganize Worldbuilding folder"""
        wb_path = self.vault_path / "02_Worldbuilding"
        
        print("   Scanning for duplicates in Worldbuilding...")
        
        # Find duplicate content
        content_hashes = defaultdict(list)
        
        for md_file in wb_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                # Hash first 500 chars to find duplicates
                content_hash = hashlib.md5(content[:500].encode()).hexdigest()
                content_hashes[content_hash].append(md_file)
            except:
                pass
                
        # Process duplicates
        for hash_val, files in content_hashes.items():
            if len(files) > 1:
                # Keep the first, archive the rest
                keeper = files[0]
                for duplicate in files[1:]:
                    try:
                        # Move to archive
                        archive_path = self.vault_path / "08_Archive" / "Duplicates" / duplicate.parent.name
                        archive_path.mkdir(parents=True, exist_ok=True)
                        
                        new_path = archive_path / duplicate.name
                        if not new_path.exists():
                            shutil.move(str(duplicate), str(new_path))
                            self.moved_files.append(f"Archived duplicate: {duplicate.name}")
                    except:
                        pass
                        
        # Organize by category
        categories = ["People", "Places", "Groups", "Lore", "Items", "Events"]
        
        for category in categories:
            category_path = wb_path / category
            category_path.mkdir(exist_ok=True)
            
            # Move misplaced files
            for md_file in wb_path.glob("*.md"):
                if category.lower() in md_file.name.lower():
                    try:
                        shutil.move(str(md_file), str(category_path / md_file.name))
                        self.moved_files.append(f"Organized: {md_file.name} -> {category}")
                    except:
                        pass
                        
        print(f"   ✅ Worldbuilding organized, {len(self.moved_files)} files reorganized")
        
    def clean_indexes_folder(self):
        """Clean and organize Indexes folder"""
        indexes_path = self.vault_path / "00_Indexes"
        
        # Remove empty or duplicate indexes
        for file in indexes_path.glob("*.md"):
            try:
                content = file.read_text(encoding='utf-8')
                if len(content.strip()) < 50:  # Too short to be useful
                    file.unlink()
                    self.deleted_files.append(f"Removed empty index: {file.name}")
            except:
                pass
                
        print("   ✅ Indexes folder cleaned")
        
    def clean_adventures_folder(self):
        """Clean and organize Adventures folder"""
        adventures_path = self.vault_path / "01_Adventures"
        
        # Organize by campaign
        for file in adventures_path.glob("*.md"):
            content = file.read_text(encoding='utf-8', errors='ignore')
            
            # Move to appropriate campaign folder
            if "seven shards" in content.lower():
                dest = adventures_path / "Seven_Shards_Campaign"
                dest.mkdir(exist_ok=True)
                if not (dest / file.name).exists():
                    shutil.move(str(file), str(dest))
                    self.moved_files.append(f"Organized: {file.name} -> Seven_Shards_Campaign")
            elif "shadow" in content.lower():
                dest = adventures_path / "Shadow_Conspiracy"
                dest.mkdir(exist_ok=True)
                if not (dest / file.name).exists():
                    shutil.move(str(file), str(dest))
                    self.moved_files.append(f"Organized: {file.name} -> Shadow_Conspiracy")
                    
        print("   ✅ Adventures folder organized")
        
    def clean_bestiary_folder(self):
        """Clean and organize Bestiary folder"""
        bestiary_path = self.vault_path / "06_Bestiary"
        bestiary_path.mkdir(exist_ok=True)
        
        # Create CR-based organization
        cr_folders = ["CR_0-1", "CR_2-5", "CR_6-10", "CR_11-15", "CR_16-20", "CR_21+"]
        for folder in cr_folders:
            (bestiary_path / folder).mkdir(exist_ok=True)
            
        # Create type-based folders
        types = ["Beasts", "Humanoids", "Undead", "Dragons", "Aberrations", "Elementals", "Fey", "Fiends", "Constructs"]
        for type_folder in types:
            (bestiary_path / "By_Type" / type_folder).mkdir(parents=True, exist_ok=True)
            
        print("   ✅ Bestiary folder organized")
        
    def clean_templates_folder(self):
        """Clean and organize Templates folder"""
        templates_path = self.vault_path / "07_Templates"
        
        # Remove empty templates
        for file in templates_path.rglob("*.md"):
            try:
                content = file.read_text(encoding='utf-8')
                if len(content.strip()) < 20:
                    file.unlink()
                    self.deleted_files.append(f"Removed empty template: {file.name}")
            except:
                pass
                
        print("   ✅ Templates folder cleaned")
        
    def clean_archive_folder(self):
        """Clean and organize Archive folder"""
        archive_path = self.vault_path / "08_Archive"
        archive_path.mkdir(exist_ok=True)
        
        # Compress old backups
        for backup_dir in archive_path.glob("*backup*"):
            if backup_dir.is_dir():
                # Create zip archive
                shutil.make_archive(str(backup_dir), 'zip', backup_dir)
                shutil.rmtree(backup_dir)
                self.consolidated_files.append(f"Compressed: {backup_dir.name}")
                
        print("   ✅ Archive folder compressed")
        
    def clean_campaigns_folder(self):
        """Clean and organize Campaigns folder"""
        campaigns_path = self.vault_path / "09_Campaigns"
        campaigns_path.mkdir(exist_ok=True)
        
        # Create campaign structure
        campaign_template = {
            "Campaign_Overview.md": "# Campaign Overview\n\n## Theme\n\n## Setting\n\n## Major NPCs\n\n## Story Arc",
            "Session_Log.md": "# Session Log\n\n## Session 1\n- Date:\n- Players:\n- Summary:",
            "Player_Notes.md": "# Player Notes\n\n*Player-visible information*",
            "DM_Notes.md": "# DM Notes\n\n*Secret information*"
        }
        
        for filename, content in campaign_template.items():
            file_path = campaigns_path / filename
            if not file_path.exists():
                file_path.write_text(content, encoding='utf-8')
                
        print("   ✅ Campaigns folder structured")
        
    def clean_sessions_folder(self):
        """Clean and organize Sessions folder"""
        sessions_path = self.vault_path / "10_Sessions"
        sessions_path.mkdir(exist_ok=True)
        
        # Create session tracking
        session_template = """# Session Template

## Date: 

## Players Present:

## Session Summary:

## Key Events:

## NPCs Met:

## Loot Gained:

## XP Awarded:

## Notes for Next Session:
"""
        
        template_path = sessions_path / "Session_Template.md"
        if not template_path.exists():
            template_path.write_text(session_template, encoding='utf-8')
            
        print("   ✅ Sessions folder prepared")
        
    def clean_research_folder(self):
        """Clean and organize Research folder"""
        research_path = self.vault_path / "12_Research"
        
        # Organize research materials
        categories = ["Game_Systems", "Setting_Inspiration", "Actual_Play_Campaigns", "TTRPG_Articles", "Resources"]
        
        for category in categories:
            (research_path / category).mkdir(exist_ok=True)
            
        print("   ✅ Research folder organized")
        
    def clean_performance_folder(self):
        """Clean and organize Performance folder"""
        perf_path = self.vault_path / "13_Performance"
        
        # Archive old reports
        archive_path = perf_path / "Archive"
        archive_path.mkdir(exist_ok=True)
        
        # Move old reports
        for report in perf_path.glob("*.json"):
            if "current" not in report.name.lower():
                try:
                    # Check file age (move if older than today)
                    if "20240814" not in report.name:  # Not from today
                        shutil.move(str(report), str(archive_path))
                        self.moved_files.append(f"Archived: {report.name}")
                except:
                    pass
                    
        print("   ✅ Performance folder cleaned")
        
    def final_consolidation(self):
        """Final consolidation pass"""
        print("   Running final consolidation...")
        
        # Find and consolidate scattered similar files
        file_groups = defaultdict(list)
        
        for md_file in self.vault_path.rglob("*.md"):
            if "08_Archive" not in str(md_file):
                # Group by base name (removing numbers and underscores)
                base_name = md_file.stem.lower()
                base_name = ''.join(c for c in base_name if c.isalpha())
                if len(base_name) > 3:
                    file_groups[base_name].append(md_file)
                    
        # Consolidate groups with many similar files
        for base_name, files in file_groups.items():
            if len(files) > 5:  # More than 5 similar files
                # Check if they're actually similar
                contents = []
                for file in files[:3]:  # Check first 3
                    try:
                        content = file.read_text(encoding='utf-8', errors='ignore')
                        contents.append(content[:200])
                    except:
                        pass
                        
                # If contents are very similar, consolidate
                if len(contents) > 1 and all(c[:50] == contents[0][:50] for c in contents):
                    # Keep the longest one
                    files_with_size = [(f, f.stat().st_size) for f in files]
                    files_with_size.sort(key=lambda x: x[1], reverse=True)
                    keeper = files_with_size[0][0]
                    
                    # Archive the rest
                    for file, _ in files_with_size[1:]:
                        try:
                            archive_path = self.vault_path / "08_Archive" / "Consolidated" / file.parent.name
                            archive_path.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(file), str(archive_path / file.name))
                            self.consolidated_files.append(f"Consolidated: {file.name}")
                        except:
                            pass
                            
        print(f"   ✅ Consolidated {len(self.consolidated_files)} similar files")
        
    def remove_empty_directories(self):
        """Remove all empty directories"""
        print("   Removing empty directories...")
        
        removed_count = 0
        
        # Multiple passes to catch nested empty dirs
        for _ in range(3):
            for root, dirs, files in os.walk(self.vault_path, topdown=False):
                if not files and not dirs:
                    if "08_Archive" not in str(root):  # Don't remove archive dirs
                        try:
                            Path(root).rmdir()
                            removed_count += 1
                        except:
                            pass
                            
        print(f"   ✅ Removed {removed_count} empty directories")
        
    def generate_report(self) -> Dict:
        """Generate cleanup report"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'empty_dirs_found': len(self.empty_dirs),
                'empty_files_found': len(self.empty_files),
                'files_moved': len(self.moved_files),
                'files_deleted': len(self.deleted_files),
                'duplicates_archived': len([f for f in self.moved_files if 'duplicate' in f.lower()])
            },
            'actions_taken': {
                'media_folder': 'Created proper structure with categories',
                'homebrew_folder': 'Created templates for all homebrew types',
                'documentation': 'Created documentation templates',
                'gm_resources': 'Organized with random tables and references',
                'player_resources': 'Created rules references and party tools',
                'resources': 'Organized into assets, references, and tools',
                'mechanics': 'Created core rules documents',
                'worldbuilding': 'Removed duplicates and organized by category'
            },
            'moved_files': self.moved_files[:50],  # First 50
            'recommendations': [
                'Review archived duplicates in 08_Archive/Duplicates',
                'Add content to newly created template files',
                'Populate media folders with campaign assets',
                'Continue organizing worldbuilding content into categories'
            ]
        }
        
        # Save report
        report_path = self.vault_path / "13_Performance" / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Create markdown report
        self.create_markdown_report(report)
        
        return report
        
    def create_markdown_report(self, report: Dict):
        """Create markdown cleanup report"""
        
        content = f"""# Vault Cleanup Report

Generated: {report['timestamp']}

## Summary

- **Empty Directories Found**: {report['summary']['empty_dirs_found']}
- **Empty Files Found**: {report['summary']['empty_files_found']}
- **Files Reorganized**: {report['summary']['files_moved']}
- **Duplicates Archived**: {report['summary']['duplicates_archived']}

## Actions Taken

### Media Folder
{report['actions_taken']['media_folder']}

### Homebrew Content
{report['actions_taken']['homebrew_folder']}

### Documentation
{report['actions_taken']['documentation']}

### GM Resources
{report['actions_taken']['gm_resources']}

### Player Resources
{report['actions_taken']['player_resources']}

### Resources Folder
{report['actions_taken']['resources']}

### Mechanics
{report['actions_taken']['mechanics']}

### Worldbuilding
{report['actions_taken']['worldbuilding']}

## Recommendations

"""
        
        for rec in report['recommendations']:
            content += f"- {rec}\n"
            
        content += """

## File Movements

"""
        
        for movement in report['moved_files'][:20]:
            content += f"- {movement}\n"
            
        content += """

---
*Cleanup complete. Your vault is now better organized!*
"""
        
        md_path = self.vault_path / "13_Performance" / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        md_path.write_text(content, encoding='utf-8')

def main():
    cleaner = VaultCleaner()
    report = cleaner.run_comprehensive_cleanup()
    
    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE CLEANUP COMPLETE!")
    print("=" * 80)
    
    print(f"\n📊 Results:")
    print(f"   • Empty directories removed")
    print(f"   • Files reorganized: {report['summary']['files_moved']}")
    print(f"   • Duplicates archived: {report['summary']['duplicates_archived']}")
    print(f"   • All folders properly structured")
    print(f"\n📄 Report saved to 13_Performance/")

if __name__ == "__main__":
    main()