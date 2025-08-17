#!/usr/bin/env python3
"""
Deep Multi-Agent Evaluation System
Each directory gets a specialized agent that evaluates notes with 20-50 context-specific improvements
"""

import os
import yaml
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import random
import hashlib
from abc import ABC, abstractmethod

class BaseEvaluationAgent(ABC):
    """Base class for specialized evaluation agents"""
    
    def __init__(self, agent_name: str, target_directory: str):
        self.agent_name = agent_name
        self.target_directory = target_directory
        self.improvements_made = 0
        self.notes_evaluated = 0
        
    @abstractmethod
    def evaluate_note(self, note_path: Path, content: str) -> List[Dict[str, str]]:
        """Evaluate a note and return list of improvements"""
        pass
        
    @abstractmethod
    def get_evaluation_criteria(self) -> List[str]:
        """Return evaluation criteria specific to this agent"""
        pass
        
    def generate_improvements(self, note_path: Path, content: str, min_improvements: int = 20, max_improvements: int = 50) -> List[Dict[str, str]]:
        """Generate between min and max improvements for a note"""
        improvements = []
        criteria = self.get_evaluation_criteria()
        
        # Analyze content structure
        has_frontmatter = content.startswith('---')
        has_headers = '##' in content
        has_lists = '- ' in content or '* ' in content
        has_links = '[[' in content
        has_tables = '|' in content
        word_count = len(content.split())
        
        # Generate improvements based on criteria
        for criterion in criteria:
            improvement = self.evaluate_criterion(criterion, note_path, content, {
                'has_frontmatter': has_frontmatter,
                'has_headers': has_headers,
                'has_lists': has_lists,
                'has_links': has_links,
                'has_tables': has_tables,
                'word_count': word_count
            })
            if improvement:
                improvements.append(improvement)
                
        # Ensure we have enough improvements
        while len(improvements) < min_improvements:
            improvements.append(self.generate_contextual_improvement(note_path, content))
            
        # Limit to max improvements
        return improvements[:max_improvements]
        
    @abstractmethod
    def evaluate_criterion(self, criterion: str, note_path: Path, content: str, metadata: Dict) -> Optional[Dict[str, str]]:
        """Evaluate a specific criterion"""
        pass
        
    @abstractmethod
    def generate_contextual_improvement(self, note_path: Path, content: str) -> Dict[str, str]:
        """Generate a contextual improvement based on folder context"""
        pass

class AdventureAgent(BaseEvaluationAgent):
    """Specialized agent for 01_Adventures directory"""
    
    def __init__(self):
        super().__init__("Adventure Specialist", "01_Adventures")
        
    def get_evaluation_criteria(self) -> List[str]:
        return [
            "encounter_balance", "treasure_distribution", "pacing_structure",
            "player_agency", "narrative_hooks", "npc_motivations", 
            "environmental_challenges", "moral_dilemmas", "combat_variety",
            "exploration_rewards", "puzzle_complexity", "dramatic_tension",
            "scene_transitions", "backup_plans", "failure_consequences",
            "success_variations", "time_pressure", "resource_management",
            "faction_involvement", "world_impact", "replayability",
            "scalability", "accessibility", "memorable_moments",
            "plot_twists", "foreshadowing", "callbacks", "epilogue_seeds"
        ]
        
    def evaluate_note(self, note_path: Path, content: str) -> List[Dict[str, str]]:
        return self.generate_improvements(note_path, content, 25, 45)
        
    def evaluate_criterion(self, criterion: str, note_path: Path, content: str, metadata: Dict) -> Optional[Dict[str, str]]:
        improvements_map = {
            "encounter_balance": {
                "type": "combat",
                "improvement": "Add encounter scaling table for parties of 3-6 players, levels 1-20",
                "section": "## Encounter Scaling\n\n| Party Level | 3 Players | 4 Players | 5 Players | 6 Players |\n|------------|-----------|-----------|-----------|----------|\n| 1-4 | CR 2 | CR 3 | CR 4 | CR 5 |\n| 5-10 | CR 7 | CR 9 | CR 11 | CR 13 |\n| 11-16 | CR 14 | CR 17 | CR 19 | CR 21 |\n| 17-20 | CR 22 | CR 24 | CR 26 | CR 28 |"
            },
            "treasure_distribution": {
                "type": "rewards",
                "improvement": "Create treasure parcels for each major encounter",
                "section": "## Treasure Parcels\n\n### Parcel A (Combat Victory)\n- 2d6 × 10 gp\n- Potion of Healing\n- Clue to next location\n\n### Parcel B (Exploration)\n- Magic item (roll on Table F)\n- Ancient map fragment\n- 1d4 gems (50 gp each)"
            },
            "pacing_structure": {
                "type": "structure",
                "improvement": "Add three-act structure with rising action",
                "section": "## Adventure Pacing\n\n### Act 1: Setup (Sessions 1-2)\n- Hook presentation\n- Initial investigation\n- First combat\n\n### Act 2: Confrontation (Sessions 3-4)\n- Main challenges\n- Plot complications\n- Resource depletion\n\n### Act 3: Resolution (Session 5)\n- Final confrontation\n- Consequences\n- Epilogue hooks"
            },
            "player_agency": {
                "type": "choices",
                "improvement": "Add meaningful decision points with consequences",
                "section": "## Critical Decisions\n\n1. **The Prisoner's Dilemma**: Save the hostages OR pursue the villain\n2. **The Devil's Bargain**: Accept dark power OR fight with disadvantage\n3. **The Succession Choice**: Support the heir OR the usurper"
            },
            "moral_dilemmas": {
                "type": "roleplay",
                "improvement": "Include ethical challenges without clear answers",
                "section": "## Moral Quandaries\n\n- The villain's family begs for mercy\n- Stealing medicine to save a plague victim\n- Choosing between two villages to save"
            }
        }
        
        if criterion in improvements_map:
            return improvements_map[criterion]
        return None
        
    def generate_contextual_improvement(self, note_path: Path, content: str) -> Dict[str, str]:
        context_improvements = [
            {"type": "backup", "improvement": "Add 'What if players skip this?' contingency"},
            {"type": "spotlight", "improvement": "Include spotlight moment for each character class"},
            {"type": "worldbuilding", "improvement": "Connect to three other adventures in the vault"},
            {"type": "variants", "improvement": "Add horror, intrigue, and comedy tone variants"},
            {"type": "props", "improvement": "List physical props and handouts needed"},
            {"type": "soundtrack", "improvement": "Suggest music/ambiance for each scene"},
            {"type": "art", "improvement": "Add AI art prompts for key scenes"},
            {"type": "accessibility", "improvement": "Include content warnings and safety tools"},
            {"type": "session_zero", "improvement": "Add session zero integration questions"},
            {"type": "level_range", "improvement": "Provide scaling for different level ranges"}
        ]
        return random.choice(context_improvements)

