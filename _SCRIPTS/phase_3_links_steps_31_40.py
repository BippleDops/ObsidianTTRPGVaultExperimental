#!/usr/bin/env python3
"""
Steps 31-40: Link Repair & Optimization
This phase focuses on fixing broken links and optimizing references
"""
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

def find_all_links():
    """Step 31-32: Scan all markdown files for links"""
    print("\n🔍 SCANNING FOR ALL LINKS (Steps 31-32)")
    
    all_links = defaultdict(list)  # file -> list of links
    link_patterns = [
        r'\[\[([^\]]+)\]\]',  # Wiki links
        r'\[([^\]]+)\]\(([^\)]+)\)',  # Markdown links
        r'!\[\[([^\]]+)\]\]',  # Embedded wiki links
        r'!\[([^\]]*)\]\(([^\)]+)\)'  # Embedded markdown links
    ]
    
    total_files = 0
    total_links = 0
    
    for root, dirs, files in os.walk("."):
        # Skip non-content directories
        if any(skip in root for skip in [".obsidian", "09_Performance", ".git"]):
            continue
            
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                total_files += 1
                
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    for pattern in link_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # Handle different match formats
                            if isinstance(match, tuple):
                                link = match[-1]  # Get the actual link part
                            else:
                                link = match
                            
                            all_links[str(file_path)].append(link)
                            total_links += 1
                            
                except Exception as e:
                    print(f"  ⚠️  Error reading {file_path}: {e}")
    
    print(f"  ✓ Scanned {total_files} files")
    print(f"  ✓ Found {total_links} total links")
    print(f"  ✓ Files with links: {len(all_links)}")
    
    return all_links

def check_link_validity(all_links):
    """Step 33-35: Check which links are broken"""
    print("\n🔧 CHECKING LINK VALIDITY (Steps 33-35)")
    
    # Build a set of all existing files
    existing_files = set()
    existing_names = {}  # basename -> full paths
    
    for root, dirs, files in os.walk("."):
        if ".obsidian" in root or ".git" in root:
            continue
        for file in files:
            full_path = Path(root) / file
            relative_path = full_path.relative_to(".")
            existing_files.add(str(relative_path))
            
            # Also track by basename for wiki links
            basename = file.replace(".md", "") if file.endswith(".md") else file
            if basename not in existing_names:
                existing_names[basename] = []
            existing_names[basename].append(str(relative_path))
    
    # Check each link
    broken_links = defaultdict(list)
    working_links = defaultdict(list)
    ambiguous_links = defaultdict(list)
    
    for source_file, links in all_links.items():
        for link in links:
            # Clean the link
            clean_link = link.strip()
            
            # Remove anchors
            if "#" in clean_link:
                clean_link = clean_link.split("#")[0]
            
            # Skip empty links or special links
            if not clean_link or clean_link.startswith("http") or clean_link.startswith("#"):
                continue
            
            # Check if it's a path or just a name
            if "/" in clean_link:
                # It's a path - check directly
                if clean_link in existing_files or f"{clean_link}.md" in existing_files:
                    working_links[source_file].append(link)
                else:
                    broken_links[source_file].append(link)
            else:
                # It's a wiki link - check by name
                if clean_link in existing_names:
                    if len(existing_names[clean_link]) == 1:
                        working_links[source_file].append(link)
                    else:
                        ambiguous_links[source_file].append((link, existing_names[clean_link]))
                else:
                    # Try with .md extension
                    if f"{clean_link}.md" in existing_names:
                        working_links[source_file].append(link)
                    else:
                        broken_links[source_file].append(link)
    
    print(f"  ✓ Working links: {sum(len(v) for v in working_links.values())}")
    print(f"  ⚠️  Broken links: {sum(len(v) for v in broken_links.values())}")
    print(f"  ⚠️  Ambiguous links: {sum(len(v) for v in ambiguous_links.values())}")
    
    return broken_links, working_links, ambiguous_links

def create_link_fix_suggestions(broken_links, existing_names):
    """Step 36-37: Generate suggestions for fixing broken links"""
    print("\n💡 GENERATING FIX SUGGESTIONS (Steps 36-37)")
    
    suggestions = {}
    
    for source_file, links in broken_links.items():
        file_suggestions = []
        
        for broken_link in links:
            clean_link = broken_link.strip().replace("#", "").replace(".md", "")
            
            # Find similar files
            possible_matches = []
            
            for existing_name in existing_names.keys():
                # Check for exact match ignoring case
                if existing_name.lower() == clean_link.lower():
                    possible_matches.append((100, existing_name))
                # Check for partial matches
                elif clean_link.lower() in existing_name.lower():
                    score = 80 - abs(len(existing_name) - len(clean_link))
                    possible_matches.append((score, existing_name))
                elif existing_name.lower() in clean_link.lower():
                    score = 70 - abs(len(existing_name) - len(clean_link))
                    possible_matches.append((score, existing_name))
                # Check for word overlap
                else:
                    clean_words = set(clean_link.lower().split())
                    existing_words = set(existing_name.lower().split())
                    overlap = len(clean_words & existing_words)
                    if overlap > 0:
                        score = overlap * 20
                        possible_matches.append((score, existing_name))
            
            # Sort by score and take top 3
            possible_matches.sort(reverse=True, key=lambda x: x[0])
            top_matches = possible_matches[:3]
            
            if top_matches:
                file_suggestions.append({
                    "broken_link": broken_link,
                    "suggestions": [match[1] for match in top_matches]
                })
        
        if file_suggestions:
            suggestions[source_file] = file_suggestions
    
    print(f"  ✓ Generated suggestions for {len(suggestions)} files")
    
    return suggestions

