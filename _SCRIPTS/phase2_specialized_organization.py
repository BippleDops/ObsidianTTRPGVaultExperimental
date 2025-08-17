#!/usr/bin/env python3
"""
Phase 2 Specialized Organization Script
Advanced content organization, NPC database creation, and quest management
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import concurrent.futures
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Phase2SpecializedOrganizer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.results = []
        
    def create_comprehensive_npc_database(self) -> List[Dict]:
        """Create a comprehensive NPC database with relationships and metadata"""
        results = []
        npcs_dir = self.vault_path / "03_People"
        
        if not npcs_dir.exists():
            npcs_dir.mkdir(parents=True)
        
        # Collect all NPC files
        npc_files = list(npcs_dir.glob("NPC*.md")) + list(npcs_dir.glob("*NPC*.md"))
        
        # NPC database structure
        npc_database = {
            "npcs": {},
            "campaigns": defaultdict(list),
            "locations": defaultdict(list),
            "factions": defaultdict(list),
            "relationships": []
        }
        
        # Process each NPC file
        for npc_file in npc_files:
            try:
                content = npc_file.read_text(encoding='utf-8')
                npc_data = self._extract_npc_data(npc_file, content)
                
                if npc_data:
                    npc_name = npc_data['name']
                    npc_database['npcs'][npc_name] = npc_data
                    
                    # Categorize by campaign
                    if npc_data.get('campaign'):
                        npc_database['campaigns'][npc_data['campaign']].append(npc_name)
                    
                    # Categorize by location
                    if npc_data.get('location'):
                        npc_database['locations'][npc_data['location']].append(npc_name)
                    
                    # Categorize by faction
                    if npc_data.get('faction'):
                        npc_database['factions'][npc_data['faction']].append(npc_name)
                    
                    results.append({
                        "action": "processed_npc",
                        "file": str(npc_file.relative_to(self.vault_path)),
                        "npc_name": npc_name
                    })
                    
            except Exception as e:
                logger.warning(f"Could not process NPC file {npc_file}: {e}")
        
        # Create master NPC index
        self._create_npc_master_index(npc_database, results)
        
        # Create relationship maps
        self._create_relationship_maps(npc_database, results)
        
        # Create quick reference sheets
        self._create_npc_quick_references(npc_database, results)
        
        logger.info(f"NPC database created with {len(npc_database['npcs'])} NPCs")
        return results

    def _extract_npc_data(self, file_path: Path, content: str) -> Dict:
        """Extract structured data from NPC file"""
        npc_data = {
            "file": str(file_path.relative_to(self.vault_path)),
            "name": file_path.stem.replace('NPC', '').replace('_', ' ').strip(),
        }
        
        # Extract from frontmatter if exists
        if content.startswith('---'):
            lines = content.split('\n')
            end_idx = None
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_idx = i
                    break
            
            if end_idx:
                frontmatter = lines[1:end_idx]
                for line in frontmatter:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        npc_data[key.strip()] = value.strip()
        
        # Extract from content patterns
        patterns = {
            'race': r'(?:Race|Species):\s*([^\n]+)',
            'class': r'(?:Class|Profession):\s*([^\n]+)',
            'alignment': r'Alignment:\s*([^\n]+)',
            'location': r'(?:Location|Current Location):\s*([^\n]+)',
            'faction': r'(?:Faction|Organization):\s*([^\n]+)',
            'role': r'(?:Role|Position):\s*([^\n]+)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match and key not in npc_data:
                npc_data[key] = match.group(1).strip()
        
        return npc_data

    def _create_npc_master_index(self, database: Dict, results: List[Dict]) -> None:
        """Create the master NPC index file"""
        index_content = f"""# NPC Master Database

*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Quick Stats
- **Total NPCs:** {len(database['npcs'])}
- **Campaigns:** {len(database['campaigns'])}
- **Locations:** {len(database['locations'])}
- **Factions:** {len(database['factions'])}