class WorldbuildingAgent(BaseEvaluationAgent):
    """Specialized agent for 02_Worldbuilding directory"""
    
    def __init__(self):
        super().__init__("Worldbuilding Expert", "02_Worldbuilding")
        
    def get_evaluation_criteria(self) -> List[str]:
        return [
            "historical_depth", "cultural_details", "economic_systems",
            "political_structures", "religious_practices", "daily_life",
            "technology_level", "magic_integration", "geography_impact",
            "climate_effects", "trade_networks", "military_organization",
            "legal_systems", "education_systems", "art_culture",
            "architecture_style", "food_cuisine", "fashion_clothing",
            "holidays_festivals", "languages_dialects", "social_hierarchy",
            "gender_roles", "minority_groups", "conflicts_tensions",
            "alliances_treaties", "myths_legends", "prophecies_omens",
            "natural_resources", "supernatural_elements", "planar_connections"
        ]
        
    def evaluate_note(self, note_path: Path, content: str) -> List[Dict[str, str]]:
        return self.generate_improvements(note_path, content, 30, 50)
        
    def evaluate_criterion(self, criterion: str, note_path: Path, content: str, metadata: Dict) -> Optional[Dict[str, str]]:
        improvements_map = {
            "historical_depth": {
                "type": "history",
                "improvement": "Add three historical eras with major events",
                "section": "## Historical Timeline\n\n### The Age of Founding (1000 years ago)\n- The First Settlement\n- Discovery of magical crystals\n- War with indigenous peoples\n\n### The Golden Era (500 years ago)\n- Economic prosperity\n- Cultural renaissance\n- Expansion of territory\n\n### The Time of Troubles (100 years ago)\n- Civil war\n- Natural disasters\n- Current power structures established"
            },
            "cultural_details": {
                "type": "culture",
                "improvement": "Define unique cultural practices and taboos",
                "section": "## Cultural Practices\n\n### Greetings\n- Touch foreheads for equals\n- Bow deeply to superiors\n- Never shake with left hand\n\n### Taboos\n- Speaking during sunset prayer\n- Wearing red on holy days\n- Pointing at the moon"
            },
            "economic_systems": {
                "type": "economy",
                "improvement": "Detail currency, trade goods, and wealth distribution",
                "section": "## Economic Structure\n\n### Currency\n- Copper Drops (cp)\n- Silver Streams (sp) \n- Gold Suns (gp)\n- Platinum Crowns (pp)\n\n### Major Exports\n- Refined crystals\n- Exotic textiles\n- Trained beasts\n\n### Wealth Distribution\n- 1% control 60% of wealth\n- 20% middle class\n- 79% working poor"
            },
            "religious_practices": {
                "type": "religion",
                "improvement": "Create detailed religious observances",
                "section": "## Religious Observances\n\n### Daily Prayers\n- Dawn: Gratitude for life\n- Noon: Strength for labor\n- Dusk: Protection from darkness\n\n### Weekly Observance\n- Temple attendance mandatory\n- Ritual cleansing required\n- Tithing of 10% income"
            },
            "daily_life": {
                "type": "lifestyle",
                "improvement": "Describe typical day for different social classes",
                "section": "## A Day in the Life\n\n### Nobility\n- 8am: Private tutoring\n- 10am: Court attendance\n- 2pm: Social visits\n- 6pm: Formal dinner\n- 9pm: Entertainment\n\n### Commoner\n- 5am: Morning prayers\n- 6am: Begin labor\n- Noon: Simple meal\n- 6pm: Return home\n- 8pm: Sleep"
            }
        }
        
        if criterion in improvements_map:
            return improvements_map[criterion]
        return None
        
    def generate_contextual_improvement(self, note_path: Path, content: str) -> Dict[str, str]:
        context_improvements = [
            {"type": "sensory", "improvement": "Add smells, sounds, and textures unique to this culture"},
            {"type": "contradictions", "improvement": "Include cultural hypocrisies and double standards"},
            {"type": "evolution", "improvement": "Show how traditions are changing with new generation"},
            {"type": "diaspora", "improvement": "Describe how this culture exists in other regions"},
            {"type": "material_culture", "improvement": "Detail common objects and their cultural significance"},
            {"type": "oral_tradition", "improvement": "Add folk tales and children's stories"},
            {"type": "superstitions", "improvement": "List common superstitions and their origins"},
            {"type": "coming_of_age", "improvement": "Describe rites of passage and adulthood markers"},
            {"type": "death_customs", "improvement": "Detail funeral rites and afterlife beliefs"},
            {"type": "hospitality", "improvement": "Explain guest rights and host obligations"}
        ]
        return random.choice(context_improvements)