def optimize_link_format(all_links):
    """Step 38-39: Suggest link format optimizations"""
    print("\n⚡ OPTIMIZING LINK FORMATS (Steps 38-39)")
    
    optimizations = defaultdict(list)
    
    for source_file, links in all_links.items():
        for link in links:
            # Check for redundant .md extensions in wiki links
            if "[[" in str(link) and link.endswith(".md]]"):
                optimizations[source_file].append({
                    "current": f"[[{link}]]",
                    "suggested": f"[[{link[:-3]}]]",
                    "reason": "Remove .md from wiki link"
                })
            
            # Check for absolute paths that could be relative
            if link.startswith("/"):
                optimizations[source_file].append({
                    "current": link,
                    "suggested": link[1:],
                    "reason": "Use relative path"
                })
    
    print(f"  ✓ Found {sum(len(v) for v in optimizations.values())} optimization opportunities")
    
    return optimizations

def create_link_report(broken_links, working_links, ambiguous_links, suggestions, optimizations):
    """Step 40: Create comprehensive link report"""
    print("\n📝 CREATING LINK REPORT (Step 40)")
    
    report_path = Path("09_Performance/link_analysis_phase3.md")
    
    with open(report_path, 'w') as f:
        f.write("# Phase 3 Link Analysis Report (Steps 31-40)\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        # Summary
        f.write("## Summary\n\n")
        total_broken = sum(len(v) for v in broken_links.values())
        total_working = sum(len(v) for v in working_links.values())
        total_ambiguous = sum(len(v) for v in ambiguous_links.values())
        
        f.write(f"- Total links analyzed: {total_broken + total_working + total_ambiguous}\n")
        f.write(f"- Working links: {total_working}\n")
        f.write(f"- Broken links: {total_broken}\n")
        f.write(f"- Ambiguous links: {total_ambiguous}\n\n")
        
        # Top broken links
        f.write("## Top Files with Broken Links\n\n")
        sorted_broken = sorted(broken_links.items(), key=lambda x: len(x[1]), reverse=True)[:20]
        for file, links in sorted_broken:
            f.write(f"### {Path(file).name} ({len(links)} broken)\n")
            for link in links[:5]:
                f.write(f"- [[{link}]]\n")
                if file in suggestions:
                    for sug in suggestions[file]:
                        if sug["broken_link"] == link and sug["suggestions"]:
                            f.write(f"  - Suggested: [[{sug['suggestions'][0]}]]\n")
            if len(links) > 5:
                f.write(f"- ... and {len(links) - 5} more\n")
            f.write("\n")
        
        # Ambiguous links
        if ambiguous_links:
            f.write("## Ambiguous Links (Multiple Targets)\n\n")
            for file, links in list(ambiguous_links.items())[:10]:
                f.write(f"### {Path(file).name}\n")
                for link, targets in links[:3]:
                    f.write(f"- [[{link}]] could be:\n")
                    for target in targets[:3]:
                        f.write(f"  - {target}\n")
                f.write("\n")
        
        # Optimization suggestions
        if optimizations:
            f.write("## Link Format Optimizations\n\n")
            total_opts = sum(len(v) for v in optimizations.values())
            f.write(f"Found {total_opts} optimization opportunities\n\n")
            
            for file, opts in list(optimizations.items())[:10]:
                f.write(f"### {Path(file).name}\n")
                for opt in opts[:3]:
                    f.write(f"- {opt['reason']}: `{opt['current']}` → `{opt['suggested']}`\n")
                f.write("\n")
    
    print(f"  ✓ Report created: {report_path}")
    
    # Also create a JSON file with all broken links for processing
    json_path = Path("09_Performance/broken_links.json")
    with open(json_path, 'w') as f:
        json.dump({
            "broken_links": {k: v for k, v in broken_links.items()},
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"  ✓ JSON data saved: {json_path}")
    
    return report_path

def main():
    print("=" * 60)
    print("PHASE 3: LINK REPAIR & OPTIMIZATION (STEPS 31-40)")
    print("=" * 60)
    
    # Step 31-32: Find all links
    all_links = find_all_links()
    
    # Step 33-35: Check link validity
    broken_links, working_links, ambiguous_links = check_link_validity(all_links)
    
    # Build name index for suggestions
    existing_names = {}
    for root, dirs, files in os.walk("."):
        if ".obsidian" not in root and ".git" not in root:
            for file in files:
                if file.endswith(".md"):
                    basename = file[:-3]
                    existing_names[basename] = Path(root) / file
    
    # Step 36-37: Generate fix suggestions
    suggestions = create_link_fix_suggestions(broken_links, existing_names)
    
    # Step 38-39: Optimize link formats
    optimizations = optimize_link_format(all_links)
    
    # Step 40: Create comprehensive report
    report_path = create_link_report(broken_links, working_links, ambiguous_links, suggestions, optimizations)
    
    print("\n" + "=" * 60)
    print("PHASE 3 COMPLETE!")
    print("=" * 60)
    print("\n📊 Results Summary:")
    print(f"✓ Steps 31-40 complete")
    print(f"✓ Analyzed {len(all_links)} files with links")
    print(f"✓ Found {sum(len(v) for v in broken_links.values())} broken links")
    print(f"✓ Generated fix suggestions")
    print(f"✓ Report: {report_path}")
    print("\n⚠️  No links were modified - analysis only")
    
    return True

if __name__ == "__main__":
    main()