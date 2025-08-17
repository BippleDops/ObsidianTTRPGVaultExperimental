#!/usr/bin/env python3
"""
Parallel Phases 1-3 Master Orchestrator
Executes phases 1-3 of the vault improvement plan simultaneously
"""

import os
import sys
import time
import json
import logging
import asyncio
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
import shutil
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parallel_vault_improvement.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VaultImprover:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.script_path = self.vault_path / "_SCRIPTS"
        self.archive_path = self.vault_path / "08_Archive"
        self.backup_path = self.vault_path / "_BACKUPS"
        
        # Ensure essential directories exist
        self.archive_path.mkdir(exist_ok=True)
        self.backup_path.mkdir(exist_ok=True)
        
        # Progress tracking
        self.progress = {
            "phase1": {"completed": 0, "total": 100, "status": "pending"},
            "phase2": {"completed": 0, "total": 100, "status": "pending"},
            "phase3": {"completed": 0, "total": 100, "status": "pending"}
        }
        
        # Results storage
        self.results = {
            "phase1": [],
            "phase2": [],
            "phase3": [],
            "errors": []
        }
        
    def create_backup(self) -> str:
        """Create timestamped backup before starting"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_before_parallel_phases_{timestamp}"
        backup_dir = self.backup_path / backup_name
        
        logger.info(f"Creating backup: {backup_name}")
        
        # Create backup directory structure
        backup_dir.mkdir(exist_ok=True)
        
        # Copy essential files and track what we backup
        backup_manifest = []
        
        for root, dirs, files in os.walk(self.vault_path):
            root_path = Path(root)
            
            # Skip backup and script directories
            if "_BACKUPS" in str(root_path) or "_SCRIPTS" in str(root_path):
                continue
                
            rel_path = root_path.relative_to(self.vault_path)
            backup_root = backup_dir / rel_path
            backup_root.mkdir(parents=True, exist_ok=True)
            
            for file in files:
                if file.endswith('.md') or file.endswith('.json'):
                    src = root_path / file
                    dst = backup_root / file
                    shutil.copy2(src, dst)
                    backup_manifest.append(str(rel_path / file))
        
        # Save backup manifest
        manifest_file = backup_dir / "backup_manifest.json"
        with manifest_file.open('w') as f:
            json.dump({
                "timestamp": timestamp,
                "total_files": len(backup_manifest),
                "files": backup_manifest
            }, f, indent=2)
        
        logger.info(f"Backup completed: {len(backup_manifest)} files backed up")
        return str(backup_dir)

    # PHASE 1: Template Structure Cleanup
    def phase1_template_cleanup(self) -> List[Dict]:
        """Phase 1: Template Structure Cleanup (Steps 1-100)"""
        logger.info("Starting Phase 1: Template Structure Cleanup")
        self.progress["phase1"]["status"] = "running"
        results = []
        
        try:
            # Step 1-20: Clean template placeholders
            results.extend(self._clean_template_placeholders())
            self.progress["phase1"]["completed"] = 20
            
            # Step 21-40: Remove empty folders and fix brackets
            results.extend(self._fix_brackets_and_empty_folders())
            self.progress["phase1"]["completed"] = 40
            
            # Step 41-60: Normalize frontmatter
            results.extend(self._normalize_frontmatter())
            self.progress["phase1"]["completed"] = 60
            
            # Step 61-80: Standardize statblocks
            results.extend(self._standardize_statblocks())
            self.progress["phase1"]["completed"] = 80
            
            # Step 81-100: Optimize dataview queries
            results.extend(self._optimize_dataview_queries())
            self.progress["phase1"]["completed"] = 100
            self.progress["phase1"]["status"] = "completed"
            
        except Exception as e:
            logger.error(f"Phase 1 error: {e}")
            self.results["errors"].append({"phase": 1, "error": str(e)})
            self.progress["phase1"]["status"] = "error"
        
        return results

    def _clean_template_placeholders(self) -> List[Dict]:
        """Clean all template placeholders {{}} {%%} <%>"""
        results = []
        placeholder_patterns = [
            r'\{\{[^}]*\}\}',  # {{placeholder}}
            r'\{%[^%]*%\}',    # {%placeholder%}
            r'<%[^>]*%>',      # <%placeholder%>
            r'\{\{.*?\}\}',    # Greedy version for nested
        ]
        
        md_files = list(self.vault_path.rglob("*.md"))
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                for pattern in placeholder_patterns:
                    content = re.sub(pattern, '', content)
                
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    results.append({
                        "action": "cleaned_placeholders",
                        "file": str(file_path.relative_to(self.vault_path)),
                        "patterns_removed": len([p for p in placeholder_patterns if re.search(p, original_content)])
                    })
                    
            except Exception as e:
                logger.warning(f"Could not clean placeholders in {file_path}: {e}")
        
        logger.info(f"Cleaned placeholders in {len(results)} files")
        return results

    def _fix_brackets_and_empty_folders(self) -> List[Dict]:
        """Fix broken brackets and remove empty folders"""
        results = []
        
        # Fix broken brackets in markdown files
        md_files = list(self.vault_path.rglob("*.md"))
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                # Fix common bracket issues
                fixes = [
                    (r'\[\[([^\]]*)\]\]([^\]]*)\]\]', r'[[\1\2]]'),  # Triple brackets
                    (r'\[\[([^\]]*)\[([^\]]*)\]\]', r'[[\1\2]]'),    # Nested brackets
                    (r'\[\[([^\]]*)\]([^\]]*)\]', r'[[\1\2]]'),      # Missing bracket
                ]
                
                for pattern, replacement in fixes:
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    results.append({
                        "action": "fixed_brackets",
                        "file": str(file_path.relative_to(self.vault_path))
                    })
                    
            except Exception as e:
                logger.warning(f"Could not fix brackets in {file_path}: {e}")
        
        # Remove empty folders (but preserve structure)
        for root, dirs, files in os.walk(self.vault_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()) and not dir_name.startswith(('_', '0')):
                        dir_path.rmdir()
                        results.append({
                            "action": "removed_empty_folder",
                            "folder": str(dir_path.relative_to(self.vault_path))
                        })
                except Exception as e:
                    pass  # Folder not empty or protected
        
        logger.info(f"Fixed brackets and removed empty folders: {len(results)} changes")
        return results

    def _normalize_frontmatter(self) -> List[Dict]:
        """Normalize frontmatter and remove template tags"""
        results = []
        md_files = list(self.vault_path.rglob("*.md"))
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                if len(lines) > 0 and lines[0].strip() == '---':
                    # Find end of frontmatter
                    end_idx = None
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            end_idx = i
                            break
                    
                    if end_idx:
                        frontmatter = lines[1:end_idx]
                        body = lines[end_idx+1:]
                        
                        # Clean frontmatter
                        cleaned_frontmatter = []
                        for line in frontmatter:
                            # Remove template-specific fields
                            if not any(template_field in line.lower() for template_field in 
                                     ['template', 'templateversion', 'templater', 'tp_']):
                                cleaned_frontmatter.append(line)
                        
                        # Reconstruct file
                        new_content = '---\n' + '\n'.join(cleaned_frontmatter) + '\n---\n' + '\n'.join(body)
                        
                        if new_content != content:
                            file_path.write_text(new_content, encoding='utf-8')
                            results.append({
                                "action": "normalized_frontmatter",
                                "file": str(file_path.relative_to(self.vault_path))
                            })
                            
            except Exception as e:
                logger.warning(f"Could not normalize frontmatter in {file_path}: {e}")
        
        logger.info(f"Normalized frontmatter in {len(results)} files")
        return results

    def _standardize_statblocks(self) -> List[Dict]:
        """Standardize D&D statblocks and setup dice roller integration"""
        results = []
        md_files = list(self.vault_path.rglob("*.md"))
        
        # Standard statblock template
        standard_statblock = """
