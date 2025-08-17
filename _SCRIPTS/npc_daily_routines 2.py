#!/usr/bin/env python3
"""
NPC Daily Routines System
Sprint 4 - Procedural Power Feature #2

Automated schedules and location tracking for NPCs to create a living world.
Generates realistic daily routines based on NPC roles, relationships, and world events.

Features:
- Dynamic schedule generation
- Location-based activity tracking
- Event-responsive routine changes
- Social interaction modeling
- Time-of-day activity patterns
"""

import os
import json
import random
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from pydantic import BaseModel, Field, validator

from common import (
    list_markdown_files, read_file, write_file, split_frontmatter,
    build_frontmatter, merge_frontmatter, ROOT_DIR, ensure_dirs
)

class ActivityType(Enum):
    WORK = "work"
    SOCIAL = "social"
    PERSONAL = "personal"
    TRAVEL = "travel"
    REST = "rest"
    SECRET = "secret"
    EMERGENCY = "emergency"

class LocationCategory(Enum):
    HOME = "home"
    WORKPLACE = "workplace"
    SOCIAL_VENUE = "social_venue"
    GOVERNMENT = "government"
    MARKET = "market"
    TRANSPORT = "transport"
    HIDDEN = "hidden"

class TimeOfDay(Enum):
    EARLY_MORNING = "early_morning"  # 5-8 AM
    MORNING = "morning"              # 8-12 PM
    MIDDAY = "midday"               # 12-2 PM
    AFTERNOON = "afternoon"          # 2-6 PM
    EVENING = "evening"             # 6-9 PM
    NIGHT = "night"                 # 9 PM-12 AM
    LATE_NIGHT = "late_night"       # 12-5 AM

class ActivityBlock(BaseModel):
    """A scheduled activity block for an NPC"""
    activity_id: str = Field(..., description="Unique identifier for activity")
    start_time: str = Field(..., description="Start time in HH:MM format")
    end_time: str = Field(..., description="End time in HH:MM format")
    activity_type: ActivityType
    location: str = Field(..., description="Primary location for activity")
    description: str = Field(..., description="What the NPC is doing")
    associated_npcs: List[str] = Field(default_factory=list, description="Other NPCs involved")
    required_items: List[str] = Field(default_factory=list, description="Items needed for activity")
    secrecy_level: int = Field(default=1, description="1=Public, 5=Extremely Secret")
    mood_modifier: str = Field(default="neutral", description="How this affects NPC's mood")
    interruption_difficulty: int = Field(default=3, description="How hard to interrupt (1-10)")
    
    @validator('start_time', 'end_time')
    def validate_time_format(cls, v):
        try:
            datetime.strptime(v, "%H:%M")
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format")

class NPCRoutine(BaseModel):
    """Complete daily routine for an NPC"""
    npc_name: str = Field(..., description="Name of the NPC")
    world: str = Field(..., description="Aquabyssos, Aethermoor, or Both")
    base_schedule: List[ActivityBlock] = Field(..., description="Standard daily schedule")
    variant_schedules: Dict[str, List[ActivityBlock]] = Field(default_factory=dict, description="Alternative schedules for special days")
    weekly_variations: Dict[str, List[str]] = Field(default_factory=dict, description="Day-of-week specific activities")
    seasonal_adjustments: Dict[str, Dict] = Field(default_factory=dict, description="Seasonal routine changes")
    event_responses: Dict[str, Dict] = Field(default_factory=dict, description="How routine changes during events")
    social_priorities: List[str] = Field(default_factory=list, description="NPCs this character prioritizes seeing")
    location_familiarity: Dict[str, int] = Field(default_factory=dict, description="How well NPC knows locations (1-10)")
    
class LocationData(BaseModel):
    """Information about a location used in routines"""
    name: str
    category: LocationCategory
    capacity: int = Field(default=10, description="How many NPCs can be here simultaneously")
    operating_hours: Tuple[str, str] = Field(default=("06:00", "22:00"), description="When location is accessible")
    associated_activities: List[ActivityType] = Field(default_factory=list)
    security_level: int = Field(default=1, description="How secure/restricted (1-10)")
    current_occupants: List[str] = Field(default_factory=list, description="NPCs currently at location")

