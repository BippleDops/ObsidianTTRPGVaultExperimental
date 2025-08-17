#!/usr/bin/env python3
"""
Fix vault structure issues and fill placeholder notes
- Flatten duplicate nested directories
- Fill empty/placeholder notes with quality content
- Improve frontmatter cross-linking
"""

import os
import re
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
import random

class VaultStructureFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.files_processed = 0
        self.files_moved = 0
        self.placeholders_filled = 0
        self.crosslinks_added = 0
        self.errors = []
        
        # Track all entities for cross-linking
        self.npcs = []
        self.locations = []
        self.organizations = []
        self.items = []
        self.adventures = []
        
    def run(self):
        """Main execution"""
        print("=" * 80)
        print("🔧 VAULT STRUCTURE & PLACEHOLDER FIXER")
        print("=" * 80)
        
        # First, scan for all entities
        print("\n📊 Phase 1: Scanning vault for entities...")
        self.scan_vault_entities()
        
        # Fix duplicate nested directories
        print("\n🗂️ Phase 2: Fixing duplicate nested directories...")
        self.fix_duplicate_nested_dirs()
        
        # Fill placeholder notes
        print("\n📝 Phase 3: Filling placeholder notes...")
        self.fill_placeholder_notes()
        
        # Improve cross-linking
        print("\n🔗 Phase 4: Improving frontmatter cross-linking...")
        self.improve_crosslinking()
        
        # Generate report
        self.generate_report()
        
    def scan_vault_entities(self):
        """Scan vault to build entity lists for cross-linking"""
        for md_file in self.vault_path.rglob("*.md"):
            relative_path = md_file.relative_to(self.vault_path)
            
            if "03_People" in str(relative_path) or "NPC" in md_file.stem:
                self.npcs.append(md_file.stem)
            elif "04_Places" in str(relative_path) or "Location" in md_file.stem:
                self.locations.append(md_file.stem)
            elif "Groups" in str(relative_path) or "Organization" in md_file.stem:
                self.organizations.append(md_file.stem)
            elif "Items" in str(relative_path):
                self.items.append(md_file.stem)
            elif "01_Adventures" in str(relative_path):
                self.adventures.append(md_file.stem)
                
        print(f"   Found: {len(self.npcs)} NPCs, {len(self.locations)} locations, "
              f"{len(self.organizations)} organizations, {len(self.items)} items")
        
    def fix_duplicate_nested_dirs(self):
        """Fix duplicate nested directory structures"""
        # Find all duplicate nested paths
        duplicate_paths = []
        
        for root, dirs, files in os.walk(self.vault_path):
            root_path = Path(root)
            # Check for patterns like 02_Worldbuilding/*/02_Worldbuilding
            if "02_Worldbuilding" in root:
                parts = root_path.parts
                if parts.count("02_Worldbuilding") > 1:
                    duplicate_paths.append(root_path)
                    
        print(f"   Found {len(duplicate_paths)} duplicate nested directories")
        
        # Process each duplicate path
        for dup_path in duplicate_paths:
            self.flatten_directory(dup_path)
            
    def flatten_directory(self, dup_path: Path):
        """Flatten a duplicate nested directory"""
        # Find the correct parent path
        parts = list(dup_path.parts)
        
        # Find indices of duplicate folder names
        duplicate_indices = []
        for i, part in enumerate(parts):
            if part in ["02_Worldbuilding", "03_People", "04_Places", "01_Adventures"]:
                duplicate_indices.append(i)
                
        if len(duplicate_indices) > 1:
            # Keep only the first occurrence
            correct_parts = parts[:duplicate_indices[1]]
            
            # Add the final folder name if it's different
            final_folder = parts[-1]
            if final_folder not in ["02_Worldbuilding", "03_People", "04_Places", "01_Adventures"]:
                correct_parts.append(final_folder)
                
            correct_path = Path(*correct_parts)
            
            # Move all files from duplicate to correct location
            for file_path in dup_path.rglob("*.md"):
                self.move_file_to_correct_location(file_path, dup_path, correct_path)
                
    def move_file_to_correct_location(self, file_path: Path, old_base: Path, new_base: Path):
        """Move a file from duplicate nested path to correct location"""
        try:
            # Calculate relative path from old base
            relative = file_path.relative_to(old_base)
            
            # Create new path
            new_path = new_base / relative
            
            # Ensure directory exists
            new_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Update any self-referential paths in content
            content = self.update_internal_paths(content, old_base, new_base)
            
            # Write to new location
            new_path.write_text(content, encoding='utf-8')
            
            # Remove old file
            file_path.unlink()
            
            self.files_moved += 1
            print(f"   ✓ Moved: {file_path.name} -> {new_path.parent}")
            
        except Exception as e:
            self.errors.append(f"Error moving {file_path}: {e}")
            
    def update_internal_paths(self, content: str, old_base: Path, new_base: Path):
        """Update internal paths in content"""
        # Update wikilinks that might reference the old path
        old_pattern = str(old_base).replace(str(self.vault_path), "")
        new_pattern = str(new_base).replace(str(self.vault_path), "")
        
        if old_pattern and new_pattern:
            content = content.replace(old_pattern, new_pattern)
            
        return content
        
    def fill_placeholder_notes(self):
        """Fill empty or placeholder notes with quality content"""
        for md_file in self.vault_path.rglob("*.md"):
            try:
                self.process_single_note(md_file)
                self.files_processed += 1
                
                if self.files_processed % 100 == 0:
                    print(f"   Processed {self.files_processed} notes...")
                    
            except Exception as e:
                self.errors.append(f"Error processing {md_file}: {e}")
                
    def process_single_note(self, file_path: Path):
        """Process a single note to fill placeholders and improve content"""
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Parse frontmatter and content
        frontmatter, body = self.parse_note(content)
        
        # Check if it's a placeholder (very short or empty body)
        if len(body.strip()) < 100:
            # Fill based on note type
            filled_body = self.fill_placeholder_content(file_path, frontmatter, body)
            if filled_body != body:
                body = filled_body
                self.placeholders_filled += 1
                print(f"   ✓ Filled placeholder: {file_path.name}")
                
        # Improve frontmatter cross-linking
        improved_frontmatter = self.improve_note_frontmatter(file_path, frontmatter)
        
        # Reconstruct content if changed
        if frontmatter != improved_frontmatter or body != self.parse_note(original_content)[1]:
            new_content = self.reconstruct_note(improved_frontmatter, body)
            file_path.write_text(new_content, encoding='utf-8')
            
    def parse_note(self, content: str) -> tuple:
        """Parse note into frontmatter and body"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2]
                except:
                    frontmatter = {}
                    body = content
            else:
                frontmatter = {}
                body = content
        else:
            frontmatter = {}
            body = content
            
        return frontmatter, body
        
    def reconstruct_note(self, frontmatter: dict, body: str) -> str:
        """Reconstruct note from frontmatter and body"""
        if frontmatter:
            yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            return f"---\n{yaml_str}---\n{body}"
        return body
        
    def fill_placeholder_content(self, file_path: Path, frontmatter: dict, body: str) -> str:
        """Fill placeholder with appropriate content based on type"""
        note_type = frontmatter.get('type', '')
        note_name = file_path.stem
        
        # Determine content type from path or frontmatter
        if 'npc' in note_type.lower() or '03_People' in str(file_path):
            return self.generate_npc_content(note_name, frontmatter)
        elif 'location' in note_type.lower() or '04_Places' in str(file_path):
            return self.generate_location_content(note_name, frontmatter)
        elif 'organization' in note_type.lower() or 'Groups' in str(file_path):
            return self.generate_organization_content(note_name, frontmatter)
        elif 'item' in note_type.lower() or 'Items' in str(file_path):
            return self.generate_item_content(note_name, frontmatter)
        elif 'adventure' in note_type.lower() or '01_Adventures' in str(file_path):
            return self.generate_adventure_content(note_name, frontmatter)
        elif 'lore' in note_type.lower() or 'Lore' in str(file_path):
            return self.generate_lore_content(note_name, frontmatter)
        else:
            return self.generate_generic_content(note_name, frontmatter, body)
            
    def generate_npc_content(self, name: str, frontmatter: dict) -> str:
        """Generate NPC content"""
        race = frontmatter.get('race', random.choice(['Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn']))
        class_type = frontmatter.get('class', random.choice(['Fighter', 'Wizard', 'Rogue', 'Cleric', 'Ranger']))
        
        # Get random connections
        location = random.choice(self.locations) if self.locations else "Unknown Location"
        organization = random.choice(self.organizations) if self.organizations else None
        
        content = f"""
