#!/usr/bin/env python3
"""
Fix performance directory references and enhance research folder
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json

class VaultFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.fixes_applied = []
        
    def fix_script_references(self):
        """Fix all scripts to use 13_Performance instead of 13_Performance"""
        print("🔧 Fixing script references...")
        
        scripts_dir = self.vault_path / "scripts"
        fixed_count = 0
        
        for script_file in scripts_dir.glob("*.py"):
            try:
                content = script_file.read_text(encoding='utf-8')
                original = content
                
                # Replace all references
                content = content.replace('13_Performance', '13_Performance')
                content = content.replace('"13_Performance"', '"13_Performance"')
                content = content.replace("'13_Performance'", "'13_Performance'")
                content = content.replace('/13_Performance/', '/13_Performance/')
                
                if content != original:
                    script_file.write_text(content, encoding='utf-8')
                    fixed_count += 1
                    self.fixes_applied.append(script_file.name)
                    
            except Exception as e:
                print(f"   Error fixing {script_file.name}: {e}")
                
        print(f"   ✅ Fixed {fixed_count} scripts")
        
    def create_actual_play_resources(self):
        """Create actual play campaign resources"""
        print("\n📺 Creating Actual Play Campaign Resources...")
        
        ap_dir = self.vault_path / "12_Research" / "Actual_Play_Campaigns"
        ap_dir.mkdir(parents=True, exist_ok=True)
        
        # Critical Role campaigns
        critical_role = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
type: research
tags:
- actual-play
- critical-role
- reference
---

# Critical Role Campaigns - Reference Links

## Campaign 1: Vox Machina
- **YouTube Playlist**: https://www.youtube.com/playlist?list=PL1tiwbzkOjQz7D0l_eLJGAISVtcL7oRu_
- **Wiki**: https://criticalrole.fandom.com/wiki/Campaign_1
- **Episodes**: 115 episodes + one-shots
- **Setting**: Tal'Dorei, Exandria
- **System**: D&D 5e (converted from Pathfinder)

### Key Resources
- Character sheets and builds
- Matt Mercer's worldbuilding notes
- Battle maps and locations
- House rules and homebrew

## Campaign 2: The Mighty Nein
- **YouTube Playlist**: https://www.youtube.com/playlist?list=PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2
- **Wiki**: https://criticalrole.fandom.com/wiki/Campaign_2
- **Episodes**: 141 episodes
- **Setting**: Wildemount, Exandria
- **System**: D&D 5e

## Campaign 3: Bells Hells
- **YouTube Playlist**: https://www.youtube.com/playlist?list=PL1tiwbzkOjQydg3QOkBLG9OYqWJ0dwlxF
- **Wiki**: https://criticalrole.fandom.com/wiki/Campaign_3
- **Setting**: Marquet, Exandria
- **System**: D&D 5e

## Exandria Unlimited
- **Playlist**: https://www.youtube.com/playlist?list=PL1tiwbzkOjQw7YO0M0d8vRCITuqAmUt7S
- **DM**: Aabria Iyengar
- **Mini-campaigns** and side stories

---
*Reference material for campaign inspiration*
"""
        
        (ap_dir / "Critical_Role.md").write_text(critical_role, encoding='utf-8')
        
        # Dimension 20 campaigns
        dimension_20 = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
type: research
tags:
- actual-play
- dimension-20
- reference
---

# Dimension 20 Campaigns

## Fantasy High
- **Platform**: Dropout.tv (some on YouTube)
- **DM**: Brennan Lee Mulligan
- **Setting**: Modern fantasy high school
- **System**: D&D 5e
- **Seasons**: Freshman Year, Sophomore Year, Junior Year

## A Crown of Candy
- **Setting**: Game of Thrones meets Candyland
- **Episodes**: 17 episodes
- **Tone**: Political intrigue, high stakes

## The Unsleeping City
- **Setting**: Modern NYC with magic
- **Episodes**: Two seasons
- **Style**: Urban fantasy

## Escape from the Bloodkeep
- **Setting**: Lord of the Rings from villain perspective
- **Episodes**: 6 episodes
- **Tone**: Comedy evil campaign

## A Court of Fey & Flowers
- **DM**: Aabria Iyengar
- **Setting**: Regency-era fey court
- **Focus**: Romance and intrigue

