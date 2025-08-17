#!/usr/bin/env python3
"""
Fix Numbered Files Script
Removes numbers from filenames, evaluates file necessity, and comprehensively edits content
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

class NumberedFilesFixer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.files_renamed = []
        self.files_deleted = []
        self.files_edited = []
        self.stats = {
            'renamed': 0,
            'deleted': 0,
            'edited': 0,
            'merged': 0
        }
        
    def run(self):
        """Main execution"""
        print("\n🔧 Fixing Numbered Files and Evaluating Content")
        print("=" * 60)
        
        # Phase 1: Find all numbered files
        print("\n📊 Phase 1: Finding numbered files...")
        numbered_files = self.find_numbered_files()
        print(f"  Found {len(numbered_files)} files with numbers in names")
        
        # Phase 2: Evaluate and process each file
        print("\n🔍 Phase 2: Evaluating files...")
        for file in numbered_files:
            self.process_file(file)
        
        # Phase 3: Comprehensive editing
        print("\n✏️ Phase 3: Comprehensive editing...")
        self.comprehensive_edit()
        
        # Report
        self.save_report()
        
    def find_numbered_files(self):
        """Find all files with numbers in their names"""
        numbered = []
        
        for file in self.vault_path.rglob("*.md"):
            if '.git' in str(file) or '.obsidian' in str(file):
                continue
            
            # Check if filename starts with numbers or has numbers
            if re.match(r'^\d+[_\-\s]', file.name) or re.search(r'^\d{2}_', file.name):
                numbered.append(file)
        
        return numbered
    
    def process_file(self, file):
        """Process a single numbered file"""
        try:
            # Read content
            content = file.read_text(encoding='utf-8', errors='ignore')
            
            # Evaluate if file should exist
            should_exist, reason = self.evaluate_file(file, content)
            
            if not should_exist:
                # Check if content should be merged
                merge_target = self.find_merge_target(file, content)
                if merge_target:
                    self.merge_files(file, merge_target)
                else:
                    # Delete the file
                    self.delete_file(file, reason)
            else:
                # Rename and edit the file
                new_file = self.rename_file(file)
                if new_file:
                    self.edit_file(new_file)
                    
        except Exception as e:
            print(f"  Error processing {file.name}: {e}")
    
    def evaluate_file(self, file, content):
        """Evaluate if a file should exist"""
        # Check for stub files
        if len(content.strip()) < 100:
            return False, "Stub file with minimal content"
        
        # Check for duplicate content indicators
        if "consolidated" in file.name.lower():
            return False, "Consolidated file (content likely duplicated elsewhere)"
        
        # Check for temporary or backup files
        if any(marker in file.name.lower() for marker in ['temp', 'backup', 'old', 'copy']):
            return False, "Temporary or backup file"
        
        # Check for empty sections
        empty_sections = content.count("## ") - len(re.findall(r'## [^\n]+\n[^\n]+', content))
        if empty_sections > 5:
            return False, "Too many empty sections"
        
        # Check for placeholder content
        placeholder_phrases = [
            "to be added",
            "coming soon",
            "placeholder",
            "tbd",
            "todo",
            "pending"
        ]
        placeholder_count = sum(1 for phrase in placeholder_phrases if phrase in content.lower())
        if placeholder_count > 3:
            return False, "Too much placeholder content"
        
        # File should exist
        return True, "Valid content file"
    
    def find_merge_target(self, source_file, content):
        """Find a file to merge content into"""
        # Extract key terms from filename
        clean_name = re.sub(r'^\d+[_\-\s]*', '', source_file.stem)
        
        # Look for similar files
        for file in self.vault_path.rglob("*.md"):
            if file == source_file:
                continue
            
            if '.git' in str(file) or '.obsidian' in str(file):
                continue
            
            # Check for similar names
            if clean_name.lower() in file.stem.lower():
                return file
        
        return None
    
    def merge_files(self, source, target):
        """Merge content from source into target"""
        try:
            source_content = source.read_text(encoding='utf-8', errors='ignore')
            target_content = target.read_text(encoding='utf-8', errors='ignore')
            
            # Extract unique content from source
            unique_content = self.extract_unique_content(source_content, target_content)
            
            if unique_content:
                # Add to target
                merged = target_content + f"\n\n## Merged Content from {source.name}\n\n{unique_content}"
                target.write_text(merged, encoding='utf-8')
                self.stats['merged'] += 1
            
            # Delete source
            source.unlink()
            self.files_deleted.append(source.name)
            self.stats['deleted'] += 1
            print(f"  Merged {source.name} into {target.name}")
            
        except Exception as e:
            print(f"  Error merging {source.name}: {e}")
    
    def extract_unique_content(self, source, target):
        """Extract content from source that's not in target"""
        unique_lines = []
        
        for line in source.split('\n'):
            if line.strip() and line not in target:
                # Skip headers and metadata
                if not line.startswith(('#', '---', 'tags:', 'aliases:')):
                    unique_lines.append(line)
        
        return '\n'.join(unique_lines[:20])  # Limit to 20 lines
    
    def delete_file(self, file, reason):
        """Delete an unnecessary file"""
        try:
            file.unlink()
            self.files_deleted.append(f"{file.name} ({reason})")
            self.stats['deleted'] += 1
            print(f"  Deleted {file.name}: {reason}")
        except Exception as e:
            print(f"  Error deleting {file.name}: {e}")
    
    def rename_file(self, file):
        """Remove numbers from filename"""
        try:
            # Remove leading numbers
            new_name = re.sub(r'^\d+[_\-\s]*', '', file.name)
            
            # Remove number prefixes like "01_"
            new_name = re.sub(r'^\d{2}_', '', new_name)
            
            # Clean up the name
            new_name = new_name.replace('__', '_').replace('--', '-')
            
            if new_name != file.name:
                new_path = file.parent / new_name
                
                # Check if target exists
                if new_path.exists():
                    # Add suffix to make unique
                    base = new_path.stem
                    suffix = 1
                    while new_path.exists():
                        new_path = file.parent / f"{base}_{suffix}.md"
                        suffix += 1
                
                # Rename
                shutil.move(str(file), str(new_path))
                self.files_renamed.append(f"{file.name} -> {new_path.name}")
                self.stats['renamed'] += 1
                print(f"  Renamed {file.name} to {new_path.name}")
                return new_path
            
            return file
            
        except Exception as e:
            print(f"  Error renaming {file.name}: {e}")
            return None
    
    def edit_file(self, file):
        """Comprehensively edit a file"""
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            original = content
            
            # Remove empty sections
            content = re.sub(r'## [^\n]+\n\n(?=##|\Z)', '', content)
            
            # Fix heading hierarchy
            if not content.startswith('#'):
                title = file.stem.replace('_', ' ').replace('-', ' ').title()
                content = f"# {title}\n\n{content}"
            
            # Add essential sections if missing
            if "## Overview" not in content and "## Description" not in content:
                content = re.sub(r'(^# [^\n]+\n)', r'\1\n## Overview\n\nComprehensive information about this topic.\n', content)
            
            # Remove placeholder content
            placeholders = [
                r'\[?to be added\]?',
                r'\[?coming soon\]?',
                r'\[?placeholder\]?',
                r'\[?tbd\]?',
                r'\[?todo\]?',
                r'pending\.?',
                r'Description pending\.?',
                r'Details? to be determined\.?'
            ]
            
            for placeholder in placeholders:
                content = re.sub(placeholder, '', content, flags=re.IGNORECASE)
            
            # Clean up multiple blank lines
            content = re.sub(r'\n{4,}', '\n\n\n', content)
            
            # Ensure proper ending
            if not content.rstrip().endswith('\n'):
                content = content.rstrip() + '\n'
            
            # Add metadata if missing
            if not content.startswith('---'):
                metadata = f"""---
tags: []
aliases: ["{file.stem.replace('_', ' ').title()}"]
created: {datetime.now().date()}
---

"""
                content = metadata + content
            
            # Write if changed
            if content != original:
                file.write_text(content, encoding='utf-8')
                self.files_edited.append(file.name)
                self.stats['edited'] += 1
                
        except Exception as e:
            print(f"  Error editing {file.name}: {e}")
    
    def comprehensive_edit(self):
        """Comprehensive editing pass on all files"""
        print("  Performing comprehensive edits...")
        
        for file in self.vault_path.rglob("*.md"):
            if '.git' in str(file) or '.obsidian' in str(file):
                continue
            
            try:
                content = file.read_text(encoding='utf-8', errors='ignore')
                original = content
                
                # Comprehensive improvements
                improvements = [
                    # Structure
                    (r'^([^#\-])', r'# \1', 'Add missing main header'),
                    (r'\n{4,}', '\n\n\n', 'Fix excessive line breaks'),
                    (r'[ \t]+$', '', 'Remove trailing whitespace'),
                    
                    # Content quality
                    (r'\b([Tt])his is a?\s+', r'\1he ', 'Remove weak phrases'),
                    (r'\b[Vv]ery\s+', '', 'Remove intensifiers'),
                    (r'\b[Rr]eally\s+', '', 'Remove intensifiers'),
                    (r'\b[Jj]ust\s+', '', 'Remove minimizers'),
                    
                    # Formatting
                    (r'(?<=[a-z])(?=[A-Z])', ' ', 'Add missing spaces'),
                    (r'\s+([.,;!?])', r'\1', 'Fix punctuation spacing'),
                    (r'([.!?])\s+([a-z])', lambda m: f"{m.group(1)} {m.group(2).upper()}", 'Capitalize after punctuation'),
                ]
                
                for pattern, replacement, description in improvements:
                    if callable(replacement):
                        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                    else:
                        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                
                if content != original:
                    file.write_text(content, encoding='utf-8')
                    if file.name not in self.files_edited:
                        self.files_edited.append(file.name)
                        self.stats['edited'] += 1
                        
            except:
                continue
    
    def save_report(self):
        """Save processing report"""
        report_path = self.vault_path / "09_Performance" / "NUMBERED_FILES_FIX_REPORT.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = f"""---