# {name}

## Basic Information
- **Race**: {race}
- **Class**: {class_type}
- **Occupation**: {frontmatter.get('occupation', 'Adventurer')}
- **Location**: [[{location}]]
- **Status**: {frontmatter.get('status', 'Alive')}

## Appearance
{name} is a {race.lower()} {class_type.lower()} with distinctive features that make them memorable. Their weathered appearance speaks to years of experience in their profession.

### Physical Description
- **Age**: {random.randint(25, 60)} years
- **Height**: Average for a {race}
- **Build**: {random.choice(['Lean', 'Muscular', 'Average', 'Stocky'])}
- **Hair**: {random.choice(['Brown', 'Black', 'Blonde', 'Red', 'Gray', 'White'])}
- **Eyes**: {random.choice(['Brown', 'Blue', 'Green', 'Gray', 'Amber'])}
- **Distinguishing Features**: A notable scar or marking that tells a story

## Personality
{name} is known for their {random.choice(['courage', 'wisdom', 'cunning', 'loyalty', 'ambition'])}.

### Traits
- **Personality Trait**: Always has a plan for when things go wrong
- **Ideal**: Freedom - Everyone should be free to pursue their own livelihood
- **Bond**: Protecting those who cannot protect themselves
- **Flaw**: Pride will probably lead to their destruction

## Background
Born and raised in the region, {name} has spent years honing their skills as a {class_type.lower()}. Their past experiences have shaped them into the person they are today.

### History
- Trained in the arts of their profession from a young age
- Experienced a defining moment that set them on their current path
- Has connections throughout [[{location}]]
{"- Member of [[" + organization + "]]" if organization else ""}

## Abilities & Skills
As a skilled {class_type}, {name} possesses:
- Combat proficiency appropriate to their class
- Professional skills related to their occupation
- Knowledge of local customs and politics

## Relationships
- **Allies**: Other members of their profession
- **Rivals**: Those who oppose their goals
- **Contacts**: Merchants, informants, and associates

## Current Activities
{name} is currently involved in:
- Pursuing their professional goals
- Maintaining their position in the community
- Dealing with ongoing challenges

## Motivations
- **Primary Goal**: Achieve recognition in their field
- **Secondary Goal**: Protect their interests and allies
- **Secret Agenda**: Has ambitions beyond what they reveal

## Plot Hooks
1. Can provide information about [[{location}]]
2. Needs assistance with a personal matter
3. Has knowledge crucial to ongoing events
4. Could become an ally or adversary based on party actions

## Quotes
> "In my experience, there's always another way."
> "Trust is earned, not given freely."
> "Every challenge is an opportunity in disguise."

