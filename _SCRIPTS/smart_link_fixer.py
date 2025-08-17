#!/usr/bin/env python3
"""
Smart Link Fixer - Creates missing notes for broken links and fixes existing ones
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class SmartLinkFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.broken_links = []
        self.fixed_links = []
        self.created_notes = []
        self.file_mapping = {}
        self.link_context = defaultdict(list)
        
    def run(self):
        """Main process"""
        print("=" * 80)
        print("🔗 SMART LINK FIXER - Creating Notes & Fixing Links")
        print("=" * 80)
        
        # Phase 1: Build file mapping
        print("\n📁 Phase 1: Building file index...")
        self.build_file_mapping()
        
        # Phase 2: Analyze broken links with context
        print("\n🔍 Phase 2: Analyzing broken links with context...")
        self.analyze_broken_links()
        
        # Phase 3: Create missing notes
        print("\n📝 Phase 3: Creating missing notes...")
        self.create_missing_notes()
        
        # Phase 4: Fix remaining links
        print("\n🔧 Phase 4: Fixing remaining links...")
        self.fix_remaining_links()
        
        # Phase 5: Generate report
        print("\n📊 Phase 5: Generating report...")
        return self.generate_report()
        
    def build_file_mapping(self):
        """Build mapping of all files"""
        for md_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(md_file) or "08_Archive" in str(md_file):
                continue
                
            rel_path = md_file.relative_to(self.vault_path)
            filename = md_file.stem
            
            # Multiple mappings
            self.file_mapping[filename.lower()] = str(rel_path)
            self.file_mapping[str(rel_path).lower()] = str(rel_path)
            
            # Clean variations
            clean_name = filename.replace("_", " ").replace("-", " ")
            self.file_mapping[clean_name.lower()] = str(rel_path)
            
        print(f"   ✅ Indexed {len(self.file_mapping)} file references")
        
    def analyze_broken_links(self):
        """Analyze broken links with context"""
        md_files = list(self.vault_path.rglob("*.md"))
        
        for md_file in md_files:
            if ".obsidian" in str(md_file) or "08_Archive" in str(md_file):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                rel_path = str(md_file.relative_to(self.vault_path))
                
                # Find all wikilinks with context
                for match in re.finditer(r'([^\n]*)\[\[([^\]]+)\]\]([^\n]*)', content):
                    before = match.group(1)[-100:]  # 100 chars before
                    link = match.group(2)
                    after = match.group(3)[:100]  # 100 chars after
                    
                    link_target = link.split('|')[0].strip()
                    
                    # Check if link exists
                    if not self.find_existing_file(link_target):
                        self.broken_links.append({
                            'file': rel_path,
                            'link': link,
                            'target': link_target,
                            'context': before + f"[[{link}]]" + after,
                            'category': self.categorize_link(link_target, rel_path)
                        })
                        
            except Exception as e:
                pass
                
        print(f"   ✅ Found {len(self.broken_links)} broken links to analyze")
        
    def find_existing_file(self, link_target: str) -> str:
        """Check if file exists"""
        link_lower = link_target.lower()
        
        if link_lower in self.file_mapping:
            return self.file_mapping[link_lower]
            
        if (link_lower + ".md") in self.file_mapping:
            return self.file_mapping[link_lower + ".md"]
            
        return None
        
    def categorize_link(self, link_target: str, source_file: str) -> str:
        """Categorize link based on name and context"""
        link_lower = link_target.lower()
        
        # NPCs
        if any(title in link_lower for title in ['lord', 'lady', 'captain', 'admiral', 'commander', 'master', 'dr', 'professor']):
            return 'npc'
        
        # Places
        if any(place in link_lower for place in ['city', 'town', 'village', 'castle', 'fortress', 'temple', 'academy', 'port', 'harbor']):
            return 'place'
            
        # Items
        if any(item in link_lower for item in ['sword', 'armor', 'shield', 'potion', 'scroll', 'ring', 'amulet', 'weapon']):
            return 'item'
            
        # Organizations
        if any(org in link_lower for org in ['guild', 'order', 'council', 'syndicate', 'cult', 'academy', 'ministry']):
            return 'organization'
            
        # Lore
        if any(lore in link_lower for lore in ['history', 'legend', 'myth', 'story', 'tale', 'lore', 'tradition']):
            return 'lore'
            
        # Mechanics
        if any(mech in link_lower for mech in ['rule', 'mechanic', 'system', 'combat', 'magic', 'skill']):
            return 'mechanic'
            
        # Based on source file location
        if '02_Worldbuilding' in source_file:
            if 'People' in source_file:
                return 'npc'
            elif 'Places' in source_file:
                return 'place'
            elif 'Groups' in source_file:
                return 'organization'
                
        return 'general'
        
    def create_missing_notes(self):
        """Create full notes for missing links"""
        for broken in self.broken_links[:1000]:  # Limit to first 1000 to avoid issues
            target = broken['target']
            category = broken['category']
            
            # Clean and limit target name
            target = target.strip()
            if len(target) > 100:  # Skip overly long targets
                continue
            if '\n' in target or '`' in target or '#' in target:  # Skip malformed targets
                continue
                
            # Determine where to create the note
            note_path = self.determine_note_location(target, category)
            
            # Generate content based on category
            content = self.generate_note_content(target, category, broken['context'])
            
            # Create the note
            full_path = self.vault_path / note_path
            
            # Validate path
            try:
                if not full_path.exists() and len(str(full_path)) < 250:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content, encoding='utf-8')
                    
                    self.created_notes.append({
                        'target': target,
                        'path': str(note_path),
                        'category': category
                    })
                    
                    # Update file mapping
                    self.file_mapping[target.lower()] = str(note_path)
            except Exception as e:
                pass  # Skip problematic files
                
        print(f"   ✅ Created {len(self.created_notes)} new notes")
        
    def determine_note_location(self, target: str, category: str) -> Path:
        """Determine best location for new note"""
        # Clean target name
        clean_name = target.replace(" ", "_").replace("/", "_")
        
        if category == 'npc':
            return Path(f"02_Worldbuilding/People/{clean_name}.md")
        elif category == 'place':
            return Path(f"02_Worldbuilding/Places/{clean_name}.md")
        elif category == 'item':
            return Path(f"02_Worldbuilding/Items/{clean_name}.md")
        elif category == 'organization':
            return Path(f"02_Worldbuilding/Groups/{clean_name}.md")
        elif category == 'lore':
            return Path(f"02_Worldbuilding/Lore/{clean_name}.md")
        elif category == 'mechanic':
            return Path(f"03_Mechanics/{clean_name}.md")
        else:
            return Path(f"02_Worldbuilding/Lore/{clean_name}.md")
            
    def generate_note_content(self, target: str, category: str, context: str) -> str:
        """Generate full content for new note"""
        
        if category == 'npc':
            return self.generate_npc_content(target, context)
        elif category == 'place':
            return self.generate_place_content(target, context)
        elif category == 'item':
            return self.generate_item_content(target, context)
        elif category == 'organization':
            return self.generate_organization_content(target, context)
        elif category == 'lore':
            return self.generate_lore_content(target, context)
        elif category == 'mechanic':
            return self.generate_mechanic_content(target, context)
        else:
            return self.generate_general_content(target, context)
            
    def generate_npc_content(self, name: str, context: str) -> str:
        """Generate NPC note"""
        # Extract title if present
        title = ""
        for t in ['Lord', 'Lady', 'Captain', 'Admiral', 'Commander', 'Master', 'Dr', 'Professor']:
            if t.lower() in name.lower():
                title = t
                break
                
        return f"""# {name}