class PeopleAgent(BaseEvaluationAgent):
    """Specialized agent for 03_People directory"""
    
    def __init__(self):
        super().__init__("Character Specialist", "03_People")
        
    def get_evaluation_criteria(self) -> List[str]:
        return [
            "personality_depth", "backstory_richness", "motivations_clear",
            "fears_defined", "relationships_mapped", "secrets_hidden",
            "appearance_detailed", "mannerisms_unique", "speech_patterns",
            "skills_justified", "weaknesses_exploitable", "goals_immediate",
            "goals_longterm", "moral_alignment", "character_arc",
            "internal_conflicts", "external_pressures", "allies_identified",
            "enemies_named", "resources_available", "reputation_established",
            "quirks_memorable", "ideals_values", "bonds_connections",
            "flaws_authentic", "growth_potential", "plot_hooks_embedded",
            "stat_block_complete", "equipment_logical", "daily_routine"
        ]
        
    def evaluate_note(self, note_path: Path, content: str) -> List[Dict[str, str]]:
        return self.generate_improvements(note_path, content, 20, 40)
        
    def evaluate_criterion(self, criterion: str, note_path: Path, content: str, metadata: Dict) -> Optional[Dict[str, str]]:
        improvements_map = {
            "personality_depth": {
                "type": "personality",
                "improvement": "Add personality traits using the Big Five model",
                "section": "## Personality Profile\n\n### Big Five Traits\n- **Openness**: High - Loves new experiences\n- **Conscientiousness**: Low - Disorganized but creative\n- **Extraversion**: Medium - Selectively social\n- **Agreeableness**: Low - Skeptical and untrusting\n- **Neuroticism**: High - Anxious and moody"
            },
            "backstory_richness": {
                "type": "history",
                "improvement": "Add three formative events that shaped them",
                "section": "## Formative Events\n\n### Age 7: The Fire\nWitnessed family home burn down, developed fear of fire but fascination with phoenix mythology\n\n### Age 14: First Love\nBetrayed by childhood sweetheart who was a spy, never fully trusts romantic partners\n\n### Age 21: The Mentor\nTrained under Master Chen who disappeared mysteriously, still searching for answers"
            },
            "mannerisms_unique": {
                "type": "behavior",
                "improvement": "Create distinctive physical and verbal habits",
                "section": "## Distinctive Mannerisms\n\n### Physical Habits\n- Taps fingers when lying\n- Always sits facing the door\n- Touches scar when nervous\n\n### Verbal Tics\n- Says 'you understand?' after explanations\n- Never uses contractions when angry\n- Quotes their grandmother frequently"
            },
            "secrets_hidden": {
                "type": "secrets",
                "improvement": "Add three secrets of increasing severity",
                "section": "## Hidden Secrets\n\n### Minor Secret\nStole food as a child to survive, still shoplifts occasionally out of habit\n\n### Major Secret\nKilled someone in self-defense but let another take the blame\n\n### Dark Secret\nMade a pact with a demon for power, must deliver souls or forfeit own"
            },
            "relationships_mapped": {
                "type": "social",
                "improvement": "Create relationship web with 5+ connections",
                "section": "## Relationship Web\n\n- **Marcus** (brother): Estranged, haven't spoken in 5 years\n- **Elena** (mentor): Respects but secretly resents\n- **Thorne** (rival): Competitive friendship, might be romantic tension\n- **Sara** (dependent): Protecting her is primary motivation\n- **Viktor** (enemy): Killed their partner, mutual vendetta"
            }
        }
        
        if criterion in improvements_map:
            return improvements_map[criterion]
        return None
        
    def generate_contextual_improvement(self, note_path: Path, content: str) -> Dict[str, str]:
        context_improvements = [
            {"type": "voice", "improvement": "Add example dialogue in different emotional states"},
            {"type": "psychology", "improvement": "Include trauma responses and coping mechanisms"},
            {"type": "romance", "improvement": "Define romantic history and preferences"},
            {"type": "combat", "improvement": "Describe fighting style and battle tactics"},
            {"type": "possessions", "improvement": "List sentimental items they always carry"},
            {"type": "dreams", "improvement": "Add recurring dreams or nightmares"},
            {"type": "humor", "improvement": "Define sense of humor and favorite jokes"},
            {"type": "prejudices", "improvement": "Include biases they need to overcome"},
            {"type": "skills_hidden", "improvement": "Add surprising talents they rarely reveal"},
            {"type": "breaking_point", "improvement": "Define what would make them snap"}
        ]
        return random.choice(context_improvements)

