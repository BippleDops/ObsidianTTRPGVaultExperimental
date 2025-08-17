#!/usr/bin/env python3
"""
Quick optimization focusing on critical improvements
"""

import re
from pathlib import Path
from datetime import datetime
import json

class QuickOptimizer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.stats = {
            "files_processed": 0,
            "metadata_added": 0,
            "links_fixed": 0,
            "formatting_fixed": 0
        }
        
    def quick_fix_file(self, file_path: Path) -> bool:
        """Quick optimization of a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original = content
            
            # 1. Add metadata if missing (quick check)
            if not content.startswith('---\n'):
                metadata = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
type: note
tags:
- vault
---

"""
                content = metadata + content
                self.stats["metadata_added"] += 1
                
            # 2. Fix obvious formatting issues
            # Multiple blank lines
            old_len = len(content)
            content = re.sub(r'\n{4,}', '\n\n\n', content)
            if len(content) != old_len:
                self.stats["formatting_fixed"] += 1
                
            # 3. Fix broken image links
            content = re.sub(r'!\[\[([^]]+)\]\]', r'![[04_Resources/Assets/\1]]', content)
            if content != original:
                self.stats["links_fixed"] += 1
                
            # Save if changed
            if content != original:
                file_path.write_text(content, encoding='utf-8')
                return True
                
        except Exception:
            pass
            
        return False
        
    def optimize_priority_directories(self):
        """Optimize the most important directories first"""
        
        priority_dirs = [
            "00_Indexes",
            "01_Adventures",
            "02_Worldbuilding/People",
            "02_Worldbuilding/Places",
            "02_Worldbuilding/Groups"
        ]
        
        print("⚡ Quick Optimization Starting...")
        print("="*60)
        
        for dir_path_str in priority_dirs:
            dir_path = self.vault_path / dir_path_str
            if not dir_path.exists():
                continue
                
            print(f"\n📁 {dir_path_str}")
            
            # Process markdown files
            count = 0
            for md_file in dir_path.rglob("*.md"):
                # Skip archives
                if '08_Archive' in str(md_file):
                    continue
                    
                if self.quick_fix_file(md_file):
                    count += 1
                    
                self.stats["files_processed"] += 1
                
                # Progress
                if self.stats["files_processed"] % 100 == 0:
                    print(f"   Processed {self.stats['files_processed']} files...")
                    
            print(f"   ✅ Fixed {count} files")
            
        # Print results
        print("\n" + "="*60)
        print("⚡ QUICK OPTIMIZATION COMPLETE")
        print("="*60)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Metadata added: {self.stats['metadata_added']}")
        print(f"Links fixed: {self.stats['links_fixed']}")
        print(f"Formatting fixed: {self.stats['formatting_fixed']}")
        
        # Save stats
        report_path = self.vault_path / "reports" / f"quick_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(self.stats, f, indent=2)
            
        print(f"\n📄 Report: {report_path}")

def main():
    optimizer = QuickOptimizer()
    optimizer.optimize_priority_directories()

if __name__ == "__main__":
    main()