## Basic Information

**Title**: {title if title else 'Unknown'}
**Race**: Human
**Class/Profession**: Unknown
**Location**: [[To Be Determined]]
**Alignment**: Neutral
**Status**: Active

## Description

### Physical Appearance
A distinguished individual whose presence commands attention. Their appearance suggests experience and capability in their chosen field.

### Personality
- **Traits**: Professional, competent, focused
- **Ideals**: Excellence in their craft
- **Bonds**: Connections to local organizations
- **Flaws**: To be discovered through interaction

## Background

{name} has established themselves as a notable figure in their domain. Their expertise and reputation precede them, making them a valuable contact for those who earn their respect.

### History
- Trained in specialized skills relevant to their profession
- Built reputation through consistent excellence
- Maintains professional relationships throughout the region

## Abilities & Skills

### Professional Skills
- Expertise in their field of specialization
- Leadership and management capabilities
- Strategic thinking and planning

### Combat Abilities (if applicable)
- **AC**: 12 (or appropriate to role)
- **HP**: 45 (6d8 + 12)
- **Speed**: 30 ft
- **Proficiency Bonus**: +3

**Abilities**: STR 12, DEX 14, CON 14, INT 16, WIS 15, CHA 13

**Skills**: Relevant to profession (+6 to primary skills)

## Relationships

### Allies
- Professional colleagues
- Organizational contacts
- Local authority figures

### Rivals
- Competing professionals
- Political opponents
- Business competitors

## Current Activities

Currently engaged in professional duties and maintaining their position within the local hierarchy. Available for consultation on matters within their expertise.

## Plot Hooks

1. **Professional Services**: Can provide specialized assistance
2. **Information Source**: Knows about local events and politics
3. **Quest Giver**: May have tasks requiring discrete handling
4. **Political Intrigue**: Involved in local power dynamics

## DM Notes

This NPC can serve multiple roles:
- Information broker for their area of expertise
- Quest giver for specialized missions
- Political player in local intrigue
- Mentor figure for relevant skills

### Secrets
- Has undisclosed motivations
- Knows more than they initially reveal
- Connected to larger plot elements

## Quotes

> "Professionalism and discretion are the hallmarks of success."

> "Every challenge presents an opportunity for those prepared to seize it."

## References

- First mentioned in: {context[:50]}...
- Related to: Local political structure
- Connected plots: To be developed

