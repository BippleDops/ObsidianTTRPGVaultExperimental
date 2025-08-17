#!/usr/bin/env python3
"""
Step 3: Broken Link Analysis
Identifies broken links WITHOUT creating files for them
"""

import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class BrokenLinkAnalyzer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.broken_links = defaultdict(list)
        self.all_files = set()
        self.link_count = 0
        self.broken_count = 0
        
    def build_file_index(self):
        """Build index of all existing files"""
        print("📚 Building file index...")
        
        for md_file in self.vault_path.glob("**/*.md"):
            # Skip system folders
            if any(skip in str(md_file) for skip in ['.obsidian', '.git', '_SCRIPTS', '09_Performance']):
                continue
                
            # Store both with and without extension for matching
            relative = md_file.relative_to(self.vault_path)
            self.all_files.add(str(relative))
            self.all_files.add(str(relative.with_suffix('')))
            
            # Also store just the filename for non-path links
            self.all_files.add(md_file.stem)
            
        print(f"  ✓ Indexed {len(self.all_files)} files")
        
    def extract_links(self, content):
        """Extract all wiki-style links from content"""
        # Pattern for [[links]] with optional display text
        pattern = r'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]'
        
        links = []
        for match in re.finditer(pattern, content):
            link = match.group(1).strip()
            # Remove any section references
            if '#' in link:
                link = link.split('#')[0].strip()
            links.append(link)
            
        return links
        
    def check_link_validity(self, link, source_file):
        """Check if a link points to an existing file"""
        # Clean the link
        link = link.strip()
        
        # Skip empty links
        if not link:
            return True
            
        # Check various forms
        checks = [
            link,  # Exact match
            f"{link}.md",  # With extension
            link.replace('/', ''),  # Flattened
        ]
        
        # If it's a relative path, resolve from source file's directory
        if '/' in link:
            source_dir = source_file.parent
            relative_path = source_dir / link
            checks.append(str(relative_path.relative_to(self.vault_path)))
            checks.append(str(relative_path.with_suffix('.md').relative_to(self.vault_path)))
            
        # Check if any form exists
        for check in checks:
            if check in self.all_files:
                return True
                
        return False
        
    def analyze_file(self, file_path):
        """Analyze a single file for broken links"""
        try:
            content = file_path.read_text(encoding='utf-8')
            links = self.extract_links(content)
            
            for link in links:
                self.link_count += 1
                
                if not self.check_link_validity(link, file_path):
                    self.broken_links[str(file_path.relative_to(self.vault_path))].append(link)
                    self.broken_count += 1
                    
        except Exception as e:
            print(f"  Error reading {file_path.name}: {e}")
            
    def scan_vault(self):
        """Scan entire vault for broken links"""
        print("\n🔍 Scanning for broken links...")
        
        files_to_check = list(self.vault_path.glob("**/*.md"))
        files_to_check = [f for f in files_to_check 
                         if not any(skip in str(f) for skip in ['.obsidian', '.git', '_SCRIPTS'])]
        
        total = len(files_to_check)
        for i, file_path in enumerate(files_to_check):
            if i % 100 == 0:
                print(f"  Progress: {i}/{total} files...")
                
            self.analyze_file(file_path)
            
        print(f"  ✓ Scanned {total} files")
        
    def generate_report(self):
        """Generate detailed broken links report"""
        report = f"""# Broken Link Analysis - Step 3/100

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Vault Path**: {self.vault_path}

## 📊 Statistics

- **Total Links Checked**: {self.link_count:,}
- **Broken Links Found**: {self.broken_count:,}
- **Files with Broken Links**: {len(self.broken_links)}
- **Link Health**: {((self.link_count - self.broken_count) / max(1, self.link_count) * 100):.1f}%

## 🔗 Broken Links by File

"""
        
        if self.broken_links:
            # Sort by number of broken links
            sorted_files = sorted(self.broken_links.items(), 
                                key=lambda x: len(x[1]), reverse=True)
            
            # Show top 20 files with most broken links
            for file_path, links in sorted_files[:20]:
                report += f"\n### {file_path}\n"
                report += f"**Broken links**: {len(links)}\n\n"
                
                # Show first 5 broken links
                for link in links[:5]:
                    report += f"- [[{link}]]\n"
                    
                if len(links) > 5:
                    report += f"- *(and {len(links) - 5} more...)*\n"
                    
            if len(sorted_files) > 20:
                report += f"\n## Additional Files\n\n"
                report += f"*{len(sorted_files) - 20} more files have broken links.*\n"
                
        else:
            report += "\n✅ **No broken links found!**\n"
            
        report += f"""

## 📋 Common Broken Link Patterns

"""
        
        # Analyze patterns
        patterns = defaultdict(int)
        for links in self.broken_links.values():
            for link in links:
                if '_CLI_' in link:
                    patterns['CLI References'] += 1
                elif 'step_' in link or 'phase_' in link:
                    patterns['Step/Phase References'] += 1
                elif link.startswith('#'):
                    patterns['Section References'] += 1
                elif '/' in link:
                    patterns['Path References'] += 1
                else:
                    patterns['Simple References'] += 1
                    
        for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{pattern}**: {count} links\n"
            
        report += f"""

## ⚠️ Important Notes

1. **DO NOT** create files for these broken links
2. These links should be:
   - Fixed to point to correct files
   - Removed if no longer relevant
   - Converted to plain text if not meant as links

## 🔧 Recommended Actions

1. Review files with most broken links
2. Identify patterns that can be bulk-fixed
3. Update or remove outdated references
4. Consider creating missing important files (with permission)

## ✅ Next Steps

Ready to proceed to Step 4: Duplicate Detection

---
*Analysis complete. No files were created or modified.*
"""
        
        report_path = self.vault_path / "09_Performance" / f"broken_links_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Report saved: {report_path.name}")
        
        # Also save detailed JSON for potential automated fixing
        import json
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "total_links": self.link_count,
                "broken_links": self.broken_count,
                "files_affected": len(self.broken_links)
            },
            "broken_links": dict(self.broken_links)
        }
        
        json_path = self.vault_path / "09_Performance" / f"broken_links_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        json_path.write_text(json.dumps(json_data, indent=2), encoding='utf-8')
        
    def run(self):
        """Execute the analysis"""
        print("=" * 60)
        print("🔗 BROKEN LINK ANALYSIS (Step 3/100)")
        print("=" * 60)
        
        self.build_file_index()
        self.scan_vault()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ ANALYSIS COMPLETE")
        print(f"   Total Links: {self.link_count:,}")
        print(f"   Broken Links: {self.broken_count:,}")
        print(f"   Health Score: {((self.link_count - self.broken_count) / max(1, self.link_count) * 100):.1f}%")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    analyzer = BrokenLinkAnalyzer(vault_path)
    analyzer.run()