## All NPCs (Dataview)
```dataview
TABLE 
  race as "Race",
  class as "Class", 
  location as "Location",
  campaign as "Campaign",
  faction as "Faction"
FROM "03_People"
WHERE type = "npc"
SORT file.name ASC
```

## NPCs by Campaign
"""
        
        for campaign, npcs in database['campaigns'].items():
            if campaign and campaign != 'unknown':
                index_content += f"\n### {campaign}\n"
                for npc in sorted(npcs):
                    npc_file = database['npcs'][npc]['file']
                    npc_filename = Path(npc_file).stem
                    index_content += f"- [[{npc_filename}|{npc}]]\n"
        
        index_content += "\n## NPCs by Location\n"
        for location, npcs in database['locations'].items():
            if location and location != 'unknown':
                index_content += f"\n### {location}\n"
                for npc in sorted(npcs):
                    npc_file = database['npcs'][npc]['file']
                    npc_filename = Path(npc_file).stem
                    index_content += f"- [[{npc_filename}|{npc}]]\n"
        
        index_content += "\n## NPCs by Faction\n"
        for faction, npcs in database['factions'].items():
            if faction and faction != 'unknown':
                index_content += f"\n### {faction}\n"
                for npc in sorted(npcs):
                    npc_file = database['npcs'][npc]['file']
                    npc_filename = Path(npc_file).stem
                    index_content += f"- [[{npc_filename}|{npc}]]\n"
        
        index_content += """
## Quick Actions
- [[NPC_Template|Create New NPC]]
- [[NPC_Relationship_Map|View Relationships]]
- [[NPC_Quick_Reference|Quick Reference]]

## Search Functions
```dataview
TABLE file.link as "NPC"
FROM "03_People"
WHERE type = "npc" AND contains(file.name, "")
```
"""
        
        index_file = self.vault_path / "03_People" / "00_NPC_Master_Database.md"
        index_file.write_text(index_content, encoding='utf-8')
        
        results.append({
            "action": "created_npc_master_index",
            "file": str(index_file.relative_to(self.vault_path)),
            "npcs_indexed": len(database['npcs'])
        })

    def _create_relationship_maps(self, database: Dict, results: List[Dict]) -> None:
        """Create NPC relationship mapping files"""
        
        # Text-based relationship map
        relationship_content = """# NPC Relationship Map

## Major Relationships

### Political Alliances
```mermaid
graph TD
    A[Political Leaders] --> B[Noble Houses]
    A --> C[Government Officials]
    B --> D[Court Members]
    C --> E[Bureaucrats]
```

### Criminal Networks
```mermaid
graph TD
    A[Crime Bosses] --> B[Lieutenants]
    B --> C[Street Contacts]
    A --> D[Corrupt Officials]
```

### Guild Connections
```mermaid
graph TD
    A[Guild Masters] --> B[Senior Members]
    B --> C[Apprentices]
    A --> D[Guild Allies]
```

## Relationship Types
- **Allied:** Work together toward common goals
- **Enemy:** Actively oppose each other
- **Rival:** Compete but not necessarily hostile
- **Family:** Blood or marriage relations
- **Mentor/Student:** Teaching relationships
- **Employer/Employee:** Professional relationships

## Dynamic Relationships
*Relationships that change based on player actions*

### Conditional Allies
- NPCs who help only under certain conditions
- Former enemies who can be redeemed
- Neutral parties who can be swayed

### Relationship Consequences
- How NPC relationships affect quests
- Ripple effects of befriending/antagonizing key figures
- Long-term campaign implications
"""
        
        rel_file = self.vault_path / "03_People" / "NPC_Relationship_Map.md"
        rel_file.write_text(relationship_content, encoding='utf-8')
        
        results.append({
            "action": "created_relationship_map",
            "file": str(rel_file.relative_to(self.vault_path))
        })

    def _create_npc_quick_references(self, database: Dict, results: List[Dict]) -> None:
        """Create quick reference sheets for NPCs"""
        
        quick_ref_content = """# NPC Quick Reference

