#!/usr/bin/env python3
"""
Campaign Coherence Checker
Validates consistency across campaign elements using Pydantic models.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Set, Optional, Any
from collections import defaultdict, Counter

# Import our Pydantic models  
import sys
sys.path.append('../data')
from models import (
    BaseVaultContent, Character, Location, Faction, Quest, Item, 
    Session, Campaign, ContentStatus, WorldRealm, ContentType,
    ValidationReport, ContentValidationError
)

class CoherenceViolation:
    """Represents a consistency violation in the campaign."""
    def __init__(self, violation_type: str, description: str, 
                 severity: str, files: List[str], suggested_fix: str = ""):
        self.violation_type = violation_type
        self.description = description
        self.severity = severity
        self.files = files
        self.suggested_fix = suggested_fix
        self.timestamp = datetime.now()

class CampaignCoherenceChecker:
    """Checks campaign consistency and coherence."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.characters: Dict[str, Dict] = {}
        self.locations: Dict[str, Dict] = {}
        self.factions: Dict[str, Dict] = {}
        self.sessions: Dict[str, Dict] = {}
        self.items: Dict[str, Dict] = {}
        
        self.violations: List[CoherenceViolation] = []
        self.character_mentions: Dict[str, List[str]] = defaultdict(list)
        self.location_mentions: Dict[str, List[str]] = defaultdict(list)
        self.faction_mentions: Dict[str, List[str]] = defaultdict(list)
        
    def load_content(self) -> None:
        """Load all vault content for analysis."""
        print("Loading vault content...")
        
        # Load characters
        character_files = list(self.vault_path.rglob("*Character*.md"))
        character_files.extend([f for f in self.vault_path.rglob("*.md") 
                               if self.is_character_file(f)])
        
        for file_path in character_files:
            char_data = self.extract_basic_data(file_path)
            if char_data:
                self.characters[char_data['name']] = {
                    **char_data,
                    'file_path': str(file_path)
                }
                
        # Load locations
        location_dirs = [
            self.vault_path / "02_Worldbuilding" / "Places",
            self.vault_path / "02_Worldbuilding" / "Locations"
        ]
        
        location_files = []
        for loc_dir in location_dirs:
            if loc_dir.exists():
                location_files.extend(loc_dir.rglob("*.md"))
                
        for file_path in location_files:
            loc_data = self.extract_basic_data(file_path)
            if loc_data:
                self.locations[loc_data['name']] = {
                    **loc_data,
                    'file_path': str(file_path)
                }
                
        # Load factions
        faction_files = list((self.vault_path / "02_Worldbuilding" / "Groups").rglob("*.md"))
        for file_path in faction_files:
            if not self.is_character_file(file_path):
                fact_data = self.extract_basic_data(file_path)
                if fact_data:
                    self.factions[fact_data['name']] = {
                        **fact_data,
                        'file_path': str(file_path)
                    }
                    
        # Load sessions
        session_dirs = [
            self.vault_path / "01_Adventures",
            self.vault_path / "1-Session Journals"
        ]
        
        session_files = []
        for sess_dir in session_dirs:
            if sess_dir.exists():
                session_files.extend(sess_dir.rglob("*.md"))
                
        for file_path in session_files:
            if "session" in file_path.name.lower():
                sess_data = self.extract_basic_data(file_path)
                if sess_data:
                    self.sessions[sess_data['name']] = {
                        **sess_data,
                        'file_path': str(file_path)
                    }
                    
        print(f"Loaded: {len(self.characters)} characters, {len(self.locations)} locations, "
              f"{len(self.factions)} factions, {len(self.sessions)} sessions")
              
    def is_character_file(self, file_path: Path) -> bool:
        """Determine if a file represents a character."""
        content = self.read_file_content(file_path)
        if not content:
            return False
            
        # Look for character indicators
        character_indicators = [
            'full name:', 'age:', 'species:', 'occupation:',
            'personality:', 'background:', 'allies:', 'enemies:',
            'physical description', 'character traits'
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in character_indicators)
        
    def read_file_content(self, file_path: Path) -> Optional[str]:
        """Read file content safely."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
            
    def extract_basic_data(self, file_path: Path) -> Optional[Dict]:
        """Extract basic data from a file."""
        content = self.read_file_content(file_path)
        if not content:
            return None
            
        name = file_path.stem
        
        # Extract world realm
        world = WorldRealm.both
        if 'aquabyssos' in content.lower():
            world = WorldRealm.aquabyssos
        elif 'aethermoor' in content.lower():
            world = WorldRealm.aethermoor
            
        return {
            'name': name,
            'world': world,
            'content': content
        }
        
    def find_references(self) -> None:
        """Find references between different content types."""
        print("Finding cross-references...")
        
        all_files = list(self.vault_path.rglob("*.md"))
        
        for file_path in all_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
                
            # Find character mentions
            for char_name in self.characters.keys():
                if char_name in content or f"[[{char_name}]]" in content:
                    self.character_mentions[char_name].append(str(file_path))
                    
            # Find location mentions
            for loc_name in self.locations.keys():
                if loc_name in content or f"[[{loc_name}]]" in content:
                    self.location_mentions[loc_name].append(str(file_path))
                    
            # Find faction mentions
            for fact_name in self.factions.keys():
                if fact_name in content or f"[[{fact_name}]]" in content:
                    self.faction_mentions[fact_name].append(str(file_path))
                    
    def check_character_consistency(self) -> None:
        """Check for character consistency violations."""
        print("Checking character consistency...")
        
        for char_name, char_data in self.characters.items():
            # Check if character appears in multiple realms consistently
            realm_appearances = set()
            
            for file_path in self.character_mentions.get(char_name, []):
                content = self.read_file_content(Path(file_path))
                if content:
                    if 'aquabyssos' in content.lower():
                        realm_appearances.add(WorldRealm.aquabyssos)
                    if 'aethermoor' in content.lower():
                        realm_appearances.add(WorldRealm.aethermoor)
                        
            # If character appears in multiple realms, check for explanation
            if len(realm_appearances) > 1 and char_data['world'] != WorldRealm.both:
                self.violations.append(CoherenceViolation(
                    violation_type="character_realm_inconsistency",
                    description=f"Character {char_name} appears in multiple realms but is marked as {char_data['world']}",
                    severity="moderate",
                    files=[char_data['file_path']] + self.character_mentions.get(char_name, []),
                    suggested_fix="Either mark character as cross-realm or provide explanation for travel"
                ))
                
            # Check for orphaned characters (mentioned but no file)
            mentions = self.character_mentions.get(char_name, [])
            if len(mentions) == 0:
                self.violations.append(CoherenceViolation(
                    violation_type="orphaned_character",
                    description=f"Character {char_name} has a file but is never mentioned elsewhere",
                    severity="low",
                    files=[char_data['file_path']],
                    suggested_fix="Add references to this character in relevant content"
                ))
                
    def check_location_consistency(self) -> None:
        """Check for location consistency violations."""
        print("Checking location consistency...")
        
        for loc_name, loc_data in self.locations.items():
            # Check realm consistency
            mentions = self.location_mentions.get(loc_name, [])
            
            realm_contexts = []
            for file_path in mentions:
                content = self.read_file_content(Path(file_path))
                if content:
                    if 'pressure' in content.lower() or 'depth' in content.lower():
                        realm_contexts.append(WorldRealm.aquabyssos)
                    if 'altitude' in content.lower() or 'wind' in content.lower():
                        realm_contexts.append(WorldRealm.aethermoor)
                        
            # Check for realm contradictions
            unique_contexts = set(realm_contexts)
            if len(unique_contexts) > 1 and loc_data['world'] != WorldRealm.both:
                self.violations.append(CoherenceViolation(
                    violation_type="location_realm_inconsistency",
                    description=f"Location {loc_name} appears in different realm contexts",
                    severity="high",
                    files=[loc_data['file_path']] + mentions,
                    suggested_fix="Clarify location's realm or mark as convergence zone"
                ))
                
    def check_faction_consistency(self) -> None:
        """Check for faction consistency violations."""
        print("Checking faction consistency...")
        
        # Check for faction relationship contradictions
        for fact_name, fact_data in self.factions.items():
            content = fact_data['content']
            
            # Extract allies and enemies from content
            allies = self.extract_relationships(content, 'allies?|allied')
            enemies = self.extract_relationships(content, 'enemies?|enemy|opposed')
            
            # Check for contradictions (same faction as both ally and enemy)
            contradictions = set(allies) & set(enemies)
            if contradictions:
                self.violations.append(CoherenceViolation(
                    violation_type="faction_relationship_contradiction",
                    description=f"Faction {fact_name} lists {contradictions} as both ally and enemy",
                    severity="high",
                    files=[fact_data['file_path']],
                    suggested_fix="Resolve relationship contradiction or explain complexity"
                ))
                
    def extract_relationships(self, content: str, pattern: str) -> List[str]:
        """Extract relationship mentions from content."""
        matches = re.findall(f'{pattern}[^.]*?([A-Z][a-zA-Z\s]+)', content, re.IGNORECASE)
        return [match.strip() for match in matches if len(match.strip()) > 2]
        
    def check_timeline_consistency(self) -> None:
        """Check for timeline consistency violations."""
        print("Checking timeline consistency...")
        
        # Extract dates from sessions
        session_dates = {}
        for sess_name, sess_data in self.sessions.items():
            content = sess_data['content']
            
            # Look for date patterns
            date_patterns = [
                r'(\d{4}-\d{2}-\d{2})',
                r'Session (\d+)',
                r'Date: ([^.\n]+)'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    session_dates[sess_name] = matches[0]
                    break
                    
        # Check for date contradictions or gaps
        numeric_sessions = {}
        for sess_name, date_info in session_dates.items():
            session_match = re.search(r'session\s+(\d+)', sess_name.lower())
            if session_match:
                session_num = int(session_match.group(1))
                numeric_sessions[session_num] = sess_name
                
        # Check for missing sessions in sequence
        if numeric_sessions:
            session_nums = sorted(numeric_sessions.keys())
            for i in range(min(session_nums), max(session_nums)):
                if i not in numeric_sessions:
                    self.violations.append(CoherenceViolation(
                        violation_type="missing_session",
                        description=f"Session {i} appears to be missing from sequence",
                        severity="moderate",
                        files=[],
                        suggested_fix="Add missing session or renumber existing sessions"
                    ))
                    
    def check_cross_references(self) -> None:
        """Check for broken cross-references."""
        print("Checking cross-references...")
        
        all_files = list(self.vault_path.rglob("*.md"))
        all_names = set()
        all_names.update(self.characters.keys())
        all_names.update(self.locations.keys())
        all_names.update(self.factions.keys())
        
        for file_path in all_files:
            content = self.read_file_content(file_path)
            if not content:
                continue
                
            # Find wikilinks
            wikilink_pattern = r'\[\[([^]]+)\]\]'
            wikilinks = re.findall(wikilink_pattern, content)
            
            for link in wikilinks:
                # Clean link (remove # fragments and | display text)
                clean_link = link.split('#')[0].split('|')[0].strip()
                
                if clean_link not in all_names and clean_link not in [f.stem for f in all_files]:
                    self.violations.append(CoherenceViolation(
                        violation_type="broken_wikilink",
                        description=f"Broken wikilink to '{clean_link}' in {file_path.name}",
                        severity="low",
                        files=[str(file_path)],
                        suggested_fix="Create missing content or fix link"
                    ))
                    
    def run_coherence_check(self) -> Dict[str, Any]:
        """Run comprehensive coherence check."""
        print("Starting coherence check...")
        
        self.load_content()
        self.find_references()
        
        self.check_character_consistency()
        self.check_location_consistency() 
        self.check_faction_consistency()
        self.check_timeline_consistency()
        self.check_cross_references()
        
        # Compile results
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_violations": len(self.violations),
            "violation_by_severity": Counter([v.severity for v in self.violations]),
            "violation_by_type": Counter([v.violation_type for v in self.violations]),
            "content_stats": {
                "characters": len(self.characters),
                "locations": len(self.locations),
                "factions": len(self.factions),
                "sessions": len(self.sessions)
            },
            "violations": [
                {
                    "type": v.violation_type,
                    "description": v.description,
                    "severity": v.severity,
                    "files": v.files,
                    "suggested_fix": v.suggested_fix,
                    "timestamp": v.timestamp.isoformat()
                }
                for v in self.violations
            ]
        }
        
        return results
        
    def export_report(self, results: Dict[str, Any], output_path: str) -> None:
        """Export coherence check report."""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"Coherence report exported to: {output_path}")
        
def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check campaign coherence in Cordelia vault")
    parser.add_argument("vault_path", help="Path to vault directory")
    parser.add_argument("--output", "-o", help="Output path for coherence report", 
                       default="coherence_report.json")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    checker = CampaignCoherenceChecker(args.vault_path)
    results = checker.run_coherence_check()
    
    print(f"\nCoherence Check Results:")
    print(f"Total violations: {results['total_violations']}")
    print(f"By severity: {dict(results['violation_by_severity'])}")
    print(f"By type: {dict(results['violation_by_type'])}")
    
    if args.verbose:
        for violation in results['violations']:
            print(f"\n{violation['severity'].upper()}: {violation['description']}")
            if violation['suggested_fix']:
                print(f"  Fix: {violation['suggested_fix']}")
                
    checker.export_report(results, args.output)
    
if __name__ == "__main__":
    main()