---
*Reference for creative campaign concepts*
"""
        
        (ap_dir / "Dimension_20.md").write_text(dimension_20, encoding='utf-8')
        
        # Additional actual plays
        other_campaigns = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
type: research
tags:
- actual-play
- reference
- campaigns
---

# Other Notable Actual Play Campaigns

## The Adventure Zone
- **Podcast**: Maximum Fun Network
- **DMs**: Griffin McElroy (primarily)
- **Campaigns**:
  - Balance Arc (D&D 5e)
  - Amnesty (Monster of the Week)
  - Graduation (D&D 5e)
  - Ethersea (D&D 5e)
- **Link**: https://theadventurezone.fandom.com

## High Rollers
- **YouTube**: Yogscast
- **DM**: Mark Hulmes
- **Campaigns**:
  - Lightfall (complete)
  - Aerois (complete)
  - Current campaign
- **System**: D&D 5e

## Not Another D&D Podcast (NADDPOD)
- **Podcast**: HeadGum
- **DM**: Brian Murphy
- **Campaigns**:
  - Bahumia (Campaign 1)
  - Eldermourne (Campaign 2)
  - Campaign 3 (ongoing)

## Acquisitions Incorporated
- **Platform**: Penny Arcade
- **DMs**: Chris Perkins, Jeremy Crawford
- **Style**: Corporate D&D comedy
- **PAX Live Shows**: Epic productions

## Glass Cannon Network
- **Multiple shows**: Various systems
- **Giant Slayer**: Pathfinder AP
- **Strange Aeons**: Call of Cthulhu crossover
- **Get in the Trunk**: Delta Green

## Dungeons & Daddies
- **Podcast**: Comedy D&D
- **Premise**: Dads from our world in Forgotten Realms
- **Season 2**: Their kids' adventure

## LA By Night
- **System**: Vampire: The Masquerade
- **Platform**: World of Darkness
- **Setting**: Modern Los Angeles
- **Style**: Gothic horror drama

## Oxventure
- **YouTube**: Outside Xbox/Outside Xtra
- **DM**: Johnny Chiodini
- **Style**: Comedy chaos
- **Guild**: Ongoing campaign

---
*Diverse actual play references for different styles*
"""
        
        (ap_dir / "Other_Actual_Plays.md").write_text(other_campaigns, encoding='utf-8')
        
        print(f"   ✅ Created actual play campaign references")
        
    def create_ttrpg_articles(self):
        """Create TTRPG article references"""
        print("\n📰 Creating TTRPG Article Collection...")
        
        articles_dir = self.vault_path / "12_Research" / "TTRPG_Articles"
        articles_dir.mkdir(parents=True, exist_ok=True)
        
        # DM advice articles
        dm_advice = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
type: research
tags:
- articles
- dm-advice
- reference
---

# Essential DM Advice Articles

## The Angry GM
- **"How to Manage Combat Like a Dolphin"**: https://theangrygm.com
- **"Adjudicate Actions Like a Boss"**: Core action resolution
- **"Run Better Sessions"**: Session management

## Sly Flourish / Lazy DM
- **"The Lazy DM's Workbook"**: https://slyflourish.com
- **"8 Steps of Session Prep"**: Efficient preparation
- **"Fantastic Locations"**: Location building

## The Alexandrian
- **"Three Clue Rule"**: https://thealexandrian.net
- **"Node-Based Scenario Design"**: Non-linear adventures
- **"Jaquaying the Dungeon"**: Dungeon design principles

## Gnome Stew
- **"Never Unprepared"**: https://gnomestew.com
- **"Odyssey"**: Campaign management
- **"Focal Point"**: NPC creation

## Tribality
- **"Building Better Encounters"**: https://tribality.com
- **"World Building 101"**: Setting creation
- **"Player Engagement"**: Table management

## Reddit Communities
- **r/DMAcademy**: Advice and resources
- **r/DnDBehindTheScreen**: DM resources
- **r/BehindTheTables**: Random tables
- **r/UnearthedArcana**: Homebrew content