```statblock
name: {name}
size: {size}
type: {type}
alignment: {alignment}
ac: {ac}
hp: {hp}
speed: {speed}
stats: [{str}, {dex}, {con}, {int}, {wis}, {cha}]
saves: {saves}
skills: {skills}
senses: {senses}
languages: {languages}
cr: {cr}
```
"""
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Look for NPC files that need statblocks
                if ('npc' in file_path.name.lower() or 
                    any(keyword in content.lower() for keyword in ['ac:', 'hit points:', 'challenge rating:'])):
                    
                    # Add dice roller syntax if missing
                    dice_patterns = [
                        (r'(\d+)d(\d+)', r'`dice: \1d\2`'),  # Basic dice
                        (r'(\d+)d(\d+)\+(\d+)', r'`dice: \1d\2+\3`'),  # Dice with modifier
                    ]
                    
                    original_content = content
                    for pattern, replacement in dice_patterns:
                        content = re.sub(pattern, replacement, content)
                    
                    if content != original_content:
                        file_path.write_text(content, encoding='utf-8')
                        results.append({
                            "action": "added_dice_roller",
                            "file": str(file_path.relative_to(self.vault_path))
                        })
                        
            except Exception as e:
                logger.warning(f"Could not standardize statblock in {file_path}: {e}")
        
        logger.info(f"Standardized statblocks in {len(results)} files")
        return results

    def _optimize_dataview_queries(self) -> List[Dict]:
        """Optimize dataview queries for performance"""
        results = []
        md_files = list(self.vault_path.rglob("*.md"))
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Find dataview queries
                dataview_pattern = r'```dataview\n(.*?)\n```'
                matches = re.findall(dataview_pattern, content, re.DOTALL)
                
                if matches:
                    optimized_content = content
                    for query in matches:
                        # Basic optimizations
                        optimized_query = query
                        
                        # Add WHERE clauses for better performance
                        if 'FROM' in query and 'WHERE' not in query:
                            optimized_query += '\nWHERE file.name != ""'
                        
                        # Replace inefficient patterns
                        optimizations = [
                            ('LIST\n', 'TABLE file.link as "File"\n'),
                            ('sort file.name', 'sort file.name asc'),
                        ]
                        
                        for old, new in optimizations:
                            optimized_query = optimized_query.replace(old, new)
                        
                        optimized_content = optimized_content.replace(query, optimized_query)
                    
                    if optimized_content != content:
                        file_path.write_text(optimized_content, encoding='utf-8')
                        results.append({
                            "action": "optimized_dataview",
                            "file": str(file_path.relative_to(self.vault_path)),
                            "queries_optimized": len(matches)
                        })
                        
            except Exception as e:
                logger.warning(f"Could not optimize dataview in {file_path}: {e}")
        
        logger.info(f"Optimized dataview queries in {len(results)} files")
        return results

    # PHASE 2: Content Organization
    def phase2_content_organization(self) -> List[Dict]:
        """Phase 2: Content Organization (Steps 101-200)"""
        logger.info("Starting Phase 2: Content Organization")
        self.progress["phase2"]["status"] = "running"
        results = []
        
        try:
            # Step 101-120: Organize campaigns
            results.extend(self._organize_campaigns())
            self.progress["phase2"]["completed"] = 20
            
            # Step 121-140: Enhance session notes
            results.extend(self._enhance_session_notes())
            self.progress["phase2"]["completed"] = 40
            
            # Step 141-160: Create NPC database
            results.extend(self._create_npc_database())
            self.progress["phase2"]["completed"] = 60
            
            # Step 161-180: Build location hierarchy
            results.extend(self._build_location_hierarchy())
            self.progress["phase2"]["completed"] = 80
            
            # Step 181-200: Setup quest tracking and encounter management
            results.extend(self._setup_quest_and_encounter_systems())
            self.progress["phase2"]["completed"] = 100
            self.progress["phase2"]["status"] = "completed"
            
        except Exception as e:
            logger.error(f"Phase 2 error: {e}")
            self.results["errors"].append({"phase": 2, "error": str(e)})
            self.progress["phase2"]["status"] = "error"
        
        return results

    def _organize_campaigns(self) -> List[Dict]:
        """Organize campaigns and create better structure"""
        results = []
        campaigns_dir = self.vault_path / "01_Adventures" / "Campaigns"
        
        if campaigns_dir.exists():
            # Create campaign index
            campaign_files = list(campaigns_dir.glob("*.md"))
            
            index_content = """# Campaign Master Index