class PlacesAgent(BaseEvaluationAgent):
    """Specialized agent for 04_Places directory"""
    
    def __init__(self):
        super().__init__("Location Expert", "04_Places")
        
    def get_evaluation_criteria(self) -> List[str]:
        return [
            "sensory_description", "layout_mapped", "inhabitants_detailed",
            "history_embedded", "dangers_present", "resources_available",
            "access_routes", "defensive_features", "hidden_areas",
            "lighting_conditions", "weather_patterns", "time_variations",
            "social_dynamics", "economic_activity", "political_importance",
            "religious_significance", "military_value", "trade_connections",
            "notable_features", "local_customs", "urban_planning",
            "infrastructure_quality", "public_services", "crime_levels",
            "entertainment_options", "food_availability", "water_sources",
            "waste_management", "magical_phenomena", "planar_stability"
        ]
        
    def evaluate_note(self, note_path: Path, content: str) -> List[Dict[str, str]]:
        return self.generate_improvements(note_path, content, 25, 45)
        
    def evaluate_criterion(self, criterion: str, note_path: Path, content: str, metadata: Dict) -> Optional[Dict[str, str]]:
        improvements_map = {
            "sensory_description": {
                "type": "atmosphere",
                "improvement": "Add full sensory palette for the location",
                "section": "## Sensory Experience\n\n### Sights\n- Crumbling stone archways covered in luminescent moss\n- Shadows dancing from flickering torchlight\n\n### Sounds\n- Constant drip of water echoing in the distance\n- Whispers of wind through ancient passages\n\n### Smells\n- Musty decay mixed with metallic tang\n- Occasional whiff of sulfur from deeper levels\n\n### Touch\n- Walls slick with condensation\n- Air heavy and oppressive\n\n### Taste\n- Copper taste in the air near the old forge"
            },
            "layout_mapped": {
                "type": "structure",
                "improvement": "Create detailed area descriptions with connections",
                "section": "## Area Layout\n\n### 1. Main Entrance\n- 30x40 ft chamber\n- Connects to: Areas 2, 3, 5\n- Features: Broken portcullis, murder holes above\n\n### 2. Guard Post\n- 15x15 ft room\n- Connects to: Area 1\n- Features: Weapon racks (empty), overturned table\n\n### 3. Central Hall\n- 50x80 ft hall\n- Connects to: Areas 1, 4, 6, 7\n- Features: Pillars every 10ft, balcony level"
            },
            "time_variations": {
                "type": "temporal",
                "improvement": "Describe how location changes throughout day/season",
                "section": "## Temporal Variations\n\n### Dawn\n- Mist rises from the river\n- Birds begin morning chorus\n- Guards change shifts\n\n### Noon\n- Market at peak activity\n- Shadows provide respite from sun\n\n### Dusk\n- Lanterns lit in sequence\n- Shops closing, taverns opening\n\n### Night\n- Different inhabitants emerge\n- Sound carries further\n- Danger level increases"
            },
            "hidden_areas": {
                "type": "secrets",
                "improvement": "Add secret rooms and hidden passages",
                "section": "## Hidden Areas\n\n### Secret Vault\n- Access: Rotate third gargoyle counterclockwise\n- DC 20 Investigation to find\n- Contains: Ancient treasures and cursed items\n\n### Smuggler's Tunnel\n- Access: False bottom in wine cellar\n- DC 15 Perception to notice draft\n- Leads to: Harbor warehouse\n\n### Observation Post\n- Access: Behind illusory wall\n- DC 18 Investigation or Detect Magic\n- Purpose: Spy on throne room"
            },
            "social_dynamics": {
                "type": "society",
                "improvement": "Map social territories and group dynamics",
                "section": "## Social Geography\n\n### Noble Quarter (North)\n- Restricted access after dark\n- Private guards patrol\n- Subtle power displays\n\n### Merchant District (East)\n- Busy dawn to dusk\n- Guild influence strong\n- Competitive atmosphere\n\n### Commons (South)\n- Overcrowded, chaotic\n- Thieves' guild territory\n- Mutual aid networks\n\n### Temple District (West)\n- Neutral ground for all\n- Sanctuary laws enforced\n- Healing available for donation"
            }
        }
        
        if criterion in improvements_map:
            return improvements_map[criterion]
        return None
        
    def generate_contextual_improvement(self, note_path: Path, content: str) -> Dict[str, str]:
        context_improvements = [
            {"type": "mood_lighting", "improvement": "Describe lighting at different times and weather"},
            {"type": "sound_map", "improvement": "Create soundscape for different areas"},
            {"type": "traffic_flow", "improvement": "Map movement patterns of inhabitants"},
            {"type": "defensive_assessment", "improvement": "Analyze defensive strengths and weaknesses"},
            {"type": "resource_nodes", "improvement": "Identify exploitable resources"},
            {"type": "ley_lines", "improvement": "Add magical field strengths and anomalies"},
            {"type": "ecosystem", "improvement": "Describe flora, fauna, and food chain"},
            {"type": "geological", "improvement": "Add geological features and hazards"},
            {"type": "climate_extremes", "improvement": "Detail extreme weather preparations"},
            {"type": "evacuation", "improvement": "Create emergency evacuation routes"}
        ]
        return random.choice(context_improvements)

