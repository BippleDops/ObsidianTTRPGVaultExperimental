#!/usr/bin/env python3
"""
Political Intrigue Web Generator
Sprint 4 - Procedural Power Feature #1

Generates dynamic conspiracy networks and faction relationships with data structures
that enhance campaign immersion. Builds on existing vault factions and NPCs.

Tracks:
- Faction relationship matrices
- Conspiracy network structures  
- Political influence webs
- Secret knowledge propagation
- Power broker relationships
- Blackmail networks
- Information flow patterns
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from common import (
    list_markdown_files, read_file, write_file, split_frontmatter,
    build_frontmatter, merge_frontmatter, ROOT_DIR, ensure_dirs
)

class RelationshipType(Enum):
    ALLY = "ally"
    ENEMY = "enemy" 
    NEUTRAL = "neutral"
    SUSPICIOUS = "suspicious"
    BLACKMAIL = "blackmail"
    PATRON = "patron"
    PUPPET = "puppet"
    RIVAL = "rival"
    SECRET_ALLY = "secret_ally"
    DOUBLE_AGENT = "double_agent"

class PowerLevel(Enum):
    SUPREME = 5    # Deep Mother, Crystal Queen
    HIGH = 4       # Parliament Leaders, Admirals
    MODERATE = 3   # Senators, Guild Masters
    LOW = 2        # Merchants, Minor Officials
    MINIMAL = 1    # Citizens, Workers

class SecrecyLevel(Enum):
    PUBLIC = 1        # Known to all
    RUMORED = 2       # Whispered about
    SUSPECTED = 3     # Only hints remain
    CLASSIFIED = 4    # Need inside access
    VOID_SECRET = 5   # Deep Mother level secrets

@dataclass
class PoliticalEntity:
    """A person, faction, or organization with political influence"""
    name: str
    entity_type: str  # "NPC", "Faction", "Organization"
    power_level: PowerLevel
    world: str  # "Aquabyssos", "Aethermoor", "Both"
    public_position: str
    hidden_agendas: List[str]
    resources: List[str]
    vulnerabilities: List[str]
    file_path: Optional[str] = None

@dataclass
class Relationship:
    """Connection between two political entities"""
    entity1: str
    entity2: str
    relationship_type: RelationshipType
    strength: int  # 1-10
    secrecy_level: SecrecyLevel
    established_date: str
    key_events: List[str]
    leverage_points: List[str]

@dataclass  
class Conspiracy:
    """A secret plan or network"""
    name: str
    description: str
    leader: str
    members: List[str]
    goals: List[str]
    methods: List[str]
    assets: List[str]
    opposition: List[str]
    timeline: Dict[str, str]
    secrecy_level: SecrecyLevel
    success_probability: int  # 1-100

@dataclass
class PowerBroker:
    """Someone who facilitates connections and trades influence"""
    name: str
    specialization: str  # "Information", "Blackmail", "Resources", "Access"
    network_size: int
    reputation: int  # 1-10
    prices: Dict[str, str]  # service_type: price
    clients: List[str]
    secrets: List[str]

class PoliticalIntrigueWeb:
    """Main system for tracking political relationships and conspiracies"""
    
    def __init__(self, vault_root: str = ROOT_DIR):
        self.vault_root = vault_root
        self.entities: Dict[str, PoliticalEntity] = {}
        self.relationships: List[Relationship] = []
        self.conspiracies: Dict[str, Conspiracy] = {}
        self.power_brokers: Dict[str, PowerBroker] = {}
        self.knowledge_graph: Dict[str, Dict[str, Any]] = {}
        
        # Load existing data
        self._scan_existing_entities()
        self._load_persisted_data()
    
    def _scan_existing_entities(self):
        """Scan vault for existing NPCs and factions to build entity database"""
        markdown_files = list_markdown_files(self.vault_root)
        
        for file_path in markdown_files:
            try:
                content = read_file(file_path)
                frontmatter, body = split_frontmatter(content)
                
                entity_type = frontmatter.get('type')
                if entity_type in ['NPC', 'Group', 'Faction']:
                    self._extract_political_entity(file_path, frontmatter, body)
                    
            except Exception as e:
                continue  # Skip malformed files
    
    def _extract_political_entity(self, file_path: str, frontmatter: Dict, body: str):
        """Extract political data from existing vault entities"""
        name = frontmatter.get('name') or os.path.splitext(os.path.basename(file_path))[0]
        
        # Determine power level from context clues
        power_level = self._infer_power_level(name, frontmatter, body)
        
        # Extract hidden information
        hidden_agendas = self._extract_agendas(body)
        resources = self._extract_resources(body)
        vulnerabilities = self._extract_vulnerabilities(body)
        
        entity = PoliticalEntity(
            name=name,
            entity_type=frontmatter.get('type', 'Unknown'),
            power_level=power_level,
            world=frontmatter.get('world', 'Both'),
            public_position=self._extract_position(body),
            hidden_agendas=hidden_agendas,
            resources=resources,
            vulnerabilities=vulnerabilities,
            file_path=file_path
        )
        
        self.entities[name] = entity
    
    def _infer_power_level(self, name: str, frontmatter: Dict, body: str) -> PowerLevel:
        """Infer power level from titles, positions, and context"""
        name_lower = name.lower()
        body_lower = body.lower()
        
        # Supreme level indicators
        if any(term in name_lower for term in ['queen', 'emperor', 'deep mother']):
            return PowerLevel.SUPREME
        
        # High level indicators  
        if any(term in name_lower for term in ['admiral', 'chancellor', 'archon', 'prime']):
            return PowerLevel.HIGH
        
        if any(term in body_lower for term in ['parliament', 'senate', 'council']):
            return PowerLevel.HIGH
            
        # Moderate level indicators
        if any(term in name_lower for term in ['senator', 'guild master', 'captain']):
            return PowerLevel.MODERATE
            
        # Low level indicators
        if any(term in name_lower for term in ['merchant', 'clerk', 'assistant']):
            return PowerLevel.LOW
            
        return PowerLevel.MINIMAL
    
    def _extract_agendas(self, body: str) -> List[str]:
        """Extract hidden agendas from entity descriptions"""
        agendas = []
        
        # Look for agenda indicators
        agenda_markers = [
            'secret goal', 'hidden agenda', 'true purpose', 'real intention',
            'secretly', 'privately', 'covertly', 'behind closed doors'
        ]
        
        lines = body.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(marker in line_lower for marker in agenda_markers):
                agendas.append(line.strip('- ').strip())
                
        return agendas[:3]  # Limit to most important
    
    def _extract_resources(self, body: str) -> List[str]:
        """Extract resources and assets from descriptions"""
        resources = []
        resource_indicators = [
            'wealth', 'money', 'gold', 'influence', 'connections',
            'network', 'army', 'fleet', 'magic', 'artifacts'
        ]
        
        lines = body.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in resource_indicators):
                resources.append(line.strip('- ').strip())
                
        return resources[:5]  # Reasonable limit
    
    def _extract_vulnerabilities(self, body: str) -> List[str]:
        """Extract weaknesses and vulnerabilities"""
        vulnerabilities = []
        vuln_indicators = [
            'weakness', 'vulnerable', 'fear', 'afraid', 'secret',
            'blackmail', 'leverage', 'flaw', 'addiction', 'debt'
        ]
        
        lines = body.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in vuln_indicators):
                vulnerabilities.append(line.strip('- ').strip())
                
        return vulnerabilities[:3]
    
    def _extract_position(self, body: str) -> str:
        """Extract public position or role"""
        lines = body.split('\n')[:10]  # Check first 10 lines
        for line in lines:
            if 'position:' in line.lower():
                return line.split(':')[1].strip()
            if 'role:' in line.lower():
                return line.split(':')[1].strip()
                
        return "Unknown Position"
    
    def _generate_conspiracy_methods(self, seed: str, members: List[PoliticalEntity]) -> List[str]:
        """Generate methods for conspiracy operations"""
        base_methods = [
            'Information gathering and surveillance',
            'Political pressure and blackmail',  
            'Economic manipulation',
            'Social influence campaigns',
            'Strategic alliance building',
            'Targeted recruitment',
            'Resource acquisition',
            'Opposition neutralization'
        ]
        
        # Add methods based on member capabilities
        enhanced_methods = base_methods.copy()
        
        for member in members:
            if 'military' in member.resources or 'Military' in member.public_position:
                enhanced_methods.append('Military coordination')
            if 'merchant' in member.resources or 'Trade' in member.resources:
                enhanced_methods.append('Trade route manipulation')
            if 'magical' in member.resources or 'Arcane' in member.public_position:
                enhanced_methods.append('Magical surveillance and influence')
                
        return enhanced_methods[:6]  # Return top 6 methods


    def generate_conspiracy_network(self, seed_entity: str, network_size: int = 5) -> Conspiracy:
        """Generate a conspiracy network around a seed entity"""
        if seed_entity not in self.entities:
            return None
            
        seed = self.entities[seed_entity]
        
        # Select conspiracy members based on power levels and worlds
        potential_members = [
            name for name, entity in self.entities.items()
            if entity.world == seed.world or entity.world == "Both"
            and entity.power_level.value >= 2  # Exclude minimal power
            and name != seed_entity
        ]
        
        members = random.sample(
            potential_members, 
            min(network_size, len(potential_members))
        )
        
        # Generate conspiracy details
        conspiracy_name = self._generate_conspiracy_name(seed)
        goals = self._generate_conspiracy_goals(seed, members)
        methods = self._generate_conspiracy_methods(seed, members)
        
        conspiracy = Conspiracy(
            name=conspiracy_name,
            description=f"A secretive network led by {seed_entity}",
            leader=seed_entity,
            members=members,
            goals=goals,
            methods=methods,
            assets=seed.resources + self._aggregate_member_assets(members),
            opposition=self._identify_opposition(seed, members),
            timeline=self._generate_timeline(),
            secrecy_level=self._determine_secrecy_level(seed),
            success_probability=self._calculate_success_probability(seed, members)
        )
        
        self.conspiracies[conspiracy_name] = conspiracy
        return conspiracy
    
    def _generate_conspiracy_name(self, seed: PoliticalEntity) -> str:
        """Generate evocative conspiracy names"""
        prefixes = [
            "The Circle of", "The Order of", "The Alliance of", "The Covenant of",
            "The Shadow", "The Silent", "The Hidden", "The Crimson", "The Azure"
        ]
        
        suffixes = [
            "Depths", "Currents", "Tides", "Winds", "Storms", "Stars",
            "Echoes", "Whispers", "Secrets", "Truth", "Power", "Unity"
        ]
        
        if seed.world == "Aquabyssos":
            suffixes.extend(["Pearls", "Trenches", "Abyss", "Pressure"])
        else:
            suffixes.extend(["Clouds", "Heights", "Crystals", "Winds"])
            
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"
    
    def _generate_conspiracy_goals(self, seed: PoliticalEntity, members: List[str]) -> List[str]:
        """Generate realistic conspiracy goals"""
        goals = []
        
        # Base on seed entity's agendas
        goals.extend(seed.hidden_agendas)
        
        # Add contextual goals based on world and power level
        if seed.world == "Aquabyssos":
            potential_goals = [
                "Gain control of Parliament voting",
                "Manipulate crystal trade routes", 
                "Infiltrate the Shadow Conspiracy",
                "Discover Deep Mother secrets",
                "Control memory extraction technology"
            ]
        else:  # Aethermoor
            potential_goals = [
                "Control wind current navigation",
                "Monopolize crystal mining operations",
                "Influence Queen Seraphina's decisions",
                "Establish sky trade dominance",
                "Access ancient Skyforge technology"
            ]
            
        # Add power-appropriate goals
        if seed.power_level.value >= 4:
            potential_goals.extend([
                "Reshape governmental structure",
                "Control inter-world relations",
                "Access reality-altering artifacts"
            ])
        
        goals.extend(random.sample(potential_goals, min(3, len(potential_goals))))
        return goals[:5]  # Limit to 5 goals
    
    def generate_relationship_matrix(self, entity_names: List[str] = None) -> Dict[str, Dict[str, Relationship]]:
        """Generate relationship matrix between entities"""
        if not entity_names:
            # Focus on high-power entities for core matrix
            entity_names = [
                name for name, entity in self.entities.items()
                if entity.power_level.value >= 3
            ][:20]  # Limit to prevent explosion
        
        matrix = {}
        
        for i, entity1 in enumerate(entity_names):
            matrix[entity1] = {}
            for entity2 in entity_names[i+1:]:
                relationship = self._generate_relationship(entity1, entity2)
                if relationship:
                    matrix[entity1][entity2] = relationship
                    
                    # Add reverse relationship
                    if entity2 not in matrix:
                        matrix[entity2] = {}
                    matrix[entity2][entity1] = self._create_reverse_relationship(relationship)
        
        return matrix
    
    def _generate_relationship(self, entity1: str, entity2: str) -> Optional[Relationship]:
        """Generate a relationship between two entities"""
        if entity1 not in self.entities or entity2 not in self.entities:
            return None
            
        e1 = self.entities[entity1]
        e2 = self.entities[entity2]
        
        # Don't create relationships between different worlds unless "Both"
        if e1.world != e2.world and e1.world != "Both" and e2.world != "Both":
            return None
        
        # Determine relationship type based on context
        rel_type = self._determine_relationship_type(e1, e2)
        strength = random.randint(3, 8)  # Moderate to strong relationships
        secrecy = self._determine_secrecy(e1, e2, rel_type)
        
        # Generate relationship history
        established_date = self._generate_past_date()
        key_events = self._generate_relationship_events(e1, e2, rel_type)
        leverage_points = self._identify_leverage_points(e1, e2)
        
        return Relationship(
            entity1=entity1,
            entity2=entity2,
            relationship_type=rel_type,
            strength=strength,
            secrecy_level=secrecy,
            established_date=established_date,
            key_events=key_events,
            leverage_points=leverage_points
        )
    
    def _determine_relationship_type(self, e1: PoliticalEntity, e2: PoliticalEntity) -> RelationshipType:
        """Determine relationship type based on entity characteristics"""
        
        # Shadow Conspiracy gets special treatment
        if "shadow" in e1.name.lower() or "shadow" in e2.name.lower():
            return RelationshipType.SECRET_ALLY if random.random() < 0.3 else RelationshipType.ENEMY
        
        # Power dynamics
        power_diff = abs(e1.power_level.value - e2.power_level.value)
        if power_diff >= 2:
            return RelationshipType.PATRON if e1.power_level.value > e2.power_level.value else RelationshipType.PUPPET
        
        # Same world entities more likely to interact
        if e1.world == e2.world:
            return random.choice([
                RelationshipType.ALLY, RelationshipType.RIVAL,
                RelationshipType.NEUTRAL, RelationshipType.SUSPICIOUS
            ])
        
        # Cross-world relationships tend to be formal
        return random.choice([
            RelationshipType.NEUTRAL, RelationshipType.ALLY, RelationshipType.SUSPICIOUS
        ])
    
    def generate_power_brokers(self, count: int = 10) -> List[PowerBroker]:
        """Generate information brokers and influence peddlers"""
        specializations = ["Information", "Blackmail", "Resources", "Access", "Assassination"]
        
        brokers = []
        for i in range(count):
            broker = PowerBroker(
                name=self._generate_broker_name(),
                specialization=random.choice(specializations),
                network_size=random.randint(5, 50),
                reputation=random.randint(3, 9),
                prices=self._generate_broker_prices(),
                clients=random.sample(list(self.entities.keys()), random.randint(3, 8)),
                secrets=self._generate_broker_secrets()
            )
            brokers.append(broker)
            self.power_brokers[broker.name] = broker
            
        return brokers
    
    def _generate_broker_name(self) -> str:
        """Generate mysterious broker names"""
        first_names = ["Whisper", "Shadow", "Silk", "Velvet", "Crystal", "Tidal", "Echo"]
        last_names = ["Smith", "Grey", "Nightfall", "Goldtounge", "Deepwatch", "Voidcaller"]
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_broker_prices(self) -> Dict[str, str]:
        """Generate broker service pricing"""
        return {
            "rumor": "50 gold",
            "secret": "500 gold or equivalent favor",
            "blackmail_material": "1000 gold + ongoing percentage",
            "introduction": "100 gold + mutual favor",
            "protection": "Variable based on threat level"
        }
    
    def _generate_broker_secrets(self) -> List[str]:
        """Generate valuable secrets brokers might know"""
        secrets = [
            "Senator Glaucus replacement date confirmed",
            "Deep Mother awakening timeline accelerated", 
            "Queen Seraphina's crystal corruption spreading",
            "Cross-world portal construction in progress",
            "Shadow Parliament voting records leaked",
            "Memory extraction facility locations mapped",
            "Reality anchor weakness discovered",
            "Ancient artifact cache location known"
        ]
        
        return random.sample(secrets, random.randint(2, 5))
    
    def generate_information_flow_map(self) -> Dict[str, Any]:
        """Map how information flows through the political network"""
        flow_map = {
            "information_hubs": [],
            "leak_sources": [],
            "disinformation_networks": [],
            "secure_channels": [],
            "compromised_channels": []
        }
        
        # Identify information hubs (high-connection entities)
        for name, entity in self.entities.items():
            connection_count = sum(1 for rel in self.relationships if name in [rel.entity1, rel.entity2])
            if connection_count >= 5:
                flow_map["information_hubs"].append({
                    "entity": name,
                    "connections": connection_count,
                    "reliability": entity.power_level.value * 20
                })
        
        # Identify leak sources (vulnerable high-power entities)
        for name, entity in self.entities.items():
            if entity.power_level.value >= 3 and entity.vulnerabilities:
                flow_map["leak_sources"].append({
                    "entity": name,
                    "vulnerability_count": len(entity.vulnerabilities),
                    "access_level": entity.power_level.value
                })
        
        return flow_map
    
    def save_system_state(self):
        """Persist the political intrigue system state"""
        ensure_dirs()
        data_dir = os.path.join(self.vault_root, "09_Performance")
        os.makedirs(data_dir, exist_ok=True)
        
        # Save entities
        entities_data = {name: asdict(entity) for name, entity in self.entities.items()}
        with open(os.path.join(data_dir, "political_entities.json"), "w") as f:
            json.dump(entities_data, f, indent=2, default=str)
        
        # Save relationships  
        relationships_data = [asdict(rel) for rel in self.relationships]
        with open(os.path.join(data_dir, "political_relationships.json"), "w") as f:
            json.dump(relationships_data, f, indent=2, default=str)
            
        # Save conspiracies
        conspiracies_data = {name: asdict(conspiracy) for name, conspiracy in self.conspiracies.items()}
        with open(os.path.join(data_dir, "conspiracies.json"), "w") as f:
            json.dump(conspiracies_data, f, indent=2, default=str)
        
        # Save power brokers
        brokers_data = {name: asdict(broker) for name, broker in self.power_brokers.items()}
        with open(os.path.join(data_dir, "power_brokers.json"), "w") as f:
            json.dump(brokers_data, f, indent=2, default=str)
    
    def _load_persisted_data(self):
        """Load previously saved system state"""
        data_dir = os.path.join(self.vault_root, "09_Performance")
        
        # Load saved data if it exists
        try:
            entities_file = os.path.join(data_dir, "political_entities.json")
            if os.path.exists(entities_file):
                with open(entities_file) as f:
                    entities_data = json.load(f)
                    # Convert back to objects (simplified for now)
                    pass
        except:
            pass  # Use generated data
    
    def create_intrigue_dashboard(self) -> str:
        """Create a comprehensive dashboard of political intrigue"""
        dashboard = []
        
        dashboard.append("# Political Intrigue Dashboard")
        dashboard.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        
        # Entity overview
        dashboard.append("## Political Entities")
        dashboard.append(f"Total entities tracked: {len(self.entities)}")
        
        by_power = {}
        for entity in self.entities.values():
            level = entity.power_level.name
            by_power[level] = by_power.get(level, 0) + 1
            
        for level, count in sorted(by_power.items(), key=lambda x: PowerLevel[x[0]].value, reverse=True):
            dashboard.append(f"- {level}: {count}")
        
        dashboard.append("")
        
        # Conspiracies overview
        dashboard.append("## Active Conspiracies")
        for name, conspiracy in self.conspiracies.items():
            dashboard.append(f"### {name}")
            dashboard.append(f"- Leader: {conspiracy.leader}")
            dashboard.append(f"- Members: {len(conspiracy.members)}")
            dashboard.append(f"- Success Probability: {conspiracy.success_probability}%")
            dashboard.append(f"- Secrecy Level: {conspiracy.secrecy_level.name}")
            dashboard.append("")
        
        # Power brokers
        dashboard.append("## Power Brokers")
        for broker in self.power_brokers.values():
            dashboard.append(f"### {broker.name}")
            dashboard.append(f"- Specialization: {broker.specialization}")
            dashboard.append(f"- Network Size: {broker.network_size}")
            dashboard.append(f"- Reputation: {broker.reputation}/10")
            dashboard.append("")
        
        return "\n".join(dashboard)
    
    def _generate_past_date(self) -> str:
        """Generate a realistic past date"""
        days_ago = random.randint(30, 1825)  # 1 month to 5 years
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d")
    
    def _generate_relationship_events(self, e1: PoliticalEntity, e2: PoliticalEntity, rel_type: RelationshipType) -> List[str]:
        """Generate key events in relationship history"""
        events = []
        
        base_events = {
            RelationshipType.ALLY: [
                f"Joint operation against common enemy",
                f"Mutual assistance during crisis",
                f"Beneficial trade agreement signed"
            ],
            RelationshipType.ENEMY: [
                f"Public confrontation in Parliament",
                f"Competing claims over territory",
                f"Betrayal during joint venture"
            ],
            RelationshipType.BLACKMAIL: [
                f"Compromising evidence obtained",
                f"Secret recorded during private meeting",
                f"Financial irregularities discovered"
            ]
        }
        
        event_pool = base_events.get(rel_type, ["Initial meeting established"])
        return random.sample(event_pool, min(2, len(event_pool)))
    
    def _identify_leverage_points(self, e1: PoliticalEntity, e2: PoliticalEntity) -> List[str]:
        """Identify mutual leverage points"""
        leverage = []
        
        # Use vulnerabilities as leverage
        leverage.extend(e1.vulnerabilities[:2])
        leverage.extend(e2.vulnerabilities[:2])
        
        # Add contextual leverage
        if e1.power_level.value > e2.power_level.value:
            leverage.append(f"{e1.name} controls resources {e2.name} needs")
        else:
            leverage.append(f"{e2.name} has access {e1.name} requires")
            
        return leverage[:3]

def main():
    """Main execution for political intrigue web generation"""
    print("Generating Political Intrigue Web...")
    
    web = PoliticalIntrigueWeb()
    
    # Generate core conspiracies  
    if "The Shadow Conspiracy" in web.entities:
        shadow_conspiracy = web.generate_conspiracy_network("The Shadow Conspiracy", 8)
        print(f"Generated conspiracy: {shadow_conspiracy.name}")
    
    # Generate relationship matrix for key entities
    relationship_matrix = web.generate_relationship_matrix()
    print(f"Generated {sum(len(relations) for relations in relationship_matrix.values())} relationships")
    
    # Generate power brokers
    brokers = web.generate_power_brokers(12)
    print(f"Generated {len(brokers)} power brokers")
    
    # Generate information flow map
    info_flow = web.generate_information_flow_map()
    print(f"Mapped information flow with {len(info_flow['information_hubs'])} hubs")
    
    # Save system state
    web.save_system_state()
    
    # Create dashboard
    dashboard_content = web.create_intrigue_dashboard()
    
    # Write dashboard to vault
    dashboard_path = os.path.join(web.vault_root, "06_GM_Resources", "Political_Intrigue_Dashboard.md")
    write_file(dashboard_path, dashboard_content)
    
    print(f"Political Intrigue Web generated successfully!")
    print(f"Dashboard saved to: Political_Intrigue_Dashboard.md")
    print(f"System data saved to: 09_Performance/")

if __name__ == "__main__":
    main()