## DM Notes
{name} can serve multiple roles in the campaign:
- Quest giver for appropriate adventures
- Source of information about the region
- Potential ally or rival depending on party actions
- Connection to larger plot threads

### Statistics
*Use {class_type} statistics from the Monster Manual or create custom stats as needed*

## Connected To
- [[{location}]] - Current location
{"- [[" + organization + "]] - Affiliated organization" if organization else ""}
- [[{random.choice(self.npcs) if self.npcs else 'Other NPCs'}]] - Known associate
"""
        return content
        
    def generate_location_content(self, name: str, frontmatter: dict) -> str:
        """Generate location content"""
        location_type = frontmatter.get('location_type', random.choice(['City', 'Town', 'Village', 'Landmark', 'Dungeon']))
        region = frontmatter.get('region', 'The Known Lands')
        
        # Get random connections
        notable_npc = random.choice(self.npcs) if self.npcs else "Notable Figure"
        organization = random.choice(self.organizations) if self.organizations else None
        
        content = f"""
# {name}

## Overview
{name} is a {location_type.lower()} located in {region}. It serves as an important location for travelers and adventurers exploring the region.

## Geography
- **Type**: {location_type}
- **Region**: [[{region}]]
- **Climate**: {random.choice(['Temperate', 'Tropical', 'Arctic', 'Desert', 'Subtropical'])}
- **Terrain**: {random.choice(['Plains', 'Mountains', 'Forest', 'Coastal', 'Hills'])}

## Description
### First Impressions
Upon approaching {name}, visitors are struck by its distinctive character. The {location_type.lower()} presents a unique blend of natural beauty and {"civilization" if location_type in ['City', 'Town'] else "wilderness"}.

### Atmosphere
The air here carries the scent of {random.choice(['pine forests', 'sea salt', 'mountain flowers', 'rich earth', 'ancient stone'])}. Sounds of {"bustling activity" if location_type in ['City', 'Town'] else "nature"} fill the environment.

## Notable Features
1. **Central Landmark**: A distinctive feature that defines the location
2. **Natural Wonder**: An element of the natural landscape worth noting
3. **Architectural Marvel**: A constructed feature of significance
4. **Hidden Secret**: Something not immediately apparent to visitors

## Demographics
- **Population**: {random.randint(50, 5000) if location_type != 'Landmark' else 'Uninhabited'}
- **Primary Race**: {random.choice(['Human', 'Mixed', 'Elf', 'Dwarf'])}
- **Government**: {random.choice(['Council', 'Mayor', 'Elder', 'None']) if location_type != 'Landmark' else 'N/A'}

## Notable NPCs
- [[{notable_npc}]] - Influential resident
- Local authority figure
- Mysterious character with secrets

## Organizations
{"- [[" + organization + "]] - Has presence here" if organization else "- Local guilds and groups"}
- Merchant associations
- Religious orders

## Points of Interest
### Major Locations
1. **The Town Center**: Heart of the community
2. **Market District**: Where commerce thrives
3. **Residential Areas**: Where people make their homes
4. **Special Sites**: Unique to this location

### Hidden Areas
- Secret passages or hidden rooms
- Underground networks
- Forgotten ruins

## History
{name} has a rich history stretching back generations. Founded during the age of expansion, it has witnessed:
- Major historical events
- Changes in rulership
- Economic fluctuations
- Cultural developments

### Timeline
- **Ancient Times**: Original settlement
- **Recent Past**: Significant developments
- **Present Day**: Current situation

## Current Events
- Ongoing political situation
- Economic conditions
- Social tensions or celebrations
- Threats or opportunities

## Resources
- **Natural Resources**: What the land provides
- **Trade Goods**: What is bought and sold
- **Services**: What visitors can find

## Adventure Hooks
1. **The Missing Person**: Someone important has disappeared
2. **The Hidden Threat**: Danger lurks beneath the surface
3. **The Ancient Mystery**: Old secrets wait to be discovered
4. **The Political Intrigue**: Power struggles create opportunities

## Travel Information
### Getting There
- Main roads and paths
- Travel times from major locations
- Hazards along the way

### Getting Around
- Local transportation
- Districts and neighborhoods
- Important landmarks for navigation

## Local Customs
- Traditions unique to this location
- Laws and regulations
- Social expectations
- Festivals and celebrations

## Rumors & Secrets
1. *"They say something stirs in the old ruins..."*
2. *"The mayor isn't who they claim to be..."*
3. *"Strange lights have been seen at night..."*
4. *"An ancient treasure lies hidden nearby..."*

## DM Notes
{name} can serve various purposes:
- Hub for adventures in the region
- Source of supplies and information
- Location for important events
- Base of operations for the party

### Potential Developments
- Political changes could affect the region
- Economic opportunities might arise
- Threats could emerge requiring heroes
- Secrets could be revealed changing everything

## Connections
- [[{region}]] - Part of this region
- [[{notable_npc}]] - Notable resident
{"- [[" + organization + "]] - Active organization" if organization else ""}
- [[{random.choice(self.locations) if len(self.locations) > 1 else 'Nearby Location'}]] - Connected location
"""
        return content
        
    def generate_organization_content(self, name: str, frontmatter: dict) -> str:
        """Generate organization content"""
        org_type = frontmatter.get('type', random.choice(['Guild', 'Cult', 'Government', 'Criminal', 'Religious']))
        
        # Get random connections
        leader = random.choice(self.npcs) if self.npcs else "Unknown Leader"
        headquarters = random.choice(self.locations) if self.locations else "Secret Location"
        
        content = f"""
# {name}

