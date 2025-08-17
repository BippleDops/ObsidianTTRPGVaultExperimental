#!/usr/bin/env python3
"""
Faction Network Analyzer
Analyzes faction relationships and power dynamics using Pydantic models.
"""

import os
import re
import json
import networkx as nx
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
from datetime import datetime

# Import our Pydantic models  
import sys
sys.path.append('../data')
from models import Faction, BaseVaultContent, WorldRealm, FactionType, ThreatLevel

class FactionNetworkAnalyzer:
    """Analyzes faction networks and power dynamics."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.factions: Dict[str, Faction] = {}
        self.power_graph = nx.DiGraph()  # Directed graph for power relationships
        self.alliance_graph = nx.Graph()  # Undirected graph for alliances
        self.conflict_graph = nx.Graph()  # Undirected graph for conflicts
        
    def extract_faction_data(self, file_path: Path) -> Optional[Faction]:
        """Extract faction data from a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            title = file_path.stem
            formal_name = title
            
            # Extract faction-specific data
            faction_type = self.determine_faction_type(content, title)
            leadership = self.extract_leadership(content)
            allies = self.extract_allies(content)
            enemies = self.extract_enemies(content)
            rivals = self.extract_rivals(content)
            core_beliefs = self.extract_beliefs(content)
            primary_goals = self.extract_goals(content)
            base_locations = self.extract_locations(content)
            
            faction = Faction(
                title=title,
                formal_name=formal_name,
                faction_type=faction_type,
                leadership=leadership,
                allies=allies,
                enemies=enemies,
                rivals=rivals,
                core_beliefs=core_beliefs,
                primary_goals=primary_goals,
                base_locations=base_locations,
                world=self.determine_world_realm(content),
                status=self.determine_status(content),
                tags=self.extract_tags(content)
            )
            
            return faction
            
        except Exception as e:
            print(f"Error processing faction file {file_path}: {e}")
            return None
            
    def determine_faction_type(self, content: str, title: str) -> FactionType:
        """Determine faction type based on content and title."""
        content_lower = content.lower()
        title_lower = title.lower()
        
        # Keywords for each faction type
        type_keywords = {
            FactionType.government: ['parliament', 'council', 'ministry', 'authority', 'administration'],
            FactionType.criminal: ['syndicate', 'conspiracy', 'shadow', 'smuggler', 'black market'],
            FactionType.academic: ['academy', 'university', 'scholar', 'research', 'institute'],
            FactionType.religious: ['temple', 'order', 'divine', 'faith', 'spiritual'],
            FactionType.merchant: ['trading', 'company', 'consortium', 'merchant', 'commerce'],
            FactionType.military: ['guard', 'navy', 'army', 'fleet', 'forces'],
            FactionType.guild: ['guild', 'artisan', 'craft', 'professional'],
            FactionType.cultural: ['cultural', 'heritage', 'tradition', 'customs'],
            FactionType.cult: ['cult', 'devoted', 'worship', 'ritual'],
            FactionType.house: ['house', 'family', 'dynasty', 'bloodline']
        }
        
        best_type = FactionType.cultural  # Default
        best_score = 0
        
        for faction_type, keywords in type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower or keyword in title_lower)
            if score > best_score:
                best_score = score
                best_type = faction_type
                
        return best_type
        
    def extract_leadership(self, content: str) -> List[str]:
        """Extract leadership figures from content."""
        leadership = []
        
        leadership_patterns = [
            r'(?:Leader|Head|Chief|Director|Chairman|President|King|Queen|Emperor|Admiral|Commander|Guildmaster):\s*(?:\[\[)?([^.\n\]]+)',
            r'led by\s+(?:\[\[)?([^.\n\]]+)',
            r'under\s+(?:\[\[)?([^.\n\]]+)\'s\s+leadership',
            r'Leadership:\s*([^.\n]+)'
        ]
        
        for pattern in leadership_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                leader = re.sub(r'\[\[|\]\]', '', match.strip())
                if leader and len(leader) < 100:  # Reasonable length check
                    leadership.append(leader)
                    
        return list(set(leadership))  # Remove duplicates
        
    def extract_allies(self, content: str) -> List[str]:
        """Extract allied factions from content."""
        allies = []
        
        ally_patterns = [
            r'(?:allies?|allied with|partners?|friends?):\s*([^.\n]+)',
            r'allied with\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)',
            r'works? with\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)',
            r'cooperation with\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)'
        ]
        
        for pattern in ally_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Split by commas and clean
                ally_list = [ally.strip() for ally in match.split(',')]
                for ally in ally_list:
                    ally = re.sub(r'\[\[|\]\]', '', ally.strip())
                    if ally and len(ally) < 100:
                        allies.append(ally)
                        
        return list(set(allies))
        
    def extract_enemies(self, content: str) -> List[str]:
        """Extract enemy factions from content."""
        enemies = []
        
        enemy_patterns = [
            r'(?:enemies|enemy|opposed to|fights?|against|hostile to):\s*([^.\n]+)',
            r'at war with\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)',
            r'conflicts? with\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)',
            r'opposes\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)'
        ]
        
        for pattern in enemy_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                enemy_list = [enemy.strip() for enemy in match.split(',')]
                for enemy in enemy_list:
                    enemy = re.sub(r'\[\[|\]\]', '', enemy.strip())
                    if enemy and len(enemy) < 100:
                        enemies.append(enemy)
                        
        return list(set(enemies))
        
    def extract_rivals(self, content: str) -> List[str]:
        """Extract rival factions from content."""
        rivals = []
        
        rival_patterns = [
            r'rivals?:\s*([^.\n]+)',
            r'competes? with\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)',
            r'rivalry with\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)',
            r'competitive relationship with\s+(?:the\s+)?(?:\[\[)?([^.\n\]]+)'
        ]
        
        for pattern in rival_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                rival_list = [rival.strip() for rival in match.split(',')]
                for rival in rival_list:
                    rival = re.sub(r'\[\[|\]\]', '', rival.strip())
                    if rival and len(rival) < 100:
                        rivals.append(rival)
                        
        return list(set(rivals))
        
    def extract_beliefs(self, content: str) -> List[str]:
        """Extract core beliefs from content."""
        beliefs = []
        
        belief_patterns = [
            r'(?:believes?|belief|ideology|principles?):\s*([^.\n]+)',
            r'core values?:\s*([^.\n]+)',
            r'dedicated to\s+([^.\n]+)',
            r'committed to\s+([^.\n]+)'
        ]
        
        for pattern in belief_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            beliefs.extend([belief.strip() for belief in matches])
            
        return list(set(beliefs))
        
    def extract_goals(self, content: str) -> List[str]:
        """Extract primary goals from content."""
        goals = []
        
        goal_patterns = [
            r'(?:goals?|objectives?|aims?):\s*([^.\n]+)',
            r'seeks? to\s+([^.\n]+)',
            r'trying to\s+([^.\n]+)',
            r'works? toward\s+([^.\n]+)'
        ]
        
        for pattern in goal_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            goals.extend([goal.strip() for goal in matches])
            
        return list(set(goals))
        
    def extract_locations(self, content: str) -> List[str]:
        """Extract base locations from content."""
        locations = []
        
        location_patterns = [
            r'(?:based|headquartered|located) (?:in|at)\s+(?:\[\[)?([^.\n\]]+)',
            r'operates? from\s+(?:\[\[)?([^.\n\]]+)',
            r'base of operations?:\s*(?:\[\[)?([^.\n\]]+)',
            r'headquarters?:\s*(?:\[\[)?([^.\n\]]+)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                location = re.sub(r'\[\[|\]\]', '', match.strip())
                if location and len(location) < 100:
                    locations.append(location)
                    
        return list(set(locations))
        
    def determine_world_realm(self, content: str) -> WorldRealm:
        """Determine faction's primary realm."""
        aquabyssos_keywords = ['aquabyssos', 'depth', 'pressure', 'abyssal', 'underwater']
        aethermoor_keywords = ['aethermoor', 'sky', 'wind', 'crystal', 'altitude']
        
        aquabyssos_score = sum(1 for keyword in aquabyssos_keywords if keyword in content.lower())
        aethermoor_score = sum(1 for keyword in aethermoor_keywords if keyword in content.lower())
        
        if aquabyssos_score > aethermoor_score:
            return WorldRealm.aquabyssos
        elif aethermoor_score > aquabyssos_score:
            return WorldRealm.aethermoor
        else:
            return WorldRealm.both
            
    def determine_status(self, content: str):
        """Determine faction development status."""
        if len(content) < 500:
            return "stub"
        elif "TODO" in content or "TBD" in content:
            return "draft"
        else:
            return "active"
            
    def extract_tags(self, content: str) -> List[str]:
        """Extract tags from content."""
        hashtag_pattern = r'#([a-zA-Z][a-zA-Z0-9_/-]*)'
        hashtags = re.findall(hashtag_pattern, content)
        return list(set(hashtags))
        
    def build_relationship_graphs(self) -> None:
        """Build NetworkX graphs for different relationship types."""
        # Add all factions as nodes
        for faction_name, faction in self.factions.items():
            node_attrs = {
                'faction_type': faction.faction_type.value,
                'world': faction.world.value,
                'leadership_count': len(faction.leadership),
                'location_count': len(faction.base_locations),
                'goal_count': len(faction.primary_goals)
            }
            
            self.power_graph.add_node(faction_name, **node_attrs)
            self.alliance_graph.add_node(faction_name, **node_attrs)
            self.conflict_graph.add_node(faction_name, **node_attrs)
            
        # Add alliance relationships
        for faction_name, faction in self.factions.items():
            for ally in faction.allies:
                if ally in self.factions:
                    self.alliance_graph.add_edge(faction_name, ally, relationship='ally')
                    
        # Add conflict relationships
        for faction_name, faction in self.factions.items():
            for enemy in faction.enemies:
                if enemy in self.factions:
                    self.conflict_graph.add_edge(faction_name, enemy, relationship='enemy')
            for rival in faction.rivals:
                if rival in self.factions:
                    self.conflict_graph.add_edge(faction_name, rival, relationship='rival')
                    
        # Add power relationships (based on faction types)
        power_hierarchy = {
            FactionType.government: 5,
            FactionType.military: 4,
            FactionType.merchant: 3,
            FactionType.guild: 2,
            FactionType.academic: 2,
            FactionType.religious: 2,
            FactionType.cultural: 1,
            FactionType.criminal: 1,
            FactionType.cult: 1,
            FactionType.house: 1
        }
        
        faction_items = list(self.factions.items())
        for i, (name1, faction1) in enumerate(faction_items):
            power1 = power_hierarchy.get(faction1.faction_type, 1)
            for name2, faction2 in faction_items[i+1:]:
                power2 = power_hierarchy.get(faction2.faction_type, 1)
                if power1 > power2:
                    self.power_graph.add_edge(name1, name2, power_difference=power1-power2)
                elif power2 > power1:
                    self.power_graph.add_edge(name2, name1, power_difference=power2-power1)
                    
    def analyze_network_metrics(self) -> Dict[str, any]:
        """Analyze network metrics and return insights."""
        analysis = {
            "total_factions": len(self.factions),
            "faction_types": Counter([f.faction_type.value for f in self.factions.values()]),
            "world_distribution": Counter([f.world.value for f in self.factions.values()]),
            "alliance_analysis": {},
            "conflict_analysis": {},
            "power_analysis": {},
            "network_clusters": []
        }
        
        # Alliance analysis
        alliance_degree = dict(self.alliance_graph.degree())
        analysis["alliance_analysis"] = {
            "total_alliances": self.alliance_graph.number_of_edges(),
            "most_allied": sorted(alliance_degree.items(), key=lambda x: x[1], reverse=True)[:5],
            "isolated_factions": [faction for faction, degree in alliance_degree.items() if degree == 0],
            "alliance_density": nx.density(self.alliance_graph)
        }
        
        # Conflict analysis
        conflict_degree = dict(self.conflict_graph.degree())
        analysis["conflict_analysis"] = {
            "total_conflicts": self.conflict_graph.number_of_edges(),
            "most_conflicted": sorted(conflict_degree.items(), key=lambda x: x[1], reverse=True)[:5],
            "peaceful_factions": [faction for faction, degree in conflict_degree.items() if degree == 0],
            "conflict_density": nx.density(self.conflict_graph)
        }
        
        # Power analysis
        power_centrality = nx.in_degree_centrality(self.power_graph)
        analysis["power_analysis"] = {
            "most_powerful": sorted(power_centrality.items(), key=lambda x: x[1], reverse=True)[:5],
            "power_concentration": max(power_centrality.values()) if power_centrality else 0
        }
        
        # Network clusters (communities)
        if self.alliance_graph.number_of_edges() > 0:
            try:
                communities = nx.community.greedy_modularity_communities(self.alliance_graph)
                analysis["network_clusters"] = [list(community) for community in communities]
            except:
                analysis["network_clusters"] = []
                
        return analysis
        
    def generate_faction_report(self, faction_name: str) -> Dict[str, any]:
        """Generate detailed report for specific faction."""
        if faction_name not in self.factions:
            return {"error": "Faction not found"}
            
        faction = self.factions[faction_name]
        
        report = {
            "faction": faction.dict(),
            "network_position": {
                "alliance_connections": len(list(self.alliance_graph.neighbors(faction_name))),
                "conflict_connections": len(list(self.conflict_graph.neighbors(faction_name))),
                "allies": list(self.alliance_graph.neighbors(faction_name)),
                "conflicts": list(self.conflict_graph.neighbors(faction_name))
            },
            "influence_analysis": {},
            "strategic_assessment": []
        }
        
        # Influence analysis
        if faction_name in self.alliance_graph:
            report["influence_analysis"] = {
                "alliance_centrality": nx.degree_centrality(self.alliance_graph)[faction_name],
                "betweenness_centrality": nx.betweenness_centrality(self.alliance_graph)[faction_name],
                "clustering_coefficient": nx.clustering(self.alliance_graph, faction_name)
            }
            
        # Strategic assessment
        assessments = []
        if len(faction.allies) > len(faction.enemies):
            assessments.append("Strong alliance network")
        if len(faction.enemies) > len(faction.allies):
            assessments.append("High conflict involvement")
        if faction.world == WorldRealm.both:
            assessments.append("Cross-realm influence")
        if len(faction.base_locations) > 1:
            assessments.append("Multi-location presence")
            
        report["strategic_assessment"] = assessments
        
        return report
        
    def load_factions(self) -> None:
        """Load all faction files from vault."""
        faction_files = []
        
        # Look in Groups directory for faction files
        groups_path = self.vault_path / "02_Worldbuilding" / "Groups"
        if groups_path.exists():
            faction_files.extend(groups_path.rglob('*.md'))
            
        print(f"Found {len(faction_files)} potential faction files")
        
        for file_path in faction_files:
            # Skip obviously non-faction files
            filename = file_path.name.lower()
            if any(skip in filename for skip in ['index', 'template', 'guide', 'master']):
                continue
                
            faction = self.extract_faction_data(file_path)
            if faction:
                self.factions[faction.formal_name] = faction
                
        print(f"Loaded {len(self.factions)} factions")
        
    def export_results(self, output_dir: str) -> None:
        """Export analysis results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export faction data
        faction_data = {name: faction.dict() for name, faction in self.factions.items()}
        with open(output_path / 'factions.json', 'w') as f:
            json.dump(faction_data, f, indent=2, default=str)
            
        # Export network analysis
        analysis = self.analyze_network_metrics()
        with open(output_path / 'faction_network_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
            
        # Export graph data
        alliance_data = nx.node_link_data(self.alliance_graph)
        with open(output_path / 'alliance_network.json', 'w') as f:
            json.dump(alliance_data, f, indent=2, default=str)
            
        conflict_data = nx.node_link_data(self.conflict_graph)
        with open(output_path / 'conflict_network.json', 'w') as f:
            json.dump(conflict_data, f, indent=2, default=str)
            
        print(f"Results exported to {output_path}")
        
def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze faction networks in Cordelia vault")
    parser.add_argument("vault_path", help="Path to vault directory")
    parser.add_argument("--output", "-o", help="Output directory for results", default="faction_analysis")
    parser.add_argument("--faction", "-f", help="Generate report for specific faction")
    
    args = parser.parse_args()
    
    analyzer = FactionNetworkAnalyzer(args.vault_path)
    
    print("Loading factions...")
    analyzer.load_factions()
    
    print("Building relationship graphs...")
    analyzer.build_relationship_graphs()
    
    if args.faction:
        report = analyzer.generate_faction_report(args.faction)
        print(f"Faction Report for {args.faction}:")
        print(json.dumps(report, indent=2, default=str))
    else:
        analysis = analyzer.analyze_network_metrics()
        print("Faction Network Analysis:")
        print(f"Total factions: {analysis['total_factions']}")
        print(f"Total alliances: {analysis['alliance_analysis']['total_alliances']}")
        print(f"Total conflicts: {analysis['conflict_analysis']['total_conflicts']}")
        print(f"Most allied: {analysis['alliance_analysis']['most_allied'][:3]}")
        
        analyzer.export_results(args.output)
        
if __name__ == "__main__":
    main()