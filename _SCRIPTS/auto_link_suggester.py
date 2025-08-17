#!/usr/bin/env python3
"""
Automatic Link Suggestion System
Intelligently suggests wikilinks for content based on vault analysis
Part of Phase 4: Advanced Automation & Dynamic Systems
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
import difflib
from dataclasses import dataclass
import yaml
from datetime import datetime

@dataclass
class LinkSuggestion:
    text: str
    target_file: str
    confidence: float
    context: str
    reason: str
    line_number: int

@dataclass 
class LinkableEntity:
    name: str
    file_path: str
    aliases: List[str]
    entity_type: str  # 'person', 'place', 'faction', 'item', etc.
    importance: int   # 1-10 scale

class AutoLinkSuggester:
    """Automatically suggests wikilinks for content."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.entities_db = {}
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'it', 'its', 'he', 'she', 'his', 'her', 'they', 'them',
            'their', 'i', 'me', 'my', 'we', 'us', 'our', 'you', 'your'
        }
        
        self.build_entities_database()
        
    def build_entities_database(self):
        """Build database of linkable entities from vault content."""
        print("Building entities database...")
        
        # Key directories to scan
        content_dirs = [
            self.vault_path / "02_Worldbuilding" / "People",
            self.vault_path / "02_Worldbuilding" / "Places", 
            self.vault_path / "02_Worldbuilding" / "Groups",
            self.vault_path / "02_Worldbuilding" / "Items",
            self.vault_path / "02_Worldbuilding" / "Lore"
        ]
        
        for content_dir in content_dirs:
            if not content_dir.exists():
                continue
                
            entity_type = content_dir.name.lower()[:-1] if content_dir.name.endswith('s') else content_dir.name.lower()
            
            for md_file in content_dir.rglob("*.md"):
                try:
                    self.process_entity_file(md_file, entity_type)
                except Exception as e:
                    print(f"Error processing {md_file}: {e}")
                    
        print(f"Built database with {len(self.entities_db)} entities")
        
    def process_entity_file(self, file_path: Path, entity_type: str):
        """Process a single entity file."""
        content = file_path.read_text(encoding='utf-8')
        
        # Extract title from filename or content
        title = file_path.stem
        
        # Parse frontmatter if it exists
        aliases = []
        importance = 5  # default
        
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    frontmatter = yaml.safe_load(parts[1])
                    if frontmatter:
                        aliases = frontmatter.get('aliases', [])
                        # Estimate importance based on tags and type
                        tags = frontmatter.get('tags', [])
                        if 'major' in tags or 'important' in tags:
                            importance = 8
                        elif 'minor' in tags:
                            importance = 3
                        elif entity_type in ['person', 'place']:
                            importance = 6
                        
                        # Override title if specified
                        if 'title' in frontmatter:
                            title = frontmatter['title']
            except:
                pass
        
        # Add variations of the name
        name_variations = [title]
        name_variations.extend(aliases)
        
        # Add common variations
        if ' ' in title:
            # Add each word as potential match
            words = title.split()
            if len(words) == 2:
                name_variations.append(words[-1])  # Last name
        
        # Remove duplicates and filter
        name_variations = [v for v in set(name_variations) if v and len(v) > 2]
        
        # Store entity
        relative_path = str(file_path.relative_to(self.vault_path))
        self.entities_db[title] = LinkableEntity(
            name=title,
            file_path=relative_path,
            aliases=name_variations,
            entity_type=entity_type,
            importance=importance
        )
        
    def suggest_links_for_file(self, file_path: Path) -> List[LinkSuggestion]:
        """Suggest links for a specific file."""
        if not file_path.exists():
            return []
            
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        suggestions = []
        
        # Skip frontmatter
        start_line = 0
        if content.startswith('---'):
            for i, line in enumerate(lines):
                if i > 0 and line.strip() == '---':
                    start_line = i + 1
                    break
        
        # Find existing links to avoid duplicates
        existing_links = set()
        link_pattern = r'\[\[([^\]]+)\]\]'
        for match in re.finditer(link_pattern, content):
            existing_links.add(match.group(1).lower())
            
        # Process each line
        for line_num, line in enumerate(lines[start_line:], start_line + 1):
            line_suggestions = self.suggest_links_for_line(
                line, line_num, existing_links, file_path
            )
            suggestions.extend(line_suggestions)
            
        # Remove duplicate suggestions and sort by confidence
        suggestions = self.deduplicate_suggestions(suggestions)
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        
        return suggestions[:20]  # Return top 20 suggestions
        
    def suggest_links_for_line(self, line: str, line_num: int, 
                              existing_links: Set[str], file_path: Path) -> List[LinkSuggestion]:
        """Suggest links for a single line."""
        suggestions = []
        
        # Skip certain line types
        if (line.strip().startswith('#') or 
            line.strip().startswith('- ') or
            line.strip().startswith('*') or
            '[[' in line):  # Already has links
            return suggestions
            
        # Look for entity matches
        for entity_name, entity in self.entities_db.items():
            if entity.file_path == str(file_path.relative_to(self.vault_path)):
                continue  # Don't link to self
                
            for alias in entity.aliases:
                if len(alias) < 3:  # Skip very short aliases
                    continue
                    
                if alias.lower() in existing_links:
                    continue  # Already linked
                    
                # Find matches in the line
                matches = self.find_phrase_matches(line, alias)
                for match_start, match_end, matched_text in matches:
                    confidence = self.calculate_confidence(
                        line, matched_text, alias, entity, match_start, match_end
                    )
                    
                    if confidence > 0.6:  # Only suggest high-confidence matches
                        suggestions.append(LinkSuggestion(
                            text=matched_text,
                            target_file=entity.name,
                            confidence=confidence,
                            context=line.strip(),
                            reason=self.get_suggestion_reason(entity, confidence),
                            line_number=line_num
                        ))
                        
        return suggestions
        
    def find_phrase_matches(self, text: str, phrase: str) -> List[Tuple[int, int, str]]:
        """Find all matches of a phrase in text, handling word boundaries."""
        matches = []
        text_lower = text.lower()
        phrase_lower = phrase.lower()
        
        # Exact match
        start = 0
        while True:
            pos = text_lower.find(phrase_lower, start)
            if pos == -1:
                break
                
            end_pos = pos + len(phrase)
            
            # Check word boundaries
            if self.is_word_boundary(text, pos, end_pos):
                matched_text = text[pos:end_pos]
                matches.append((pos, end_pos, matched_text))
                
            start = pos + 1
            
        return matches
        
    def is_word_boundary(self, text: str, start: int, end: int) -> bool:
        """Check if the match is at word boundaries."""
        # Check character before
        if start > 0 and text[start - 1].isalnum():
            return False
            
        # Check character after
        if end < len(text) and text[end].isalnum():
            return False
            
        return True
        
    def calculate_confidence(self, line: str, matched_text: str, alias: str, 
                           entity: LinkableEntity, start: int, end: int) -> float:
        """Calculate confidence score for a link suggestion."""
        confidence = 0.0
        
        # Base confidence from entity importance
        confidence += entity.importance / 10.0 * 0.3
        
        # Exact match bonus
        if matched_text.lower() == alias.lower():
            confidence += 0.4
        else:
            # Partial match penalty
            similarity = difflib.SequenceMatcher(None, matched_text.lower(), alias.lower()).ratio()
            confidence += similarity * 0.2
            
        # Context analysis
        context_words = line.lower().split()
        
        # Proper noun capitalization bonus
        if matched_text[0].isupper():
            confidence += 0.2
            
        # Entity type context bonus
        if entity.entity_type == 'person':
            person_indicators = ['said', 'told', 'spoke', 'replied', 'asked', 'declared']
            if any(indicator in context_words for indicator in person_indicators):
                confidence += 0.2
                
        elif entity.entity_type == 'place':
            place_indicators = ['in', 'at', 'to', 'from', 'near', 'inside', 'outside']
            if any(indicator in context_words for indicator in place_indicators):
                confidence += 0.2
                
        elif entity.entity_type == 'group':
            group_indicators = ['member', 'faction', 'guild', 'order', 'organization']
            if any(indicator in context_words for indicator in group_indicators):
                confidence += 0.2
        
        # Position context
        position = start / len(line) if line else 0.5
        if 0.2 < position < 0.8:  # Middle of line is more likely to be content
            confidence += 0.1
            
        # Avoid common false positives
        common_words = ['crystal', 'shadow', 'deep', 'wind', 'storm', 'tide']
        if matched_text.lower() in common_words and entity.importance < 7:
            confidence -= 0.3
            
        return max(0.0, min(1.0, confidence))
        
    def get_suggestion_reason(self, entity: LinkableEntity, confidence: float) -> str:
        """Generate human-readable reason for the suggestion."""
        reasons = []
        
        if confidence > 0.9:
            reasons.append("High confidence match")
        elif confidence > 0.7:
            reasons.append("Good match")
        else:
            reasons.append("Possible match")
            
        reasons.append(f"{entity.entity_type.title()} entity")
        
        if entity.importance >= 8:
            reasons.append("Important entity")
        elif entity.importance <= 3:
            reasons.append("Minor entity")
            
        return ", ".join(reasons)
        
    def deduplicate_suggestions(self, suggestions: List[LinkSuggestion]) -> List[LinkSuggestion]:
        """Remove duplicate suggestions, keeping the highest confidence."""
        seen = {}
        deduplicated = []
        
        for suggestion in suggestions:
            key = (suggestion.line_number, suggestion.text.lower())
            
            if key not in seen or suggestion.confidence > seen[key].confidence:
                seen[key] = suggestion
                
        return list(seen.values())
        
    def apply_suggestions(self, file_path: Path, suggestions: List[LinkSuggestion], 
                         auto_apply_threshold: float = 0.9) -> Dict[str, any]:
        """Apply link suggestions to a file."""
        if not suggestions:
            return {"applied": 0, "skipped": 0, "errors": 0}
            
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        applied = 0
        skipped = 0
        errors = 0
        
        # Sort suggestions by line number (descending) to avoid position shifts
        suggestions.sort(key=lambda x: x.line_number, reverse=True)
        
        for suggestion in suggestions:
            try:
                line_idx = suggestion.line_number - 1
                if line_idx >= len(lines):
                    errors += 1
                    continue
                    
                line = lines[line_idx]
                
                # Apply high-confidence suggestions automatically
                if suggestion.confidence >= auto_apply_threshold:
                    # Replace the text with a wikilink
                    old_text = suggestion.text
                    new_text = f"[[{suggestion.target_file}|{old_text}]]"
                    
                    # Only replace if not already a link
                    if f"[[{suggestion.target_file}" not in line:
                        lines[line_idx] = line.replace(old_text, new_text, 1)
                        applied += 1
                    else:
                        skipped += 1
                else:
                    skipped += 1
                    
            except Exception as e:
                print(f"Error applying suggestion: {e}")
                errors += 1
                
        # Write back to file if changes were made
        if applied > 0:
            new_content = '\n'.join(lines)
            
            # Backup original file
            backup_path = file_path.with_suffix(f'.md.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            file_path.write_text(new_content, encoding='utf-8')
            
        return {
            "applied": applied,
            "skipped": skipped,
            "errors": errors
        }
        
    def generate_suggestions_report(self, target_dir: Path = None) -> str:
        """Generate a comprehensive suggestions report."""
        if not target_dir:
            target_dir = self.vault_path / "02_Worldbuilding"
            
        all_suggestions = []
        processed_files = 0
        
        for md_file in target_dir.rglob("*.md"):
            if md_file.name.startswith('.'):
                continue
                
            suggestions = self.suggest_links_for_file(md_file)
            if suggestions:
                all_suggestions.extend([(md_file, s) for s in suggestions])
                processed_files += 1
                
        # Generate report
        report_lines = [
            "# Auto-Link Suggestions Report",
            f"Generated: {datetime.now().isoformat()}",
            f"Files processed: {processed_files}",
            f"Total suggestions: {len(all_suggestions)}",
            "",
        ]
        
        if all_suggestions:
            # Sort by confidence
            all_suggestions.sort(key=lambda x: x[1].confidence, reverse=True)
            
            # Group by target file
            by_target = defaultdict(list)
            for file_path, suggestion in all_suggestions:
                by_target[suggestion.target_file].append((file_path, suggestion))
                
            report_lines.extend([
                "## Top Suggestions by Target",
                ""
            ])
            
            for target, file_suggestions in sorted(by_target.items(), 
                                                 key=lambda x: len(x[1]), reverse=True)[:10]:
                report_lines.extend([
                    f"### {target} ({len(file_suggestions)} suggestions)",
                    ""
                ])
                
                for file_path, suggestion in file_suggestions[:5]:  # Top 5 per target
                    rel_path = file_path.relative_to(self.vault_path)
                    report_lines.extend([
                        f"- **{suggestion.text}** in `{rel_path}`",
                        f"  - Confidence: {suggestion.confidence:.2f}",
                        f"  - Context: {suggestion.context[:80]}{'...' if len(suggestion.context) > 80 else ''}",
                        f"  - Reason: {suggestion.reason}",
                        ""
                    ])
                    
            # High-confidence suggestions ready for auto-apply
            high_confidence = [(f, s) for f, s in all_suggestions if s.confidence >= 0.9]
            if high_confidence:
                report_lines.extend([
                    f"## High-Confidence Suggestions ({len(high_confidence)})",
                    "*These can be automatically applied*",
                    ""
                ])
                
                for file_path, suggestion in high_confidence[:20]:  # Top 20
                    rel_path = file_path.relative_to(self.vault_path)
                    report_lines.append(f"- `{rel_path}` line {suggestion.line_number}: **{suggestion.text}** → [[{suggestion.target_file}]]")
                    
        else:
            report_lines.append("No suggestions found.")
            
        return '\n'.join(report_lines)
        
    def export_suggestions_json(self, output_path: Path) -> Dict:
        """Export suggestions as JSON for external processing."""
        all_suggestions = []
        
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.name.startswith('.'):
                continue
                
            suggestions = self.suggest_links_for_file(md_file)
            
            for suggestion in suggestions:
                all_suggestions.append({
                    "file": str(md_file.relative_to(self.vault_path)),
                    "text": suggestion.text,
                    "target": suggestion.target_file,
                    "confidence": suggestion.confidence,
                    "context": suggestion.context,
                    "reason": suggestion.reason,
                    "line_number": suggestion.line_number
                })
                
        output_data = {
            "generated": datetime.now().isoformat(),
            "total_suggestions": len(all_suggestions),
            "entities_count": len(self.entities_db),
            "suggestions": all_suggestions
        }
        
        output_path.write_text(json.dumps(output_data, indent=2), encoding='utf-8')
        return output_data

def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto Link Suggester")
    parser.add_argument("--vault-path", default=".", help="Path to vault root")
    parser.add_argument("--file", help="Suggest links for specific file")
    parser.add_argument("--report", action="store_true", help="Generate suggestions report")
    parser.add_argument("--export-json", help="Export suggestions as JSON")
    parser.add_argument("--auto-apply", action="store_true", help="Auto-apply high-confidence suggestions")
    parser.add_argument("--threshold", type=float, default=0.9, help="Auto-apply confidence threshold")
    
    args = parser.parse_args()
    
    suggester = AutoLinkSuggester(args.vault_path)
    
    if args.file:
        file_path = Path(args.file)
        suggestions = suggester.suggest_links_for_file(file_path)
        
        print(f"Link suggestions for {file_path}:")
        print("=" * 50)
        
        for suggestion in suggestions:
            print(f"Line {suggestion.line_number}: {suggestion.text}")
            print(f"  → [[{suggestion.target_file}]]")
            print(f"  Confidence: {suggestion.confidence:.2f}")
            print(f"  Context: {suggestion.context}")
            print(f"  Reason: {suggestion.reason}")
            print()
            
        if args.auto_apply and suggestions:
            result = suggester.apply_suggestions(file_path, suggestions, args.threshold)
            print(f"Applied: {result['applied']}, Skipped: {result['skipped']}, Errors: {result['errors']}")
            
    elif args.report:
        report = suggester.generate_suggestions_report()
        
        report_path = Path(args.vault_path) / "auto_link_suggestions_report.md"
        report_path.write_text(report, encoding='utf-8')
        
        print(f"Report generated: {report_path}")
        print()
        print(report[:1000] + "..." if len(report) > 1000 else report)
        
    elif args.export_json:
        output_path = Path(args.export_json)
        data = suggester.export_suggestions_json(output_path)
        
        print(f"Exported {data['total_suggestions']} suggestions to {output_path}")
        
    else:
        print("Please specify --file, --report, or --export-json")

if __name__ == "__main__":
    main()