## Overview
{name} is a {org_type.lower()} organization that operates throughout the region. Their influence extends across multiple settlements and their actions shape local politics.

## Basic Information
- **Type**: {org_type}
- **Founded**: Generations ago
- **Headquarters**: [[{headquarters}]]
- **Membership**: {random.randint(10, 500)} members
- **Influence**: {random.choice(['Local', 'Regional', 'National', 'International'])}

## Leadership
### Current Leadership
- **Leader**: [[{leader}]]
- **Second in Command**: Trusted lieutenant
- **Council Members**: Advisory body

### Hierarchy
1. **Leadership Tier**: Decision makers
2. **Officer Tier**: Implementers
3. **Member Tier**: Active participants
4. **Associate Tier**: Supporters and allies

## Purpose & Goals
### Public Mission
The organization publicly claims to:
- Serve the community's interests
- Protect certain values or traditions
- Provide necessary services

### True Objectives
Behind closed doors, they seek to:
- Expand their influence
- Accumulate resources
- Achieve specific long-term goals

### Secret Agenda
*Known only to inner circle:*
- Hidden motivations
- Controversial methods
- Ultimate ambitions

## Structure & Operations
### Organizational Structure
The {name} operates through:
- Formal hierarchy with clear ranks
- Specialized departments or divisions
- Network of contacts and informants

### Standard Operations
- Regular meetings and gatherings
- Ongoing projects and initiatives
- Revenue generating activities
- Member recruitment and training

## Resources & Assets
### Financial Resources
- Treasury and liquid assets
- Income streams
- Investment holdings
- Emergency reserves

### Physical Assets
- Properties and buildings
- Equipment and supplies
- Vehicles and transportation
- Special items or artifacts

### Human Resources
- Skilled specialists
- Loyal operatives
- Informant networks
- Allied organizations

## Members
### Notable Members
- [[{leader}]] - Organization leader
- Key officers and specialists
- Rising stars within the ranks
- Controversial figures

### Membership Requirements
- Qualifications needed to join
- Initiation process
- Ongoing obligations
- Benefits of membership

## Activities
### Regular Activities
- Routine operations
- Member services
- Public functions
- Revenue generation

### Special Operations
- Covert missions
- Strategic initiatives
- Emergency responses
- Long-term projects

## Relationships
### Allies
- Friendly organizations
- Business partners
- Political supporters
- Mutual aid agreements

### Rivals
- Competing organizations
- Political opponents
- Economic competitors
- Ideological enemies

### Neutral Parties
- Potential allies or enemies
- Trading partners
- Information brokers
- Mercenary groups

## Reputation
### Public Perception
How different groups view the organization:
- **Common Folk**: {random.choice(['Suspicious', 'Supportive', 'Fearful', 'Indifferent'])}
- **Nobility**: {random.choice(['Allied', 'Opposed', 'Neutral', 'Manipulative'])}
- **Merchants**: {random.choice(['Profitable', 'Dangerous', 'Necessary', 'Parasitic'])}
- **Authorities**: {random.choice(['Legitimate', 'Tolerated', 'Criminal', 'Unknown'])}

## History
### Founding
The organization was established when:
- Initial circumstances that led to formation
- Founding members and their motivations
- Early challenges and victories

### Major Events
- Significant achievements
- Notable failures
- Turning points
- Recent developments

## Customs & Culture
### Traditions
- Regular ceremonies
- Special observances
- Initiation rites
- Advancement rituals

### Symbols & Identification
- Official insignia
- Secret signs
- Recognition codes
- Uniforms or dress codes

## Current Situation
### Ongoing Concerns
- Active threats
- Internal conflicts
- External pressures
- Resource challenges

### Opportunities
- Expansion possibilities
- Alliance prospects
- Profit ventures
- Power consolidation

## Secrets
1. The organization's true founding purpose
2. Hidden connections to other groups
3. Secret resources or capabilities
4. Controversial past actions

## Plot Hooks
1. **The Recruitment**: The party is approached to join or assist
2. **The Opposition**: The party's actions conflict with the organization
3. **The Investigation**: Strange activities require looking into
4. **The Alliance**: Mutual interests create temporary partnership

## DM Notes
{name} can serve various campaign roles:
- Major antagonist organization
- Potential ally with complications
- Source of quests and missions
- Background political force

### Development Options
- Power struggles within leadership
- Expansion into new territories
- Conflict with rival organizations
- Revelation of secrets

## Connections
- [[{headquarters}]] - Base of operations
- [[{leader}]] - Current leader
- [[{random.choice(self.organizations) if len(self.organizations) > 1 else 'Rival Organization'}]] - Related organization
- [[{random.choice(self.locations) if self.locations else 'Area of Influence'}]] - Territory
"""
        return content
        
    def generate_item_content(self, name: str, frontmatter: dict) -> str:
        """Generate item content"""
        item_type = frontmatter.get('item_type', random.choice(['Weapon', 'Armor', 'Potion', 'Artifact', 'Tool']))
        rarity = frontmatter.get('rarity', random.choice(['Common', 'Uncommon', 'Rare', 'Very Rare', 'Legendary']))
        
        content = f"""
# {name}

## Overview
{name} is a {rarity.lower()} {item_type.lower()} that has found its way into legend through its remarkable properties and storied history.

## Basic Properties
- **Type**: {item_type}
- **Rarity**: {rarity}
- **Attunement**: {random.choice(['Required', 'Not Required', 'Required by a Spellcaster', 'Required by a Warrior'])}
- **Weight**: {random.randint(1, 10)} lbs
- **Value**: {random.randint(100, 10000)} gp

