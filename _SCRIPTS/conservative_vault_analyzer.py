#!/usr/bin/env python3
"""
Obsidian Vault TTRPG File Analyzer - Conservative Edition
Preserves quality content while identifying truly vestigial files
Philosophy: When in doubt, keep it. Your campaign notes are irreplaceable.
"""

import os
import re
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
from difflib import SequenceMatcher
from enum import Enum
import zipfile

# Try to import frontmatter, provide fallback if not available
try:
    import frontmatter
except ImportError:
    print("Warning: frontmatter not installed. Install with: pip3 install python-frontmatter")
    frontmatter = None

# CONSERVATIVE THRESHOLDS - We want to be VERY sure before archiving anything
MINIMUM_WORDS_FOR_CONTENT = 10  # Even 10 words might be a useful NPC name + description
PLACEHOLDER_THRESHOLD = 0.8  # File must be 80% placeholders to consider archiving
ABANDONMENT_DAYS = 365  # Only flag as abandoned after a full year
DUPLICATE_THRESHOLD = 0.95  # Must be nearly identical to flag as duplicate

class ContentType(str, Enum):
    """Content types specific to TTRPG management"""
    NPC = "npc"
    LOCATION = "location"
    ITEM = "item"
    SPELL = "spell"
    MONSTER = "monster"
    LORE = "lore"
    SESSION = "session"
    RULES = "rules"
    QUEST = "quest"
    PLAYER = "player"
    ENCOUNTER = "encounter"
    ORGANIZATION = "organization"
    DEITY = "deity"
    RANDOM_TABLE = "random_table"
    UNKNOWN = "unknown"

class FileAction(str, Enum):
    """Conservative action recommendations"""
    KEEP = "keep"  # Default - when in doubt, keep it
    ARCHIVE_CANDIDATE = "archive_candidate"  # Suggest for archive but require confirmation
    MERGE_CANDIDATE = "merge_candidate"  # Suggest merging with another file
    RENAME = "rename"  # Just needs renaming (path issues)
    ENRICH = "enrich"  # File needs more content but has good foundation
    REVIEW = "review"  # Manual review needed

