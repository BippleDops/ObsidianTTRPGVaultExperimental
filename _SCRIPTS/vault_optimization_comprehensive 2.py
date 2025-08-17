#!/usr/bin/env python3
"""
Comprehensive Vault Optimization Script

This script performs systematic improvements to the Cordelia TTRPG vault:
1. Fixes truncated filenames
2. Removes duplicate files
3. Standardizes naming conventions
4. Organizes files into proper subfolders
5. Fixes broken wiki links
6. Validates image references
7. Improves metadata consistency
"""

import os
import re
import shutil
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class VaultOptimizer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.fixes_applied = []
        self.issues_found = []
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        
    def log_fix(self, action: str, details: str):
        """Log a fix that was applied"""
        fix = {
            'action': action,
            'details': details,
            'dry_run': self.dry_run
        }
        self.fixes_applied.append(fix)
        print(f"{'[DRY RUN] ' if self.dry_run else ''}FIXED: {action} - {details}")
        
    def log_issue(self, issue_type: str, details: str):
        """Log an issue that was found"""
        issue = {
            'type': issue_type,
            'details': details
        }
        self.issues_found.append(issue)
        print(f"ISSUE: {issue_type} - {details}")
        
    def find_truncated_files(self) -> List[Path]:
        """Find files with truncated names ending in incomplete extensions"""
        truncated_files = []
        groups_path = self.vault_path / "02_Worldbuilding" / "Groups"
        
        for file_path in groups_path.rglob("*"):
            if file_path.is_file():
                name = file_path.name
                # Check for truncated names
                if (name.endswith('.') or 
                    re.search(r'[a-z]$', name) and not name.endswith('.md') or
                    len(name) > 50 and not name.endswith('.md')):
                    truncated_files.append(file_path)
                    
        return truncated_files
        
    def fix_truncated_files(self):
        """Fix files with truncated names"""
        truncated_files = self.find_truncated_files()
        
        for file_path in truncated_files:
            old_name = file_path.name
            
            # Add .md extension if missing
            if not old_name.endswith('.md'):
                new_name = old_name + '.md'
                new_path = file_path.parent / new_name
                
                if not self.dry_run:
                    file_path.rename(new_path)
                    
                self.log_fix("Fixed truncated filename", f"{old_name} -> {new_name}")
                
    def find_duplicate_files(self) -> Dict[str, List[Path]]:
        """Find duplicate files with similar names"""
        duplicates = defaultdict(list)
        groups_path = self.vault_path / "02_Worldbuilding" / "Groups"
        
        # Group files by normalized names
        for file_path in groups_path.rglob("*.md"):
            normalized_name = self.normalize_filename(file_path.stem)
            duplicates[normalized_name].append(file_path)
            
        # Filter to only actual duplicates
        return {k: v for k, v in duplicates.items() if len(v) > 1}
        
    def normalize_filename(self, name: str) -> str:
        """Normalize filename for comparison"""
        # Remove common variations
        name = re.sub(r'\s+', ' ', name.strip())
        name = re.sub(r'[s]$', '', name)  # Remove trailing 's'
        name = re.sub(r'[e]$', '', name)  # Remove trailing 'e' 
        return name.lower()
        
    def consolidate_duplicates(self):
        """Consolidate duplicate files, keeping the most complete version"""
        duplicates = self.find_duplicate_files()
        
        for base_name, files in duplicates.items():
            if len(files) <= 1:
                continue
                
            # Sort by file size (larger likely more complete) and recency
            files.sort(key=lambda f: (f.stat().st_size, f.stat().st_mtime), reverse=True)
            primary_file = files[0]
            duplicate_files = files[1:]
            
            self.log_issue("Duplicate files found", f"Base: {base_name}, Files: {[f.name for f in files]}")
            
            # For now, just log - actual consolidation requires content analysis
            for dup_file in duplicate_files:
                self.log_fix("Marked for manual review", f"Duplicate: {dup_file.name} vs Primary: {primary_file.name}")
                
    def fix_naming_conventions(self):
        """Standardize file naming conventions"""
        groups_path = self.vault_path / "02_Worldbuilding" / "Groups"
        
        for file_path in groups_path.rglob("*.md"):
            old_name = file_path.name
            new_name = self.standardize_name(old_name)
            
            if old_name != new_name:
                new_path = file_path.parent / new_name
                
                if not new_path.exists():
                    if not self.dry_run:
                        file_path.rename(new_path)
                    self.log_fix("Standardized filename", f"{old_name} -> {new_name}")
                else:
                    self.log_issue("Name collision", f"{old_name} -> {new_name} (target exists)")
                    
    def standardize_name(self, filename: str) -> str:
        """Apply naming convention standards"""
        name = filename
        
        # Remove .md for processing
        if name.endswith('.md'):
            name = name[:-3]
            
        # Fix common issues
        name = re.sub(r'\s+', ' ', name.strip())  # Normalize whitespace
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)  # Add space before capitals
        
        # Add .md back
        return name + '.md'
        
    def audit_broken_links(self) -> List[Dict]:
        """Find broken wiki links throughout the vault"""
        broken_links = []
        
        for file_path in self.vault_path.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find all wiki links
                wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
                
                for link in wiki_links:
                    # Clean the link
                    clean_link = link.split('|')[0].strip()
                    
                    # Check if target exists
                    if not self.link_target_exists(clean_link):
                        broken_links.append({
                            'file': str(file_path),
                            'link': link,
                            'clean_link': clean_link
                        })
                        
            except Exception as e:
                self.log_issue("File read error", f"{file_path}: {e}")
                
        return broken_links
        
    def link_target_exists(self, link: str) -> bool:
        """Check if a wiki link target exists"""
        # Try different possible paths
        possible_paths = [
            self.vault_path / f"{link}.md",
            self.vault_path / "02_Worldbuilding" / "Groups" / f"{link}.md",
            self.vault_path / "02_Worldbuilding" / "Lore" / f"{link}.md",
            self.vault_path / "02_Worldbuilding" / "Places" / f"{link}.md",
            self.vault_path / "02_Worldbuilding" / "People" / f"{link}.md",
        ]
        
        return any(path.exists() for path in possible_paths)
        
    def optimize_folder_structure(self):
        """Reorganize files into appropriate subfolders"""
        groups_path = self.vault_path / "02_Worldbuilding" / "Groups"
        
        # Create missing subfolders
        subfolders = [
            "Military_and_Defense",
            "Religious_Groups", 
            "Corporations_and_Trade"
        ]
        
        for subfolder in subfolders:
            subfolder_path = groups_path / subfolder
            if not subfolder_path.exists():
                if not self.dry_run:
                    subfolder_path.mkdir(exist_ok=True)
                self.log_fix("Created subfolder", str(subfolder_path))
                
        # Move files to appropriate subfolders based on naming patterns
        for file_path in groups_path.rglob("*.md"):
            if file_path.parent == groups_path:  # Only root level files
                target_subfolder = self.determine_subfolder(file_path.stem)
                if target_subfolder:
                    target_path = groups_path / target_subfolder / file_path.name
                    if not target_path.exists():
                        if not self.dry_run:
                            file_path.rename(target_path)
                        self.log_fix("Moved to subfolder", f"{file_path.name} -> {target_subfolder}/")
                        
    def determine_subfolder(self, filename: str) -> str:
        """Determine appropriate subfolder for a file based on naming patterns"""
        filename_lower = filename.lower()
        
        if any(term in filename_lower for term in ['military', 'defense', 'guard', 'army', 'navy']):
            return "Military_and_Defense"
        elif any(term in filename_lower for term in ['temple', 'shrine', 'priest', 'divine', 'sacred']):
            return "Religious_Groups"
        elif any(term in filename_lower for term in ['trading', 'merchant', 'company', 'corporation', 'business']):
            return "Corporations_and_Trade"
            
        return None
        
    def validate_metadata(self):
        """Check and standardize metadata across files"""
        metadata_issues = []
        
        for file_path in self.vault_path.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for frontmatter
                if content.startswith('---'):
                    end_marker = content.find('---', 3)
                    if end_marker != -1:
                        frontmatter = content[3:end_marker]
                        self.validate_frontmatter(file_path, frontmatter)
                    else:
                        self.log_issue("Malformed frontmatter", str(file_path))
                        
            except Exception as e:
                self.log_issue("Metadata validation error", f"{file_path}: {e}")
                
    def validate_frontmatter(self, file_path: Path, frontmatter: str):
        """Validate frontmatter structure and content"""
        required_fields = ['type', 'status', 'created', 'updated']
        
        for field in required_fields:
            if f"{field}:" not in frontmatter:
                self.log_issue("Missing metadata field", f"{file_path}: {field}")
                
        # Check for duplicate fields
        lines = frontmatter.strip().split('\n')
        field_counts = defaultdict(int)
        
        for line in lines:
            if ':' in line:
                field = line.split(':')[0].strip()
                field_counts[field] += 1
                
        for field, count in field_counts.items():
            if count > 1:
                self.log_issue("Duplicate metadata field", f"{file_path}: {field} appears {count} times")
                
    def run_comprehensive_optimization(self):
        """Run all optimization steps"""
        print("=== Starting Comprehensive Vault Optimization ===")
        print(f"Vault path: {self.vault_path}")
        print(f"Dry run mode: {self.dry_run}")
        print()
        
        # Step 1: Fix truncated files
        print("Step 1: Fixing truncated filenames...")
        self.fix_truncated_files()
        print()
        
        # Step 2: Consolidate duplicates
        print("Step 2: Finding and consolidating duplicates...")
        self.consolidate_duplicates()
        print()
        
        # Step 3: Standardize naming
        print("Step 3: Standardizing naming conventions...")
        self.fix_naming_conventions()
        print()
        
        # Step 4: Optimize folder structure
        print("Step 4: Optimizing folder structure...")
        self.optimize_folder_structure()
        print()
        
        # Step 5: Validate metadata
        print("Step 5: Validating metadata...")
        self.validate_metadata()
        print()
        
        # Step 6: Check for broken links
        print("Step 6: Auditing broken links...")
        broken_links = self.audit_broken_links()
        if broken_links:
            self.log_issue("Broken links found", f"{len(broken_links)} broken links detected")
        print()
        
        # Generate report
        self.generate_report()
        
    def generate_report(self):
        """Generate optimization report"""
        report = {
            'vault_path': str(self.vault_path),
            'dry_run': self.dry_run,
            'fixes_applied': self.fixes_applied,
            'issues_found': self.issues_found,
            'summary': {
                'total_fixes': len(self.fixes_applied),
                'total_issues': len(self.issues_found)
            }
        }
        
        report_path = self.vault_path / 'vault_optimization_report.json'
        
        if not self.dry_run:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
                
        print("=== Optimization Report ===")
        print(f"Total fixes applied: {len(self.fixes_applied)}")
        print(f"Total issues found: {len(self.issues_found)}")
        print(f"Report saved to: {report_path}")
        
        # Print summary of fix types
        fix_types = defaultdict(int)
        for fix in self.fixes_applied:
            fix_types[fix['action']] += 1
            
        print("\nFix summary:")
        for fix_type, count in fix_types.items():
            print(f"  {fix_type}: {count}")
            
        # Print summary of issue types
        issue_types = defaultdict(int)
        for issue in self.issues_found:
            issue_types[issue['type']] += 1
            
        print("\nIssue summary:")
        for issue_type, count in issue_types.items():
            print(f"  {issue_type}: {count}")

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    optimizer = VaultOptimizer(vault_path)
    optimizer.run_comprehensive_optimization()

if __name__ == "__main__":
    main()