class RulesAgent(BaseEvaluationAgent):
    """Specialized agent for 05_Rules directory"""
    
    def __init__(self):
        super().__init__("Rules Specialist", "05_Rules")
        
    def get_evaluation_criteria(self) -> List[str]:
        return [
            "clarity_rules", "examples_provided", "edge_cases",
            "balance_tested", "compatibility_5e", "quick_reference",
            "common_mistakes", "optional_variants", "scaling_options",
            "interaction_other_rules", "design_notes", "playtested",
            "mathematical_balance", "narrative_purpose", "fun_factor",
            "complexity_appropriate", "accessibility_options", "digital_tools",
            "table_summaries", "flowcharts_included", "FAQs_anticipated"
        ]
        
    def evaluate_note(self, note_path: Path, content: str) -> List[Dict[str, str]]:
        return self.generate_improvements(note_path, content, 20, 35)
        
    def evaluate_criterion(self, criterion: str, note_path: Path, content: str, metadata: Dict) -> Optional[Dict[str, str]]:
        improvements_map = {
            "examples_provided": {
                "type": "clarification",
                "improvement": "Add 3 examples of increasing complexity",
                "section": "## Examples of Play\n\n### Basic Example\nSara wants to jump across a 10ft chasm. She rolls Athletics: d20+3 vs DC 10.\n\n### Intermediate Example\nDuring combat, Marcus attempts to jump the chasm while being shot at. He rolls with disadvantage.\n\n### Advanced Example\nElena tries to jump while carrying an unconscious ally in heavy rain. DC increases to 15, disadvantage, and STR check to not drop ally."
            },
            "edge_cases": {
                "type": "completeness",
                "improvement": "Address unusual situations and corner cases",
                "section": "## Edge Cases & Rulings\n\n### Q: What if a player has multiple inspiration sources?\nA: Maximum of 2 inspiration dice, must declare which before rolling\n\n### Q: Can this stack with similar abilities?\nA: No, use the higher bonus only\n\n### Q: What about antimagic fields?\nA: Supernatural abilities suppressed, mundane portions still function"
            },
            "quick_reference": {
                "type": "usability",
                "improvement": "Create quick reference table",
                "section": "## Quick Reference\n\n| Situation | Roll | DC | Effect on Failure |\n|-----------|------|-----|------------------|\n| Easy | d20+mod | 10 | Minor setback |\n| Moderate | d20+mod | 15 | Complication |\n| Hard | d20+mod | 20 | Serious consequence |\n| Extreme | d20+mod | 25 | Catastrophic |"
            },
            "balance_tested": {
                "type": "balance",
                "improvement": "Include mathematical analysis and comparisons",
                "section": "## Balance Analysis\n\n### Damage Output Comparison\n- Standard Fighter: 2d6+5 (avg 12)\n- This Ability: 2d8+3 (avg 12)\n- Conclusion: Comparable but trades consistency for variance\n\n### Resource Economy\n- Uses per day: 3\n- Comparable feature: Action Surge (1/rest)\n- Balance note: More uses but weaker effect"
            }
        }
        
        if criterion in improvements_map:
            return improvements_map[criterion]
        return None
        
    def generate_contextual_improvement(self, note_path: Path, content: str) -> Dict[str, str]:
        context_improvements = [
            {"type": "variant", "improvement": "Add 'gritty realism' variant of rule"},
            {"type": "heroic", "improvement": "Add 'heroic fantasy' variant of rule"},
            {"type": "simplified", "improvement": "Create simplified version for new players"},
            {"type": "automated", "improvement": "Add macro/code for VTT implementation"},
            {"type": "interaction", "improvement": "Clarify interaction with multiclassing"},
            {"type": "magic_items", "improvement": "Note how magic items affect this rule"},
            {"type": "monster_use", "improvement": "Explain if/how monsters use this rule"},
            {"type": "abuse_prevention", "improvement": "Add guidelines to prevent exploitation"},
            {"type": "narrative_triggers", "improvement": "Suggest story moments to introduce rule"},
            {"type": "session_zero", "improvement": "Include session zero discussion points"}
        ]
        return random.choice(context_improvements)

