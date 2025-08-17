#!/usr/bin/env python3
"""
Cordelia Vault Content Validator
Validates vault content against Pydantic models for consistency and completeness.
"""

import os
import re
import json
import yaml
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Import our Pydantic models
import sys
sys.path.append('../data')
from models import (
    BaseVaultContent, Character, Location, Faction, Quest, Item, 
    Session, Campaign, ValidationReport, ContentValidationError,
    ContentStatus, WorldRealm, ContentType
)

@dataclass
class FileMetadata:
    """Extracted frontmatter from a vault file."""
    path: str
    title: Optional[str] = None
    created: Optional[str] = None
    updated: Optional[str] = None
    status: Optional[str] = None
    world: Optional[str] = None
    content_type: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class VaultContentValidator:
    """Validates vault content against Pydantic models."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.errors: List[ContentValidationError] = []
        self.warnings: List[ContentValidationError] = []
        
    def extract_frontmatter(self, file_path: Path) -> Optional[FileMetadata]:
        """Extract YAML frontmatter from a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for YAML frontmatter
            frontmatter_pattern = r'^---\n(.*?)\n---'
            match = re.search(frontmatter_pattern, content, re.DOTALL)
            
            if not match:
                return FileMetadata(path=str(file_path))
                
            yaml_content = match.group(1)
            metadata = yaml.safe_load(yaml_content)
            
            return FileMetadata(
                path=str(file_path),
                title=metadata.get('title'),
                created=metadata.get('created'),
                updated=metadata.get('updated'),
                status=metadata.get('status'),
                world=metadata.get('world'),
                content_type=metadata.get('type'),
                tags=metadata.get('tags', [])
            )
            
        except Exception as e:
            self.errors.append(ContentValidationError(
                file_path=str(file_path),
                error_type="frontmatter_parsing_error",
                error_message=f"Failed to parse frontmatter: {str(e)}",
                severity="moderate",
                suggested_fix="Check YAML syntax in frontmatter"
            ))
            return None
    
    def validate_base_content(self, metadata: FileMetadata) -> bool:
        """Validate against BaseVaultContent model."""
        try:
            # Attempt to create BaseVaultContent from metadata
            base_content = BaseVaultContent(
                title=metadata.title or Path(metadata.path).stem,
                content_type=ContentType(metadata.content_type) if metadata.content_type else ContentType.lore,
                status=ContentStatus(metadata.status) if metadata.status else ContentStatus.draft,
                world=WorldRealm(metadata.world) if metadata.world else WorldRealm.both,
                tags=metadata.tags or []
            )
            return True
            
        except ValueError as e:
            self.errors.append(ContentValidationError(
                file_path=metadata.path,
                error_type="model_validation_error",
                error_message=f"BaseVaultContent validation failed: {str(e)}",
                severity="high",
                suggested_fix="Check enum values and required fields"
            ))
            return False
            
    def validate_character_file(self, metadata: FileMetadata) -> bool:
        """Validate character files against Character model."""
        if not metadata.content_type or metadata.content_type.lower() != 'character':
            return True  # Not a character file
            
        try:
            # For now, just validate basic structure
            # In a full implementation, we'd parse the entire file content
            character = Character(
                title=metadata.title or "Unnamed Character",
                full_name=metadata.title or "Unnamed Character",
                world=WorldRealm(metadata.world) if metadata.world else WorldRealm.both,
                status=ContentStatus(metadata.status) if metadata.status else ContentStatus.draft,
                tags=metadata.tags or []
            )
            return True
            
        except ValueError as e:
            self.errors.append(ContentValidationError(
                file_path=metadata.path,
                error_type="character_validation_error", 
                error_message=f"Character validation failed: {str(e)}",
                severity="high",
                suggested_fix="Ensure character has required fields (full_name, etc.)"
            ))
            return False
            
    def validate_location_file(self, metadata: FileMetadata) -> bool:
        """Validate location files against Location model."""
        if not metadata.content_type or metadata.content_type.lower() != 'location':
            return True  # Not a location file
            
        try:
            location = Location(
                title=metadata.title or "Unnamed Location",
                world=WorldRealm(metadata.world) if metadata.world else WorldRealm.both,
                status=ContentStatus(metadata.status) if metadata.status else ContentStatus.draft,
                tags=metadata.tags or []
            )
            return True
            
        except ValueError as e:
            self.errors.append(ContentValidationError(
                file_path=metadata.path,
                error_type="location_validation_error",
                error_message=f"Location validation failed: {str(e)}",
                severity="high",
                suggested_fix="Check location-specific required fields"
            ))
            return False
            
    def check_naming_conventions(self, file_path: Path) -> None:
        """Check if file naming follows conventions."""
        filename = file_path.name
        
        # Check for problematic characters
        if re.search(r'[<>:"|?*]', filename):
            self.warnings.append(ContentValidationError(
                file_path=str(file_path),
                error_type="filename_convention_warning",
                error_message="Filename contains problematic characters",
                severity="low",
                suggested_fix="Use only alphanumeric characters, hyphens, and underscores"
            ))
            
        # Check for very long filenames
        if len(filename) > 100:
            self.warnings.append(ContentValidationError(
                file_path=str(file_path),
                error_type="filename_length_warning",
                error_message="Filename is very long (>100 characters)",
                severity="low",
                suggested_fix="Consider shortening the filename"
            ))
            
    def validate_file(self, file_path: Path) -> bool:
        """Validate a single file."""
        if not file_path.suffix == '.md':
            return True  # Skip non-markdown files
            
        self.check_naming_conventions(file_path)
        
        metadata = self.extract_frontmatter(file_path)
        if metadata is None:
            return False
            
        # Validate against base model
        valid_base = self.validate_base_content(metadata)
        
        # Validate against specific models based on content type
        valid_specific = True
        if metadata.content_type:
            if metadata.content_type.lower() == 'character':
                valid_specific = self.validate_character_file(metadata)
            elif metadata.content_type.lower() == 'location':
                valid_specific = self.validate_location_file(metadata)
                
        return valid_base and valid_specific
        
    def validate_vault(self) -> ValidationReport:
        """Validate the entire vault."""
        total_files = 0
        valid_files = 0
        
        # Find all markdown files
        for md_file in self.vault_path.rglob('*.md'):
            total_files += 1
            if self.validate_file(md_file):
                valid_files += 1
                
        # Create validation report
        report = ValidationReport(
            total_files_checked=total_files,
            valid_files=valid_files,
            errors=self.errors,
            warnings=self.warnings
        )
        
        return report
        
    def save_report(self, report: ValidationReport, output_path: str) -> None:
        """Save validation report to file."""
        output = {
            "validation_report": {
                "timestamp": report.timestamp.isoformat(),
                "total_files_checked": report.total_files_checked,
                "valid_files": report.valid_files,
                "success_rate": report.success_rate,
                "errors": [error.dict() for error in report.errors],
                "warnings": [warning.dict() for warning in report.warnings]
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
            
def main():
    """Main validation function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Cordelia vault content")
    parser.add_argument("vault_path", help="Path to vault directory")
    parser.add_argument("--output", "-o", help="Output path for validation report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    validator = VaultContentValidator(args.vault_path)
    report = validator.validate_vault()
    
    print(f"Validation Results:")
    print(f"Files checked: {report.total_files_checked}")
    print(f"Valid files: {report.valid_files}")
    print(f"Success rate: {report.success_rate:.1f}%")
    print(f"Errors: {len(report.errors)}")
    print(f"Warnings: {len(report.warnings)}")
    
    if args.verbose:
        for error in report.errors:
            print(f"ERROR: {error.file_path} - {error.error_message}")
        for warning in report.warnings:
            print(f"WARNING: {warning.file_path} - {warning.error_message}")
            
    if args.output:
        validator.save_report(report, args.output)
        print(f"Report saved to: {args.output}")
        
if __name__ == "__main__":
    main()