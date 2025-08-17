#!/usr/bin/env python3
"""
Virtual Table Integration (#31)
Sprint 2 - Collaboration Core

Export and sync TTRPG content to Roll20/Foundry VTT platforms with one-click transfer.
Built following lean/agile MVI principles for immediate usability.
"""

import json
import os
import argparse
import zipfile
import base64
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import xml.etree.ElementTree as ET


@dataclass
class VTTAsset:
    """Represents an asset for VTT export"""
    name: str
    type: str  # npc, location, item, spell, handout
    description: str
    image_path: Optional[str] = None
    stats: Optional[Dict] = None
    metadata: Optional[Dict] = None


@dataclass
class VTTExportJob:
    """Represents an export operation"""
    job_id: str
    platform: str  # roll20, foundry
    status: str  # pending, processing, completed, failed
    created_at: str
    content_paths: List[str]
    export_path: Optional[str] = None
    error_message: Optional[str] = None


class VTTExporter:
    """Core VTT export system"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.export_dir = self.vault_path / "scripts" / "vtt_exports"
        self.export_dir.mkdir(exist_ok=True)
        
        self.jobs_file = self.export_dir / "export_jobs.json"
        self.jobs = self._load_jobs()
    
    def _load_jobs(self) -> Dict[str, VTTExportJob]:
        """Load export jobs from storage"""
        if not self.jobs_file.exists():
            return {}
        
        try:
            with open(self.jobs_file, 'r') as f:
                data = json.load(f)
            return {job_id: VTTExportJob(**job_data) for job_id, job_data in data.items()}
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def _save_jobs(self):
        """Save export jobs to storage"""
        with open(self.jobs_file, 'w') as f:
            data = {job_id: asdict(job) for job_id, job in self.jobs.items()}
            json.dump(data, f, indent=2)
    
    def _generate_job_id(self) -> str:
        """Generate unique job ID"""
        timestamp = str(int(datetime.now().timestamp()))
        hash_input = f"{timestamp}{len(self.jobs)}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:8]
    
    def _parse_markdown_content(self, file_path: Path) -> VTTAsset:
        """Parse markdown file and extract VTT-relevant data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter = {}
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        import yaml
                        frontmatter = yaml.safe_load(parts[1]) or {}
                    except ImportError:
                        # Parse basic frontmatter without YAML
                        for line in parts[1].strip().split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                frontmatter[key.strip()] = value.strip()
                    content = parts[2]
            
            # Determine asset type based on path and content
            path_str = str(file_path.relative_to(self.vault_path))
            asset_type = self._determine_asset_type(path_str, content, frontmatter)
            
            # Extract name
            name = frontmatter.get('title') or file_path.stem
            
            # Clean description
            description = self._clean_content_for_vtt(content)
            
            # Extract stats if it's an NPC
            stats = None
            if asset_type == 'npc':
                stats = self._extract_npc_stats(content)
            elif asset_type == 'item':
                stats = self._extract_item_stats(content)
            
            return VTTAsset(
                name=name,
                type=asset_type,
                description=description,
                stats=stats,
                metadata={
                    'source_file': path_str,
                    'tags': frontmatter.get('tags', []),
                    'world': frontmatter.get('world', 'Both'),
                    'type': frontmatter.get('type', 'Unknown')
                }
            )
            
        except Exception as e:
            # Return minimal asset on error
            return VTTAsset(
                name=file_path.stem,
                type='handout',
                description=f"Error parsing content: {str(e)}",
                metadata={'source_file': str(file_path.relative_to(self.vault_path))}
            )
    
    def _determine_asset_type(self, path: str, content: str, frontmatter: Dict) -> str:
        """Determine VTT asset type from file path and content"""
        path_lower = path.lower()
        content_lower = content.lower()
        
        # Check frontmatter type
        fm_type = frontmatter.get('type', '').lower()
        if fm_type in ['npc', 'character', 'creature']:
            return 'npc'
        elif fm_type in ['item', 'artifact', 'weapon', 'armor']:
            return 'item'
        elif fm_type in ['location', 'place']:
            return 'location'
        elif fm_type in ['spell', 'magic']:
            return 'spell'
        
        # Check path patterns
        if 'groups' in path_lower or 'npc' in path_lower:
            return 'npc'
        elif 'items' in path_lower:
            return 'item'
        elif 'locations' in path_lower or 'places' in path_lower:
            return 'location'
        elif 'lore' in path_lower or 'worldbuilding' in path_lower:
            return 'handout'
        elif 'mechanics' in path_lower and 'spell' in content_lower:
            return 'spell'
        
        # Check content patterns
        if any(stat in content_lower for stat in ['ac:', 'armor class', 'hit points', 'hp:', 'str:', 'dex:', 'con:']):
            return 'npc'
        elif any(item in content_lower for item in ['damage:', 'weight:', 'rarity:', 'requires attunement']):
            return 'item'
        
        return 'handout'
    
    def _clean_content_for_vtt(self, content: str) -> str:
        """Clean markdown content for VTT consumption"""
        # Remove frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        
        # Convert markdown to simpler format
        # Remove wiki links but keep the text
        content = re.sub(r'\[\[([^\]]+)\]\]', r'\1', content)
        
        # Convert headers
        content = re.sub(r'^# (.+)$', r'**\1**', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'**\1**', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'*\1*', content, flags=re.MULTILINE)
        
        # Clean up excessive whitespace
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        return content.strip()
    
    def _extract_npc_stats(self, content: str) -> Optional[Dict]:
        """Extract D&D 5e style stats from NPC content"""
        stats = {}
        
        # Look for common stat patterns
        patterns = {
            'ac': r'(?:AC|Armor Class)[:\s]+(\d+)',
            'hp': r'(?:HP|Hit Points)[:\s]+(\d+)',
            'speed': r'Speed[:\s]+([^\n]+)',
            'str': r'STR[:\s]+(\d+)',
            'dex': r'DEX[:\s]+(\d+)',
            'con': r'CON[:\s]+(\d+)',
            'int': r'INT[:\s]+(\d+)',
            'wis': r'WIS[:\s]+(\d+)',
            'cha': r'CHA[:\s]+(\d+)',
            'cr': r'(?:CR|Challenge Rating)[:\s]+([\d/]+)',
            'proficiency': r'Proficiency Bonus[:\s]+\+?(\d+)'
        }
        
        content_upper = content.upper()
        for stat, pattern in patterns.items():
            match = re.search(pattern, content_upper, re.IGNORECASE)
            if match:
                stats[stat] = match.group(1).strip()
        
        return stats if stats else None
    
    def _extract_item_stats(self, content: str) -> Optional[Dict]:
        """Extract item stats from content"""
        stats = {}
        
        patterns = {
            'type': r'Type[:\s]+([^\n]+)',
            'rarity': r'Rarity[:\s]+([^\n]+)',
            'damage': r'Damage[:\s]+([^\n]+)',
            'weight': r'Weight[:\s]+([^\n]+)',
            'value': r'(?:Value|Cost)[:\s]+([^\n]+)',
            'attunement': r'(Requires Attunement)'
        }
        
        for stat, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                stats[stat] = match.group(1).strip()
        
        return stats if stats else None
    
    def create_export_job(self, platform: str, content_paths: List[str]) -> str:
        """Create new export job"""
        job_id = self._generate_job_id()
        
        job = VTTExportJob(
            job_id=job_id,
            platform=platform,
            status='pending',
            created_at=datetime.now().isoformat(),
            content_paths=content_paths
        )
        
        self.jobs[job_id] = job
        self._save_jobs()
        return job_id
    
    def process_export_job(self, job_id: str) -> bool:
        """Process an export job"""
        if job_id not in self.jobs:
            return False
        
        job = self.jobs[job_id]
        job.status = 'processing'
        self._save_jobs()
        
        try:
            # Collect assets
            assets = []
            for content_path in job.content_paths:
                file_path = self.vault_path / content_path
                if file_path.exists() and file_path.suffix == '.md':
                    asset = self._parse_markdown_content(file_path)
                    assets.append(asset)
            
            # Export based on platform
            if job.platform == 'roll20':
                export_path = self._export_to_roll20(job_id, assets)
            elif job.platform == 'foundry':
                export_path = self._export_to_foundry(job_id, assets)
            else:
                raise ValueError(f"Unsupported platform: {job.platform}")
            
            job.status = 'completed'
            job.export_path = str(export_path)
            
        except Exception as e:
            job.status = 'failed'
            job.error_message = str(e)
            return False
        finally:
            self._save_jobs()
        
        return True
    
    def _export_to_roll20(self, job_id: str, assets: List[VTTAsset]) -> Path:
        """Export assets to Roll20 format"""
        export_path = self.export_dir / f"roll20_{job_id}"
        export_path.mkdir(exist_ok=True)
        
        # Create handouts
        handouts = []
        characters = []
        
        for asset in assets:
            if asset.type == 'npc':
                character = self._create_roll20_character(asset)
                characters.append(character)
            else:
                handout = self._create_roll20_handout(asset)
                handouts.append(handout)
        
        # Save as JSON files for Roll20 API consumption
        with open(export_path / 'handouts.json', 'w') as f:
            json.dump(handouts, f, indent=2)
        
        with open(export_path / 'characters.json', 'w') as f:
            json.dump(characters, f, indent=2)
        
        # Create import script
        import_script = self._create_roll20_import_script(handouts, characters)
        with open(export_path / 'import_script.js', 'w') as f:
            f.write(import_script)
        
        # Create README
        readme = self._create_roll20_readme()
        with open(export_path / 'README.md', 'w') as f:
            f.write(readme)
        
        # Create zip file
        zip_path = export_path.parent / f"roll20_{job_id}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in export_path.rglob('*'):
                if file_path.is_file():
                    zf.write(file_path, file_path.relative_to(export_path))
        
        return zip_path
    
    def _export_to_foundry(self, job_id: str, assets: List[VTTAsset]) -> Path:
        """Export assets to Foundry VTT format"""
        export_path = self.export_dir / f"foundry_{job_id}"
        export_path.mkdir(exist_ok=True)
        
        # Create module structure
        actors = []
        items = []
        journal_entries = []
        
        for asset in assets:
            if asset.type == 'npc':
                actor = self._create_foundry_actor(asset)
                actors.append(actor)
            elif asset.type == 'item':
                item = self._create_foundry_item(asset)
                items.append(item)
            else:
                journal = self._create_foundry_journal(asset)
                journal_entries.append(journal)
        
        # Create module manifest
        manifest = {
            "name": "cordelia-export",
            "title": "Cordelia Vault Export",
            "description": f"Exported content from Cordelia TTRPG Vault - Job {job_id}",
            "version": "1.0.0",
            "author": "Cordelia Vault System",
            "systems": ["dnd5e"],
            "minimumCoreVersion": "10.291",
            "packs": []
        }
        
        if actors:
            manifest["packs"].append({
                "name": "actors",
                "label": "Actors",
                "type": "Actor",
                "path": "./packs/actors.db"
            })
        
        if items:
            manifest["packs"].append({
                "name": "items", 
                "label": "Items",
                "type": "Item",
                "path": "./packs/items.db"
            })
        
        if journal_entries:
            manifest["packs"].append({
                "name": "journals",
                "label": "Journal Entries", 
                "type": "JournalEntry",
                "path": "./packs/journals.db"
            })
        
        with open(export_path / 'module.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Create pack data files (simplified JSON for this MVI)
        packs_dir = export_path / 'packs'
        packs_dir.mkdir(exist_ok=True)
        
        if actors:
            with open(packs_dir / 'actors.json', 'w') as f:
                json.dump(actors, f, indent=2)
        
        if items:
            with open(packs_dir / 'items.json', 'w') as f:
                json.dump(items, f, indent=2)
        
        if journal_entries:
            with open(packs_dir / 'journals.json', 'w') as f:
                json.dump(journal_entries, f, indent=2)
        
        # Create installation README
        readme = self._create_foundry_readme()
        with open(export_path / 'README.md', 'w') as f:
            f.write(readme)
        
        # Create zip file
        zip_path = export_path.parent / f"foundry_{job_id}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in export_path.rglob('*'):
                if file_path.is_file():
                    zf.write(file_path, file_path.relative_to(export_path))
        
        return zip_path
    
    def _create_roll20_character(self, asset: VTTAsset) -> Dict:
        """Create Roll20 character sheet data"""
        character = {
            "name": asset.name,
            "bio": asset.description,
            "gmnotes": f"Imported from: {asset.metadata.get('source_file', 'Unknown')}",
            "controlledby": "",
            "inplayerjournals": "",
            "defaulttoken": "",
            "archived": False
        }
        
        # Add stats if available
        if asset.stats:
            attributes = {}
            stat_mapping = {
                'ac': 'ac',
                'hp': 'hp',
                'str': 'strength',
                'dex': 'dexterity', 
                'con': 'constitution',
                'int': 'intelligence',
                'wis': 'wisdom',
                'cha': 'charisma'
            }
            
            for stat_key, roll20_key in stat_mapping.items():
                if stat_key in asset.stats:
                    attributes[roll20_key] = {
                        "current": asset.stats[stat_key],
                        "max": asset.stats[stat_key]
                    }
            
            if attributes:
                character["attributes"] = attributes
        
        return character
    
    def _create_roll20_handout(self, asset: VTTAsset) -> Dict:
        """Create Roll20 handout data"""
        return {
            "name": asset.name,
            "notes": asset.description,
            "gmnotes": f"Type: {asset.type}\nSource: {asset.metadata.get('source_file', 'Unknown')}",
            "inplayerjournals": "all",
            "controlledby": "",
            "archived": False
        }
    
    def _create_foundry_actor(self, asset: VTTAsset) -> Dict:
        """Create Foundry VTT actor data"""
        actor = {
            "_id": self._generate_foundry_id(),
            "name": asset.name,
            "type": "npc",
            "img": "icons/mystery-man.svg",
            "data": {
                "details": {
                    "biography": {
                        "value": asset.description,
                        "public": ""
                    }
                }
            },
            "token": {},
            "items": [],
            "effects": [],
            "folder": None,
            "sort": 0,
            "permission": {"default": 0},
            "flags": {
                "cordelia": {
                    "source_file": asset.metadata.get('source_file', 'Unknown'),
                    "imported_at": datetime.now().isoformat()
                }
            }
        }
        
        # Add stats if available
        if asset.stats:
            abilities = actor["data"]["abilities"] = {}
            stat_mapping = {
                'str': 'str', 'dex': 'dex', 'con': 'con',
                'int': 'int', 'wis': 'wis', 'cha': 'cha'
            }
            
            for stat_key, foundry_key in stat_mapping.items():
                if stat_key in asset.stats:
                    try:
                        value = int(asset.stats[stat_key])
                        abilities[foundry_key] = {
                            "value": value,
                            "proficient": 0,
                            "bonuses": {"check": "", "save": ""}
                        }
                    except ValueError:
                        pass
            
            # Add other stats
            actor["data"]["attributes"] = {}
            if 'ac' in asset.stats:
                try:
                    actor["data"]["attributes"]["ac"] = {"value": int(asset.stats['ac'])}
                except ValueError:
                    pass
            
            if 'hp' in asset.stats:
                try:
                    hp_val = int(asset.stats['hp'])
                    actor["data"]["attributes"]["hp"] = {
                        "value": hp_val,
                        "max": hp_val,
                        "temp": 0,
                        "tempmax": 0
                    }
                except ValueError:
                    pass
        
        return actor
    
    def _create_foundry_item(self, asset: VTTAsset) -> Dict:
        """Create Foundry VTT item data"""
        item = {
            "_id": self._generate_foundry_id(),
            "name": asset.name,
            "type": "equipment",
            "img": "icons/svg/item-bag.svg",
            "data": {
                "description": {
                    "value": asset.description,
                    "chat": "",
                    "unidentified": ""
                },
                "source": asset.metadata.get('source_file', 'Unknown'),
                "quantity": 1,
                "weight": 0,
                "price": 0,
                "attunement": 0,
                "equipped": False,
                "rarity": "",
                "identified": True
            },
            "effects": [],
            "folder": None,
            "sort": 0,
            "permission": {"default": 0},
            "flags": {
                "cordelia": {
                    "source_file": asset.metadata.get('source_file', 'Unknown'),
                    "imported_at": datetime.now().isoformat()
                }
            }
        }
        
        # Add item-specific stats
        if asset.stats:
            if 'rarity' in asset.stats:
                item["data"]["rarity"] = asset.stats['rarity'].lower()
            if 'weight' in asset.stats:
                try:
                    item["data"]["weight"] = float(re.findall(r'[\d.]+', asset.stats['weight'])[0])
                except (ValueError, IndexError):
                    pass
            if 'attunement' in asset.stats:
                item["data"]["attunement"] = 1
        
        return item
    
    def _create_foundry_journal(self, asset: VTTAsset) -> Dict:
        """Create Foundry VTT journal entry data"""
        return {
            "_id": self._generate_foundry_id(),
            "name": asset.name,
            "content": asset.description,
            "img": None,
            "folder": None,
            "sort": 0,
            "permission": {"default": 0},
            "flags": {
                "cordelia": {
                    "source_file": asset.metadata.get('source_file', 'Unknown'),
                    "asset_type": asset.type,
                    "imported_at": datetime.now().isoformat()
                }
            }
        }
    
    def _generate_foundry_id(self) -> str:
        """Generate Foundry-compatible ID"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    
    def _create_roll20_import_script(self, handouts: List[Dict], characters: List[Dict]) -> str:
        """Create Roll20 API import script"""
        return f'''
// Cordelia Vault Import Script for Roll20
// This script imports {len(handouts)} handouts and {len(characters)} characters

// Import handouts
const handouts = {json.dumps(handouts, indent=2)};
handouts.forEach(handoutData => {{
    createObj("handout", handoutData);
}});

// Import characters  
const characters = {json.dumps(characters, indent=2)};
characters.forEach(characterData => {{
    createObj("character", characterData);
}});

sendChat("Import Script", "Successfully imported " + handouts.length + " handouts and " + characters.length + " characters from Cordelia Vault!");
'''
    
    def _create_roll20_readme(self) -> str:
        """Create Roll20 installation instructions"""
        return '''# Cordelia Vault - Roll20 Export

This package contains exported content from the Cordelia TTRPG Vault for use in Roll20.

## Installation Instructions

1. **Manual Import (Recommended for small datasets)**:
   - Open your Roll20 campaign
   - Go to Journal tab
   - Use the handouts.json and characters.json files to manually create content

2. **API Script Import (For Pro subscribers)**:
   - Copy the content of `import_script.js`
   - Paste it into the API Scripts section of your Roll20 campaign
   - Save and run the script

## Files Included

- `handouts.json` - Journal entries and lore content
- `characters.json` - NPCs and creatures
- `import_script.js` - Automated import script for Roll20 API
- `README.md` - This file

## Support

This export was generated by the Cordelia Vault VTT Integration system.
For issues or questions, please refer to your vault documentation.

## Legal

Content exported from Cordelia Vault. Please respect any applicable licensing terms.
'''
    
    def _create_foundry_readme(self) -> str:
        """Create Foundry installation instructions"""
        return '''# Cordelia Vault - Foundry VTT Module

This module contains exported content from the Cordelia TTRPG Vault.

## Installation Instructions

1. **Manual Installation**:
   - Extract this zip file to your Foundry `Data/modules/` directory
   - Restart Foundry VTT
   - Enable the "Cordelia Export" module in your world

2. **Package Installation**:
   - In Foundry, go to Add-on Modules
   - Click "Install Module"  
   - Use the module.json manifest file

## Content Included

The module includes compendium packs with:
- **Actors**: NPCs and creatures from the vault
- **Items**: Magical items, weapons, and artifacts  
- **Journal Entries**: Lore, locations, and handout content

## Usage

After enabling the module:
1. Open the Compendium tab
2. Browse the Cordelia export packs
3. Drag and drop content into your world

## Technical Notes

- Compatible with D&D 5e system
- Requires Foundry VTT version 10.291 or higher
- All content is flagged with source file information

## Support

This module was generated by the Cordelia Vault VTT Integration system.
For issues or questions, please refer to your vault documentation.
'''
    
    def get_job_status(self, job_id: str) -> Optional[VTTExportJob]:
        """Get export job status"""
        return self.jobs.get(job_id)
    
    def list_jobs(self) -> List[Dict]:
        """List all export jobs with summary info"""
        return [
            {
                "job_id": job.job_id,
                "platform": job.platform,
                "status": job.status,
                "created_at": job.created_at,
                "content_count": len(job.content_paths),
                "export_path": job.export_path,
                "error_message": job.error_message
            }
            for job in self.jobs.values()
        ]
    
    def discover_exportable_content(self) -> Dict[str, List[str]]:
        """Discover content suitable for VTT export"""
        exportable = {
            'npcs': [],
            'items': [],
            'locations': [],
            'handouts': [],
            'adventures': []
        }
        
        # Scan vault for exportable content
        for file_path in self.vault_path.rglob('*.md'):
            if file_path.name.startswith('.'):
                continue
            
            relative_path = str(file_path.relative_to(self.vault_path))
            path_lower = relative_path.lower()
            
            # Categorize based on path patterns
            if 'groups' in path_lower or 'people' in path_lower:
                exportable['npcs'].append(relative_path)
            elif 'items' in path_lower:
                exportable['items'].append(relative_path)
            elif 'locations' in path_lower or 'places' in path_lower:
                exportable['locations'].append(relative_path)
            elif 'adventures' in path_lower or 'campaigns' in path_lower:
                exportable['adventures'].append(relative_path)
            elif any(folder in path_lower for folder in ['lore', 'worldbuilding']):
                exportable['handouts'].append(relative_path)
        
        # Sort and limit results
        for category in exportable:
            exportable[category] = sorted(exportable[category])[:100]  # Limit for performance
        
        return exportable


def main():
    """Command line interface for VTT integration"""
    parser = argparse.ArgumentParser(description="Virtual Table Integration System")
    parser.add_argument("--vault", default=".", help="Vault directory path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Discover content command
    discover = subparsers.add_parser("discover", help="Discover exportable content")
    
    # Create export command  
    create_export = subparsers.add_parser("export", help="Create export job")
    create_export.add_argument("platform", choices=["roll20", "foundry"], help="Target platform")
    create_export.add_argument("--files", nargs="+", required=True, help="Files to export")
    
    # Process job command
    process = subparsers.add_parser("process", help="Process export job")
    process.add_argument("job_id", help="Job ID to process")
    
    # Status command
    status = subparsers.add_parser("status", help="Check job status")
    status.add_argument("job_id", help="Job ID to check")
    
    # List jobs command
    subparsers.add_parser("list-jobs", help="List all export jobs")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize exporter
    exporter = VTTExporter(args.vault)
    
    if args.command == "discover":
        content = exporter.discover_exportable_content()
        print("🔍 Exportable Content Discovery:")
        for category, files in content.items():
            print(f"\n📁 {category.upper()} ({len(files)} files):")
            for file_path in files[:10]:  # Show first 10
                print(f"  {file_path}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")
    
    elif args.command == "export":
        job_id = exporter.create_export_job(args.platform, args.files)
        print(f"✅ Created export job: {job_id}")
        print(f"Platform: {args.platform}")
        print(f"Files: {len(args.files)}")
        print(f"\nTo process the job, run:")
        print(f"python3 scripts/vtt_integration.py process {job_id}")
    
    elif args.command == "process":
        success = exporter.process_export_job(args.job_id)
        if success:
            job = exporter.get_job_status(args.job_id)
            print(f"✅ Export job {args.job_id} completed successfully!")
            print(f"Export file: {job.export_path}")
        else:
            job = exporter.get_job_status(args.job_id)
            if job and job.error_message:
                print(f"❌ Export job {args.job_id} failed: {job.error_message}")
            else:
                print(f"❌ Export job {args.job_id} not found or failed")
    
    elif args.command == "status":
        job = exporter.get_job_status(args.job_id)
        if job:
            print(f"📋 Job Status: {args.job_id}")
            print(f"  Platform: {job.platform}")
            print(f"  Status: {job.status}")
            print(f"  Created: {job.created_at}")
            print(f"  Content Files: {len(job.content_paths)}")
            if job.export_path:
                print(f"  Export Path: {job.export_path}")
            if job.error_message:
                print(f"  Error: {job.error_message}")
        else:
            print(f"❌ Job {args.job_id} not found")
    
    elif args.command == "list-jobs":
        jobs = exporter.list_jobs()
        if jobs:
            print("📋 Export Jobs:")
            for job in jobs:
                status_icon = {"pending": "⏳", "processing": "🔄", "completed": "✅", "failed": "❌"}
                icon = status_icon.get(job["status"], "❓")
                print(f"  {icon} {job['job_id']} - {job['platform']} ({job['content_count']} files)")
                print(f"      Created: {job['created_at'][:19].replace('T', ' ')}")
                if job['error_message']:
                    print(f"      Error: {job['error_message']}")
        else:
            print("No export jobs found.")


if __name__ == "__main__":
    main()