#!/usr/bin/env python3
"""
NPC Memory System - Sprint 3 Intelligence Layer Feature

This system tracks NPC interactions with players and evolves relationships
over time. It provides basic memory persistence and relationship dynamics
for enhanced campaign storytelling.

Features:
- Track interactions by NPC and session
- Evolve relationship states (Hostile -> Neutral -> Friendly -> Allied)
- Store memories with emotional context and importance levels
- Generate relationship summaries and interaction histories
- Suggest relationship evolution opportunities
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
import re
from dataclasses import dataclass
from enum import Enum

# Set up paths
VAULT_ROOT = Path(__file__).parent.parent
MEMORY_DATA_DIR = VAULT_ROOT / "scripts" / "memory_data"
MEMORY_DATA_DIR.mkdir(exist_ok=True)

class RelationshipState(Enum):
    """Possible relationship states between NPCs and players"""
    HOSTILE = "hostile"
    SUSPICIOUS = "suspicious" 
    NEUTRAL = "neutral"
    FRIENDLY = "friendly"
    ALLIED = "allied"
    ROMANTIC = "romantic"
    FAMILIAL = "familial"

class MemoryImportance(Enum):
    """Importance levels for NPC memories"""
    TRIVIAL = 1
    MINOR = 2
    MODERATE = 3
    SIGNIFICANT = 4
    CRITICAL = 5

@dataclass
class NPCMemory:
    """Represents a single memory/interaction"""
    timestamp: str
    session_id: str
    interaction_type: str  # conversation, combat, quest, favor, etc.
    description: str
    emotional_context: str  # happy, angry, grateful, suspicious, etc.
    importance: MemoryImportance
    players_involved: List[str]
    location: str
    consequences: List[str]  # What happened as a result

@dataclass
class NPCRelationship:
    """Tracks relationship between NPC and specific player/party"""
    npc_name: str
    target: str  # player name or "party"
    current_state: RelationshipState
    relationship_history: List[Tuple[str, RelationshipState, str]]  # timestamp, state, reason
    trust_level: int  # -100 to +100
    respect_level: int  # -100 to +100
    personal_connection: int  # -100 to +100
    memories: List[NPCMemory]
    last_interaction: Optional[str]
    relationship_notes: str

class NPCMemorySystem:
    """Main system for managing NPC memories and relationships"""
    
    def __init__(self):
        self.memory_file = MEMORY_DATA_DIR / "npc_memories.json"
        self.relationship_file = MEMORY_DATA_DIR / "npc_relationships.json"
        self.config_file = MEMORY_DATA_DIR / "memory_config.json"
        
        # Load existing data
        self.memories = self._load_memories()
        self.relationships = self._load_relationships()
        self.config = self._load_config()
        
    def _load_memories(self) -> Dict[str, List[NPCMemory]]:
        """Load NPC memories from file"""
        if not self.memory_file.exists():
            return {}
        
        with open(self.memory_file, 'r') as f:
            data = json.load(f)
        
        memories = {}
        for npc_name, memory_list in data.items():
            memories[npc_name] = []
            for mem_data in memory_list:
                memory = NPCMemory(
                    timestamp=mem_data['timestamp'],
                    session_id=mem_data['session_id'],
                    interaction_type=mem_data['interaction_type'],
                    description=mem_data['description'],
                    emotional_context=mem_data['emotional_context'],
                    importance=MemoryImportance(mem_data['importance']),
                    players_involved=mem_data['players_involved'],
                    location=mem_data['location'],
                    consequences=mem_data['consequences']
                )
                memories[npc_name].append(memory)
        
        return memories
    
    def _save_memories(self):
        """Save memories to file"""
        data = {}
        for npc_name, memory_list in self.memories.items():
            data[npc_name] = []
            for memory in memory_list:
                mem_data = {
                    'timestamp': memory.timestamp,
                    'session_id': memory.session_id,
                    'interaction_type': memory.interaction_type,
                    'description': memory.description,
                    'emotional_context': memory.emotional_context,
                    'importance': memory.importance.value,
                    'players_involved': memory.players_involved,
                    'location': memory.location,
                    'consequences': memory.consequences
                }
                data[npc_name].append(mem_data)
        
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_relationships(self) -> Dict[str, NPCRelationship]:
        """Load NPC relationships from file"""
        if not self.relationship_file.exists():
            return {}
        
        with open(self.relationship_file, 'r') as f:
            data = json.load(f)
        
        relationships = {}
        for key, rel_data in data.items():
            relationship = NPCRelationship(
                npc_name=rel_data['npc_name'],
                target=rel_data['target'],
                current_state=RelationshipState(rel_data['current_state']),
                relationship_history=[(h[0], RelationshipState(h[1]), h[2]) for h in rel_data['relationship_history']],
                trust_level=rel_data['trust_level'],
                respect_level=rel_data['respect_level'],
                personal_connection=rel_data['personal_connection'],
                memories=[],  # Will be loaded separately
                last_interaction=rel_data.get('last_interaction'),
                relationship_notes=rel_data.get('relationship_notes', '')
            )
            relationships[key] = relationship
        
        return relationships
    
    def _save_relationships(self):
        """Save relationships to file"""
        data = {}
        for key, relationship in self.relationships.items():
            rel_data = {
                'npc_name': relationship.npc_name,
                'target': relationship.target,
                'current_state': relationship.current_state.value,
                'relationship_history': [(h[0], h[1].value, h[2]) for h in relationship.relationship_history],
                'trust_level': relationship.trust_level,
                'respect_level': relationship.respect_level,
                'personal_connection': relationship.personal_connection,
                'last_interaction': relationship.last_interaction,
                'relationship_notes': relationship.relationship_notes
            }
            data[key] = rel_data
        
        with open(self.relationship_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_config(self) -> Dict:
        """Load system configuration"""
        default_config = {
            'relationship_evolution_thresholds': {
                'trust_change_per_positive': 5,
                'trust_change_per_negative': -10,
                'respect_change_per_positive': 3,
                'respect_change_per_negative': -7,
                'connection_change_per_personal': 8,
                'state_change_thresholds': {
                    'hostile_to_suspicious': -50,
                    'suspicious_to_neutral': 0,
                    'neutral_to_friendly': 30,
                    'friendly_to_allied': 60
                }
            },
            'memory_retention': {
                'max_trivial_memories': 5,
                'max_minor_memories': 10,
                'max_moderate_memories': 15,
                'max_significant_memories': 25,
                'critical_memories_unlimited': True
            }
        }
        
        if not self.config_file.exists():
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
        
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def add_memory(self, npc_name: str, session_id: str, interaction_type: str, 
                   description: str, emotional_context: str, importance: MemoryImportance,
                   players_involved: List[str], location: str, consequences: List[str] = None) -> bool:
        """Add a new memory for an NPC"""
        
        if consequences is None:
            consequences = []
        
        memory = NPCMemory(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            interaction_type=interaction_type,
            description=description,
            emotional_context=emotional_context,
            importance=importance,
            players_involved=players_involved,
            location=location,
            consequences=consequences
        )
        
        # Initialize NPC memory list if needed
        if npc_name not in self.memories:
            self.memories[npc_name] = []
        
        self.memories[npc_name].append(memory)
        
        # Update relationships based on this memory
        for player in players_involved:
            self._update_relationship(npc_name, player, memory)
        
        # Clean up old memories if needed
        self._manage_memory_retention(npc_name)
        
        self._save_memories()
        self._save_relationships()
        
        return True
    
    def _update_relationship(self, npc_name: str, player: str, memory: NPCMemory):
        """Update relationship based on new memory"""
        rel_key = f"{npc_name}:{player}"
        
        # Initialize relationship if needed
        if rel_key not in self.relationships:
            self.relationships[rel_key] = NPCRelationship(
                npc_name=npc_name,
                target=player,
                current_state=RelationshipState.NEUTRAL,
                relationship_history=[],
                trust_level=0,
                respect_level=0,
                personal_connection=0,
                memories=[],
                last_interaction=None,
                relationship_notes=""
            )
        
        relationship = self.relationships[rel_key]
        old_state = relationship.current_state
        
        # Update metrics based on interaction type and emotional context
        trust_change = 0
        respect_change = 0
        connection_change = 0
        
        # Determine changes based on emotional context
        positive_emotions = ['happy', 'grateful', 'pleased', 'impressed', 'relieved']
        negative_emotions = ['angry', 'disappointed', 'suspicious', 'hurt', 'betrayed']
        
        if any(emotion in memory.emotional_context.lower() for emotion in positive_emotions):
            trust_change = self.config['relationship_evolution_thresholds']['trust_change_per_positive']
            respect_change = self.config['relationship_evolution_thresholds']['respect_change_per_positive']
        elif any(emotion in memory.emotional_context.lower() for emotion in negative_emotions):
            trust_change = self.config['relationship_evolution_thresholds']['trust_change_per_negative']
            respect_change = self.config['relationship_evolution_thresholds']['respect_change_per_negative']
        
        # Personal interactions increase connection
        if memory.interaction_type in ['conversation', 'favor', 'personal']:
            connection_change = self.config['relationship_evolution_thresholds']['connection_change_per_personal']
        
        # Scale by importance
        importance_multiplier = memory.importance.value / 3
        trust_change = int(trust_change * importance_multiplier)
        respect_change = int(respect_change * importance_multiplier)
        connection_change = int(connection_change * importance_multiplier)
        
        # Apply changes
        relationship.trust_level = max(-100, min(100, relationship.trust_level + trust_change))
        relationship.respect_level = max(-100, min(100, relationship.respect_level + respect_change))
        relationship.personal_connection = max(-100, min(100, relationship.personal_connection + connection_change))
        relationship.last_interaction = memory.timestamp
        
        # Determine new state based on combined metrics
        combined_score = (relationship.trust_level + relationship.respect_level + relationship.personal_connection) / 3
        thresholds = self.config['relationship_evolution_thresholds']['state_change_thresholds']
        
        new_state = relationship.current_state
        if combined_score >= thresholds['friendly_to_allied']:
            new_state = RelationshipState.ALLIED
        elif combined_score >= thresholds['neutral_to_friendly']:
            new_state = RelationshipState.FRIENDLY
        elif combined_score >= thresholds['suspicious_to_neutral']:
            new_state = RelationshipState.NEUTRAL
        elif combined_score >= thresholds['hostile_to_suspicious']:
            new_state = RelationshipState.SUSPICIOUS
        else:
            new_state = RelationshipState.HOSTILE
        
        # Record state change if it occurred
        if new_state != old_state:
            relationship.relationship_history.append((
                memory.timestamp,
                new_state,
                f"Changed from {old_state.value} to {new_state.value} due to: {memory.description[:50]}..."
            ))
            relationship.current_state = new_state
    
    def _manage_memory_retention(self, npc_name: str):
        """Remove old memories based on retention policy"""
        if npc_name not in self.memories:
            return
        
        memories = self.memories[npc_name]
        retention = self.config['memory_retention']
        
        # Group memories by importance
        by_importance = {}
        for memory in memories:
            if memory.importance not in by_importance:
                by_importance[memory.importance] = []
            by_importance[memory.importance].append(memory)
        
        # Remove excess memories for each importance level
        kept_memories = []
        
        for importance, memory_list in by_importance.items():
            if importance == MemoryImportance.CRITICAL and retention['critical_memories_unlimited']:
                kept_memories.extend(memory_list)
                continue
            
            max_count = {
                MemoryImportance.TRIVIAL: retention['max_trivial_memories'],
                MemoryImportance.MINOR: retention['max_minor_memories'],
                MemoryImportance.MODERATE: retention['max_moderate_memories'],
                MemoryImportance.SIGNIFICANT: retention['max_significant_memories'],
                MemoryImportance.CRITICAL: 100  # High limit if not unlimited
            }[importance]
            
            # Keep most recent memories
            memory_list.sort(key=lambda m: m.timestamp, reverse=True)
            kept_memories.extend(memory_list[:max_count])
        
        self.memories[npc_name] = kept_memories
    
    def get_npc_memories(self, npc_name: str, limit: int = None) -> List[NPCMemory]:
        """Get memories for a specific NPC"""
        if npc_name not in self.memories:
            return []
        
        memories = self.memories[npc_name]
        memories.sort(key=lambda m: m.timestamp, reverse=True)
        
        if limit:
            return memories[:limit]
        return memories
    
    def get_relationship(self, npc_name: str, player: str) -> Optional[NPCRelationship]:
        """Get relationship between NPC and player"""
        rel_key = f"{npc_name}:{player}"
        return self.relationships.get(rel_key)
    
    def generate_relationship_summary(self, npc_name: str, player: str) -> str:
        """Generate a narrative summary of the relationship"""
        relationship = self.get_relationship(npc_name, player)
        if not relationship:
            return f"{npc_name} has no recorded interactions with {player}."
        
        memories = self.get_npc_memories(npc_name)
        player_memories = [m for m in memories if player in m.players_involved]
        
        summary = f"**{npc_name} & {player} Relationship Summary**\n\n"
        summary += f"**Current Status:** {relationship.current_state.value.title()}\n"
        summary += f"**Trust:** {relationship.trust_level}/100\n"
        summary += f"**Respect:** {relationship.respect_level}/100\n" 
        summary += f"**Personal Connection:** {relationship.personal_connection}/100\n\n"
        
        if relationship.last_interaction:
            last_date = datetime.fromisoformat(relationship.last_interaction).strftime("%Y-%m-%d")
            summary += f"**Last Interaction:** {last_date}\n\n"
        
        if player_memories:
            summary += "**Recent Significant Interactions:**\n"
            for memory in player_memories[:5]:
                date = datetime.fromisoformat(memory.timestamp).strftime("%m/%d")
                summary += f"- {date}: {memory.description} ({memory.emotional_context})\n"
        
        if relationship.relationship_history:
            summary += f"\n**Relationship Evolution:**\n"
            for timestamp, state, reason in relationship.relationship_history[-3:]:
                date = datetime.fromisoformat(timestamp).strftime("%m/%d")
                summary += f"- {date}: {reason}\n"
        
        return summary
    
    def suggest_relationship_opportunities(self, npc_name: str) -> List[str]:
        """Suggest opportunities for relationship development"""
        suggestions = []
        
        if npc_name not in self.memories:
            suggestions.append(f"No interactions recorded with {npc_name} yet - perfect opportunity to establish first contact!")
            return suggestions
        
        memories = self.get_npc_memories(npc_name)
        
        # Analyze patterns
        interaction_types = set(m.interaction_type for m in memories)
        emotional_contexts = [m.emotional_context for m in memories]
        recent_memories = memories[:5]
        
        # Check for relationship development opportunities
        if 'conversation' not in interaction_types:
            suggestions.append(f"Consider a deeper conversation with {npc_name} - they've had no recorded personal talks")
        
        if 'favor' not in interaction_types and len(memories) > 3:
            suggestions.append(f"{npc_name} might appreciate a favor - could strengthen the relationship")
        
        # Check emotional patterns
        negative_recent = sum(1 for m in recent_memories if any(neg in m.emotional_context for neg in ['angry', 'suspicious', 'hurt']))
        if negative_recent > 2:
            suggestions.append(f"{npc_name} has had several negative interactions lately - time for reconciliation?")
        
        # Check for stagnant relationships
        if len(memories) > 5:
            states = [rel[1] for rel in self.relationships.get(f"{npc_name}:party", NPCRelationship('', '', RelationshipState.NEUTRAL, [], 0, 0, 0, [], None, '')).relationship_history]
            if not states or (len(states) == 1 and len(memories) > 8):
                suggestions.append(f"Relationship with {npc_name} hasn't evolved much - perhaps it's time for a significant interaction")
        
        return suggestions or [f"{npc_name} relationship seems stable - maintain current interactions"]
    
    def search_memories(self, query: str, npc_name: str = None) -> List[Tuple[str, NPCMemory]]:
        """Search memories by description or context"""
        results = []
        query_lower = query.lower()
        
        npcs_to_search = [npc_name] if npc_name else self.memories.keys()
        
        for npc in npcs_to_search:
            if npc in self.memories:
                for memory in self.memories[npc]:
                    if (query_lower in memory.description.lower() or 
                        query_lower in memory.emotional_context.lower() or
                        query_lower in memory.location.lower() or
                        any(query_lower in consequence.lower() for consequence in memory.consequences)):
                        results.append((npc, memory))
        
        return results
    
    def export_relationship_data(self, format_type: str = "json") -> str:
        """Export relationship data for analysis"""
        if format_type == "json":
            data = {
                'relationships': {},
                'memory_counts': {},
                'generated_at': datetime.now().isoformat()
            }
            
            for key, relationship in self.relationships.items():
                data['relationships'][key] = {
                    'npc_name': relationship.npc_name,
                    'target': relationship.target,
                    'current_state': relationship.current_state.value,
                    'trust_level': relationship.trust_level,
                    'respect_level': relationship.respect_level,
                    'personal_connection': relationship.personal_connection,
                    'interaction_count': len(self.get_npc_memories(relationship.npc_name)),
                    'last_interaction': relationship.last_interaction
                }
            
            for npc_name, memories in self.memories.items():
                data['memory_counts'][npc_name] = {
                    'total': len(memories),
                    'by_importance': {imp.value: sum(1 for m in memories if m.importance == imp) for imp in MemoryImportance}
                }
            
            return json.dumps(data, indent=2)
        
        return "Unsupported format"

def main():
    parser = argparse.ArgumentParser(description="NPC Memory System - Track relationships and interactions")
    parser.add_argument('command', choices=['add-memory', 'view-memories', 'relationship', 'summary', 'search', 'suggest', 'export'])
    
    # Add memory arguments
    parser.add_argument('--npc', required=False, help='NPC name')
    parser.add_argument('--player', required=False, help='Player name')
    parser.add_argument('--session', required=False, help='Session ID')
    parser.add_argument('--type', required=False, help='Interaction type (conversation, combat, quest, favor)')
    parser.add_argument('--description', required=False, help='Description of interaction')
    parser.add_argument('--emotion', required=False, help='Emotional context')
    parser.add_argument('--importance', type=int, choices=[1,2,3,4,5], help='Importance level (1-5)')
    parser.add_argument('--location', required=False, help='Location of interaction')
    parser.add_argument('--consequences', required=False, help='Consequences (comma-separated)')
    
    # View arguments
    parser.add_argument('--limit', type=int, help='Limit number of results')
    parser.add_argument('--query', help='Search query')
    
    args = parser.parse_args()
    
    system = NPCMemorySystem()
    
    if args.command == 'add-memory':
        if not all([args.npc, args.player, args.session, args.type, args.description, args.emotion, args.importance, args.location]):
            print("Error: add-memory requires --npc, --player, --session, --type, --description, --emotion, --importance, and --location")
            return
        
        consequences = args.consequences.split(',') if args.consequences else []
        players_involved = [args.player]  # Could be extended to multiple players
        
        success = system.add_memory(
            npc_name=args.npc,
            session_id=args.session,
            interaction_type=args.type,
            description=args.description,
            emotional_context=args.emotion,
            importance=MemoryImportance(args.importance),
            players_involved=players_involved,
            location=args.location,
            consequences=consequences
        )
        
        if success:
            print(f"✅ Memory added for {args.npc}")
            # Show updated relationship status
            relationship = system.get_relationship(args.npc, args.player)
            if relationship:
                print(f"Relationship with {args.player}: {relationship.current_state.value} (Trust: {relationship.trust_level}, Respect: {relationship.respect_level})")
        else:
            print("❌ Failed to add memory")
    
    elif args.command == 'view-memories':
        if not args.npc:
            print("Error: view-memories requires --npc")
            return
        
        memories = system.get_npc_memories(args.npc, args.limit)
        if not memories:
            print(f"No memories found for {args.npc}")
            return
        
        print(f"\n📖 **Memories for {args.npc}** ({len(memories)} total)\n")
        for memory in memories:
            date = datetime.fromisoformat(memory.timestamp).strftime("%Y-%m-%d %H:%M")
            print(f"**{date}** - {memory.interaction_type.title()}")
            print(f"   Players: {', '.join(memory.players_involved)}")
            print(f"   Location: {memory.location}")
            print(f"   Context: {memory.emotional_context}")
            print(f"   Importance: {memory.importance.name}")
            print(f"   Description: {memory.description}")
            if memory.consequences:
                print(f"   Consequences: {', '.join(memory.consequences)}")
            print()
    
    elif args.command == 'relationship':
        if not all([args.npc, args.player]):
            print("Error: relationship requires --npc and --player")
            return
        
        summary = system.generate_relationship_summary(args.npc, args.player)
        print(summary)
    
    elif args.command == 'summary':
        relationships = system.relationships
        memories = system.memories
        
        print("🧠 **NPC Memory System Summary**\n")
        print(f"**NPCs with memories:** {len(memories)}")
        print(f"**Active relationships:** {len(relationships)}")
        
        if memories:
            total_memories = sum(len(mem_list) for mem_list in memories.values())
            print(f"**Total memories stored:** {total_memories}")
            
            print("\n**NPCs by memory count:**")
            npc_counts = [(npc, len(mems)) for npc, mems in memories.items()]
            npc_counts.sort(key=lambda x: x[1], reverse=True)
            for npc, count in npc_counts[:10]:
                print(f"  {npc}: {count} memories")
        
        if relationships:
            print("\n**Relationship states:**")
            state_counts = {}
            for rel in relationships.values():
                state = rel.current_state.value
                state_counts[state] = state_counts.get(state, 0) + 1
            
            for state, count in sorted(state_counts.items()):
                print(f"  {state.title()}: {count}")
    
    elif args.command == 'search':
        if not args.query:
            print("Error: search requires --query")
            return
        
        results = system.search_memories(args.query, args.npc)
        if not results:
            print(f"No memories found matching '{args.query}'")
            return
        
        print(f"\n🔍 **Search results for '{args.query}'** ({len(results)} found)\n")
        for npc_name, memory in results:
            date = datetime.fromisoformat(memory.timestamp).strftime("%Y-%m-%d")
            print(f"**{npc_name}** - {date} - {memory.interaction_type}")
            print(f"   {memory.description}")
            print(f"   Emotion: {memory.emotional_context}, Location: {memory.location}")
            print()
    
    elif args.command == 'suggest':
        if not args.npc:
            print("Error: suggest requires --npc")
            return
        
        suggestions = system.suggest_relationship_opportunities(args.npc)
        print(f"\n💡 **Relationship opportunities for {args.npc}:**\n")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
    
    elif args.command == 'export':
        data = system.export_relationship_data()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = MEMORY_DATA_DIR / f"relationship_export_{timestamp}.json"
        
        with open(filename, 'w') as f:
            f.write(data)
        
        print(f"✅ Relationship data exported to: {filename}")

if __name__ == "__main__":
    main()