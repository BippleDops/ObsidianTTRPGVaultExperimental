#!/usr/bin/env python3
"""
Vault Hygiene Audit Script
Analyzes vault for common issues and provides actionable report.
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import json

class VaultAuditor:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.issues = defaultdict(list)
        self.stats = {
            'total_files': 0,
            'markdown_files': 0,
            'orphaned_files': 0,
            'missing_frontmatter': 0,
            'duplicate_ids': 0,
            'broken_links': 0,
            'large_files': 0,
            'conflicted_files': 0,
            'anomalous_names': 0
        }
        self.id_map = {}
        self.link_map = defaultdict(set)
        
    def audit(self):
        """Run complete audit"""
        print("Starting Vault Hygiene Audit...")
        print("=" * 50)
        
        self.scan_files()
        self.check_broken_links()
        self.check_file_sizes()
        self.check_anomalous_names()
        self.generate_report()
        
    def scan_files(self):
        """Scan all files in vault"""
        for root, dirs, files in os.walk(self.vault_path):
            # Skip hidden and system directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                self.stats['total_files'] += 1
                
                if file.endswith('.md'):
                    self.stats['markdown_files'] += 1
                    file_path = Path(root) / file
                    self.analyze_markdown(file_path)
                    
                # Check for conflicted files
                if 'conflicted' in file.lower():
                    self.stats['conflicted_files'] += 1
                    self.issues['conflicted'].append(str(Path(root) / file))
                    
    def analyze_markdown(self, file_path: Path):
        """Analyze individual markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check frontmatter
            if not content.startswith('---'):
                self.stats['missing_frontmatter'] += 1
                self.issues['missing_frontmatter'].append(str(file_path))
            else:
                # Extract frontmatter
                fm_end = content.find('---', 3)
                if fm_end > 0:
                    fm_text = content[3:fm_end]
                    try:
                        frontmatter = yaml.safe_load(fm_text) or {}
                        
                        # Check for ID
                        if 'id' in frontmatter:
                            file_id = frontmatter['id']
                            if file_id in self.id_map:
                                self.stats['duplicate_ids'] += 1
                                self.issues['duplicate_ids'].append(
                                    f"{file_id}: {file_path} and {self.id_map[file_id]}"
                                )
                            else:
                                self.id_map[file_id] = str(file_path)
                                
                        # Check for required fields
                        required = ['status', 'type', 'domain']
                        for field in required:
                            if field not in frontmatter:
                                self.issues['missing_fields'].append(
                                    f"{file_path}: missing '{field}'"
                                )
                    except:
                        self.issues['invalid_frontmatter'].append(str(file_path))
                        
            # Extract links
            wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
            for link in wiki_links:
                # Clean link (remove aliases)
                clean_link = link.split('|')[0].strip()
                self.link_map[str(file_path)].add(clean_link)
                
        except Exception as e:
            self.issues['read_errors'].append(f"{file_path}: {e}")
            
    def check_broken_links(self):
        """Check for broken internal links"""
        all_files = set()
        
        # Build set of all existing files
        for root, dirs, files in os.walk(self.vault_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.endswith('.md'):
                    # Store without extension for matching
                    file_name = file[:-3]
                    all_files.add(file_name)
                    # Also store with path
                    rel_path = Path(root).relative_to(self.vault_path) / file_name
                    all_files.add(str(rel_path))
                    
        # Check all links
        for source_file, links in self.link_map.items():
            for link in links:
                # Skip external links and headers
                if link.startswith('http') or '#' in link:
                    continue
                    
                # Check if link target exists
                if link not in all_files:
                    self.stats['broken_links'] += 1
                    self.issues['broken_links'].append(
                        f"{source_file}: [[{link}]]"
                    )
                    
    def check_file_sizes(self):
        """Check for unusually large files"""
        for root, dirs, files in os.walk(self.vault_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                size = file_path.stat().st_size
                
                # Flag files over 1MB
                if size > 1_000_000:
                    self.stats['large_files'] += 1
                    size_mb = size / 1_000_000
                    self.issues['large_files'].append(
                        f"{file_path}: {size_mb:.2f} MB"
                    )
                    
    def check_anomalous_names(self):
        """Check for files with problematic names"""
        patterns = [
            (r'^#', 'starts with #'),
            (r'^\$', 'starts with $'),
            (r'^%', 'starts with %'),
            (r'^<', 'starts with <'),
            (r'\s+\(\w+\)\.md$', 'has (category) suffix'),
            (r'_\d+\.md$', 'has duplicate marker'),
            (r'\.png\.md$', 'image extension.md'),
            (r'\.svg\.md$', 'image extension.md'),
            (r'\.json\.md$', 'data extension.md'),
            (r'^step_\d+.*phase', 'step_X phase pattern')
        ]
        
        for root, dirs, files in os.walk(self.vault_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                for pattern, description in patterns:
                    if re.search(pattern, file):
                        self.stats['anomalous_names'] += 1
                        self.issues['anomalous_names'].append(
                            f"{Path(root) / file}: {description}"
                        )
                        break
                        
        
    def generate_report(self):
        """Generate and display audit report"""
        print("\n" + "=" * 50)
        print("VAULT HYGIENE AUDIT REPORT")
        print("=" * 50)
        
        # Statistics
        print("\n📊 STATISTICS:")
        print(f"  Total Files: {self.stats['total_files']:,}")
        print(f"  Markdown Files: {self.stats['markdown_files']:,}")
        print(f"  Missing Frontmatter: {self.stats['missing_frontmatter']:,}")
        print(f"  Duplicate IDs: {self.stats['duplicate_ids']:,}")
        print(f"  Broken Links: {self.stats['broken_links']:,}")
        print(f"  Large Files: {self.stats['large_files']:,}")
        print(f"  Conflicted Files: {self.stats['conflicted_files']:,}")
        print(f"  Anomalous Names: {self.stats['anomalous_names']:,}")
        
        # Critical Issues
        critical = ['conflicted', 'duplicate_ids', 'large_files']
        has_critical = False
        
        for issue_type in critical:
            if self.issues[issue_type]:
                if not has_critical:
                    print("\n🚨 CRITICAL ISSUES:")
                    has_critical = True
                    
                print(f"\n  {issue_type.upper().replace('_', ' ')}:")
                for item in self.issues[issue_type][:10]:
                    print(f"    - {item}")
                if len(self.issues[issue_type]) > 10:
                    print(f"    ... and {len(self.issues[issue_type]) - 10} more")
                    
        # Warnings
        warnings = ['missing_frontmatter', 'broken_links', 'anomalous_names']
        has_warnings = False
        
        for issue_type in warnings:
            if self.issues[issue_type]:
                if not has_warnings:
                    print("\n⚠️  WARNINGS:")
                    has_warnings = True
                    
                print(f"\n  {issue_type.upper().replace('_', ' ')}:")
                for item in self.issues[issue_type][:5]:
                    print(f"    - {item}")
                if len(self.issues[issue_type]) > 5:
                    print(f"    ... and {len(self.issues[issue_type]) - 5} more")
                    
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        
        if self.stats['conflicted_files'] > 0:
            print("  1. Run conflict resolution script")
        if self.stats['duplicate_ids'] > 0:
            print("  2. Run ID deduplication script")
        if self.stats['missing_frontmatter'] > 100:
            print("  3. Run frontmatter generation script")
        if self.stats['broken_links'] > 50:
            print("  4. Run broken link cleanup script")
        if self.stats['large_files'] > 0:
            print("  5. Review and optimize large files")
        if self.stats['anomalous_names'] > 0:
            print("  6. Run naming normalization script")
            
        # Save detailed report
        report_path = self.vault_path / '_METADATA' / 'hygiene_audit_report.json'
        report_path.parent.mkdir(exist_ok=True)
        
        report_data = {
            'timestamp': str(Path.cwd()),
            'statistics': self.stats,
            'issues': dict(self.issues)
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: {report_path}")
        print("=" * 50)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Audit vault hygiene')
    parser.add_argument('--vault', 
                       default="/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVaultExperimental",
                       help='Path to vault')
    
    args = parser.parse_args()
    
    auditor = VaultAuditor(args.vault)
    auditor.audit()

if __name__ == "__main__":
    main()