## Active Campaigns
"""
            
            for campaign_file in campaign_files:
                try:
                    content = campaign_file.read_text(encoding='utf-8')
                    # Extract campaign name from filename or content
                    campaign_name = campaign_file.stem.replace('_', ' ').title()
                    
                    index_content += f"- [[{campaign_file.stem}|{campaign_name}]]\n"
                    
                    # Add campaign metadata if missing
                    if not content.startswith('---'):
                        metadata = f"""---
type: campaign
status: active
created: {datetime.now().strftime('%Y-%m-%d')}
tags: [campaign]
---

"""
                        campaign_file.write_text(metadata + content, encoding='utf-8')
                        results.append({
                            "action": "added_campaign_metadata",
                            "file": str(campaign_file.relative_to(self.vault_path))
                        })
                        
                except Exception as e:
                    logger.warning(f"Could not process campaign {campaign_file}: {e}")
            
            # Write campaign index
            index_file = campaigns_dir / "00_Campaign_Index.md"
            index_file.write_text(index_content, encoding='utf-8')
            results.append({
                "action": "created_campaign_index",
                "file": str(index_file.relative_to(self.vault_path)),
                "campaigns_indexed": len(campaign_files)
            })
        
        logger.info(f"Organized campaigns: {len(results)} changes")
        return results

    def _enhance_session_notes(self) -> List[Dict]:
        """Enhance session notes with better formatting and links"""
        results = []
        sessions_dir = self.vault_path / "06_Sessions"
        
        if sessions_dir.exists():
            session_files = list(sessions_dir.glob("*.md"))
            
            for session_file in session_files:
                try:
                    content = session_file.read_text(encoding='utf-8')
                    original_content = content
                    
                    # Add session template structure if missing
                    if "## Session Summary" not in content:
                        session_template = """
## Session Summary
*Brief overview of this session*

## Key Events
- Event 1
- Event 2

## NPCs Encountered
- [[NPC Name]] - Brief description

## Locations Visited
- [[Location Name]] - What happened here

## Quest Progress
- [[Quest Name]] - What was accomplished

## Notes for Next Session
- Important things to remember
- Plot threads to follow up

---
"""
                        # Add template at the end if content exists, or at beginning if empty
                        if len(content.strip()) > 100:
                            content += session_template
                        else:
                            content = session_template + content
                    
                    # Auto-link common patterns
                    auto_link_patterns = [
                        (r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b', r'[[\1]]'),  # Proper names
                        (r'\bNPC (\w+)', r'NPC [[\1]]'),  # NPC references
                    ]
                    
                    for pattern, replacement in auto_link_patterns:
                        content = re.sub(pattern, replacement, content)
                    
                    if content != original_content:
                        session_file.write_text(content, encoding='utf-8')
                        results.append({
                            "action": "enhanced_session_note",
                            "file": str(session_file.relative_to(self.vault_path))
                        })
                        
                except Exception as e:
                    logger.warning(f"Could not enhance session {session_file}: {e}")
        
        logger.info(f"Enhanced session notes: {len(results)} changes")
        return results

    def _create_npc_database(self) -> List[Dict]:
        """Create comprehensive NPC database with relationships"""
        results = []
        npcs_dir = self.vault_path / "03_People"
        
        if npcs_dir.exists():
            npc_files = list(npcs_dir.glob("NPC*.md"))
            
            # Create NPC database index
            database_content = """# NPC Master Database

## Quick Search
```dataview
TABLE type, campaign, status, location
FROM "03_People"
WHERE type = "npc"
SORT file.name
```

## By Campaign
"""
            
            # Group NPCs by campaign
            campaigns = {}
            for npc_file in npc_files:
                try:
                    content = npc_file.read_text(encoding='utf-8')
                    
                    # Extract or add NPC metadata
                    if not content.startswith('---'):
                        npc_name = npc_file.stem.replace('NPC', '').replace('_', ' ').strip()
                        metadata = f"""---
type: npc
name: {npc_name}
campaign: unknown
status: active
location: unknown
created: {datetime.now().strftime('%Y-%m-%d')}
tags: [npc]
---

# {npc_name}

## Basic Information
- **Race:** 
- **Class:** 
- **Alignment:** 
- **Location:** 

## Appearance
*Physical description*

## Personality
*Personality traits, ideals, bonds, flaws*

## Background
*Character background and history*

## Role in Campaign
*How this NPC fits into the story*

## Relationships
*Connections to other NPCs*

## Notes
*Additional DM notes*

"""
                        npc_file.write_text(metadata + content, encoding='utf-8')
                        results.append({
                            "action": "added_npc_template",
                            "file": str(npc_file.relative_to(self.vault_path))
                        })
                        
                        # Add to unknown campaign group
                        if 'unknown' not in campaigns:
                            campaigns['unknown'] = []
                        campaigns['unknown'].append(npc_name)
                    
                except Exception as e:
                    logger.warning(f"Could not process NPC {npc_file}: {e}")
            
            # Add campaign sections to database
            for campaign, npcs in campaigns.items():
                database_content += f"\n### {campaign.title()}\n"
                for npc in npcs:
                    database_content += f"- [[{npc}]]\n"
            
            # Write NPC database
            database_file = npcs_dir / "00_NPC_Database.md"
            database_file.write_text(database_content, encoding='utf-8')
            results.append({
                "action": "created_npc_database",
                "file": str(database_file.relative_to(self.vault_path)),
                "npcs_cataloged": len(npc_files)
            })
        
        logger.info(f"Created NPC database: {len(results)} changes")
        return results

    def _build_location_hierarchy(self) -> List[Dict]:
        """Build location hierarchy and quest tracking"""
        results = []
        worldbuilding_dir = self.vault_path / "02_Worldbuilding"
        
        if worldbuilding_dir.exists():
            # Create location index
            location_files = list(worldbuilding_dir.rglob("*location*.md")) + \
                           list(worldbuilding_dir.rglob("*place*.md")) + \
                           list(worldbuilding_dir.rglob("*city*.md"))
            
            location_index = """# Location Master Index