class RoutineEvent(BaseModel):
    """An event that can disrupt or modify routines"""
    event_id: str
    name: str
    description: str
    duration_days: int
    affected_locations: List[str] = Field(default_factory=list)
    routine_modifications: Dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=5, description="Event priority (1-10)")

class NPCDailyRoutineSystem:
    """Main system for managing NPC daily routines"""
    
    def __init__(self, vault_root: str = ROOT_DIR):
        self.vault_root = vault_root
        self.npcs: Dict[str, Dict] = {}  # NPC data from vault
        self.routines: Dict[str, NPCRoutine] = {}  # Generated routines
        self.locations: Dict[str, LocationData] = {}  # Location database
        self.current_events: List[RoutineEvent] = []  # Active events
        self.time_blocks = self._create_time_blocks()
        
        # Load existing data
        self._scan_vault_npcs()
        self._scan_vault_locations()
        self._load_persisted_routines()
    
    def _create_time_blocks(self) -> Dict[TimeOfDay, Tuple[str, str]]:
        """Define standard time blocks for routine generation"""
        return {
            TimeOfDay.EARLY_MORNING: ("05:00", "08:00"),
            TimeOfDay.MORNING: ("08:00", "12:00"),
            TimeOfDay.MIDDAY: ("12:00", "14:00"),
            TimeOfDay.AFTERNOON: ("14:00", "18:00"),
            TimeOfDay.EVENING: ("18:00", "21:00"),
            TimeOfDay.NIGHT: ("21:00", "24:00"),
            TimeOfDay.LATE_NIGHT: ("00:00", "05:00")
        }
    
    def _scan_vault_npcs(self):
        """Scan vault for NPCs to generate routines for"""
        markdown_files = list_markdown_files(self.vault_root)
        
        for file_path in markdown_files:
            try:
                content = read_file(file_path)
                frontmatter, body = split_frontmatter(content)
                
                if frontmatter.get('type') == 'NPC':
                    npc_name = frontmatter.get('name') or os.path.splitext(os.path.basename(file_path))[0]
                    
                    # Extract NPC data for routine generation
                    npc_data = {
                        'name': npc_name,
                        'world': frontmatter.get('world', 'Both'),
                        'occupation': self._extract_occupation(body),
                        'location': self._extract_primary_location(body),
                        'personality': self._extract_personality_traits(body),
                        'relationships': self._extract_relationships(body),
                        'secrets': self._extract_secrets(body),
                        'power_level': self._infer_power_level(npc_name, body),
                        'file_path': file_path
                    }
                    
                    self.npcs[npc_name] = npc_data
                    
            except Exception as e:
                continue  # Skip malformed files
    
    def _scan_vault_locations(self):
        """Scan vault for locations to use in routines"""
        markdown_files = list_markdown_files(self.vault_root)
        
        for file_path in markdown_files:
            try:
                content = read_file(file_path)
                frontmatter, body = split_frontmatter(content)
                
                if frontmatter.get('type') == 'Location':
                    location_name = frontmatter.get('name') or os.path.splitext(os.path.basename(file_path))[0]
                    
                    location_data = LocationData(
                        name=location_name,
                        category=self._categorize_location(location_name, body),
                        capacity=self._infer_capacity(body),
                        operating_hours=self._extract_operating_hours(body),
                        associated_activities=self._extract_location_activities(body),
                        security_level=self._infer_security_level(body)
                    )
                    
                    self.locations[location_name] = location_data
                    
            except Exception as e:
                continue  # Skip malformed files
    
    def _extract_occupation(self, body: str) -> str:
        """Extract NPC's occupation from description"""
        occupation_keywords = {
            'merchant': ['trade', 'goods', 'market', 'sell', 'buy'],
            'politician': ['parliament', 'senator', 'chancellor', 'vote'],
            'military': ['admiral', 'captain', 'guard', 'soldier', 'navy'],
            'scholar': ['research', 'study', 'academy', 'library', 'knowledge'],
            'criminal': ['shadow', 'thief', 'smuggler', 'conspiracy'],
            'noble': ['lord', 'lady', 'duke', 'duchess', 'court'],
            'artisan': ['craft', 'forge', 'create', 'workshop', 'guild'],
            'priest': ['temple', 'worship', 'divine', 'prayer', 'faith']
        }
        
        body_lower = body.lower()
        for occupation, keywords in occupation_keywords.items():
            if any(keyword in body_lower for keyword in keywords):
                return occupation
                
        return 'citizen'
    
    def _extract_primary_location(self, body: str) -> str:
        """Extract NPC's primary location/residence"""
        lines = body.split('\n')
        for line in lines:
            line_lower = line.lower()
            if 'lives in' in line_lower or 'resides at' in line_lower:
                # Extract location name (simplified)
                parts = line_lower.split('lives in' if 'lives in' in line_lower else 'resides at')
                if len(parts) > 1:
                    return parts[1].strip().split()[0].title()
                    
        # Default based on world
        return "Unknown District"
    
    def _extract_personality_traits(self, body: str) -> List[str]:
        """Extract personality traits that affect routine"""
        trait_indicators = {
            'introverted': ['quiet', 'shy', 'withdrawn', 'private'],
            'extroverted': ['social', 'outgoing', 'charismatic', 'public'],
            'suspicious': ['paranoid', 'cautious', 'distrustful', 'wary'],
            'ambitious': ['power', 'climb', 'advancement', 'success'],
            'lazy': ['avoid', 'reluctant', 'unmotivated', 'procrastinate'],
            'workaholic': ['dedicated', 'obsessed', 'tireless', 'committed']
        }
        
        traits = []
        body_lower = body.lower()
        for trait, keywords in trait_indicators.items():
            if any(keyword in body_lower for keyword in keywords):
                traits.append(trait)
                
        return traits[:3]  # Limit to 3 main traits
    
    def _extract_relationships(self, body: str) -> List[str]:
        """Extract important relationships that affect routine"""
        relationships = []
        
        # Look for wiki links to other NPCs
        import re
        wiki_pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(wiki_pattern, body)
        
        for match in matches:
            # Filter for likely NPC names (simplified)
            if any(title in match.lower() for title in ['lord', 'lady', 'admiral', 'senator']):
                relationships.append(match)
                
        return relationships[:5]  # Limit relationships
    
    def _extract_secrets(self, body: str) -> List[str]:
        """Extract secrets that create secret activities"""
        secrets = []
        secret_indicators = ['secret', 'hidden', 'covert', 'private meeting', 'conspiracy']
        
        lines = body.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in secret_indicators):
                secrets.append(line.strip())
                
        return secrets[:3]
    
    def generate_routine_for_npc(self, npc_name: str) -> NPCRoutine:
        """Generate a complete daily routine for an NPC"""
        if npc_name not in self.npcs:
            return None
            
        npc_data = self.npcs[npc_name]
        occupation = npc_data['occupation']
        
        # Generate base schedule
        base_schedule = self._create_base_schedule(npc_data)
        
        # Generate variants
        variant_schedules = {}
        if npc_data['power_level'] >= 3:  # High-power NPCs have meeting days
            variant_schedules['meeting_day'] = self._create_meeting_day_schedule(npc_data)
        
        if npc_data['secrets']:  # NPCs with secrets have covert days
            variant_schedules['covert_day'] = self._create_covert_day_schedule(npc_data)
        
        # Generate weekly variations
        weekly_variations = self._create_weekly_variations(npc_data)
        
        # Create routine object
        routine = NPCRoutine(
            npc_name=npc_name,
            world=npc_data['world'],
            base_schedule=base_schedule,
            variant_schedules=variant_schedules,
            weekly_variations=weekly_variations,
            social_priorities=npc_data['relationships'][:3],
            location_familiarity=self._generate_location_familiarity(npc_data)
        )
        
        self.routines[npc_name] = routine
        return routine
    
    def _create_base_schedule(self, npc_data: Dict) -> List[ActivityBlock]:
        """Create the standard daily schedule for an NPC"""
        schedule = []
        occupation = npc_data['occupation']
        
        # Early Morning (5-8 AM)
        early_activity = self._create_early_morning_activity(npc_data)
        if early_activity:
            schedule.append(early_activity)
        
        # Morning Work Block (8 AM-12 PM) 
        morning_work = self._create_work_activity(npc_data, "08:00", "12:00")
        schedule.append(morning_work)
        
        # Midday Break (12-2 PM)
        midday_activity = ActivityBlock(
            activity_id=f"{npc_data['name']}_midday",
            start_time="12:00",
            end_time="14:00",
            activity_type=ActivityType.PERSONAL,
            location=self._select_meal_location(npc_data),
            description="Midday meal and brief rest",
            mood_modifier="content",
            interruption_difficulty=2
        )
        schedule.append(midday_activity)
        
        # Afternoon Work (2-6 PM)
        afternoon_work = self._create_work_activity(npc_data, "14:00", "18:00")
        schedule.append(afternoon_work)
        
        # Evening Social/Personal (6-9 PM)
        evening_activity = self._create_evening_activity(npc_data)
        schedule.append(evening_activity)
        
        # Night Rest (9 PM+)
        night_activity = ActivityBlock(
            activity_id=f"{npc_data['name']}_rest",
            start_time="21:00",
            end_time="05:00",
            activity_type=ActivityType.REST,
            location=npc_data['location'],  # Home
            description="Sleep and personal time",
            mood_modifier="rested",
            interruption_difficulty=8
        )
        schedule.append(night_activity)
        
        return schedule
    
    def _create_work_activity(self, npc_data: Dict, start_time: str, end_time: str) -> ActivityBlock:
        """Create work-related activity block"""
        occupation = npc_data['occupation']
        
        work_locations = {
            'merchant': 'Market District',
            'politician': 'Parliament of Echoes',
            'military': 'Naval Command',
            'scholar': 'Academy of Depths',
            'criminal': 'Shadow Hideout',
            'noble': 'Royal Court',
            'artisan': 'Artisan Quarter',
            'priest': 'Temple Complex'
        }
        
        work_descriptions = {
            'merchant': 'Managing trade operations and negotiations',
            'politician': 'Attending sessions and committee meetings',
            'military': 'Strategic planning and troop oversight',
            'scholar': 'Research and documentation work',
            'criminal': 'Coordinating illicit operations',
            'noble': 'Court duties and social obligations',
            'artisan': 'Creating and refining craft works',
            'priest': 'Conducting services and counseling'
        }
        
        return ActivityBlock(
            activity_id=f"{npc_data['name']}_work_{start_time}",
            start_time=start_time,
            end_time=end_time,
            activity_type=ActivityType.WORK,
            location=work_locations.get(occupation, 'Workplace'),
            description=work_descriptions.get(occupation, 'Professional duties'),
            mood_modifier="focused",
            interruption_difficulty=6
        )
    
    def _create_evening_activity(self, npc_data: Dict) -> ActivityBlock:
        """Create evening social/personal activity"""
        personality = npc_data['personality']
        
        if 'introverted' in personality:
            return ActivityBlock(
                activity_id=f"{npc_data['name']}_evening_personal",
                start_time="18:00",
                end_time="21:00",
                activity_type=ActivityType.PERSONAL,
                location=npc_data['location'],
                description="Personal time, reading, and reflection",
                mood_modifier="peaceful",
                interruption_difficulty=4
            )
        else:
            return ActivityBlock(
                activity_id=f"{npc_data['name']}_evening_social",
                start_time="18:00",
                end_time="21:00",
                activity_type=ActivityType.SOCIAL,
                location="Social Venue",
                description="Social gatherings and networking",
                associated_npcs=npc_data['relationships'][:2],
                mood_modifier="sociable",
                interruption_difficulty=3
            )
    
    def _create_covert_day_schedule(self, npc_data: Dict) -> List[ActivityBlock]:
        """Create schedule for days with secret activities"""
        base_schedule = self._create_base_schedule(npc_data)
        
        # Replace afternoon work with secret meeting
        secret_meeting = ActivityBlock(
            activity_id=f"{npc_data['name']}_secret_meeting",
            start_time="15:00",
            end_time="17:00",
            activity_type=ActivityType.SECRET,
            location="Hidden Location",
            description="Confidential meeting - purpose unknown",
            secrecy_level=5,
            mood_modifier="tense",
            interruption_difficulty=10
        )
        
        # Replace the afternoon work block
        modified_schedule = []
        for activity in base_schedule:
            if activity.start_time == "14:00" and activity.activity_type == ActivityType.WORK:
                modified_schedule.append(secret_meeting)
                # Add shortened work block
                modified_schedule.append(ActivityBlock(
                    activity_id=f"{npc_data['name']}_work_short",
                    start_time="17:00",
                    end_time="18:00",
                    activity_type=ActivityType.WORK,
                    location=activity.location,
                    description="Brief return to normal duties",
                    mood_modifier="distracted",
                    interruption_difficulty=4
                ))
            else:
                modified_schedule.append(activity)
                
        return modified_schedule
    
    def get_npc_current_activity(self, npc_name: str, current_time: str) -> Optional[ActivityBlock]:
        """Get what an NPC is doing at a specific time"""
        if npc_name not in self.routines:
            return None
            
        routine = self.routines[npc_name]
        current_dt = datetime.strptime(current_time, "%H:%M").time()
        
        # Check base schedule
        for activity in routine.base_schedule:
            start_dt = datetime.strptime(activity.start_time, "%H:%M").time()
            end_dt = datetime.strptime(activity.end_time, "%H:%M").time()
            
            # Handle overnight activities
            if end_dt < start_dt:  # Crosses midnight
                if current_dt >= start_dt or current_dt <= end_dt:
                    return activity
            else:
                if start_dt <= current_dt < end_dt:
                    return activity
                    
        return None
    
    def get_location_occupants(self, location_name: str, current_time: str) -> List[str]:
        """Get all NPCs currently at a location"""
        occupants = []
        
        for npc_name in self.routines:
            activity = self.get_npc_current_activity(npc_name, current_time)
            if activity and activity.location == location_name:
                occupants.append(npc_name)
                
        return occupants
    
    def simulate_random_encounter(self, party_location: str, current_time: str) -> Dict[str, Any]:
        """Generate a random encounter based on who's at the location"""
        occupants = self.get_location_occupants(party_location, current_time)
        
        if not occupants:
            return {"type": "empty", "description": "The location is quiet and empty."}
            
        encounter_npc = random.choice(occupants)
        activity = self.get_npc_current_activity(encounter_npc, current_time)
        
        npc_data = self.npcs.get(encounter_npc, {})
        
        encounter_data = {
            "type": "npc_encounter",
            "npc": encounter_npc,
            "activity": activity.description if activity else "Unknown activity",
            "mood": activity.mood_modifier if activity else "neutral",
            "interruption_difficulty": activity.interruption_difficulty if activity else 5,
            "location": party_location,
            "time": current_time,
            "potential_interactions": self._generate_interaction_options(npc_data, activity)
        }
        
        return encounter_data
    
    def _generate_interaction_options(self, npc_data: Dict, activity: Optional[ActivityBlock]) -> List[str]:
        """Generate possible interaction options with an NPC"""
        options = ["Approach for conversation", "Observe from distance"]
        
        if activity:
            if activity.activity_type == ActivityType.WORK:
                options.extend([
                    "Request professional services",
                    "Discuss work-related matters"
                ])
            elif activity.activity_type == ActivityType.SOCIAL:
                options.extend([
                    "Join the social gathering",
                    "Request private audience"
                ])
            elif activity.activity_type == ActivityType.SECRET:
                options.extend([
                    "Attempt to eavesdrop (risky)",
                    "Follow at distance (risky)"
                ])
                
        if npc_data.get('occupation') == 'merchant':
            options.append("Browse available goods")
        elif npc_data.get('occupation') == 'politician':
            options.append("Seek political favor")
            
        return options
    
    def save_routine_data(self):
        """Persist routine data to vault"""
        ensure_dirs()
        data_dir = os.path.join(self.vault_root, "09_Performance")
        os.makedirs(data_dir, exist_ok=True)
        
        # Save routines as JSON (Pydantic models serialize well)
        routines_data = {}
        for name, routine in self.routines.items():
            routines_data[name] = routine.model_dump()
            
        with open(os.path.join(data_dir, "npc_routines.json"), "w") as f:
            json.dump(routines_data, f, indent=2, default=str)
            
        # Save locations
        locations_data = {}
        for name, location in self.locations.items():
            locations_data[name] = location.model_dump()
            
        with open(os.path.join(data_dir, "routine_locations.json"), "w") as f:
            json.dump(locations_data, f, indent=2, default=str)
    
    def create_routine_dashboard(self) -> str:
        """Create comprehensive routine dashboard"""
        dashboard = []
        
        dashboard.append("# NPC Daily Routines Dashboard")
        dashboard.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        
        dashboard.append(f"## System Overview")
        dashboard.append(f"- Total NPCs tracked: {len(self.routines)}")
        dashboard.append(f"- Total locations: {len(self.locations)}")
        dashboard.append(f"- Active events: {len(self.current_events)}")
        dashboard.append("")
        
        # Sample current activities for a few times
        sample_times = ["08:00", "12:00", "18:00", "22:00"]
        
        for time_sample in sample_times:
            dashboard.append(f"### Activities at {time_sample}")
            
            location_activities = {}
            for npc_name in list(self.routines.keys())[:10]:  # Sample first 10
                activity = self.get_npc_current_activity(npc_name, time_sample)
                if activity:
                    if activity.location not in location_activities:
                        location_activities[activity.location] = []
                    location_activities[activity.location].append(f"- {npc_name}: {activity.description}")
            
            for location, activities in location_activities.items():
                dashboard.append(f"**{location}:**")
                for activity_line in activities:
                    dashboard.append(activity_line)
                dashboard.append("")
        
        return "\n".join(dashboard)
    
    def _load_persisted_routines(self):
        """Load previously saved routine data"""
        data_dir = os.path.join(self.vault_root, "09_Performance")
        
        try:
            routines_file = os.path.join(data_dir, "npc_routines.json")
            if os.path.exists(routines_file):
                with open(routines_file) as f:
                    routines_data = json.load(f)
                    for name, data in routines_data.items():
                        # Convert back to Pydantic models
                        self.routines[name] = NPCRoutine(**data)
        except Exception as e:
            pass  # Use generated data if loading fails

