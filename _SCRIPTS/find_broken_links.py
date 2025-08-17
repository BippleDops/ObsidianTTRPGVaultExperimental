#!/usr/bin/env python3
"""
Find broken WikiLinks and orphaned files
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter

class BrokenLinkFinder:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.all_files = set()
        self.file_stems = {}  # stem -> full_path
        self.broken_links = defaultdict(list)
        self.orphaned_files = set()
        self.all_links = defaultdict(set)
        self.incoming_links = defaultdict(set)
        
    def scan_files(self):
        """Get all markdown files and their stems"""
        print("Scanning for all markdown files...")
        
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.is_file():
                rel_path = str(md_file.relative_to(self.vault_path))
                self.all_files.add(rel_path)
                stem = md_file.stem
                self.file_stems[stem] = rel_path
        
        print(f"Found {len(self.all_files)} markdown files")
    
    def find_broken_links(self):
        """Find WikiLinks that don't resolve to actual files"""
        print("Analyzing WikiLinks...")
        
        wikilink_pattern = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
        
        for md_file in self.vault_path.rglob("*.md"):
            if not md_file.is_file():
                continue
                
            rel_path = str(md_file.relative_to(self.vault_path))
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all WikiLinks
                for match in wikilink_pattern.finditer(content):
                    link_target = match.group(1).strip()
                    
                    # Clean up the link target
                    if '#' in link_target:
                        link_target = link_target.split('#')[0]
                    
                    if '/' in link_target:
                        # Path-style link
                        target_path = link_target + ('.md' if not link_target.endswith('.md') else '')
                        if target_path not in self.all_files:
                            self.broken_links[rel_path].append(link_target)
                        else:
                            self.incoming_links[target_path].add(rel_path)
                    else:
                        # Name-only link
                        if link_target in self.file_stems:
                            target_file = self.file_stems[link_target]
                            self.incoming_links[target_file].add(rel_path)
                        else:
                            # Check if it exists with .md extension
                            target_with_ext = f"{link_target}.md"
                            found = False
                            for file_path in self.all_files:
                                if Path(file_path).name == target_with_ext:
                                    self.incoming_links[file_path].add(rel_path)
                                    found = True
                                    break
                            
                            if not found:
                                self.broken_links[rel_path].append(link_target)
                    
                    self.all_links[rel_path].add(link_target)
                    
            except Exception as e:
                print(f"Error reading {md_file}: {e}")
    
    def find_orphaned_files(self):
        """Find files with no incoming links"""
        print("Finding orphaned files...")
        
        # Navigation and index files that shouldn't be considered orphans
        navigation_files = {
            'README.md', 'AQUABYSSOS_VAULT_README.md', 'Master_Campaign_Index.md',
            'Campaign_Dashboard.md', 'Vault_Navigation_Hub.md', 'CLAUDE.md',
            '1-DM Toolkit/Home.md', '07_Player_Resources/Player_Portal.md',
            '07_Player_Resources/INDEX.md'
        }
        
        # Files that have incoming links
        linked_files = set(self.incoming_links.keys())
        
        # Find orphans
        for file_path in self.all_files:
            if file_path not in linked_files and file_path not in navigation_files:
                # Skip archive, report, and script files
                if not any(skip in file_path for skip in ['08_Archive', 'reports/', 'scripts/', 'nohup.out', '.txt', '.py']):
                    self.orphaned_files.add(file_path)
    
    def analyze(self):
        """Run complete analysis"""
        self.scan_files()
        self.find_broken_links()
        self.find_orphaned_files()
        
        # Print results
        print(f"\n{'='*50}")
        print("BROKEN LINKS ANALYSIS")
        print(f"{'='*50}")
        
        total_broken = sum(len(links) for links in self.broken_links.values())
        print(f"Files with broken links: {len(self.broken_links)}")
        print(f"Total broken links: {total_broken}")
        
        if self.broken_links:
            print(f"\nTop files with broken links:")
            sorted_broken = sorted(self.broken_links.items(), key=lambda x: len(x[1]), reverse=True)
            for file_path, broken_links in sorted_broken[:10]:
                print(f"  {file_path}: {len(broken_links)} broken link(s)")
                for link in broken_links[:3]:  # Show first 3
                    print(f"    -> {link}")
                if len(broken_links) > 3:
                    print(f"    ... and {len(broken_links) - 3} more")
        
        print(f"\n{'='*50}")
        print("ORPHANED FILES ANALYSIS")
        print(f"{'='*50}")
        print(f"Orphaned files: {len(self.orphaned_files)}")
        
        if self.orphaned_files:
            print(f"\nOrphaned files (first 20):")
            for orphan in sorted(list(self.orphaned_files))[:20]:
                print(f"  {orphan}")
            
            if len(self.orphaned_files) > 20:
                print(f"  ... and {len(self.orphaned_files) - 20} more")
        
        return {
            'broken_links': dict(self.broken_links),
            'orphaned_files': list(self.orphaned_files),
            'summary': {
                'total_files': len(self.all_files),
                'files_with_broken_links': len(self.broken_links),
                'total_broken_links': total_broken,
                'orphaned_files': len(self.orphaned_files)
            }
        }

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    finder = BrokenLinkFinder(vault_path)
    results = finder.analyze()
    
    # Save results for further processing
    import json
    with open(f"{vault_path}/broken_links_analysis.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to broken_links_analysis.json")

if __name__ == "__main__":
    main()