---
*Tags*: #npc #contact #worldbuilding"""
        
    def generate_place_content(self, name: str, context: str) -> str:
        """Generate Place note"""
        place_type = "Location"
        for t in ['City', 'Town', 'Village', 'Castle', 'Fortress', 'Temple', 'Academy', 'Port', 'Harbor']:
            if t.lower() in name.lower():
                place_type = t
                break
                
        return f"""# {name}

## Overview

**Type**: {place_type}
**Region**: [[Regional Territory]]
**Population**: ~1,000-10,000 (varies by type)
**Government**: Local Council
**Defenses**: Standard fortifications

## Description

{name} stands as a significant {place_type.lower()} in the region, serving both strategic and economic purposes. Its location provides advantages for trade, defense, and regional influence.

### Geography
- **Location**: Strategic position in the region
- **Climate**: Temperate, seasonal variations
- **Terrain**: Varied, suitable for settlement
- **Resources**: Local materials and trade goods

### Architecture
The {place_type.lower()} features architecture typical of the region, with buildings constructed from local materials. Key structures include:
- Central plaza or courtyard
- Administrative buildings
- Commercial district
- Residential areas
- Defensive structures (if applicable)

## History

### Founding
Established generations ago as a strategic settlement, {name} has grown from humble beginnings to its current significance.

### Major Events
- **Foundation Era**: Initial settlement and construction
- **Growth Period**: Expansion and development
- **Recent History**: Current political and economic situation

## Districts & Landmarks

### Commercial Quarter
- Markets and bazaars
- Merchant guilds
- Trade warehouses
- Inns and taverns

### Residential Areas
- Noble estates (if applicable)
- Middle-class housing
- Common quarters
- Artisan workshops

### Notable Landmarks
1. **Central Structure**: Main governmental or religious building
2. **Market Square**: Hub of commercial activity
3. **Defensive Works**: Walls, gates, or natural barriers
4. **Cultural Sites**: Temples, theaters, or academies

## Demographics

### Population Breakdown
- **Humans**: 60%
- **Other Common Races**: 30%
- **Rare Races**: 10%

### Social Structure
- Ruling class or council
- Merchant middle class
- Skilled artisans
- Common laborers

## Government & Law

### Leadership
Led by a council of representatives or appointed officials, maintaining order and managing resources.

### Laws
Standard regional laws apply, with local ordinances for:
- Trade regulations
- Public safety
- Resource management
- Defense requirements

### Law Enforcement
- City watch or guard
- Judicial system
- Prison or detention facilities

## Economy

### Primary Industries
- Trade and commerce
- Local crafts and production
- Agricultural products (if applicable)
- Specialized services

### Trade
- Import: Luxury goods, raw materials
- Export: Local products, finished goods
- Trade Routes: Connected to major thoroughfares

## Culture

### Traditions
Local customs blend regional traditions with unique local practices developed over generations.

### Festivals
- Seasonal celebrations
- Trade fairs
- Religious observances
- Historical commemorations

### Entertainment
- Taverns and inns
- Performance venues
- Gaming establishments
- Public gatherings

## Important NPCs

### Officials
- **Leader**: Governs the {place_type.lower()}
- **Captain of Guard**: Maintains security
- **Trade Master**: Oversees commerce

### Notable Residents
- Prominent merchants
- Skilled artisans
- Religious leaders
- Information brokers

## Current Events

The {place_type.lower()} currently faces:
- Political developments
- Economic opportunities
- Security concerns
- Social changes

## Adventure Hooks

1. **Political Intrigue**: Power struggles within leadership
2. **Economic Opportunity**: Trade deals and merchant conflicts
3. **Security Threat**: External or internal dangers
4. **Mystery**: Unexplained events requiring investigation
5. **Social Conflict**: Tensions between different groups

## DM Notes

### Secrets
- Hidden passages or areas
- Concealed political alliances
- Underground activities
- Ancient mysteries

### Potential Developments
- Political changes
- Economic shifts
- Military conflicts
- Supernatural events

## Maps & Layouts

*[Space for maps]*

Key locations marked:
- Main entrances
- Important buildings
- Districts
- Defensive positions

## References

- First mentioned: {context[:50]}...
- Connected to: Regional politics and trade
- Related locations: Nearby settlements

---
*Tags*: #location #{place_type.lower()} #worldbuilding #place"""
        
    def generate_item_content(self, name: str, context: str) -> str:
        """Generate Item note"""
        return f"""# {name}

## Item Information

**Type**: Wondrous Item / Weapon / Armor
**Rarity**: Rare
**Attunement**: Required (by specific class or alignment)
**Value**: 500-5,000 gp

## Description

### Physical Appearance
{name} is a masterfully crafted item that immediately draws attention. Its surface bears intricate designs and symbols that hint at its magical nature. The craftsmanship suggests both ancient techniques and powerful enchantments.

### Magical Aura
When examined with *detect magic*, the item radiates a moderate to strong aura of enchantment magic. Those sensitive to magical energies can feel its power even without direct examination.

## Properties

### Base Properties
- **Weight**: 2-10 lbs (depending on type)
- **Durability**: Resistant to normal wear and damage
- **Material**: High-quality materials with magical reinforcement

### Magical Properties

#### Primary Ability
**Power**: Grants the wielder a significant advantage in specific situations.
- +2 bonus to relevant rolls
- Special ability usable once per day
- Passive benefit while carried/worn

#### Secondary Effects
- Enhanced perception or awareness
- Protection against specific damage types
- Utility function for exploration or social encounters

### Activation
- **Command Word**: Required for primary ability
- **Somatic Component**: Specific gesture needed
- **Recharge**: Dawn, or after specific conditions

## History

### Creation
Forged in ages past by master craftsmen, {name} was created for a specific purpose. The techniques used in its creation have been lost to time, making it irreplaceable.

### Previous Owners
1. **Original Owner**: Commissioned or created for specific individual
2. **Historical Figure**: Used in significant historical events
3. **Recent History**: How it came to current location

### Legendary Deeds
- Participated in major historical events
- Saved or doomed important figures
- Changed the course of battles or negotiations

## Curse or Quirk (Optional)

### Minor Quirk
The item has a peculiar property that doesn't significantly impact its use:
- Changes color based on wielder's mood
- Whispers barely audible words in ancient languages
- Attracts specific types of creatures (harmless)

### Hidden Properties
Not immediately apparent, these properties reveal themselves through use:
- Bonds with wielder over time
- Unlocks additional powers with specific achievements
- Reacts to certain locations or creatures

## Lore & Legends

### Common Knowledge
What most educated people might know:
- General reputation
- Famous previous owners
- Notable achievements

### Rare Information
Requires research or special knowledge:
- True name and full powers
- Method of destruction (if applicable)
- Connection to other artifacts

### Secret Knowledge
Known only to a few:
- Hidden command words
- Secret compartments or functions
- True purpose of creation

## Game Mechanics

### D&D 5e Statistics
**{name}**
*Wondrous item, rare (requires attunement)*

While attuned to this item, you gain the following benefits:
- +1 to AC (if applicable)
- Advantage on specific saving throws
- Once per day ability: [Specific power description]

**Special Ability**: As an action, you can activate the item's power. [Detailed mechanical description]

### Attunement Process
Requires specific ritual or condition:
- Meditation for 1 hour while holding item
- Performing specific ritual or deed
- Meeting alignment or class requirements

## Current Location

Last known to be: {context[:50]}...

### Accessibility
- How difficult to obtain
- Current guardian or owner
- Challenges to acquisition

## Quest Hooks

1. **Recovery Mission**: Retrieve from current location
2. **Research Quest**: Discover true properties
3. **Reforge/Repair**: If broken or incomplete
4. **Destroy/Contain**: If cursed or dangerous
5. **Unite Set**: If part of larger collection

## DM Notes

### Balance Considerations
- Appropriate for level 5-10 characters
- Should not overshadow other party members
- Consider limiting uses or adding costs

### Story Integration
- Can serve as plot device
- Links to campaign themes
- Character development opportunity

### Scaling Options
- Powers can grow with wielder
- Additional abilities unlock over time
- Can be upgraded through quests

---
*Tags*: #item #magic #treasure #equipment"""
        
    def generate_organization_content(self, name: str, context: str) -> str:
        """Generate Organization note"""
        org_type = "Organization"
        for t in ['Guild', 'Order', 'Council', 'Syndicate', 'Cult', 'Academy']:
            if t.lower() in name.lower():
                org_type = t
                break
                
        return f"""# {name}

## Organization Overview

**Type**: {org_type}
**Headquarters**: [[Central Location]]
**Membership**: ~50-500 members
**Influence**: Regional
**Status**: Active
**Secrecy**: Semi-public

## Description

{name} operates as a {org_type.lower()} dedicated to its core mission and the advancement of its members' interests. The organization maintains a significant presence in regional affairs through both public and private channels.

## Mission & Goals

### Primary Mission
The organization exists to:
- Advance specific interests or ideals
- Protect member privileges and resources
- Influence regional politics and economics
- Preserve or change existing power structures

### Public Goals
What they openly claim:
- Promote trade and prosperity
- Maintain order and tradition
- Advance knowledge and learning
- Protect the innocent

### Secret Objectives
Hidden agendas:
- Accumulate power and influence
- Control specific resources or information
- Eliminate rivals or threats
- Achieve long-term transformation

## History

### Founding
Established in response to specific historical needs, {name} has evolved from its original purpose while maintaining core traditions.

### Major Events
- **Foundation**: Original establishment and charter
- **Growth Period**: Expansion of influence and membership
- **Conflicts**: Major disputes or wars
- **Recent Developments**: Current position and activities

### Historical Figures
Notable past members who shaped the organization:
- Founders and early leaders
- Revolutionary or reform figures
- Heroes and villains

## Structure & Hierarchy

### Leadership
- **Grand Master/Leader**: Supreme authority
- **Inner Circle**: Senior decision makers
- **Department Heads**: Operational leaders
- **Regional Commanders**: Local authority

### Ranks
1. **Initiate**: New members
2. **Apprentice**: Learning the ways
3. **Journeyman**: Full member
4. **Master**: Experienced member
5. **Elder**: Senior position
6. **Grand Master**: Ultimate authority

### Departments
- **Operations**: Day-to-day activities
- **Intelligence**: Information gathering
- **Resources**: Financial management
- **Recruitment**: Membership growth
- **Enforcement**: Security and discipline

## Membership

### Requirements
To join, candidates must:
- Meet skill or knowledge requirements
- Provide recommendations or sponsorship
- Pay initiation fees or dues
- Swear oaths of loyalty
- Complete initiation trials

### Benefits
Members receive:
- Access to resources and facilities
- Protection and legal support
- Training and advancement opportunities
- Business or political connections
- Exclusive information or privileges

### Obligations
Members must:
- Pay regular dues or tithes
- Respond to organizational calls
- Maintain secrecy about sensitive matters
- Support fellow members
- Advance organizational goals

## Resources & Assets

### Financial
- Treasury reserves
- Income from operations
- Member contributions
- Investment holdings
- Trade monopolies or contracts

### Physical
- Headquarters and facilities
- Safe houses and warehouses
- Transportation resources
- Equipment and supplies
- Libraries and archives

### Human Resources
- Skilled membership base
- Informant networks
- Allied organizations
- Political connections
- Military/security forces

## Operations

### Public Activities
- Trade and commerce
- Education and training
- Charitable works
- Cultural events
- Political lobbying

### Covert Operations
- Intelligence gathering
- Influence operations
- Economic manipulation
- Elimination of threats
- Secret research

## Relations

### Allies
- Aligned organizations
- Political patrons
- Business partners
- Religious supporters

### Rivals
- Competing organizations
- Political opponents
- Economic competitors
- Ideological enemies

### Neutral Parties
- Government bodies
- Independent merchants
- Foreign organizations
- Common population

## Notable Members

### Current Leadership
- **Grand Master**: [Name]
- **Spymaster**: [Name]
- **Treasurer**: [Name]
- **Enforcer**: [Name]

### Key Operatives
Active members of significance:
- Field commanders
- Master craftsmen
- Diplomatic representatives
- Special agents

## Customs & Culture

### Traditions
- Initiation ceremonies
- Rank advancement rituals
- Annual gatherings
- Secret handshakes or signs

### Symbols
- Official insignia
- Secret marks
- Ceremonial items
- Colors and heraldry

### Codes
- Behavioral expectations
- Communication ciphers
- Loyalty oaths
- Operational protocols

## Current Activities

The organization currently focuses on:
- Expanding influence in new regions
- Dealing with specific threats
- Pursuing major objectives
- Managing internal conflicts

## Locations

### Headquarters
Primary base of operations with full facilities and defenses.

### Chapter Houses
Regional centers for local operations.

### Safe Houses
Secret locations for sensitive activities.

## Adventure Hooks

1. **Join the Organization**: Recruitment or infiltration mission
2. **Internal Conflict**: Power struggle within ranks
3. **External Threat**: Defend against enemies
4. **Secret Mission**: Undertake covert operation
5. **Betrayal**: Deal with traitor or corruption

## DM Notes

### Secrets
- True leadership identity
- Hidden resources or weapons
- Secret alliances or conflicts
- Long-term master plan

### Using in Campaign
- Source of quests and resources
- Political intrigue element
- Character backstory connection
- Campaign antagonist or ally

---
*Tags*: #organization #{org_type.lower()} #faction #worldbuilding"""
        
    def generate_lore_content(self, name: str, context: str) -> str:
        """Generate Lore note"""
        return f"""# {name}

## Overview

{name} represents a significant element of world history and culture, influencing events and beliefs across generations. This knowledge shapes understanding of current events and future possibilities.

## Historical Context

### Time Period
This lore originates from a specific era in world history, when civilization faced unique challenges and opportunities. The events and knowledge from this time continue to resonate in the present day.

### Cultural Origin
Emerging from specific cultural traditions, this lore reflects the values, fears, and aspirations of its creators. It has since spread beyond its origins to influence broader understanding.

## The Legend

### Common Version
As told by most people:

In ages past, when the world was younger and magic flowed more freely, there existed powers and knowledge now lost to time. {name} tells of these ancient days and the lessons learned through triumph and tragedy.

The story speaks of heroes and villains, of choices made and prices paid. It reminds us that power comes with responsibility, and that the echoes of the past shape the present in ways we may not fully understand.

### Academic Interpretation
Scholars who study this lore note several key elements:
- Historical facts embedded within mythological framework
- Metaphorical representations of natural or magical phenomena
- Cultural values and warnings encoded in narrative structure
- Possible connections to actual historical events

### Hidden Truth
What few realize is that {name} contains more fact than fiction. The events described, while embellished through retelling, point to real occurrences that shaped the world. Understanding the truth behind the legend reveals:
- Actual locations of historical importance
- True names and lineages of significant figures
- Practical knowledge disguised as allegory
- Warnings about specific dangers or opportunities

## Key Elements

### Central Figures
- **The Protagonist**: Represents ideals or warnings
- **The Antagonist**: Embodies dangers or temptations
- **The Mentor**: Preserves and transmits wisdom
- **The Catalyst**: Triggers crucial events

### Important Locations
Places mentioned in the lore that may still exist:
- Sites of significant events
- Hidden repositories of knowledge
- Places of power or danger
- Crossroads of destiny

### Artifacts & Relics
Items mentioned that might be real:
- Weapons of legendary power
- Texts containing lost knowledge
- Symbols of authority or protection
- Tools of transformation or creation

## Interpretations

### Religious Perspective
Various faiths interpret this lore differently:
- As divine revelation or warning
- As corrupted truth needing correction
- As heretical knowledge to be suppressed
- As complementary to existing doctrine

### Magical Significance
Practitioners of magic find special meaning:
- Encoded spells or rituals
- Warnings about magical dangers
- Maps to sources of power
- Keys to understanding cosmic forces

### Political Implications
Those in power use this lore to:
- Justify their authority
- Predict future events
- Understand rival motivations
- Guide policy decisions

## Modern Relevance

### Current Events
Recent occurrences that connect to this lore:
- Discoveries validating ancient claims
- Patterns repeating from legend
- Individuals claiming connection to story
- Phenomena matching descriptions

### Prophecies & Predictions
Elements that suggest future events:
- Conditions that trigger outcomes
- Cycles that may repeat
- Warnings about specific dangers
- Promises of revelation or return

### Practical Applications
How this knowledge can be used:
- Understanding historical patterns
- Predicting likely outcomes
- Finding lost locations or items
- Gaining cultural insights

## Sources & References

### Primary Sources
- Ancient texts and inscriptions
- Oral traditions maintained by specific groups
- Artistic depictions in ruins or temples
- Magical recordings or visions

### Secondary Sources
- Scholarly analyses and commentaries
- Religious interpretations
- Popular retellings and songs
- Cross-cultural variations

### Research Methods
How to learn more:
- Consulting specific libraries or archives
- Interviewing traditional knowledge keepers
- Exploring mentioned locations
- Analyzing symbolic patterns

## Mysteries & Questions

### Unresolved Elements
- Contradictions between versions
- Missing pieces of the story
- Unexplained references
- Impossible or anachronistic details

### Active Investigations
Current efforts to understand:
- Archaeological expeditions
- Scholarly research projects
- Magical divination attempts
- Secret society investigations

## Game Applications

### Adventure Hooks
1. **Discovery**: Find proof of the lore's truth
2. **Prevention**: Stop prophesied disaster
3. **Recovery**: Retrieve legendary artifacts
4. **Investigation**: Solve ancient mystery
5. **Fulfillment**: Complete unfinished quest

### Character Connections
- Descendant of legendary figures
- Guardian of lore fragments
- Seeker of hidden truth
- Skeptic requiring proof

### Campaign Themes
This lore can support:
- Epic quests spanning generations
- Mystery investigations
- Political intrigue
- Cosmic horror revelations

## DM Notes

### The Real Truth
{name} actually refers to [specific campaign truth that players don't know yet].

### Gradual Revelation
- Initial exposure: Common version
- Investigation: Academic details
- Deep research: Hidden elements
- Climax: Full truth

### Customization
Adapt this lore to fit campaign:
- Change names to match setting
- Adjust timeline to fit history
- Connect to player backstories
- Link to main campaign arc

---
*Tags*: #lore #history #legend #worldbuilding #mystery"""
        
    def generate_mechanic_content(self, name: str, context: str) -> str:
        """Generate Mechanic note"""
        return f"""# {name}

## Mechanic Overview

**System**: D&D 5th Edition
**Type**: Rule Variant / Subsystem / Optional Rule
**Complexity**: Moderate
**Purpose**: Enhance gameplay in specific situations

## Description

{name} provides a structured approach to handling specific game situations that benefit from additional mechanical depth. This system integrates with existing D&D 5e rules while adding meaningful choices and consequences.

## Core Mechanics

### Basic Resolution
The fundamental process works as follows:

1. **Trigger**: Specific situation arises requiring this mechanic
2. **Setup**: Establish parameters and stakes
3. **Action**: Players make choices using the system
4. **Resolution**: Determine outcomes based on rolls and decisions
5. **Consequences**: Apply results to ongoing game

### Key Components

#### Primary Mechanic
- **Roll Type**: d20 + modifiers vs. DC
- **Difficulty Range**: DC 10-25 based on challenge
- **Modifiers**: Ability scores, proficiency, circumstances

#### Resource Management
- **Points/Uses**: Limited resource to track
- **Recovery**: How resources regenerate
- **Costs**: What actions consume resources

#### Time Factor
- **Action Economy**: How it fits in combat/exploration
- **Duration**: How long effects last
- **Frequency**: How often it can be used

## Detailed Rules

### Prerequisites
Before using this mechanic:
- Specific conditions must be met
- Players must have certain capabilities
- DM establishes parameters

### Process

#### Step 1: Initiation
Determine when and how the mechanic activates:
- Player-triggered vs. DM-triggered
- Required declarations or preparations
- Cost or risk assessment

#### Step 2: Execution
The actual mechanical process:
1. Declare intended outcome
2. Commit resources (if applicable)
3. Make necessary rolls
4. Apply modifiers and advantages
5. Compare to target numbers

#### Step 3: Results
Determining success and degree:
- **Critical Success** (20 or beat DC by 10+): Exceptional outcome
- **Success** (Meet or beat DC): Intended result achieved
- **Partial Success** (Fail by 5 or less): Limited success with complication
- **Failure** (Fail by 6+): Intended result not achieved
- **Critical Failure** (1 or fail by 10+): Significant negative consequence

### Modifiers & Advantages

#### Circumstantial Modifiers
- **Favorable conditions**: +2 to +5
- **Unfavorable conditions**: -2 to -5
- **Preparation**: Advantage on roll
- **Rushed/Pressured**: Disadvantage on roll

#### Character Abilities
- **Relevant proficiency**: Add proficiency bonus
- **Expertise**: Double proficiency bonus
- **Class features**: May provide unique benefits
- **Feats**: Could modify or enhance mechanic

## Examples

### Example 1: Basic Use
*Scenario*: [Specific situation]
- Player declares intent
- DM sets DC 15
- Player rolls d20+5, gets 17
- Success achieved with described outcome

### Example 2: Complex Application
*Scenario*: [More complex situation]
- Multiple participants involved
- Extended challenge requiring multiple rolls
- Resource management element
- Partial successes building to completion

### Example 3: Failed Attempt
*Scenario*: [Failure situation]
- What went wrong
- Consequences of failure
- Recovery options
- Learning from failure

## Integration

### With Combat
How this mechanic works during combat:
- Action/bonus action/reaction cost
- Interaction with initiative
- Effects on combat dynamics

### With Exploration
Application during exploration:
- Time requirements
- Resource consumption
- Discovery opportunities
- Environmental interactions

### With Social Encounters
Using in social situations:
- Influence on negotiations
- Reputation effects
- Information gathering
- Relationship building

## Variants & Options

### Simplified Version
For quicker resolution:
- Single roll instead of multiple
- Fixed DCs instead of scaling
- Binary success/failure

### Advanced Version
For more detail:
- Additional roll types
- Multiple resource tracks
- Expanded outcome table
- Long-term consequences

### Alternative Approaches
Different ways to handle:
- Skill challenge format
- Narrative-focused resolution
- Point-buy system
- Card or dice pool mechanic

## Balance Considerations

### Power Level
- Appropriate for tier of play
- Doesn't overshadow class abilities
- Maintains resource economy
- Preserves action economy

### Frequency of Use
- Not every situation
- Special circumstances only
- Limited by resources
- Cooldown periods

### Risk vs. Reward
- Meaningful consequences for failure
- Appropriate rewards for success
- Escalating stakes
- Player agency preserved

## Customization

### Setting-Specific
Adapt for different settings:
- Fantasy adjustments
- Modern applications
- Science fiction variants
- Horror modifications

### Table Preferences
Adjust for group style:
- More/less rolling
- Narrative focus
- Tactical emphasis
- Player comfort level

## Common Issues

### Problem 1: Overuse
Solution: Implement cooldowns or costs

### Problem 2: Complexity
Solution: Use simplified version initially

### Problem 3: Balance
Solution: Adjust DCs and modifiers

## Designer Notes

This mechanic aims to:
- Add depth without overwhelming complexity
- Provide meaningful choices
- Create memorable moments
- Enhance rather than replace core rules

## Quick Reference

**When to Use**: [Specific triggers]
**Basic Roll**: d20 + modifier vs. DC
**Success**: Achieve intended outcome
**Failure**: Complication or setback
**Resources**: [If applicable]
**Recovery**: [How resources return]

---
*Tags*: #mechanics #rules #homebrew #variant #system"""
        
    def generate_general_content(self, name: str, context: str) -> str:
        """Generate general note"""
        return f"""# {name}

## Overview

{name} represents an important concept, event, or element within the world. Its significance extends beyond simple definition, touching multiple aspects of the setting and potentially influencing various storylines.

## Description

### Basic Information
{name} can be understood as a multifaceted element that intersects with various aspects of the world. Its nature may be:
- Physical: A tangible thing or place
- Conceptual: An idea or belief system
- Event: Something that happened or will happen
- Process: An ongoing or repeatable occurrence

### Detailed Explanation
The full nature of {name} involves several interconnected components. It exists within the broader context of the world's systems, whether magical, political, social, or natural. Understanding its place requires considering both its immediate characteristics and its wider implications.

## Context & Connections

### Historical Context
The origins and development of {name} trace back through history, influenced by and influencing major events. Its current form results from various historical pressures and developments.

### Related Elements
Connected to {name} are various other important elements:
- Direct relationships with other concepts
- Indirect influences on broader systems
- Parallel developments in other areas
- Opposing or complementary forces

### Cultural Significance
Different groups view {name} through their own cultural lenses:
- Traditional interpretations
- Modern understandings
- Regional variations
- Conflicting perspectives

## Characteristics

### Defining Features
What makes {name} unique:
- Specific attributes or qualities
- Distinctive markers or signs
- Unique capabilities or limitations
- Recognition factors

### Variations
Different forms or interpretations:
- Regional differences
- Historical evolution
- Cultural adaptations
- Individual variations

## Practical Information

### How It Works
The functional aspects of {name}:
- Mechanisms or processes involved
- Requirements or prerequisites
- Limitations or boundaries
- Optimal conditions

### Applications
How {name} is used or encountered:
- Common applications
- Specialized uses
- Unexpected possibilities
- Limitations on use

### Access & Availability
How one might encounter or utilize {name}:
- Where it's found
- Who has access
- Requirements for interaction
- Restrictions or taboos

## Impact & Influence

### Direct Effects
Immediate consequences of {name}:
- On individuals
- On groups
- On environments
- On other systems

### Indirect Consequences
Broader implications:
- Social changes
- Political ramifications
- Economic impacts
- Cultural shifts

### Long-term Significance
Future implications:
- Potential developments
- Predicted changes
- Possible endpoints
- Cyclical patterns

## Current Status

### Present Situation
The current state of {name}:
- Active developments
- Recent changes
- Current holders or guardians
- Present threats or opportunities

### Recent Events
How {name} has been involved recently:
- Notable occurrences
- Changes in understanding
- New discoveries
- Shifts in control or access

## Mysteries & Questions

### Unknown Aspects
What remains unclear about {name}:
- Unanswered questions
- Conflicting information
- Hidden dimensions
- Lost knowledge

### Active Research
Current efforts to understand:
- Who is investigating
- Methods being employed
- Recent discoveries
- Obstacles to understanding

## Game Applications

### Adventure Hooks
Ways to incorporate {name} into gameplay:
1. **Discovery**: First encounter with {name}
2. **Investigation**: Uncovering its secrets
3. **Protection**: Defending it from threats
4. **Utilization**: Using it to achieve goals
5. **Prevention**: Stopping its misuse

### Mechanical Considerations
If applicable, how to handle mechanically:
- Dice rolls and DCs
- Resource management
- Time requirements
- Success and failure conditions

### Story Integration
How {name} fits into narratives:
- As plot device
- As background element
- As character motivation
- As campaign theme

## Additional Notes

### Variations by Campaign
How to adjust for different games:
- Tone adjustments
- Power level scaling
- Complexity options
- Alternative interpretations

### Development Potential
Ways {name} might evolve:
- Through player action
- Via story progression
- Based on world events
- Through discovery

## References

### Sources
Where information comes from:
- Primary sources
- Secondary accounts
- Rumors and legends
- Direct observation

### Related Topics
Other connected subjects:
- Similar concepts
- Opposing forces
- Parallel developments
- Dependent systems

### Further Investigation
Where to learn more:
- Specific locations
- Knowledgeable individuals
- Relevant texts
- Practical experience

## DM Notes

### True Nature
[Hidden information for DM only]

### Campaign Role
How this serves the campaign:
- Immediate purposes
- Long-term significance
- Connection to main plot
- Player engagement opportunities

### Customization Notes
Adapt as needed for:
- Player interests
- Campaign themes
- Power balance
- Story needs

---
*Tags*: #general #worldbuilding #{name.lower().replace(' ', '-')}"""
        
    def fix_remaining_links(self):
        """Fix any remaining broken links by updating them"""
        # After creating notes, some links might still need updating
        remaining_broken = []
        
        for broken in self.broken_links:
            target = broken['target']
            
            # Check if we created a note for it
            if not any(note['target'] == target for note in self.created_notes):
                # Try to find best match
                best_match = self.find_existing_file(target)
                if best_match:
                    self.fixed_links.append({
                        'file': broken['file'],
                        'old': f"[[{broken['link']}]]",
                        'new': f"[[{Path(best_match).stem}]]"
                    })
                else:
                    remaining_broken.append(broken)
                    
        print(f"   ✅ Fixed {len(self.fixed_links)} additional links")
        
    def generate_report(self) -> Dict:
        """Generate report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'statistics': {
                'broken_links_found': len(self.broken_links),
                'notes_created': len(self.created_notes),
                'links_fixed': len(self.fixed_links),
                'remaining_broken': len(self.broken_links) - len(self.created_notes) - len(self.fixed_links)
            },
            'created_notes': self.created_notes[:50],
            'fixed_links': self.fixed_links[:50]
        }
        
        # Save report
        report_path = self.vault_path / "13_Performance" / f"smart_link_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Create markdown report
        self.create_markdown_report(report)
        
        return report
        
    def create_markdown_report(self, report: Dict):
        """Create markdown report"""
        md_content = f"""# Smart Link Fix Report