def main():
    """Main execution for NPC daily routines system"""
    print("Generating NPC Daily Routines System...")
    
    system = NPCDailyRoutineSystem()
    
    # Generate routines for all discovered NPCs
    routine_count = 0
    for npc_name in list(system.npcs.keys())[:20]:  # Limit for initial implementation
        routine = system.generate_routine_for_npc(npc_name)
        if routine:
            routine_count += 1
            print(f"Generated routine for: {npc_name}")
    
    print(f"Generated {routine_count} NPC routines")
    
    # Test current activity lookups
    print("\nSample current activities:")
    test_time = "14:30"
    for npc_name in list(system.routines.keys())[:5]:
        activity = system.get_npc_current_activity(npc_name, test_time)
        if activity:
            print(f"{npc_name} at {test_time}: {activity.description} at {activity.location}")
    
    # Test location occupants
    print(f"\nLocation occupants at {test_time}:")
    sample_locations = list(system.locations.keys())[:3]
    for location in sample_locations:
        occupants = system.get_location_occupants(location, test_time)
        if occupants:
            print(f"{location}: {', '.join(occupants)}")
    
    # Save system state
    system.save_routine_data()
    
    # Create dashboard
    dashboard_content = system.create_routine_dashboard()
    
    # Write dashboard to vault
    dashboard_path = os.path.join(system.vault_root, "06_GM_Resources", "NPC_Routines_Dashboard.md")
    write_file(dashboard_path, dashboard_content)
    
    print(f"NPC Daily Routines System generated successfully!")
    print(f"Dashboard saved to: NPC_Routines_Dashboard.md")

if __name__ == "__main__":
    main()
    def _extract_npc_data(self, file_path: str) -> Dict[str, Any]:
        """Extract NPC data from markdown file"""
        try:
            from common import read_file, split_frontmatter
            content = read_file(file_path)
            frontmatter, body = split_frontmatter(content)
            
            return {
                'name': frontmatter.get('name', os.path.basename(file_path)[:-3]),
                'world': frontmatter.get('world', 'Both'),
                'occupation': frontmatter.get('occupation', 'citizen'),
                'location': frontmatter.get('location', 'Unknown'),
                'personality': frontmatter.get('personality', ['neutral']),
                'relationships': frontmatter.get('relationships', []),
                'secrets': frontmatter.get('secrets', []),
                'power_level': frontmatter.get('power_level', 1),
                'file_path': file_path
            }
        except Exception as e:
            # Return default data if file can't be read
            return {
                'name': os.path.basename(file_path)[:-3],
                'world': 'Both',
                'occupation': 'citizen',
                'location': 'Unknown',
                'personality': ['neutral'],
                'relationships': [],
                'secrets': [],
                'power_level': 1,
                'file_path': file_path
            }