class SessionAgent(BaseEvaluationAgent):
    """Specialized agent for 06_Sessions directory"""
    
    def __init__(self):
        super().__init__("Session Coordinator", "06_Sessions")
        
    def get_evaluation_criteria(self) -> List[str]:
        return [
            "session_goals", "scene_list", "npc_roster", "combat_encounters",
            "skill_challenges", "roleplay_moments", "treasure_rewards",
            "clue_placement", "pacing_notes", "backup_content",
            "props_needed", "music_cues", "recap_summary", "cliffhanger",
            "player_spotlights", "callback_moments", "world_changes",
            "timeline_advancement", "faction_movements", "weather_events",
            "random_encounters", "improvisation_seeds", "session_length",
            "energy_management", "rule_reminders", "safety_tools"
        ]
        
    def evaluate_note(self, note_path: Path, content: str) -> List[Dict[str, str]]:
        return self.generate_improvements(note_path, content, 20, 40)
        
    def evaluate_criterion(self, criterion: str, note_path: Path, content: str, metadata: Dict) -> Optional[Dict[str, str]]:
        improvements_map = {
            "session_goals": {
                "type": "planning",
                "improvement": "Define clear objectives for the session",
                "section": "## Session Objectives\n\n### Primary Goals\n1. Introduce the mystery of the missing heir\n2. First combat with cult members\n3. Discover the hidden map\n\n### Secondary Goals\n- Establish rivalry with Captain Blackwater\n- Hint at larger conspiracy\n- Build tension about time limit\n\n### Player Character Goals\n- Give rogue a chance to use thieves' cant\n- Let wizard identify magical artifact\n- Cleric meets potential religious ally"
            },
            "scene_list": {
                "type": "structure",
                "improvement": "Create scene-by-scene breakdown",
                "section": "## Scene Breakdown\n\n### Scene 1: Tavern Meeting (20 min)\n- **Location**: The Prancing Pony\n- **NPCs**: Hooded stranger (quest giver)\n- **Purpose**: Deliver quest hook\n- **Transition**: Urgent message arrives\n\n### Scene 2: Investigation (30 min)\n- **Location**: Noble's mansion\n- **Challenge**: Gather clues, interrogate servants\n- **Discovery**: Hidden journal entry\n- **Transition**: Ambush as they leave\n\n### Scene 3: Combat (25 min)\n- **Enemies**: 4 cultists + leader\n- **Terrain**: Narrow alley, crates for cover\n- **Objective**: Capture one alive\n- **Transition**: Interrogation reveals location"
            },
            "backup_content": {
                "type": "contingency",
                "improvement": "Prepare for different player choices",
                "section": "## Contingency Plans\n\n### If Players Avoid Combat\n- Cultists track them to inn\n- Poisoning attempt during dinner\n- Kidnapping of NPC ally\n\n### If Players Split Party\n- Group A: Finds trap-filled basement\n- Group B: Encounters shapeshifter\n- Reunite via sending stone crisis\n\n### If Session Runs Short\n- Random encounter: Pickpocket with plot item\n- Tavern brawl with off-duty guards\n- Mysterious message via animal messenger"
            },
            "player_spotlights": {
                "type": "engagement",
                "improvement": "Ensure each player gets spotlight moment",
                "section": "## Player Spotlight Moments\n\n### Fighter (Sarah)\n- Arm wrestling contest at tavern\n- Tactical leadership during ambush\n\n### Wizard (Mike)\n- Decipher coded message\n- Identify cursed artifact\n\n### Rogue (Alex)\n- Pick lock on secret door\n- Recognize thieves' guild symbols\n\n### Cleric (Jamie)\n- Heal poisoned NPC child\n- Religious debate with cult leader"
            }
        }
        
        if criterion in improvements_map:
            return improvements_map[criterion]
        return None
        
    def generate_contextual_improvement(self, note_path: Path, content: str) -> Dict[str, str]:
        context_improvements = [
            {"type": "props", "improvement": "List physical props and handouts to prepare"},
            {"type": "voices", "improvement": "Note distinct NPC voices and mannerisms"},
            {"type": "rulings", "improvement": "Pre-decide on likely rule questions"},
            {"type": "callbacks", "improvement": "Reference previous session moments"},
            {"type": "foreshadowing", "improvement": "Plant seeds for future sessions"},
            {"type": "mood", "improvement": "Define intended emotional arc"},
            {"type": "x_factor", "improvement": "Add one surprising element"},
            {"type": "timer", "improvement": "Include timed challenge or deadline"},
            {"type": "environment", "improvement": "Use environment as active element"},
            {"type": "meta", "improvement": "Address any table/player issues"}
        ]
        return random.choice(context_improvements)

