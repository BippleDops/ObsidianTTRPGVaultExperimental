#!/usr/bin/env python3
"""
Narrative Consistency AI - Sprint 3 Intelligence Layer Feature

This system detects contradictions, inconsistencies, and lore compliance issues
across campaign content. It provides intelligent analysis to maintain narrative
continuity and catch potential plot holes.

Features:
- Detect factual contradictions between documents
- Check lore compliance against established canon
- Identify temporal inconsistencies in events
- Verify character consistency across appearances
- Flag potential plot holes and logical inconsistencies
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import argparse
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import difflib

# Set up paths
VAULT_ROOT = Path(__file__).parent.parent
CONSISTENCY_DATA_DIR = VAULT_ROOT / "scripts" / "consistency_data"
CONSISTENCY_DATA_DIR.mkdir(exist_ok=True)

@dataclass
class FactClaim:
    """Represents a factual claim extracted from content"""
    claim_id: str
    source_file: str
    claim_text: str
    subject: str
    predicate: str
    object: str
    confidence: float
    context: str
    line_number: int = 0
    timestamp: str = ""

@dataclass
class Contradiction:
    """Represents a detected contradiction between claims"""
    contradiction_id: str
    claim1: FactClaim
    claim2: FactClaim
    contradiction_type: str  # factual, temporal, character, lore
    severity: str  # low, medium, high, critical
    description: str
    suggested_resolution: str
    auto_resolvable: bool = False

@dataclass
class ConsistencyRule:
    """Represents a lore consistency rule"""
    rule_id: str
    rule_type: str  # character_trait, world_law, timeline, relationship
    pattern: str
    description: str
    severity: str
    active: bool = True

@dataclass
class LoreViolation:
    """Represents a violation of established lore"""
    violation_id: str
    rule: ConsistencyRule
    source_file: str
    violation_text: str
    line_number: int
    severity: str
    suggested_fix: str

class NarrativeConsistencyAI:
    """Main system for detecting narrative inconsistencies"""
    
    def __init__(self):
        self.facts_file = CONSISTENCY_DATA_DIR / "extracted_facts.json"
        self.rules_file = CONSISTENCY_DATA_DIR / "consistency_rules.json"
        self.contradictions_file = CONSISTENCY_DATA_DIR / "detected_contradictions.json"
        self.violations_file = CONSISTENCY_DATA_DIR / "lore_violations.json"
        self.analysis_cache = CONSISTENCY_DATA_DIR / "analysis_cache.json"
        
        # Load existing data
        self.facts = self._load_facts()
        self.rules = self._load_rules()
        self.contradictions = self._load_contradictions()
        self.violations = self._load_violations()
        self.cache = self._load_cache()
        
        # Initialize default rules
        if not self.rules:
            self._create_default_rules()
    
    def _load_facts(self) -> List[FactClaim]:
        """Load extracted facts from file"""
        if not self.facts_file.exists():
            return []
        
        with open(self.facts_file, 'r') as f:
            data = json.load(f)
        
        facts = []
        for fact_data in data:
            fact = FactClaim(
                claim_id=fact_data['claim_id'],
                source_file=fact_data['source_file'],
                claim_text=fact_data['claim_text'],
                subject=fact_data['subject'],
                predicate=fact_data['predicate'],
                object=fact_data['object'],
                confidence=fact_data['confidence'],
                context=fact_data['context'],
                line_number=fact_data.get('line_number', 0),
                timestamp=fact_data.get('timestamp', '')
            )
            facts.append(fact)
        
        return facts
    
    def _save_facts(self):
        """Save facts to file"""
        data = []
        for fact in self.facts:
            fact_data = {
                'claim_id': fact.claim_id,
                'source_file': fact.source_file,
                'claim_text': fact.claim_text,
                'subject': fact.subject,
                'predicate': fact.predicate,
                'object': fact.object,
                'confidence': fact.confidence,
                'context': fact.context,
                'line_number': fact.line_number,
                'timestamp': fact.timestamp
            }
            data.append(fact_data)
        
        with open(self.facts_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_rules(self) -> List[ConsistencyRule]:
        """Load consistency rules from file"""
        if not self.rules_file.exists():
            return []
        
        with open(self.rules_file, 'r') as f:
            data = json.load(f)
        
        rules = []
        for rule_data in data:
            rule = ConsistencyRule(
                rule_id=rule_data['rule_id'],
                rule_type=rule_data['rule_type'],
                pattern=rule_data['pattern'],
                description=rule_data['description'],
                severity=rule_data['severity'],
                active=rule_data.get('active', True)
            )
            rules.append(rule)
        
        return rules
    
    def _save_rules(self):
        """Save consistency rules to file"""
        data = []
        for rule in self.rules:
            rule_data = {
                'rule_id': rule.rule_id,
                'rule_type': rule.rule_type,
                'pattern': rule.pattern,
                'description': rule.description,
                'severity': rule.severity,
                'active': rule.active
            }
            data.append(rule_data)
        
        with open(self.rules_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_contradictions(self) -> List[Contradiction]:
        """Load detected contradictions from file"""
        if not self.contradictions_file.exists():
            return []
        
        with open(self.contradictions_file, 'r') as f:
            data = json.load(f)
        
        contradictions = []
        for contra_data in data:
            # Reconstruct fact claims
            claim1_data = contra_data['claim1']
            claim1 = FactClaim(
                claim_id=claim1_data['claim_id'],
                source_file=claim1_data['source_file'],
                claim_text=claim1_data['claim_text'],
                subject=claim1_data['subject'],
                predicate=claim1_data['predicate'],
                object=claim1_data['object'],
                confidence=claim1_data['confidence'],
                context=claim1_data['context']
            )
            
            claim2_data = contra_data['claim2']
            claim2 = FactClaim(
                claim_id=claim2_data['claim_id'],
                source_file=claim2_data['source_file'],
                claim_text=claim2_data['claim_text'],
                subject=claim2_data['subject'],
                predicate=claim2_data['predicate'],
                object=claim2_data['object'],
                confidence=claim2_data['confidence'],
                context=claim2_data['context']
            )
            
            contradiction = Contradiction(
                contradiction_id=contra_data['contradiction_id'],
                claim1=claim1,
                claim2=claim2,
                contradiction_type=contra_data['contradiction_type'],
                severity=contra_data['severity'],
                description=contra_data['description'],
                suggested_resolution=contra_data['suggested_resolution'],
                auto_resolvable=contra_data.get('auto_resolvable', False)
            )
            contradictions.append(contradiction)
        
        return contradictions
    
    def _save_contradictions(self):
        """Save contradictions to file"""
        data = []
        for contradiction in self.contradictions:
            claim1_data = {
                'claim_id': contradiction.claim1.claim_id,
                'source_file': contradiction.claim1.source_file,
                'claim_text': contradiction.claim1.claim_text,
                'subject': contradiction.claim1.subject,
                'predicate': contradiction.claim1.predicate,
                'object': contradiction.claim1.object,
                'confidence': contradiction.claim1.confidence,
                'context': contradiction.claim1.context
            }
            
            claim2_data = {
                'claim_id': contradiction.claim2.claim_id,
                'source_file': contradiction.claim2.source_file,
                'claim_text': contradiction.claim2.claim_text,
                'subject': contradiction.claim2.subject,
                'predicate': contradiction.claim2.predicate,
                'object': contradiction.claim2.object,
                'confidence': contradiction.claim2.confidence,
                'context': contradiction.claim2.context
            }
            
            contra_data = {
                'contradiction_id': contradiction.contradiction_id,
                'claim1': claim1_data,
                'claim2': claim2_data,
                'contradiction_type': contradiction.contradiction_type,
                'severity': contradiction.severity,
                'description': contradiction.description,
                'suggested_resolution': contradiction.suggested_resolution,
                'auto_resolvable': contradiction.auto_resolvable
            }
            data.append(contra_data)
        
        with open(self.contradictions_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_violations(self) -> List[LoreViolation]:
        """Load lore violations from file"""
        if not self.violations_file.exists():
            return []
        
        with open(self.violations_file, 'r') as f:
            data = json.load(f)
        
        violations = []
        for viol_data in data:
            # Reconstruct rule
            rule_data = viol_data['rule']
            rule = ConsistencyRule(
                rule_id=rule_data['rule_id'],
                rule_type=rule_data['rule_type'],
                pattern=rule_data['pattern'],
                description=rule_data['description'],
                severity=rule_data['severity'],
                active=rule_data.get('active', True)
            )
            
            violation = LoreViolation(
                violation_id=viol_data['violation_id'],
                rule=rule,
                source_file=viol_data['source_file'],
                violation_text=viol_data['violation_text'],
                line_number=viol_data['line_number'],
                severity=viol_data['severity'],
                suggested_fix=viol_data['suggested_fix']
            )
            violations.append(violation)
        
        return violations
    
    def _save_violations(self):
        """Save violations to file"""
        data = []
        for violation in self.violations:
            rule_data = {
                'rule_id': violation.rule.rule_id,
                'rule_type': violation.rule.rule_type,
                'pattern': violation.rule.pattern,
                'description': violation.rule.description,
                'severity': violation.rule.severity,
                'active': violation.rule.active
            }
            
            viol_data = {
                'violation_id': violation.violation_id,
                'rule': rule_data,
                'source_file': violation.source_file,
                'violation_text': violation.violation_text,
                'line_number': violation.line_number,
                'severity': violation.severity,
                'suggested_fix': violation.suggested_fix
            }
            data.append(viol_data)
        
        with open(self.violations_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_cache(self) -> Dict:
        """Load analysis cache"""
        if not self.analysis_cache.exists():
            return {'last_full_check': '', 'file_checksums': {}}
        
        with open(self.analysis_cache, 'r') as f:
            return json.load(f)
    
    def _save_cache(self):
        """Save analysis cache"""
        with open(self.analysis_cache, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _create_default_rules(self):
        """Create default consistency rules for Cordelia world"""
        default_rules = [
            # Character consistency rules
            ConsistencyRule(
                rule_id="char_age_consistency",
                rule_type="character_trait", 
                pattern=r"age.*?(\d+)",
                description="Character ages should be consistent across documents",
                severity="medium"
            ),
            ConsistencyRule(
                rule_id="char_death_consistency",
                rule_type="character_trait",
                pattern=r"(died|dead|killed|deceased)",
                description="Dead characters should not appear alive in later events", 
                severity="high"
            ),
            
            # World law rules
            ConsistencyRule(
                rule_id="pressure_mechanics",
                rule_type="world_law",
                pattern=r"depth.*pressure|pressure.*depth",
                description="Pressure mechanics should follow established physics",
                severity="medium"
            ),
            ConsistencyRule(
                rule_id="crystal_corruption",
                rule_type="world_law", 
                pattern=r"crystal.*corrupt|corrupt.*crystal",
                description="Crystal corruption should follow established rules",
                severity="high"
            ),
            
            # Timeline rules  
            ConsistencyRule(
                rule_id="event_chronology",
                rule_type="timeline",
                pattern=r"session \d+|year \d+|before|after",
                description="Events should follow logical chronological order",
                severity="high"
            ),
            
            # Relationship rules
            ConsistencyRule(
                rule_id="political_relationships",
                rule_type="relationship",
                pattern=r"ally|enemy|oppose|support|allied|hostile",
                description="Political relationships should remain consistent unless explicitly changed",
                severity="medium"
            )
        ]
        
        self.rules.extend(default_rules)
        self._save_rules()
    
    def extract_facts_from_content(self, force_refresh: bool = False) -> int:
        """Extract factual claims from vault content"""
        print("🔍 Extracting facts from campaign content...")
        
        # Get all markdown files
        content_dirs = [
            VAULT_ROOT / "02_Worldbuilding",
            VAULT_ROOT / "01_Adventures",
            VAULT_ROOT / "1-Session Journals"
        ]
        
        files_to_process = []
        for content_dir in content_dirs:
            if content_dir.exists():
                files_to_process.extend(content_dir.rglob("*.md"))
        
        print(f"Processing {len(files_to_process)} files for fact extraction...")
        
        new_facts = []
        for file_path in files_to_process:
            if self._should_skip_file(file_path):
                continue
            
            file_facts = self._extract_facts_from_file(file_path)
            new_facts.extend(file_facts)
        
        # Merge with existing facts
        existing_ids = set(fact.claim_id for fact in self.facts)
        unique_new_facts = [fact for fact in new_facts if fact.claim_id not in existing_ids]
        
        self.facts.extend(unique_new_facts)
        self._save_facts()
        
        print(f"✅ Extracted {len(unique_new_facts)} new facts ({len(self.facts)} total)")
        return len(unique_new_facts)
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during analysis"""
        skip_patterns = [
            'backup', '.backup', 'archive', 'template', 'README',
            'index', 'hub', 'report', 'log', 'interface'
        ]
        
        file_str = str(file_path).lower()
        return any(pattern in file_str for pattern in skip_patterns)
    
    def _extract_facts_from_file(self, file_path: Path) -> List[FactClaim]:
        """Extract facts from a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return []
        
        if len(content.strip()) < 50:
            return []
        
        facts = []
        lines = content.split('\n')
        
        # Patterns for fact extraction
        patterns = [
            # Character facts
            (r'(\w+(?:\s+\w+)*)\s+(?:is|was)\s+([\w\s,]+)', 'character_trait'),
            (r'(\w+(?:\s+\w+)*)\s+(?:rules?|leads?|commands?)\s+([\w\s,]+)', 'leadership'),
            (r'(\w+(?:\s+\w+)*)\s+(?:age|aged)\s*:?\s*(\d+)', 'age'),
            (r'(\w+(?:\s+\w+)*)\s+(?:died|was killed|deceased)\s*(?:in|during)?\s*([\w\s,]*)', 'death'),
            
            # Location facts
            (r'(\w+(?:\s+\w+)*)\s+(?:located|situated|found)\s+(?:in|at|on)\s+([\w\s,]+)', 'location'),
            (r'(\w+(?:\s+\w+)*)\s+(?:contains|houses|holds)\s+([\w\s,]+)', 'contents'),
            
            # Relationship facts
            (r'(\w+(?:\s+\w+)*)\s+(?:allied with|enemies of|opposes?)\s+([\w\s,]+)', 'relationship'),
            (r'(\w+(?:\s+\w+)*)\s+(?:supports?|backs?)\s+([\w\s,]+)', 'support'),
            
            # Event facts
            (r'(?:in|during)\s+(\w+(?:\s+\w+)*),?\s+(\w+(?:\s+\w+)*)\s+(?:happened|occurred|took place)', 'event_timing'),
            (r'(\w+(?:\s+\w+)*)\s+(?:before|after)\s+(\w+(?:\s+\w+)*)', 'sequence')
        ]
        
        for line_num, line in enumerate(lines, 1):
            # Skip markdown formatting and very short lines
            clean_line = re.sub(r'^#+\s*|^\*+\s*|^-+\s*|\[([^\]]+)\]|\*\*([^*]+)\*\*', '', line).strip()
            if len(clean_line) < 10:
                continue
            
            for pattern, fact_type in patterns:
                matches = re.finditer(pattern, clean_line, re.IGNORECASE)
                for match in matches:
                    subject = match.group(1).strip()
                    predicate = fact_type
                    object_val = match.group(2).strip() if len(match.groups()) > 1 else ""
                    
                    # Create fact claim
                    claim_id = f"{file_path.stem}_{line_num}_{len(facts)}"
                    fact = FactClaim(
                        claim_id=claim_id,
                        source_file=str(file_path.relative_to(VAULT_ROOT)),
                        claim_text=match.group(0),
                        subject=subject,
                        predicate=predicate,
                        object=object_val,
                        confidence=0.7,  # Default confidence
                        context=clean_line,
                        line_number=line_num,
                        timestamp=datetime.now().isoformat()
                    )
                    facts.append(fact)
        
        return facts
    
    def detect_contradictions(self) -> List[Contradiction]:
        """Detect contradictions between facts"""
        print("🔍 Analyzing facts for contradictions...")
        
        new_contradictions = []
        
        # Group facts by subject for easier comparison
        facts_by_subject = defaultdict(list)
        for fact in self.facts:
            facts_by_subject[fact.subject.lower()].append(fact)
        
        # Check each subject's facts for contradictions
        for subject, subject_facts in facts_by_subject.items():
            contradictions = self._find_contradictions_in_subject(subject_facts)
            new_contradictions.extend(contradictions)
        
        # Add cross-subject contradictions
        cross_contradictions = self._find_cross_subject_contradictions()
        new_contradictions.extend(cross_contradictions)
        
        # Filter out existing contradictions
        existing_ids = set(contra.contradiction_id for contra in self.contradictions)
        unique_contradictions = [contra for contra in new_contradictions 
                               if contra.contradiction_id not in existing_ids]
        
        self.contradictions.extend(unique_contradictions)
        self._save_contradictions()
        
        print(f"✅ Found {len(unique_contradictions)} new contradictions")
        return unique_contradictions
    
    def _find_contradictions_in_subject(self, facts: List[FactClaim]) -> List[Contradiction]:
        """Find contradictions within facts about the same subject"""
        contradictions = []
        
        for i, fact1 in enumerate(facts):
            for fact2 in facts[i+1:]:
                contradiction = self._analyze_fact_pair(fact1, fact2)
                if contradiction:
                    contradictions.append(contradiction)
        
        return contradictions
    
    def _analyze_fact_pair(self, fact1: FactClaim, fact2: FactClaim) -> Optional[Contradiction]:
        """Analyze two facts for potential contradiction"""
        # Skip if same file (might be intentional development)
        if fact1.source_file == fact2.source_file:
            return None
        
        # Check for direct contradictions
        contradiction = None
        
        # Death vs. alive contradictions
        if ((fact1.predicate == 'death' and fact2.predicate in ['leadership', 'character_trait']) or
            (fact2.predicate == 'death' and fact1.predicate in ['leadership', 'character_trait'])):
            
            # Check if death fact comes chronologically before the other
            death_fact = fact1 if fact1.predicate == 'death' else fact2
            life_fact = fact2 if fact1.predicate == 'death' else fact1
            
            contradiction = Contradiction(
                contradiction_id=f"death_contradiction_{fact1.claim_id}_{fact2.claim_id}",
                claim1=death_fact,
                claim2=life_fact,
                contradiction_type="character",
                severity="high",
                description=f"{fact1.subject} appears both dead and alive in different sources",
                suggested_resolution=f"Verify the chronology and update content to reflect correct status",
                auto_resolvable=False
            )
        
        # Age contradictions
        elif fact1.predicate == 'age' and fact2.predicate == 'age':
            age1 = re.search(r'\d+', fact1.object)
            age2 = re.search(r'\d+', fact2.object)
            
            if age1 and age2:
                age_diff = abs(int(age1.group()) - int(age2.group()))
                if age_diff > 5:  # Significant age difference
                    contradiction = Contradiction(
                        contradiction_id=f"age_contradiction_{fact1.claim_id}_{fact2.claim_id}",
                        claim1=fact1,
                        claim2=fact2,
                        contradiction_type="character",
                        severity="medium",
                        description=f"{fact1.subject}'s age differs significantly between sources ({fact1.object} vs {fact2.object})",
                        suggested_resolution="Verify correct age and update inconsistent references",
                        auto_resolvable=True
                    )
        
        # Relationship contradictions
        elif fact1.predicate == 'relationship' and fact2.predicate == 'relationship':
            # Simple check for opposing relationships
            opposing_pairs = [
                ('allied', 'enemies'),
                ('supports', 'opposes'),
                ('friend', 'enemy')
            ]
            
            obj1_lower = fact1.object.lower()
            obj2_lower = fact2.object.lower()
            
            for term1, term2 in opposing_pairs:
                if ((term1 in obj1_lower and term2 in obj2_lower) or
                    (term2 in obj1_lower and term1 in obj2_lower)):
                    
                    contradiction = Contradiction(
                        contradiction_id=f"relationship_contradiction_{fact1.claim_id}_{fact2.claim_id}",
                        claim1=fact1,
                        claim2=fact2,
                        contradiction_type="relationship",
                        severity="medium",
                        description=f"{fact1.subject} has contradictory relationships: {fact1.object} vs {fact2.object}",
                        suggested_resolution="Determine correct relationship status and update accordingly",
                        auto_resolvable=False
                    )
                    break
        
        return contradiction
    
    def _find_cross_subject_contradictions(self) -> List[Contradiction]:
        """Find contradictions between different subjects"""
        # This is a placeholder for more complex cross-subject analysis
        # Could include temporal contradictions, power structure contradictions, etc.
        return []
    
    def check_lore_compliance(self) -> List[LoreViolation]:
        """Check content against lore consistency rules"""
        print("📋 Checking lore compliance...")
        
        new_violations = []
        
        # Get all content files again for rule checking
        content_dirs = [
            VAULT_ROOT / "02_Worldbuilding",
            VAULT_ROOT / "01_Adventures", 
            VAULT_ROOT / "1-Session Journals"
        ]
        
        files_to_check = []
        for content_dir in content_dirs:
            if content_dir.exists():
                files_to_check.extend(content_dir.rglob("*.md"))
        
        # Check each file against each active rule
        for file_path in files_to_check:
            if self._should_skip_file(file_path):
                continue
            
            file_violations = self._check_file_against_rules(file_path)
            new_violations.extend(file_violations)
        
        # Filter out existing violations
        existing_ids = set(viol.violation_id for viol in self.violations)
        unique_violations = [viol for viol in new_violations 
                           if viol.violation_id not in existing_ids]
        
        self.violations.extend(unique_violations)
        self._save_violations()
        
        print(f"✅ Found {len(unique_violations)} lore compliance issues")
        return unique_violations
    
    def _check_file_against_rules(self, file_path: Path) -> List[LoreViolation]:
        """Check a file against all consistency rules"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return []
        
        violations = []
        lines = content.split('\n')
        
        for rule in self.rules:
            if not rule.active:
                continue
            
            # Check rule pattern against content
            for line_num, line in enumerate(lines, 1):
                matches = re.finditer(rule.pattern, line, re.IGNORECASE)
                for match in matches:
                    # For now, we'll create a violation for each match
                    # In a full implementation, we'd have more sophisticated rule logic
                    violation_id = f"{rule.rule_id}_{file_path.stem}_{line_num}"
                    
                    suggested_fix = self._generate_fix_suggestion(rule, match.group(0), line)
                    
                    violation = LoreViolation(
                        violation_id=violation_id,
                        rule=rule,
                        source_file=str(file_path.relative_to(VAULT_ROOT)),
                        violation_text=match.group(0),
                        line_number=line_num,
                        severity=rule.severity,
                        suggested_fix=suggested_fix
                    )
                    violations.append(violation)
        
        return violations
    
    def _generate_fix_suggestion(self, rule: ConsistencyRule, violation_text: str, context: str) -> str:
        """Generate a fix suggestion for a lore violation"""
        if rule.rule_type == "character_trait":
            return f"Verify that '{violation_text}' is consistent with established character information"
        elif rule.rule_type == "world_law":
            return f"Ensure '{violation_text}' follows established world mechanics and laws"
        elif rule.rule_type == "timeline":
            return f"Check chronological consistency of '{violation_text}' with established timeline"
        elif rule.rule_type == "relationship":
            return f"Verify relationship consistency: '{violation_text}'"
        else:
            return f"Review '{violation_text}' for consistency with established lore"
    
    def generate_consistency_report(self) -> str:
        """Generate comprehensive consistency report"""
        report = "# Narrative Consistency Report\n\n"
        report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Summary
        report += "## Summary\n\n"
        report += f"- **Total Facts Extracted:** {len(self.facts)}\n"
        report += f"- **Contradictions Found:** {len(self.contradictions)}\n"
        report += f"- **Lore Violations:** {len(self.violations)}\n"
        report += f"- **Active Rules:** {sum(1 for rule in self.rules if rule.active)}\n\n"
        
        # Contradictions by severity
        if self.contradictions:
            contra_by_severity = Counter(contra.severity for contra in self.contradictions)
            report += "### Contradictions by Severity\n\n"
            for severity in ['critical', 'high', 'medium', 'low']:
                count = contra_by_severity.get(severity, 0)
                if count > 0:
                    report += f"- **{severity.title()}:** {count}\n"
            report += "\n"
        
        # Top contradictions
        if self.contradictions:
            report += "## Critical Contradictions\n\n"
            critical_contras = [c for c in self.contradictions if c.severity in ['critical', 'high']][:5]
            
            for contra in critical_contras:
                report += f"### {contra.contradiction_type.title()} Contradiction\n"
                report += f"**Severity:** {contra.severity.title()}\n"
                report += f"**Description:** {contra.description}\n\n"
                report += f"**Conflicting Claims:**\n"
                report += f"1. {contra.claim1.claim_text} ({contra.claim1.source_file})\n"
                report += f"2. {contra.claim2.claim_text} ({contra.claim2.source_file})\n\n"
                report += f"**Suggested Resolution:** {contra.suggested_resolution}\n\n"
                report += "---\n\n"
        
        # Lore violations
        if self.violations:
            report += "## Lore Compliance Issues\n\n"
            high_violations = [v for v in self.violations if v.severity in ['critical', 'high']][:5]
            
            for violation in high_violations:
                report += f"### {violation.rule.description}\n"
                report += f"**File:** {violation.source_file}:{violation.line_number}\n"
                report += f"**Violation:** {violation.violation_text}\n"
                report += f"**Suggested Fix:** {violation.suggested_fix}\n\n"
                report += "---\n\n"
        
        # Recommendations
        report += "## Recommendations\n\n"
        
        if len(self.contradictions) > 0:
            report += f"1. **Address High-Priority Contradictions:** Review and resolve {len([c for c in self.contradictions if c.severity in ['critical', 'high']])} high-priority contradictions\n"
        
        if len(self.violations) > 0:
            report += f"2. **Fix Lore Violations:** Update content to address {len(self.violations)} lore compliance issues\n"
        
        report += "3. **Regular Consistency Checks:** Run consistency analysis after major content updates\n"
        report += "4. **Update Rules:** Review and refine consistency rules based on campaign development\n\n"
        
        return report
    
    def export_analysis_data(self, format_type: str = "json") -> str:
        """Export complete analysis data"""
        if format_type == "json":
            data = {
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_facts': len(self.facts),
                    'total_contradictions': len(self.contradictions),
                    'total_violations': len(self.violations),
                    'active_rules': sum(1 for rule in self.rules if rule.active)
                },
                'contradictions_by_severity': dict(Counter(c.severity for c in self.contradictions)),
                'violations_by_severity': dict(Counter(v.severity for v in self.violations)),
                'facts_by_type': dict(Counter(f.predicate for f in self.facts)),
                'critical_issues': {
                    'contradictions': [
                        {
                            'id': c.contradiction_id,
                            'type': c.contradiction_type,
                            'severity': c.severity,
                            'description': c.description
                        }
                        for c in self.contradictions if c.severity in ['critical', 'high']
                    ][:10],
                    'violations': [
                        {
                            'id': v.violation_id,
                            'rule_type': v.rule.rule_type,
                            'severity': v.severity,
                            'file': v.source_file
                        }
                        for v in self.violations if v.severity in ['critical', 'high']
                    ][:10]
                }
            }
            
            return json.dumps(data, indent=2)
        
        return "Unsupported format"