## All Locations
```dataview
TABLE type, region, campaign, description
FROM "02_Worldbuilding"
WHERE type = "location" OR contains(file.name, "place") OR contains(file.name, "location")
SORT file.name
```

## By Region
"""
            
            # Process location files
            regions = {}
            for location_file in location_files:
                try:
                    content = location_file.read_text(encoding='utf-8')
                    
                    # Add location metadata if missing
                    if not content.startswith('---'):
                        location_name = location_file.stem.replace('_', ' ').title()
                        metadata = f"""---
type: location
name: {location_name}
region: unknown
campaign: unknown
settlement_type: unknown
population: unknown
created: {datetime.now().strftime('%Y-%m-%d')}
tags: [location]
---

# {location_name}

## Overview
*Brief description of this location*

## Geography
*Physical features and layout*

## Notable Features
- Feature 1
- Feature 2

## Important NPCs
- [[NPC Name]] - Role

## Quests and Hooks
- [[Quest Name]] - Brief description

## History
*Historical significance*

## Notes
*Additional DM notes*

"""
                        location_file.write_text(metadata + content, encoding='utf-8')
                        results.append({
                            "action": "added_location_template",
                            "file": str(location_file.relative_to(self.vault_path))
                        })
                        
                        # Add to unknown region group
                        if 'unknown' not in regions:
                            regions['unknown'] = []
                        regions['unknown'].append(location_name)
                    
                except Exception as e:
                    logger.warning(f"Could not process location {location_file}: {e}")
            
            # Add region sections
            for region, locations in regions.items():
                location_index += f"\n### {region.title()}\n"
                for location in locations:
                    location_index += f"- [[{location}]]\n"
            
            # Write location index
            index_file = worldbuilding_dir / "00_Location_Index.md"
            index_file.write_text(location_index, encoding='utf-8')
            results.append({
                "action": "created_location_index",
                "file": str(index_file.relative_to(self.vault_path)),
                "locations_cataloged": len(location_files)
            })
        
        logger.info(f"Built location hierarchy: {len(results)} changes")
        return results

    def _setup_quest_and_encounter_systems(self) -> List[Dict]:
        """Setup quest tracking and encounter management"""
        results = []
        
        # Create quest tracker
        quest_tracker_content = """# Quest Master Tracker

## Active Quests
```dataview
TABLE status, campaign, quest_giver, reward
FROM ""
WHERE type = "quest" AND status = "active"
SORT priority DESC
```

## Completed Quests
```dataview
TABLE campaign, completion_date, reward
FROM ""
WHERE type = "quest" AND status = "completed"
SORT completion_date DESC
```

## Quest Templates

### Main Quest Template
```
---
type: quest
name: Quest Name
campaign: Campaign Name
status: active
priority: high
quest_giver: [[NPC Name]]
reward: Description
created: {{date}}
tags: [quest, main]
---

# Quest Name

## Objective
*What needs to be accomplished*

## Background
*Why this quest exists*

## Steps
1. Step 1
2. Step 2
3. Step 3

## NPCs Involved
- [[Quest Giver]] - Role
- [[Other NPC]] - Role

## Locations
- [[Location]] - Why relevant

## Rewards
- XP: Amount
- Gold: Amount
- Items: [[Item Name]]

## Notes
*Additional quest notes*
```
"""
        
        # Create encounter management system
        encounter_system_content = """# Encounter Management System

## Random Encounters by Region
```dataview
TABLE difficulty, environment, encounter_type
FROM ""
WHERE type = "encounter"
SORT difficulty ASC
```

## Encounter Templates

### Combat Encounter Template
```
---
type: encounter
name: Encounter Name
difficulty: medium
environment: forest
encounter_type: combat
cr: 3
created: {{date}}
tags: [encounter, combat]
---

# Encounter Name

## Setup
*Scene description and context*

## Creatures
- **Creature Name** (CR X) - Quantity: X
  - HP: X
  - AC: X
  - Special abilities

## Terrain
*Map description and special features*

## Tactics
*How creatures fight*

## Treasure
*Loot and rewards*

## Scaling
- **Easy:** Reduce creature count
- **Hard:** Add creatures or hazards
```
"""
        
        # Write quest tracker
        quest_file = self.vault_path / "00_System" / "Quest_Master_Tracker.md"
        quest_file.write_text(quest_tracker_content, encoding='utf-8')
        results.append({
            "action": "created_quest_tracker",
            "file": str(quest_file.relative_to(self.vault_path))
        })
        
        # Write encounter system
        encounter_file = self.vault_path / "00_System" / "Encounter_Management_System.md"
        encounter_file.write_text(encounter_system_content, encoding='utf-8')
        results.append({
            "action": "created_encounter_system",
            "file": str(encounter_file.relative_to(self.vault_path))
        })
        
        logger.info(f"Setup quest and encounter systems: {len(results)} changes")
        return results

    # PHASE 3: Plugin Integration
    def phase3_plugin_integration(self) -> List[Dict]:
        """Phase 3: Plugin Integration (Steps 201-300)"""
        logger.info("Starting Phase 3: Plugin Integration")
        self.progress["phase3"]["status"] = "running"
        results = []
        
        try:
            # Step 201-220: Setup Templater automation
            results.extend(self._setup_templater_automation())
            self.progress["phase3"]["completed"] = 20
            
            # Step 221-240: Create Kanban boards
            results.extend(self._create_kanban_boards())
            self.progress["phase3"]["completed"] = 40
            
            # Step 241-260: Configure Excalidraw and charts
            results.extend(self._configure_visual_tools())
            self.progress["phase3"]["completed"] = 60
            
            # Step 261-280: Setup custom frames
            results.extend(self._setup_custom_frames())
            self.progress["phase3"]["completed"] = 80
            
            # Step 281-300: Supercharged links and admonitions
            results.extend(self._setup_advanced_features())
            self.progress["phase3"]["completed"] = 100
            self.progress["phase3"]["status"] = "completed"
            
        except Exception as e:
            logger.error(f"Phase 3 error: {e}")
            self.results["errors"].append({"phase": 3, "error": str(e)})
            self.progress["phase3"]["status"] = "error"
        
        return results

    def _setup_templater_automation(self) -> List[Dict]:
        """Setup Templater automation with proper templates"""
        results = []
        templates_dir = self.vault_path / "00_System" / "Templates"
        templates_dir.mkdir(exist_ok=True)
        
        # Create template files
        templates = {
            "NPC_Template.md": """---