class FileMetrics:
    """
    Complete metrics for analyzing vault files.
    Each metric helps identify whether a file contains valuable campaign content
    or is truly vestigial.
    """
    
    def __init__(self, filepath: Path, content: str, frontmatter_data: dict = None):
        self.filepath = filepath
        self.filename = filepath.stem
        self.content = content
        self.frontmatter = frontmatter_data or {}
        
        # Content Structure Metrics (1-6)
        self.word_count = 0
        self.heading_depth = 0
        self.internal_links = []
        self.orphan_status = True
        self.tags = []
        self.completion_markers = []
        
        # TTRPG Classification (7-10)
        self.content_type = ContentType.UNKNOWN
        self.campaign = None
        self.world_region = None
        self.timeline_markers = []
        
        # Game Mechanics (11-16)
        self.stat_block_complete = 0.0
        self.rules_references = []
        self.cr_mentions = []
        self.dice_notations = []
        self.spell_levels = []
        self.magic_item_rarity = None
        
        # Narrative Quality (17-21)
        self.description_ratio = 0.0
        self.sensory_details = {
            "sight": 0, "sound": 0, "smell": 0, "touch": 0, "taste": 0
        }
        self.plot_hooks = []
        self.dialogue_count = 0
        self.secrets_count = 0
        
        # Usability (22-26)
        self.tables_count = 0
        self.read_aloud_blocks = 0
        self.quick_ref_sections = 0
        self.embedded_images = 0
        self.session_readiness = 0.0
        
        # Interconnectedness (27-30)
        self.npc_links = []
        self.location_links = []
        self.quest_connections = []
        self.pc_mentions = []
        
        # Vestigial Detection (31-35)
        self.days_since_modified = 0
        self.empty_ratio = 0.0
        self.placeholder_ratio = 0.0
        self.template_remnants = []
        self.broken_links = []
        
        # Duplicate Detection (36-40)
        self.title_similarity_matches = []
        self.content_hash = ""
        self.substring_title_issues = []
        self.duplicate_stat_blocks = []
        self.content_overlap_files = []
        
        # Path & Naming Issues (41-45)
        self.path_in_title = False
        self.unnecessary_nesting = False
        self.redundant_folder_context = False
        self.special_char_issues = []
        self.case_inconsistent = False
        
        # Structural Problems (46-50)
        self.single_link_orphan = False
        self.circular_only = False
        self.is_meta_note = False
        self.abandoned_draft_days = None
        self.import_artifacts = []
        
        # Quality indicators - reasons to KEEP a file
        self.has_unique_content = False
        self.has_player_notes = False
        self.has_worldbuilding = False
        self.has_mechanics = False
        self.has_future_plans = False
    
    @property
    def preservation_score(self) -> float:
        """
        Score from 0-1 indicating how important it is to preserve this file.
        Higher = more important to keep.
        """
        score = 0.0
        
        # Content existence is valuable
        if self.word_count > 50:
            score += 0.2
        elif self.word_count > 10:
            score += 0.1
            
        # Game mechanics are always valuable
        if self.dice_notations or self.cr_mentions or self.spell_levels:
            score += 0.3
            
        # Narrative content is precious
        if self.dialogue_count > 0 or self.secrets_count > 0:
            score += 0.2
            
        # Sensory details indicate crafted content
        total_sensory = sum(self.sensory_details.values())
        if total_sensory > 5:
            score += 0.2
            
        # Connected files are part of the world
        if self.internal_links:
            score += 0.1
            
        # Player-facing content is critical
        if self.pc_mentions or self.read_aloud_blocks:
            score += 0.3
            
        # Images and tables took effort
        if self.embedded_images or self.tables_count:
            score += 0.2
            
        return min(1.0, score)
    
    @property
    def recommended_action(self) -> FileAction:
        """
        VERY conservative recommendation system.
        We err on the side of keeping content.
        """
        # Check for quality content FIRST - if it exists, always keep
        if self.preservation_score > 0.3:
            return FileAction.KEEP
            
        # Even with low preservation score, be very careful
        if self.word_count < MINIMUM_WORDS_FOR_CONTENT:
            # But wait - does it have ANY game content?
            if self.dice_notations or self.cr_mentions or self.internal_links:
                return FileAction.ENRICH  # Has potential, needs expansion
            # Check if it's a placeholder file from an empty link
            if self.single_link_orphan and not self.frontmatter:
                return FileAction.ARCHIVE_CANDIDATE
        
        # High placeholder ratio AND old AND minimal content
        if (self.placeholder_ratio > PLACEHOLDER_THRESHOLD and 
            self.days_since_modified > ABANDONMENT_DAYS and
            self.word_count < 50):
            return FileAction.ARCHIVE_CANDIDATE
            
        # Near-duplicate content
        if self.content_overlap_files:
            best_match = max(self.content_overlap_files, key=lambda x: x[1])
            if best_match[1] > DUPLICATE_THRESHOLD:
                return FileAction.MERGE_CANDIDATE
                
        # Path issues are just rename candidates
        if self.path_in_title or self.unnecessary_nesting:
            return FileAction.RENAME
            
        # Meta notes might be useful for organization
        if self.is_meta_note:
            return FileAction.REVIEW
            
        # Default to keeping
        return FileAction.KEEP