## Voice & Personality Quick Notes

### Major NPCs
| Name | Voice | Key Trait | Quick Note |
|------|-------|-----------|------------|
"""
        
        # Add major NPCs to quick reference
        major_npcs = [npc for npc, data in database['npcs'].items() 
                     if data.get('importance') == 'major' or 'major' in data.get('tags', '')]
        
        for npc in major_npcs[:20]:  # Limit for readability
            npc_data = database['npcs'][npc]
            quick_ref_content += f"| {npc} | *Add voice* | *Add trait* | *Add note* |\n"
        
        quick_ref_content += """
### Minor NPCs
| Name | One-line Description |
|------|---------------------|
"""
        
        minor_npcs = [npc for npc, data in database['npcs'].items() 
                     if npc not in major_npcs]
        
        for npc in minor_npcs[:30]:  # Limit for readability
            quick_ref_content += f"| {npc} | *Brief description* |\n"
        
        quick_ref_content += """
## Random NPC Generator

### Names by Region
- **Aquabyssos:** Marina, Nerida, Poseidon, Theron
- **Aethermoor:** Celeste, Zephyr, Aurora, Magnus
- **Shadowlands:** Raven, Vex, Nyx, Mordecai

### Quick Personality Traits
| d6 | Trait |
|----|-------|
| 1  | Nervous and twitchy |
| 2  | Overly friendly |
| 3  | Suspicious of strangers |
| 4  | Speaks in whispers |
| 5  | Always eating something |
| 6  | Constantly checking timepiece |

### Quick Motivations
| d6 | Motivation |
|----|-----------|
| 1  | Protecting family |
| 2  | Seeking revenge |
| 3  | Accumulating wealth |
| 4  | Gaining power |
| 5  | Finding truth |
| 6  | Achieving redemption |
"""
        
        quick_ref_file = self.vault_path / "03_People" / "NPC_Quick_Reference.md"
        quick_ref_file.write_text(quick_ref_content, encoding='utf-8')
        
        results.append({
            "action": "created_npc_quick_reference",
            "file": str(quick_ref_file.relative_to(self.vault_path))
        })

    def create_advanced_location_system(self) -> List[Dict]:
        """Create advanced location organization with hierarchies"""
        results = []
        worldbuilding_dir = self.vault_path / "02_Worldbuilding"
        
        if not worldbuilding_dir.exists():
            return results
        
        # Find all location files
        location_files = []
        for pattern in ["*location*.md", "*place*.md", "*city*.md", "*town*.md", "*village*.md"]:
            location_files.extend(worldbuilding_dir.rglob(pattern))
        
        # Create location hierarchy
        location_hierarchy = {
            "regions": defaultdict(lambda: defaultdict(list)),
            "settlement_types": defaultdict(list),
            "campaigns": defaultdict(list)
        }
        
        for location_file in location_files:
            try:
                content = location_file.read_text(encoding='utf-8')
                location_data = self._extract_location_data(location_file, content)
                
                if location_data:
                    name = location_data['name']
                    region = location_data.get('region', 'Unknown')
                    settlement_type = location_data.get('settlement_type', 'Unknown')
                    campaign = location_data.get('campaign', 'Unknown')
                    
                    location_hierarchy['regions'][region][settlement_type].append(name)
                    location_hierarchy['settlement_types'][settlement_type].append(name)
                    location_hierarchy['campaigns'][campaign].append(name)
                    
                    results.append({
                        "action": "processed_location",
                        "file": str(location_file.relative_to(self.vault_path)),
                        "location_name": name
                    })
                    
            except Exception as e:
                logger.warning(f"Could not process location file {location_file}: {e}")
        
        # Create location master index
        self._create_location_master_index(location_hierarchy, results)
        
        # Create travel system
        self._create_travel_system(location_hierarchy, results)
        
        logger.info(f"Location system created with {len(location_files)} locations")
        return results

    def _extract_location_data(self, file_path: Path, content: str) -> Dict:
        """Extract structured data from location file"""
        location_data = {
            "file": str(file_path.relative_to(self.vault_path)),
            "name": file_path.stem.replace('_', ' ').title(),
        }
        
        # Extract from frontmatter
        if content.startswith('---'):
            lines = content.split('\n')
            end_idx = None
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_idx = i
                    break
            
            if end_idx:
                frontmatter = lines[1:end_idx]
                for line in frontmatter:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        location_data[key.strip()] = value.strip()
        
        # Extract from content patterns
        patterns = {
            'settlement_type': r'(?:Type|Settlement Type):\s*([^\n]+)',
            'population': r'Population:\s*([^\n]+)',
            'government': r'Government:\s*([^\n]+)',
            'notable_features': r'Notable Features:\s*([^\n]+)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match and key not in location_data:
                location_data[key] = match.group(1).strip()
        
        return location_data

    def _create_location_master_index(self, hierarchy: Dict, results: List[Dict]) -> None:
        """Create master location index"""
        
        index_content = f"""# Location Master Index