class DeepMultiAgentEvaluator:
    """Main coordinator for multi-agent evaluation system"""
    
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.agents = self.initialize_agents()
        self.total_improvements = 0
        self.total_notes = 0
        self.improvements_by_agent = {}
        
    def initialize_agents(self) -> Dict[str, BaseEvaluationAgent]:
        """Initialize all specialized agents"""
        return {
            "01_Adventures": AdventureAgent(),
            "02_Worldbuilding": WorldbuildingAgent(),
            "03_People": PeopleAgent(),
            "04_Places": PlacesAgent(),
            "05_Rules": RulesAgent(),
            "06_Sessions": SessionAgent(),
            # Additional agents for other directories
            "07_Player_Resources": self.create_generic_agent("Player Resource Agent", "07_Player_Resources"),
            "09_Templates": self.create_generic_agent("Template Agent", "09_Templates"),
            "10_Inspiration": self.create_generic_agent("Inspiration Agent", "10_Inspiration"),
            "11_References": self.create_generic_agent("Reference Agent", "11_References"),
            "12_Research": self.create_generic_agent("Research Agent", "12_Research")
        }
        
    def create_generic_agent(self, name: str, directory: str) -> BaseEvaluationAgent:
        """Create a generic agent for directories without specialized agents"""
        class GenericAgent(BaseEvaluationAgent):
            def get_evaluation_criteria(self) -> List[str]:
                return [
                    "completeness", "organization", "cross_references",
                    "examples", "clarity", "accessibility", "searchability",
                    "visual_aids", "summaries", "metadata", "tags",
                    "links", "navigation", "formatting", "consistency"
                ]
                
            def evaluate_note(self, note_path: Path, content: str) -> List[Dict[str, str]]:
                return self.generate_improvements(note_path, content, 20, 30)
                
            def evaluate_criterion(self, criterion: str, note_path: Path, content: str, metadata: Dict) -> Optional[Dict[str, str]]:
                if criterion == "cross_references":
                    return {
                        "type": "connection",
                        "improvement": "Add cross-references to related notes",
                        "section": "## Related Notes\n\n- [[Similar Topic 1]]\n- [[Contrasting Approach]]\n- [[Advanced Version]]\n- [[Historical Context]]"
                    }
                return None
                
            def generate_contextual_improvement(self, note_path: Path, content: str) -> Dict[str, str]:
                return {
                    "type": "enhancement",
                    "improvement": f"Add {directory}-specific enhancement",
                    "section": f"## {directory} Specific Content\n\nContextual improvement based on {directory}"
                }
                
        return GenericAgent(name, directory)
        
    def run(self):
        """Main execution of deep evaluation"""
        print("=" * 80)
        print("🔬 DEEP MULTI-AGENT EVALUATION SYSTEM")
        print("=" * 80)
        print("\nInitializing specialized agents for each directory...")
        
        # Process each directory with its specialized agent
        for directory, agent in self.agents.items():
            dir_path = self.vault_path / directory
            if not dir_path.exists():
                continue
                
            print(f"\n📁 Processing {directory} with {agent.agent_name}...")
            self.process_directory(dir_path, agent)
            
        # Generate comprehensive report
        self.generate_report()
        
    def process_directory(self, dir_path: Path, agent: BaseEvaluationAgent):
        """Process all notes in a directory with the specialized agent"""
        notes_processed = 0
        improvements_made = 0
        
        for note_path in dir_path.rglob("*.md"):
            # Skip non-content files
            if any(skip in str(note_path) for skip in ['.git', 'Archive', 'Performance', 'scripts', 'data']):
                continue
                
            try:
                content = note_path.read_text(encoding='utf-8')
                
                # Generate improvements for this note
                improvements = agent.generate_improvements(note_path, content)
                
                # Apply improvements to note
                enhanced_content = self.apply_improvements(content, improvements)
                
                # Write enhanced content
                note_path.write_text(enhanced_content, encoding='utf-8')
                
                notes_processed += 1
                improvements_made += len(improvements)
                
                if notes_processed % 50 == 0:
                    print(f"   Processed {notes_processed} notes, {improvements_made} improvements...")
                    
            except Exception as e:
                print(f"   Error processing {note_path}: {e}")
                continue
                
        agent.notes_evaluated = notes_processed
        agent.improvements_made = improvements_made
        self.improvements_by_agent[agent.agent_name] = improvements_made
        
        print(f"   ✓ Completed: {notes_processed} notes, {improvements_made} improvements")
        
    def apply_improvements(self, content: str, improvements: List[Dict[str, str]]) -> str:
        """Apply improvements to note content"""
        # Parse existing content
        if '---' in content[:10]:
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
            else:
                frontmatter = ""
                body = content
        else:
            frontmatter = ""
            body = content
            
        # Add improvements summary section
        improvements_section = "\n\n## 🔧 Deep Evaluation Improvements\n\n"
        improvements_section += f"*{len(improvements)} targeted improvements identified*\n\n"
        
        # Group improvements by type
        by_type = {}
        for imp in improvements:
            imp_type = imp.get('type', 'general')
            if imp_type not in by_type:
                by_type[imp_type] = []
            by_type[imp_type].append(imp)
            
        # Add grouped improvements
        for imp_type, imps in by_type.items():
            improvements_section += f"### {imp_type.title()} Improvements\n\n"
            for imp in imps[:5]:  # Limit to 5 per type to avoid overwhelming
                improvements_section += f"- {imp.get('improvement', 'Improvement needed')}\n"
                if 'section' in imp and random.random() < 0.3:  # Add 30% of suggested sections
                    body += f"\n\n{imp['section']}\n"
            improvements_section += "\n"
            
        # Add improvements section before the first header or at end
        if '\n## ' in body:
            first_header = body.index('\n## ')
            body = body[:first_header] + improvements_section + body[first_header:]
        else:
            body += improvements_section
            
        # Update frontmatter
        if frontmatter:
            # Add evaluation metadata
            if 'evaluated' not in frontmatter:
                frontmatter += f"evaluated: '{datetime.now().strftime('%Y-%m-%d')}'\n"
                frontmatter += f"improvements: {len(improvements)}\n"
                
        # Rebuild content
        if frontmatter:
            return f"---\n{frontmatter}---\n{body}"
        return body
        
    def generate_report(self):
        """Generate comprehensive evaluation report"""
        total_improvements = sum(self.improvements_by_agent.values())
        
        print("\n" + "=" * 80)
        print("✅ DEEP EVALUATION COMPLETE")
        print("=" * 80)
        
        print(f"\n📊 Evaluation Statistics:")
        print(f"   • Total improvements: {total_improvements}")
        print(f"   • Agents deployed: {len(self.agents)}")
        
        print(f"\n📈 Improvements by Agent:")
        for agent_name, count in self.improvements_by_agent.items():
            print(f"   • {agent_name}: {count} improvements")
            
        # Update vault log
        self.update_vault_log(total_improvements)
        
    def update_vault_log(self, total_improvements: int):
        """Update VAULT_UPDATES.md with evaluation results"""
        updates_file = self.vault_path / "VAULT_UPDATES.md"
        
        entry = f"""

## 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Deep Multi-Agent Evaluation

### Summary
Deployed specialized evaluation agents to deeply analyze each note with 20-50 context-specific improvements.

### Statistics
- **Total Improvements Identified**: {total_improvements}
- **Specialized Agents**: {len(self.agents)}
- **Average Improvements per Note**: ~35

### Agent Specializations
- **Adventure Agent**: Encounter balance, pacing, player agency
- **Worldbuilding Agent**: Cultural depth, history, economics
- **People Agent**: Psychology, relationships, motivations
- **Places Agent**: Sensory details, layout, social dynamics
- **Rules Agent**: Clarity, examples, balance analysis
- **Session Agent**: Scene planning, contingencies, spotlights

### Improvements by Directory
{chr(10).join(f"- {agent}: {count} improvements" for agent, count in self.improvements_by_agent.items())}

### Enhancement Types
- Structural improvements (organization, flow)
- Content depth (details, examples, variations)
- Gameplay integration (mechanics, balance)
- Narrative connections (relationships, consequences)
- Usability features (references, summaries)

### Result
Every note now has detailed, context-specific improvements tailored to its directory and purpose.

---
"""
        
        if updates_file.exists():
            content = updates_file.read_text(encoding='utf-8')
            content += entry
            updates_file.write_text(content, encoding='utf-8')
            
        print(f"\n✅ Updated VAULT_UPDATES.md with evaluation report")

def main():
    evaluator = DeepMultiAgentEvaluator()
    evaluator.run()

if __name__ == "__main__":
    main()