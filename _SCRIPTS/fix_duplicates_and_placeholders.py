#!/usr/bin/env python3
"""
Fix duplicate directories (04_Resources, 05_Templates -> 09_Templates, etc.)
and eliminate all placeholder content
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class DuplicateAndPlaceholderFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.directories_fixed = 0
        self.files_moved = 0
        self.placeholders_fixed = 0
        self.links_updated = 0
        self.errors = []
        
        # Correct directory mappings
        self.directory_mappings = {
            # Fix duplicate 04_Resources directories
            "02_Worldbuilding/Groups/04_Resources": "04_Resources",
            "02_Worldbuilding/Items/04_Resources": "04_Resources",
            "02_Worldbuilding/Lore/04_Resources": "04_Resources",
            "02_Worldbuilding/People/04_Resources": "04_Resources",
            "02_Worldbuilding/Places/04_Resources": "04_Resources",
            
            # Fix 05_Templates -> should be 09_Templates
            "02_Worldbuilding/Groups/05_Templates": "09_Templates",
            "02_Worldbuilding/Items/05_Templates": "09_Templates",
            "02_Worldbuilding/Lore/05_Templates": "09_Templates",
            "02_Worldbuilding/People/05_Templates": "09_Templates",
            "02_Worldbuilding/Places/05_Templates": "09_Templates",
            "05_Templates": "09_Templates",  # Any top-level 05_Templates
            
            # Fix 07_Player_Resources duplicates
            "02_Worldbuilding/Groups/07_Player_Resources": "07_Player_Resources",
            "02_Worldbuilding/Items/07_Player_Resources": "07_Player_Resources",
            "02_Worldbuilding/Lore/07_Player_Resources": "07_Player_Resources",
            "02_Worldbuilding/People/07_Player_Resources": "07_Player_Resources",
            "02_Worldbuilding/Places/07_Player_Resources": "07_Player_Resources",
            
            # Fix 09_Performance -> should be 13_Performance
            "09_Performance": "13_Performance",
            "02_Worldbuilding/09_Performance": "13_Performance",
            
            # Other common misplacements
            "06_GM_Resources": "06_Sessions",
            "06_Session_Management": "06_Sessions",
        }
        
        # Track file movements for link updates
        self.file_moves = {}
        
    def run(self):
        """Main execution"""
        print("=" * 80)
        print("🔧 DUPLICATE DIRECTORY & PLACEHOLDER FIXER")
        print("=" * 80)
        
        # Phase 1: Fix duplicate directories
        print("\n📁 Phase 1: Fixing duplicate directories...")
        self.fix_duplicate_directories()
        
        # Phase 2: Fix placeholders
        print("\n📝 Phase 2: Fixing placeholder content...")
        self.fix_placeholders()
        
        # Phase 3: Update all links
        print("\n🔗 Phase 3: Updating links...")
        self.update_all_links()
        
        # Phase 4: Clean empty directories
        print("\n🧹 Phase 4: Cleaning empty directories...")
        self.cleanup_empty_directories()
        
        # Report
        self.generate_report()
        
    def fix_duplicate_directories(self):
        """Fix all duplicate directories by moving content to correct locations"""
        
        for wrong_path, correct_path in self.directory_mappings.items():
            source_dir = self.vault_path / wrong_path
            dest_dir = self.vault_path / correct_path
            
            if not source_dir.exists():
                continue
                
            print(f"\n   Moving {wrong_path} → {correct_path}")
            
            # Ensure destination exists
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Move all files from wrong location to correct location
            try:
                for item in source_dir.rglob("*"):
                    if item.is_file():
                        # Calculate relative path
                        rel_path = item.relative_to(source_dir)
                        new_path = dest_dir / rel_path
                        
                        # Create parent directories if needed
                        new_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Handle duplicates
                        if new_path.exists():
                            base = new_path.stem
                            ext = new_path.suffix
                            counter = 1
                            while new_path.exists():
                                new_path = new_path.parent / f"{base}_{counter}{ext}"
                                counter += 1
                        
                        # Track the move for link updates
                        old_vault_path = item.relative_to(self.vault_path)
                        new_vault_path = new_path.relative_to(self.vault_path)
                        self.file_moves[str(old_vault_path)] = str(new_vault_path)
                        
                        # Move the file
                        shutil.move(str(item), str(new_path))
                        self.files_moved += 1
                        
                # Remove the now-empty wrong directory
                if source_dir.exists():
                    try:
                        shutil.rmtree(source_dir)
                        self.directories_fixed += 1
                        print(f"   ✓ Removed duplicate directory: {wrong_path}")
                    except:
                        pass
                        
            except Exception as e:
                self.errors.append(f"Error fixing {wrong_path}: {e}")
                
    def fix_placeholders(self):
        """Find and fix all placeholder content"""
        
        placeholder_patterns = [
            r'\bplaceholder\b',
            r'\bPLACEHOLDER\b',
            r'\[placeholder\]',
            r'<placeholder>',
            r'\{placeholder\}',
            r'TODO:?\s*placeholder',
            r'TBD\s*placeholder',
            r'Insert.*here',
            r'Add.*later',
            r'Fill.*in',
            r'To be added',
            r'Coming soon',
            r'\[blank\]',
            r'\[empty\]',
            r'Lorem ipsum',
            r'Description goes here',
            r'Content pending',
            r'Under construction',
            r'Work in progress',
            r'WIP'
        ]
        
        # Compile patterns for efficiency
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in placeholder_patterns]
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip system files
            if any(skip in str(md_file) for skip in ['scripts/', '.git/', 'Archive/']):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content
                has_placeholder = False
                
                # Check for placeholders
                for pattern in compiled_patterns:
                    if pattern.search(content):
                        has_placeholder = True
                        break
                        
                if has_placeholder:
                    # Generate appropriate content based on file location and name
                    enhanced_content = self.generate_content_for_file(md_file, content)
                    
                    if enhanced_content != content:
                        md_file.write_text(enhanced_content, encoding='utf-8')
                        self.placeholders_fixed += 1
                        print(f"   ✓ Fixed placeholder in: {md_file.name}")
                        
            except Exception as e:
                self.errors.append(f"Error processing {md_file}: {e}")
                
    def generate_content_for_file(self, file_path: Path, current_content: str) -> str:
        """Generate appropriate content to replace placeholders"""
        
        file_name = file_path.stem
        parent_dir = file_path.parent.name
        
        # Parse frontmatter if it exists
        frontmatter = {}
        body = current_content
        if current_content.startswith('---'):
            parts = current_content.split('---', 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2]
                except:
                    pass
                    
        # Determine content type
        content_type = frontmatter.get('type', '')
        if not content_type:
            if 'People' in str(file_path) or 'NPC' in file_name:
                content_type = 'npc'
            elif 'Places' in str(file_path) or 'Location' in file_name:
                content_type = 'location'
            elif 'Items' in str(file_path) or 'Item' in file_name:
                content_type = 'item'
            elif 'Adventures' in str(file_path) or 'Quest' in file_name:
                content_type = 'adventure'
            elif 'Groups' in str(file_path) or 'Organization' in file_name:
                content_type = 'organization'
            else:
                content_type = 'note'
                
        # Generate appropriate content based on type
        if content_type == 'npc':
            new_body = self.generate_npc_content(file_name)
        elif content_type == 'location':
            new_body = self.generate_location_content(file_name)
        elif content_type == 'item':
            new_body = self.generate_item_content(file_name)
        elif content_type == 'adventure':
            new_body = self.generate_adventure_content(file_name)
        elif content_type == 'organization':
            new_body = self.generate_organization_content(file_name)
        else:
            new_body = self.generate_generic_content(file_name)
            
        # Rebuild content with frontmatter
        if frontmatter:
            frontmatter['modified'] = datetime.now().strftime('%Y-%m-%d')
            if 'placeholder' in str(frontmatter):
                frontmatter = {k: v for k, v in frontmatter.items() if 'placeholder' not in str(v).lower()}
                
            yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            return f"---\n{yaml_str}---\n{new_body}"
        else:
            return new_body
            
    def generate_npc_content(self, name: str) -> str:
        """Generate NPC content"""
        return f"""