*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## All Locations (Dataview)
```dataview
TABLE 
  settlement_type as "Type",
  region as "Region", 
  population as "Population",
  campaign as "Campaign"
FROM "02_Worldbuilding"
WHERE type = "location"
SORT region, settlement_type, file.name
```

## Locations by Region
"""
        
        for region, settlements in hierarchy['regions'].items():
            if region and region != 'Unknown':
                index_content += f"\n### {region}\n"
                for settlement_type, locations in settlements.items():
                    if locations:
                        index_content += f"\n#### {settlement_type}\n"
                        for location in sorted(locations):
                            index_content += f"- [[{location}]]\n"
        
        index_content += "\n## Settlement Types\n"
        for settlement_type, locations in hierarchy['settlement_types'].items():
            if settlement_type and settlement_type != 'Unknown' and locations:
                index_content += f"\n### {settlement_type}\n"
                for location in sorted(locations):
                    index_content += f"- [[{location}]]\n"
        
        index_content += """
## Quick Actions
- [[Location_Template|Create New Location]]
- [[Travel_System|Plan Travel Routes]]
- [[Random_Locations|Generate Random Locations]]

## Map Integration
- [[Regional_Maps|View Regional Maps]]
- [[Settlement_Maps|Settlement Detail Maps]]
- [[Travel_Maps|Travel Route Maps]]
"""
        
        index_file = self.vault_path / "02_Worldbuilding" / "00_Location_Master_Index.md"
        index_file.write_text(index_content, encoding='utf-8')
        
        results.append({
            "action": "created_location_master_index",
            "file": str(index_file.relative_to(self.vault_path)),
            "locations_indexed": sum(len(locs) for settlements in hierarchy['regions'].values() 
                                   for locs in settlements.values())
        })

    def _create_travel_system(self, hierarchy: Dict, results: List[Dict]) -> None:
        """Create travel time and route system"""
        
        travel_content = """# Travel System

## Travel Times Between Major Locations

### Aquabyssos Region
| From | To | Travel Time | Method | Difficulty |
|------|----|-----------|---------|-----------| 
| Capital | Port City | 2 days | Ship | Easy |
| Capital | Border Town | 5 days | Land | Medium |

### Aethermoor Region  
| From | To | Travel Time | Method | Difficulty |
|------|----|-----------|---------|-----------| 
| Sky City | Mountain Keep | 1 day | Flying Mount | Easy |
| Sky City | Valley Settlement | 3 days | Land | Hard |

## Travel Methods

### By Land
- **Walking:** 20 miles/day normal, 15 miles/day difficult terrain
- **Horse:** 30 miles/day normal, 20 miles/day difficult terrain
- **Cart:** 15 miles/day normal, 10 miles/day difficult terrain