## Description
### Physical Appearance
{name} exhibits exceptional craftsmanship in every detail. The {item_type.lower()} bears distinctive markings that hint at its origins and purpose. Its surface shows signs of age and use, yet remains remarkably preserved.

### Distinctive Features
- Unique visual characteristics
- Special markings or inscriptions
- Unusual materials or construction
- Signs of magical enhancement

## Properties & Abilities
### Base Properties
*As a {item_type}:*
- Standard {item_type.lower()} statistics
- Quality of construction
- Durability and maintenance

### Magical Properties
The item grants the following benefits:
1. **Primary Power**: Main magical effect
2. **Secondary Ability**: Additional benefit
3. **Passive Effect**: Constant enhancement
{"4. **Activated Power**: Special ability with limitations" if rarity in ['Rare', 'Very Rare', 'Legendary'] else ""}

### Curse or Drawback
{"This item carries a curse or limitation:" if rarity in ['Very Rare', 'Legendary'] else "No known curses or drawbacks."}

## History & Lore
### Origins
{name} was created during a significant period in history. The craftsman who made it imbued it with purpose and power beyond ordinary {item_type.lower()}s.

### Previous Owners
1. **Original Owner**: The first to wield it
2. **Historical Figure**: Made it famous
3. **Recent Owner**: Last known possessor

### Legendary Deeds
- Participated in major historical events
- Accomplished impossible tasks
- Changed the course of battles
- Saved or destroyed kingdoms

## Identification
### Detecting Magic
When subjected to magical detection:
- Auras revealed by *Detect Magic*
- School of magic identified
- Strength of enchantment

### Full Identification
Complete understanding requires:
- *Identify* spell or similar magic
- Historical research
- Experimentation with powers
- Discovering command words

## Usage
### Activation
{"- Command word: (Hidden until discovered)" if item_type in ['Artifact', 'Weapon'] else "- No activation required"}
- Gesture or ritual required
- Conditions for use
- Limitations on activation

### Recharge
{"- Regains charges at dawn" if rarity in ['Rare', 'Very Rare', 'Legendary'] else "- No recharge needed"}
- Usage limitations per day
- Special recharge conditions
- Consequences of overuse

## Value & Trade
### Market Value
- Base monetary value
- Factors affecting price
- Interested buyers
- Black market value

### Trade Considerations
- Legal restrictions
- Cultural significance
- Practical difficulties
- Reputation effects

## Current Location
The item is currently:
- In possession of a specific NPC
- Hidden in a dungeon or vault
- Lost to history
- Actively being sought

## Replicas & Fakes
Several copies exist:
- How to identify authentic version
- Quality of replicas
- Who creates fakes
- Consequences of counterfeits

## Quest Hooks
1. **The Search**: Finding the lost item
2. **The Heist**: Stealing it from current owner
3. **The Authentication**: Determining if it's real
4. **The Restoration**: Repairing or recharging it
5. **The Destruction**: Preventing its misuse

## Mechanical Statistics

### 5E Statistics
```
{name}
{item_type}, {rarity.lower()} {"(requires attunement)" if frontmatter.get('attunement', True) else ""}

{"+1 to +3 bonus as appropriate" if item_type in ['Weapon', 'Armor'] else "Effect description"}

{"Special properties based on rarity and type" if rarity != 'Common' else ""}
```

## DM Notes
### Campaign Integration
{name} can serve as:
- Major quest objective
- Reward for significant achievement
- Source of ongoing complications
- Key to larger mystery

### Balance Considerations
- Power level appropriate for party
- Limitations to prevent abuse
- Story implications of possession
- Long-term campaign effects

## Connected Items
- Related artifacts from same creator
- Part of a set with greater power
- Natural opposition to another item
- Required components for ritual

## References
- Source inspiration
- Similar items in lore
- Historical parallels
- Game balance comparisons
"""
        return content
        
    def generate_adventure_content(self, name: str, frontmatter: dict) -> str:
        """Generate adventure content"""
        level_range = frontmatter.get('level', '3-5')
        adventure_type = frontmatter.get('type', random.choice(['Dungeon', 'Investigation', 'Political', 'Wilderness', 'Urban']))
        
        # Get random connections
        location = random.choice(self.locations) if self.locations else "Adventure Location"
        villain = random.choice(self.npcs) if self.npcs else "Main Antagonist"
        
        content = f"""
# {name}

## Adventure Overview
- **Type**: {adventure_type}
- **Levels**: {level_range}
- **Duration**: {random.choice(['One Session', '2-3 Sessions', '4-6 Sessions', 'Mini Campaign'])}
- **Setting**: [[{location}]]
- **Theme**: {random.choice(['Heroism', 'Mystery', 'Survival', 'Politics', 'Horror'])}

## Synopsis
A {adventure_type.lower()} adventure where the party must confront challenges that will test their skills and resolve. The fate of {location} hangs in the balance as dark forces work to achieve their goals.

## Background
### The Situation
Recent events have created a crisis that requires heroic intervention. What started as isolated incidents has escalated into a threat that conventional authorities cannot handle.

### The Threat
[[{villain}]] orchestrates events from the shadows, pursuing goals that will bring disaster if left unchecked. Their plans are already in motion, and time is running short.

### The Stakes
- **Immediate**: Lives are in immediate danger
- **Short-term**: Community stability threatened
- **Long-term**: Regional implications
- **Personal**: Individual party member hooks

## Adventure Hooks
### Primary Hooks
1. **The Direct Request**: An authority figure seeks help
2. **The Personal Connection**: Someone important to a PC is involved
3. **The Chance Encounter**: Party stumbles into the situation
4. **The Moral Obligation**: Ignoring it would have consequences

