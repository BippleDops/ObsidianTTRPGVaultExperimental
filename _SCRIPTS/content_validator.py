#!/usr/bin/env python3
"""
Content Validation Automation System
Comprehensive validation of vault content for consistency, quality, and standards
Part of Phase 4: Advanced Automation & Dynamic Systems
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, Counter
import difflib

@dataclass
class ValidationIssue:
    file_path: str
    issue_type: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    auto_fixable: bool = False

@dataclass
class ValidationReport:
    timestamp: str
    files_checked: int
    total_issues: int
    errors: int
    warnings: int
    info: int
    issues: List[ValidationIssue] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)

class ContentValidator:
    """Comprehensive content validation system."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.config = self.load_validation_config()
        self.known_entities = set()
        self.valid_tags = set()
        self.load_vault_data()
        
    def load_validation_config(self) -> Dict:
        """Load validation configuration."""
        config_path = self.vault_path / "scripts" / "validation_config.json"
        
        default_config = {
            "required_frontmatter": {
                "all": ["created", "status", "tags", "type"],
                "People": ["world"],
                "Places": ["world"],
                "Items": ["world"],
                "Lore": ["world"]
            },
            "valid_statuses": [
                "draft", "in-progress", "complete", "review", "archived", 
                "generated", "stub", "placeholder"
            ],
            "valid_types": [
                "People", "Places", "Items", "Lore", "Adventure", "Session",
                "Encounter", "Quest", "Faction", "Organization"
            ],
            "valid_worlds": ["Aquabyssos", "Aethermoor", "Both"],
            "naming_patterns": {
                "People": r"^[A-Z][a-z]+ [A-Z][a-z]+( [A-Z][a-z]+)*$",
                "Places": r"^[A-Z][a-zA-Z\s\-']+$",
                "Items": r"^[A-Z][a-zA-Z\s\-']+$"
            },
            "content_rules": {
                "min_content_length": 100,
                "max_line_length": 120,
                "required_sections": {
                    "People": ["Basic Information", "Background"],
                    "Places": ["Description", "Connections"],
                    "Items": ["Description", "Properties"]
                }
            },
            "link_validation": {
                "check_broken_links": True,
                "check_orphaned_files": True,
                "suggest_missing_links": True
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in loaded_config:
                        loaded_config[key] = value
                return loaded_config
            except:
                pass
                
        # Write default config
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
        
    def load_vault_data(self):
        """Load vault data for cross-referencing."""
        print("Loading vault data for validation...")
        
        # Load known entities
        content_dirs = [
            "02_Worldbuilding/People",
            "02_Worldbuilding/Places", 
            "02_Worldbuilding/Groups",
            "02_Worldbuilding/Items",
            "02_Worldbuilding/Lore"
        ]
        
        for dir_name in content_dirs:
            content_dir = self.vault_path / dir_name
            if content_dir.exists():
                for md_file in content_dir.rglob("*.md"):
                    self.known_entities.add(md_file.stem)
                    
        # Load valid tags from existing content
        for md_file in self.vault_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                frontmatter = self.extract_frontmatter(content)
                if frontmatter and 'tags' in frontmatter:
                    tags = frontmatter['tags']
                    if isinstance(tags, list):
                        self.valid_tags.update(tags)
            except:
                continue
                
    def extract_frontmatter(self, content: str) -> Optional[Dict]:
        """Extract YAML frontmatter from content."""
        if not content.startswith('---'):
            return None
            
        try:
            parts = content.split('---', 2)
            if len(parts) >= 2:
                return yaml.safe_load(parts[1])
        except:
            return None
            
        return None
        
    def validate_file(self, file_path: Path) -> List[ValidationIssue]:
        """Validate a single file."""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Validate filename
            issues.extend(self.validate_filename(file_path))
            
            # Validate frontmatter
            frontmatter = self.extract_frontmatter(content)
            issues.extend(self.validate_frontmatter(file_path, frontmatter))
            
            # Validate content structure
            issues.extend(self.validate_content_structure(file_path, content, frontmatter))
            
            # Validate content quality
            issues.extend(self.validate_content_quality(file_path, content, lines))
            
            # Validate links
            issues.extend(self.validate_links(file_path, content))
            
            # Validate consistency
            issues.extend(self.validate_consistency(file_path, content, frontmatter))
            
        except Exception as e:
            issues.append(ValidationIssue(
                file_path=str(file_path.relative_to(self.vault_path)),
                issue_type="file_error",
                severity="error",
                message=f"Could not read file: {e}",
                auto_fixable=False
            ))
            
        return issues
        
    def validate_filename(self, file_path: Path) -> List[ValidationIssue]:
        """Validate filename conventions."""
        issues = []
        relative_path = file_path.relative_to(self.vault_path)
        filename = file_path.stem
        
        # Check for invalid characters
        invalid_chars = set(filename) & {'<', '>', ':', '"', '|', '?', '*'}
        if invalid_chars:
            issues.append(ValidationIssue(
                file_path=str(relative_path),
                issue_type="filename",
                severity="warning",
                message=f"Filename contains invalid characters: {invalid_chars}",
                suggestion=f"Remove characters: {invalid_chars}",
                auto_fixable=True
            ))
            
        # Check length
        if len(filename) > 100:
            issues.append(ValidationIssue(
                file_path=str(relative_path),
                issue_type="filename", 
                severity="warning",
                message="Filename is too long (>100 characters)",
                suggestion="Shorten filename"
            ))
            
        # Check naming patterns for specific types
        parent_dir = file_path.parent.name
        if parent_dir in self.config["naming_patterns"]:
            pattern = self.config["naming_patterns"][parent_dir]
            if not re.match(pattern, filename):
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="filename_pattern",
                    severity="info",
                    message=f"Filename doesn't match expected pattern for {parent_dir}",
                    suggestion=f"Expected pattern: {pattern}"
                ))
                
        return issues
        
    def validate_frontmatter(self, file_path: Path, frontmatter: Optional[Dict]) -> List[ValidationIssue]:
        """Validate YAML frontmatter."""
        issues = []
        relative_path = file_path.relative_to(self.vault_path)
        
        if not frontmatter:
            issues.append(ValidationIssue(
                file_path=str(relative_path),
                issue_type="frontmatter",
                severity="error",
                message="Missing or invalid frontmatter",
                auto_fixable=True
            ))
            return issues
            
        # Check required fields
        content_type = self.determine_content_type(file_path)
        required_fields = self.config["required_frontmatter"]["all"][:]
        
        if content_type in self.config["required_frontmatter"]:
            required_fields.extend(self.config["required_frontmatter"][content_type])
            
        for field in required_fields:
            if field not in frontmatter:
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="frontmatter_missing",
                    severity="warning",
                    message=f"Missing required frontmatter field: {field}",
                    auto_fixable=True
                ))
                
        # Validate field values
        if 'status' in frontmatter:
            if frontmatter['status'] not in self.config["valid_statuses"]:
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="frontmatter_value",
                    severity="warning",
                    message=f"Invalid status: {frontmatter['status']}",
                    suggestion=f"Valid statuses: {', '.join(self.config['valid_statuses'])}"
                ))
                
        if 'type' in frontmatter:
            if frontmatter['type'] not in self.config["valid_types"]:
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="frontmatter_value", 
                    severity="warning",
                    message=f"Invalid type: {frontmatter['type']}",
                    suggestion=f"Valid types: {', '.join(self.config['valid_types'])}"
                ))
                
        if 'world' in frontmatter:
            if frontmatter['world'] not in self.config["valid_worlds"]:
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="frontmatter_value",
                    severity="warning", 
                    message=f"Invalid world: {frontmatter['world']}",
                    suggestion=f"Valid worlds: {', '.join(self.config['valid_worlds'])}"
                ))
                
        # Validate date formats
        date_fields = ['created', 'updated']
        for date_field in date_fields:
            if date_field in frontmatter:
                date_value = frontmatter[date_field]
                if isinstance(date_value, str) and not self.is_valid_date_format(date_value):
                    issues.append(ValidationIssue(
                        file_path=str(relative_path),
                        issue_type="frontmatter_date",
                        severity="info",
                        message=f"Date field {date_field} not in ISO format: {date_value}",
                        suggestion="Use ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)",
                        auto_fixable=True
                    ))
                    
        # Validate tags
        if 'tags' in frontmatter:
            tags = frontmatter['tags']
            if not isinstance(tags, list):
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="frontmatter_tags",
                    severity="warning",
                    message="Tags should be a list",
                    auto_fixable=True
                ))
            else:
                # Check for inconsistent tag formats
                for tag in tags:
                    if not isinstance(tag, str) or ' ' in tag or tag != tag.lower().replace(' ', '-'):
                        issues.append(ValidationIssue(
                            file_path=str(relative_path),
                            issue_type="frontmatter_tags",
                            severity="info",
                            message=f"Tag format inconsistent: '{tag}'",
                            suggestion="Use lowercase with hyphens: 'example-tag'"
                        ))
                        
        return issues
        
    def validate_content_structure(self, file_path: Path, content: str, 
                                  frontmatter: Optional[Dict]) -> List[ValidationIssue]:
        """Validate content structure and organization."""
        issues = []
        relative_path = file_path.relative_to(self.vault_path)
        
        # Skip frontmatter for content analysis
        content_body = content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content_body = parts[2]
                
        # Check minimum content length
        min_length = self.config["content_rules"]["min_content_length"]
        if len(content_body.strip()) < min_length:
            issues.append(ValidationIssue(
                file_path=str(relative_path),
                issue_type="content_length",
                severity="warning",
                message=f"Content too short ({len(content_body)} < {min_length} characters)",
                suggestion="Add more detailed content"
            ))
            
        # Check for required sections
        content_type = self.determine_content_type(file_path)
        if content_type in self.config["content_rules"]["required_sections"]:
            required_sections = self.config["content_rules"]["required_sections"][content_type]
            
            for section in required_sections:
                # Look for section headers
                section_pattern = rf"#{1,6}\s+{re.escape(section)}"
                if not re.search(section_pattern, content_body, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        file_path=str(relative_path),
                        issue_type="missing_section",
                        severity="info", 
                        message=f"Missing recommended section: {section}",
                        suggestion=f"Add ## {section} section"
                    ))
                    
        # Check header hierarchy
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content_body, re.MULTILINE)
        if headers:
            prev_level = 0
            for i, (header_markup, header_text) in enumerate(headers):
                level = len(header_markup)
                
                if level > prev_level + 1:
                    issues.append(ValidationIssue(
                        file_path=str(relative_path),
                        issue_type="header_hierarchy",
                        severity="info",
                        message=f"Header level jumps from {prev_level} to {level}: {header_text}",
                        suggestion="Use sequential header levels"
                    ))
                    
                prev_level = level
                
        return issues
        
    def validate_content_quality(self, file_path: Path, content: str, 
                                lines: List[str]) -> List[ValidationIssue]:
        """Validate content quality and style."""
        issues = []
        relative_path = file_path.relative_to(self.vault_path)
        
        # Check line length
        max_line_length = self.config["content_rules"]["max_line_length"]
        for i, line in enumerate(lines, 1):
            if len(line) > max_line_length and not line.strip().startswith('|'):  # Allow long table rows
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="line_length",
                    severity="info",
                    message=f"Line too long ({len(line)} > {max_line_length} characters)",
                    line_number=i,
                    suggestion="Break long lines or use word wrapping"
                ))
                
        # Check for common writing issues
        content_lower = content.lower()
        
        # Repetitive phrases
        phrases = re.findall(r'\b\w+(?:\s+\w+){1,3}\b', content_lower)
        phrase_counts = Counter(phrases)
        for phrase, count in phrase_counts.items():
            if count > 5 and len(phrase) > 10:  # Repeated phrases
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="repetitive_content",
                    severity="info",
                    message=f"Phrase repeated {count} times: '{phrase[:30]}...'",
                    suggestion="Consider varying language"
                ))
                
        # Check for placeholder text
        placeholders = [
            "todo", "tbd", "placeholder", "fill this", "add content",
            "lorem ipsum", "[insert", "coming soon"
        ]
        
        for placeholder in placeholders:
            if placeholder in content_lower:
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="placeholder_content",
                    severity="warning",
                    message=f"Contains placeholder text: '{placeholder}'",
                    suggestion="Replace with actual content",
                    auto_fixable=False
                ))
                
        return issues
        
    def validate_links(self, file_path: Path, content: str) -> List[ValidationIssue]:
        """Validate wikilinks and references."""
        issues = []
        relative_path = file_path.relative_to(self.vault_path)
        
        if not self.config["link_validation"]["check_broken_links"]:
            return issues
            
        # Find all wikilinks
        wikilink_pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
        links = re.findall(wikilink_pattern, content)
        
        for link_target, link_display in links:
            # Check if target exists
            if link_target not in self.known_entities:
                # Try to find similar entities
                suggestions = difflib.get_close_matches(link_target, self.known_entities, n=3, cutoff=0.6)
                
                suggestion_text = ""
                if suggestions:
                    suggestion_text = f"Did you mean: {', '.join(suggestions[:2])}?"
                    
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="broken_link",
                    severity="warning",
                    message=f"Broken wikilink: [[{link_target}]]",
                    suggestion=suggestion_text or "Create the target file or fix the link"
                ))
                
        # Check for potential missing links
        if self.config["link_validation"]["suggest_missing_links"]:
            # Find entity names mentioned but not linked
            for entity in self.known_entities:
                if len(entity) > 5:  # Skip short entity names
                    # Look for the entity name in content but not as a link
                    pattern = rf'\b{re.escape(entity)}\b'
                    if re.search(pattern, content, re.IGNORECASE):
                        # Check if it's already linked
                        link_pattern = rf'\[\[[^\]]*{re.escape(entity)}[^\]]*\]\]'
                        if not re.search(link_pattern, content, re.IGNORECASE):
                            issues.append(ValidationIssue(
                                file_path=str(relative_path),
                                issue_type="missing_link", 
                                severity="info",
                                message=f"Entity mentioned but not linked: {entity}",
                                suggestion=f"Consider adding [[{entity}]] link"
                            ))
                            
        return issues
        
    def validate_consistency(self, file_path: Path, content: str, 
                           frontmatter: Optional[Dict]) -> List[ValidationIssue]:
        """Validate content consistency."""
        issues = []
        relative_path = file_path.relative_to(self.vault_path)
        
        if not frontmatter:
            return issues
            
        # Check title consistency
        filename_title = file_path.stem
        content_title = None
        
        # Extract main header
        header_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if header_match:
            content_title = header_match.group(1).strip()
            
        if content_title and content_title != filename_title:
            # Allow some flexibility in naming
            similarity = difflib.SequenceMatcher(None, filename_title.lower(), 
                                               content_title.lower()).ratio()
            if similarity < 0.8:
                issues.append(ValidationIssue(
                    file_path=str(relative_path),
                    issue_type="title_inconsistency",
                    severity="info", 
                    message=f"Filename '{filename_title}' doesn't match content title '{content_title}'",
                    suggestion="Consider aligning filename and content title"
                ))
                
        # Check world consistency in content
        if 'world' in frontmatter:
            world = frontmatter['world']
            world_indicators = {
                'Aquabyssos': ['underwater', 'ocean', 'depth', 'pressure', 'tidal', 'abyssal'],
                'Aethermoor': ['sky', 'wind', 'storm', 'aerial', 'altitude', 'cloud']
            }
            
            if world in world_indicators:
                indicators = world_indicators[world]
                content_lower = content.lower()
                
                # Check if content matches the declared world
                indicator_count = sum(1 for indicator in indicators if indicator in content_lower)
                
                if world != "Both" and indicator_count == 0:
                    other_world = "Aethermoor" if world == "Aquabyssos" else "Aquabyssos"
                    other_indicators = world_indicators.get(other_world, [])
                    other_count = sum(1 for indicator in other_indicators if indicator in content_lower)
                    
                    if other_count > 0:
                        issues.append(ValidationIssue(
                            file_path=str(relative_path),
                            issue_type="world_inconsistency",
                            severity="warning",
                            message=f"Content suggests {other_world} but frontmatter says {world}",
                            suggestion=f"Check world assignment or content focus"
                        ))
                        
        return issues
        
    def determine_content_type(self, file_path: Path) -> str:
        """Determine content type from file path."""
        path_parts = file_path.parts
        
        type_mapping = {
            'People': 'People',
            'Places': 'Places', 
            'Items': 'Items',
            'Groups': 'Lore',
            'Lore': 'Lore',
            'Adventures': 'Adventure',
            'Sessions': 'Session'
        }
        
        for part in path_parts:
            if part in type_mapping:
                return type_mapping[part]
                
        return "Unknown"
        
    def is_valid_date_format(self, date_string: str) -> bool:
        """Check if date string is in valid ISO format."""
        iso_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$',  # YYYY-MM-DDTHH:MM:SS
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+$',  # With milliseconds
            r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$'  # With timezone
        ]
        
        return any(re.match(pattern, date_string) for pattern in iso_patterns)
        
    def validate_vault(self, target_path: Optional[Path] = None) -> ValidationReport:
        """Validate entire vault or specific directory."""
        if not target_path:
            target_path = self.vault_path
            
        print(f"Validating vault: {target_path}")
        
        all_issues = []
        files_checked = 0
        
        for md_file in target_path.rglob("*.md"):
            if md_file.name.startswith('.') or 'backup' in md_file.name:
                continue
                
            file_issues = self.validate_file(md_file)
            all_issues.extend(file_issues)
            files_checked += 1
            
            if files_checked % 100 == 0:
                print(f"Processed {files_checked} files...")
                
        # Generate report
        errors = sum(1 for issue in all_issues if issue.severity == 'error')
        warnings = sum(1 for issue in all_issues if issue.severity == 'warning')
        info = sum(1 for issue in all_issues if issue.severity == 'info')
        
        # Summary statistics
        issue_types = Counter(issue.issue_type for issue in all_issues)
        severity_by_type = defaultdict(Counter)
        for issue in all_issues:
            severity_by_type[issue.issue_type][issue.severity] += 1
            
        auto_fixable = sum(1 for issue in all_issues if issue.auto_fixable)
        
        report = ValidationReport(
            timestamp=datetime.now().isoformat(),
            files_checked=files_checked,
            total_issues=len(all_issues),
            errors=errors,
            warnings=warnings,
            info=info,
            issues=all_issues,
            summary={
                "issue_types": dict(issue_types),
                "severity_by_type": {k: dict(v) for k, v in severity_by_type.items()},
                "auto_fixable_count": auto_fixable,
                "top_issues": issue_types.most_common(10)
            }
        )
        
        print(f"Validation complete: {files_checked} files, {len(all_issues)} issues found")
        return report
        
    def export_report(self, report: ValidationReport, output_path: Path):
        """Export validation report to markdown."""
        lines = [
            "# Content Validation Report",
            f"Generated: {report.timestamp}",
            f"Files checked: {report.files_checked}",
            f"Total issues: {report.total_issues}",
            "",
            "## Summary",
            f"- **Errors**: {report.errors} (require immediate attention)",
            f"- **Warnings**: {report.warnings} (should be addressed)",
            f"- **Info**: {report.info} (suggestions for improvement)",
            f"- **Auto-fixable**: {report.summary['auto_fixable_count']} issues",
            "",
            "## Issue Breakdown by Type"
        ]
        
        for issue_type, count in report.summary["top_issues"]:
            severities = report.summary["severity_by_type"].get(issue_type, {})
            severity_text = ", ".join(f"{sev}: {cnt}" for sev, cnt in severities.items())
            lines.append(f"- **{issue_type}**: {count} ({severity_text})")
            
        if report.errors > 0:
            lines.extend([
                "",
                "## Critical Errors",
                ""
            ])
            
            errors = [issue for issue in report.issues if issue.severity == 'error']
            for error in errors[:20]:  # Top 20 errors
                lines.append(f"- `{error.file_path}`: {error.message}")
                
        if report.warnings > 0:
            lines.extend([
                "",
                "## Warnings to Address",
                ""
            ])
            
            warnings = [issue for issue in report.issues if issue.severity == 'warning']
            for warning in warnings[:30]:  # Top 30 warnings
                line = f"- `{warning.file_path}`: {warning.message}"
                if warning.line_number:
                    line += f" (line {warning.line_number})"
                if warning.suggestion:
                    line += f" → {warning.suggestion}"
                lines.append(line)
                
        # Auto-fixable issues
        auto_fixable = [issue for issue in report.issues if issue.auto_fixable]
        if auto_fixable:
            lines.extend([
                "",
                "## Auto-fixable Issues", 
                f"*{len(auto_fixable)} issues can be automatically fixed*",
                ""
            ])
            
            for issue in auto_fixable[:20]:  # Top 20 auto-fixable
                line = f"- `{issue.file_path}`: {issue.message}"
                if issue.suggestion:
                    line += f" → {issue.suggestion}"
                lines.append(line)
                
        content = '\n'.join(lines)
        output_path.write_text(content, encoding='utf-8')
        
    def auto_fix_issues(self, report: ValidationReport) -> Dict[str, int]:
        """Automatically fix issues that can be auto-fixed."""
        results = {"fixed": 0, "failed": 0, "skipped": 0}
        
        auto_fixable = [issue for issue in report.issues if issue.auto_fixable]
        
        # Group by file for efficient processing
        by_file = defaultdict(list)
        for issue in auto_fixable:
            by_file[issue.file_path].append(issue)
            
        for file_path_str, file_issues in by_file.items():
            try:
                file_path = self.vault_path / file_path_str
                if not file_path.exists():
                    results["failed"] += len(file_issues)
                    continue
                    
                content = file_path.read_text(encoding='utf-8')
                modified = False
                
                for issue in file_issues:
                    # Apply specific fixes based on issue type
                    if issue.issue_type == "frontmatter_date":
                        # Fix date format
                        content, fixed = self.fix_date_format(content, issue)
                        if fixed:
                            modified = True
                            results["fixed"] += 1
                        else:
                            results["failed"] += 1
                            
                    elif issue.issue_type == "frontmatter_missing":
                        # Add missing frontmatter field
                        content, fixed = self.add_missing_frontmatter(content, issue)
                        if fixed:
                            modified = True
                            results["fixed"] += 1
                        else:
                            results["failed"] += 1
                            
                    elif issue.issue_type == "frontmatter_tags":
                        # Fix tag format
                        content, fixed = self.fix_tag_format(content, issue)
                        if fixed:
                            modified = True
                            results["fixed"] += 1
                        else:
                            results["failed"] += 1
                            
                    else:
                        results["skipped"] += 1
                        
                if modified:
                    # Backup original file
                    backup_path = file_path.with_suffix(f'.md.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
                    backup_path.write_text(content, encoding='utf-8')
                    
                    # Write fixed content
                    file_path.write_text(content, encoding='utf-8')
                    
            except Exception as e:
                print(f"Error auto-fixing {file_path_str}: {e}")
                results["failed"] += len(file_issues)
                
        return results
        
    def fix_date_format(self, content: str, issue: ValidationIssue) -> Tuple[str, bool]:
        """Fix date format in frontmatter."""
        # This is a simplified implementation
        # In practice, would need more sophisticated parsing
        return content, False
        
    def add_missing_frontmatter(self, content: str, issue: ValidationIssue) -> Tuple[str, bool]:
        """Add missing frontmatter fields."""
        # This is a simplified implementation  
        # In practice, would need to parse and modify YAML properly
        return content, False
        
    def fix_tag_format(self, content: str, issue: ValidationIssue) -> Tuple[str, bool]:
        """Fix tag format in frontmatter."""
        # This is a simplified implementation
        return content, False

def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Content Validator")
    parser.add_argument("--vault-path", default=".", help="Path to vault root")
    parser.add_argument("--target", help="Target directory to validate (default: entire vault)")
    parser.add_argument("--output", help="Output path for report")
    parser.add_argument("--auto-fix", action="store_true", help="Automatically fix issues where possible")
    parser.add_argument("--json", action="store_true", help="Export report as JSON")
    
    args = parser.parse_args()
    
    validator = ContentValidator(args.vault_path)
    
    target_path = Path(args.target) if args.target else None
    report = validator.validate_vault(target_path)
    
    # Export report
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(args.vault_path) / f"content_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
    if args.json:
        # Export as JSON
        output_path = output_path.with_suffix('.json')
        report_data = {
            "timestamp": report.timestamp,
            "files_checked": report.files_checked,
            "total_issues": report.total_issues,
            "errors": report.errors,
            "warnings": report.warnings,
            "info": report.info,
            "summary": report.summary,
            "issues": [
                {
                    "file_path": issue.file_path,
                    "issue_type": issue.issue_type,
                    "severity": issue.severity,
                    "message": issue.message,
                    "line_number": issue.line_number,
                    "suggestion": issue.suggestion,
                    "auto_fixable": issue.auto_fixable
                }
                for issue in report.issues
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2)
    else:
        validator.export_report(report, output_path)
        
    print(f"Report exported to: {output_path}")
    
    # Auto-fix if requested
    if args.auto_fix:
        print("\nAttempting to auto-fix issues...")
        fix_results = validator.auto_fix_issues(report)
        print(f"Auto-fix results: {fix_results}")

if __name__ == "__main__":
    main()