### By Water
- **River:** 30 miles/day downstream, 15 miles/day upstream
- **Ocean:** 50 miles/day good winds, 25 miles/day calm

### By Air (Aethermoor)
- **Flying Mount:** 100 miles/day, weather dependent
- **Airship:** 150 miles/day, requires crew

## Random Travel Encounters

### Road Encounters (d10)
| Roll | Encounter |
|------|-----------|
| 1-2  | Merchant caravan |
| 3-4  | Bandits |
| 5-6  | Fellow travelers |
| 7-8  | Wild animals |
| 9    | Broken bridge/obstacle |
| 10   | Something unusual |

### Sea Encounters (d8)
| Roll | Encounter |
|------|-----------|
| 1-2  | Pirates |
| 3-4  | Storm |
| 5-6  | Other ship |
| 7    | Sea creatures |
| 8    | Mysterious island |

## Weather Effects
- **Clear:** Normal travel
- **Rain:** -25% speed, disadvantage on perception
- **Storm:** No travel, seek shelter
- **Snow:** -50% speed, cold damage risk
- **Fog:** -50% speed, easy to get lost
"""
        
        travel_file = self.vault_path / "02_Worldbuilding" / "Travel_System.md"
        travel_file.write_text(travel_content, encoding='utf-8')
        
        results.append({
            "action": "created_travel_system",
            "file": str(travel_file.relative_to(self.vault_path))
        })

    def create_quest_management_system(self) -> List[Dict]:
        """Create comprehensive quest tracking and management"""
        results = []
        
        # Quest tracker with advanced features
        quest_tracker_content = """# Advanced Quest Management System

## Active Quests Dashboard
```dataview
TABLE 
  priority as "Priority",
  status as "Status",
  quest_giver as "Quest Giver",
  location as "Location",
  reward as "Reward",
  deadline as "Deadline"
FROM ""
WHERE type = "quest" AND status = "active"
SORT priority DESC, deadline ASC
```

## Quest Status Tracking

### By Priority
```dataview
TABLE file.link as "Quest", quest_giver, deadline
FROM ""
WHERE type = "quest" AND priority = "high"
SORT deadline ASC
```

### By Campaign
```dataview
TABLE status, priority, quest_giver
FROM ""
WHERE type = "quest"
GROUP BY campaign
SORT campaign, priority DESC
```

## Quest Chains and Dependencies

### Main Story Arcs
```mermaid
graph TD
    A[Opening Quest] --> B[Investigation Phase]
    B --> C[Confrontation]
    C --> D[Resolution]
    B --> E[Side Quest Branch]
    E --> F[Optional Conclusion]
```

### Character Development Quests
```mermaid
graph TD
    A[Personal Hook] --> B[Character Growth]
    B --> C[Major Choice]
    C --> D[Consequence]
    C --> E[Alternative Path]
```

## Quest Templates by Type

### Investigation Quest
```
---
type: quest
name: Quest Name
campaign: Campaign
status: active
priority: medium
quest_type: investigation
quest_giver: [[NPC Name]]
location: [[Location]]
reward: Information/Item
deadline: Date
tags: [quest, investigation]
---

## Mystery
*What needs to be uncovered*

## Clues
1. First clue location
2. Second clue source
3. Final revelation

## Red Herrings
- False lead 1
- False lead 2

## Resolution Paths
- Direct confrontation
- Subtle investigation
- Social manipulation
```

### Combat Quest
```
---
type: quest
name: Quest Name
campaign: Campaign
status: active
priority: high
quest_type: combat
quest_giver: [[NPC Name]]
target: Enemy/Monster
location: [[Location]]
reward: XP/Gold/Items
deadline: Date
tags: [quest, combat]
---

## Objective
*Who/what to defeat and why*

## Enemy Details
- **Type:** Monster/Humanoid
- **CR:** Challenge Rating
- **Weaknesses:** Vulnerabilities
- **Tactics:** How they fight

## Battlefield
- **Terrain:** Description
- **Hazards:** Environmental dangers
- **Advantages:** Tactical opportunities

## Scaling Options
- **Easy:** Reduce enemy numbers
- **Hard:** Add reinforcements/hazards
```

