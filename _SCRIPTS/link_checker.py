#!/usr/bin/env python3
"""
Automated link checker and reporter
"""
import re
from pathlib import Path
from datetime import datetime
import json

def check_links():
    """Check for broken links and generate report"""
    broken_links = []
    total_links = 0
    
    # Build file index
    all_files = set()
    for file in Path(".").rglob("*.md"):
        all_files.add(file.stem)
    
    # Check links in sample of files
    for file_path in list(Path(".").rglob("*.md"))[:100]:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            links = re.findall(r"\[\[([^\]]+)\]\]", content)
            
            for link in links:
                total_links += 1
                clean_link = link.split("#")[0].strip()
                if clean_link and clean_link not in all_files:
                    broken_links.append({
                        "file": str(file_path),
                        "broken_link": link
                    })
        except:
            pass
    
    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_links_checked": total_links,
        "broken_links_found": len(broken_links),
        "sample_broken": broken_links[:10]
    }
    
    report_path = Path("09_Performance/link_check_auto.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Link check complete: {len(broken_links)} broken links found")
    return report

if __name__ == "__main__":
    check_links()
