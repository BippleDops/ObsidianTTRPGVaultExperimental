#!/usr/bin/env python3
"""
Analyze vault structure against Obsidian TTRPG best practices.
Identifies naming issues and suggests tag-based organization.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

class VaultStructureAnalyzer:
    def __init__(self, vault_root: Path):
        self.vault_root = Path(vault_root)
        self.issues = defaultdict(list)
        self.recommendations = defaultdict(list)
        
    def analyze_folder(self, folder_path: Path, folder_name: str):
        """Analyze a specific folder for structure issues."""
        print(f"\n=== Analyzing {folder_name} ===")
        
        if folder_name == "03_People":
            self.analyze_people_folder(folder_path)
        elif folder_name == "01_Adventures":
            self.analyze_adventures_folder(folder_path)
        elif folder_name == "02_Worldbuilding":
            self.analyze_worldbuilding_folder(folder_path)
        elif folder_name == "05_Rules":
            self.analyze_rules_folder(folder_path)
        elif folder_name == "06_Sessions":
            self.analyze_sessions_folder(folder_path)
        elif folder_name == "04_Resources":
            self.analyze_resources_folder(folder_path)
            
    def analyze_people_folder(self, folder_path: Path):
        """Analyze the People folder structure."""
        npc_files = list(folder_path.glob("NPC*.md"))
        non_npc_files = [f for f in folder_path.glob("*.md") if not f.name.startswith("NPC")]
        
        # Issue: NPC prefix in filename instead of tags
        if npc_files:
            self.issues["03_People"].append({
                "type": "naming_convention",
                "description": f"{len(npc_files)} files use 'NPC' prefix in filename",
                "recommendation": "Use character names as filenames, add 'npc' tag in frontmatter",
                "example": "NPC00407_Hestara_Dawnstrider.md → Hestara Dawnstrider.md with tags: [npc, warrior, ally]"
            })
            
        # Check for faction files mixed with NPCs
        faction_files = [f for f in folder_path.rglob("*.md") if "Factions" in str(f)]
        if faction_files:
            self.recommendations["03_People"].append({
                "structure": "Good - Factions separated in subfolder",
                "count": len(faction_files)
            })
            
        # Check for proper categorization
        print(f"  NPCs with prefix: {len(npc_files)}")
        print(f"  NPCs without prefix: {len(non_npc_files)}")
        print(f"  Faction files: {len(faction_files)}")
        
    def analyze_adventures_folder(self, folder_path: Path):
        """Analyze the Adventures folder structure."""
        quest_files = list((folder_path / "quests").glob("QUEST*.md") if (folder_path / "quests").exists() else [])
        quest_natural = list((folder_path / "quests").glob("Quest*.md") if (folder_path / "quests").exists() else [])
        
        # Issue: QUEST prefix with numbers
        if quest_files:
            self.issues["01_Adventures"].append({
                "type": "naming_convention", 
                "description": f"{len(quest_files)} files use 'QUEST####' prefix",
                "recommendation": "Use descriptive quest names, add quest type/status in tags",
                "example": "QUEST00108_Main_Quest_109.md → The Void Conspiracy.md with tags: [quest, main-quest, active]"
            })
            
        # Check Campaigns folder
        campaigns_path = folder_path / "Campaigns"
        if campaigns_path.exists():
            campaign_files = list(campaigns_path.glob("*.md"))
            
            # Look for duplicate numbered files
            duplicates = [f for f in campaign_files if " 2.md" in f.name or " 3.md" in f.name]
            if duplicates:
                self.issues["01_Adventures"].append({
                    "type": "duplicate_files",
                    "description": f"{len(duplicates)} duplicate files with ' 2' or ' 3' suffix",
                    "recommendation": "Merge duplicate content or use version control",
                    "files": [f.name for f in duplicates[:5]]
                })
                
        print(f"  Quest files with QUEST prefix: {len(quest_files)}")
        print(f"  Quest files with natural names: {len(quest_natural)}")
        
    def analyze_worldbuilding_folder(self, folder_path: Path):
        """Analyze the Worldbuilding folder structure."""
        all_files = list(folder_path.rglob("*.md"))
        
        # Check for files that should be in other folders
        npc_like = [f for f in all_files if any(title in f.name for title in 
                    ["Captain", "Admiral", "Lord", "Lady", "Master", "Brother", "Sister"])]
        
        if npc_like:
            self.issues["02_Worldbuilding"].append({
                "type": "misplaced_content",
                "description": f"{len(npc_like)} files appear to be NPCs in Worldbuilding",
                "recommendation": "Move character files to 03_People, keep only location/lore here",
                "examples": [f.name for f in npc_like[:5]]
            })
            
        # Check for proper location structure
        location_keywords = ["City", "Town", "Village", "District", "Palace", "Tower", "Temple"]
        locations = [f for f in all_files if any(kw in f.name for kw in location_keywords)]
        
        print(f"  Total worldbuilding files: {len(all_files)}")
        print(f"  Likely NPC files: {len(npc_like)}")
        print(f"  Location files: {len(locations)}")
        
    def analyze_rules_folder(self, folder_path: Path):
        """Analyze the Rules folder structure."""
        all_files = list(folder_path.rglob("*.md"))
        
        # Check for D&D reference files
        dnd_refs = [f for f in all_files if "xphb" in f.name.lower() or "phb" in f.name.lower()]
        spell_files = [f for f in all_files if f.name.endswith("Xphb.md")]
        
        if spell_files:
            self.issues["05_Rules"].append({
                "type": "naming_convention",
                "description": f"{len(spell_files)} spell files with 'Xphb' suffix",
                "recommendation": "Use spell name only, add source in tags/frontmatter",
                "example": "Acid Splash Xphb.md → Acid Splash.md with tags: [spell, cantrip, xphb]"
            })
            
        # Check for monster stats vs rules
        stat_blocks = [f for f in all_files if "stat" in f.name.lower() or "creature" in f.name.lower()]
        
        print(f"  Total rules files: {len(all_files)}")
        print(f"  D&D reference files: {len(dnd_refs)}")
        print(f"  Spell files: {len(spell_files)}")
        
    def analyze_sessions_folder(self, folder_path: Path):
        """Analyze the Sessions folder structure."""
        session_files = list(folder_path.glob("Session*.md"))
        daily_notes = list((folder_path / "Daily_Notes").glob("*.md") if (folder_path / "Daily_Notes").exists() else [])
        
        # Check for proper session naming
        numbered_sessions = [f for f in session_files if re.match(r"Session_\d+", f.name)]
        
        if numbered_sessions:
            self.recommendations["06_Sessions"].append({
                "structure": "Good - Using numbered session format",
                "count": len(numbered_sessions)
            })
            
        print(f"  Session files: {len(session_files)}")
        print(f"  Daily notes: {len(daily_notes)}")
        
    def analyze_resources_folder(self, folder_path: Path):
        """Analyze the Resources folder structure."""
        all_files = list(folder_path.rglob("*"))
        
        # Check for proper asset organization
        images = [f for f in all_files if f.suffix in [".png", ".jpg", ".jpeg", ".svg"]]
        markdown_assets = [f for f in all_files if f.suffix == ".md" and "Asset" in f.name]
        
        # Issue: Markdown files for images
        image_md_files = [f for f in all_files if f.name.endswith(".png.md") or f.name.endswith(".svg.md")]
        if image_md_files:
            self.issues["04_Resources"].append({
                "type": "incorrect_file_type",
                "description": f"{len(image_md_files)} markdown files for images",
                "recommendation": "Remove .md files for images, use direct image embedding",
                "examples": [f.name for f in image_md_files[:5]]
            })
            
        print(f"  Image files: {len(images)}")
        print(f"  Asset markdown files: {len(markdown_assets)}")
        
    def generate_recommendations(self):
        """Generate overall recommendations based on analysis."""
        recommendations = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": []
        }
        
        # Critical: File naming preventing proper Obsidian features
        if self.issues.get("03_People"):
            recommendations["CRITICAL"].append({
                "folder": "03_People",
                "action": "Remove NPC prefix from 2089 files",
                "reason": "Prefixes prevent natural wiki-linking and search",
                "solution": "Rename to character names, use tags for categorization"
            })
            
        if self.issues.get("01_Adventures"):
            recommendations["HIGH"].append({
                "folder": "01_Adventures/quests",
                "action": "Remove QUEST#### prefix from 197 files",
                "reason": "Numeric prefixes make quests hard to reference",
                "solution": "Use descriptive names, track quest IDs in frontmatter"
            })
            
        if self.issues.get("02_Worldbuilding"):
            recommendations["MEDIUM"].append({
                "folder": "02_Worldbuilding",
                "action": "Move NPC files to 03_People",
                "reason": "Characters mixed with locations breaks organization",
                "solution": "Separate people from places for better navigation"
            })
            
        return recommendations
        
    def run_analysis(self):
        """Run complete vault analysis."""
        folders = [
            "03_People",
            "01_Adventures", 
            "02_Worldbuilding",
            "05_Rules",
            "06_Sessions",
            "04_Resources"
        ]
        
        for folder_name in folders:
            folder_path = self.vault_root / folder_name
            if folder_path.exists():
                self.analyze_folder(folder_path, folder_name)
                
        # Generate and display recommendations
        recommendations = self.generate_recommendations()
        
        print("\n" + "="*60)
        print("VAULT STRUCTURE ANALYSIS SUMMARY")
        print("="*60)
        
        for priority, items in recommendations.items():
            if items:
                print(f"\n{priority} PRIORITY:")
                for item in items:
                    print(f"  📁 {item['folder']}")
                    print(f"     Action: {item['action']}")
                    print(f"     Reason: {item['reason']}")
                    print(f"     Solution: {item['solution']}")
                    
        # Save detailed report
        report = {
            "issues": dict(self.issues),
            "recommendations": dict(self.recommendations),
            "priorities": recommendations
        }
        
        report_path = self.vault_root / "09_Performance" / "vault_structure_analysis.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        print(f"\nDetailed report saved to: {report_path}")
        
        return recommendations

def main():
    vault_root = Path.cwd()
    
    print("=== OBSIDIAN TTRPG VAULT STRUCTURE ANALYZER ===")
    print(f"Analyzing: {vault_root}")
    print("Checking against Obsidian best practices for TTRPG vaults...")
    
    analyzer = VaultStructureAnalyzer(vault_root)
    analyzer.run_analysis()

if __name__ == "__main__":
    main()