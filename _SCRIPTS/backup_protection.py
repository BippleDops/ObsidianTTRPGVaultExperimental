#!/usr/bin/env python3
"""
Backup Protection and Link Cleanup System
- Remove all links to backup folders
- Zip backup directories to prevent future deduplication issues
- Ensure link integrity is maintained
"""

import os
import re
import zipfile
import shutil
import argparse
from datetime import datetime
from typing import List, Dict, Set
from common import ROOT_DIR, list_markdown_files, read_file, write_file, backup_file

class BackupProtectionSystem:
    def __init__(self, vault_path: str = None):
        self.vault_path = vault_path or ROOT_DIR
        self.backup_patterns = [
            r'backup',
            r'vault_backup',
            r'\.backup',
            r'_backup_'
        ]
        self.removed_links = []
        self.zipped_backups = []
        
    def find_backup_directories(self) -> List[str]:
        """Find all backup directories"""
        backup_dirs = []
        
        for root, dirs, files in os.walk(self.vault_path):
            for directory in dirs:
                dir_lower = directory.lower()
                if any(pattern in dir_lower for pattern in self.backup_patterns):
                    backup_path = os.path.join(root, directory)
                    # Skip if it's already a zip file directory
                    if not backup_path.endswith('.zip'):
                        backup_dirs.append(backup_path)
        
        return backup_dirs
    
    def remove_backup_links(self, dry_run: bool = True) -> Dict[str, List[str]]:
        """Remove all wikilinks that reference backup directories"""
        results = {
            'files_modified': [],
            'links_removed': [],
            'errors': []
        }
        
        markdown_files = list_markdown_files(self.vault_path)
        
        for file_path in markdown_files:
            # Skip backup directories themselves
            if any(pattern in file_path.lower() for pattern in self.backup_patterns):
                continue
                
            try:
                content = read_file(file_path)
                original_content = content
                
                # Find and remove backup links
                # Pattern: [[backup_folder/file.md]] or [[folder/backup_folder/file.md]]
                wikilink_pattern = r'\[\[([^\]]*(?:backup|vault_backup)[^\]]*)\]\]'
                matches = re.findall(wikilink_pattern, content, re.IGNORECASE)
                
                if matches:
                    for match in matches:
                        full_link = f'[[{match}]]'
                        results['links_removed'].append({
                            'file': file_path,
                            'link': full_link,
                            'target': match
                        })
                    
                    # Remove the links
                    content = re.sub(wikilink_pattern, '', content, flags=re.IGNORECASE)
                    
                    # Clean up extra whitespace
                    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
                    content = content.strip() + '\n'
                    
                    if content != original_content:
                        results['files_modified'].append(file_path)
                        
                        if not dry_run:
                            backup_file(file_path)
                            write_file(file_path, content)
                        
            except Exception as e:
                results['errors'].append(f"Error processing {file_path}: {e}")
        
        return results
    
    def zip_backup_directories(self, dry_run: bool = True) -> List[Dict[str, str]]:
        """Zip all backup directories to prevent future deduplication issues"""
        backup_dirs = self.find_backup_directories()
        zipped_backups = []
        
        for backup_dir in backup_dirs:
            try:
                # Create zip filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dir_name = os.path.basename(backup_dir)
                zip_name = f"{dir_name}_{timestamp}.zip"
                zip_path = os.path.join(os.path.dirname(backup_dir), zip_name)
                
                if not dry_run:
                    # Create zip file
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(backup_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, backup_dir)
                                zipf.write(file_path, arcname)
                    
                    # Remove original directory after successful zip
                    if os.path.exists(zip_path):
                        shutil.rmtree(backup_dir)
                        print(f"Zipped and removed: {backup_dir} -> {zip_path}")
                
                zipped_backups.append({
                    'original_dir': backup_dir,
                    'zip_file': zip_path,
                    'status': 'completed' if not dry_run else 'planned'
                })
                
            except Exception as e:
                zipped_backups.append({
                    'original_dir': backup_dir,
                    'zip_file': '',
                    'status': f'error: {e}'
                })
        
        return zipped_backups
    
    def validate_link_integrity(self) -> Dict[str, List[str]]:
        """Validate that all remaining wikilinks point to existing files"""
        results = {
            'valid_links': [],
            'broken_links': [],
            'backup_links_found': []
        }
        
        markdown_files = list_markdown_files(self.vault_path)
        
        for file_path in markdown_files:
            # Skip backup directories
            if any(pattern in file_path.lower() for pattern in self.backup_patterns):
                continue
                
            try:
                content = read_file(file_path)
                
                # Find all wikilinks
                wikilink_pattern = r'\[\[([^\]]+)\]\]'
                matches = re.findall(wikilink_pattern, content)
                
                for link_text in matches:
                    # Extract target (ignore display text after |)
                    target = link_text.split('|')[0].strip()
                    
                    # Check if it's a backup link (shouldn't exist after cleanup)
                    if any(pattern in target.lower() for pattern in self.backup_patterns):
                        results['backup_links_found'].append({
                            'file': file_path,
                            'link': f'[[{link_text}]]',
                            'target': target
                        })
                        continue
                    
                    # Try to find the target file
                    target_found = False
                    
                    # Direct path check
                    if target.endswith('.md'):
                        direct_path = os.path.join(self.vault_path, target)
                        if os.path.exists(direct_path):
                            target_found = True
                    
                    # Search by filename
                    if not target_found:
                        filename = os.path.basename(target)
                        if not filename.endswith('.md'):
                            filename += '.md'
                        
                        for md_file in markdown_files:
                            if os.path.basename(md_file) == filename:
                                target_found = True
                                break
                    
                    if target_found:
                        results['valid_links'].append({
                            'file': file_path,
                            'link': f'[[{link_text}]]',
                            'target': target
                        })
                    else:
                        results['broken_links'].append({
                            'file': file_path,
                            'link': f'[[{link_text}]]',
                            'target': target
                        })
                        
            except Exception as e:
                print(f"Error validating links in {file_path}: {e}")
        
        return results
    
    def create_link_integrity_report(self) -> str:
        """Create a comprehensive link integrity report"""
        integrity_results = self.validate_link_integrity()
        
        report = [
            "# Vault Link Integrity Report",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Summary",
            f"- Valid links: {len(integrity_results['valid_links'])}",
            f"- Broken links: {len(integrity_results['broken_links'])}",
            f"- Backup links found: {len(integrity_results['backup_links_found'])}",
            ""
        ]
        
        if integrity_results['backup_links_found']:
            report.extend([
                "## ⚠️  Backup Links Still Present",
                "These links reference backup directories and should be removed:",
                ""
            ])
            
            for item in integrity_results['backup_links_found']:
                report.append(f"- `{item['file']}`: {item['link']}")
            
            report.append("")
        
        if integrity_results['broken_links']:
            report.extend([
                "## 🔍 Broken Links Found",
                "These links point to non-existent files:",
                ""
            ])
            
            # Group by source file
            by_file = {}
            for item in integrity_results['broken_links']:
                file_path = item['file']
                if file_path not in by_file:
                    by_file[file_path] = []
                by_file[file_path].append(item)
            
            for file_path, links in by_file.items():
                report.append(f"### {os.path.relpath(file_path, self.vault_path)}")
                for link in links:
                    report.append(f"- {link['link']} → `{link['target']}`")
                report.append("")
        
        if not integrity_results['broken_links'] and not integrity_results['backup_links_found']:
            report.extend([
                "## ✅ All Links Valid",
                "No broken or backup links found. Vault integrity is good!",
                ""
            ])
        
        return '\n'.join(report)
    
    def full_protection_sequence(self, dry_run: bool = True) -> Dict[str, any]:
        """Run the complete backup protection sequence"""
        print("🔄 Starting backup protection sequence...")
        
        results = {
            'backup_dirs_found': [],
            'link_removal': {},
            'zip_operations': [],
            'integrity_check': {},
            'report_path': None
        }
        
        # Step 1: Find backup directories
        print("Step 1: Finding backup directories...")
        backup_dirs = self.find_backup_directories()
        results['backup_dirs_found'] = backup_dirs
        print(f"Found {len(backup_dirs)} backup directories")
        
        # Step 2: Remove backup links
        print("Step 2: Removing links to backup directories...")
        link_results = self.remove_backup_links(dry_run)
        results['link_removal'] = link_results
        print(f"Would {'remove' if dry_run else 'removed'} {len(link_results['links_removed'])} backup links from {len(link_results['files_modified'])} files")
        
        # Step 3: Zip backup directories
        print("Step 3: Zipping backup directories...")
        zip_results = self.zip_backup_directories(dry_run)
        results['zip_operations'] = zip_results
        print(f"Would {'zip' if dry_run else 'zipped'} {len([z for z in zip_results if z['status'] in ['completed', 'planned']])} directories")
        
        # Step 4: Validate link integrity
        print("Step 4: Validating link integrity...")
        integrity_results = self.validate_link_integrity()
        results['integrity_check'] = integrity_results
        
        # Step 5: Create report
        print("Step 5: Creating integrity report...")
        report_content = self.create_link_integrity_report()
        report_path = os.path.join(self.vault_path, "Link_Integrity_Report.md")
        
        if not dry_run:
            write_file(report_path, report_content)
        
        results['report_path'] = report_path
        
        print(f"✅ Backup protection sequence {'would be' if dry_run else 'is'} complete!")
        return results

