#!/usr/bin/env python3
"""
Comprehensive Link Integrity Analyzer for Obsidian Vault
Analyzes WikiLinks, broken references, orphaned files, and link density
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

class LinkIntegrityAnalyzer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.md_files = set()
        self.all_links = defaultdict(list)  # file -> list of links
        self.backlinks = defaultdict(set)   # target -> set of files linking to it
        self.broken_links = defaultdict(list)
        self.orphan_files = set()
        self.duplicate_links = defaultdict(list)
        self.link_density = {}
        
        # Patterns for different link types
        self.wikilink_pattern = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
        self.markdown_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
    def scan_vault(self):
        """Scan the entire vault for markdown files and collect links"""
        print("Scanning vault for markdown files...")
        
        for file_path in self.vault_path.rglob('*.md'):
            if file_path.is_file():
                relative_path = str(file_path.relative_to(self.vault_path))
                self.md_files.add(relative_path)
                self._extract_links_from_file(file_path, relative_path)
        
        print(f"Found {len(self.md_files)} markdown files")
        
    def _extract_links_from_file(self, file_path: Path, relative_path: str):
        """Extract all WikiLinks and markdown links from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract WikiLinks
            wikilinks = self.wikilink_pattern.findall(content)
            for link_target, display_text in wikilinks:
                # Clean the link target
                target = link_target.strip()
                if '|' in target:
                    target = target.split('|')[0].strip()
                
                self.all_links[relative_path].append({
                    'type': 'wikilink',
                    'target': target,
                    'display': display_text or target,
                    'raw': f'[[{link_target}]]'
                })
                
                # Build backlinks
                self.backlinks[target].add(relative_path)
                
            # Extract markdown links to local files
            md_links = self.markdown_link_pattern.findall(content)
            for display_text, link_target in md_links:
                if not (link_target.startswith('http') or link_target.startswith('mailto:')):
                    self.all_links[relative_path].append({
                        'type': 'markdown',
                        'target': link_target,
                        'display': display_text,
                        'raw': f'[{display_text}]({link_target})'
                    })
                    
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    def find_broken_links(self):
        """Identify broken WikiLinks and file references"""
        print("Analyzing broken links...")
        
        for source_file, links in self.all_links.items():
            for link in links:
                target = link['target']
                is_broken = False
                
                if link['type'] == 'wikilink':
                    # Check various possible paths for WikiLinks
                    possible_paths = [
                        f"{target}.md",
                        target,
                        f"02_Worldbuilding/People/{target}.md",
                        f"02_Worldbuilding/Places/{target}.md",
                        f"02_Worldbuilding/Groups/{target}.md",
                        f"02_Worldbuilding/Lore/{target}.md",
                        f"02_Worldbuilding/Items/{target}.md",
                        f"03_Mechanics/{target}.md",
                    ]
                    
                    # Also check if it's a reference to a file in any subdirectory
                    if not any(path in self.md_files for path in possible_paths):
                        # Check if target exists anywhere in vault (fuzzy matching)
                        found = False
                        for md_file in self.md_files:
                            file_name = Path(md_file).stem
                            if file_name == target or file_name.replace('_', ' ') == target:
                                found = True
                                break
                        
                        if not found:
                            is_broken = True
                            
                elif link['type'] == 'markdown':
                    # Check if markdown link target exists
                    target_path = Path(self.vault_path / source_file).parent / target
                    if not target_path.exists():
                        is_broken = True
                
                if is_broken:
                    self.broken_links[source_file].append(link)
    
    def find_orphan_files(self):
        """Find files with no incoming links"""
        print("Identifying orphan files...")
        
        linked_files = set()
        
        # Collect all linked targets
        for target_set in self.backlinks.values():
            linked_files.update(target_set)
        
        # Also consider files mentioned in links (even if broken)
        for source_file, links in self.all_links.items():
            for link in links:
                target = link['target']
                # Try to match target to actual files
                for md_file in self.md_files:
                    file_name = Path(md_file).stem
                    if file_name == target or file_name.replace('_', ' ') == target:
                        linked_files.add(md_file)
        
        # Files with no incoming links are orphans
        self.orphan_files = self.md_files - linked_files
        
        # Remove index files and main navigation files from orphans
        navigation_files = {
            'README.md', 'INDEX.md', 'Master_Campaign_Index.md',
            'Player_Portal.md', 'Campaign_Dashboard.md',
            '1-DM Toolkit/Home.md', 'Vault_Navigation_Hub.md'
        }
        
        self.orphan_files = {f for f in self.orphan_files if f not in navigation_files}
    
    def find_duplicate_links(self):
        """Find duplicate and redundant links"""
        print("Analyzing duplicate links...")
        
        for source_file, links in self.all_links.items():
            # Group links by target
            target_count = Counter(link['target'] for link in links)
            
            # Find targets with multiple links
            for target, count in target_count.items():
                if count > 1:
                    duplicate_links = [link for link in links if link['target'] == target]
                    self.duplicate_links[source_file].append({
                        'target': target,
                        'count': count,
                        'links': duplicate_links
                    })
    
    def calculate_link_density(self):
        """Calculate link density metrics"""
        print("Calculating link density...")
        
        for file_path in self.md_files:
            outgoing = len(self.all_links.get(file_path, []))
            incoming = len(self.backlinks.get(Path(file_path).stem, set()))
            
            self.link_density[file_path] = {
                'outgoing': outgoing,
                'incoming': incoming,
                'total': outgoing + incoming
            }
    
    def generate_report(self) -> Dict:
        """Generate comprehensive report"""
        print("Generating analysis report...")
        
        # Find highly connected files
        high_outgoing = sorted(
            [(f, data['outgoing']) for f, data in self.link_density.items()],
            key=lambda x: x[1], reverse=True
        )[:10]
        
        high_incoming = sorted(
            [(f, data['incoming']) for f, data in self.link_density.items()],
            key=lambda x: x[1], reverse=True
        )[:10]
        
        report = {
            'summary': {
                'total_files': len(self.md_files),
                'total_links': sum(len(links) for links in self.all_links.values()),
                'broken_links_count': sum(len(links) for links in self.broken_links.values()),
                'orphan_files_count': len(self.orphan_files),
                'files_with_duplicates': len(self.duplicate_links)
            },
            'broken_links': dict(self.broken_links),
            'orphan_files': list(self.orphan_files),
            'duplicate_links': dict(self.duplicate_links),
            'link_density': {
                'high_outgoing': high_outgoing,
                'high_incoming': high_incoming,
                'zero_outgoing': [f for f, data in self.link_density.items() if data['outgoing'] == 0],
                'zero_incoming': [f for f, data in self.link_density.items() if data['incoming'] == 0]
            }
        }
        
        return report
    
    def analyze(self) -> Dict:
        """Run complete analysis"""
        self.scan_vault()
        self.find_broken_links()
        self.find_orphan_files()
        self.find_duplicate_links()
        self.calculate_link_density()
        return self.generate_report()

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    analyzer = LinkIntegrityAnalyzer(vault_path)
    report = analyzer.analyze()
    
    # Save detailed report
    with open(f"{vault_path}/link_integrity_analysis.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n" + "="*50)
    print("LINK INTEGRITY ANALYSIS SUMMARY")
    print("="*50)
    print(f"Total Files: {report['summary']['total_files']}")
    print(f"Total Links: {report['summary']['total_links']}")
    print(f"Broken Links: {report['summary']['broken_links_count']}")
    print(f"Orphan Files: {report['summary']['orphan_files_count']}")
    print(f"Files with Duplicate Links: {report['summary']['files_with_duplicates']}")
    
    if report['broken_links']:
        print("\nFILES WITH BROKEN LINKS:")
        for file_path, broken in list(report['broken_links'].items())[:10]:
            print(f"  {file_path}: {len(broken)} broken link(s)")
    
    if report['orphan_files']:
        print(f"\nORPHAN FILES (showing first 10 of {len(report['orphan_files'])}):")
        for orphan in report['orphan_files'][:10]:
            print(f"  {orphan}")
    
    print(f"\nDetailed report saved to: link_integrity_analysis.json")

if __name__ == "__main__":
    main()