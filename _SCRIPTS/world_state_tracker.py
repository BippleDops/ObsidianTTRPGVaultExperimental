#!/usr/bin/env python3
"""
World State Tracker
Tracks world state changes across campaigns using Pydantic models.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Set
from collections import defaultdict, Counter

# Import our Pydantic models  
import sys
sys.path.append('../data')
from models import BaseVaultContent, Location, Faction, WorldRealm, ContentStatus

class WorldStateChange:
    """Represents a change in world state."""
    def __init__(self, change_type: str, entity: str, description: str, 
                 session: Optional[str] = None, timestamp: Optional[datetime] = None):
        self.change_type = change_type  # "location", "faction", "character", "political"
        self.entity = entity
        self.description = description
        self.session = session
        self.timestamp = timestamp or datetime.now()

class WorldStateTracker:
    """Tracks world state changes across campaigns."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.world_changes: List[WorldStateChange] = []
        self.current_state: Dict[str, Dict[str, Any]] = {
            "locations": {},
            "factions": {},
            "political": {},
            "economic": {},
            "environmental": {}
        }
        self.timeline: List[Dict[str, Any]] = []
        
    def extract_world_changes_from_session(self, file_path: Path) -> List[WorldStateChange]:
        """Extract world state changes from a session file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return []
            
        changes = []
        session_name = file_path.stem
        
        # Look for world changes section
        change_patterns = [
            r'world\s+changes?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'consequences?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'aftermath:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'world\s+state:?\s*((?:[-*]\s*[^\n]+\n?)+)'
        ]
        
        for pattern in change_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                change_text = match.group(1)
                change_items = re.findall(r'[-*]\s*([^\n]+)', change_text)
                
                for item in change_items:
                    change_type = self.classify_change_type(item)
                    entity = self.extract_entity_from_change(item)
                    
                    changes.append(WorldStateChange(
                        change_type=change_type,
                        entity=entity,
                        description=item.strip(),
                        session=session_name
                    ))
                break
                
        # Look for specific change indicators in content
        location_changes = self.extract_location_changes(content, session_name)
        faction_changes = self.extract_faction_changes(content, session_name)
        political_changes = self.extract_political_changes(content, session_name)
        
        changes.extend(location_changes)
        changes.extend(faction_changes)
        changes.extend(political_changes)
        
        return changes
        
    def classify_change_type(self, change_description: str) -> str:
        """Classify the type of world change."""
        desc_lower = change_description.lower()
        
        if any(word in desc_lower for word in ['destroyed', 'built', 'renovated', 'abandoned', 'occupied']):
            return "location"
        elif any(word in desc_lower for word in ['alliance', 'war', 'treaty', 'faction', 'guild', 'disbanded']):
            return "faction"
        elif any(word in desc_lower for word in ['elected', 'crowned', 'overthrown', 'government', 'parliament']):
            return "political"
        elif any(word in desc_lower for word in ['trade', 'economy', 'market', 'prices', 'shortage']):
            return "economic"
        elif any(word in desc_lower for word in ['weather', 'disaster', 'environmental', 'climate']):
            return "environmental"
        else:
            return "general"
            
    def extract_entity_from_change(self, change_description: str) -> str:
        """Extract the main entity affected by the change."""
        # Look for wikilinks first
        wikilink_match = re.search(r'\[\[([^]]+)\]\]', change_description)
        if wikilink_match:
            return wikilink_match.group(1).split('|')[0].split('#')[0].strip()
            
        # Look for proper nouns (capitalized words)
        words = change_description.split()
        proper_nouns = [word for word in words if word[0].isupper() and len(word) > 2]
        
        if proper_nouns:
            # Try to find the most significant proper noun
            for noun in proper_nouns:
                if noun.lower() not in ['the', 'and', 'or', 'but', 'session']:
                    return noun
                    
        return "Unknown"
        
    def extract_location_changes(self, content: str, session: str) -> List[WorldStateChange]:
        """Extract location-specific changes from content."""
        changes = []
        
        # Look for location destruction/creation patterns
        location_patterns = [
            r'([A-Z][a-zA-Z\s]+)\s+was\s+(destroyed|damaged|rebuilt|abandoned)',
            r'(destroyed|built|renovated)\s+([A-Z][a-zA-Z\s]+)',
            r'([A-Z][a-zA-Z\s]+)\s+is\s+now\s+(occupied|empty|sealed|open)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    if match[0].lower() in ['destroyed', 'built', 'renovated']:
                        location = match[1]
                        action = match[0]
                    else:
                        location = match[0]
                        action = match[1]
                        
                    changes.append(WorldStateChange(
                        change_type="location",
                        entity=location.strip(),
                        description=f"{location} was {action}",
                        session=session
                    ))
                    
        return changes
        
    def extract_faction_changes(self, content: str, session: str) -> List[WorldStateChange]:
        """Extract faction-specific changes from content."""
        changes = []
        
        faction_patterns = [
            r'([A-Z][a-zA-Z\s]+)\s+(?:declared\s+war\s+on|allied\s+with|disbanded|formed\s+alliance)\s+([A-Z][a-zA-Z\s]+)',
            r'(alliance|war|treaty|truce)\s+between\s+([A-Z][a-zA-Z\s]+)\s+and\s+([A-Z][a-zA-Z\s]+)',
            r'([A-Z][a-zA-Z\s]+)\s+was\s+(disbanded|reformed|merged\s+with)'
        ]
        
        for pattern in faction_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    entity = match[0] if match[0][0].isupper() else match[1]
                    description = ' '.join(match)
                    
                    changes.append(WorldStateChange(
                        change_type="faction",
                        entity=entity.strip(),
                        description=description,
                        session=session
                    ))
                    
        return changes
        
    def extract_political_changes(self, content: str, session: str) -> List[WorldStateChange]:
        """Extract political changes from content."""
        changes = []
        
        political_patterns = [
            r'([A-Z][a-zA-Z\s]+)\s+was\s+(elected|crowned|overthrown|assassinated)',
            r'(new\s+law|decree|edict|proclamation)\s+([^.\n]+)',
            r'(parliament|government|council)\s+([^.\n]+)'
        ]
        
        for pattern in political_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                entity = match[0].strip()
                description = ' '.join(match)
                
                changes.append(WorldStateChange(
                    change_type="political",
                    entity=entity,
                    description=description,
                    session=session
                ))
                
        return changes
        
    def load_current_world_state(self) -> None:
        """Load current world state from location and faction files."""
        # Load locations
        location_dirs = [
            self.vault_path / "02_Worldbuilding" / "Places",
            self.vault_path / "02_Worldbuilding" / "Locations"
        ]
        
        for loc_dir in location_dirs:
            if loc_dir.exists():
                for file_path in loc_dir.rglob("*.md"):
                    location_data = self.extract_location_state(file_path)
                    if location_data:
                        self.current_state["locations"][location_data["name"]] = location_data
                        
        # Load factions
        faction_dir = self.vault_path / "02_Worldbuilding" / "Groups"
        if faction_dir.exists():
            for file_path in faction_dir.rglob("*.md"):
                faction_data = self.extract_faction_state(file_path)
                if faction_data:
                    self.current_state["factions"][faction_data["name"]] = faction_data
                    
    def extract_location_state(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract current state of a location."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return None
            
        name = file_path.stem
        
        # Extract key state information
        state = {
            "name": name,
            "status": self.extract_location_status(content),
            "population": self.extract_population(content),
            "ruler": self.extract_ruler(content),
            "threats": self.extract_threats(content),
            "resources": self.extract_resources(content),
            "last_updated": datetime.now()
        }
        
        return state
        
    def extract_location_status(self, content: str) -> str:
        """Extract location status from content."""
        status_patterns = [
            r'status:?\s*([^.\n]+)',
            r'condition:?\s*([^.\n]+)',
            r'state:?\s*([^.\n]+)'
        ]
        
        for pattern in status_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
                
        # Look for status indicators
        if 'destroyed' in content.lower() or 'ruins' in content.lower():
            return "destroyed"
        elif 'abandoned' in content.lower():
            return "abandoned"
        elif 'thriving' in content.lower() or 'prosperous' in content.lower():
            return "thriving"
        else:
            return "stable"
            
    def extract_population(self, content: str) -> Optional[int]:
        """Extract population from content."""
        pop_patterns = [
            r'population:?\s*(\d+)',
            r'(\d+)\s+(?:people|residents|inhabitants|citizens)'
        ]
        
        for pattern in pop_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return int(match.group(1))
                
        return None
        
    def extract_ruler(self, content: str) -> Optional[str]:
        """Extract ruler/leader from content."""
        ruler_patterns = [
            r'ruled?\s+by:?\s*(?:\[\[)?([^.\n\]]+)',
            r'leader:?\s*(?:\[\[)?([^.\n\]]+)',
            r'governor:?\s*(?:\[\[)?([^.\n\]]+)',
            r'mayor:?\s*(?:\[\[)?([^.\n\]]+)'
        ]
        
        for pattern in ruler_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
                
        return None
        
    def extract_threats(self, content: str) -> List[str]:
        """Extract current threats from content."""
        threats = []
        
        threat_patterns = [
            r'threats?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'dangers?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'problems?:?\s*((?:[-*]\s*[^\n]+\n?)+)'
        ]
        
        for pattern in threat_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                threat_text = match.group(1)
                threat_items = re.findall(r'[-*]\s*([^\n]+)', threat_text)
                threats.extend([item.strip() for item in threat_items])
                break
                
        return threats
        
    def extract_resources(self, content: str) -> List[str]:
        """Extract resources from content."""
        resources = []
        
        resource_patterns = [
            r'resources?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'exports?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'produces?:?\s*((?:[-*]\s*[^\n]+\n?)+)'
        ]
        
        for pattern in resource_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                resource_text = match.group(1)
                resource_items = re.findall(r'[-*]\s*([^\n]+)', resource_text)
                resources.extend([item.strip() for item in resource_items])
                break
                
        return resources
        
    def extract_faction_state(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract current state of a faction."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return None
            
        name = file_path.stem
        
        state = {
            "name": name,
            "status": self.extract_faction_status(content),
            "leadership": self.extract_faction_leadership(content),
            "size": self.extract_faction_size(content),
            "goals": self.extract_faction_goals(content),
            "allies": self.extract_faction_allies(content),
            "enemies": self.extract_faction_enemies(content),
            "last_updated": datetime.now()
        }
        
        return state
        
    def extract_faction_status(self, content: str) -> str:
        """Extract faction status."""
        if 'disbanded' in content.lower() or 'dissolved' in content.lower():
            return "disbanded"
        elif 'growing' in content.lower() or 'expanding' in content.lower():
            return "growing"
        elif 'declining' in content.lower() or 'weakening' in content.lower():
            return "declining"
        else:
            return "active"
            
    def extract_faction_leadership(self, content: str) -> List[str]:
        """Extract faction leadership."""
        leadership = []
        
        leader_patterns = [
            r'leader(?:ship)?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'led\s+by:?\s*([^.\n]+)',
            r'head:?\s*([^.\n]+)'
        ]
        
        for pattern in leader_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                if '[-*]' in match.group(1):
                    leader_items = re.findall(r'[-*]\s*([^\n]+)', match.group(1))
                    leadership.extend([item.strip() for item in leader_items])
                else:
                    leadership.append(match.group(1).strip())
                break
                
        return leadership
        
    def extract_faction_size(self, content: str) -> Optional[str]:
        """Extract faction size indicator."""
        size_patterns = [
            r'size:?\s*([^.\n]+)',
            r'members?:?\s*(\d+)',
            r'(\d+)\s+members?'
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
                
        # Look for size indicators
        if 'large' in content.lower() or 'massive' in content.lower():
            return "large"
        elif 'small' in content.lower() or 'minor' in content.lower():
            return "small"
        elif 'medium' in content.lower() or 'moderate' in content.lower():
            return "medium"
            
        return None
        
    def extract_faction_goals(self, content: str) -> List[str]:
        """Extract faction goals."""
        goals = []
        
        goal_patterns = [
            r'goals?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'objectives?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'aims?:?\s*((?:[-*]\s*[^\n]+\n?)+)'
        ]
        
        for pattern in goal_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                goal_text = match.group(1)
                goal_items = re.findall(r'[-*]\s*([^\n]+)', goal_text)
                goals.extend([item.strip() for item in goal_items])
                break
                
        return goals
        
    def extract_faction_allies(self, content: str) -> List[str]:
        """Extract faction allies."""
        allies = []
        
        ally_patterns = [
            r'allies?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'allied\s+with:?\s*([^.\n]+)',
            r'friends?:?\s*([^.\n]+)'
        ]
        
        for pattern in ally_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                if '[-*]' in match.group(1):
                    ally_items = re.findall(r'[-*]\s*([^\n]+)', match.group(1))
                    allies.extend([item.strip() for item in ally_items])
                else:
                    allies.append(match.group(1).strip())
                break
                
        return allies
        
    def extract_faction_enemies(self, content: str) -> List[str]:
        """Extract faction enemies."""
        enemies = []
        
        enemy_patterns = [
            r'enemies?:?\s*((?:[-*]\s*[^\n]+\n?)+)',
            r'opposed\s+to:?\s*([^.\n]+)',
            r'conflicts?\s+with:?\s*([^.\n]+)'
        ]
        
        for pattern in enemy_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                if '[-*]' in match.group(1):
                    enemy_items = re.findall(r'[-*]\s*([^\n]+)', match.group(1))
                    enemies.extend([item.strip() for item in enemy_items])
                else:
                    enemies.append(match.group(1).strip())
                break
                
        return enemies
        
    def track_world_changes(self) -> None:
        """Track all world state changes from session files."""
        session_dirs = [
            self.vault_path / "01_Adventures",
            self.vault_path / "1-Session Journals"
        ]
        
        session_files = []
        for sess_dir in session_dirs:
            if sess_dir.exists():
                session_files.extend(sess_dir.rglob("*.md"))
                
        # Sort by session number if possible
        def session_sort_key(file_path):
            name = file_path.name.lower()
            session_match = re.search(r'session[_\s]*(\d+)', name)
            return int(session_match.group(1)) if session_match else 999
            
        session_files.sort(key=session_sort_key)
        
        for file_path in session_files:
            if 'session' in file_path.name.lower():
                changes = self.extract_world_changes_from_session(file_path)
                self.world_changes.extend(changes)
                
    def build_timeline(self) -> None:
        """Build chronological timeline of world changes."""
        # Sort changes by session
        session_order = {}
        session_counter = 0
        
        for change in self.world_changes:
            if change.session and change.session not in session_order:
                session_order[change.session] = session_counter
                session_counter += 1
                
        # Group changes by session
        session_changes = defaultdict(list)
        for change in self.world_changes:
            session_changes[change.session or "Unknown"].append(change)
            
        # Build timeline
        for session_name in sorted(session_changes.keys(), 
                                 key=lambda x: session_order.get(x, 999)):
            changes = session_changes[session_name]
            
            self.timeline.append({
                "session": session_name,
                "timestamp": changes[0].timestamp.isoformat() if changes else datetime.now().isoformat(),
                "changes": [
                    {
                        "type": c.change_type,
                        "entity": c.entity,
                        "description": c.description
                    }
                    for c in changes
                ]
            })
            
    def generate_world_state_report(self) -> Dict[str, Any]:
        """Generate comprehensive world state report."""
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_changes": len(self.world_changes),
                "change_types": dict(Counter([c.change_type for c in self.world_changes])),
                "active_locations": len([loc for loc, data in self.current_state["locations"].items() 
                                       if data.get("status") != "destroyed"]),
                "active_factions": len([fact for fact, data in self.current_state["factions"].items() 
                                      if data.get("status") != "disbanded"])
            },
            "current_state": self.current_state,
            "timeline": self.timeline,
            "recent_changes": [
                {
                    "type": c.change_type,
                    "entity": c.entity,
                    "description": c.description,
                    "session": c.session
                }
                for c in sorted(self.world_changes, key=lambda x: x.timestamp, reverse=True)[:20]
            ],
            "impact_analysis": self.analyze_change_impacts()
        }
        
    def analyze_change_impacts(self) -> Dict[str, Any]:
        """Analyze the impacts of world changes."""
        # Count changes by entity
        entity_changes = Counter([c.entity for c in self.world_changes])
        
        # Analyze change frequency by type
        type_frequency = Counter([c.change_type for c in self.world_changes])
        
        # Find most impacted entities
        most_impacted = entity_changes.most_common(10)
        
        return {
            "most_impacted_entities": most_impacted,
            "change_frequency_by_type": dict(type_frequency),
            "total_entities_affected": len(entity_changes),
            "average_changes_per_entity": sum(entity_changes.values()) / len(entity_changes) if entity_changes else 0
        }
        
    def export_results(self, report: Dict[str, Any], output_path: str) -> None:
        """Export world state report."""
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        print(f"World state report exported to: {output_path}")
        
def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Track world state changes in Cordelia vault")
    parser.add_argument("vault_path", help="Path to vault directory")
    parser.add_argument("--output", "-o", help="Output path for world state report", 
                       default="world_state_report.json")
    
    args = parser.parse_args()
    
    tracker = WorldStateTracker(args.vault_path)
    
    print("Loading current world state...")
    tracker.load_current_world_state()
    
    print("Tracking world changes...")
    tracker.track_world_changes()
    
    print("Building timeline...")
    tracker.build_timeline()
    
    report = tracker.generate_world_state_report()
    
    print(f"\nWorld State Report:")
    print(f"Total changes tracked: {report['summary']['total_changes']}")
    print(f"Active locations: {report['summary']['active_locations']}")
    print(f"Active factions: {report['summary']['active_factions']}")
    print(f"Timeline events: {len(report['timeline'])}")
    
    tracker.export_results(report, args.output)
    
if __name__ == "__main__":
    main()