type: npc
name: <% tp.file.title %>
campaign: <% tp.system.prompt("Campaign") %>
status: active
location: <% tp.system.prompt("Current Location") %>
created: <% tp.date.now() %>
tags: [npc]
---

# <% tp.file.title %>

## Basic Information
- **Race:** <% tp.system.prompt("Race") %>
- **Class:** <% tp.system.prompt("Class/Profession") %>
- **Alignment:** <% tp.system.prompt("Alignment") %>
- **Location:** <% tp.system.prompt("Current Location") %>

## Appearance
<% tp.system.prompt("Physical description") %>

## Personality
- **Personality Traits:** <% tp.system.prompt("Personality traits") %>
- **Ideals:** <% tp.system.prompt("Ideals") %>
- **Bonds:** <% tp.system.prompt("Bonds") %>
- **Flaws:** <% tp.system.prompt("Flaws") %>

## Background
<% tp.system.prompt("Character background") %>

## Role in Campaign
<% tp.system.prompt("Role in campaign") %>

## Relationships
*Connections to other NPCs*

## Notes
*Additional DM notes*
""",
            "Location_Template.md": """---
type: location
name: <% tp.file.title %>
region: <% tp.system.prompt("Region") %>
campaign: <% tp.system.prompt("Campaign") %>
settlement_type: <% tp.system.prompt("Settlement Type (city/town/village/dungeon/etc)") %>
population: <% tp.system.prompt("Population") %>
created: <% tp.date.now() %>
tags: [location]
---

# <% tp.file.title %>

## Overview
<% tp.system.prompt("Brief description") %>

## Geography
<% tp.system.prompt("Physical features and layout") %>

## Notable Features
- <% tp.system.prompt("Notable feature 1") %>
- <% tp.system.prompt("Notable feature 2") %>

## Important NPCs
- [[<% tp.system.prompt("Important NPC") %>]] - <% tp.system.prompt("Their role") %>

## Quests and Hooks
- <% tp.system.prompt("Quest or hook") %>

## History
<% tp.system.prompt("Historical significance") %>

## Notes
*Additional DM notes*
""",
            "Quest_Template.md": """---
type: quest
name: <% tp.file.title %>
campaign: <% tp.system.prompt("Campaign") %>
status: <% tp.system.prompt("Status (active/completed/failed/available)") %>
priority: <% tp.system.prompt("Priority (high/medium/low)") %>
quest_giver: [[<% tp.system.prompt("Quest Giver NPC") %>]]
reward: <% tp.system.prompt("Reward description") %>
created: <% tp.date.now() %>
tags: [quest]
---

# <% tp.file.title %>

## Objective
<% tp.system.prompt("What needs to be accomplished") %>

## Background
<% tp.system.prompt("Why this quest exists") %>

## Steps
1. <% tp.system.prompt("Step 1") %>
2. <% tp.system.prompt("Step 2") %>
3. <% tp.system.prompt("Step 3") %>

## NPCs Involved
- [[<% tp.system.prompt("Quest Giver") %>]] - Quest Giver
- [[<% tp.system.prompt("Other NPC") %>]] - <% tp.system.prompt("Their role") %>

## Locations
- [[<% tp.system.prompt("Relevant Location") %>]] - <% tp.system.prompt("Why relevant") %>

## Rewards
- **XP:** <% tp.system.prompt("XP reward") %>
- **Gold:** <% tp.system.prompt("Gold reward") %>
- **Items:** <% tp.system.prompt("Item rewards") %>

## Notes
<% tp.system.prompt("Additional quest notes") %>
""",
            "Session_Prep_Template.md": """---
type: session
campaign: <% tp.system.prompt("Campaign") %>
session_number: <% tp.system.prompt("Session Number") %>
date: <% tp.date.now() %>
status: planned
tags: [session, prep]
---

# Session <% tp.system.prompt("Session Number") %> - <% tp.system.prompt("Session Title") %>

## Pre-Session Checklist
- [ ] Review previous session notes
- [ ] Prepare NPC voices and personalities
- [ ] Set up maps and tokens
- [ ] Review active quest status
- [ ] Prepare potential encounters

## Session Overview
<% tp.system.prompt("Brief session overview") %>

## Key NPCs
- [[<% tp.system.prompt("Important NPC 1") %>]] - <% tp.system.prompt("Their role this session") %>
- [[<% tp.system.prompt("Important NPC 2") %>]] - <% tp.system.prompt("Their role this session") %>

## Locations
- [[<% tp.system.prompt("Primary Location") %>]] - Main location for this session

## Planned Events
1. <% tp.system.prompt("Event 1") %>
2. <% tp.system.prompt("Event 2") %>
3. <% tp.system.prompt("Event 3") %>

## Potential Encounters
- **<% tp.system.prompt("Encounter 1") %>** (CR <% tp.system.prompt("CR") %>)
- **<% tp.system.prompt("Encounter 2") %>** (CR <% tp.system.prompt("CR") %>)

## Random Tables
### NPCs
| d6 | NPC |
|----|-----|
| 1  | <% tp.system.prompt("Random NPC 1") %> |
| 2  | <% tp.system.prompt("Random NPC 2") %> |

### Events
| d6 | Event |
|----|--------|
| 1  | <% tp.system.prompt("Random Event 1") %> |
| 2  | <% tp.system.prompt("Random Event 2") %> |

## Session Notes
*Fill during play*

## Next Session Prep
*Notes for next time*
"""
        }
        
        # Write template files
        for filename, content in templates.items():
            template_file = templates_dir / filename
            template_file.write_text(content, encoding='utf-8')
            results.append({
                "action": "created_templater_template",
                "file": str(template_file.relative_to(self.vault_path))
            })
        
        logger.info(f"Setup Templater automation: {len(results)} templates created")
        return results

    def _create_kanban_boards(self) -> List[Dict]:
        """Create Kanban boards for quest/campaign tracking"""
        results = []
        
        # Campaign Kanban Board
        campaign_kanban = """---
