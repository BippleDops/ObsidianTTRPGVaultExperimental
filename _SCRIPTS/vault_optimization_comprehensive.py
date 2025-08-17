#!/usr/bin/env python3
"""
Comprehensive Vault Optimization System
Handles deleted file recovery, link validation, and content organization
"""

import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
from pydantic import BaseModel, Field
import hashlib


class VaultConfig(BaseModel):
    """Configuration for vault optimization"""
    vault_path: Path = Field(default=Path("."))
    dry_run: bool = Field(default=True)
    verbose: bool = Field(default=True)
    
    # Directory structure
    adventures_dir: str = "01_Adventures"
    worldbuilding_dir: str = "02_Worldbuilding"
    mechanics_dir: str = "03_Mechanics"
    resources_dir: str = "04_Resources"
    player_dir: str = "05_Player_Resources"
    session_dir: str = "06_Session_Management"
    archive_dir: str = "08_Archive"
    docs_dir: str = "09_Documentation"
    
    # Optimization settings
    fix_broken_links: bool = Field(default=True)
    standardize_wikilinks: bool = Field(default=True)
    remove_duplicates: bool = Field(default=True)
    organize_unlinked: bool = Field(default=True)
    validate_frontmatter: bool = Field(default=True)
    check_deleted_files: bool = Field(default=True)


