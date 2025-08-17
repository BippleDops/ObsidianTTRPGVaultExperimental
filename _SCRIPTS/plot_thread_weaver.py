#!/usr/bin/env python3
"""
Plot Thread Weaver - Sprint 3 Intelligence Layer Feature

This system analyzes campaign content to identify narrative patterns, plot threads,
and story connections. It suggests links between content, identifies narrative gaps,
and helps GMs weave cohesive storylines.

Features:
- Analyze content for plot patterns and themes
- Identify connection opportunities between NPCs, locations, and events
- Detect narrative gaps and unresolved plot threads
- Suggest story development opportunities
- Generate plot thread maps and story arc visualizations
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import argparse
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import glob

# Set up paths
VAULT_ROOT = Path(__file__).parent.parent
PLOT_DATA_DIR = VAULT_ROOT / "scripts" / "plot_data"
PLOT_DATA_DIR.mkdir(exist_ok=True)

@dataclass
class PlotElement:
    """Represents a plot element (character, location, event, etc.)"""
    name: str
    element_type: str  # npc, location, event, faction, item, concept
    file_path: str
    content_snippet: str
    tags: List[str] = field(default_factory=list)
    connections: List[str] = field(default_factory=list)
    first_mentioned: str = ""
    last_referenced: str = ""
    importance_score: float = 0.0
    narrative_role: str = ""  # protagonist, antagonist, catalyst, background, etc.

@dataclass
class PlotThread:
    """Represents a narrative thread or story arc"""
    thread_id: str
    title: str
    description: str
    elements: List[PlotElement] = field(default_factory=list)
    status: str = "active"  # active, resolved, abandoned, potential
    complexity: int = 1  # 1-5 scale
    last_development: str = ""
    resolution_potential: float = 0.0
    narrative_gaps: List[str] = field(default_factory=list)

@dataclass
class StoryConnection:
    """Represents a potential or existing connection between plot elements"""
    element1: str
    element2: str
    connection_type: str  # conflict, alliance, mystery, cause-effect, etc.
    strength: float  # 0.0-1.0
    evidence: List[str] = field(default_factory=list)
    suggested_development: str = ""
    file_references: List[str] = field(default_factory=list)

class PlotThreadWeaver:
    """Main system for analyzing and weaving plot threads"""
    
    def __init__(self):
        self.elements_file = PLOT_DATA_DIR / "plot_elements.json"
        self.threads_file = PLOT_DATA_DIR / "plot_threads.json"
        self.connections_file = PLOT_DATA_DIR / "story_connections.json"
        self.analysis_cache = PLOT_DATA_DIR / "analysis_cache.json"
        
        # Load existing data
        self.plot_elements = self._load_elements()
        self.plot_threads = self._load_threads()
        self.connections = self._load_connections()
        self.cache = self._load_cache()
        
        # Analysis patterns
        self.conflict_patterns = [
            r'oppose[sd]?', r'enemy', r'rival', r'conflict', r'tension', r'hostil',
            r'against', r'rebel', r'resist', r'fight', r'battle', r'war'
        ]
        
        self.alliance_patterns = [
            r'ally', r'friend', r'support', r'help', r'assist', r'cooper',
            r'partner', r'alliance', r'united', r'together', r'join'
        ]
        
        self.mystery_patterns = [
            r'secret', r'hidden', r'mystery', r'unknown', r'discover', r'reveal',
            r'investigate', r'clue', r'evidence', r'suspicious', r'conspiracy'
        ]
        
        self.power_patterns = [
            r'crown', r'throne', r'rule', r'govern', r'command', r'control',
            r'power', r'authority', r'influence', r'leader', r'king', r'queen'
        ]
        
    def _load_elements(self) -> Dict[str, PlotElement]:
        """Load plot elements from file"""
        if not self.elements_file.exists():
            return {}
        
        with open(self.elements_file, 'r') as f:
            data = json.load(f)
        
        elements = {}
        for name, elem_data in data.items():
            element = PlotElement(
                name=elem_data['name'],
                element_type=elem_data['element_type'],
                file_path=elem_data['file_path'],
                content_snippet=elem_data['content_snippet'],
                tags=elem_data.get('tags', []),
                connections=elem_data.get('connections', []),
                first_mentioned=elem_data.get('first_mentioned', ''),
                last_referenced=elem_data.get('last_referenced', ''),
                importance_score=elem_data.get('importance_score', 0.0),
                narrative_role=elem_data.get('narrative_role', '')
            )
            elements[name] = element
        
        return elements
    
    def _save_elements(self):
        """Save plot elements to file"""
        data = {}
        for name, element in self.plot_elements.items():
            data[name] = {
                'name': element.name,
                'element_type': element.element_type,
                'file_path': element.file_path,
                'content_snippet': element.content_snippet,
                'tags': element.tags,
                'connections': element.connections,
                'first_mentioned': element.first_mentioned,
                'last_referenced': element.last_referenced,
                'importance_score': element.importance_score,
                'narrative_role': element.narrative_role
            }
        
        with open(self.elements_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_threads(self) -> Dict[str, PlotThread]:
        """Load plot threads from file"""
        if not self.threads_file.exists():
            return {}
        
        with open(self.threads_file, 'r') as f:
            data = json.load(f)
        
        threads = {}
        for thread_id, thread_data in data.items():
            thread = PlotThread(
                thread_id=thread_data['thread_id'],
                title=thread_data['title'],
                description=thread_data['description'],
                elements=[self.plot_elements.get(e, None) for e in thread_data.get('element_names', [])],
                status=thread_data.get('status', 'active'),
                complexity=thread_data.get('complexity', 1),
                last_development=thread_data.get('last_development', ''),
                resolution_potential=thread_data.get('resolution_potential', 0.0),
                narrative_gaps=thread_data.get('narrative_gaps', [])
            )
            # Filter out None elements
            thread.elements = [e for e in thread.elements if e is not None]
            threads[thread_id] = thread
        
        return threads
    
    def _save_threads(self):
        """Save plot threads to file"""
        data = {}
        for thread_id, thread in self.plot_threads.items():
            data[thread_id] = {
                'thread_id': thread.thread_id,
                'title': thread.title,
                'description': thread.description,
                'element_names': [e.name for e in thread.elements],
                'status': thread.status,
                'complexity': thread.complexity,
                'last_development': thread.last_development,
                'resolution_potential': thread.resolution_potential,
                'narrative_gaps': thread.narrative_gaps
            }
        
        with open(self.threads_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_connections(self) -> List[StoryConnection]:
        """Load story connections from file"""
        if not self.connections_file.exists():
            return []
        
        with open(self.connections_file, 'r') as f:
            data = json.load(f)
        
        connections = []
        for conn_data in data:
            connection = StoryConnection(
                element1=conn_data['element1'],
                element2=conn_data['element2'],
                connection_type=conn_data['connection_type'],
                strength=conn_data['strength'],
                evidence=conn_data.get('evidence', []),
                suggested_development=conn_data.get('suggested_development', ''),
                file_references=conn_data.get('file_references', [])
            )
            connections.append(connection)
        
        return connections
    
    def _save_connections(self):
        """Save story connections to file"""
        data = []
        for connection in self.connections:
            conn_data = {
                'element1': connection.element1,
                'element2': connection.element2,
                'connection_type': connection.connection_type,
                'strength': connection.strength,
                'evidence': connection.evidence,
                'suggested_development': connection.suggested_development,
                'file_references': connection.file_references
            }
            data.append(conn_data)
        
        with open(self.connections_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_cache(self) -> Dict:
        """Load analysis cache"""
        if not self.analysis_cache.exists():
            return {'last_full_analysis': '', 'file_checksums': {}}
        
        with open(self.analysis_cache, 'r') as f:
            return json.load(f)
    
    def _save_cache(self):
        """Save analysis cache"""
        with open(self.analysis_cache, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def scan_vault_content(self, force_rescan: bool = False) -> bool:
        """Scan vault content for plot elements"""
        print("🔍 Scanning vault for plot elements...")
        
        # Get all markdown files
        content_dirs = [
            VAULT_ROOT / "02_Worldbuilding",
            VAULT_ROOT / "01_Adventures", 
            VAULT_ROOT / "1-Session Journals"
        ]
        
        files_found = []
        for content_dir in content_dirs:
            if content_dir.exists():
                files_found.extend(content_dir.rglob("*.md"))
        
        print(f"Found {len(files_found)} content files")
        
        # Process each file
        new_elements = 0
        updated_elements = 0
        
        for file_path in files_found:
            if self._should_skip_file(file_path):
                continue
                
            element = self._extract_plot_element(file_path)
            if element:
                if element.name not in self.plot_elements:
                    new_elements += 1
                else:
                    updated_elements += 1
                self.plot_elements[element.name] = element
        
        # Save updates
        self._save_elements()
        self.cache['last_full_analysis'] = datetime.now().isoformat()
        self._save_cache()
        
        print(f"✅ Scan complete: {new_elements} new elements, {updated_elements} updated")
        return True
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during analysis"""
        skip_patterns = [
            'backup', '.backup', 'archive', 'template', 'README',
            'index', 'hub', 'report', 'log'
        ]
        
        file_str = str(file_path).lower()
        return any(pattern in file_str for pattern in skip_patterns)
    
    def _extract_plot_element(self, file_path: Path) -> Optional[PlotElement]:
        """Extract plot element from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return None
        
        if len(content.strip()) < 50:  # Skip very short files
            return None
        
        # Extract title/name
        name = self._extract_name_from_content(content, file_path)
        if not name:
            return None
        
        # Determine element type
        element_type = self._classify_element_type(file_path, content)
        
        # Extract snippet
        snippet = self._extract_content_snippet(content)
        
        # Extract tags and metadata
        tags = self._extract_tags(content)
        
        # Find connections
        connections = self._find_connections_in_content(content)
        
        # Calculate importance score
        importance = self._calculate_importance_score(content, file_path)
        
        # Determine narrative role
        narrative_role = self._determine_narrative_role(content)
        
        element = PlotElement(
            name=name,
            element_type=element_type,
            file_path=str(file_path.relative_to(VAULT_ROOT)),
            content_snippet=snippet,
            tags=tags,
            connections=connections,
            first_mentioned=datetime.now().isoformat(),
            last_referenced=datetime.now().isoformat(),
            importance_score=importance,
            narrative_role=narrative_role
        )
        
        return element
    
    def _extract_name_from_content(self, content: str, file_path: Path) -> str:
        """Extract the primary name/title from content"""
        # Try to get from first heading
        heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if heading_match:
            return heading_match.group(1).strip()
        
        # Fall back to filename
        name = file_path.stem
        # Clean up filename
        name = re.sub(r'^\d+[_-]?', '', name)  # Remove leading numbers
        name = re.sub(r'[_-]', ' ', name)  # Replace underscores/dashes with spaces
        return name.strip()
    
    def _classify_element_type(self, file_path: Path, content: str) -> str:
        """Classify the type of plot element"""
        path_str = str(file_path).lower()
        content_lower = content.lower()
        
        if 'people' in path_str or 'npc' in path_str:
            return 'npc'
        elif 'places' in path_str or 'location' in path_str:
            return 'location' 
        elif 'groups' in path_str or 'faction' in path_str:
            return 'faction'
        elif 'items' in path_str or 'artifact' in path_str:
            return 'item'
        elif 'adventures' in path_str or 'session' in path_str:
            return 'event'
        elif any(word in content_lower for word in ['concept', 'philosophy', 'principle', 'theory']):
            return 'concept'
        else:
            return 'lore'
    
    def _extract_content_snippet(self, content: str, max_length: int = 200) -> str:
        """Extract a meaningful snippet from content"""
        # Remove markdown formatting
        cleaned = re.sub(r'^---[\s\S]*?---', '', content)  # Remove frontmatter
        cleaned = re.sub(r'#+ ', '', cleaned)  # Remove headers
        cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned)  # Remove links
        cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)  # Remove bold
        cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)  # Remove italic
        cleaned = re.sub(r'\n+', ' ', cleaned)  # Replace newlines with spaces
        
        # Get first meaningful sentence
        sentences = re.split(r'[.!?]+', cleaned)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and not re.match(r'^\s*$', sentence):
                return sentence[:max_length].strip() + ('...' if len(sentence) > max_length else '')
        
        # Fallback to first chunk
        return cleaned[:max_length].strip() + ('...' if len(cleaned) > max_length else '')
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content"""
        tags = []
        
        # From frontmatter
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            fm_content = frontmatter_match.group(1)
            tag_match = re.search(r'^tags:\s*\n((?:^[-\s]*\w+.*\n?)*)', fm_content, re.MULTILINE)
            if tag_match:
                tag_lines = tag_match.group(1)
                for line in tag_lines.split('\n'):
                    line = line.strip()
                    if line.startswith('-'):
                        tag = line[1:].strip()
                        if tag:
                            tags.append(tag)
        
        # Infer from content patterns
        content_lower = content.lower()
        if any(pattern in content_lower for pattern in ['shadow', 'conspiracy', 'secret']):
            tags.append('intrigue')
        if any(pattern in content_lower for pattern in ['magic', 'crystal', 'power']):
            tags.append('magical')
        if any(pattern in content_lower for pattern in ['political', 'parliament', 'government']):
            tags.append('political')
        if any(pattern in content_lower for pattern in ['combat', 'battle', 'fight']):
            tags.append('conflict')
        
        return list(set(tags))
    
    def _find_connections_in_content(self, content: str) -> List[str]:
        """Find references to other elements in content"""
        connections = []
        
        # Find wikilinks [[Name]]
        wikilink_pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(wikilink_pattern, content)
        for match in matches:
            # Clean up the link
            clean_name = match.split('|')[0]  # Remove alias if present
            clean_name = clean_name.strip()
            if clean_name:
                connections.append(clean_name)
        
        return list(set(connections))
    
    def _calculate_importance_score(self, content: str, file_path: Path) -> float:
        """Calculate importance score for element"""
        score = 0.0
        
        # Base score from content length
        score += min(len(content) / 1000, 2.0)
        
        # Bonus for being in important directories
        path_str = str(file_path).lower()
        if 'adventures' in path_str:
            score += 2.0
        elif 'people' in path_str:
            score += 1.5
        elif 'groups' in path_str:
            score += 1.0
        
        # Bonus for royal/important titles
        content_lower = content.lower()
        if any(title in content_lower for title in ['queen', 'king', 'emperor', 'ruler']):
            score += 3.0
        elif any(title in content_lower for title in ['commander', 'admiral', 'leader']):
            score += 2.0
        elif any(title in content_lower for title in ['ambassador', 'minister', 'council']):
            score += 1.5
        
        # Bonus for frequency indicators
        if content.count('[[') > 10:  # Many connections
            score += 1.0
        
        return min(score, 10.0)  # Cap at 10
    
    def _determine_narrative_role(self, content: str) -> str:
        """Determine the narrative role of an element"""
        content_lower = content.lower()
        
        # Check for antagonist patterns
        if any(re.search(pattern, content_lower) for pattern in self.conflict_patterns):
            if any(word in content_lower for word in ['evil', 'corrupt', 'enemy', 'villain']):
                return 'antagonist'
        
        # Check for protagonist patterns
        if any(word in content_lower for word in ['hero', 'champion', 'savior', 'protector']):
            return 'protagonist'
        
        # Check for authority figures
        if any(word in content_lower for word in ['queen', 'king', 'ruler', 'leader', 'commander']):
            return 'authority'
        
        # Check for catalysts
        if any(word in content_lower for word in ['catalyst', 'trigger', 'cause', 'mysterious']):
            return 'catalyst'
        
        # Check for supporters
        if any(re.search(pattern, content_lower) for pattern in self.alliance_patterns):
            return 'ally'
        
        return 'background'
    
    def analyze_plot_threads(self) -> List[PlotThread]:
        """Analyze content to identify plot threads"""
        print("🧵 Analyzing plot threads...")
        
        # Group elements by common themes
        theme_groups = self._group_elements_by_theme()
        
        # Convert theme groups to plot threads
        threads = []
        for theme, elements in theme_groups.items():
            if len(elements) >= 2:  # Need at least 2 elements for a thread
                thread_id = f"thread_{theme.lower().replace(' ', '_')}"
                thread = self._create_plot_thread(thread_id, theme, elements)
                threads.append(thread)
                self.plot_threads[thread_id] = thread
        
        # Save threads
        self._save_threads()
        
        print(f"✅ Identified {len(threads)} plot threads")
        return threads
    
    def _group_elements_by_theme(self) -> Dict[str, List[PlotElement]]:
        """Group plot elements by common themes"""
        theme_groups = defaultdict(list)
        
        for element in self.plot_elements.values():
            # Group by tags
            for tag in element.tags:
                theme_groups[f"Theme: {tag}"].append(element)
            
            # Group by narrative role
            if element.narrative_role:
                theme_groups[f"Role: {element.narrative_role}"].append(element)
            
            # Group by element type
            theme_groups[f"Type: {element.element_type}"].append(element)
            
            # Group by shared connections
            for connection in element.connections:
                if connection in self.plot_elements:
                    theme_key = f"Connected to {connection}"
                    theme_groups[theme_key].append(element)
        
        # Filter groups that are too small or too large
        filtered_groups = {}
        for theme, elements in theme_groups.items():
            if 2 <= len(elements) <= 20:  # Reasonable thread size
                filtered_groups[theme] = elements
        
        return filtered_groups
    
    def _create_plot_thread(self, thread_id: str, title: str, elements: List[PlotElement]) -> PlotThread:
        """Create a plot thread from elements"""
        # Generate description based on elements
        description = self._generate_thread_description(elements)
        
        # Calculate complexity
        complexity = min(len(elements) // 3 + 1, 5)
        
        # Identify gaps
        gaps = self._identify_narrative_gaps(elements)
        
        thread = PlotThread(
            thread_id=thread_id,
            title=title,
            description=description,
            elements=elements,
            status='active',
            complexity=complexity,
            last_development=datetime.now().isoformat(),
            resolution_potential=0.5,  # Default middle value
            narrative_gaps=gaps
        )
        
        return thread
    
    def _generate_thread_description(self, elements: List[PlotElement]) -> str:
        """Generate a description for a plot thread"""
        element_types = Counter(e.element_type for e in elements)
        key_elements = sorted(elements, key=lambda e: e.importance_score, reverse=True)[:3]
        
        description = f"Thread involving {len(elements)} elements"
        if key_elements:
            names = [e.name for e in key_elements]
            description += f", centered around {', '.join(names[:2])}"
            if len(names) > 2:
                description += f" and {names[2]}"
        
        return description
    
    def _identify_narrative_gaps(self, elements: List[PlotElement]) -> List[str]:
        """Identify potential gaps in the narrative"""
        gaps = []
        
        # Check for missing connections
        connection_count = sum(len(e.connections) for e in elements)
        if connection_count < len(elements):
            gaps.append("Elements may need more interconnections")
        
        # Check for resolution potential
        antagonists = [e for e in elements if e.narrative_role == 'antagonist']
        protagonists = [e for e in elements if e.narrative_role == 'protagonist']
        
        if antagonists and not protagonists:
            gaps.append("Potential protagonist needed to oppose antagonist forces")
        elif protagonists and not antagonists:
            gaps.append("Consider adding conflict or challenges for protagonists")
        
        return gaps
    
    def find_connection_opportunities(self, limit: int = 20) -> List[StoryConnection]:
        """Find potential connections between plot elements"""
        print("🔗 Analyzing connection opportunities...")
        
        opportunities = []
        elements = list(self.plot_elements.values())
        
        # Compare each pair of elements
        for i, elem1 in enumerate(elements):
            for elem2 in elements[i+1:]:
                connection = self._analyze_element_pair(elem1, elem2)
                if connection and connection.strength > 0.3:  # Only strong connections
                    opportunities.append(connection)
        
        # Sort by strength and limit results
        opportunities.sort(key=lambda c: c.strength, reverse=True)
        opportunities = opportunities[:limit]
        
        # Update connections list
        self.connections.extend(opportunities)
        self._save_connections()
        
        print(f"✅ Found {len(opportunities)} connection opportunities")
        return opportunities
    
    def _analyze_element_pair(self, elem1: PlotElement, elem2: PlotElement) -> Optional[StoryConnection]:
        """Analyze potential connection between two elements"""
        if elem1.name == elem2.name:
            return None
        
        # Check if already connected
        if elem2.name in elem1.connections or elem1.name in elem2.connections:
            return None
        
        # Analyze content for connection patterns
        combined_content = f"{elem1.content_snippet} {elem2.content_snippet}".lower()
        
        connection_type = ""
        strength = 0.0
        evidence = []
        
        # Check for conflict patterns
        conflict_score = sum(1 for pattern in self.conflict_patterns if re.search(pattern, combined_content))
        if conflict_score > 0:
            connection_type = "conflict"
            strength = min(conflict_score * 0.2, 1.0)
            evidence.append(f"Conflict indicators found in content ({conflict_score})")
        
        # Check for alliance patterns
        alliance_score = sum(1 for pattern in self.alliance_patterns if re.search(pattern, combined_content))
        if alliance_score > conflict_score:
            connection_type = "alliance"
            strength = min(alliance_score * 0.2, 1.0)
            evidence.append(f"Alliance indicators found in content ({alliance_score})")
        
        # Check for mystery connections
        mystery_score = sum(1 for pattern in self.mystery_patterns if re.search(pattern, combined_content))
        if mystery_score > max(conflict_score, alliance_score):
            connection_type = "mystery"
            strength = min(mystery_score * 0.25, 1.0)
            evidence.append(f"Mystery indicators found in content ({mystery_score})")
        
        # Bonus for shared tags
        shared_tags = set(elem1.tags) & set(elem2.tags)
        if shared_tags:
            strength += len(shared_tags) * 0.1
            evidence.append(f"Shared tags: {', '.join(shared_tags)}")
        
        # Bonus for complementary types
        if elem1.element_type != elem2.element_type:
            strength += 0.1
            evidence.append(f"Complementary types: {elem1.element_type} and {elem2.element_type}")
        
        # Bonus for narrative role compatibility
        if ((elem1.narrative_role == 'protagonist' and elem2.narrative_role == 'antagonist') or
            (elem1.narrative_role == 'antagonist' and elem2.narrative_role == 'protagonist')):
            strength += 0.3
            evidence.append("Protagonist-antagonist relationship potential")
        
        if strength < 0.1:
            return None
        
        # Generate development suggestion
        suggestion = self._generate_development_suggestion(elem1, elem2, connection_type)
        
        return StoryConnection(
            element1=elem1.name,
            element2=elem2.name,
            connection_type=connection_type or "thematic",
            strength=min(strength, 1.0),
            evidence=evidence,
            suggested_development=suggestion,
            file_references=[elem1.file_path, elem2.file_path]
        )
    
    def _generate_development_suggestion(self, elem1: PlotElement, elem2: PlotElement, connection_type: str) -> str:
        """Generate a development suggestion for a connection"""
        if connection_type == "conflict":
            return f"Consider developing tension between {elem1.name} and {elem2.name}. Perhaps they have opposing goals or compete for the same resource."
        elif connection_type == "alliance":
            return f"{elem1.name} and {elem2.name} could form a strategic partnership. What common threat or goal might unite them?"
        elif connection_type == "mystery":
            return f"There may be hidden connections between {elem1.name} and {elem2.name}. Consider how their paths might intersect in unexpected ways."
        else:
            return f"Explore how {elem1.name} and {elem2.name} relate to each other in the broader narrative context."
    
    def identify_narrative_gaps(self) -> List[Dict]:
        """Identify gaps in the overall narrative"""
        print("🔍 Identifying narrative gaps...")
        
        gaps = []
        
        # Analyze thread distribution
        thread_status = Counter(thread.status for thread in self.plot_threads.values())
        if thread_status.get('active', 0) < 3:
            gaps.append({
                'type': 'insufficient_threads',
                'description': 'Campaign may need more active plot threads for engagement',
                'priority': 'medium',
                'suggestion': 'Consider developing 3-5 active threads for a dynamic campaign'
            })
        
        # Analyze element distribution
        element_types = Counter(elem.element_type for elem in self.plot_elements.values())
        
        if element_types.get('antagonist', 0) == 0:
            gaps.append({
                'type': 'missing_antagonist',
                'description': 'No clear antagonist identified in campaign',
                'priority': 'high',
                'suggestion': 'Develop compelling opposition for player characters'
            })
        
        if element_types.get('npc', 0) < 5:
            gaps.append({
                'type': 'insufficient_npcs',
                'description': 'May need more NPCs for rich interactions',
                'priority': 'low',
                'suggestion': 'Add supporting characters to flesh out the world'
            })
        
        # Analyze connection density
        total_connections = sum(len(elem.connections) for elem in self.plot_elements.values())
        avg_connections = total_connections / max(len(self.plot_elements), 1)
        
        if avg_connections < 2:
            gaps.append({
                'type': 'low_interconnection',
                'description': 'World elements may be too isolated from each other',
                'priority': 'medium',
                'suggestion': 'Develop more connections between NPCs, locations, and factions'
            })
        
        print(f"✅ Identified {len(gaps)} narrative gaps")
        return gaps
    
    def generate_thread_map(self, thread_id: str = None) -> str:
        """Generate a visual map of plot threads"""
        if thread_id:
            threads = [self.plot_threads[thread_id]] if thread_id in self.plot_threads else []
        else:
            threads = list(self.plot_threads.values())
        
        map_content = "# Plot Thread Map\n\n"
        
        for thread in threads:
            map_content += f"## {thread.title}\n"
            map_content += f"**Status:** {thread.status.title()}\n"
            map_content += f"**Complexity:** {thread.complexity}/5\n"
            map_content += f"**Description:** {thread.description}\n\n"
            
            if thread.elements:
                map_content += "**Elements:**\n"
                for element in thread.elements:
                    map_content += f"- **{element.name}** ({element.element_type}) - {element.narrative_role}\n"
                    if element.connections:
                        map_content += f"  - Connected to: {', '.join(element.connections[:3])}\n"
                map_content += "\n"
            
            if thread.narrative_gaps:
                map_content += "**Narrative Gaps:**\n"
                for gap in thread.narrative_gaps:
                    map_content += f"- {gap}\n"
                map_content += "\n"
            
            map_content += "---\n\n"
        
        return map_content
    
    def export_analysis(self, format_type: str = "json") -> str:
        """Export complete analysis data"""
        if format_type == "json":
            data = {
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_elements': len(self.plot_elements),
                    'total_threads': len(self.plot_threads),
                    'total_connections': len(self.connections),
                    'element_types': dict(Counter(e.element_type for e in self.plot_elements.values())),
                    'thread_statuses': dict(Counter(t.status for t in self.plot_threads.values()))
                },
                'top_elements': [
                    {
                        'name': elem.name,
                        'type': elem.element_type,
                        'importance': elem.importance_score,
                        'connections': len(elem.connections)
                    }
                    for elem in sorted(self.plot_elements.values(), key=lambda e: e.importance_score, reverse=True)[:10]
                ],
                'active_threads': [
                    {
                        'id': thread.thread_id,
                        'title': thread.title,
                        'complexity': thread.complexity,
                        'element_count': len(thread.elements),
                        'gaps': len(thread.narrative_gaps)
                    }
                    for thread in self.plot_threads.values() if thread.status == 'active'
                ],
                'connection_opportunities': [
                    {
                        'elements': f"{conn.element1} - {conn.element2}",
                        'type': conn.connection_type,
                        'strength': conn.strength,
                        'suggestion': conn.suggested_development
                    }
                    for conn in sorted(self.connections, key=lambda c: c.strength, reverse=True)[:10]
                ]
            }
            
            return json.dumps(data, indent=2)
        
        return "Unsupported format"