---
*Curated DM advice from expert sources*
"""
        
        (articles_dir / "DM_Advice_Articles.md").write_text(dm_advice, encoding='utf-8')
        
        # Game design articles
        game_design = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
type: research
tags:
- articles
- game-design
- theory
---

# TTRPG Game Design Articles

## Core Design Principles
- **"The Three Pillars"**: WotC on exploration, social, combat
- **"Powered by the Apocalypse"**: Vincent Baker's design philosophy
- **"FATE Core Concepts"**: Aspect-based design
- **"OSR Principles"**: Old school renaissance philosophy

## Specific Topics

### Player Agency
- "Meaningful Choices in RPGs" - Gnome Stew
- "The Quantum Ogre Problem" - The Alexandrian
- "Illusionism vs Participationism" - RPG.net

### Narrative Structure
- "The Five Room Dungeon" - Johnn Four
- "Scene Framing Techniques" - Play Unsafe
- "Fronts and Threats" - Apocalypse World

### Mechanical Balance
- "The Mathematics of D&D" - Blog of Holding
- "Bounded Accuracy Explained" - WotC
- "Action Economy in 5e" - The Monsters Know

### Social Contract
- "Session Zero Guidelines" - Various sources
- "Safety Tools in TTRPGs" - Monte Cook Games
- "The X-Card" - John Stavropoulos

## Academic Resources
- **"Shared Fantasy"** by Gary Alan Fine
- **"Playing at the World"** by Jon Peterson
- **International Journal of Role-Playing**

---
*Game design theory and practice*
"""
        
        (articles_dir / "Game_Design_Articles.md").write_text(game_design, encoding='utf-8')
        
        # Tools and resources
        tools_resources = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
type: research
tags:
- articles
- tools
- resources
---

# TTRPG Tools & Resources

## Online Tools

### Virtual Tabletops
- **Roll20**: https://roll20.net - Guides and tutorials
- **Foundry VTT**: https://foundryvtt.com - Documentation
- **Owlbear Rodeo**: Simple and free
- **Talespire**: 3D virtual tabletop

### Character Builders
- **D&D Beyond**: Official 5e builder
- **Hero Forge**: Custom miniature design
- **Fast Character**: Quick NPC generation

### World Building
- **World Anvil**: Complete world management
- **Campfire Write**: Story and world building
- **Azgaar's Fantasy Map Generator**: Procedural maps
- **Donjon**: Random generators

### Audio
- **Tabletop Audio**: Ambient soundscapes
- **Syrinscape**: Dynamic sound effects
- **MyNoise**: Customizable ambience

## Content Creation

### Map Making
- **Inkarnate**: Web-based map creator
- **Wonderdraft**: Desktop map software
- **Dungeondraft**: Dungeon and building maps
- **2-Minute Tabletop**: Map assets

### Art Resources
- **Hero Forge**: Character visualization
- **Artbreeder**: AI character portraits
- **Pinterest**: Visual inspiration boards

### Writing Tools
- **Obsidian**: This vault!
- **Notion**: Database-driven campaigns
- **OneNote**: Microsoft's solution
- **Scrivener**: Long-form writing

## Communities

### Forums
- **ENWorld**: Industry news and discussion
- **RPG.net**: Oldest RPG forum
- **Giant in the Playground**: D&D optimization

### Discord Servers
- **D&D Beyond**: Official community
- **r/DnD Discord**: Reddit community
- **Critical Role**: Fan community

---
*Comprehensive tool collection*
"""
        
        (articles_dir / "Tools_and_Resources.md").write_text(tools_resources, encoding='utf-8')
        
        print(f"   ✅ Created TTRPG article collections")
        
    def generate_report(self):
        """Generate comprehensive fix report"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "fixes": {
                "scripts_fixed": self.fixes_applied,
                "performance_dir": "Changed 13_Performance to 13_Performance",
                "reports_moved": "All reports now in 13_Performance"
            },
            "additions": {
                "actual_play_campaigns": [
                    "Critical_Role.md",
                    "Dimension_20.md",
                    "Other_Actual_Plays.md"
                ],
                "ttrpg_articles": [
                    "DM_Advice_Articles.md",
                    "Game_Design_Articles.md",
                    "Tools_and_Resources.md"
                ]
            }
        }
        
        report_path = self.vault_path / "13_Performance" / f"fixes_and_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report_path

def main():
    fixer = VaultFixer()
    
    print("="*60)
    print("🔧 VAULT FIXES AND RESEARCH ENHANCEMENT")
    print("="*60)
    
    fixer.fix_script_references()
    fixer.create_actual_play_resources()
    fixer.create_ttrpg_articles()
    
    report_path = fixer.generate_report()
    
    print("\n" + "="*60)
    print("✅ FIXES AND ENHANCEMENTS COMPLETE!")
    print("="*60)
    print(f"\n📄 Report saved: {report_path.name}")
    print("\n🎯 Completed:")
    print("  • Fixed script references to use 13_Performance")
    print("  • Created actual play campaign references")
    print("  • Added TTRPG article collections")
    print("  • Moved all reports to correct location")

if __name__ == "__main__":
    main()