#!/usr/bin/env python3
"""
Dynamic Quest State Tracking System
Advanced quest management with state tracking and dynamic updates
Part of Phase 4: Advanced Automation & Dynamic Systems
"""

import json
import sqlite3
import yaml
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum
import re

class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ON_HOLD = "on_hold"
    ABANDONED = "abandoned"

class ObjectiveStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    OPTIONAL_SKIPPED = "optional_skipped"

@dataclass
class QuestObjective:
    objective_id: str
    title: str
    description: str
    status: ObjectiveStatus = ObjectiveStatus.PENDING
    is_optional: bool = False
    prerequisite_objectives: List[str] = field(default_factory=list)
    completion_triggers: List[str] = field(default_factory=list)
    reward_xp: int = 0
    notes: str = ""
    completed_at: Optional[str] = None

@dataclass
class QuestState:
    quest_id: str
    title: str
    description: str
    status: QuestStatus = QuestStatus.NOT_STARTED
    objectives: List[QuestObjective] = field(default_factory=list)
    start_date: Optional[str] = None
    completion_date: Optional[str] = None
    participants: List[str] = field(default_factory=list)
    quest_giver: str = ""
    location: str = ""
    level_requirement: int = 1
    estimated_duration: str = ""
    rewards: Dict[str, Any] = field(default_factory=dict)
    consequences: Dict[str, Any] = field(default_factory=dict)
    related_npcs: List[str] = field(default_factory=list)
    related_locations: List[str] = field(default_factory=list)
    related_factions: List[str] = field(default_factory=list)
    session_log: List[str] = field(default_factory=list)
    gm_notes: str = ""
    player_notes: str = ""

