#!/usr/bin/env python3
"""
Find broken links and problematic bracket patterns in the vault
"""

import re
from pathlib import Path
from collections import defaultdict

def extract_links(content):
    """Extract all [[wiki-style]] links from content"""
    # Pattern to match [[link]] or [[link|alias]]
    pattern = r'\[\[([^\]]+?)\]\]'
    matches = re.findall(pattern, content)
    
    links = []
    for match in matches:
        # Handle aliases - get the actual link part
        if '|' in match:
            link = match.split('|')[0]
        else:
            link = match
        
        # Handle section links
        if '#' in link:
            link = link.split('#')[0]
            
        links.append(link.strip())
    
    return links

def find_template_placeholders(content):
    """Find {{template}} or {%template%} placeholders"""
    templates = []
    
    # Find {{...}} patterns
    double_bracket = re.findall(r'\{\{([^}]+)\}\}', content)
    templates.extend([f"{{{{{t}}}}}" for t in double_bracket])
    
    # Find {%...%} patterns  
    percent_bracket = re.findall(r'\{%([^%]+)%\}', content)
    templates.extend([f"{{%{t}%}}" for t in percent_bracket])
    
    return templates

def main():
    vault_root = Path.cwd()
    
    # Collect all markdown files (excluding archives)
    all_files = {}
    for md_file in vault_root.rglob("*.md"):
        if any(skip in str(md_file) for skip in ['08_Archive', '09_Performance', '.git', '_SCRIPTS']):
            continue
        
        # Store both full path and just the name for matching
        rel_path = md_file.relative_to(vault_root)
        all_files[str(rel_path)] = md_file
        all_files[md_file.stem] = md_file  # Just the filename without extension
    
    # Analyze links
    broken_links = defaultdict(list)
    template_files = []
    empty_brackets = defaultdict(list)
    
    for filepath in all_files.values():
        if filepath.is_file():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                rel_path = filepath.relative_to(vault_root)
                
                # Check for template placeholders in filename
                if '{{' in filepath.name or '{%' in filepath.name:
                    template_files.append(str(rel_path))
                
                # Extract and check links
                links = extract_links(content)
                for link in links:
                    if not link:  # Empty link [[]]
                        empty_brackets[str(rel_path)].append("[[]]")
                        continue
                        
                    # Check if link target exists
                    found = False
                    
                    # Try exact match
                    if link in all_files:
                        found = True
                    
                    # Try with .md extension
                    elif link + '.md' in all_files:
                        found = True
                    
                    # Try as relative path from current file
                    else:
                        current_dir = filepath.parent
                        potential_path = current_dir / link
                        if potential_path.with_suffix('.md').exists():
                            found = True
                    
                    if not found:
                        broken_links[str(rel_path)].append(f"[[{link}]]")
                
                # Find template placeholders in content
                templates = find_template_placeholders(content)
                if templates:
                    empty_brackets[str(rel_path)].extend(templates)
                    
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    
    # Output results
    print("=" * 80)
    print("BROKEN LINKS AND BRACKET ANALYSIS REPORT")
    print("=" * 80)
    
    print("\n### TEMPLATE/PLACEHOLDER FILES (files with {{}} or {%%} in name):")
    print("-" * 40)
    if template_files:
        for file in sorted(template_files):
            print(f"  - {file}")
    else:
        print("  None found")
    
    print(f"\n### BROKEN WIKI LINKS (target doesn't exist):")
    print("-" * 40)
    if broken_links:
        total_broken = sum(len(links) for links in broken_links.values())
        print(f"Found {total_broken} broken links in {len(broken_links)} files:\n")
        
        # Group by link target for easier review
        link_targets = defaultdict(list)
        for file, links in broken_links.items():
            for link in links:
                # Extract just the link text
                clean_link = link.replace('[[', '').replace(']]', '')
                link_targets[clean_link].append(file)
        
        # Sort by frequency
        sorted_targets = sorted(link_targets.items(), key=lambda x: len(x[1]), reverse=True)
        
        for target, files in sorted_targets[:50]:  # Show top 50 most common broken links
            print(f"\n  [[{target}]] - Found in {len(files)} file(s):")
            for file in files[:3]:  # Show first 3 files
                print(f"    - {file}")
            if len(files) > 3:
                print(f"    ... and {len(files) - 3} more")
    else:
        print("  No broken links found!")
    
    print(f"\n### EMPTY BRACKETS OR TEMPLATE PLACEHOLDERS IN CONTENT:")
    print("-" * 40)
    if empty_brackets:
        print(f"Found problematic brackets in {len(empty_brackets)} files:\n")
        for file, brackets in list(empty_brackets.items())[:20]:  # Show first 20
            print(f"  {file}:")
            for bracket in set(brackets):  # Unique brackets only
                print(f"    - {bracket}")
        
        if len(empty_brackets) > 20:
            print(f"\n  ... and {len(empty_brackets) - 20} more files")
    else:
        print("  No empty brackets found")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print(f"  - Template/placeholder files: {len(template_files)}")
    print(f"  - Files with broken links: {len(broken_links)}")
    print(f"  - Total broken links: {sum(len(links) for links in broken_links.values())}")
    print(f"  - Files with empty/template brackets: {len(empty_brackets)}")
    print("=" * 80)
    
    return broken_links, template_files, empty_brackets

if __name__ == "__main__":
    main()