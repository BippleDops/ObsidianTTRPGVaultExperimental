#!/usr/bin/env python3
"""
Steps 21-30: Organization Within Folders
This phase organizes files WITHIN existing folders without changing structure
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

def create_backup():
    """Create lightweight backup before organization"""
    backup_dir = Path("09_Performance/organization_backup")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "file_locations": {}
    }
    
    # Record current locations of all markdown files
    for root, dirs, files in os.walk("."):
        if any(skip in root for skip in ["09_Performance", ".obsidian", "08_Archive"]):
            continue
        for file in files:
            if file.endswith(".md"):
                manifest["file_locations"][file] = root
    
    manifest_path = backup_dir / f"manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✓ Backup manifest created: {manifest_path}")
    return manifest_path

def organize_adventures():
    """Step 21-23: Organize adventure content within 01_Adventures"""
    print("\n📚 ORGANIZING ADVENTURES (Steps 21-23)")
    adventures_dir = Path("01_Adventures")
    
    # Define subcategories
    categories = {
        "Campaigns": ["campaign", "adventure path", "story arc"],
        "Quests": ["quest", "mission", "task", "objective"],
        "Encounters": ["encounter", "combat", "battle", "fight"],
        "Hooks": ["hook", "plot hook", "adventure hook", "rumor"],
        "Scenarios": ["scenario", "scene", "situation"]
    }
    
    organized = defaultdict(list)
    
    # Scan and categorize
    for file_path in adventures_dir.rglob("*.md"):
        if "Archive" in str(file_path):
            continue
            
        content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
        filename = file_path.name.lower()
        
        categorized = False
        for category, keywords in categories.items():
            if any(kw in filename or kw in content[:500] for kw in keywords):
                organized[category].append(file_path)
                categorized = True
                break
        
        if not categorized:
            organized["General"].append(file_path)
    
    # Report findings (don't move without permission)
    print("\n📊 Adventure Organization Analysis:")
    for category, files in organized.items():
        print(f"  {category}: {len(files)} files")
        if len(files) <= 5:
            for f in files:
                print(f"    - {f.name}")
    
    return organized

def organize_worldbuilding():
    """Step 24-26: Organize worldbuilding within 02_Worldbuilding"""
    print("\n🌍 ORGANIZING WORLDBUILDING (Steps 24-26)")
    world_dir = Path("02_Worldbuilding")
    
    categories = {
        "Locations": ["location", "place", "city", "town", "region", "kingdom"],
        "Lore": ["lore", "history", "legend", "myth", "story", "tale"],
        "Factions": ["faction", "guild", "order", "organization", "group"],
        "Geography": ["map", "geography", "terrain", "climate"],
        "Culture": ["culture", "tradition", "custom", "religion", "deity"]
    }
    
    organized = defaultdict(list)
    
    for file_path in world_dir.rglob("*.md"):
        if "Archive" in str(file_path):
            continue
            
        content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
        filename = file_path.name.lower()
        
        categorized = False
        for category, keywords in categories.items():
            if any(kw in filename or kw in content[:500] for kw in keywords):
                organized[category].append(file_path)
                categorized = True
                break
        
        if not categorized:
            organized["General"].append(file_path)
    
    print("\n📊 Worldbuilding Organization Analysis:")
    for category, files in organized.items():
        print(f"  {category}: {len(files)} files")
    
    return organized

def organize_npcs():
    """Step 27-28: Organize NPCs within 03_People"""
    print("\n👥 ORGANIZING NPCs (Steps 27-28)")
    people_dir = Path("03_People")
    
    categories = {
        "Major_NPCs": ["major", "important", "key", "main", "recurring"],
        "Minor_NPCs": ["minor", "background", "shopkeeper", "guard"],
        "Villains": ["villain", "antagonist", "enemy", "bbeg", "evil"],
        "Allies": ["ally", "friend", "companion", "helper"],
        "Factions_Leaders": ["leader", "chief", "king", "queen", "lord"]
    }
    
    organized = defaultdict(list)
    
    for file_path in people_dir.rglob("*.md"):
        if "Archive" in str(file_path):
            continue
            
        content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
        filename = file_path.name.lower()
        
        # Check for NPC markers
        if "npc" in filename or "character" in filename or re.search(r'race:|class:|level:', content):
            categorized = False
            for category, keywords in categories.items():
                if any(kw in filename or kw in content[:500] for kw in keywords):
                    organized[category].append(file_path)
                    categorized = True
                    break
            
            if not categorized:
                organized["General_NPCs"].append(file_path)
    
    print("\n📊 NPC Organization Analysis:")
    for category, files in organized.items():
        print(f"  {category}: {len(files)} files")
    
    return organized

def organize_resources():
    """Step 29-30: Organize resources within 04_Resources"""
    print("\n📦 ORGANIZING RESOURCES (Steps 29-30)")
    resources_dir = Path("04_Resources")
    
    categories = {
        "Maps": [".png", ".jpg", ".jpeg", ".svg", "map", "battlemap"],
        "Handouts": ["handout", "player handout", "document", "letter"],
        "Assets": ["asset", "token", "portrait", "art"],
        "Tables": ["table", "random", "generator", "roll"],
        "References": ["reference", "guide", "cheat sheet", "quick ref"]
    }
    
    organized = defaultdict(list)
    
    for file_path in resources_dir.rglob("*"):
        if file_path.is_file() and "Archive" not in str(file_path):
            filename = file_path.name.lower()
            ext = file_path.suffix.lower()
            
            categorized = False
            for category, keywords in categories.items():
                if any(kw in filename or kw == ext for kw in keywords):
                    organized[category].append(file_path)
                    categorized = True
                    break
            
            if not categorized:
                organized["General"].append(file_path)
    
    print("\n📊 Resources Organization Analysis:")
    for category, files in organized.items():
        print(f"  {category}: {len(files)} files")
        # Show file types
        extensions = defaultdict(int)
        for f in files:
            extensions[f.suffix] += 1
        if extensions:
            print(f"    File types: {dict(extensions)}")
    
    return organized

def create_organization_report(all_organized):
    """Create detailed organization report"""
    report_path = Path("09_Performance/organization_report_phase2.md")
    
    with open(report_path, 'w') as f:
        f.write("# Phase 2 Organization Report (Steps 21-30)\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        f.write("## Summary\n\n")
        f.write("Analyzed file organization within existing folders.\n")
        f.write("NO FILES WERE MOVED - Analysis only.\n\n")
        
        for section, organized in all_organized.items():
            f.write(f"## {section}\n\n")
            total_files = sum(len(files) for files in organized.values())
            f.write(f"Total files analyzed: {total_files}\n\n")
            
            for category, files in organized.items():
                f.write(f"### {category} ({len(files)} files)\n")
                if len(files) <= 10:
                    for file in files:
                        f.write(f"- {file.name}\n")
                else:
                    f.write(f"- [Too many to list - {len(files)} files]\n")
                f.write("\n")
    
    print(f"\n✓ Organization report created: {report_path}")
    return report_path

def main():
    print("=" * 60)
    print("PHASE 2: ORGANIZATION WITHIN FOLDERS (STEPS 21-30)")
    print("=" * 60)
    print("\n⚠️  This phase ANALYZES organization only")
    print("    No files will be moved without permission\n")
    
    # Create backup manifest
    backup_path = create_backup()
    
    # Analyze each major directory
    all_organized = {}
    
    # Steps 21-23: Adventures
    all_organized["Adventures"] = organize_adventures()
    
    # Steps 24-26: Worldbuilding
    all_organized["Worldbuilding"] = organize_worldbuilding()
    
    # Steps 27-28: NPCs
    all_organized["NPCs"] = organize_npcs()
    
    # Steps 29-30: Resources
    all_organized["Resources"] = organize_resources()
    
    # Create comprehensive report
    report_path = create_organization_report(all_organized)
    
    print("\n" + "=" * 60)
    print("PHASE 2 COMPLETE!")
    print("=" * 60)
    print("\n📊 Results Summary:")
    print(f"✓ Steps 21-30 complete")
    print(f"✓ Analyzed 4 major directories")
    print(f"✓ Created organization report: {report_path}")
    print(f"✓ Backup manifest: {backup_path}")
    print("\n⚠️  No files were moved - analysis only")
    print("    Review report for organization recommendations")
    
    return True

if __name__ == "__main__":
    main()