@dataclass
class QuestEvent:
    event_id: str
    quest_id: str
    event_type: str  # 'objective_completed', 'status_changed', 'note_added', etc.
    timestamp: str
    description: str
    affected_objective: Optional[str] = None
    session_number: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class DynamicQuestTracker:
    """Dynamic quest state tracking and management system."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.config = self.load_config()
        
        # Database setup
        self.db_path = self.vault_path / "scripts" / "quest_tracker.db"
        self.init_database()
        
        # Quest state cache
        self.quest_states = {}
        self.load_quest_states()
        
    def load_config(self) -> Dict:
        """Load quest tracking configuration."""
        config_path = self.vault_path / "scripts" / "quest_tracker_config.json"
        
        default_config = {
            "tracking_settings": {
                "auto_detect_objectives": True,
                "auto_update_from_sessions": True,
                "track_npc_interactions": True,
                "track_location_visits": True,
                "generate_progress_reports": True
            },
            "notification_settings": {
                "notify_objective_complete": True,
                "notify_quest_status_change": True,
                "notify_overdue_quests": True,
                "notify_conflicting_objectives": True
            },
            "automation": {
                "auto_create_follow_ups": True,
                "auto_link_related_content": True,
                "auto_update_faction_relations": True,
                "auto_generate_consequences": True
            },
            "display_settings": {
                "show_optional_objectives": True,
                "group_by_status": True,
                "show_completion_percentage": True,
                "highlight_overdue": True
            },
            "file_patterns": {
                "quest_files": ["01_Adventures/**/*.md", "06_GM_Resources/**/Quest*.md"],
                "session_files": ["1-Session Journals/**/*.md"],
                "npc_files": ["02_Worldbuilding/People/**/*.md"]
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in loaded_config:
                        loaded_config[key] = value
                return loaded_config
            except Exception as e:
                print(f"Error loading quest tracker config: {e}")
                
        # Write default config
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
        
    def init_database(self):
        """Initialize SQLite database for quest tracking."""
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quests (
                    quest_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    start_date TEXT,
                    completion_date TEXT,
                    participants TEXT,
                    quest_giver TEXT,
                    location TEXT,
                    level_requirement INTEGER,
                    estimated_duration TEXT,
                    rewards TEXT,
                    consequences TEXT,
                    related_npcs TEXT,
                    related_locations TEXT,
                    related_factions TEXT,
                    session_log TEXT,
                    gm_notes TEXT,
                    player_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS objectives (
                    objective_id TEXT PRIMARY KEY,
                    quest_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    is_optional BOOLEAN DEFAULT FALSE,
                    prerequisite_objectives TEXT,
                    completion_triggers TEXT,
                    reward_xp INTEGER DEFAULT 0,
                    notes TEXT,
                    completed_at TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quest_id) REFERENCES quests (quest_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quest_events (
                    event_id TEXT PRIMARY KEY,
                    quest_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    description TEXT,
                    affected_objective TEXT,
                    session_number INTEGER,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quest_id) REFERENCES quests (quest_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quest_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quest_id TEXT NOT NULL,
                    related_quest_id TEXT NOT NULL,
                    relationship_type TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quest_id) REFERENCES quests (quest_id),
                    FOREIGN KEY (related_quest_id) REFERENCES quests (quest_id)
                )
            """)
            
            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_quests_status ON quests (status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_objectives_quest ON objectives (quest_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_quest ON quest_events (quest_id)")
            
            conn.commit()
            
    def load_quest_states(self):
        """Load quest states from database."""
        with sqlite3.connect(self.db_path) as conn:
            # Load quests
            cursor = conn.execute("""
                SELECT quest_id, title, description, status, start_date, completion_date,
                       participants, quest_giver, location, level_requirement, 
                       estimated_duration, rewards, consequences, related_npcs,
                       related_locations, related_factions, session_log, gm_notes, player_notes
                FROM quests
            """)
            
            for row in cursor.fetchall():
                quest_data = dict(zip([col[0] for col in cursor.description], row))
                
                # Parse JSON fields
                for field in ['participants', 'rewards', 'consequences', 'related_npcs', 
                             'related_locations', 'related_factions', 'session_log']:
                    if quest_data[field]:
                        try:
                            quest_data[field] = json.loads(quest_data[field])
                        except:
                            quest_data[field] = []
                    else:
                        quest_data[field] = [] if field != 'rewards' and field != 'consequences' else {}
                        
                quest_data['status'] = QuestStatus(quest_data['status'])
                quest_state = QuestState(**quest_data)
                
                # Load objectives
                obj_cursor = conn.execute("""
                    SELECT objective_id, title, description, status, is_optional,
                           prerequisite_objectives, completion_triggers, reward_xp,
                           notes, completed_at
                    FROM objectives WHERE quest_id = ?
                """, (quest_state.quest_id,))
                
                for obj_row in obj_cursor.fetchall():
                    obj_data = dict(zip([col[0] for col in obj_cursor.description], obj_row))
                    
                    # Parse JSON fields
                    for field in ['prerequisite_objectives', 'completion_triggers']:
                        if obj_data[field]:
                            try:
                                obj_data[field] = json.loads(obj_data[field])
                            except:
                                obj_data[field] = []
                        else:
                            obj_data[field] = []
                            
                    obj_data['status'] = ObjectiveStatus(obj_data['status'])
                    objective = QuestObjective(**obj_data)
                    quest_state.objectives.append(objective)
                    
                self.quest_states[quest_state.quest_id] = quest_state
                
    def create_quest(self, quest_data: Dict[str, Any]) -> str:
        """Create a new quest."""
        quest_id = quest_data.get('quest_id', f"quest_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        quest_state = QuestState(
            quest_id=quest_id,
            title=quest_data['title'],
            description=quest_data.get('description', ''),
            quest_giver=quest_data.get('quest_giver', ''),
            location=quest_data.get('location', ''),
            level_requirement=quest_data.get('level_requirement', 1),
            estimated_duration=quest_data.get('estimated_duration', ''),
            related_npcs=quest_data.get('related_npcs', []),
            related_locations=quest_data.get('related_locations', []),
            related_factions=quest_data.get('related_factions', []),
            gm_notes=quest_data.get('gm_notes', '')
        )
        
        # Add objectives if provided
        for obj_data in quest_data.get('objectives', []):
            objective = QuestObjective(
                objective_id=f"{quest_id}_obj_{len(quest_state.objectives)+1}",
                title=obj_data['title'],
                description=obj_data.get('description', ''),
                is_optional=obj_data.get('is_optional', False),
                prerequisite_objectives=obj_data.get('prerequisite_objectives', []),
                reward_xp=obj_data.get('reward_xp', 0)
            )
            quest_state.objectives.append(objective)
            
        # Save to database
        self.save_quest_state(quest_state)
        self.quest_states[quest_id] = quest_state
        
        # Log creation event
        self.log_quest_event(quest_id, "quest_created", f"Quest '{quest_state.title}' created")
        
        return quest_id
        
    def save_quest_state(self, quest_state: QuestState):
        """Save quest state to database."""
        with sqlite3.connect(self.db_path) as conn:
            # Save quest
            conn.execute("""
                INSERT OR REPLACE INTO quests 
                (quest_id, title, description, status, start_date, completion_date,
                 participants, quest_giver, location, level_requirement, estimated_duration,
                 rewards, consequences, related_npcs, related_locations, related_factions,
                 session_log, gm_notes, player_notes, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                quest_state.quest_id, quest_state.title, quest_state.description,
                quest_state.status.value, quest_state.start_date, quest_state.completion_date,
                json.dumps(quest_state.participants), quest_state.quest_giver, quest_state.location,
                quest_state.level_requirement, quest_state.estimated_duration,
                json.dumps(quest_state.rewards), json.dumps(quest_state.consequences),
                json.dumps(quest_state.related_npcs), json.dumps(quest_state.related_locations),
                json.dumps(quest_state.related_factions), json.dumps(quest_state.session_log),
                quest_state.gm_notes, quest_state.player_notes
            ))
            
            # Clear existing objectives
            conn.execute("DELETE FROM objectives WHERE quest_id = ?", (quest_state.quest_id,))
            
            # Save objectives
            for objective in quest_state.objectives:
                conn.execute("""
                    INSERT INTO objectives 
                    (objective_id, quest_id, title, description, status, is_optional,
                     prerequisite_objectives, completion_triggers, reward_xp, notes, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    objective.objective_id, quest_state.quest_id, objective.title,
                    objective.description, objective.status.value, objective.is_optional,
                    json.dumps(objective.prerequisite_objectives),
                    json.dumps(objective.completion_triggers), objective.reward_xp,
                    objective.notes, objective.completed_at
                ))
                
    def update_quest_status(self, quest_id: str, new_status: QuestStatus, notes: str = ""):
        """Update quest status."""
        if quest_id not in self.quest_states:
            print(f"Quest {quest_id} not found")
            return False
            
        quest_state = self.quest_states[quest_id]
        old_status = quest_state.status
        quest_state.status = new_status
        
        # Set dates based on status
        if new_status == QuestStatus.ACTIVE and not quest_state.start_date:
            quest_state.start_date = datetime.now().isoformat()
        elif new_status in [QuestStatus.COMPLETED, QuestStatus.FAILED]:
            quest_state.completion_date = datetime.now().isoformat()
            
        # Save changes
        self.save_quest_state(quest_state)
        
        # Log event
        description = f"Quest status changed from {old_status.value} to {new_status.value}"
        if notes:
            description += f": {notes}"
        self.log_quest_event(quest_id, "status_changed", description)
        
        return True
        
    def complete_objective(self, quest_id: str, objective_id: str, notes: str = ""):
        """Mark an objective as completed."""
        if quest_id not in self.quest_states:
            return False
            
        quest_state = self.quest_states[quest_id]
        
        for objective in quest_state.objectives:
            if objective.objective_id == objective_id:
                objective.status = ObjectiveStatus.COMPLETED
                objective.completed_at = datetime.now().isoformat()
                if notes:
                    objective.notes = notes
                    
                # Save changes
                self.save_quest_state(quest_state)
                
                # Log event
                self.log_quest_event(quest_id, "objective_completed", 
                                   f"Objective '{objective.title}' completed",
                                   affected_objective=objective_id)
                
                # Check if quest should be completed
                self.check_quest_completion(quest_id)
                
                return True
                
        return False
        
    def check_quest_completion(self, quest_id: str):
        """Check if quest should be marked as completed."""
        if quest_id not in self.quest_states:
            return
            
        quest_state = self.quest_states[quest_id]
        
        # Check if all required objectives are completed
        required_objectives = [obj for obj in quest_state.objectives if not obj.is_optional]
        completed_required = [obj for obj in required_objectives 
                            if obj.status == ObjectiveStatus.COMPLETED]
        
        if len(completed_required) == len(required_objectives) and len(required_objectives) > 0:
            if quest_state.status != QuestStatus.COMPLETED:
                self.update_quest_status(quest_id, QuestStatus.COMPLETED, 
                                       "All required objectives completed")
                
    def add_objective(self, quest_id: str, objective_data: Dict[str, Any]) -> str:
        """Add a new objective to a quest."""
        if quest_id not in self.quest_states:
            return ""
            
        quest_state = self.quest_states[quest_id]
        
        objective_id = f"{quest_id}_obj_{len(quest_state.objectives)+1}"
        objective = QuestObjective(
            objective_id=objective_id,
            title=objective_data['title'],
            description=objective_data.get('description', ''),
            is_optional=objective_data.get('is_optional', False),
            prerequisite_objectives=objective_data.get('prerequisite_objectives', []),
            completion_triggers=objective_data.get('completion_triggers', []),
            reward_xp=objective_data.get('reward_xp', 0)
        )
        
        quest_state.objectives.append(objective)
        self.save_quest_state(quest_state)
        
        # Log event
        self.log_quest_event(quest_id, "objective_added", 
                           f"New objective added: '{objective.title}'",
                           affected_objective=objective_id)
        
        return objective_id
        
    def log_quest_event(self, quest_id: str, event_type: str, description: str,
                       affected_objective: str = None, session_number: int = None,
                       metadata: Dict = None):
        """Log a quest event."""
        event_id = f"{quest_id}_{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        event = QuestEvent(
            event_id=event_id,
            quest_id=quest_id,
            event_type=event_type,
            timestamp=datetime.now().isoformat(),
            description=description,
            affected_objective=affected_objective,
            session_number=session_number,
            metadata=metadata or {}
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO quest_events 
                (event_id, quest_id, event_type, timestamp, description, 
                 affected_objective, session_number, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.event_id, event.quest_id, event.event_type, event.timestamp,
                event.description, event.affected_objective, event.session_number,
                json.dumps(event.metadata)
            ))
            
    def scan_session_files(self) -> List[Dict]:
        """Scan session files for quest updates."""
        updates = []
        
        if not self.config["tracking_settings"]["auto_update_from_sessions"]:
            return updates
            
        # Find session files
        session_files = []
        for pattern in self.config["file_patterns"]["session_files"]:
            session_files.extend(self.vault_path.glob(pattern))
            
        # Scan each session file
        for session_file in session_files:
            try:
                content = session_file.read_text(encoding='utf-8')
                
                # Extract session number if possible
                session_number = self.extract_session_number(session_file.name)
                
                # Look for quest-related content
                quest_mentions = self.find_quest_mentions(content)
                
                for mention in quest_mentions:
                    updates.append({
                        "file": str(session_file),
                        "session_number": session_number,
                        "quest_id": mention.get("quest_id"),
                        "type": mention.get("type"),
                        "content": mention.get("content")
                    })
                    
            except Exception as e:
                print(f"Error scanning session file {session_file}: {e}")
                
        return updates
        
    def extract_session_number(self, filename: str) -> Optional[int]:
        """Extract session number from filename."""
        # Look for patterns like "Session 1", "Session_1", "1-", etc.
        patterns = [
            r'Session\s*(\d+)',
            r'Session_(\d+)',
            r'(\d+)-',
            r'S(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return int(match.group(1))
                
        return None
        
    def find_quest_mentions(self, content: str) -> List[Dict]:
        """Find quest mentions in content."""
        mentions = []
        
        # Simple pattern matching - could be enhanced with NLP
        quest_patterns = [
            (r'completed\s+(?:quest|objective)[:.]?\s*(.+)', 'objective_completed'),
            (r'finished\s+(?:quest|objective)[:.]?\s*(.+)', 'objective_completed'),
            (r'started\s+(?:quest|objective)[:.]?\s*(.+)', 'objective_started'),
            (r'failed\s+(?:quest|objective)[:.]?\s*(.+)', 'objective_failed'),
            (r'abandoned\s+(?:quest|objective)[:.]?\s*(.+)', 'quest_abandoned'),
        ]
        
        for pattern, mention_type in quest_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                mentions.append({
                    "type": mention_type,
                    "content": match.group(1).strip(),
                    "quest_id": self.find_matching_quest_id(match.group(1))
                })
                
        return mentions
        
    def find_matching_quest_id(self, text: str) -> Optional[str]:
        """Find matching quest ID for text description."""
        text_lower = text.lower()
        
        # Check against existing quest titles
        for quest_id, quest_state in self.quest_states.items():
            if quest_state.title.lower() in text_lower:
                return quest_id
                
            # Check objectives
            for objective in quest_state.objectives:
                if objective.title.lower() in text_lower:
                    return quest_id
                    
        return None
        
    def generate_quest_summary(self, quest_id: str) -> str:
        """Generate a comprehensive quest summary."""
        if quest_id not in self.quest_states:
            return f"Quest {quest_id} not found"
            
        quest = self.quest_states[quest_id]
        
        lines = [
            f"# Quest: {quest.title}",
            f"**Status**: {quest.status.value.replace('_', ' ').title()}",
            "",
            f"## Description",
            quest.description,
            ""
        ]
        
        if quest.quest_giver:
            lines.extend([f"**Quest Giver**: {quest.quest_giver}", ""])
            
        if quest.location:
            lines.extend([f"**Location**: {quest.location}", ""])
            
        if quest.start_date:
            lines.extend([f"**Started**: {quest.start_date[:10]}", ""])
            
        if quest.completion_date:
            lines.extend([f"**Completed**: {quest.completion_date[:10]}", ""])
            
        # Objectives
        if quest.objectives:
            lines.extend(["## Objectives", ""])
            
            for obj in quest.objectives:
                status_icon = {
                    ObjectiveStatus.PENDING: "⭕",
                    ObjectiveStatus.IN_PROGRESS: "🔄",
                    ObjectiveStatus.COMPLETED: "✅",
                    ObjectiveStatus.FAILED: "❌",
                    ObjectiveStatus.OPTIONAL_SKIPPED: "⏭️"
                }.get(obj.status, "⭕")
                
                optional_marker = " (Optional)" if obj.is_optional else ""
                lines.append(f"- {status_icon} **{obj.title}**{optional_marker}")
                
                if obj.description:
                    lines.append(f"  - {obj.description}")
                    
                if obj.notes:
                    lines.append(f"  - *Notes: {obj.notes}*")
                    
                lines.append("")
                
        # Progress statistics
        total_objectives = len(quest.objectives)
        completed_objectives = len([obj for obj in quest.objectives 
                                  if obj.status == ObjectiveStatus.COMPLETED])
        
        if total_objectives > 0:
            progress_pct = (completed_objectives / total_objectives) * 100
            lines.extend([
                f"## Progress",
                f"**Completion**: {completed_objectives}/{total_objectives} objectives ({progress_pct:.1f}%)",
                ""
            ])
            
        # Related entities
        if quest.related_npcs:
            lines.extend([
                "## Related NPCs",
                ""
            ])
            for npc in quest.related_npcs:
                lines.append(f"- [[{npc}]]")
            lines.append("")
            
        if quest.related_locations:
            lines.extend([
                "## Related Locations", 
                ""
            ])
            for location in quest.related_locations:
                lines.append(f"- [[{location}]]")
            lines.append("")
            
        if quest.gm_notes:
            lines.extend([
                "## GM Notes",
                quest.gm_notes,
                ""
            ])
            
        return '\n'.join(lines)
        
    def generate_campaign_quest_report(self) -> str:
        """Generate comprehensive campaign quest report."""
        lines = [
            "# Campaign Quest Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        
        # Statistics
        by_status = defaultdict(int)
        total_objectives = 0
        completed_objectives = 0
        
        for quest in self.quest_states.values():
            by_status[quest.status] += 1
            total_objectives += len(quest.objectives)
            completed_objectives += len([obj for obj in quest.objectives 
                                       if obj.status == ObjectiveStatus.COMPLETED])
                                       
        lines.extend([
            "## Summary Statistics",
            f"- **Total Quests**: {len(self.quest_states)}",
            f"- **Active Quests**: {by_status[QuestStatus.ACTIVE]}",
            f"- **Completed Quests**: {by_status[QuestStatus.COMPLETED]}",
            f"- **Failed/Abandoned**: {by_status[QuestStatus.FAILED] + by_status[QuestStatus.ABANDONED]}",
            f"- **Total Objectives**: {total_objectives}",
            f"- **Completed Objectives**: {completed_objectives}",
            ""
        ])
        
        if total_objectives > 0:
            overall_progress = (completed_objectives / total_objectives) * 100
            lines.append(f"**Overall Campaign Progress**: {overall_progress:.1f}%")
            lines.append("")
            
        # Active quests
        active_quests = [q for q in self.quest_states.values() if q.status == QuestStatus.ACTIVE]
        if active_quests:
            lines.extend([
                "## Active Quests",
                ""
            ])
            
            for quest in sorted(active_quests, key=lambda x: x.start_date or ""):
                obj_completed = len([obj for obj in quest.objectives 
                                   if obj.status == ObjectiveStatus.COMPLETED])
                obj_total = len(quest.objectives)
                progress = f"{obj_completed}/{obj_total}" if obj_total > 0 else "No objectives"
                
                lines.append(f"### {quest.title}")
                lines.append(f"- **Progress**: {progress}")
                if quest.quest_giver:
                    lines.append(f"- **Quest Giver**: {quest.quest_giver}")
                if quest.location:
                    lines.append(f"- **Location**: {quest.location}")
                lines.append("")
                
        # Recently completed quests
        completed_quests = [q for q in self.quest_states.values() if q.status == QuestStatus.COMPLETED]
        recent_completed = sorted(completed_quests, 
                                key=lambda x: x.completion_date or "", reverse=True)[:5]
        
        if recent_completed:
            lines.extend([
                "## Recently Completed",
                ""
            ])
            
            for quest in recent_completed:
                completion_date = quest.completion_date[:10] if quest.completion_date else "Unknown"
                lines.append(f"- **{quest.title}** (Completed: {completion_date})")
                
        return '\n'.join(lines)

def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dynamic Quest Tracker")
    parser.add_argument("--vault-path", default=".", help="Path to vault root")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # List quests
    list_parser = subparsers.add_parser("list", help="List quests")
    list_parser.add_argument("--status", help="Filter by status")
    
    # Create quest
    create_parser = subparsers.add_parser("create", help="Create new quest")
    create_parser.add_argument("title", help="Quest title")
    create_parser.add_argument("--description", help="Quest description")
    create_parser.add_argument("--giver", help="Quest giver")
    
    # Update quest
    update_parser = subparsers.add_parser("update", help="Update quest status")
    update_parser.add_argument("quest_id", help="Quest ID")
    update_parser.add_argument("status", choices=[s.value for s in QuestStatus])
    
    # Complete objective
    complete_parser = subparsers.add_parser("complete", help="Complete objective")
    complete_parser.add_argument("quest_id", help="Quest ID")
    complete_parser.add_argument("objective_id", help="Objective ID")
    
    # Show quest details
    show_parser = subparsers.add_parser("show", help="Show quest details")
    show_parser.add_argument("quest_id", help="Quest ID")
    
    # Generate report
    report_parser = subparsers.add_parser("report", help="Generate quest report")
    
    # Scan sessions
    scan_parser = subparsers.add_parser("scan", help="Scan session files for updates")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    tracker = DynamicQuestTracker(args.vault_path)
    
    if args.command == "list":
        quests = list(tracker.quest_states.values())
        
        if args.status:
            status_filter = QuestStatus(args.status)
            quests = [q for q in quests if q.status == status_filter]
            
        print(f"{'Quest ID':<20} {'Title':<30} {'Status':<12} {'Progress'}")
        print("-" * 75)
        
        for quest in quests:
            obj_completed = len([obj for obj in quest.objectives 
                               if obj.status == ObjectiveStatus.COMPLETED])
            obj_total = len(quest.objectives)
            progress = f"{obj_completed}/{obj_total}" if obj_total > 0 else "0/0"
            
            print(f"{quest.quest_id:<20} {quest.title[:28]:<30} "
                  f"{quest.status.value:<12} {progress}")
                  
    elif args.command == "create":
        quest_data = {
            "title": args.title,
            "description": args.description or "",
            "quest_giver": args.giver or ""
        }
        
        quest_id = tracker.create_quest(quest_data)
        print(f"Created quest: {quest_id}")
        
    elif args.command == "update":
        status = QuestStatus(args.status)
        success = tracker.update_quest_status(args.quest_id, status)
        
        if success:
            print(f"Updated quest {args.quest_id} to {status.value}")
        else:
            print(f"Quest {args.quest_id} not found")
            
    elif args.command == "complete":
        success = tracker.complete_objective(args.quest_id, args.objective_id)
        
        if success:
            print(f"Completed objective {args.objective_id} in quest {args.quest_id}")
        else:
            print(f"Objective or quest not found")
            
    elif args.command == "show":
        summary = tracker.generate_quest_summary(args.quest_id)
        print(summary)
        
    elif args.command == "report":
        report = tracker.generate_campaign_quest_report()
        print(report)
        
    elif args.command == "scan":
        updates = tracker.scan_session_files()
        
        print(f"Found {len(updates)} potential quest updates:")
        for update in updates:
            print(f"- {update['type']}: {update['content']} (Session {update.get('session_number', '?')})")

if __name__ == "__main__":
    main()