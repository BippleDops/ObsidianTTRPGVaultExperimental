#!/usr/bin/env python3
"""
Fix truncated filenames and update references
"""

import os
import re
import shutil
from pathlib import Path

class TruncatedFileFixer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.truncation_patterns = {
            'Guil': 'Guild',
            'Orde': 'Order', 
            'Cente': 'Center',
            'Academ': 'Academy',
            'Authorit': 'Authority',
            'Syste': 'System',
            'Structur': 'Structure',
            'Inde': 'Index',
            'Cul': 'Cult',
            'Intelligenc': 'Intelligence',
            'Societie': 'Society',
            'Committe': 'Committee',
            'Covenan': 'Covenant',
            'Movemen': 'Movement',
            'Compan': 'Company',
            'Exchang': 'Exchange',
            'Ministrie': 'Ministry',
            'Authoritie': 'Authority'
        }
        
        self.file_pairs = []
        self.broken_references = []
        
    def find_truncated_files(self):
        """Find truncated files and their full counterparts"""
        truncated_files = []
        
        # Find files with truncated endings
        for pattern in self.truncation_patterns.keys():
            pattern_files = list(self.vault_path.rglob(f"*{pattern}.md"))
            truncated_files.extend(pattern_files)
        
        for truncated_file in truncated_files:
            # Generate what the full filename should be
            truncated_name = truncated_file.name
            for pattern, replacement in self.truncation_patterns.items():
                if truncated_name.endswith(f"{pattern}.md"):
                    full_name = truncated_name.replace(f"{pattern}.md", f"{replacement}.md")
                    full_path = truncated_file.parent / full_name
                    
                    if full_path.exists():
                        self.file_pairs.append({
                            'truncated': truncated_file,
                            'full': full_path,
                            'pattern': pattern,
                            'replacement': replacement
                        })
                        print(f"Found pair: {truncated_file} -> {full_path}")
                    break
    
    def find_references_to_fix(self):
        """Find references to truncated filenames in other files"""
        for pair in self.file_pairs:
            truncated_name = pair['truncated'].stem
            full_name = pair['full'].stem
            
            # Search for references to the truncated name
            for md_file in self.vault_path.rglob("*.md"):
                if md_file == pair['truncated'] or md_file == pair['full']:
                    continue
                
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Look for WikiLinks to truncated name
                    if f"[[{truncated_name}]]" in content or f"[[{truncated_name}|" in content:
                        self.broken_references.append({
                            'file': md_file,
                            'old_ref': truncated_name,
                            'new_ref': full_name,
                            'content': content
                        })
                        
                except Exception as e:
                    print(f"Error reading {md_file}: {e}")
    
    def fix_references(self):
        """Update references from truncated to full names"""
        for ref in self.broken_references:
            try:
                content = ref['content']
                old_ref = ref['old_ref']
                new_ref = ref['new_ref']
                
                # Replace WikiLinks
                content = re.sub(
                    rf'\[\[{re.escape(old_ref)}\]\]',
                    f'[[{new_ref}]]',
                    content
                )
                content = re.sub(
                    rf'\[\[{re.escape(old_ref)}\|([^\]]+)\]\]',
                    rf'[[{new_ref}|\1]]',
                    content
                )
                
                # Write updated content
                with open(ref['file'], 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Updated references in {ref['file']}")
                
            except Exception as e:
                print(f"Error updating {ref['file']}: {e}")
    
    def remove_truncated_files(self):
        """Remove truncated files after fixing references"""
        for pair in self.file_pairs:
            try:
                # Move truncated file to backup before deletion
                backup_path = self.vault_path / "08_Archive" / f"truncated_{pair['truncated'].name}"
                shutil.move(str(pair['truncated']), str(backup_path))
                print(f"Moved {pair['truncated']} to {backup_path}")
                
            except Exception as e:
                print(f"Error removing {pair['truncated']}: {e}")
    
    def run_fix(self):
        """Run the complete fix process"""
        print("Finding truncated files...")
        self.find_truncated_files()
        
        print(f"\nFound {len(self.file_pairs)} truncated file pairs")
        
        print("\nFinding references to fix...")
        self.find_references_to_fix()
        
        print(f"Found {len(self.broken_references)} files with broken references")
        
        print("\nFixing references...")
        self.fix_references()
        
        print("\nRemoving truncated files...")
        self.remove_truncated_files()
        
        print("\nTruncated file fix complete!")
        
        return {
            'pairs_fixed': len(self.file_pairs),
            'references_updated': len(self.broken_references)
        }

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    fixer = TruncatedFileFixer(vault_path)
    results = fixer.run_fix()
    
    print(f"\nSUMMARY:")
    print(f"File pairs fixed: {results['pairs_fixed']}")
    print(f"Reference files updated: {results['references_updated']}")

if __name__ == "__main__":
    main()