class DeletedFileRecovery:
    """Handles recovery of deleted files from git history"""
    
    def __init__(self, config: VaultConfig):
        self.config = config
        self.deleted_files: List[str] = []
        self.recoverable_files: Dict[str, str] = {}
        
    def find_deleted_files(self) -> List[str]:
        """Find all deleted files in git status"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.config.vault_path
            )
            
            for line in result.stdout.split("\n"):
                if line.startswith(" D ") or line.startswith("D  "):
                    file_path = line[3:].strip().strip('"')
                    if file_path.endswith(".md"):
                        self.deleted_files.append(file_path)
                        
            return self.deleted_files
        except Exception as e:
            print(f"Error finding deleted files: {e}")
            return []
            
    def analyze_deleted_content(self) -> Dict[str, Any]:
        """Analyze deleted files to understand what was removed"""
        analysis = {
            "total_deleted": len(self.deleted_files),
            "by_category": defaultdict(list),
            "critical_files": [],
            "index_files": [],
            "campaign_content": []
        }
        
        for file_path in self.deleted_files:
            # Categorize by directory
            parts = Path(file_path).parts
            if parts:
                category = parts[0]
                analysis["by_category"][category].append(file_path)
                
            # Identify critical files
            filename = Path(file_path).name
            if "index" in filename.lower() or "hub" in filename.lower():
                analysis["index_files"].append(file_path)
            elif "overview" in filename.lower() or "guide" in filename.lower():
                analysis["critical_files"].append(file_path)
            elif any(campaign in file_path.lower() for campaign in ["seven_shards", "shadow_conspiracy", "crystal_plague"]):
                analysis["campaign_content"].append(file_path)
                
        return analysis
        
    def recover_critical_files(self, file_list: List[str] = None) -> Dict[str, bool]:
        """Recover specific deleted files from git"""
        if file_list is None:
            # Default to recovering index and critical files
            analysis = self.analyze_deleted_content()
            file_list = analysis["index_files"] + analysis["critical_files"]
            
        recovery_status = {}
        
        for file_path in file_list:
            try:
                if not self.config.dry_run:
                    subprocess.run(
                        ["git", "checkout", "HEAD~1", "--", file_path],
                        check=True,
                        cwd=self.config.vault_path
                    )
                    recovery_status[file_path] = True
                    print(f"✅ Recovered: {file_path}")
                else:
                    print(f"[DRY RUN] Would recover: {file_path}")
                    recovery_status[file_path] = True
            except subprocess.CalledProcessError:
                recovery_status[file_path] = False
                print(f"❌ Failed to recover: {file_path}")
                
        return recovery_status


class LinkValidator:
    """Validates and fixes broken links in the vault"""
    
    def __init__(self, config: VaultConfig):
        self.config = config
        self.all_files: Set[Path] = set()
        self.broken_links: Dict[Path, List[str]] = defaultdict(list)
        self.link_mapping: Dict[str, Path] = {}
        
    def scan_vault_files(self) -> None:
        """Build index of all markdown files"""
        for md_file in self.config.vault_path.glob("**/*.md"):
            if not any(part.startswith('.') for part in md_file.parts):
                self.all_files.add(md_file)
                # Create mapping for link resolution
                name_without_ext = md_file.stem
                self.link_mapping[name_without_ext] = md_file
                
    def extract_links(self, content: str) -> List[str]:
        """Extract all wikilinks from content"""
        # Match [[Link]] and [[Link|Alias]]
        pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        matches = re.findall(pattern, content)
        return matches
        
    def validate_links(self) -> Dict[Path, List[str]]:
        """Check all links in all files"""
        for md_file in self.all_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                links = self.extract_links(content)
                
                for link in links:
                    # Remove any anchors
                    link_base = link.split('#')[0].strip()
                    
                    # Check if target exists
                    if link_base and link_base not in self.link_mapping:
                        self.broken_links[md_file].append(link)
                        
            except Exception as e:
                print(f"Error reading {md_file}: {e}")
                
        return self.broken_links
        
    def fix_broken_links(self) -> Dict[Path, int]:
        """Attempt to fix broken links by finding similar files"""
        fixes_applied = {}
        
        for file_path, broken_links in self.broken_links.items():
            if not broken_links:
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                fixes_count = 0
                
                for broken_link in broken_links:
                    # Try to find a close match
                    best_match = self.find_best_match(broken_link)
                    
                    if best_match:
                        # Replace the broken link
                        old_pattern = f"[[{broken_link}]]"
                        new_pattern = f"[[{best_match.stem}]]"
                        
                        if old_pattern in content:
                            content = content.replace(old_pattern, new_pattern)
                            fixes_count += 1
                            print(f"  Fixed: {broken_link} -> {best_match.stem}")
                            
                if fixes_count > 0 and not self.config.dry_run:
                    file_path.write_text(content, encoding='utf-8')
                    fixes_applied[file_path] = fixes_count
                elif fixes_count > 0:
                    print(f"[DRY RUN] Would fix {fixes_count} links in {file_path}")
                    fixes_applied[file_path] = fixes_count
                    
            except Exception as e:
                print(f"Error fixing links in {file_path}: {e}")
                
        return fixes_applied
        
    def find_best_match(self, broken_link: str) -> Optional[Path]:
        """Find the best matching file for a broken link"""
        broken_parts = broken_link.lower().replace('_', ' ').replace('-', ' ').split()
        
        best_match = None
        best_score = 0
        
        for file_name, file_path in self.link_mapping.items():
            file_parts = file_name.lower().replace('_', ' ').replace('-', ' ').split()
            
            # Calculate similarity score
            common_parts = set(broken_parts) & set(file_parts)
            if common_parts:
                score = len(common_parts) / max(len(broken_parts), len(file_parts))
                
                if score > best_score and score > 0.5:  # Threshold for match
                    best_score = score
                    best_match = file_path
                    
        return best_match


class ContentOrganizer:
    """Organizes and standardizes vault content"""
    
    def __init__(self, config: VaultConfig):
        self.config = config
        self.unlinked_files: Set[Path] = set()
        self.duplicate_files: Dict[str, List[Path]] = defaultdict(list)
        
    def find_duplicates(self) -> Dict[str, List[Path]]:
        """Find duplicate files based on content similarity (99%+ match required)"""
        all_files = []
        duplicate_groups = defaultdict(list)
        
        # First pass: collect all files with their content
        for md_file in self.config.vault_path.glob("**/*.md"):
            if any(part.startswith('.') for part in md_file.parts):
                continue
            if 'backup' in str(md_file).lower() or 'archive' in str(md_file).lower():
                continue  # Skip backup/archive directories
                
            try:
                content = md_file.read_text(encoding='utf-8')
                # Skip empty or very small files
                if len(content.strip()) < 50:
                    continue
                all_files.append((md_file, content))
            except Exception as e:
                print(f"Error reading {md_file}: {e}")
        
        # Second pass: find near-duplicates (99%+ similarity)
        processed = set()
        for i, (file1, content1) in enumerate(all_files):
            if file1 in processed:
                continue
                
            similar_files = [file1]
            
            for j, (file2, content2) in enumerate(all_files[i+1:], i+1):
                if file2 in processed:
                    continue
                    
                # Check similarity
                similarity = self.calculate_similarity(content1, content2)
                if similarity >= 0.99:  # 99% threshold
                    similar_files.append(file2)
                    processed.add(file2)
                    
            if len(similar_files) > 1:
                # Use content hash as key for the group
                content_hash = hashlib.md5(content1.encode()).hexdigest()
                duplicate_groups[content_hash] = similar_files
                
        self.duplicate_files = duplicate_groups
        return self.duplicate_files
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity ratio between two texts"""
        # Normalize whitespace for comparison
        norm1 = re.sub(r'\s+', ' ', text1).strip()
        norm2 = re.sub(r'\s+', ' ', text2).strip()
        
        # Quick check: if lengths are very different, not duplicates
        if abs(len(norm1) - len(norm2)) > len(norm1) * 0.1:  # >10% length difference
            return 0.0
            
        # Character-level similarity
        matches = sum(1 for a, b in zip(norm1, norm2) if a == b)
        max_len = max(len(norm1), len(norm2))
        
        if max_len == 0:
            return 0.0
            
        return matches / max_len
        
    def remove_duplicates(self) -> int:
        """Remove duplicate files, keeping the one in the best location"""
        removed_count = 0
        
        for content_hash, file_list in self.duplicate_files.items():
            if len(file_list) <= 1:
                continue
                
            # Sort by priority (prefer organized directories)
            priority_dirs = [
                self.config.adventures_dir,
                self.config.worldbuilding_dir,
                self.config.mechanics_dir
            ]
            
            def get_priority(path: Path) -> int:
                for i, priority_dir in enumerate(priority_dirs):
                    if priority_dir in str(path):
                        return i
                return len(priority_dirs)
                
            sorted_files = sorted(file_list, key=get_priority)
            keep_file = sorted_files[0]
            
            for duplicate_file in sorted_files[1:]:
                if not self.config.dry_run:
                    duplicate_file.unlink()
                    removed_count += 1
                    print(f"  Removed duplicate: {duplicate_file}")
                else:
                    print(f"[DRY RUN] Would remove duplicate: {duplicate_file}")
                    removed_count += 1
                    
        return removed_count
        
    def find_unlinked_files(self) -> Set[Path]:
        """Find files that aren't linked from anywhere"""
        all_files = set(self.config.vault_path.glob("**/*.md"))
        linked_files = set()
        
        # Build set of all linked files
        for md_file in all_files:
            if any(part.startswith('.') for part in md_file.parts):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                
                for link in links:
                    link_base = link.split('#')[0].strip()
                    # Find matching file
                    for potential_match in all_files:
                        if potential_match.stem == link_base:
                            linked_files.add(potential_match)
                            break
                            
            except Exception as e:
                print(f"Error scanning {md_file}: {e}")
                
        self.unlinked_files = all_files - linked_files
        return self.unlinked_files
        
    def organize_unlinked_files(self) -> int:
        """Move unlinked files to appropriate directories"""
        organized_count = 0
        
        for unlinked_file in self.unlinked_files:
            # Skip system files and already organized files
            if any(part.startswith('.') for part in unlinked_file.parts):
                continue
            if self.config.archive_dir in str(unlinked_file):
                continue
                
            # Determine target directory based on content
            target_dir = self.determine_target_directory(unlinked_file)
            
            if target_dir and target_dir != unlinked_file.parent:
                target_path = self.config.vault_path / target_dir / unlinked_file.name
                
                if not self.config.dry_run:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(unlinked_file), str(target_path))
                    organized_count += 1
                    print(f"  Moved: {unlinked_file.name} -> {target_dir}")
                else:
                    print(f"[DRY RUN] Would move: {unlinked_file.name} -> {target_dir}")
                    organized_count += 1
                    
        return organized_count
        
    def determine_target_directory(self, file_path: Path) -> Optional[str]:
        """Determine the best directory for a file based on its content"""
        try:
            content = file_path.read_text(encoding='utf-8').lower()
            filename = file_path.stem.lower()
            
            # Check for campaign content
            if any(term in content or term in filename for term in ["session", "adventure", "campaign", "quest"]):
                return self.config.adventures_dir
                
            # Check for worldbuilding
            if any(term in content or term in filename for term in ["lore", "history", "location", "npc", "faction"]):
                return f"{self.config.worldbuilding_dir}/Lore"
                
            # Check for mechanics
            if any(term in content or term in filename for term in ["rule", "mechanic", "stat", "ability", "spell"]):
                return self.config.mechanics_dir
                
            # Default to archive for unclear content
            return f"{self.config.archive_dir}/Unsorted"
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None


