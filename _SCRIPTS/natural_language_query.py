#!/usr/bin/env python3
"""
Natural Language Query System - Sprint 1 MVI
Enable searches like "find all NPCs who oppose the queen"
"""

import os
import re
import json
import argparse
from typing import Dict, List, Any, Optional, Set
from common import (
    list_markdown_files, read_file, split_frontmatter, 
    ROOT_DIR, save_json, load_json
)

class NaturalLanguageQueryEngine:
    def __init__(self, vault_path: str = None):
        self.vault_path = vault_path or ROOT_DIR
        self.query_patterns = {
            # Pattern: (regex, handler_method)
            'find_by_type_and_relation': (
                r"find all (\w+)s? (?:who|that) (.+)",
                self._find_by_type_and_relation
            ),
            'find_by_type': (
                r"find all (\w+)s?",
                self._find_by_type
            ),
            'search_content': (
                r"search for (.+)",
                self._search_content
            ),
            'find_locations_in': (
                r"find locations in (.+)",
                self._find_locations_in
            ),
            'find_groups_with': (
                r"find groups with (.+)",
                self._find_groups_with
            )
        }
        self._index_cache = None
        
    def _build_content_index(self) -> Dict[str, Any]:
        """Build searchable index of vault content"""
        if self._index_cache:
            return self._index_cache
            
        index = {
            'files': {},
            'by_type': {'npc': [], 'location': [], 'group': [], 'lore': [], 'item': []},
            'content_search': {}
        }
        
        for file_path in list_markdown_files(self.vault_path):
            try:
                content = read_file(file_path)
                frontmatter, body = split_frontmatter(content)
                
                file_info = {
                    'path': file_path,
                    'title': os.path.splitext(os.path.basename(file_path))[0],
                    'frontmatter': frontmatter,
                    'body': body.lower(),  # for case-insensitive search
                    'content_full': content.lower()
                }
                
                # Index by file
                index['files'][file_path] = file_info
                
                # Index by type
                entity_type = frontmatter.get('type', '').lower()
                if entity_type in index['by_type']:
                    index['by_type'][entity_type].append(file_info)
                
                # Content search index (keywords)
                keywords = self._extract_keywords(body)
                index['content_search'][file_path] = keywords
                
            except Exception as e:
                print(f"Error indexing {file_path}: {e}")
                continue
        
        self._index_cache = index
        return index
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract searchable keywords from text"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        return {word for word in words if len(word) > 2 and word not in stopwords}
    
    def parse_and_execute(self, query: str) -> List[Dict[str, Any]]:
        """Parse natural language query and return results"""
        query = query.lower().strip()
        
        for pattern_name, (regex, handler) in self.query_patterns.items():
            match = re.match(regex, query, re.IGNORECASE)
            if match:
                return handler(match.groups())
        
        # Fallback to general search
        return self._general_search(query)
    
    def _find_by_type_and_relation(self, groups: tuple) -> List[Dict[str, Any]]:
        """Find entities of type that match relation (e.g., 'NPCs who oppose the queen')"""
        entity_type, relation = groups
        entity_type = entity_type.lower()
        
        # Map common type variations
        type_mapping = {
            'npc': 'npc', 'character': 'npc', 'person': 'npc',
            'location': 'location', 'place': 'location',
            'group': 'group', 'organization': 'group', 'faction': 'group'
        }
        
        mapped_type = type_mapping.get(entity_type, entity_type)
        index = self._build_content_index()
        
        results = []
        entities = index['by_type'].get(mapped_type, [])
        
        for entity in entities:
            # Check if relation matches in content
            if self._matches_relation(entity, relation):
                results.append({
                    'title': entity['title'],
                    'path': entity['path'],
                    'type': entity['frontmatter'].get('type', 'Unknown'),
                    'relevance_reason': f"Contains: {relation}",
                    'world': entity['frontmatter'].get('world', 'Unknown')
                })
        
        return results
    
    def _find_by_type(self, groups: tuple) -> List[Dict[str, Any]]:
        """Find all entities of specific type"""
        entity_type = groups[0].lower()
        
        type_mapping = {
            'npc': 'npc', 'character': 'npc', 'person': 'npc',
            'location': 'location', 'place': 'location',
            'group': 'group', 'organization': 'group', 'faction': 'group'
        }
        
        mapped_type = type_mapping.get(entity_type, entity_type)
        index = self._build_content_index()
        
        results = []
        entities = index['by_type'].get(mapped_type, [])
        
        for entity in entities:
            results.append({
                'title': entity['title'],
                'path': entity['path'],
                'type': entity['frontmatter'].get('type', 'Unknown'),
                'world': entity['frontmatter'].get('world', 'Unknown'),
                'status': entity['frontmatter'].get('status', 'Unknown')
            })
        
        return results
    
    def _search_content(self, groups: tuple) -> List[Dict[str, Any]]:
        """Search for specific content across all files"""
        search_term = groups[0].lower()
        index = self._build_content_index()
        
        results = []
        for file_path, file_info in index['files'].items():
            if search_term in file_info['content_full']:
                # Find context around the match
                context = self._get_context(file_info['content_full'], search_term)
                results.append({
                    'title': file_info['title'],
                    'path': file_path,
                    'type': file_info['frontmatter'].get('type', 'Unknown'),
                    'context': context,
                    'world': file_info['frontmatter'].get('world', 'Unknown')
                })
        
        return results
    
    def _find_locations_in(self, groups: tuple) -> List[Dict[str, Any]]:
        """Find locations within a specific area/world"""
        area = groups[0].lower()
        index = self._build_content_index()
        
        results = []
        locations = index['by_type'].get('location', [])
        
        for location in locations:
            if (area in location['content_full'] or 
                area in location['frontmatter'].get('world', '').lower()):
                results.append({
                    'title': location['title'],
                    'path': location['path'],
                    'type': 'Location',
                    'world': location['frontmatter'].get('world', 'Unknown'),
                    'relevance_reason': f"Located in {area}"
                })
        
        return results
    
    def _find_groups_with(self, groups: tuple) -> List[Dict[str, Any]]:
        """Find groups with specific characteristics"""
        characteristic = groups[0].lower()
        index = self._build_content_index()
        
        results = []
        groups_list = index['by_type'].get('group', [])
        
        for group in groups_list:
            if self._matches_characteristic(group, characteristic):
                results.append({
                    'title': group['title'],
                    'path': group['path'],
                    'type': 'Group',
                    'world': group['frontmatter'].get('world', 'Unknown'),
                    'relevance_reason': f"Has characteristic: {characteristic}"
                })
        
        return results
    
    def _matches_relation(self, entity: Dict[str, Any], relation: str) -> bool:
        """Check if entity matches the relation description"""
        relation_keywords = relation.split()
        content = entity['content_full']
        
        # Look for key relationship indicators
        if 'oppose' in relation or 'against' in relation:
            return any(keyword in content for keyword in ['oppose', 'against', 'enemy', 'rebel', 'revolt'])
        if 'support' in relation or 'ally' in relation:
            return any(keyword in content for keyword in ['support', 'ally', 'loyal', 'friend'])
        if 'serve' in relation:
            return any(keyword in content for keyword in ['serve', 'servant', 'work for', 'employee'])
        
        # General keyword matching
        return any(keyword in content for keyword in relation_keywords)
    
    def _matches_characteristic(self, entity: Dict[str, Any], characteristic: str) -> bool:
        """Check if entity has specific characteristic"""
        return characteristic in entity['content_full']
    
    def _get_context(self, content: str, search_term: str, context_chars: int = 100) -> str:
        """Get context around search term"""
        pos = content.lower().find(search_term.lower())
        if pos == -1:
            return ""
        
        start = max(0, pos - context_chars)
        end = min(len(content), pos + len(search_term) + context_chars)
        
        return "..." + content[start:end] + "..."
    
    def _general_search(self, query: str) -> List[Dict[str, Any]]:
        """Fallback general search"""
        return self._search_content((query,))

def main():
    parser = argparse.ArgumentParser(description='Natural Language Query System')
    parser.add_argument('query', help='Natural language query')
    parser.add_argument('--format', choices=['json', 'simple'], default='simple',
                       help='Output format')
    
    args = parser.parse_args()
    
    engine = NaturalLanguageQueryEngine()
    results = engine.parse_and_execute(args.query)
    
    if args.format == 'json':
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print("No results found.")
        else:
            print(f"\nFound {len(results)} result(s) for: '{args.query}'\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['title']} ({result['type']})")
                print(f"   Path: {result['path']}")
                print(f"   World: {result.get('world', 'Unknown')}")
                if 'relevance_reason' in result:
                    print(f"   Reason: {result['relevance_reason']}")
                if 'context' in result:
                    print(f"   Context: {result['context']}")
                print()

if __name__ == "__main__":
    main()