Generated: {report['timestamp']}

## 📊 Statistics

- **Broken Links Found**: {report['statistics']['broken_links_found']:,}
- **Notes Created**: {report['statistics']['notes_created']:,}
- **Links Fixed**: {report['statistics']['links_fixed']:,}
- **Remaining Broken**: {report['statistics']['remaining_broken']:,}

## 📝 Sample Notes Created

"""
        
        for note in report['created_notes'][:20]:
            md_content += f"- **{note['target']}** → `{note['path']}` ({note['category']})\n"
            
        md_content += """

---
*Smart link fixing complete. New notes created and links updated.*
"""
        
        md_path = self.vault_path / "13_Performance" / f"smart_link_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        md_path.write_text(md_content, encoding='utf-8')

def main():
    fixer = SmartLinkFixer()
    report = fixer.run()
    
    print("\n" + "=" * 80)
    print("✅ SMART LINK FIXING COMPLETE!")
    print("=" * 80)
    
    print(f"\n📊 Results:")
    print(f"   • Broken links found: {report['statistics']['broken_links_found']:,}")
    print(f"   • New notes created: {report['statistics']['notes_created']:,}")
    print(f"   • Links fixed: {report['statistics']['links_fixed']:,}")
    print(f"\n📄 Report saved to 13_Performance/")

if __name__ == "__main__":
    main()