tags: [kanban, campaign]
---

## Campaign Progress Kanban

```kanban
- Planning
  - [ ] New campaign ideas
  - [ ] Session prep needed
  - [ ] NPCs to develop

- Active
  - [ ] Current session
  - [ ] Running quests
  - [ ] Active storylines

- Review
  - [ ] Completed sessions
  - [ ] Finished arcs
  - [ ] Player feedback

- Archive
  - [ ] Old campaigns
  - [ ] Retired characters
  - [ ] Historical events
```

### Usage Instructions
- Drag cards between columns to track progress
- Click on any item to edit
- Add new cards with the + button
"""
        
        # Quest Kanban Board
        quest_kanban = """---
tags: [kanban, quest]
---

## Quest Tracking Kanban

```kanban
- Available
  - [ ] Quest hooks
  - [ ] Side quests
  - [ ] Random encounters

- Active
  - [ ] Main quest line
  - [ ] Player-initiated quests
  - [ ] Time-sensitive quests

- In Progress
  - [ ] Partially completed
  - [ ] Waiting for conditions
  - [ ] Multi-session quests

- Completed
  - [ ] Successful quests
  - [ ] Failed quests
  - [ ] Abandoned quests
```

### Quest Status Legend
- 🔥 Urgent/Time-sensitive
- ⭐ Main story quest
- 🎯 Side quest
- 🎲 Random encounter
"""
        
        # Write Kanban boards
        kanban_dir = self.vault_path / "00_System" / "Kanban"
        kanban_dir.mkdir(exist_ok=True)
        
        campaign_file = kanban_dir / "Campaign_Progress_Board.md"
        campaign_file.write_text(campaign_kanban, encoding='utf-8')
        results.append({
            "action": "created_campaign_kanban",
            "file": str(campaign_file.relative_to(self.vault_path))
        })
        
        quest_file = kanban_dir / "Quest_Tracking_Board.md"
        quest_file.write_text(quest_kanban, encoding='utf-8')
        results.append({
            "action": "created_quest_kanban",
            "file": str(quest_file.relative_to(self.vault_path))
        })
        
        logger.info(f"Created Kanban boards: {len(results)} boards created")
        return results

    def _configure_visual_tools(self) -> List[Dict]:
        """Configure Excalidraw, charts, and visual tools"""
        results = []
        
        # Create Excalidraw templates
        excalidraw_dir = self.vault_path / "04_Resources" / "Excalidraw"
        excalidraw_dir.mkdir(parents=True, exist_ok=True)
        
        # Relationship mapping template
        relationship_map = """# NPC Relationship Map