### Alternative Hooks
- Hired by interested party
- Following up on rumors
- Continuing from previous adventure
- Prophetic dreams or visions

## Act Structure

### Act 1: The Introduction
**Sessions**: 1
**Purpose**: Establish situation and stakes

#### Opening Scene
The adventure begins with immediate action or intrigue that draws the party in.

#### Investigation Phase
- Gathering initial information
- Meeting key NPCs
- Discovering the scope of the problem
- First encounter with opposition

#### Complications
- False leads or misdirection
- Time pressure introduced
- Resources limited
- Allies prove unreliable

### Act 2: The Development
**Sessions**: 1-2
**Purpose**: Deepen mystery and raise stakes

#### Escalation
- Initial threat grows worse
- New complications arise
- Hidden connections revealed
- Opposition becomes active

#### Key Encounters
1. **Combat**: Minions of the antagonist
2. **Social**: Negotiating with factions
3. **Exploration**: Discovering crucial locations
4. **Puzzle**: Overcoming magical or mechanical obstacles

#### Revelations
- True nature of threat exposed
- Antagonist's identity discovered
- Betrayal or surprise alliance
- Ancient history becomes relevant

### Act 3: The Climax
**Sessions**: 1
**Purpose**: Final confrontation and resolution

#### Final Approach
- Last preparations
- Point of no return
- Allies and resources marshaled
- Final clues or advantages gained

#### Climactic Battle
- Confrontation with [[{villain}]]
- Environmental hazards
- Time pressure elements
- Moral choices with consequences

#### Resolution
- Immediate aftermath
- Rewards and recognition
- Loose ends tied up
- Seeds for future adventures

## Key NPCs
### Allies
- **Quest Giver**: Initial contact and sponsor
- **Information Source**: Provides crucial knowledge
- **Unexpected Aid**: Helps at critical moment

### Antagonists
- **Primary**: [[{villain}]]
- **Lieutenant**: Capable subordinate
- **Minions**: Expendable forces
- **Wild Card**: Unpredictable element

### Neutral Parties
- Could be swayed either way
- Have their own agendas
- Provide services for price
- Add complexity to situations

## Locations
### Primary Locations
1. **Starting Point**: Where adventure begins
2. **Investigation Site**: Where clues are found
3. **Conflict Zone**: Where battles occur
4. **Final Location**: Where climax happens

### Secondary Locations
- Safe havens for rest
- Resource locations
- Information sources
- Red herrings

## Encounters
### Combat Encounters
1. **Easy**: Warm-up fight
2. **Medium**: Standard challenge
3. **Hard**: Serious threat
4. **Deadly**: Boss battle

### Non-Combat Challenges
- Social negotiations
- Environmental hazards
- Puzzles and riddles
- Skill challenges

## Treasure & Rewards
### Monetary Rewards
- Appropriate gold for level
- Valuable trade goods
- Titles or property
- Future favors

### Magic Items
- Level-appropriate items
- Story-relevant artifacts
- Consumable resources
- Unique creations

### Story Rewards
- Allies gained
- Reputation improved
- Secrets learned
- Access granted

## Adjusting Difficulty
### For Lower Levels
- Reduce enemy numbers
- Lower save DCs
- Provide more healing
- Add helpful NPCs

### For Higher Levels
- Add legendary actions
- Include environmental hazards
- Add time pressure
- Increase complexity

## Consequences
### Success
- Threat eliminated
- Region stabilized
- Heroes recognized
- New opportunities

### Failure
- Villain achieves goals
- Casualties mount
- Region destabilized
- Future complications

### Partial Success
- Mixed outcomes
- Pyrrhic victory
- Unresolved threads
- Moral ambiguity

## Continuing the Adventure
### Direct Sequels
- Villain returns
- Consequences unfold
- New threat emerges
- Allies need help

### Campaign Integration
- Ties to larger plot
- Recurring NPCs
- Lasting changes
- Character development

## DM Notes
### Preparation Tips
- Read entire adventure first
- Prepare key NPC voices
- Have maps ready
- Anticipate player actions

### Customization
- Adapt to party composition
- Include character backstories
- Adjust to campaign tone
- Modify for setting

### Potential Issues
- Party splits up
- Key NPC killed early
- Puzzle too hard/easy
- Combat imbalanced

## Appendices
### Maps Required
- Regional overview
- Key locations
- Dungeon layouts
- Battle maps

### Stat Blocks
- Custom monsters
- Modified creatures
- NPC statistics
- Environmental hazards

### Handouts
- Clues and letters
- Maps for players
- Puzzle elements
- Prophecies or riddles

## Quick Reference
### Key Information
- Main villain: [[{villain}]]
- Primary location: [[{location}]]
- Central conflict: Power struggle
- Time limit: Before the full moon

### Session Checklist
- [ ] Review previous session
- [ ] Prepare encounters
- [ ] Ready NPC voices
- [ ] Set up maps
- [ ] Prepare handouts
"""
        return content
        
    def generate_lore_content(self, name: str, frontmatter: dict) -> str:
        """Generate lore content"""
        lore_type = frontmatter.get('lore_type', random.choice(['History', 'Legend', 'Religion', 'Culture', 'Magic']))
        
        content = f"""
# {name}

## Overview
{name} represents an important aspect of {lore_type.lower()} that shapes the understanding of the world and its inhabitants.

## Category
- **Type**: {lore_type}
- **Origin**: {random.choice(['Ancient', 'Historical', 'Recent', 'Mythical', 'Unknown'])}
- **Reliability**: {random.choice(['Documented Fact', 'Widely Believed', 'Disputed', 'Legend', 'Rumor'])}
- **Significance**: {random.choice(['World-Shaping', 'Regionally Important', 'Locally Significant', 'Academically Interesting'])}

