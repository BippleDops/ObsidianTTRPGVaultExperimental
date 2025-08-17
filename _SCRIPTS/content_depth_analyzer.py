#!/usr/bin/env python3
"""
Content Depth Analyzer
Analyzes content development depth and suggests improvements using Pydantic models.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter, defaultdict
import statistics

# Import our Pydantic models  
import sys
sys.path.append('../data')
from models import (
    BaseVaultContent, Character, Location, Faction, ContentStatus, 
    ContentType, WorldRealm
)

class ContentDepthMetrics:
    """Metrics for measuring content depth."""
    
    def __init__(self):
        self.word_count = 0
        self.paragraph_count = 0
        self.section_count = 0
        self.list_items = 0
        self.wikilinks = 0
        self.external_links = 0
        self.images = 0
        self.details_sections = 0
        self.dialogue_instances = 0
        self.sensory_descriptions = 0
        self.relationship_mentions = 0
        
    def calculate_depth_score(self) -> float:
        """Calculate overall depth score (0-100)."""
        score = 0
        
        # Word count contribution (0-25 points)
        if self.word_count >= 2000:
            score += 25
        elif self.word_count >= 1000:
            score += 20
        elif self.word_count >= 500:
            score += 15
        elif self.word_count >= 250:
            score += 10
        elif self.word_count >= 100:
            score += 5
            
        # Structure contribution (0-20 points)
        score += min(self.section_count * 2, 10)
        score += min(self.paragraph_count, 10)
        
        # Interconnection contribution (0-20 points)
        score += min(self.wikilinks * 1.5, 15)
        score += min(self.external_links, 5)
        
        # Rich content contribution (0-20 points)
        score += min(self.details_sections * 3, 10)
        score += min(self.dialogue_instances * 2, 5)
        score += min(self.sensory_descriptions, 5)
        
        # Relationship depth contribution (0-15 points)
        score += min(self.relationship_mentions * 1.5, 15)
        
        return min(score, 100)

class ContentDepthAnalyzer:
    """Analyzes content depth across the vault."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.content_metrics: Dict[str, ContentDepthMetrics] = {}
        self.content_types: Dict[str, ContentType] = {}
        self.content_status: Dict[str, ContentStatus] = {}
        self.content_worlds: Dict[str, WorldRealm] = {}
        
    def analyze_file_depth(self, file_path: Path) -> ContentDepthMetrics:
        """Analyze depth metrics for a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return ContentDepthMetrics()
            
        metrics = ContentDepthMetrics()
        
        # Basic text metrics
        metrics.word_count = len(content.split())
        metrics.paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
        
        # Structure metrics
        metrics.section_count = len(re.findall(r'^#+\s', content, re.MULTILINE))
        metrics.list_items = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
        
        # Link metrics
        metrics.wikilinks = len(re.findall(r'\[\[[^\]]+\]\]', content))
        metrics.external_links = len(re.findall(r'https?://[^\s\]]+', content))
        
        # Media metrics
        metrics.images = len(re.findall(r'!\[.*?\]\([^)]+\)', content))
        
        # Content quality metrics
        detail_indicators = [
            r'(?i)physical\s+description',
            r'(?i)personality',
            r'(?i)background',
            r'(?i)history',
            r'(?i)appearance',
            r'(?i)motivation',
            r'(?i)goals?',
            r'(?i)relationships?',
            r'(?i)secrets?'
        ]
        
        for indicator in detail_indicators:
            if re.search(indicator, content):
                metrics.details_sections += 1
                
        # Dialogue detection
        metrics.dialogue_instances = len(re.findall(r'"[^"]{10,}"', content))
        
        # Sensory description detection
        sensory_words = [
            'smell', 'scent', 'aroma', 'stench',
            'sound', 'hear', 'listen', 'noise', 'echo',
            'see', 'sight', 'view', 'glimpse', 'observe',
            'feel', 'touch', 'texture', 'rough', 'smooth',
            'taste', 'flavor', 'bitter', 'sweet'
        ]
        
        content_lower = content.lower()
        metrics.sensory_descriptions = sum(1 for word in sensory_words if word in content_lower)
        
        # Relationship mentions
        relationship_indicators = [
            'friend', 'ally', 'enemy', 'rival', 'mentor', 'student',
            'family', 'parent', 'child', 'sibling', 'spouse',
            'colleague', 'partner', 'companion', 'follower'
        ]
        
        metrics.relationship_mentions = sum(1 for word in relationship_indicators if word in content_lower)
        
        return metrics
        
    def determine_content_type(self, file_path: Path, content: str) -> ContentType:
        """Determine content type from file location and content."""
        path_str = str(file_path).lower()
        content_lower = content.lower()
        
        # Check file location
        if 'adventures' in path_str or 'campaign' in path_str:
            return ContentType.adventure
        elif 'session' in path_str:
            return ContentType.session
        elif 'characters' in path_str or 'groups' in path_str:
            # Distinguish between characters and factions
            character_indicators = ['age:', 'species:', 'personality:', 'physical description']
            if any(indicator in content_lower for indicator in character_indicators):
                return ContentType.character
            else:
                return ContentType.faction
        elif 'places' in path_str or 'locations' in path_str:
            return ContentType.location
        elif 'items' in path_str:
            return ContentType.item
        elif 'mechanics' in path_str:
            return ContentType.mechanics
        elif 'templates' in path_str:
            return ContentType.template
        else:
            return ContentType.lore
            
    def determine_status(self, content: str) -> ContentStatus:
        """Determine development status from content."""
        if len(content.strip()) < 100:
            return ContentStatus.stub
        elif any(indicator in content.upper() for indicator in ['TODO', 'TBD', 'DRAFT']):
            return ContentStatus.draft
        elif 'DEPRECATED' in content.upper() or 'ARCHIVED' in content.upper():
            return ContentStatus.archived
        else:
            return ContentStatus.active
            
    def determine_world(self, content: str) -> WorldRealm:
        """Determine world realm from content."""
        content_lower = content.lower()
        
        aquabyssos_score = sum(1 for word in ['aquabyssos', 'depth', 'pressure', 'abyssal', 'underwater'] 
                              if word in content_lower)
        aethermoor_score = sum(1 for word in ['aethermoor', 'sky', 'wind', 'crystal', 'altitude'] 
                              if word in content_lower)
        
        if aquabyssos_score > aethermoor_score:
            return WorldRealm.aquabyssos
        elif aethermoor_score > aquabyssos_score:
            return WorldRealm.aethermoor
        else:
            return WorldRealm.both
            
    def analyze_vault_depth(self) -> Dict[str, Any]:
        """Analyze depth across entire vault."""
        print("Analyzing vault content depth...")
        
        markdown_files = list(self.vault_path.rglob('*.md'))
        print(f"Found {len(markdown_files)} markdown files")
        
        for file_path in markdown_files:
            # Skip certain files
            if any(skip in file_path.name.lower() 
                   for skip in ['readme', 'index', '.obsidian']):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
                
            relative_path = str(file_path.relative_to(self.vault_path))
            
            # Analyze depth
            metrics = self.analyze_file_depth(file_path)
            self.content_metrics[relative_path] = metrics
            
            # Determine metadata
            self.content_types[relative_path] = self.determine_content_type(file_path, content)
            self.content_status[relative_path] = self.determine_status(content)
            self.content_worlds[relative_path] = self.determine_world(content)
            
        return self.compile_analysis_results()
        
    def compile_analysis_results(self) -> Dict[str, Any]:
        """Compile comprehensive analysis results."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_files": len(self.content_metrics),
            "depth_statistics": {},
            "content_type_analysis": {},
            "status_analysis": {},
            "world_analysis": {},
            "improvement_suggestions": [],
            "top_content": [],
            "development_priorities": []
        }
        
        # Calculate depth statistics
        depth_scores = [m.calculate_depth_score() for m in self.content_metrics.values()]
        
        if depth_scores:
            results["depth_statistics"] = {
                "mean_depth": statistics.mean(depth_scores),
                "median_depth": statistics.median(depth_scores),
                "std_deviation": statistics.stdev(depth_scores) if len(depth_scores) > 1 else 0,
                "min_depth": min(depth_scores),
                "max_depth": max(depth_scores),
                "depth_distribution": {
                    "excellent (80-100)": len([s for s in depth_scores if s >= 80]),
                    "good (60-79)": len([s for s in depth_scores if 60 <= s < 80]),
                    "moderate (40-59)": len([s for s in depth_scores if 40 <= s < 60]),
                    "basic (20-39)": len([s for s in depth_scores if 20 <= s < 40]),
                    "minimal (0-19)": len([s for s in depth_scores if s < 20])
                }
            }
            
        # Analyze by content type
        type_metrics = defaultdict(list)
        for path, content_type in self.content_types.items():
            if path in self.content_metrics:
                score = self.content_metrics[path].calculate_depth_score()
                type_metrics[content_type.value].append(score)
                
        results["content_type_analysis"] = {
            content_type: {
                "count": len(scores),
                "mean_depth": statistics.mean(scores) if scores else 0,
                "median_depth": statistics.median(scores) if scores else 0
            }
            for content_type, scores in type_metrics.items()
        }
        
        # Analyze by status
        status_metrics = defaultdict(list)
        for path, status in self.content_status.items():
            if path in self.content_metrics:
                score = self.content_metrics[path].calculate_depth_score()
                status_metrics[status.value].append(score)
                
        results["status_analysis"] = {
            status: {
                "count": len(scores),
                "mean_depth": statistics.mean(scores) if scores else 0
            }
            for status, scores in status_metrics.items()
        }
        
        # Top content by depth
        file_scores = [(path, metrics.calculate_depth_score()) 
                      for path, metrics in self.content_metrics.items()]
        file_scores.sort(key=lambda x: x[1], reverse=True)
        
        results["top_content"] = file_scores[:20]
        
        # Development priorities (lowest scoring content that should be improved)
        low_scoring = [(path, score) for path, score in file_scores 
                      if score < 40 and self.content_status[path] in [ContentStatus.active, ContentStatus.draft]]
        results["development_priorities"] = low_scoring[-20:]  # Bottom 20
        
        # Generate improvement suggestions
        results["improvement_suggestions"] = self.generate_improvement_suggestions(file_scores)
        
        return results
        
    def generate_improvement_suggestions(self, file_scores: List[Tuple[str, float]]) -> List[Dict[str, Any]]:
        """Generate specific improvement suggestions."""
        suggestions = []
        
        # Find stub content that could be expanded
        stub_files = [path for path, status in self.content_status.items() 
                     if status == ContentStatus.stub]
        
        if len(stub_files) > 10:
            suggestions.append({
                "priority": "high",
                "category": "content_expansion", 
                "description": f"Expand {len(stub_files)} stub files to draft or active status",
                "specific_files": stub_files[:10]
            })
            
        # Find files with low interconnection
        low_connection_files = []
        for path, metrics in self.content_metrics.items():
            if metrics.wikilinks < 3 and metrics.calculate_depth_score() > 20:
                low_connection_files.append(path)
                
        if low_connection_files:
            suggestions.append({
                "priority": "medium",
                "category": "interconnection",
                "description": f"Add more cross-references to {len(low_connection_files)} files",
                "specific_files": low_connection_files[:10]
            })
            
        # Find content lacking sensory details
        sensory_lacking = []
        for path, metrics in self.content_metrics.items():
            content_type = self.content_types.get(path)
            if (content_type in [ContentType.location, ContentType.character] and 
                metrics.sensory_descriptions < 3):
                sensory_lacking.append(path)
                
        if sensory_lacking:
            suggestions.append({
                "priority": "medium", 
                "category": "sensory_enhancement",
                "description": f"Add sensory descriptions to {len(sensory_lacking)} location/character files",
                "specific_files": sensory_lacking[:10]
            })
            
        return suggestions
        
    def generate_file_report(self, file_path: str) -> Dict[str, Any]:
        """Generate detailed report for specific file."""
        if file_path not in self.content_metrics:
            return {"error": "File not found in analysis"}
            
        metrics = self.content_metrics[file_path]
        depth_score = metrics.calculate_depth_score()
        
        report = {
            "file_path": file_path,
            "depth_score": depth_score,
            "content_type": self.content_types[file_path].value,
            "status": self.content_status[file_path].value,
            "world": self.content_worlds[file_path].value,
            "metrics": {
                "word_count": metrics.word_count,
                "paragraph_count": metrics.paragraph_count,
                "section_count": metrics.section_count,
                "wikilinks": metrics.wikilinks,
                "details_sections": metrics.details_sections,
                "sensory_descriptions": metrics.sensory_descriptions,
                "relationship_mentions": metrics.relationship_mentions
            },
            "strengths": [],
            "improvement_areas": [],
            "specific_suggestions": []
        }
        
        # Identify strengths
        if metrics.word_count >= 1000:
            report["strengths"].append("Good word count")
        if metrics.wikilinks >= 5:
            report["strengths"].append("Well interconnected")
        if metrics.sensory_descriptions >= 5:
            report["strengths"].append("Rich sensory details")
        if metrics.section_count >= 3:
            report["strengths"].append("Well structured")
            
        # Identify improvement areas
        if metrics.word_count < 500:
            report["improvement_areas"].append("Content length")
            report["specific_suggestions"].append("Expand content with more details and examples")
        if metrics.wikilinks < 3:
            report["improvement_areas"].append("Interconnection")
            report["specific_suggestions"].append("Add links to related characters, locations, or factions")
        if metrics.sensory_descriptions < 3:
            report["improvement_areas"].append("Sensory immersion")
            report["specific_suggestions"].append("Add descriptions of sights, sounds, smells")
        if metrics.relationship_mentions < 2:
            report["improvement_areas"].append("Character relationships")
            report["specific_suggestions"].append("Describe connections to other characters or groups")
            
        return report
        
    def export_results(self, results: Dict[str, Any], output_dir: str) -> None:
        """Export analysis results."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export main results
        with open(output_path / 'content_depth_analysis.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        # Export detailed metrics
        detailed_metrics = {
            path: {
                "depth_score": metrics.calculate_depth_score(),
                "metrics": metrics.__dict__,
                "content_type": self.content_types.get(path, "unknown"),
                "status": self.content_status.get(path, "unknown"),
                "world": self.content_worlds.get(path, "unknown")
            }
            for path, metrics in self.content_metrics.items()
        }
        
        with open(output_path / 'detailed_metrics.json', 'w') as f:
            json.dump(detailed_metrics, f, indent=2, default=str)
            
        print(f"Results exported to {output_path}")
        
def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze content depth in Cordelia vault")
    parser.add_argument("vault_path", help="Path to vault directory")
    parser.add_argument("--output", "-o", help="Output directory for results", 
                       default="content_depth_analysis")
    parser.add_argument("--file", "-f", help="Generate report for specific file")
    
    args = parser.parse_args()
    
    analyzer = ContentDepthAnalyzer(args.vault_path)
    results = analyzer.analyze_vault_depth()
    
    if args.file:
        report = analyzer.generate_file_report(args.file)
        print(f"File Report for {args.file}:")
        print(json.dumps(report, indent=2, default=str))
    else:
        print("Content Depth Analysis Results:")
        stats = results["depth_statistics"]
        print(f"Total files: {results['total_files']}")
        print(f"Mean depth score: {stats['mean_depth']:.1f}")
        print(f"Depth distribution: {results['depth_statistics']['depth_distribution']}")
        print(f"Improvement suggestions: {len(results['improvement_suggestions'])}")
        
        analyzer.export_results(results, args.output)
        
if __name__ == "__main__":
    main()