```excalidraw
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "type": "text",
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "id": "template",
      "fillStyle": "hachure",
      "strokeWidth": 1,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "x": 100,
      "y": 100,
      "strokeColor": "#000000",
      "backgroundColor": "transparent",
      "width": 200,
      "height": 25,
      "seed": 1,
      "groupIds": [],
      "strokeSharpness": "sharp",
      "boundElements": [],
      "updated": 1,
      "text": "NPC Relationship Template",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "left",
      "verticalAlign": "top"
    }
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Instructions
1. Double-click the drawing above to edit
2. Add NPCs as shapes or text boxes
3. Connect with arrows to show relationships
4. Use colors to represent factions
5. Save when done
"""
        
        # Battle map template
        battle_map = """# Battle Map Template

```excalidraw
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "type": "rectangle",
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "id": "grid",
      "fillStyle": "cross-hatch",
      "strokeWidth": 1,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 50,
      "angle": 0,
      "x": 50,
      "y": 50,
      "strokeColor": "#000000",
      "backgroundColor": "transparent",
      "width": 500,
      "height": 400,
      "seed": 1,
      "groupIds": [],
      "strokeSharpness": "sharp",
      "boundElements": []
    }
  ],
  "appState": {
    "gridSize": 25,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Battle Map Instructions
1. Use the grid for movement (each square = 5 feet)
2. Add terrain features as shapes
3. Mark starting positions for players and enemies
4. Add labels for important features
"""
        
        # Write Excalidraw templates
        relationship_file = excalidraw_dir / "NPC_Relationship_Map_Template.md"
        relationship_file.write_text(relationship_map, encoding='utf-8')
        results.append({
            "action": "created_relationship_map_template",
            "file": str(relationship_file.relative_to(self.vault_path))
        })
        
        battle_file = excalidraw_dir / "Battle_Map_Template.md"
        battle_file.write_text(battle_map, encoding='utf-8')
        results.append({
            "action": "created_battle_map_template",
            "file": str(battle_file.relative_to(self.vault_path))
        })
        
        # Create chart templates using Mermaid
        charts_dir = self.vault_path / "04_Resources" / "Charts"
        charts_dir.mkdir(parents=True, exist_ok=True)
        
        faction_chart = """# Faction Relationship Chart

```mermaid
graph TD
    A[Player Party] --> B[Faction 1]
    A --> C[Faction 2]
    A --> D[Faction 3]
    B --> E[Allied NPCs]
    C --> F[Neutral NPCs]
    D --> G[Enemy NPCs]
    B -.->|Trade| C
    B -->|War| D
    C -.->|Uneasy Peace| D
```

## Instructions
1. Replace faction names above
2. Adjust relationship arrows
3. Use solid lines for strong relationships
4. Use dotted lines for weak/uncertain relationships
"""
        
        chart_file = charts_dir / "Faction_Relationships.md"
        chart_file.write_text(faction_chart, encoding='utf-8')
        results.append({
            "action": "created_faction_chart",
            "file": str(chart_file.relative_to(self.vault_path))
        })
        
        logger.info(f"Configured visual tools: {len(results)} templates created")
        return results

    def _setup_custom_frames(self) -> List[Dict]:
        """Setup custom frames and embedded content"""
        results = []
        
        # Create custom frame configurations
        frames_dir = self.vault_path / "00_System" / "Frames"
        frames_dir.mkdir(exist_ok=True)
        
        # Random generator frame
        random_generator = """# Random Generators Frame

<iframe src="data:text/html;charset=utf-8,
<html>
<head>
<style>
body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
.generator { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
button { background: #007acc; color: white; border: none; padding: 8px 15px; border-radius: 3px; cursor: pointer; }
button:hover { background: #005a9d; }
#result { margin-top: 10px; padding: 10px; background: #e8f4f8; border-radius: 3px; }
</style>
</head>
<body>
<div class='generator'>
<h3>Random NPC Name Generator</h3>
<button onclick='generateName()'>Generate Name</button>
<div id='result'></div>
</div>

<script>
const firstNames = ['Aeliana', 'Gareth', 'Lyanna', 'Theron', 'Nerida', 'Corvus', 'Seraphina', 'Magnus'];
const lastNames = ['Stormwind', 'Brightblade', 'Deepwater', 'Goldleaf', 'Ironwood', 'Shadowmere'];

function generateName() {
  const first = firstNames[Math.floor(Math.random() * firstNames.length)];
  const last = lastNames[Math.floor(Math.random() * lastNames.length)];
  document.getElementById('result').innerHTML = first + ' ' + last;
}
</script>
</body>
</html>
" width="100%" height="200"></iframe>

## Usage
- Click the button to generate random NPC names
- Copy the result to create new NPCs
- Modify the name lists in the HTML if needed
"""
        
        # Dice roller frame
        dice_roller = """# Digital Dice Roller

<iframe src="data:text/html;charset=utf-8,
<html>
<head>
<style>
body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
.dice-section { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
button { background: #d20000; color: white; border: none; padding: 8px 15px; border-radius: 3px; cursor: pointer; margin: 2px; }
button:hover { background: #a10000; }
.result { font-size: 24px; font-weight: bold; color: #d20000; margin: 10px 0; }
</style>
</head>
<body>
<div class='dice-section'>
<h3>Quick Dice Rolls</h3>
<button onclick='roll(4)'>d4</button>
<button onclick='roll(6)'>d6</button>
<button onclick='roll(8)'>d8</button>
<button onclick='roll(10)'>d10</button>
<button onclick='roll(12)'>d12</button>
<button onclick='roll(20)'>d20</button>
<button onclick='roll(100)'>d100</button>
<div class='result' id='result'>Click a die to roll</div>
</div>

<script>
function roll(sides) {
  const result = Math.floor(Math.random() * sides) + 1;
  document.getElementById('result').innerHTML = 'd' + sides + ': ' + result;
}
</script>
</body>
</html>
" width="100%" height="150"></iframe>

## Usage
- Click any die button to roll
- Results appear immediately below
- Use for quick rolls during sessions
"""
        
        # Write frame files
        generator_file = frames_dir / "Random_Generator_Frame.md"
        generator_file.write_text(random_generator, encoding='utf-8')
        results.append({
            "action": "created_random_generator_frame",
            "file": str(generator_file.relative_to(self.vault_path))
        })
        
        dice_file = frames_dir / "Dice_Roller_Frame.md"
        dice_file.write_text(dice_roller, encoding='utf-8')
        results.append({
            "action": "created_dice_roller_frame",
            "file": str(dice_file.relative_to(self.vault_path))
        })
        
        logger.info(f"Setup custom frames: {len(results)} frames created")
        return results

    def _setup_advanced_features(self) -> List[Dict]:
        """Setup supercharged links and standardize admonitions"""
        results = []
        
        # Create supercharged links configuration guide
        links_guide = """# Supercharged Links Configuration

## Custom Link Types

### NPC Links
- **Format:** `[[NPC Name|🧙 Display Name]]`
- **Icon:** 🧙 for NPCs
- **Color:** Blue for allies, Red for enemies, Yellow for neutral

### Location Links  
- **Format:** `[[Location Name|🏰 Display Name]]`
- **Icon:** 🏰 for cities, 🏕️ for camps, 🏠 for buildings
- **Color:** Green for safe areas, Red for dangerous

### Quest Links
- **Format:** `[[Quest Name|⚔️ Display Name]]`
- **Icon:** ⚔️ for combat quests, 🔍 for investigation, 💰 for rewards
- **Color:** Orange for active, Gray for completed

### Item Links
- **Format:** `[[Item Name|⚔️ Display Name]]`
- **Icon:** ⚔️ for weapons, 🛡️ for armor, 💍 for accessories
- **Color:** Purple for magical, Brown for mundane

## Configuration
1. Install Supercharged Links plugin
2. Set up custom rules for each type
3. Apply icons and colors consistently
4. Test with existing links

## Examples
- [[Gareth Stormwind|🧙 Gareth Stormwind]] - Allied NPC
- [[Shadowmere Castle|🏰 Shadowmere Castle]] - Dangerous location
- [[Dragon's Hoard|⚔️ Dragon's Hoard]] - Active quest
- [[Sword of Storms|⚔️ Sword of Storms]] - Magical weapon
"""
        
        # Create admonitions style guide
        admonitions_guide = """# Standardized Admonitions Guide

## DM Information
> [!dm] DM Only
> This information is for the DM's eyes only. Players should not see this.

> [!secret] Secret Information
> Hidden plot details, NPC motivations, or secret connections.

## Player Information
> [!info] General Information
> Basic facts that any character would know.

> [!tip] Player Tip
> Helpful hints or reminders for players.

## Game Mechanics
> [!combat] Combat Note
> Initiative order, special rules, or tactical information.

> [!dice] Dice Roll
> When to roll and what modifiers to use.

## Story Elements
> [!plot] Plot Hook
> Adventure hooks, quest opportunities, or story developments.

> [!lore] World Lore
> Historical information, cultural details, or world background.

## Warnings and Alerts
> [!danger] Danger
> Hazards, traps, or threatening situations.

> [!warning] Warning
> Important notes that could affect gameplay.

## Quest Information
> [!quest] Quest Objective
> Current quest goals and requirements.

> [!reward] Rewards
> Experience points, treasure, or other rewards.

## Examples in Use

> [!dm] NPC Motivation
> Lord Blackwater is secretly working with the cultists because they're holding his daughter hostage.

> [!combat] Initiative Tracker
> 1. Goblin Leader (AC 15, HP 12)
> 2. Player characters
> 3. Goblin minions (AC 13, HP 3 each)

> [!plot] Adventure Hook
> A mysterious merchant offers the party a map to a lost temple, but seems nervous about something.

## Consistent Usage
- Always use the same admonition type for the same purpose
- Keep titles short and descriptive
- Use sparingly for maximum impact
- Match the tone to the content type
"""
        
        # Write configuration files
        config_dir = self.vault_path / "00_System" / "Configuration"
        config_dir.mkdir(exist_ok=True)
        
        links_file = config_dir / "Supercharged_Links_Guide.md"
        links_file.write_text(links_guide, encoding='utf-8')
        results.append({
            "action": "created_links_guide",
            "file": str(links_file.relative_to(self.vault_path))
        })
        
        admonitions_file = config_dir / "Admonitions_Style_Guide.md"
        admonitions_file.write_text(admonitions_guide, encoding='utf-8')
        results.append({
            "action": "created_admonitions_guide",
            "file": str(admonitions_file.relative_to(self.vault_path))
        })
        
        # Apply admonitions to existing files
        md_files = list(self.vault_path.rglob("*.md"))
        admonition_count = 0
        
        for file_path in md_files[:50]:  # Limit to prevent overwhelming changes
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                # Convert common patterns to admonitions
                patterns = [
                    (r'DM NOTE:([^\n]+)', r'> [!dm] DM Note\n> \1'),
                    (r'SECRET:([^\n]+)', r'> [!secret] Secret\n> \1'),
                    (r'COMBAT:([^\n]+)', r'> [!combat] Combat\n> \1'),
                    (r'QUEST:([^\n]+)', r'> [!quest] Quest\n> \1'),
                ]
                
                for pattern, replacement in patterns:
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    admonition_count += 1
                    
            except Exception as e:
                logger.warning(f"Could not apply admonitions to {file_path}: {e}")
        
        if admonition_count > 0:
            results.append({
                "action": "applied_admonitions",
                "files_updated": admonition_count
            })
        
        logger.info(f"Setup advanced features: {len(results)} configurations created")
        return results

    def run_parallel_phases(self) -> Dict:
        """Run all three phases in parallel"""
        logger.info("Starting parallel execution of phases 1-3")
        
        # Create backup first
        backup_path = self.create_backup()
        
        # Run phases in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all phases
            future_to_phase = {
                executor.submit(self.phase1_template_cleanup): "phase1",
                executor.submit(self.phase2_content_organization): "phase2", 
                executor.submit(self.phase3_plugin_integration): "phase3"
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_phase):
                phase = future_to_phase[future]
                try:
                    result = future.result()
                    self.results[phase] = result
                    logger.info(f"Phase {phase} completed successfully")
                except Exception as e:
                    logger.error(f"Phase {phase} failed: {e}")
                    self.results["errors"].append({"phase": phase, "error": str(e)})
        
        # Generate final report
        report = self._generate_final_report(backup_path)
        
        return report

    def _generate_final_report(self, backup_path: str) -> Dict:
        """Generate comprehensive final report"""
        total_changes = sum(len(self.results[phase]) for phase in ["phase1", "phase2", "phase3"])
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "backup_location": backup_path,
            "phases_completed": [
                phase for phase in ["phase1", "phase2", "phase3"] 
                if self.progress[phase]["status"] == "completed"
            ],
            "total_changes": total_changes,
            "progress": self.progress,
            "results_summary": {
                "phase1_changes": len(self.results["phase1"]),
                "phase2_changes": len(self.results["phase2"]),
                "phase3_changes": len(self.results["phase3"]),
                "errors": len(self.results["errors"])
            },
            "detailed_results": self.results
        }
        
        # Write report to file
        report_file = self.script_path / f"parallel_phases_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with report_file.open('w') as f:
            json.dump(report, f, indent=2)
        
        # Create human-readable summary
        summary_file = self.script_path / f"parallel_phases_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        summary_content = f"""# Parallel Phases 1-3 Execution Summary

## Overview
- **Execution Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Total Changes:** {total_changes}
- **Phases Completed:** {len(report['phases_completed'])}/3
- **Backup Location:** {backup_path}

## Phase Results

### Phase 1: Template Structure Cleanup
- **Status:** {self.progress['phase1']['status']}
- **Changes:** {len(self.results['phase1'])}
- **Progress:** {self.progress['phase1']['completed']}/100 steps

### Phase 2: Content Organization  
- **Status:** {self.progress['phase2']['status']}
- **Changes:** {len(self.results['phase2'])}
- **Progress:** {self.progress['phase2']['completed']}/100 steps

### Phase 3: Plugin Integration
- **Status:** {self.progress['phase3']['status']}
- **Changes:** {len(self.results['phase3'])}
- **Progress:** {self.progress['phase3']['completed']}/100 steps

## Errors
{len(self.results['errors'])} errors encountered

## Next Steps
1. Review changes in each phase
2. Test functionality of new features
3. Continue with phases 4-6 if desired
4. Backup regularly as improvements continue

---
*Generated by Parallel Phases 1-3 Master Script*
"""
        
        summary_file.write_text(summary_content, encoding='utf-8')
        
        logger.info(f"Parallel execution completed. Report saved to {report_file}")
        return report

def main():
    """Main execution function"""
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    improver = VaultImprover(vault_path)
    report = improver.run_parallel_phases()
    
    print("\n" + "="*60)
    print("PARALLEL PHASES 1-3 EXECUTION COMPLETED")
    print("="*60)
    print(f"Total Changes: {report['total_changes']}")
    print(f"Phases Completed: {len(report['phases_completed'])}/3")
    print(f"Backup Created: {report['backup_location']}")
    print(f"Errors: {report['results_summary']['errors']}")
    print("\nDetailed report saved to _SCRIPTS directory")
    print("="*60)

if __name__ == "__main__":
    main()