## The Core Concept
{name} fundamentally deals with the nature of {lore_type.lower()} in the world. This knowledge shapes how people understand their place in the cosmos and their relationship with the forces that govern reality.

## Historical Context
### Origins
The concept of {name} first emerged during a period of great change. Scholars trace its origins to:
- Ancient texts and prophecies
- Oral traditions passed down through generations
- Archaeological discoveries
- Mystical revelations

### Development Over Time
Through the ages, understanding of {name} has evolved:
1. **Ancient Period**: Initial discovery or revelation
2. **Classical Era**: Formalization and study
3. **Middle Period**: Practical applications developed
4. **Modern Era**: Current understanding and debates

## Cultural Impact
### Influence on Society
{name} has shaped civilization in numerous ways:
- Religious and philosophical movements
- Political structures and laws
- Social customs and traditions
- Art, literature, and music

### Regional Variations
Different cultures interpret {name} differently:
- **Northern Traditions**: Emphasis on practical applications
- **Southern Beliefs**: Mystical and spiritual focus
- **Eastern Philosophy**: Integration with natural order
- **Western Approach**: Systematic study and documentation

## Practical Applications
### In Daily Life
Common people encounter {name} through:
- Religious observances
- Cultural practices
- Professional applications
- Folk wisdom

### In Specialized Fields
Experts utilize knowledge of {name} for:
- Magical research and development
- Religious ceremonies and rites
- Academic study and teaching
- Political and social engineering

## Key Figures
### Historical Personalities
- **The Discoverer**: First to document the concept
- **The Prophet**: Spread the knowledge widely
- **The Skeptic**: Challenged accepted beliefs
- **The Revolutionary**: Changed understanding fundamentally

### Contemporary Experts
- Leading scholars and researchers
- Religious authorities
- Practical practitioners
- Popular interpreters

## Schools of Thought
### Orthodox Interpretation
The mainstream understanding holds that:
- Established doctrine is correct
- Traditional practices should be maintained
- Authority should be respected
- Change should be gradual

### Heterodox Views
Alternative perspectives suggest:
- Radical reinterpretation needed
- Hidden truths exist
- Current understanding is flawed
- Revolutionary change required

### Syncretic Approaches
Some attempt to reconcile different views:
- Combining multiple traditions
- Finding common ground
- Creating new synthesis
- Practical compromises

## Mysteries and Controversies
### Unanswered Questions
- Fundamental nature still debated
- Practical limits unknown
- Origins disputed
- Future implications unclear

### Active Debates
Current scholarly arguments focus on:
- Interpretation of ancient texts
- Validity of recent discoveries
- Practical versus theoretical applications
- Moral and ethical implications

## Evidence and Sources
### Primary Sources
- Ancient texts and inscriptions
- Archaeological artifacts
- Eyewitness accounts
- Magical phenomena

### Secondary Analysis
- Scholarly commentaries
- Historical chronicles
- Comparative studies
- Modern research

## Prophecies and Predictions
### Ancient Prophecies
Old texts speak of {name} in terms of:
- Future revelations
- Coming transformations
- Cyclical patterns
- Ultimate destinies

### Modern Interpretations
Contemporary seers and scholars predict:
- Near-term developments
- Long-term trends
- Potential crises
- Opportunities for advancement

## Game Applications
### Adventure Hooks
1. **The Discovery**: New evidence changes everything
2. **The Conspiracy**: Hidden knowledge suppressed
3. **The Quest**: Seeking deeper understanding
4. **The Conflict**: Competing interpretations clash

### Character Connections
- Scholars studying the subject
- Believers following its tenets
- Skeptics challenging assumptions
- Guardians protecting secrets

### World Building
{name} provides:
- Cultural depth and complexity
- Historical continuity
- Conflict sources
- Mystery elements

## Related Topics
### Connected Concepts
- Related philosophical ideas
- Similar historical events
- Parallel cultural developments
- Comparable phenomena

### Opposing Ideas
- Contradictory beliefs
- Competing theories
- Alternative explanations
- Rival traditions

## Truth and Legend
### What Is Known
Established facts about {name}:
- Documented historical events
- Verified magical effects
- Consistent observations
- Reproducible phenomena

### What Is Believed
Common beliefs that may or may not be true:
- Popular interpretations
- Folk explanations
- Religious doctrine
- Cultural assumptions

### What Is Hidden
Secret knowledge known to few:
- Suppressed information
- Dangerous truths
- Protected mysteries
- Forgotten lore

## DM Secrets
*For DM eyes only:*

The truth about {name} is more complex than anyone suspects. Hidden factors include:
- Secret organizations involved
- True historical events different from accepted version
- Magical implications not yet discovered
- Future revelations that will change everything

### Campaign Integration
Use {name} to:
- Provide campaign backbone
- Create long-term mysteries
- Generate conflicts
- Reward deep investigation

## References
- Historical chronicles
- Religious texts
- Scholarly treatises
- Popular accounts
- Secret documents
"""
        return content
        
    def generate_generic_content(self, name: str, frontmatter: dict, existing_body: str) -> str:
        """Generate generic content for untyped notes"""
        # Keep any existing body content
        if existing_body.strip():
            body = existing_body
        else:
            body = ""
            
        # Add generic structure
        content = f"""
# {name}

## Overview
{name} is an important element of the world that intersects with various aspects of the campaign.

{body}

## Description
This entry contains information about {name} and its role in the greater narrative. It connects to multiple other elements throughout the world.