## Quest Consequences System

### Success Outcomes
- Experience gained
- Relationships improved
- New opportunities unlocked
- World state changes

### Failure Outcomes  
- Alternative paths opened
- Relationships damaged
- Consequences for world
- Future complications

### Partial Success
- Mixed results
- Unintended consequences
- Future quest hooks
- Character development

## Random Quest Generator

### Quest Types (d8)
| Roll | Type |
|------|------|
| 1 | Rescue/Recovery |
| 2 | Investigation |
| 3 | Escort/Protection |
| 4 | Elimination |
| 5 | Exploration |
| 6 | Negotiation |
| 7 | Delivery |
| 8 | Construction/Repair |

### Quest Complications (d6)
| Roll | Complication |
|------|-------------|
| 1 | Time pressure |
| 2 | Rival group |
| 3 | Missing information |
| 4 | Moral dilemma |
| 5 | Resource shortage |
| 6 | Betrayal |

### Quest Rewards (d8)
| Roll | Reward Type |
|------|------------|
| 1 | Gold/Treasure |
| 2 | Magic Item |
| 3 | Information |
| 4 | Ally/Contact |
| 5 | Territory/Property |
| 6 | Title/Status |
| 7 | Special Ability |
| 8 | Future Favor |
"""
        
        quest_file = self.vault_path / "00_System" / "Advanced_Quest_Management.md"
        quest_file.write_text(quest_tracker_content, encoding='utf-8')
        
        results.append({
            "action": "created_advanced_quest_system",
            "file": str(quest_file.relative_to(self.vault_path))
        })
        
        return results

    def enhance_session_documentation(self) -> List[Dict]:
        """Enhance session notes with better structure and linking"""
        results = []
        sessions_dir = self.vault_path / "06_Sessions"
        
        if not sessions_dir.exists():
            return results
        
        session_files = list(sessions_dir.glob("*.md"))
        
        for session_file in session_files:
            try:
                content = session_file.read_text(encoding='utf-8')
                enhanced_content = self._enhance_single_session(content)
                
                if enhanced_content != content:
                    session_file.write_text(enhanced_content, encoding='utf-8')
                    results.append({
                        "action": "enhanced_session_note",
                        "file": str(session_file.relative_to(self.vault_path))
                    })
                    
            except Exception as e:
                logger.warning(f"Could not enhance session {session_file}: {e}")
        
        # Create session index
        self._create_session_index(session_files, results)
        
        logger.info(f"Enhanced {len(results)} session files")
        return results

    def _enhance_single_session(self, content: str) -> str:
        """Enhance a single session note with better structure"""
        
        # Add frontmatter if missing
        if not content.startswith('---'):
            session_frontmatter = f"""---
type: session
campaign: Unknown
session_number: TBD
date: {datetime.now().strftime('%Y-%m-%d')}
status: completed
tags: [session]
---

"""
            content = session_frontmatter + content
        
        # Enhanced session template
        enhanced_template = """
## Session Summary
*Brief overview of what happened this session*

## Key Events
- Major event 1
- Major event 2
- Major event 3

## NPCs Encountered
- [[NPC Name]] - Brief interaction description
- [[NPC Name]] - Role in this session

## Locations Visited
- [[Location Name]] - What happened here
- [[Location Name]] - Significance

## Quest Progress
- [[Quest Name]] - Progress made
- [[Quest Name]] - New developments

## Character Moments
- Player character highlights
- Important character decisions
- Roleplay moments

## Loot & Rewards
- Items gained
- XP awarded
- Other rewards

## Plot Threads
### New Threads
- New mysteries introduced
- Hooks for future sessions

### Ongoing Threads
- Continued storylines
- Developing situations