class VaultOptimizer:
    """Main optimization orchestrator"""
    
    def __init__(self, config: VaultConfig):
        self.config = config
        self.recovery = DeletedFileRecovery(config)
        self.validator = LinkValidator(config)
        self.organizer = ContentOrganizer(config)
        self.report = {}
        
    def run_full_optimization(self) -> Dict[str, Any]:
        """Run complete vault optimization"""
        print("🚀 Starting Comprehensive Vault Optimization")
        print(f"   Mode: {'DRY RUN' if self.config.dry_run else 'LIVE'}")
        print("="*60)
        
        # Step 1: Analyze deleted files
        if self.config.check_deleted_files:
            print("\n📋 Step 1: Analyzing Deleted Files")
            deleted_files = self.recovery.find_deleted_files()
            deletion_analysis = self.recovery.analyze_deleted_content()
            
            print(f"  Found {len(deleted_files)} deleted files")
            print(f"  Critical files: {len(deletion_analysis['critical_files'])}")
            print(f"  Index files: {len(deletion_analysis['index_files'])}")
            
            if deletion_analysis['critical_files'] or deletion_analysis['index_files']:
                print("\n  🔄 Recovering critical files...")
                recovery_status = self.recovery.recover_critical_files()
                self.report['recovered_files'] = recovery_status
                
        # Step 2: Scan vault structure
        print("\n📊 Step 2: Scanning Vault Structure")
        self.validator.scan_vault_files()
        print(f"  Found {len(self.validator.all_files)} markdown files")
        
        # Step 3: Validate links
        if self.config.fix_broken_links:
            print("\n🔗 Step 3: Validating Links")
            broken_links = self.validator.validate_links()
            total_broken = sum(len(links) for links in broken_links.values())
            print(f"  Found {total_broken} broken links in {len(broken_links)} files")
            
            if broken_links:
                print("  🔧 Attempting to fix broken links...")
                fixes = self.validator.fix_broken_links()
                self.report['fixed_links'] = fixes
                
        # Step 4: Find and remove duplicates
        if self.config.remove_duplicates:
            print("\n🔍 Step 4: Finding Duplicates")
            duplicates = self.organizer.find_duplicates()
            total_duplicates = sum(len(v) - 1 for v in duplicates.values())
            print(f"  Found {total_duplicates} duplicate files")
            
            if duplicates:
                print("  🗑️ Removing duplicates...")
                removed = self.organizer.remove_duplicates()
                self.report['removed_duplicates'] = removed
                
        # Step 5: Organize unlinked files
        if self.config.organize_unlinked:
            print("\n📁 Step 5: Organizing Unlinked Files")
            unlinked = self.organizer.find_unlinked_files()
            print(f"  Found {len(unlinked)} unlinked files")
            
            if unlinked:
                print("  📂 Organizing unlinked files...")
                organized = self.organizer.organize_unlinked_files()
                self.report['organized_files'] = organized
                
        # Generate report
        self.generate_report()
        
        return self.report
        
    def generate_report(self) -> None:
        """Generate optimization report"""
        print("\n" + "="*60)
        print("📊 OPTIMIZATION REPORT")
        print("="*60)
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "mode": "DRY RUN" if self.config.dry_run else "LIVE",
            "results": self.report
        }
        
        # Save report
        report_path = self.config.vault_path / "reports" / f"optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        print(f"\n📄 Report saved to: {report_path}")
        
        # Print summary
        if 'recovered_files' in self.report:
            recovered = sum(1 for v in self.report['recovered_files'].values() if v)
            print(f"✅ Recovered {recovered} critical files")
            
        if 'fixed_links' in self.report:
            fixed = sum(self.report['fixed_links'].values())
            print(f"✅ Fixed {fixed} broken links")
            
        if 'removed_duplicates' in self.report:
            print(f"✅ Removed {self.report['removed_duplicates']} duplicate files")
            
        if 'organized_files' in self.report:
            print(f"✅ Organized {self.report['organized_files']} unlinked files")
            
        print("\n🎯 Optimization complete!")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive Vault Optimization")
    parser.add_argument("--live", action="store_true", help="Run in live mode (applies changes)")
    parser.add_argument("--no-recovery", action="store_true", help="Skip deleted file recovery")
    parser.add_argument("--no-links", action="store_true", help="Skip link validation")
    parser.add_argument("--no-duplicates", action="store_true", help="Skip duplicate removal")
    parser.add_argument("--no-organize", action="store_true", help="Skip file organization")
    
    args = parser.parse_args()
    
    config = VaultConfig(
        dry_run=not args.live,
        check_deleted_files=not args.no_recovery,
        fix_broken_links=not args.no_links,
        remove_duplicates=not args.no_duplicates,
        organize_unlinked=not args.no_organize
    )
    
    optimizer = VaultOptimizer(config)
    optimizer.run_full_optimization()


if __name__ == "__main__":
    main()