class VaultAnalyzer:
    """
    Conservative analyzer that preserves campaign content
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.files = {}
        self.link_graph = defaultdict(set)
        
        print(f"Initializing conservative analyzer for: {vault_path}")
        print("Philosophy: Preserve quality content, only flag truly vestigial files")
        
        # Compile regex patterns for efficiency
        self.patterns = self._compile_patterns()
        self.sensory_patterns = self._compile_sensory_patterns()
        
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """
        Compile all regex patterns once for performance.
        These patterns help identify TTRPG-specific content.
        """
        return {
            'wiki_link': re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'),
            'tag': re.compile(r'#[\w/\-]+'),
            'dice': re.compile(r'\b\d*d\d+(?:[+-]\d+)?\b'),
            'spell_level': re.compile(r'\b(?:cantrip|[1-9](?:st|nd|rd|th)[\- ]level)\b', re.IGNORECASE),
            'cr': re.compile(r'\bCR\s*\d+(?:/\d+)?\b', re.IGNORECASE),
            'dialogue': re.compile(r'"[^"]{10,}"'),  # At least 10 chars suggests real dialogue
            'secret': re.compile(r'(?:DM\s*(?:only|note|secret)|hidden|spoiler|reveal)', re.IGNORECASE),
            'placeholder': re.compile(r'\b(?:TODO|TBD|WIP|FIXME|XXX|COMING\s*SOON|PLACEHOLDER)\b', re.IGNORECASE),
            'template_var': re.compile(r'{{[^}]+}}|<%[^%]+%>'),
            'read_aloud': re.compile(r'(?:read\s*aloud|boxed\s*text|narration):', re.IGNORECASE),
            'import_artifact': re.compile(r'(?:Source:|Imported from|©|All rights reserved|D&D Beyond)', re.IGNORECASE),
            
            # Additional patterns for preserving content
            'player_mention': re.compile(r'\b(?:player|PC|character)\s+(?:name|called|known as)\b', re.IGNORECASE),
            'future_plan': re.compile(r'\b(?:next\s+session|upcoming|planned|future|eventually|later)\b', re.IGNORECASE),
            'worldbuilding': re.compile(r'\b(?:history|culture|tradition|religion|pantheon|creation|founding)\b', re.IGNORECASE),
            'heading': re.compile(r'^#+\s+(.+)$', re.MULTILINE),
            'table': re.compile(r'^\|.*\|.*\|', re.MULTILINE),
            'image': re.compile(r'!\[\[([^\]]+)\]\]|!\[([^\]]*)\]\(([^)]+)\)'),
        }
    
    def _compile_sensory_patterns(self) -> Dict[str, re.Pattern]:
        """Compile patterns for sensory details"""
        return {
            'sight': re.compile(r'\b(?:see|saw|look|appear|visible|color|bright|dark|shadow|light)\b', re.IGNORECASE),
            'sound': re.compile(r'\b(?:hear|heard|sound|noise|quiet|loud|echo|whisper|roar|clatter)\b', re.IGNORECASE),
            'smell': re.compile(r'\b(?:smell|scent|odor|aroma|stench|fragran|reek|musty|fresh)\b', re.IGNORECASE),
            'touch': re.compile(r'\b(?:feel|felt|touch|rough|smooth|cold|warm|wet|dry|soft|hard)\b', re.IGNORECASE),
            'taste': re.compile(r'\b(?:taste|flavor|sweet|sour|bitter|salty|savory|delicious|disgusting)\b', re.IGNORECASE),
        }
    
    def analyze_file(self, filepath: Path) -> Optional[FileMetrics]:
        """
        Analyze a single file with focus on preserving valuable content
        """
        relative_path = filepath.relative_to(self.vault_path)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                if frontmatter:
                    post = frontmatter.load(f)
                    content = post.content
                    fm_data = post.metadata
                else:
                    content = f.read()
                    fm_data = {}
        except Exception as e:
            print(f"    Warning: Could not read {relative_path}: {e}")
            return None
        
        metrics = FileMetrics(filepath, content, fm_data)
        
        # CHECK FOR QUALITY CONTENT INDICATORS FIRST
        # This is crucial - we want to identify value early
        
        # 1. Check for player-created content (always valuable)
        if 'author' in fm_data or 'player' in fm_data:
            metrics.has_player_notes = True
            
        # 2. Check for worldbuilding
        if self.patterns['worldbuilding'].search(content):
            metrics.has_worldbuilding = True
            
        # 3. Check for future campaign plans
        if self.patterns['future_plan'].search(content):
            metrics.has_future_plans = True
            
        # 4. Check for unique NPCs or locations
        # Even a single named entity makes a file worth keeping
        proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        if len(proper_nouns) > 2:  # More than just a title
            metrics.has_unique_content = True
        
        # Basic content metrics
        metrics.word_count = len(content.split())
        
        # Find headings and their depth
        headings = self.patterns['heading'].findall(content)
        if headings:
            metrics.heading_depth = max(len(h) - len(h.lstrip('#')) for h in headings)
        
        # Find internal links
        metrics.internal_links = self.patterns['wiki_link'].findall(content)
        
        # Find tags
        metrics.tags = self.patterns['tag'].findall(content)
        
        # Detect dice notations (critical for game content)
        metrics.dice_notations = self.patterns['dice'].findall(content)
        
        # Detect CR mentions
        metrics.cr_mentions = self.patterns['cr'].findall(content)
        
        # Detect spell levels
        spell_matches = self.patterns['spell_level'].findall(content)
        metrics.spell_levels = spell_matches
        
        # Count dialogue
        metrics.dialogue_count = len(self.patterns['dialogue'].findall(content))
        
        # Count secrets
        metrics.secrets_count = len(self.patterns['secret'].findall(content))
        
        # Count tables
        metrics.tables_count = len(self.patterns['table'].findall(content))
        
        # Count images
        metrics.embedded_images = len(self.patterns['image'].findall(content))
        
        # Count read-aloud blocks
        metrics.read_aloud_blocks = len(self.patterns['read_aloud'].findall(content))
        
        # Detect sensory details
        for sense, pattern in self.sensory_patterns.items():
            metrics.sensory_details[sense] = len(pattern.findall(content))
        
        # Check for placeholders
        placeholders = self.patterns['placeholder'].findall(content)
        if metrics.word_count > 0:
            metrics.placeholder_ratio = len(placeholders) / max(1, metrics.word_count // 10)
        
        # Check for template remnants
        metrics.template_remnants = self.patterns['template_var'].findall(content)
        
        # Check for import artifacts
        metrics.import_artifacts = self.patterns['import_artifact'].findall(content)
        
        # Calculate days since modified
        try:
            mod_time = os.path.getmtime(filepath)
            metrics.days_since_modified = (datetime.now() - datetime.fromtimestamp(mod_time)).days
        except:
            metrics.days_since_modified = 0
        
        # Check for PC mentions
        metrics.pc_mentions = self.patterns['player_mention'].findall(content)
        
        # Detect content type based on path and content
        path_str = str(relative_path).lower()
        if 'npc' in path_str or 'character' in path_str:
            metrics.content_type = ContentType.NPC
        elif 'location' in path_str or 'place' in path_str:
            metrics.content_type = ContentType.LOCATION
        elif 'item' in path_str or 'equipment' in path_str:
            metrics.content_type = ContentType.ITEM
        elif 'spell' in path_str:
            metrics.content_type = ContentType.SPELL
        elif 'session' in path_str:
            metrics.content_type = ContentType.SESSION
        elif 'quest' in path_str or 'adventure' in path_str:
            metrics.content_type = ContentType.QUEST
        elif 'lore' in path_str or 'history' in path_str:
            metrics.content_type = ContentType.LORE
        elif 'rule' in path_str or 'mechanic' in path_str:
            metrics.content_type = ContentType.RULES
        
        # Generate content hash
        metrics.content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Check for path issues
        if '/' in metrics.filename or '\\' in metrics.filename:
            metrics.path_in_title = True
        
        # Check if file is in deeply nested folders
        if len(relative_path.parts) > 5:
            metrics.unnecessary_nesting = True
        
        # Check for special characters
        special_chars = re.findall(r'[^\w\s\-.]', metrics.filename)
        if special_chars:
            metrics.special_char_issues = special_chars
        
        return metrics
    
    def analyze_vault(self):
        """
        Analyze all markdown files in the vault
        """
        md_files = list(self.vault_path.rglob("*.md"))
        total_files = len(md_files)
        
        print(f"\nFound {total_files} markdown files to analyze")
        print("Analyzing files (this may take a moment)...")
        
        for i, filepath in enumerate(md_files, 1):
            if i % 100 == 0:
                print(f"  Progress: {i}/{total_files} files analyzed...")
            
            # Skip system files and backups
            if any(part.startswith('.') for part in filepath.parts):
                continue
            if 'backup' in str(filepath).lower() or 'archive' in str(filepath).lower():
                continue
            
            metrics = self.analyze_file(filepath)
            if metrics:
                file_key = str(filepath.relative_to(self.vault_path))
                self.files[file_key] = metrics
                
                # Build link graph
                for link in metrics.internal_links:
                    self.link_graph[file_key].add(link)
        
        print(f"✓ Analyzed {len(self.files)} files successfully")
        
        # Post-processing: identify orphans and duplicates
        self._identify_orphans()
        self._identify_duplicates()
    
    def _identify_orphans(self):
        """
        Identify orphaned files (not linked from anywhere)
        """
        linked_files = set()
        for links in self.link_graph.values():
            linked_files.update(links)
        
        for file_key, metrics in self.files.items():
            # Check if this file is linked from anywhere
            file_name = Path(file_key).stem
            if file_name in linked_files or file_key in linked_files:
                metrics.orphan_status = False
            
            # Check for single-link orphans (only linked once, possibly auto-created)
            link_count = sum(1 for links in self.link_graph.values() if file_name in links)
            if link_count == 1 and metrics.word_count < 50:
                metrics.single_link_orphan = True
    
    def _identify_duplicates(self):
        """
        Identify potential duplicate files
        """
        # Group files by content hash for exact duplicates
        hash_groups = defaultdict(list)
        for file_key, metrics in self.files.items():
            hash_groups[metrics.content_hash].append(file_key)
        
        # Check for similar content
        file_list = list(self.files.items())
        for i, (key1, metrics1) in enumerate(file_list):
            for key2, metrics2 in file_list[i+1:]:
                # Skip if files are very different in size
                if abs(metrics1.word_count - metrics2.word_count) > 100:
                    continue
                
                # Calculate similarity
                similarity = SequenceMatcher(None, metrics1.content, metrics2.content).ratio()
                if similarity > DUPLICATE_THRESHOLD:
                    metrics1.content_overlap_files.append((key2, similarity))
                    metrics2.content_overlap_files.append((key1, similarity))
    
    def generate_preservation_report(self) -> Dict:
        """
        Generate a detailed report that errs on the side of preservation
        """
        print("\n" + "="*60)
        print("PRESERVATION ANALYSIS")
        print("="*60)
        
        # Categorize files by action
        actions = defaultdict(list)
        preservation_stats = {
            'total_files': len(self.files),
            'high_value': 0,
            'medium_value': 0,
            'low_value': 0,
            'archive_candidates': 0
        }
        
        for metrics in self.files.values():
            actions[metrics.recommended_action].append(metrics)
            
            # Track preservation scores
            if metrics.preservation_score > 0.7:
                preservation_stats['high_value'] += 1
            elif metrics.preservation_score > 0.3:
                preservation_stats['medium_value'] += 1
            else:
                preservation_stats['low_value'] += 1
        
        preservation_stats['archive_candidates'] = len(actions[FileAction.ARCHIVE_CANDIDATE])
        
        # Print summary
        print(f"\n📊 File Categories:")
        print(f"  Keep: {len(actions[FileAction.KEEP])} files")
        print(f"  Enrich: {len(actions[FileAction.ENRICH])} files (have potential)")
        print(f"  Rename: {len(actions[FileAction.RENAME])} files (path issues)")
        print(f"  Review: {len(actions[FileAction.REVIEW])} files (need manual review)")
        print(f"  Merge Candidates: {len(actions[FileAction.MERGE_CANDIDATE])} files")
        print(f"  Archive Candidates: {len(actions[FileAction.ARCHIVE_CANDIDATE])} files")
        
        # CRITICAL: Review archive candidates manually
        if FileAction.ARCHIVE_CANDIDATE in actions:
            print(f"\n⚠️  ARCHIVE CANDIDATES ({len(actions[FileAction.ARCHIVE_CANDIDATE])} files)")
            print("These files MIGHT be vestigial, but please review each one:\n")
            
            for metrics in actions[FileAction.ARCHIVE_CANDIDATE][:10]:  # Show first 10
                print(f"  📄 {metrics.filepath.relative_to(self.vault_path)}")
                print(f"     Words: {metrics.word_count}")
                print(f"     Last modified: {metrics.days_since_modified} days ago")
                
                # Show a snippet of content for context
                snippet = metrics.content[:100].replace('\n', ' ').strip()
                if snippet:
                    print(f"     Content preview: '{snippet}...'")
                    
                # Explain WHY it's flagged
                reasons = []
                if metrics.word_count < MINIMUM_WORDS_FOR_CONTENT:
                    reasons.append("very short")
                if metrics.placeholder_ratio > PLACEHOLDER_THRESHOLD:
                    reasons.append(f"{metrics.placeholder_ratio:.0%} placeholders")
                if metrics.single_link_orphan:
                    reasons.append("single-link orphan")
                    
                print(f"     Flagged because: {', '.join(reasons)}")
                print(f"     Preservation score: {metrics.preservation_score:.2f}/1.00")
                
                # CHECK FOR HIDDEN VALUE
                if metrics.has_unique_content or metrics.has_worldbuilding:
                    print("     ⚠️  WARNING: Contains unique content - consider keeping!")
                
                print()
            
            if len(actions[FileAction.ARCHIVE_CANDIDATE]) > 10:
                print(f"  ... and {len(actions[FileAction.ARCHIVE_CANDIDATE]) - 10} more files")
        
        return {
            'actions': dict(actions),
            'stats': preservation_stats
        }
    
    def export_detailed_metrics(self, output_path: str):
        """
        Export detailed metrics to CSV for review
        """
        import csv
        
        with open(output_path, 'w', newline='') as f:
            fieldnames = [
                'File', 'Action', 'Preservation Score', 'Word Count',
                'Days Since Modified', 'Content Type', 'Has Unique Content',
                'Has Worldbuilding', 'Has Player Notes', 'Dice Notations',
                'Internal Links', 'Tags'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for file_key, metrics in self.files.items():
                writer.writerow({
                    'File': file_key,
                    'Action': metrics.recommended_action,
                    'Preservation Score': f"{metrics.preservation_score:.2f}",
                    'Word Count': metrics.word_count,
                    'Days Since Modified': metrics.days_since_modified,
                    'Content Type': metrics.content_type,
                    'Has Unique Content': metrics.has_unique_content,
                    'Has Worldbuilding': metrics.has_worldbuilding,
                    'Has Player Notes': metrics.has_player_notes,
                    'Dice Notations': len(metrics.dice_notations),
                    'Internal Links': len(metrics.internal_links),
                    'Tags': len(metrics.tags)
                })
        
        print(f"✓ Exported detailed metrics to {output_path}")
    
    def archive_files(self, files_to_archive: List[FileMetrics], archive_name: str):
        """
        Archive files to a zip file
        """
        archive_path = self.vault_path / archive_name
        
        with zipfile.ZipFile(archive_path, 'w') as zf:
            for metrics in files_to_archive:
                # Add file to archive
                arcname = str(metrics.filepath.relative_to(self.vault_path))
                zf.write(metrics.filepath, arcname)
                
                # Remove original file
                metrics.filepath.unlink()
                print(f"   ✓ Archived: {arcname}")
        
        print(f"\n✓ Created archive: {archive_name}")
        print(f"  Contains {len(files_to_archive)} files")
    
    def execute_cleanup(self, dry_run: bool = True, require_confirmation: bool = True):
        """
        Execute cleanup with multiple safety checks
        """
        if not dry_run:
            print("\n" + "="*60)
            print("⚠️  REAL EXECUTION MODE - FILES WILL BE MODIFIED")
            print("="*60)
            
            if require_confirmation:
                backup_prompt = input("\nHave you created a backup? (yes/no): ")
                if backup_prompt.lower() != 'yes':
                    print("❌ Aborting - Please backup your vault first!")
                    print(f"   Run: cp -r '{self.vault_path}' '{self.vault_path}_backup'")
                    return
                
                confirm = input("\nType 'PRESERVE MY CAMPAIGN' to proceed: ")
                if confirm != 'PRESERVE MY CAMPAIGN':
                    print("❌ Aborting - Confirmation not received")
                    return
        
        report = self.generate_preservation_report()
        actions = report['actions']
        
        # 1. RENAME operations are safe
        if FileAction.RENAME in actions:
            print(f"\n📝 Renaming {len(actions[FileAction.RENAME])} files with path issues...")
            for metrics in actions[FileAction.RENAME]:
                old_path = metrics.filepath
                # Clean up the filename
                new_name = metrics.filename
                new_name = re.sub(r'[-_/\\]+', ' ', new_name).strip()
                new_name = re.sub(r'\s+', ' ', new_name)
                
                if not dry_run:
                    new_path = old_path.parent / f"{new_name}.md"
                    if not new_path.exists():
                        old_path.rename(new_path)
                        print(f"   ✓ Renamed: {old_path.name} → {new_path.name}")
                else:
                    print(f"   Would rename: {old_path.name} → {new_name}.md")
        
        # 2. ARCHIVE CANDIDATES require manual review
        if FileAction.ARCHIVE_CANDIDATE in actions:
            candidates = actions[FileAction.ARCHIVE_CANDIDATE]
            
            print(f"\n📦 Archive Candidates: {len(candidates)} files")
            
            if not dry_run:
                print("Would you like to review each file individually? (recommended)")
                
                review_each = input("Review each file? (yes/no): ").lower() == 'yes'
                
                to_archive = []
                
                if review_each:
                    for metrics in candidates:
                        print(f"\n📄 {metrics.filepath.name}")
                        print(f"   Content: {metrics.content[:200]}...")
                        action = input("   Archive this file? (y/n/skip all): ").lower()
                        
                        if action == 'y':
                            to_archive.append(metrics)
                        elif action == 'skip all':
                            break
                else:
                    # Archive all candidates - but with a strong warning
                    print("\n⚠️  WARNING: Archiving without review is risky!")
                    confirm = input("Type 'ARCHIVE ALL' to proceed: ")
                    if confirm == 'ARCHIVE ALL':
                        to_archive = candidates
                
                if to_archive:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    archive_name = f"vault_archive_{timestamp}.zip"
                    self.archive_files(to_archive, archive_name)
            else:
                print("   (Dry run - no files would be archived)")
        
        # 3. MERGE CANDIDATES need careful handling
        if FileAction.MERGE_CANDIDATE in actions:
            print(f"\n🔀 Merge Candidates: {len(actions[FileAction.MERGE_CANDIDATE])} files")
            print("These files appear to be duplicates.")
            print("Manual review recommended - merging will be skipped in automated mode")
            
            for metrics in actions[FileAction.MERGE_CANDIDATE][:5]:  # Show first 5
                if metrics.content_overlap_files:
                    similar_to, score = metrics.content_overlap_files[0]
                    print(f"   {metrics.filename} ≈ {Path(similar_to).stem} ({score:.0%} similar)")
        
        # Final summary
        print("\n" + "="*60)
        print("PRESERVATION SUMMARY")
        print("="*60)
        print(f"Total files analyzed: {report['stats']['total_files']}")
        print(f"High value content: {report['stats']['high_value']} files")
        print(f"Medium value content: {report['stats']['medium_value']} files")
        print(f"Low value content: {report['stats']['low_value']} files")
        print(f"Archive candidates: {report['stats']['archive_candidates']} files")
        
        if not dry_run:
            print("\n✅ Cleanup complete - your campaign content has been preserved!")
        else:
            print("\n💡 This was a dry run. Use --execute to perform actual cleanup")
            print("   Remember: When in doubt, keep the file!")

def main():
    """
    Main execution with safety-first approach
    """
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Conservative TTRPG Vault Analyzer - Preserves Quality Content"
    )
    parser.add_argument("vault_path", help="Path to your Obsidian vault")
    parser.add_argument("--execute", action="store_true", 
                       help="Actually perform cleanup (dry run by default)")
    parser.add_argument("--skip-confirmation", action="store_true",
                       help="Skip confirmation prompts (dangerous!)")
    parser.add_argument("--export-metrics", help="Export detailed metrics to CSV")
    
    args = parser.parse_args()
    
    print("🎲 TTRPG Vault Analyzer - Conservative Edition")
    print("=" * 60)
    print(f"Vault: {args.vault_path}")
    print(f"Mode: {'EXECUTE' if args.execute else 'DRY RUN'}")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = VaultAnalyzer(args.vault_path)
    
    # Run analysis
    print("\nPhase 1: Analyzing files...")
    analyzer.analyze_vault()
    
    # Export metrics if requested
    if args.export_metrics:
        print(f"\nExporting metrics to {args.export_metrics}...")
        analyzer.export_detailed_metrics(args.export_metrics)
    
    # Generate preservation report
    print("\nPhase 2: Generating preservation report...")
    report = analyzer.generate_preservation_report()
    
    # Execute cleanup
    print("\nPhase 3: Cleanup recommendations...")
    analyzer.execute_cleanup(
        dry_run=not args.execute,
        require_confirmation=not args.skip_confirmation
    )
    
    print("\n✨ Analysis complete!")
    print("\nRemember: When in doubt, keep the file. Your campaign notes are irreplaceable.")

if __name__ == "__main__":
    main()