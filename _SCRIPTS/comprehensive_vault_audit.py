#!/usr/bin/env python3
"""
Comprehensive vault audit - goes through every file systematically
"""

import os
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import json
from datetime import datetime
from collections import defaultdict


class VaultAuditor:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.audit_results = {
            "directories": {},
            "duplicates": [],
            "broken_links": [],
            "dnd_content": {},
            "issues": [],
            "recommendations": []
        }
        
    def audit_directory_structure(self):
        """Audit the complete directory structure"""
        print("📁 Auditing Directory Structure...")
        
        # Expected structure
        expected = {
            "00_Indexes": "Navigation and indexes",
            "01_Adventures": "Campaigns and sessions",
            "02_Worldbuilding": "Lore, NPCs, locations",
            "03_Mechanics": "Rules and systems",
            "04_Resources": "Assets and handouts",
            "05_Player_Resources": "Player tools",
            "06_GM_Resources": "GM tools",
            "07_Templates": "Note templates",
            "08_Archive": "Backups and old content",
            "09_Documentation": "Guides and docs",
            "10_Homebrew": "Custom content",
            "11_Media": "Images and media",
            "12_Research": "D&D sourcebooks",
            "13_Performance": "System monitoring"
        }
        
        # Check what actually exists
        for num in range(14):
            pattern = f"{num:02d}_*"
            matching_dirs = list(self.vault_path.glob(pattern))
            
            if len(matching_dirs) > 1:
                self.audit_results["issues"].append(f"DUPLICATE: Multiple {num:02d}_ directories: {[d.name for d in matching_dirs]}")
                
            for dir_path in matching_dirs:
                # Count contents
                md_files = list(dir_path.rglob("*.md"))
                img_files = list(dir_path.rglob("*.png")) + list(dir_path.rglob("*.jpg"))
                
                self.audit_results["directories"][dir_path.name] = {
                    "markdown_files": len(md_files),
                    "image_files": len(img_files),
                    "total_size_mb": sum(f.stat().st_size for f in dir_path.rglob("*") if f.is_file()) / (1024*1024),
                    "expected_purpose": expected.get(dir_path.name.split('_')[0] + '_' + dir_path.name.split('_')[1] if '_' in dir_path.name else "Unknown"),
                    "subdirectories": [d.name for d in dir_path.iterdir() if d.is_dir()][:10]  # First 10 subdirs
                }
                
    def find_all_duplicates(self):
        """Find ALL duplicate content in the vault"""
        print("🔍 Finding Duplicate Content...")
        
        file_hashes = defaultdict(list)
        
        # Hash all markdown files
        for md_file in self.vault_path.glob("**/*.md"):
            if any(part.startswith('.') for part in md_file.parts):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                # Normalize whitespace for comparison
                normalized = ' '.join(content.split())
                content_hash = hashlib.md5(normalized.encode()).hexdigest()
                file_hashes[content_hash].append(md_file)
            except:
                pass
                
        # Identify duplicates
        for content_hash, file_list in file_hashes.items():
            if len(file_list) > 1:
                self.audit_results["duplicates"].append({
                    "files": [str(f.relative_to(self.vault_path)) for f in file_list],
                    "count": len(file_list),
                    "size": file_list[0].stat().st_size
                })
                
    def audit_dnd_content(self):
        """Audit D&D 5e content organization"""
        print("🎲 Auditing D&D 5e Content...")
        
        dnd_locations = {
            "sourcebooks": [],
            "cli_reference": [],
            "statblocks": [],
            "tables": [],
            "misplaced": []
        }
        
        # Check primary location
        research_dir = self.vault_path / "12_Research"
        if research_dir.exists():
            sourcebooks = research_dir / "D&D_Sourcebooks"
            if sourcebooks.exists():
                # Count sourcebooks
                for item in sourcebooks.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        dnd_locations["sourcebooks"].append(item.name)
                        
                # Check CLI Reference
                cli_ref = sourcebooks / "CLI_Reference"
                if cli_ref.exists():
                    for subdir in ["bestiary", "spells", "items", "rules", "tables"]:
                        if (cli_ref / subdir).exists():
                            count = len(list((cli_ref / subdir).glob("*.md")))
                            dnd_locations["cli_reference"].append(f"{subdir}: {count} files")
                            
        # Check for D&D content in wrong locations
        for md_file in self.vault_path.glob("**/*.md"):
            if "12_Research" not in str(md_file):
                try:
                    content = md_file.read_text(encoding='utf-8')[:1000]  # Check first 1000 chars
                    if re.search(r'CR \d+|Challenge Rating|D&D|5e|PHB|DMG', content):
                        relative_path = md_file.relative_to(self.vault_path)
                        if str(relative_path).split('/')[0] not in ["12_Research", "08_Archive"]:
                            dnd_locations["misplaced"].append(str(relative_path))
                except:
                    pass
                    
        self.audit_results["dnd_content"] = dnd_locations
        
    def check_critical_files(self):
        """Check for critical missing files"""
        print("⚠️ Checking Critical Files...")
        
        critical_files = [
            "00_Indexes/Master_Campaign_Index.md",
            "00_Indexes/Vault_Navigation_Hub.md",
            "01_Adventures/Seven_Shards_Campaign/Campaign_Overview.md",
            "02_Worldbuilding/Groups/Shadow_Conspiracy.md",
            "03_Mechanics/Crystal_Plague_Mechanics.md",
            "12_Research/D&D_Sourcebooks/5E_Official_Content_Integration.md"
        ]
        
        for file_path in critical_files:
            full_path = self.vault_path / file_path
            if not full_path.exists():
                self.audit_results["issues"].append(f"MISSING CRITICAL FILE: {file_path}")
                
    def generate_recommendations(self):
        """Generate specific recommendations based on audit"""
        print("💡 Generating Recommendations...")
        
        # Check for empty directories that should have content
        for dir_name, info in self.audit_results["directories"].items():
            if info["markdown_files"] == 0:
                if "Template" in dir_name:
                    self.audit_results["recommendations"].append(
                        f"CREATE TEMPLATES: {dir_name} is empty - add standard templates"
                    )
                elif "Documentation" in dir_name:
                    self.audit_results["recommendations"].append(
                        f"ADD DOCUMENTATION: {dir_name} needs guides and instructions"
                    )
                elif "Homebrew" in dir_name or "Media" in dir_name:
                    # These can be empty initially
                    pass
                else:
                    self.audit_results["recommendations"].append(
                        f"REVIEW: {dir_name} is empty - consider removing or populating"
                    )
                    
        # Check for duplicate directories
        seen_numbers = {}
        for dir_name in self.audit_results["directories"].keys():
            if '_' in dir_name:
                number = dir_name.split('_')[0]
                if number in seen_numbers:
                    self.audit_results["recommendations"].append(
                        f"MERGE: {dir_name} and {seen_numbers[number]} have same number - consolidate"
                    )
                else:
                    seen_numbers[number] = dir_name
                    
        # Check duplicate files
        if len(self.audit_results["duplicates"]) > 100:
            self.audit_results["recommendations"].append(
                f"DEDUPLICATE: Found {len(self.audit_results['duplicates'])} duplicate file groups - run deduplication"
            )
            
        # Check D&D content
        if self.audit_results["dnd_content"].get("misplaced"):
            self.audit_results["recommendations"].append(
                f"RELOCATE: {len(self.audit_results['dnd_content']['misplaced'])} D&D files in wrong locations"
            )
            
    def generate_report(self):
        """Generate comprehensive audit report"""
        
        # Run all audits
        self.audit_directory_structure()
        self.find_all_duplicates()
        self.audit_dnd_content()
        self.check_critical_files()
        self.generate_recommendations()
        
        # Calculate statistics
        total_files = sum(info["markdown_files"] for info in self.audit_results["directories"].values())
        total_size = sum(info["total_size_mb"] for info in self.audit_results["directories"].values())
        
        # Create report
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_markdown_files": total_files,
                "total_size_mb": round(total_size, 2),
                "directories": len(self.audit_results["directories"]),
                "duplicate_groups": len(self.audit_results["duplicates"]),
                "issues_found": len(self.audit_results["issues"]),
                "recommendations": len(self.audit_results["recommendations"])
            },
            "details": self.audit_results
        }
        
        # Save report
        report_path = self.vault_path / "reports" / f"vault_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        # Print summary
        print("\n" + "="*60)
        print("📊 VAULT AUDIT COMPLETE")
        print("="*60)
        print(f"Total Files: {total_files:,}")
        print(f"Total Size: {total_size:.1f} MB")
        print(f"Directories: {len(self.audit_results['directories'])}")
        print(f"Duplicate Groups: {len(self.audit_results['duplicates'])}")
        print(f"Issues Found: {len(self.audit_results['issues'])}")
        
        if self.audit_results["issues"]:
            print("\n❌ CRITICAL ISSUES:")
            for issue in self.audit_results["issues"][:5]:
                print(f"  • {issue}")
                
        if self.audit_results["recommendations"]:
            print("\n💡 TOP RECOMMENDATIONS:")
            for rec in self.audit_results["recommendations"][:5]:
                print(f"  • {rec}")
                
        print(f"\n📄 Full report: {report_path}")
        
        return report


def main():
    auditor = VaultAuditor()
    auditor.generate_report()


if __name__ == "__main__":
    main()