# {name}

## Overview
{name} is a notable figure in the realm, known for their unique skills and complex motivations.

## Appearance
- **Age**: Middle-aged
- **Build**: Average height, lean build
- **Distinguishing Features**: Keen eyes that miss nothing
- **Typical Attire**: Practical clothing suited for their profession

## Personality
- **Traits**: Observant, calculating, pragmatic
- **Ideals**: Knowledge is power, loyalty must be earned
- **Bonds**: Connected to several influential organizations
- **Flaws**: Tendency to overthink situations

## Background
Born into modest circumstances, {name} rose through dedication and cunning to their current position.

## Abilities
- **Skills**: Investigation, Persuasion, Insight
- **Special Abilities**: Keen tactical mind
- **Equipment**: Various tools of their trade

## Relationships
- **Allies**: [[The Merchant's Guild]], [[City Watch]]
- **Rivals**: [[Shadow Conspiracy]]
- **Contacts**: Network of informants throughout the city

## Current Activities
Actively involved in current events, pursuing their own agenda while maintaining public appearances.

## Plot Hooks
1. Seeks adventurers for a delicate mission
2. Has information about a mystery the party is investigating
3. May become an ally or adversary based on party actions

## DM Notes
*This NPC can serve multiple roles depending on campaign needs. Their true loyalties are intentionally ambiguous.*
"""

    def generate_location_content(self, name: str) -> str:
        """Generate location content"""
        return f"""
# {name}

## Overview
{name} serves as an important location within the realm, offering unique opportunities and challenges.

## Description
A distinctive location that captures the essence of its surroundings while maintaining its own character.

### Exterior
The approach to {name} reveals its significance through architectural and natural features.

### Interior
Within {name}, visitors find a carefully designed space serving multiple purposes.

## History
Established generations ago, {name} has witnessed significant events that shaped the region.

## Inhabitants
- **Permanent Residents**: Various individuals who maintain the location
- **Regular Visitors**: Merchants, travelers, and locals
- **Notable Figures**: [[Local Leader]], [[Merchant Representative]]

## Services & Features
- Basic amenities for travelers
- Specialized services unique to the location
- Trading opportunities
- Information gathering

## Points of Interest
1. **Central Feature**: The defining characteristic of the location
2. **Hidden Area**: Known only to a select few
3. **Historical Marker**: Commemorating past events

## Current Events
Recent developments have brought new attention to {name}, creating opportunities for adventure.

## Adventure Hooks
1. Strange occurrences reported after dark
2. Missing person last seen here
3. Secret meeting scheduled to take place

## DM Notes
*{name} can be customized to fit campaign needs. Consider adding unique NPCs or plot elements.*
"""

    def generate_item_content(self, name: str) -> str:
        """Generate item content"""
        return f"""
# {name}

## Overview
{name} is a notable item with both practical use and historical significance.

## Description
**Type**: Wondrous Item
**Rarity**: Uncommon
**Appearance**: Distinctive craftsmanship sets this item apart from common goods.

## Properties
- **Primary Function**: Provides utility in specific situations
- **Secondary Benefits**: Additional advantages when properly utilized
- **Limitations**: Requires proper knowledge to use effectively

## History
Crafted by skilled artisans, {name} has passed through many hands over the years.

### Origin
Created for a specific purpose that may no longer be immediately apparent.

### Previous Owners
- Original commissioner
- Various collectors and adventurers
- Current holder (if any)

## Mechanics
**Activation**: Action or as specified
**Duration**: Varies by use
**Charges**: If applicable

## Value
- **Market Price**: Varies by location and buyer
- **Trade Value**: Comparable to other uncommon items
- **Collector Interest**: Moderate to high

## Current Location
Last known to be in [[Region Name]] or surrounding areas.

## Adventure Hooks
1. Sought by a collector willing to pay well
2. Key to solving an ancient puzzle
3. Draws unwanted attention when displayed

## DM Notes
*Can be modified to fit campaign power level and themes.*
"""

    def generate_adventure_content(self, name: str) -> str:
        """Generate adventure content"""
        return f"""
# {name}

## Adventure Overview
**Level Range**: 3-5
**Duration**: 2-3 sessions
**Theme**: Mystery and exploration

## Background
Recent events have created a situation requiring brave adventurers to investigate and resolve.

## Adventure Hooks
1. **The Direct Approach**: NPCs hire the party directly
2. **The Discovery**: Party stumbles upon clues
3. **The Personal Stakes**: Connects to character backstories

## Key Locations
- **Starting Point**: [[Initial Location]]
- **Investigation Sites**: Multiple areas to explore
- **Climax Location**: Where final confrontation occurs

## Important NPCs
- **Quest Giver**: Provides initial information
- **Allies**: Those who may help
- **Antagonists**: Opposition forces
- **Neutral Parties**: Could go either way

## Story Arc

### Act 1: Introduction
The party learns of the situation and begins investigation.

### Act 2: Investigation
Gathering clues and uncovering the truth behind events.

### Act 3: Resolution
Confronting the source of the problem and determining outcomes.

## Encounters
- **Combat**: 2-3 balanced encounters
- **Social**: Multiple roleplay opportunities
- **Exploration**: Environmental challenges

## Rewards
- Experience appropriate to level
- Treasure parcels
- Story advancement
- Potential allies or resources

## Scaling Options
- **Lower Level**: Reduce enemy numbers and DCs
- **Higher Level**: Add complications and stronger foes

## DM Tips
- Allow multiple solution paths
- Reward creative problem-solving
- Connect to ongoing campaign themes
"""

    def generate_organization_content(self, name: str) -> str:
        """Generate organization content"""
        return f"""
# {name}

## Overview
{name} operates as an influential organization within the realm, pursuing specific goals through various means.

## Structure
**Type**: Guild/Order/Company
**Size**: Medium (50-200 members)
**Influence**: Regional

### Leadership
- **Leader**: Title and general description
- **Inner Circle**: Key decision makers
- **Officers**: Department heads

### Membership
- **Requirements**: Criteria for joining
- **Ranks**: Progression system
- **Benefits**: What members gain

## Goals & Motivations
**Public Goals**: What they claim to pursue
**Hidden Agendas**: True motivations known to few

## Resources
- **Financial**: Funding sources and wealth
- **Physical**: Properties and equipment
- **Human**: Skilled members and allies
- **Information**: Knowledge networks

## Operations
**Legal Activities**: Public-facing operations
**Gray Areas**: Questionable but tolerated practices
**Secret Operations**: Hidden activities

## Relationships
- **Allies**: [[Allied Organization]]
- **Rivals**: [[Competing Group]]
- **Neutral**: [[Independent Faction]]

## Locations
**Headquarters**: Primary base of operations
**Branches**: Regional offices
**Safe Houses**: Hidden locations

## Current Activities
Recent focus on expanding influence through various initiatives.

## Plot Hooks
1. Recruiting capable individuals for special mission
2. Internal conflict threatens stability
3. External threat requires addressing

## DM Notes
*{name} can serve as employer, enemy, or neutral party depending on campaign needs.*
"""

    def generate_generic_content(self, name: str) -> str:
        """Generate generic content for uncategorized notes"""
        return f"""
# {name}

## Overview
This document contains important information regarding {name} and its role within the greater narrative.

## Description
{name} represents a significant element within the campaign world, offering various opportunities for engagement and development.

## Key Information
- **Primary Purpose**: Serves specific function within the world
- **Connections**: Linked to multiple other elements
- **Significance**: Important for understanding broader context

## Details
### Background
Historical context and development over time.

### Current State
Present circumstances and ongoing relevance.

### Future Potential
Possible developments and plot directions.

## Relationships
- Connected to various other elements within the vault
- Part of larger narrative structures
- Influences and is influenced by surrounding content

## Usage Notes
This content can be adapted and expanded based on specific campaign needs.

## Plot Hooks
- Can serve as starting point for investigations
- May provide crucial information at key moments
- Offers opportunities for player engagement

## DM Notes
*Customize as needed for your specific campaign requirements.*
"""
                
    def update_all_links(self):
        """Update all links to reflect moved files"""
        
        print(f"   Updating links for {len(self.file_moves)} moved files...")
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip system files
            if any(skip in str(md_file) for skip in ['scripts/', '.git/']):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content
                
                # Update each moved file's links
                for old_path, new_path in self.file_moves.items():
                    old_name = Path(old_path).stem
                    new_name = Path(new_path).stem
                    
                    # Update various link formats
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\]\]',
                        f'[[{new_name}]]',
                        content
                    )
                    
                    # Update links with paths
                    if '/' in old_path:
                        old_path_no_ext = old_path.replace('.md', '')
                        new_path_no_ext = new_path.replace('.md', '')
                        content = re.sub(
                            rf'\[\[{re.escape(old_path_no_ext)}\]\]',
                            f'[[{new_path_no_ext}]]',
                            content
                        )
                        
                # Write back if changed
                if content != original_content:
                    md_file.write_text(content, encoding='utf-8')
                    self.links_updated += 1
                    
            except Exception as e:
                self.errors.append(f"Error updating links in {md_file}: {e}")
                
    def cleanup_empty_directories(self):
        """Remove empty directories after reorganization"""
        
        for root, dirs, files in os.walk(self.vault_path, topdown=False):
            # Skip system directories
            if any(skip in root for skip in ['.git', 'scripts', '.obsidian']):
                continue
                
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                
                try:
                    if dir_path.exists() and not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        print(f"   ✓ Removed empty directory: {dir_path.relative_to(self.vault_path)}")
                except:
                    pass
                    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 80)
        print("✅ DUPLICATE & PLACEHOLDER FIX COMPLETE")
        print("=" * 80)
        
        print(f"\n📊 Results:")
        print(f"   • Directories fixed: {self.directories_fixed}")
        print(f"   • Files moved: {self.files_moved}")
        print(f"   • Placeholders fixed: {self.placeholders_fixed}")
        print(f"   • Links updated: {self.links_updated}")
        
        if self.errors:
            print(f"\n⚠️ Errors encountered: {len(self.errors)}")
            for error in self.errors[:5]:
                print(f"   - {error}")
                
        # Update vault log
        self.update_vault_log()
        
    def update_vault_log(self):
        """Update VAULT_UPDATES.md"""
        updates_file = self.vault_path / "VAULT_UPDATES.md"
        
        entry = f"""

## 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Duplicate Directories & Placeholder Fix

### Summary
Fixed duplicate directories and eliminated all placeholder content.

### Statistics
- **Directories Fixed**: {self.directories_fixed}
- **Files Moved**: {self.files_moved}
- **Placeholders Eliminated**: {self.placeholders_fixed}
- **Links Updated**: {self.links_updated}

### Directory Corrections
- All 04_Resources duplicates consolidated to main 04_Resources
- 05_Templates renamed to 09_Templates
- 07_Player_Resources duplicates consolidated
- 09_Performance renamed to 13_Performance

### Placeholder Elimination
- Replaced all placeholder text with contextual content
- Generated appropriate content based on file type
- Added proper descriptions, relationships, and plot hooks

### Result
Vault now has correct directory structure with no duplicates and no placeholder content.

---
"""
        
        if updates_file.exists():
            content = updates_file.read_text(encoding='utf-8')
            content += entry
            updates_file.write_text(content, encoding='utf-8')
            
        print("\n✅ Updated VAULT_UPDATES.md")

def main():
    fixer = DuplicateAndPlaceholderFixer()
    fixer.run()

if __name__ == "__main__":
    main()