### Resolved Threads
- Completed plot points
- Answered questions

## DM Notes
### What Went Well
- Successful elements

### What to Improve
- Areas for enhancement

### Player Feedback
- Direct player comments
- Observed reactions

## Next Session Prep
- Important things to remember
- NPCs to prepare
- Locations to detail
- Encounters to plan

---
*Session completed on {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        # Only add template if session is very short (likely incomplete)
        if len(content.strip()) < 200:
            content += enhanced_template
        
        return content

    def _create_session_index(self, session_files: List[Path], results: List[Dict]) -> None:
        """Create comprehensive session index"""
        
        index_content = f"""# Session Master Index

*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## All Sessions
```dataview
TABLE 
  session_number as "Session",
  campaign as "Campaign",
  date as "Date",
  status as "Status"
FROM "06_Sessions"
WHERE type = "session"
SORT campaign, session_number ASC
```

## Recent Sessions
```dataview
TABLE 
  file.link as "Session",
  campaign as "Campaign",
  session_number as "#"
FROM "06_Sessions"
WHERE type = "session"
SORT date DESC
LIMIT 10
```

## Sessions by Campaign
```dataview
TABLE 
  session_number as "#",
  date as "Date",
  status as "Status"
FROM "06_Sessions"
WHERE type = "session"
GROUP BY campaign
SORT campaign, session_number ASC
```

## Session Statistics
- **Total Sessions:** {len(session_files)}
- **Campaigns Active:** *Count from dataview*
- **Average Session Length:** *Calculate from content*

## Quick Actions
- [[Session_Template|Create New Session]]
- [[Session_Prep_Checklist|Prep Next Session]]
- [[Campaign_Timeline|View Timeline]]

## Session Analysis
### Attendance Tracking
*Track which players attended which sessions*

### Plot Thread Tracking
*Monitor ongoing storylines across sessions*

### XP and Milestone Tracking
*Character progression through sessions*
"""
        
        index_file = self.vault_path / "06_Sessions" / "00_Session_Master_Index.md"
        index_file.write_text(index_content, encoding='utf-8')
        
        results.append({
            "action": "created_session_index",
            "file": str(index_file.relative_to(self.vault_path)),
            "sessions_indexed": len(session_files)
        })

    def run_phase2_specialized(self) -> Dict:
        """Run all specialized Phase 2 improvements"""
        logger.info("Starting Phase 2 Specialized Organization")
        
        all_results = []
        
        # Execute all improvements
        improvements = [
            ("Create Comprehensive NPC Database", self.create_comprehensive_npc_database),
            ("Create Advanced Location System", self.create_advanced_location_system),
            ("Create Quest Management System", self.create_quest_management_system),
            ("Enhance Session Documentation", self.enhance_session_documentation),
        ]
        
        for name, func in improvements:
            logger.info(f"Running: {name}")
            try:
                result = func()
                all_results.extend(result)
                logger.info(f"Completed: {name} - {len(result)} changes")
            except Exception as e:
                logger.error(f"Failed: {name} - {e}")
                all_results.append({
                    "action": "error",
                    "improvement": name,
                    "error": str(e)
                })
        
        # Create summary report
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_changes": len(all_results),
            "improvements_completed": len([r for r in all_results if r.get("action") != "error"]),
            "errors": len([r for r in all_results if r.get("action") == "error"]),
            "results": all_results
        }
        
        # Save report
        report_file = self.vault_path / "_SCRIPTS" / f"phase2_specialized_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with report_file.open('w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Phase 2 Specialized completed: {summary['total_changes']} total changes")
        return summary

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    organizer = Phase2SpecializedOrganizer(vault_path)
    result = organizer.run_phase2_specialized()
    
    print(f"\nPhase 2 Specialized Organization Completed!")
    print(f"Total Changes: {result['total_changes']}")
    print(f"Improvements: {result['improvements_completed']}")
    print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    main()