## Significance
### Immediate Relevance
- Current impact on the world
- Active connections to ongoing events
- Practical applications

### Historical Importance
- Past events and influences
- Legacy and lasting effects
- Cultural memory

### Future Potential
- Possible developments
- Emerging threats or opportunities
- Long-term implications

## Connections
### Related Entries
- Similar concepts or entities
- Historical connections
- Thematic links

### Geographic Ties
- Relevant locations
- Regional influences
- Territorial claims

### Social Networks
- Associated individuals
- Organizational involvement
- Cultural groups

## Practical Information
### Common Knowledge
What most people know or believe about {name}:
- Surface-level understanding
- Popular misconceptions
- Cultural associations

### Specialized Knowledge
What experts understand:
- Technical details
- Hidden complexities
- Professional applications

### Secret Knowledge
What few realize:
- Hidden truths
- Suppressed information
- Dangerous secrets

## Current Status
- Present situation
- Recent developments
- Ongoing changes
- Active threats or opportunities

## Adventure Potential
Ways {name} could feature in adventures:
1. Central focus of a quest
2. Background element adding depth
3. Complication to existing plans
4. Source of resources or information

## Development Opportunities
How {name} might evolve:
- Natural progression
- Response to party actions
- External influences
- Random events

## Notes
Additional information and considerations for using {name} in the campaign.

### DM Considerations
- Balance implications
- Story integration
- Player engagement
- Campaign consistency

## References
Links to related information and sources.
"""
        return content
        
    def improve_note_frontmatter(self, file_path: Path, frontmatter: dict) -> dict:
        """Improve frontmatter with better cross-linking"""
        # Ensure basic fields
        if 'title' not in frontmatter:
            frontmatter['title'] = file_path.stem
            
        if 'type' not in frontmatter:
            # Determine type from path
            if '03_People' in str(file_path):
                frontmatter['type'] = 'npc'
            elif '04_Places' in str(file_path):
                frontmatter['type'] = 'location'
            elif 'Groups' in str(file_path):
                frontmatter['type'] = 'organization'
            elif 'Items' in str(file_path):
                frontmatter['type'] = 'item'
            elif '01_Adventures' in str(file_path):
                frontmatter['type'] = 'adventure'
            elif 'Lore' in str(file_path):
                frontmatter['type'] = 'lore'
                
        # Add cross-links based on type
        if frontmatter.get('type') == 'npc' and not frontmatter.get('locations'):
            if self.locations:
                frontmatter['locations'] = random.sample(self.locations, min(3, len(self.locations)))
                self.crosslinks_added += len(frontmatter['locations'])
                
        if frontmatter.get('type') == 'location' and not frontmatter.get('npcs'):
            if self.npcs:
                frontmatter['npcs'] = random.sample(self.npcs, min(5, len(self.npcs)))
                self.crosslinks_added += len(frontmatter['npcs'])
                
        if frontmatter.get('type') == 'organization':
            if not frontmatter.get('members') and self.npcs:
                frontmatter['members'] = random.sample(self.npcs, min(10, len(self.npcs)))
                self.crosslinks_added += len(frontmatter['members'])
            if not frontmatter.get('locations') and self.locations:
                frontmatter['locations'] = random.sample(self.locations, min(3, len(self.locations)))
                self.crosslinks_added += len(frontmatter['locations'])
                
        # Add tags if missing
        if 'tags' not in frontmatter:
            frontmatter['tags'] = []
            
        # Ensure tags based on type
        if frontmatter.get('type') and frontmatter['type'] not in frontmatter.get('tags', []):
            frontmatter['tags'].append(frontmatter['type'])
            
        # Add dates
        if 'created' not in frontmatter:
            frontmatter['created'] = datetime.now().strftime('%Y-%m-%d')
            
        if 'modified' not in frontmatter:
            frontmatter['modified'] = datetime.now().strftime('%Y-%m-%d')
            
        return frontmatter
        
    def improve_crosslinking(self):
        """Improve cross-linking across all notes"""
        for md_file in self.vault_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                frontmatter, body = self.parse_note(content)
                
                # Improve frontmatter links
                improved_fm = self.improve_note_frontmatter(md_file, frontmatter)
                
                if frontmatter != improved_fm:
                    new_content = self.reconstruct_note(improved_fm, body)
                    md_file.write_text(new_content, encoding='utf-8')
                    
            except Exception as e:
                self.errors.append(f"Error improving crosslinks in {md_file}: {e}")
                
    def generate_report(self):
        """Generate final report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'files_processed': self.files_processed,
            'files_moved': self.files_moved,
            'placeholders_filled': self.placeholders_filled,
            'crosslinks_added': self.crosslinks_added,
            'errors': len(self.errors)
        }
        
        # Save JSON report
        report_dir = self.vault_path / "13_Performance"
        report_dir.mkdir(exist_ok=True)
        
        report_file = report_dir / f"structure_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        import json
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print("\n" + "=" * 80)
        print("✅ VAULT STRUCTURE & PLACEHOLDER FIX COMPLETE")
        print("=" * 80)
        print(f"📊 Results:")
        print(f"   • Files processed: {self.files_processed}")
        print(f"   • Files moved: {self.files_moved}")
        print(f"   • Placeholders filled: {self.placeholders_filled}")
        print(f"   • Cross-links added: {self.crosslinks_added}")
        print(f"   • Errors: {len(self.errors)}")
        
        if self.errors:
            print(f"\n⚠️ Errors encountered:")
            for error in self.errors[:10]:
                print(f"   - {error}")

def main():
    fixer = VaultStructureFixer()
    fixer.run()

if __name__ == "__main__":
    main()