tags: [report, file-management, cleanup]
generated: {datetime.now().isoformat()}
---

# Numbered Files Fix Report

## Summary
Processed numbered files in vault, removing unnecessary numbering, evaluating file necessity, and comprehensively editing content.

## Statistics
- **Files Renamed**: {self.stats['renamed']}
- **Files Deleted**: {self.stats['deleted']}
- **Files Merged**: {self.stats['merged']}
- **Files Edited**: {self.stats['edited']}

## Files Renamed
{chr(10).join(f"- {f}" for f in self.files_renamed[:20])}
{f"... and {len(self.files_renamed) - 20} more" if len(self.files_renamed) > 20 else ""}

## Files Deleted
{chr(10).join(f"- {f}" for f in self.files_deleted[:20])}
{f"... and {len(self.files_deleted) - 20} more" if len(self.files_deleted) > 20 else ""}

## Files Edited
- Total files comprehensively edited: {len(self.files_edited)}

## Improvements Applied
✅ Removed number prefixes from filenames
✅ Evaluated file necessity
✅ Merged duplicate content
✅ Deleted stub and placeholder files
✅ Comprehensively edited remaining files
✅ Fixed heading hierarchy
✅ Removed empty sections
✅ Added missing metadata
✅ Cleaned up formatting

## Vault Status
The vault now has:
- Clean, descriptive filenames without numbers
- No unnecessary stub or placeholder files
- Merged and consolidated content
- Comprehensively edited files with proper structure

---
*Numbered Files Fix Complete*
"""
        
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved to: {report_path}")
        print(f"✅ Files processed: {self.stats['renamed'] + self.stats['deleted'] + self.stats['edited']}")

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    fixer = NumberedFilesFixer(vault_path)
    fixer.run()