def main():
    parser = argparse.ArgumentParser(description='Backup Protection System')
    parser.add_argument('action', choices=['analyze', 'protect', 'validate', 'report'])
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Show what would be done without making changes')
    parser.add_argument('--execute', action='store_true',
                       help='Actually perform the operations (overrides --dry-run)')
    
    args = parser.parse_args()
    
    # If --execute is specified, turn off dry_run
    dry_run = args.dry_run and not args.execute
    
    protection = BackupProtectionSystem()
    
    if args.action == 'analyze':
        backup_dirs = protection.find_backup_directories()
        print(f"Found {len(backup_dirs)} backup directories:")
        for backup_dir in backup_dirs:
            print(f"  - {backup_dir}")
    
    elif args.action == 'protect':
        results = protection.full_protection_sequence(dry_run)
        
        print("\n📊 Protection Results:")
        print(f"Backup directories: {len(results['backup_dirs_found'])}")
        print(f"Links removed: {len(results['link_removal']['links_removed'])}")
        print(f"Files modified: {len(results['link_removal']['files_modified'])}")
        print(f"Zip operations: {len(results['zip_operations'])}")
        print(f"Broken links found: {len(results['integrity_check']['broken_links'])}")
        
        if dry_run:
            print("\n⚠️  This was a dry run. Use --execute to perform actual changes.")
    
    elif args.action == 'validate':
        integrity_results = protection.validate_link_integrity()
        print(f"Valid links: {len(integrity_results['valid_links'])}")
        print(f"Broken links: {len(integrity_results['broken_links'])}")
        print(f"Backup links: {len(integrity_results['backup_links_found'])}")
        
        if integrity_results['backup_links_found']:
            print("\n⚠️  Backup links found:")
            for item in integrity_results['backup_links_found'][:5]:
                print(f"  {item['file']}: {item['link']}")
    
    elif args.action == 'report':
        report = protection.create_link_integrity_report()
        print(report)

if __name__ == "__main__":
    main()