def main():
    parser = argparse.ArgumentParser(description="Plot Thread Weaver - Analyze and weave narrative connections")
    parser.add_argument('command', choices=['scan', 'analyze', 'threads', 'connections', 'gaps', 'map', 'export'])
    
    parser.add_argument('--force', action='store_true', help='Force full rescan')
    parser.add_argument('--thread-id', help='Specific thread ID for operations')
    parser.add_argument('--limit', type=int, default=20, help='Limit number of results')
    parser.add_argument('--format', default='json', help='Export format')
    
    args = parser.parse_args()
    
    weaver = PlotThreadWeaver()
    
    if args.command == 'scan':
        success = weaver.scan_vault_content(args.force)
        if success:
            print(f"📊 Found {len(weaver.plot_elements)} total plot elements")
        else:
            print("❌ Scan failed")
    
    elif args.command == 'analyze':
        weaver.scan_vault_content(args.force)
        threads = weaver.analyze_plot_threads()
        connections = weaver.find_connection_opportunities(args.limit)
        gaps = weaver.identify_narrative_gaps()
        
        print(f"\n📊 **Analysis Complete:**")
        print(f"- **Plot Elements:** {len(weaver.plot_elements)}")
        print(f"- **Plot Threads:** {len(threads)}")
        print(f"- **Connections:** {len(connections)}")
        print(f"- **Narrative Gaps:** {len(gaps)}")
    
    elif args.command == 'threads':
        if not weaver.plot_threads:
            print("No threads found. Run 'analyze' first.")
            return
        
        print(f"\n🧵 **Plot Threads ({len(weaver.plot_threads)})**\n")
        for thread in weaver.plot_threads.values():
            print(f"**{thread.title}**")
            print(f"  Status: {thread.status} | Complexity: {thread.complexity}/5")
            print(f"  Elements: {len(thread.elements)} | Description: {thread.description}")
            if thread.narrative_gaps:
                print(f"  Gaps: {len(thread.narrative_gaps)}")
            print()
    
    elif args.command == 'connections':
        if not weaver.connections:
            weaver.find_connection_opportunities(args.limit)
        
        connections = sorted(weaver.connections, key=lambda c: c.strength, reverse=True)[:args.limit]
        
        print(f"\n🔗 **Story Connections ({len(connections)})**\n")
        for conn in connections:
            print(f"**{conn.element1} ↔ {conn.element2}**")
            print(f"  Type: {conn.connection_type} | Strength: {conn.strength:.2f}")
            print(f"  Suggestion: {conn.suggested_development}")
            if conn.evidence:
                print(f"  Evidence: {', '.join(conn.evidence[:2])}")
            print()
    
    elif args.command == 'gaps':
        gaps = weaver.identify_narrative_gaps()
        
        print(f"\n🔍 **Narrative Gaps ({len(gaps)})**\n")
        for gap in gaps:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(gap['priority'], "⚪")
            print(f"{priority_emoji} **{gap['type'].replace('_', ' ').title()}**")
            print(f"  {gap['description']}")
            print(f"  💡 {gap['suggestion']}")
            print()
    
    elif args.command == 'map':
        thread_map = weaver.generate_thread_map(args.thread_id)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = PLOT_DATA_DIR / f"plot_thread_map_{timestamp}.md"
        
        with open(filename, 'w') as f:
            f.write(thread_map)
        
        print(f"✅ Thread map generated: {filename}")
        print(f"\nPreview:\n{thread_map[:500]}...")
    
    elif args.command == 'export':
        data = weaver.export_analysis(args.format)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = PLOT_DATA_DIR / f"plot_analysis_{timestamp}.{args.format}"
        
        with open(filename, 'w') as f:
            f.write(data)
        
        print(f"✅ Analysis exported: {filename}")

if __name__ == "__main__":
    main()