def main():
    parser = argparse.ArgumentParser(description="Narrative Consistency AI - Detect contradictions and lore violations")
    parser.add_argument('command', choices=['extract', 'check', 'analyze', 'report', 'export'])
    
    parser.add_argument('--force', action='store_true', help='Force full analysis')
    parser.add_argument('--format', default='json', help='Export format')
    
    args = parser.parse_args()
    
    ai = NarrativeConsistencyAI()
    
    if args.command == 'extract':
        count = ai.extract_facts_from_content(args.force)
        print(f"📊 Fact extraction complete: {count} new facts added")
        
    elif args.command == 'check':
        contradictions = ai.detect_contradictions()
        violations = ai.check_lore_compliance()
        
        print(f"\n🔍 **Consistency Check Results:**")
        print(f"- **New Contradictions:** {len(contradictions)}")
        print(f"- **New Violations:** {len(violations)}")
        
        if contradictions:
            print(f"\n**Critical Contradictions:**")
            for contra in [c for c in contradictions if c.severity in ['critical', 'high']][:3]:
                print(f"- {contra.description}")
        
        if violations:
            print(f"\n**Major Lore Issues:**")
            for viol in [v for v in violations if v.severity in ['critical', 'high']][:3]:
                print(f"- {viol.rule.description}: {viol.source_file}")
    
    elif args.command == 'analyze':
        # Full analysis
        ai.extract_facts_from_content(args.force)
        contradictions = ai.detect_contradictions()
        violations = ai.check_lore_compliance()
        
        print(f"\n📊 **Full Analysis Complete:**")
        print(f"- **Total Facts:** {len(ai.facts)}")
        print(f"- **Contradictions:** {len(ai.contradictions)}")
        print(f"- **Lore Violations:** {len(ai.violations)}")
        print(f"- **Active Rules:** {sum(1 for rule in ai.rules if rule.active)}")
    
    elif args.command == 'report':
        report = ai.generate_consistency_report()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = CONSISTENCY_DATA_DIR / f"consistency_report_{timestamp}.md"
        
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"✅ Consistency report generated: {filename}")
        print(f"\nPreview:\n{report[:500]}...")
    
    elif args.command == 'export':
        data = ai.export_analysis_data(args.format)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = CONSISTENCY_DATA_DIR / f"consistency_export_{timestamp}.{args.format}"
        
        with open(filename, 'w') as f:
            f.write(data)
        
        print(f"✅ Analysis data exported: {filename}")

if __name__ == "__main__":
    main()