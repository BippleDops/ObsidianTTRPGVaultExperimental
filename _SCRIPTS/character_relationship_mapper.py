#!/usr/bin/env python3
"""
Character Relationship Mapper
Analyzes and visualizes character relationships using Pydantic models.
"""

import os
import re
import json
import networkx as nx
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter

# Import our Pydantic models  
import sys
sys.path.append('../data')
from models import Character, BaseVaultContent, WorldRealm, ContentType

class CharacterRelationshipMapper:
    """Maps and analyzes character relationships across the vault."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.characters: Dict[str, Character] = {}
        self.relationships: Dict[str, Dict[str, str]] = defaultdict(dict)
        self.co_occurrences: Dict[str, Dict[str, int]] = defaultdict(Counter)
        self.graph = nx.Graph()
        
    def extract_character_data(self, file_path: Path) -> Character:
        """Extract character data from a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract title from filename if no frontmatter title
            title = file_path.stem
            
            # Look for character-specific patterns
            full_name = title
            aliases = self.extract_aliases(content)
            factions = self.extract_factions(content)
            relationships = self.extract_explicit_relationships(content)
            
            # Create Character model
            character = Character(
                title=title,
                full_name=full_name,
                aliases=aliases,
                factions=factions,
                relationships=relationships,
                world=self.determine_world_realm(content),
                status=self.determine_status(content),
                tags=self.extract_tags(content)
            )
            
            return character
            
        except Exception as e:
            print(f"Error processing character file {file_path}: {e}")
            return None
            
    def extract_aliases(self, content: str) -> List[str]:
        """Extract character aliases from content."""
        aliases = []
        
        # Look for "also known as", "aka", "called" patterns
        alias_patterns = [
            r'(?:also known as|aka|called|known as)\s+([^.\n]+)',
            r'Aliases?:\s*([^.\n]+)',
            r'Names?:\s*([^.\n]+)'
        ]
        
        for pattern in alias_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Split by commas and clean up
                alias_list = [alias.strip() for alias in match.split(',')]
                aliases.extend(alias_list)
                
        return list(set(aliases))  # Remove duplicates
        
    def extract_factions(self, content: str) -> List[str]:
        """Extract faction affiliations from content."""
        factions = []
        
        # Look for faction mentions
        faction_patterns = [
            r'\[\[([^]]+(?:Guild|Academy|Order|Parliament|Conspiracy|Syndicate|Brotherhood|Company)[^]]*)\]\]',
            r'member of\s+(?:the\s+)?([^.\n]+)',
            r'affiliated with\s+(?:the\s+)?([^.\n]+)',
            r'works for\s+(?:the\s+)?([^.\n]+)'
        ]
        
        for pattern in faction_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            factions.extend(matches)
            
        return list(set(factions))  # Remove duplicates
        
    def extract_explicit_relationships(self, content: str) -> Dict[str, str]:
        """Extract explicit relationship declarations."""
        relationships = {}
        
        # Look for relationship patterns
        relationship_patterns = [
            r'([A-Z][a-zA-Z\s]+) (?:is|was) (?:his|her|their) ([a-z\s]+)',
            r'Relationship with \[\[([^]]+)\]\]: ([^.\n]+)',
            r'([A-Z][a-zA-Z\s]+) - ([^.\n]+relationship[^.\n]*)'
        ]
        
        for pattern in relationship_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) == 2:
                    character_name = match[0].strip()
                    relationship_type = match[1].strip()
                    relationships[character_name] = relationship_type
                    
        return relationships
        
    def determine_world_realm(self, content: str) -> WorldRealm:
        """Determine character's primary realm based on content."""
        aquabyssos_keywords = ['depth', 'pressure', 'abyssal', 'coral', 'submarine']
        aethermoor_keywords = ['altitude', 'wind', 'crystal', 'sky', 'airship']
        
        aquabyssos_score = sum(1 for keyword in aquabyssos_keywords if keyword in content.lower())
        aethermoor_score = sum(1 for keyword in aethermoor_keywords if keyword in content.lower())
        
        if aquabyssos_score > aethermoor_score:
            return WorldRealm.aquabyssos
        elif aethermoor_score > aquabyssos_score:
            return WorldRealm.aethermoor
        else:
            return WorldRealm.both
            
    def determine_status(self, content: str):
        """Determine character development status."""
        if len(content) < 500:
            return "stub"
        elif "TODO" in content or "TBD" in content:
            return "draft"
        else:
            return "active"
            
    def extract_tags(self, content: str) -> List[str]:
        """Extract tags from content."""
        tags = []
        
        # Look for hashtags
        hashtag_pattern = r'#([a-zA-Z][a-zA-Z0-9_/-]*)'
        hashtags = re.findall(hashtag_pattern, content)
        tags.extend(hashtags)
        
        return list(set(tags))
        
    def find_co_occurrences(self) -> None:
        """Find character co-occurrences in files."""
        character_names = set(self.characters.keys())
        
        # Search through all files for character mentions
        for file_path in self.vault_path.rglob('*.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find all character names mentioned in this file
                mentioned_chars = set()
                for char_name in character_names:
                    # Look for exact name or in wikilinks
                    if char_name in content or f"[[{char_name}]]" in content:
                        mentioned_chars.add(char_name)
                        
                # Record co-occurrences
                mentioned_list = list(mentioned_chars)
                for i, char1 in enumerate(mentioned_list):
                    for char2 in mentioned_list[i+1:]:
                        self.co_occurrences[char1][char2] += 1
                        self.co_occurrences[char2][char1] += 1
                        
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                
    def build_relationship_graph(self) -> None:
        """Build NetworkX graph of character relationships."""
        # Add all characters as nodes
        for char_name, character in self.characters.items():
            self.graph.add_node(char_name, **character.dict())
            
        # Add explicit relationship edges
        for char1, relationships in self.relationships.items():
            for char2, relationship_type in relationships.items():
                if char2 in self.characters:
                    self.graph.add_edge(char1, char2, 
                                      relationship=relationship_type, 
                                      type="explicit")
                                      
        # Add co-occurrence edges
        for char1, co_occur_dict in self.co_occurrences.items():
            for char2, count in co_occur_dict.items():
                if count >= 2:  # Only if mentioned together multiple times
                    if not self.graph.has_edge(char1, char2):
                        self.graph.add_edge(char1, char2, 
                                          co_occurrences=count, 
                                          type="co_occurrence")
                    else:
                        self.graph[char1][char2]['co_occurrences'] = count
                        
    def analyze_relationships(self) -> Dict[str, any]:
        """Analyze relationship patterns and return insights."""
        analysis = {
            "total_characters": len(self.characters),
            "total_relationships": self.graph.number_of_edges(),
            "most_connected_characters": [],
            "faction_clusters": {},
            "cross_realm_relationships": 0,
            "relationship_types": Counter(),
            "orphaned_characters": []
        }
        
        # Most connected characters
        degree_centrality = nx.degree_centrality(self.graph)
        sorted_by_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
        analysis["most_connected_characters"] = sorted_by_degree[:10]
        
        # Faction clustering
        faction_chars = defaultdict(list)
        for char_name, character in self.characters.items():
            for faction in character.factions:
                faction_chars[faction].append(char_name)
        analysis["faction_clusters"] = dict(faction_chars)
        
        # Cross-realm relationships
        for char1, char2 in self.graph.edges():
            world1 = self.characters[char1].world
            world2 = self.characters[char2].world
            if world1 != world2 and world1 != WorldRealm.both and world2 != WorldRealm.both:
                analysis["cross_realm_relationships"] += 1
                
        # Relationship types
        for char1, char2, data in self.graph.edges(data=True):
            if 'relationship' in data:
                analysis["relationship_types"][data['relationship']] += 1
                
        # Orphaned characters (no connections)
        analysis["orphaned_characters"] = [char for char in self.characters.keys() 
                                         if self.graph.degree(char) == 0]
        
        return analysis
        
    def generate_character_report(self, character_name: str) -> Dict[str, any]:
        """Generate detailed report for specific character."""
        if character_name not in self.characters:
            return {"error": "Character not found"}
            
        character = self.characters[character_name]
        neighbors = list(self.graph.neighbors(character_name))
        
        report = {
            "character": character.dict(),
            "direct_connections": len(neighbors),
            "connected_characters": [],
            "faction_connections": [],
            "cross_realm_connections": []
        }
        
        # Analyze connections
        for neighbor in neighbors:
            edge_data = self.graph[character_name][neighbor]
            neighbor_char = self.characters[neighbor]
            
            connection_info = {
                "name": neighbor,
                "relationship": edge_data.get('relationship', 'unknown'),
                "co_occurrences": edge_data.get('co_occurrences', 0),
                "world": neighbor_char.world.value,
                "factions": neighbor_char.factions
            }
            report["connected_characters"].append(connection_info)
            
            # Check for cross-realm connections
            if character.world != neighbor_char.world and character.world != WorldRealm.both and neighbor_char.world != WorldRealm.both:
                report["cross_realm_connections"].append(neighbor)
                
        # Faction connections
        for faction in character.factions:
            faction_members = [char for char, c in self.characters.items() 
                             if faction in c.factions and char != character_name]
            report["faction_connections"].extend(faction_members)
            
        return report
        
    def load_characters(self) -> None:
        """Load all character files from vault."""
        character_files = []
        
        # Look in Groups and Lore directories for character files
        search_paths = [
            self.vault_path / "02_Worldbuilding" / "Groups",
            self.vault_path / "02_Worldbuilding" / "Lore"
        ]
        
        for search_path in search_paths:
            if search_path.exists():
                character_files.extend(search_path.rglob('*.md'))
                
        print(f"Found {len(character_files)} potential character files")
        
        for file_path in character_files:
            # Skip files that are clearly not characters
            filename = file_path.name.lower()
            if any(skip in filename for skip in ['index', 'template', 'guide']):
                continue
                
            character = self.extract_character_data(file_path)
            if character:
                self.characters[character.full_name] = character
                
        print(f"Loaded {len(self.characters)} characters")
        
    def export_results(self, output_dir: str) -> None:
        """Export analysis results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export character data
        character_data = {name: char.dict() for name, char in self.characters.items()}
        with open(output_path / 'characters.json', 'w') as f:
            json.dump(character_data, f, indent=2, default=str)
            
        # Export relationship analysis
        analysis = self.analyze_relationships()
        with open(output_path / 'relationship_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
            
        # Export graph data
        graph_data = nx.node_link_data(self.graph)
        with open(output_path / 'relationship_graph.json', 'w') as f:
            json.dump(graph_data, f, indent=2, default=str)
            
        print(f"Results exported to {output_path}")
        
def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Map character relationships in Cordelia vault")
    parser.add_argument("vault_path", help="Path to vault directory")
    parser.add_argument("--output", "-o", help="Output directory for results", default="character_analysis")
    parser.add_argument("--character", "-c", help="Generate report for specific character")
    
    args = parser.parse_args()
    
    mapper = CharacterRelationshipMapper(args.vault_path)
    
    print("Loading characters...")
    mapper.load_characters()
    
    print("Finding co-occurrences...")
    mapper.find_co_occurrences()
    
    print("Building relationship graph...")
    mapper.build_relationship_graph()
    
    if args.character:
        report = mapper.generate_character_report(args.character)
        print(f"Character Report for {args.character}:")
        print(json.dumps(report, indent=2, default=str))
    else:
        analysis = mapper.analyze_relationships()
        print("Relationship Analysis:")
        print(f"Total characters: {analysis['total_characters']}")
        print(f"Total relationships: {analysis['total_relationships']}")
        print(f"Cross-realm relationships: {analysis['cross_realm_relationships']}")
        print(f"Most connected: {analysis['most_connected_characters'][:5]}")
        
        mapper.export_results(args.output)
        
if __name__ == "__main__":
    main()