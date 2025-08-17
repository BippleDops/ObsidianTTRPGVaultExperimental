#!/usr/bin/env python3
"""
Comprehensive Broken Link Repair Script
Systematically fixes broken internal links in the vault.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import json
from difflib import SequenceMatcher

class ComprehensiveLinkFixer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.file_index = {}  # Map of file names to paths
        self.id_index = {}    # Map of IDs to files
        self.broken_links = defaultdict(list)
        self.fixed_count = 0
        self.unfixable_count = 0
        
        # Common link patterns that are actually OK
        self.ignore_patterns = [
            r'^https?://',      # External URLs
            r'^#',              # Headers only
            r'^\d+$',           # Pure numbers
            r'^TODO',           # TODO markers
            r'^TBD',            # TBD markers
            r'^XXX',            # Placeholder markers
            r'^\.\.',           # Relative paths
            r'^/',              # Absolute paths
        ]
        
    def build_file_index(self):
        """Build an index of all files in the vault"""
        print("Building file index...")
        
        for root, dirs, files in os.walk(self.vault_path):
            # Skip system directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            if any(skip in root for skip in ['.git', '.obsidian', '08_Archive']):
                continue
                
            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file
                    
                    # Store by various keys for matching
                    name_no_ext = file[:-3]
                    
                    # Full name
                    self.file_index[name_no_ext] = file_path
                    
                    # Without ID prefix
                    if re.match(r'^[A-Z]{2,4}\d{3,5}[-_]', name_no_ext):
                        clean_name = re.sub(r'^[A-Z]{2,4}\d{3,5}[-_]', '', name_no_ext)
                        self.file_index[clean_name] = file_path
                    
                    # Underscores to spaces
                    spaced_name = name_no_ext.replace('_', ' ')
                    self.file_index[spaced_name] = file_path
                    
                    # Extract ID from frontmatter
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if content.startswith('---'):
                                fm_end = content.find('---', 3)
                                if fm_end > 0:
                                    fm_text = content[3:fm_end]
                                    # Simple ID extraction
                                    id_match = re.search(r'^id:\s*(.+)$', fm_text, re.MULTILINE)
                                    if id_match:
                                        file_id = id_match.group(1).strip()
                                        self.id_index[file_id] = file_path
                    except:
                        pass
                        
        print(f"Indexed {len(self.file_index)} file variations")
        print(f"Found {len(self.id_index)} files with IDs")
        
    def find_broken_links(self):
        """Find all broken links in the vault"""
        print("\nScanning for broken links...")
        
        for root, dirs, files in os.walk(self.vault_path):
            # Skip system directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            if any(skip in root for skip in ['.git', '.obsidian', '08_Archive']):
                continue
                
            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file
                    self.scan_file_links(file_path)
                    
        total_broken = sum(len(links) for links in self.broken_links.values())
        print(f"Found {total_broken} broken links in {len(self.broken_links)} files")
        
    def scan_file_links(self, file_path: Path):
        """Scan a single file for broken links"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all wiki links
            wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
            
            for link in wiki_links:
                # Remove alias if present
                link_target = link.split('|')[0].strip()
                
                # Skip ignored patterns
                if any(re.match(pattern, link_target) for pattern in self.ignore_patterns):
                    continue
                    
                # Remove section references
                base_link = link_target.split('#')[0].strip()
                
                if base_link and not self.link_exists(base_link):
                    self.broken_links[str(file_path)].append(link_target)
                    
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
            
    def link_exists(self, link: str) -> bool:
        """Check if a link target exists"""
        # Direct match
        if link in self.file_index:
            return True
            
        # ID match
        if link in self.id_index:
            return True
            
        # Try with .md extension removed
        if link.endswith('.md'):
            return self.link_exists(link[:-3])
            
        # Try relative path resolution
        if '/' in link:
            parts = link.split('/')
            filename = parts[-1]
            if filename in self.file_index:
                return True
                
        return False
        
    def find_best_match(self, broken_link: str) -> str:
        """Find the best matching file for a broken link"""
        # Clean the link
        clean_link = broken_link.split('#')[0].strip()
        clean_link = clean_link.replace('.md', '')
        
        # Try exact ID match
        if clean_link in self.id_index:
            return self.make_relative_link(self.id_index[clean_link])
            
        # Try various transformations
        candidates = []
        
        # Direct name match
        if clean_link in self.file_index:
            candidates.append((1.0, self.file_index[clean_link]))
            
        # Try with underscores/spaces swapped
        underscore_version = clean_link.replace(' ', '_')
        if underscore_version in self.file_index:
            candidates.append((0.9, self.file_index[underscore_version]))
            
        space_version = clean_link.replace('_', ' ')
        if space_version in self.file_index:
            candidates.append((0.9, self.file_index[space_version]))
            
        # Fuzzy matching for similar names
        clean_lower = clean_link.lower()
        for name, path in self.file_index.items():
            if clean_lower in name.lower() or name.lower() in clean_lower:
                similarity = SequenceMatcher(None, clean_link.lower(), name.lower()).ratio()
                if similarity > 0.6:  # 60% similarity threshold
                    candidates.append((similarity, path))
                    
        # Return best match
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return self.make_relative_link(candidates[0][1])
            
        return None
        
    def make_relative_link(self, target_path: Path) -> str:
        """Create a proper link to the target file"""
        # Use just the filename without extension for Obsidian
        return target_path.stem
        
    def fix_file_links(self, file_path: str, broken_links: List[str]) -> int:
        """Fix broken links in a single file"""
        fixed_in_file = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            for broken_link in broken_links:
                # Find the best match
                fixed_link = self.find_best_match(broken_link)
                
                if fixed_link:
                    # Replace the broken link
                    # Handle both with and without aliases
                    if '|' in broken_link:
                        # Preserve alias
                        alias = broken_link.split('|')[1]
                        old_pattern = f'[[{broken_link}]]'
                        new_pattern = f'[[{fixed_link}|{alias}]]'
                    else:
                        old_pattern = f'[[{broken_link}]]'
                        new_pattern = f'[[{fixed_link}]]'
                        
                    if old_pattern in content:
                        content = content.replace(old_pattern, new_pattern)
                        fixed_in_file += 1
                        self.fixed_count += 1
                else:
                    self.unfixable_count += 1
                    
            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")
            
        return fixed_in_file
        
    def fix_broken_links(self, dry_run: bool = False):
        """Fix all broken links"""
        print("\n" + "=" * 50)
        print("FIXING BROKEN LINKS")
        print("=" * 50)
        
        if dry_run:
            print("\n🔍 DRY RUN MODE - No files will be modified")
            
        files_to_fix = list(self.broken_links.keys())
        total_files = len(files_to_fix)
        
        for i, file_path in enumerate(files_to_fix, 1):
            broken = self.broken_links[file_path]
            
            if dry_run:
                if i <= 10:  # Show first 10 files in dry run
                    print(f"\n[{i}/{total_files}] {Path(file_path).name}")
                    print(f"  Would fix {len(broken)} broken links")
                    
                    # Show examples
                    for link in broken[:3]:
                        match = self.find_best_match(link)
                        if match:
                            print(f"    [[{link}]] → [[{match}]]")
                        else:
                            print(f"    [[{link}]] → [NO MATCH FOUND]")
                            
                    if len(broken) > 3:
                        print(f"    ... and {len(broken) - 3} more")
            else:
                fixed = self.fix_file_links(file_path, broken)
                if fixed > 0:
                    print(f"[{i}/{total_files}] Fixed {fixed}/{len(broken)} links in {Path(file_path).name}")
                    
        if dry_run and total_files > 10:
            print(f"\n... and {total_files - 10} more files")
                    
    def generate_report(self):
        """Generate a report of the fixes"""
        print("\n" + "=" * 50)
        print("BROKEN LINK REPAIR REPORT")
        print("=" * 50)
        
        print(f"\n📊 Statistics:")
        print(f"  Files scanned: {len(self.file_index)}")
        print(f"  Files with broken links: {len(self.broken_links)}")
        print(f"  Total broken links found: {sum(len(links) for links in self.broken_links.values())}")
        print(f"  Links fixed: {self.fixed_count}")
        print(f"  Links unfixable: {self.unfixable_count}")
        
        if self.unfixable_count > 0:
            print(f"\n⚠️  {self.unfixable_count} links could not be automatically fixed")
            print("  These may be:")
            print("    - References to files that don't exist")
            print("    - Placeholder links")
            print("    - Links to sections that were removed")
            
        # Save detailed report
        report_path = self.vault_path / '_METADATA' / 'broken_links_report.json'
        report_data = {
            'statistics': {
                'files_scanned': len(self.file_index),
                'files_with_broken_links': len(self.broken_links),
                'total_broken_links': sum(len(links) for links in self.broken_links.values()),
                'links_fixed': self.fixed_count,
                'links_unfixable': self.unfixable_count
            },
            'unfixable_links': {}
        }
        
        # Collect unfixable links
        for file_path, links in self.broken_links.items():
            unfixable = []
            for link in links:
                if not self.find_best_match(link):
                    unfixable.append(link)
            if unfixable:
                report_data['unfixable_links'][file_path] = unfixable[:10]  # Limit to 10 per file
                
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: {report_path}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix broken internal links')
    parser.add_argument('--vault',
                       default="/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVaultExperimental",
                       help='Path to vault')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview fixes without making changes')
    parser.add_argument('--limit', type=int, default=100,
                       help='Limit number of files to process')
    
    args = parser.parse_args()
    
    fixer = ComprehensiveLinkFixer(args.vault)
    
    # Build indexes
    fixer.build_file_index()
    
    # Find broken links
    fixer.find_broken_links()
    
    # Fix them
    if args.limit and args.limit < len(fixer.broken_links):
        # Limit for testing
        limited = dict(list(fixer.broken_links.items())[:args.limit])
        fixer.broken_links = limited
        print(f"\n⚠️  Limited to first {args.limit} files for safety")
        
    fixer.fix_broken_links(dry_run=args.dry_run)
    
    # Report
    fixer.generate_report()

if __name__ == "__main__":
    main()