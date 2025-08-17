#!/usr/bin/env python3
"""
Comprehensive script to fix ALL problematic links in the vault:
- vault_backup references
- vaultbackup references  
- Absolute path references
- References to backups, reports, scripts, data folders
"""

import re
import os
from pathlib import Path
from collections import defaultdict

class ComprehensiveLinkFixer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.fixes_made = defaultdict(int)
        self.files_fixed = []
        self.errors = []
        
        # Absolute path to remove
        self.absolute_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental/"
        
        # Define all patterns to fix
        self.patterns = []
        
        # 1. Vault backup folder patterns (with various spellings)
        vault_backup_patterns = [
            # Standard vault_backup patterns
            (r'\[\[vault_backup_\d{8}_\d{6}/', '[['),
            (r'!\[\[vault_backup_\d{8}_\d{6}/', '![['),
            (r'\[\[backups/vault_backup_\d{8}_\d{6}/', '[['),
            (r'!\[\[backups/vault_backup_\d{8}_\d{6}/', '![['),
            
            # Vaultbackup (no underscore) patterns
            (r'\[\[vaultbackup_\d{8}_\d{6}/', '[['),
            (r'!\[\[vaultbackup_\d{8}_\d{6}/', '![['),
            (r'\[\[backups/vaultbackup_\d{8}_\d{6}/', '[['),
            (r'!\[\[backups/vaultbackup_\d{8}_\d{6}/', '![['),
            
            # Mixed case variations
            (r'\[\[VaultBackup_\d{8}_\d{6}/', '[['),
            (r'\[\[Vault_Backup_\d{8}_\d{6}/', '[['),
            (r'\[\[vault-backup-\d{8}-\d{6}/', '[['),
        ]
        self.patterns.extend(vault_backup_patterns)
        
        # 2. Absolute path patterns
        absolute_patterns = [
            # Full absolute paths in links
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental/backups/([^\]]+)\]\]', r'[[\1]]'),
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental/reports/([^\]]+)\]\]', r'[[reports/\1]]'),
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental/scripts/([^\]]+)\]\]', r'[[scripts/\1]]'),
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental/data/([^\]]+)\]\]', r'[[data/\1]]'),
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental/([^\]]+)\]\]', r'[[\1]]'),
            
            # Embedded files with absolute paths
            (r'!\[\[/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental/backups/([^\]]+)\]\]', r'![[\1]]'),
            (r'!\[\[/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental/([^\]]+)\]\]', r'![[\1]]'),
            
            # Alternative path format (without ~)
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloudmdobsidian/Documents/ObsidianTTRPGVault Experimental/backups/([^\]]+)\]\]', r'[[\1]]'),
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloudmdobsidian/Documents/ObsidianTTRPGVault Experimental/reports/([^\]]+)\]\]', r'[[reports/\1]]'),
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloudmdobsidian/Documents/ObsidianTTRPGVault Experimental/scripts/([^\]]+)\]\]', r'[[scripts/\1]]'),
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloudmdobsidian/Documents/ObsidianTTRPGVault Experimental/data/([^\]]+)\]\]', r'[[data/\1]]'),
            (r'\[\[/Users/jongosussmango/Library/Mobile Documents/iCloudmdobsidian/Documents/ObsidianTTRPGVault Experimental/([^\]]+)\]\]', r'[[\1]]'),
        ]
        self.patterns.extend(absolute_patterns)
        
        # 3. Direct backup folder references to remove
        backup_folder_patterns = [
            # Remove references to backups folder in links
            (r'\[\[backups/([^\]]+)\]\]', r'[[\1]]'),
            (r'!\[\[backups/([^\]]+)\]\]', r'![[\1]]'),
            
            # Remove backup folder prefixes
            (r'backups/vault_backup_\d{8}_\d{6}/', ''),
            (r'backups/vaultbackup_\d{8}_\d{6}/', ''),
            (r'08_Archive/backups/vault_backup_\d{8}_\d{6}/', ''),
            
            # File naming and hierarchical backups
            (r'file_naming_backup_\d{8}_\d{6}/', ''),
            (r'hierarchical_tags_backup_\d{8}_\d{6}/', ''),
        ]
        self.patterns.extend(backup_folder_patterns)
        
        # 4. Clean up double slashes and path issues
        cleanup_patterns = [
            (r'//', '/'),  # Double slashes
            (r'\[\[/([^\]]+)\]\]', r'[[\1]]'),  # Remove leading slash in links
            (r'!\[\[/([^\]]+)\]\]', r'![[\1]]'),  # Remove leading slash in embeds
        ]
        self.patterns.extend(cleanup_patterns)
    
    def fix_file(self, file_path):
        """Fix all problematic links in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            fixes_in_file = 0
            
            # Apply all pattern fixes
            for pattern, replacement in self.patterns:
                try:
                    new_content, count = re.subn(pattern, replacement, content)
                    if count > 0:
                        fixes_in_file += count
                        self.fixes_made[pattern] += count
                        content = new_content
                except Exception as e:
                    self.errors.append(f"Pattern error in {file_path}: {pattern} - {e}")
            
            # Only write if changes were made
            if fixes_in_file > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.files_fixed.append(str(file_path))
                return fixes_in_file
            
            return 0
            
        except Exception as e:
            self.errors.append(f"Error processing {file_path}: {e}")
            return 0
    
    def scan_vault(self):
        """Scan entire vault for problematic links"""
        files_to_fix = []
        
        print("🔍 Scanning vault for problematic links...")
        print("  Looking for:")
        print("  - vault_backup and vaultbackup references")
        print("  - Absolute path references")
        print("  - Direct backups folder references")
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip actual backup folders
            if "backups" in str(md_file.parent) or "08_Archive/backups" in str(md_file):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if file contains any problematic patterns
                needs_fix = False
                
                # Check for vault backup references
                if re.search(r'vault.?backup', content, re.IGNORECASE):
                    needs_fix = True
                
                # Check for absolute paths
                if '/Users/jongosussmango' in content:
                    needs_fix = True
                
                # Check for backups folder references
                if re.search(r'\[\[backups/', content):
                    needs_fix = True
                
                if needs_fix:
                    files_to_fix.append(md_file)
                    
            except Exception as e:
                self.errors.append(f"Error scanning {md_file}: {e}")
        
        return files_to_fix
    
    def fix_all(self):
        """Fix all problematic links in the vault"""
        print("\n🔧 Comprehensive Link Fixer")
        print("=" * 60)
        
        # Find files needing fixes
        files_to_fix = self.scan_vault()
        
        if not files_to_fix:
            print("✅ No problematic links found!")
            return
        
        print(f"\nFound {len(files_to_fix)} files with problematic links")
        print("Fixing links...")
        print("-" * 60)
        
        total_fixes = 0
        for i, file_path in enumerate(files_to_fix, 1):
            fixes = self.fix_file(file_path)
            total_fixes += fixes
            
            if i % 100 == 0:
                print(f"  Processed {i}/{len(files_to_fix)} files...")
        
        print("-" * 60)
        print(f"✅ Fixed {total_fixes} problematic links in {len(self.files_fixed)} files")
        
        # Show fix statistics
        if self.fixes_made:
            print("\n📊 Fix Statistics:")
            
            # Group by type
            vault_backup_fixes = sum(count for pattern, count in self.fixes_made.items() 
                                    if 'vault' in pattern.lower() and 'backup' in pattern.lower())
            absolute_path_fixes = sum(count for pattern, count in self.fixes_made.items() 
                                     if '/Users/' in pattern)
            backup_folder_fixes = sum(count for pattern, count in self.fixes_made.items() 
                                    if 'backups/' in pattern and '/Users/' not in pattern)
            
            if vault_backup_fixes > 0:
                print(f"  - Vault backup references: {vault_backup_fixes}")
            if absolute_path_fixes > 0:
                print(f"  - Absolute path references: {absolute_path_fixes}")
            if backup_folder_fixes > 0:
                print(f"  - Backup folder references: {backup_folder_fixes}")
        
        # Show errors if any
        if self.errors:
            print(f"\n⚠️ {len(self.errors)} errors occurred")
            unique_errors = list(set(self.errors))[:5]
            for error in unique_errors:
                print(f"  - {error}")
        
        # Save report
        self.save_report(total_fixes)
    
    def save_report(self, total_fixes):
        """Save a detailed report"""
        report_path = self.vault_path / "reports" / "comprehensive_link_fixes_report.md"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Link Fixes Report\n\n")
            f.write(f"**Total Fixes**: {total_fixes}\n")
            f.write(f"**Files Fixed**: {len(self.files_fixed)}\n\n")
            
            f.write("## Types of Fixes\n\n")
            f.write("- Vault backup references (vault_backup, vaultbackup)\n")
            f.write("- Absolute path references (/Users/...)\n")
            f.write("- Direct backup folder references\n")
            f.write("- Path cleanup (double slashes, etc.)\n\n")
            
            if self.files_fixed:
                f.write("## Sample Files Fixed\n\n")
                for file_path in sorted(self.files_fixed)[:20]:
                    rel_path = Path(file_path).relative_to(self.vault_path)
                    f.write(f"- {rel_path}\n")
        
        print(f"\n📄 Report saved to: reports/comprehensive_link_fixes_report.md")

def verify_complete(vault_path):
    """Final verification that all problematic links are fixed"""
    vault_path = Path(vault_path)
    issues = []
    
    print("\n🔍 Final Verification...")
    
    for md_file in vault_path.rglob("*.md"):
        if "backups" in str(md_file.parent) or "08_Archive" in str(md_file):
            continue
            
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for remaining issues
            if re.search(r'\[\[vault.?backup.*\d{6}', content, re.IGNORECASE):
                issues.append(f"{md_file.name}: vault backup reference")
            
            if re.search(r'\[\[/Users/jongosussmango', content):
                issues.append(f"{md_file.name}: absolute path")
                
        except:
            pass
    
    if not issues:
        print("✅ All problematic links have been fixed!")
    else:
        print(f"⚠️ {len(issues)} potential issues remain:")
        for issue in issues[:5]:
            print(f"  - {issue}")
    
    return len(issues) == 0

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    print("🔄 Comprehensive Link Fixing")
    print("=" * 60)
    print("This will fix:")
    print("  ✓ vault_backup and vaultbackup references")
    print("  ✓ Absolute path references")
    print("  ✓ Direct backup folder references")
    print("  ✓ Path formatting issues")
    print("=" * 60)
    
    # Create fixer and run
    fixer = ComprehensiveLinkFixer(vault_path)
    fixer.fix_all()
    
    # Verify completion
    verify_complete(vault_path)
    
    print("\n✨ Comprehensive link fixing complete!")

if __name__ == "__main__":
    main()