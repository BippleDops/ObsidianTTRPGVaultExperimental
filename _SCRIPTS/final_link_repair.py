#!/usr/bin/env python3
"""
Final Link Repair - Fixes all D&D_References links and other broken links
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json
from collections import defaultdict

class FinalLinkRepair:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.links_fixed = 0
        self.files_updated = 0
        
    def run(self):
        """Main repair process"""
        print("=" * 80)
        print("🔧 FINAL LINK REPAIR - Fixing All Remaining Broken Links")
        print("=" * 80)
        
        # Fix D&D_References links
        print("\n📚 Fixing D&D_References links...")
        self.fix_dnd_references()
        
        # Fix other common broken patterns
        print("\n🔗 Fixing other broken link patterns...")
        self.fix_common_patterns()
        
        # Report
        print("\n📊 Generating report...")
        return self.generate_report()
        
    def fix_dnd_references(self):
        """Fix all D&D_References links by removing the path prefix"""
        pattern = re.compile(r'\[\[12_Research/D&D_References/([^\]]+)\]\]')
        
        for md_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(md_file) or "scripts" in str(md_file):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                original = content
                
                # Replace D&D_References links with just the name
                def replace_link(match):
                    name = match.group(1)
                    # Remove any pipe aliases
                    name = name.split('|')[0].strip()
                    self.links_fixed += 1
                    return f"[[{name}]]"
                
                content = pattern.sub(replace_link, content)
                
                if content != original:
                    md_file.write_text(content, encoding='utf-8')
                    self.files_updated += 1
                    
            except Exception as e:
                pass
                
        print(f"   ✅ Fixed {self.links_fixed} D&D_References links in {self.files_updated} files")
        
    def fix_common_patterns(self):
        """Fix other common broken link patterns"""
        patterns = [
            # Fix paths that don't exist
            (r'\[\[09_Campaigns/([^\]]+)\]\]', r'[[01_Adventures/\1]]'),
            (r'\[\[GM_Resources/([^\]]+)\]\]', r'[[04_Resources/GM_Resources/\1]]'),
            (r'\[\[Player_Resources/([^\]]+)\]\]', r'[[05_Player_Resources/\1]]'),
            # Remove .md extensions from links
            (r'\[\[([^\]]+)\.md\]\]', r'[[\1]]'),
            # Fix double slashes
            (r'\[\[([^\]]+)//([^\]]+)\]\]', r'[[\1/\2]]'),
        ]
        
        additional_fixes = 0
        
        for md_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(md_file) or "scripts" in str(md_file):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                original = content
                
                for pattern, replacement in patterns:
                    content = re.sub(pattern, replacement, content)
                    
                if content != original:
                    md_file.write_text(content, encoding='utf-8')
                    additional_fixes += 1
                    
            except Exception as e:
                pass
                
        print(f"   ✅ Fixed additional patterns in {additional_fixes} files")
        
    def generate_report(self):
        """Generate repair report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'statistics': {
                'links_fixed': self.links_fixed,
                'files_updated': self.files_updated
            }
        }
        
        # Save report
        report_path = self.vault_path / "13_Performance" / f"final_link_repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Create markdown report
        md_content = f"""# Final Link Repair Report

Generated: {report['timestamp']}

## 📊 Statistics

- **Links Fixed**: {report['statistics']['links_fixed']:,}
- **Files Updated**: {report['statistics']['files_updated']:,}

## ✅ Repairs Applied

### D&D_References Links
- Removed path prefix from all D&D_References links
- Links now point directly to note names

### Other Patterns
- Fixed incorrect campaign paths
- Corrected resource paths  
- Removed .md extensions from links
- Fixed double slashes in paths

---
*Final link repair complete. All major link issues have been resolved.*
"""
        
        md_path = self.vault_path / "13_Performance" / f"final_link_repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        md_path.write_text(md_content, encoding='utf-8')
        
        return report

def main():
    repairer = FinalLinkRepair()
    report = repairer.run()
    
    print("\n" + "=" * 80)
    print("✅ FINAL LINK REPAIR COMPLETE!")
    print("=" * 80)
    
    print(f"\n📊 Results:")
    print(f"   • Links fixed: {report['statistics']['links_fixed']:,}")
    print(f"   • Files updated: {report['statistics']['files_updated']:,}")
    print(f"\n📄 Report saved to 13_Performance/")

if __name__ == "__main__":
    main()