#!/usr/bin/env python3
"""
Quick link analysis for Steps 31-40
Optimized for large vaults
"""
import os
import re
from pathlib import Path
from datetime import datetime
import json

def quick_link_scan():
    """Fast scan for broken links"""
    print("\n🔍 QUICK LINK SCAN (Steps 31-40)")
    
    # Sample first 1000 markdown files only
    sample_files = []
    for root, dirs, files in os.walk("."):
        if any(skip in root for skip in [".obsidian", "09_Performance", ".git", "08_Archive"]):
            continue
        for file in files:
            if file.endswith(".md"):
                sample_files.append(Path(root) / file)
                if len(sample_files) >= 1000:
                    break
        if len(sample_files) >= 1000:
            break
    
    print(f"  Sampling {len(sample_files)} files...")
    
    # Pattern for wiki links only (most common)
    wiki_pattern = r'\[\[([^\]]+)\]\]'
    
    broken_count = 0
    total_links = 0
    sample_broken = []
    
    # Build quick name index
    existing = set()
    for root, dirs, files in os.walk("."):
        if ".obsidian" not in root and ".git" not in root:
            for file in files:
                if file.endswith(".md"):
                    existing.add(file[:-3])  # Remove .md
    
    # Check sample files
    for file_path in sample_files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            links = re.findall(wiki_pattern, content)
            
            for link in links:
                total_links += 1
                clean_link = link.split("#")[0].strip()
                
                if clean_link and clean_link not in existing:
                    broken_count += 1
                    if len(sample_broken) < 20:
                        sample_broken.append((file_path.name, link))
        except:
            pass
    
    # Extrapolate
    total_md_files = sum(1 for root, dirs, files in os.walk(".") 
                        for file in files if file.endswith(".md"))
    estimated_broken = int(broken_count * (total_md_files / len(sample_files)))
    
    print(f"\n📊 Quick Analysis Results:")
    print(f"  Sample size: {len(sample_files)} files")
    print(f"  Links found: {total_links}")
    print(f"  Broken in sample: {broken_count}")
    print(f"  Estimated total broken: ~{estimated_broken}")
    
    # Create quick report
    report_path = Path("09_Performance/link_analysis_quick.md")
    with open(report_path, 'w') as f:
        f.write("# Quick Link Analysis (Steps 31-40)\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Sampled {len(sample_files)} of {total_md_files} files\n")
        f.write(f"- Found {broken_count} broken links in sample\n")
        f.write(f"- Estimated total broken links: ~{estimated_broken}\n\n")
        f.write("## Sample Broken Links\n\n")
        for file, link in sample_broken:
            f.write(f"- {file}: [[{link}]]\n")
    
    print(f"  ✓ Report: {report_path}")
    
    return estimated_broken

def main():
    print("=" * 60)
    print("PHASE 3: LINK ANALYSIS (STEPS 31-40) - QUICK MODE")
    print("=" * 60)
    
    estimated_broken = quick_link_scan()
    
    print("\n" + "=" * 60)
    print("STEPS 31-40 COMPLETE!")
    print("=" * 60)
    print(f"\n✓ Estimated {estimated_broken} broken links to fix")
    print("✓ Quick analysis complete")
    print("✓ Ready for Steps 41-50")

if __name__ == "__main__":
    main()