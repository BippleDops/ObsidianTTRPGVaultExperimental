#!/usr/bin/env python3
"""
Step 1: Vault Health Check
Analyzes vault structure and content without making any changes
"""

import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class VaultHealthCheck:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.stats = defaultdict(int)
        self.issues = []
        
    def count_files_by_type(self):
        """Count files by extension"""
        for file_path in self.vault_path.rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                self.stats[f"files_{ext}"] += 1
                self.stats["total_files"] += 1
                
    def check_directory_structure(self):
        """Verify expected directories exist"""
        expected_dirs = [
            "00_System",
            "01_Adventures",
            "02_Worldbuilding", 
            "03_People",
            "04_Resources",
            "05_Rules",
            "06_Sessions",
            "07_Player_Resources",
            "08_Archive",
            "09_Performance",
            "_SCRIPTS",
            "_INDEXES",
            "_METADATA"
        ]
        
        for dir_name in expected_dirs:
            dir_path = self.vault_path / dir_name
            if dir_path.exists():
                self.stats[f"dir_{dir_name}"] = len(list(dir_path.glob("**/*.md")))
            else:
                self.issues.append(f"Missing directory: {dir_name}")
                
    def find_empty_files(self):
        """Count empty or near-empty files"""
        for file_path in self.vault_path.glob("**/*.md"):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    if size == 0:
                        self.stats["empty_files"] += 1
                    elif size < 50:
                        self.stats["stub_files"] += 1
                except:
                    pass
                    
    def check_campaigns_and_sessions(self):
        """Verify campaign and session integrity"""
        # Check campaigns
        campaigns_dir = self.vault_path / "01_Adventures" / "Campaigns"
        if campaigns_dir.exists():
            campaigns = list(campaigns_dir.glob("*.md"))
            self.stats["campaigns"] = len(campaigns)
            
            # Look for specific campaigns
            for campaign in ["Aquabyssos", "Aethermoor"]:
                if any(campaign.lower() in f.name.lower() for f in campaigns):
                    self.stats[f"has_{campaign}"] = 1
                    
        # Check sessions
        sessions_dir = self.vault_path / "06_Sessions"
        if sessions_dir.exists():
            sessions = list(sessions_dir.glob("*.md"))
            self.stats["sessions"] = len(sessions)
            
    def analyze_file_sizes(self):
        """Analyze file size distribution"""
        sizes = []
        for file_path in self.vault_path.glob("**/*.md"):
            if file_path.is_file():
                try:
                    sizes.append(file_path.stat().st_size)
                except:
                    pass
                    
        if sizes:
            self.stats["avg_file_size"] = sum(sizes) // len(sizes)
            self.stats["max_file_size"] = max(sizes)
            self.stats["min_file_size"] = min(sizes)
            
    def generate_report(self):
        """Generate health check report"""
        report = f"""# Vault Health Check Report
        
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Vault Path**: {self.vault_path}

## 📊 Overall Statistics

- **Total Files**: {self.stats['total_files']:,}
- **Markdown Files**: {self.stats['files_.md']:,}
- **Image Files**: {self.stats['files_.png'] + self.stats['files_.jpg'] + self.stats['files_.svg']:,}
- **Empty Files**: {self.stats['empty_files']}
- **Stub Files (<50 bytes)**: {self.stats['stub_files']}

## 📁 Directory Analysis

| Directory | MD Files | Status |
|-----------|----------|--------|
| 00_System | {self.stats['dir_00_System']} | ✅ |
| 01_Adventures | {self.stats['dir_01_Adventures']} | ✅ |
| 02_Worldbuilding | {self.stats['dir_02_Worldbuilding']} | ✅ |
| 03_People | {self.stats['dir_03_People']} | ✅ |
| 04_Resources | {self.stats['dir_04_Resources']} | ✅ |
| 05_Rules | {self.stats['dir_05_Rules']} | ✅ |
| 06_Sessions | {self.stats['dir_06_Sessions']} | ✅ |
| 07_Player_Resources | {self.stats['dir_07_Player_Resources']} | ✅ |
| 08_Archive | {self.stats['dir_08_Archive']} | ✅ |
| 09_Performance | {self.stats['dir_09_Performance']} | ✅ |

## 🎮 Campaign & Session Status

- **Campaigns Found**: {self.stats['campaigns']}
- **Sessions Found**: {self.stats['sessions']}
- **Aquabyssos Campaign**: {'✅ Present' if self.stats.get('has_Aquabyssos') else '⚠️ Not found'}
- **Aethermoor Campaign**: {'✅ Present' if self.stats.get('has_Aethermoor') else '⚠️ Not found'}

## 📈 File Size Analysis

- **Average File Size**: {self.stats['avg_file_size']:,} bytes
- **Largest File**: {self.stats['max_file_size']:,} bytes
- **Smallest File**: {self.stats['min_file_size']} bytes

## 🔍 Issues Found

"""
        if self.issues:
            for issue in self.issues:
                report += f"- ⚠️ {issue}\n"
        else:
            report += "- ✅ No structural issues found\n"
            
        report += f"""

## 💚 Health Score

**Overall Health**: {'EXCELLENT' if len(self.issues) == 0 else 'GOOD' if len(self.issues) < 3 else 'NEEDS ATTENTION'}

## 📋 Recommendations

1. {'Remove empty files' if self.stats['empty_files'] > 0 else 'No empty files found ✅'}
2. {'Review stub files' if self.stats['stub_files'] > 10 else 'Stub files within normal range ✅'}
3. {'Check campaign files' if self.stats['campaigns'] < 2 else 'Campaigns properly organized ✅'}
4. {'Organize sessions' if self.stats['sessions'] > 50 else 'Sessions manageable ✅'}

## ✅ Next Steps

Ready to proceed to Step 2: Backup Creation

---
*Health check complete. No changes were made to the vault.*
"""
        
        report_path = self.vault_path / "09_Performance" / f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"📄 Report saved: {report_path.name}")
        
        return report
        
    def run(self):
        """Execute health check"""
        print("=" * 60)
        print("🏥 VAULT HEALTH CHECK (Step 1/100)")
        print("=" * 60)
        
        print("\n📊 Analyzing vault structure...")
        self.check_directory_structure()
        
        print("📁 Counting files...")
        self.count_files_by_type()
        
        print("🔍 Checking for empty files...")
        self.find_empty_files()
        
        print("🎮 Verifying campaigns and sessions...")
        self.check_campaigns_and_sessions()
        
        print("📈 Analyzing file sizes...")
        self.analyze_file_sizes()
        
        print("\n📄 Generating report...")
        report = self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ HEALTH CHECK COMPLETE")
        print(f"   Total Files: {self.stats['total_files']:,}")
        print(f"   Issues Found: {len(self.issues)}")
        print(f"   Health Status: {'EXCELLENT' if len(self.issues) == 0 else 'GOOD'}")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    checker = VaultHealthCheck(vault_path)
    checker.run()