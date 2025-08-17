#!/usr/bin/env python3
"""
Parallel Broken Link Fixer
Processes files in parallel for better performance.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

class ParallelLinkFixer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.file_index = {}  # Map of file names to paths
        self.id_index = {}    # Map of IDs to files
        self.stats_lock = threading.Lock()
        self.fixed_count = 0
        self.unfixable_count = 0
        self.files_processed = 0
        
        # Common link patterns that are actually OK
        self.ignore_patterns = [
            r'^https?://',      # External URLs
            r'^#',              # Headers only
            r'^\d+$',           # Pure numbers
            r'^TODO',           # TODO markers
            r'^TBD',            # TBD markers
            r'^XXX',            # Placeholder markers
            r'^\..',           # Relative paths
            r'^/',              # Absolute paths
            r'^step_\d+',       # Step references (to be removed)
            r'^Related_Content', # Meta placeholders
            r'^SYSTEM_STATUS',
            r'^NPC Motivations',
            r'^Diplomacy Rules',
            r'^Political Factions',
        ]
        
    def build_file_index(self):
        """Build an index of all files in the vault"""
        print("Building file index...")
        
        for root, dirs, files in os.walk(self.vault_path):
            # Skip system directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            if any(skip in root for skip in ['.git', '.obsidian', '08_Archive', '09_Performance', '_SCRIPTS']):
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
                    
                    # Extract ID from frontmatter (quick scan)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            # Just read first 500 chars for frontmatter
                            start = f.read(500)
                            if start.startswith('---'):
                                fm_end = start.find('---', 3)
                                if fm_end > 0:
                                    fm_text = start[3:fm_end]
                                    id_match = re.search(r'^id:\s*(.+)$', fm_text, re.MULTILINE)
                                    if id_match:
                                        file_id = id_match.group(1).strip()
                                        self.id_index[file_id] = file_path
                    except:
                        pass
                        
        print(f"Indexed {len(self.file_index)} file variations")
        print(f"Found {len(self.id_index)} files with IDs")
        
    def find_best_match(self, broken_link: str) -> str:
        """Find the best matching file for a broken link"""
        # Clean the link
        clean_link = broken_link.split('#')[0].strip()
        clean_link = clean_link.replace('.md', '')
        
        # Try exact ID match
        if clean_link in self.id_index:
            return self.id_index[clean_link].stem
            
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
            
        # Return best match
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1].stem
            
        return None
        
    def process_file(self, file_path: Path) -> Tuple[int, int]:
        """Process a single file and fix its broken links"""
        fixed_in_file = 0
        unfixable_in_file = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Remove meta placeholders first
            meta_placeholders = [
                r'\[\[Related_Content\]\]',
                r'\[\[SYSTEM_STATUS\]\]',
                r'\[\[NPC Motivations\]\]',
                r'\[\[Diplomacy Rules\]\]',
                r'\[\[Political Factions\]\]'
            ]
            
            for placeholder in meta_placeholders:
                if re.search(placeholder, content):
                    content = re.sub(placeholder, '', content)
                    fixed_in_file += len(re.findall(placeholder, original_content))
            
            # Remove step references
            step_pattern = r'\[\[step_\d+(?:\s*\([^)]+\))?\]\]'
            step_matches = re.findall(step_pattern, content)
            if step_matches:
                content = re.sub(step_pattern, '', content)
                fixed_in_file += len(step_matches)
            
            # Find and fix other broken links
            wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
            
            for link in wiki_links:
                # Remove alias if present
                link_target = link.split('|')[0].strip()
                
                # Skip ignored patterns
                if any(re.match(pattern, link_target) for pattern in self.ignore_patterns):
                    continue
                    
                # Remove section references
                base_link = link_target.split('#')[0].strip()
                
                if base_link:
                    # Check if link exists
                    fixed_link = self.find_best_match(base_link)
                    
                    if fixed_link and fixed_link != base_link:
                        # Replace the broken link
                        if '|' in link:
                            # Preserve alias
                            alias = link.split('|')[1]
                            old_pattern = f'[[{link}]]'
                            new_pattern = f'[[{fixed_link}|{alias}]]'
                        else:
                            old_pattern = f'[[{link}]]'
                            new_pattern = f'[[{fixed_link}]]'
                            
                        if old_pattern in content:
                            content = content.replace(old_pattern, new_pattern)
                            fixed_in_file += 1
                    elif not fixed_link and base_link not in self.file_index and base_link not in self.id_index:
                        unfixable_in_file += 1
            
            # Clean up multiple blank lines created by removals
            if fixed_in_file > 0:
                content = re.sub(r'\n{3,}', '\n\n', content)
                content = re.sub(r'  +', ' ', content)
                content = re.sub(r' \n', '\n', content)
                
                # Write back if changes were made
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            
        return fixed_in_file, unfixable_in_file
        
    def process_batch(self, files: List[Path], batch_num: int, total_batches: int):
        """Process a batch of files"""
        batch_fixed = 0
        batch_unfixable = 0
        
        for i, file_path in enumerate(files, 1):
            fixed, unfixable = self.process_file(file_path)
            batch_fixed += fixed
            batch_unfixable += unfixable
            
            with self.stats_lock:
                self.fixed_count += fixed
                self.unfixable_count += unfixable
                self.files_processed += 1
                
            if i % 10 == 0:
                print(f"  Batch {batch_num}/{total_batches}: Processed {i}/{len(files)} files...")
                
        return batch_fixed, batch_unfixable
        
    def fix_broken_links_parallel(self, max_workers: int = 4, batch_size: int = 100):
        """Fix broken links in parallel"""
        print("\n" + "=" * 50)
        print("PARALLEL BROKEN LINK REPAIR")
        print("=" * 50)
        
        # Get all markdown files
        all_files = []
        for root, dirs, files in os.walk(self.vault_path):
            # Skip system directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            if any(skip in root for skip in ['.git', '.obsidian', '08_Archive', '09_Performance', '_SCRIPTS']):
                continue
                
            for file in files:
                if file.endswith('.md'):
                    all_files.append(Path(root) / file)
                    
        print(f"Found {len(all_files)} markdown files to process")
        
        # Process in batches
        batches = [all_files[i:i+batch_size] for i in range(0, len(all_files), batch_size)]
        total_batches = len(batches)
        
        print(f"Processing in {total_batches} batches of up to {batch_size} files")
        print(f"Using {max_workers} parallel workers")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for batch_num, batch in enumerate(batches, 1):
                future = executor.submit(self.process_batch, batch, batch_num, total_batches)
                futures.append(future)
                
            for i, future in enumerate(as_completed(futures), 1):
                batch_fixed, batch_unfixable = future.result()
                print(f"Completed batch {i}/{total_batches}: Fixed {batch_fixed} links")
                
                # Show progress every 10 batches
                if i % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = self.files_processed / elapsed
                    remaining = (len(all_files) - self.files_processed) / rate
                    print(f"\n📊 Progress: {self.files_processed}/{len(all_files)} files")
                    print(f"   Fixed: {self.fixed_count} links")
                    print(f"   Rate: {rate:.1f} files/sec")
                    print(f"   ETA: {remaining:.0f} seconds\n")
                    
        elapsed = time.time() - start_time
        print(f"\n✅ Completed in {elapsed:.1f} seconds")
        print(f"   Processed: {self.files_processed} files")
        print(f"   Fixed: {self.fixed_count} links")
        print(f"   Unfixable: {self.unfixable_count} links")
        print(f"   Rate: {self.files_processed/elapsed:.1f} files/sec")
        
    def generate_report(self):
        """Generate a summary report"""
        report_path = self.vault_path / '_METADATA' / 'parallel_fix_report.json'
        
        report_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': {
                'files_processed': self.files_processed,
                'links_fixed': self.fixed_count,
                'links_unfixable': self.unfixable_count,
                'files_in_index': len(self.file_index),
                'files_with_ids': len(self.id_index)
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Report saved to: {report_path}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix broken links in parallel')
    parser.add_argument('--vault',
                       default="/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVaultExperimental",
                       help='Path to vault')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers')
    parser.add_argument('--batch-size', type=int, default=100,
                       help='Files per batch')
    
    args = parser.parse_args()
    
    fixer = ParallelLinkFixer(args.vault)
    
    # Build indexes
    fixer.build_file_index()
    
    # Fix links in parallel
    fixer.fix_broken_links_parallel(max_workers=args.workers, batch_size=args.batch_size)
    
    # Generate report
    fixer.generate_report()

if __name__ == "__main__":
    main()