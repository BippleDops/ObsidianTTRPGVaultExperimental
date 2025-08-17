#!/usr/bin/env python3
"""
Comprehensive cleanup and Phase 1 Steps 31-60 deployment
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
import json
import hashlib
from typing import List, Dict

class VaultCleanupAndPhase1:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.cleanup_report = {
            "json_files_archived": [],
            "scripts_archived": [],
            "consistency_issues": [],
            "phase1_additions": []
        }
        
    def cleanup_json_files(self):
        """Consolidate and archive JSON files in vault root"""
        print("📦 Consolidating JSON files...")
        
        # Create archive directory
        archive_dir = self.vault_path / "08_Archive" / "json_backups"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all JSON files in root
        json_files = list(self.vault_path.glob("*.json"))
        
        if json_files:
            # Create archive
            archive_name = f"json_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            archive_path = archive_dir / archive_name
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for json_file in json_files:
                    zipf.write(json_file, json_file.name)
                    self.cleanup_report["json_files_archived"].append(json_file.name)
                    
            # Remove original files
            for json_file in json_files:
                json_file.unlink()
                
            print(f"   ✅ Archived {len(json_files)} JSON files to {archive_name}")
        else:
            print("   ℹ️ No JSON files in root to archive")
            
    def cleanup_old_scripts(self):
        """Archive outdated scripts"""
        print("\n📦 Cleaning up scripts...")
        
        scripts_dir = self.vault_path / "scripts"
        archive_dir = self.vault_path / "08_Archive" / "script_backups"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Identify outdated scripts (duplicates, test versions, etc.)
        outdated_patterns = [
            "*_backup*.py",
            "*_old*.py",
            "*_test*.py",
            "test_*.py",
            "*_temp*.py"
        ]
        
        scripts_to_archive = []
        for pattern in outdated_patterns:
            scripts_to_archive.extend(scripts_dir.glob(pattern))
            
        if scripts_to_archive:
            archive_name = f"scripts_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            archive_path = archive_dir / archive_name
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for script in scripts_to_archive:
                    zipf.write(script, script.name)
                    self.cleanup_report["scripts_archived"].append(script.name)
                    script.unlink()
                    
            print(f"   ✅ Archived {len(scripts_to_archive)} outdated scripts")
        else:
            print("   ℹ️ No outdated scripts to archive")
            
    def verify_vault_consistency(self):
        """Verify vault consistency file by file"""
        print("\n🔍 Verifying vault consistency...")
        
        issues = []
        checked = 0
        
        for md_file in self.vault_path.rglob("*.md"):
            if "08_Archive" in str(md_file):
                continue
                
            checked += 1
            
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Check for frontmatter
                if not content.startswith('---\n'):
                    issues.append(f"Missing frontmatter: {md_file.relative_to(self.vault_path)}")
                    
                # Check for broken image links
                if '![[' in content and '04_Resources/Assets' not in content:
                    broken_images = len([1 for line in content.split('\n') if '![[' in line and '04_Resources/Assets' not in line])
                    if broken_images > 0:
                        issues.append(f"Broken images ({broken_images}): {md_file.relative_to(self.vault_path)}")
                        
                # Progress indicator
                if checked % 100 == 0:
                    print(f"   Checked {checked} files...")
                    
            except Exception as e:
                issues.append(f"Error reading: {md_file.relative_to(self.vault_path)} - {e}")
                
        self.cleanup_report["consistency_issues"] = issues[:50]  # Keep first 50 issues
        
        print(f"   ✅ Checked {checked} files")
        print(f"   ⚠️ Found {len(issues)} consistency issues")
        
    def create_phase1_31_40(self):
        """Steps 31-40: Quick-access sidebars"""
        print("\n📝 Phase 1 Steps 31-40: Creating Quick Access Sidebars...")
        
        content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: sidebar
cssclass: quick-access
tags:
- navigation
- sidebar
- quick-access
---

# ⚡ Quick Access Panel

## 🎯 Frequent Actions

### DM Tools
- [[Dice Roller|🎲 Roll Dice]]
- [[Initiative Tracker|⚔️ Track Initiative]]
- [[Random NPC Generator|👤 Generate NPC]]
- [[Loot Generator|💰 Generate Loot]]
- [[Random Encounter|🐾 Random Encounter]]

### Session Tools
- [[Session Template|📝 New Session]]
- [[Session Recap|📋 Write Recap]]
- [[Session Timer|⏱️ Session Timer]]
- [[Player Notes|📓 Player Notes]]
- [[XP Calculator|📊 Calculate XP]]

### Quick References
- [[Conditions Reference|🤒 Conditions]]
- [[Spell List|✨ Spells]]
- [[Item Prices|💎 Items]]
- [[CR Calculator|⚖️ CR Calculator]]
- [[Travel Times|🗺️ Travel]]

## 📌 Pinned Content

```dataview
LIST
FROM ""
WHERE contains(tags, "pinned") OR contains(tags, "favorite")
SORT file.name ASC
```

## 🔥 Hot Keys

| Action | Shortcut | Description |
|--------|----------|-------------|
| Quick Search | `Cmd/Ctrl + O` | Open file |
| Command Palette | `Cmd/Ctrl + P` | Commands |
| Daily Note | `Cmd/Ctrl + D` | Today's note |
| Graph View | `Cmd/Ctrl + G` | Visual graph |
| Tag Search | `Cmd/Ctrl + T` | Find by tag |

## 🎲 Quick Rolls

### Standard Rolls
- `[[1d20]]` - Attack/Check
- `[[2d20kh1]]` - Advantage
- `[[2d20kl1]]` - Disadvantage
- `[[1d100]]` - Percentile

### Damage Rolls
- `[[1d6]]` - Light weapon
- `[[1d8]]` - Medium weapon
- `[[2d6]]` - Greatsword
- `[[8d6]]` - Fireball

## 📍 Jump Points

### Campaigns
```dataview
LIST
FROM "01_Adventures"
WHERE type = "campaign" AND status = "active"
LIMIT 3
```

### Current NPCs
```dataview
LIST
FROM "02_Worldbuilding/People"
WHERE contains(tags, "current") OR contains(tags, "active")
LIMIT 5
```

### Active Locations
```dataview
LIST
FROM "02_Worldbuilding/Places"
WHERE contains(tags, "current") OR last-visited = date(today)
LIMIT 5
```

---
*Quick access sidebar for rapid navigation*
"""
        
        sidebar_path = self.vault_path / "00_Indexes" / "Quick_Access_Sidebar.md"
        sidebar_path.write_text(content, encoding='utf-8')
        self.cleanup_report["phase1_additions"].append(str(sidebar_path))
        print(f"   ✅ Created Quick Access Sidebar")
        
    def create_phase1_41_50(self):
        """Steps 41-50: Tag-based navigation"""
        print("\n📝 Phase 1 Steps 41-50: Creating Tag Navigation System...")
        
        content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: navigation
cssclass: tag-hierarchy
tags:
- navigation
- tags
- hierarchy
---

# 🏷️ Tag Navigation System

## 📊 Tag Hierarchy

### World Tags
- `#world/aquabyssos` - Underwater realm content
- `#world/aethermoor` - Sky realm content
- `#world/both` - Cross-realm content
- `#world/material` - Material plane
- `#world/planar` - Other planes

### Content Type Tags
- `#type/npc` - Non-player characters
- `#type/location` - Places and locations
- `#type/item` - Items and equipment
- `#type/quest` - Quests and objectives
- `#type/session` - Game sessions
- `#type/lore` - World lore

### Status Tags
- `#status/active` - Currently in use
- `#status/draft` - Work in progress
- `#status/complete` - Finished content
- `#status/archived` - Old/unused content
- `#status/idea` - Future possibilities

### Gameplay Tags
- `#combat` - Combat encounters
- `#social` - Social interactions
- `#exploration` - Exploration content
- `#puzzle` - Puzzles and riddles
- `#stealth` - Stealth missions

## 🔍 Tag Search Queries

### Find by Single Tag
```dataview
TABLE WITHOUT ID
  file.link as Content,
  file.folder as Location
FROM #combat
LIMIT 10
```

### Find by Multiple Tags
```dataview
TABLE WITHOUT ID
  file.link as Content,
  tags as Tags
FROM #npc AND #aquabyssos
LIMIT 10
```

### Tag Combinations
```dataview
TABLE WITHOUT ID
  file.link as Content,
  status as Status
FROM (#quest OR #adventure) AND #active
```

## 📈 Tag Statistics

```dataview
TABLE WITHOUT ID
  tag as Tag,
  length(rows) as "Usage Count"
FROM ""
FLATTEN tags as tag
WHERE tag != null
GROUP BY tag
SORT length(rows) DESC
LIMIT 20
```

## 🎯 Smart Tag Groups

### Campaign Tags
```dataview
LIST
FROM #campaign OR #seven-shards OR #shadow-conspiracy
GROUP BY file.folder
```

### Faction Tags
```dataview
LIST
FROM #faction OR #guild OR #organization
GROUP BY tags
```

### Danger Level Tags
```dataview
TABLE WITHOUT ID
  file.link as Content,
  danger-level as "Danger"
FROM #dangerous OR #deadly OR #safe
SORT danger-level DESC
```

## 🔧 Tag Management

### Recently Tagged
```dataview
TABLE WITHOUT ID
  file.link as Content,
  file.tags as Tags,
  file.mtime as Modified
FROM ""
WHERE file.mtime >= date(today) - dur(3 days) AND tags != null
SORT file.mtime DESC
LIMIT 10
```

### Untagged Content
```dataview
LIST
FROM ""
WHERE !tags OR tags = null
LIMIT 20
```

---
*Tag-based navigation powered by Dataview*
"""
        
        tag_path = self.vault_path / "00_Indexes" / "Tag_Navigation.md"
        tag_path.write_text(content, encoding='utf-8')
        self.cleanup_report["phase1_additions"].append(str(tag_path))
        print(f"   ✅ Created Tag Navigation System")
        
    def create_phase1_51_60(self):
        """Steps 51-60: Session-based navigation for DMs"""
        print("\n📝 Phase 1 Steps 51-60: Creating DM Session Navigator...")
        
        content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: dm-tool
cssclass: session-navigator
tags:
- dm-tool
- session
- navigation
---

# 🎭 DM Session Navigator

## 📅 Session Timeline

### Next Session
```dataview
TABLE WITHOUT ID
  file.link as Session,
  campaign as Campaign,
  date as Date,
  prep-status as "Prep Status"
FROM "01_Adventures"
WHERE type = "session" AND date >= date(today)
SORT date ASC
LIMIT 1
```

### Session History
```dataview
TABLE WITHOUT ID
  file.link as Session,
  date as Date,
  players as Players,
  xp-awarded as XP
FROM "01_Adventures"
WHERE type = "session" AND status = "completed"
SORT date DESC
LIMIT 5
```

## 🎯 Session Prep Checklist

### Pre-Session
- [ ] Review last session notes
- [ ] Update NPC stats/motivations
- [ ] Prepare encounter maps
- [ ] Queue music playlists
- [ ] Print player handouts
- [ ] Review player backstories
- [ ] Set up initiative tracker
- [ ] Prepare random tables

### Required NPCs
```dataview
TABLE WITHOUT ID
  file.link as NPC,
  faction as Faction,
  location as Location,
  stat-block as "Stats Ready?"
FROM "02_Worldbuilding/People"
WHERE session-appearance = this.file.name OR contains(tags, "next-session")
```

### Required Locations
```dataview
TABLE WITHOUT ID
  file.link as Location,
  type as Type,
  map as "Map Ready?",
  description as "Description"
FROM "02_Worldbuilding/Places"
WHERE session-appearance = this.file.name OR contains(tags, "next-session")
```

## 📊 Session Metrics

### Player Attendance
```dataview
TABLE WITHOUT ID
  player as Player,
  length(rows) as "Sessions Attended",
  last-session as "Last Seen"
FROM "01_Adventures"
WHERE type = "session" AND players
FLATTEN players as player
GROUP BY player
```

### Session Pacing
```dataview
TABLE WITHOUT ID
  file.link as Session,
  combat-time as "Combat %",
  rp-time as "RP %",
  exploration-time as "Exploration %"
FROM "01_Adventures"
WHERE type = "session" AND status = "completed"
SORT date DESC
LIMIT 5
```

## 🎲 Quick Session Tools

### Random Generators
- [[Random NPC|👤 Quick NPC]]
- [[Random Shop|🏪 Shop Inventory]]
- [[Random Tavern|🍺 Tavern Generator]]
- [[Random Encounter|⚔️ Encounter]]
- [[Random Loot|💰 Treasure]]

### Combat Tools
- [[Initiative Tracker|📋 Initiative]]
- [[HP Tracker|❤️ Hit Points]]
- [[Condition Tracker|🤒 Conditions]]
- [[Spell Slot Tracker|✨ Spell Slots]]

### Reference Sheets
- [[DC Guidelines|🎯 Difficulty Classes]]
- [[XP Thresholds|📊 Experience]]
- [[Encounter Builder|⚖️ Balance]]
- [[Travel Pace|🗺️ Movement]]

## 📝 Session Notes Template

```markdown
# Session [Number]: [Title]
Date: [Date]
Players: [List]
Level: [X]

## Recap
[Previous session summary]

## Events
[What happened]

## NPCs Met
- [NPC]: [Interaction]

## Locations Visited
- [Location]: [Events]

## Combat
- [Encounter]: [Outcome]

## Loot
- [Items found]

## XP Awarded
[Amount and reason]

## Notes for Next Session
[Hooks and reminders]
```

## 🔮 Upcoming Plot Points

```dataview
LIST
FROM ""
WHERE contains(tags, "plot-point") AND status = "pending"
SORT priority DESC
```

---
*DM session navigation and management toolkit*
"""
        
        dm_path = self.vault_path / "00_Indexes" / "DM_Session_Navigator.md"
        dm_path.write_text(content, encoding='utf-8')
        self.cleanup_report["phase1_additions"].append(str(dm_path))
        print(f"   ✅ Created DM Session Navigator")
        
    def generate_cleanup_report(self):
        """Generate comprehensive cleanup report"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "cleanup": {
                "json_files_archived": self.cleanup_report["json_files_archived"],
                "scripts_archived": self.cleanup_report["scripts_archived"],
                "consistency_issues": self.cleanup_report["consistency_issues"][:20]  # First 20 issues
            },
            "phase1_progress": {
                "steps_completed": "1-60",
                "percentage": "60%",
                "files_created": self.cleanup_report["phase1_additions"]
            }
        }
        
        report_path = self.vault_path / "reports" / f"cleanup_phase1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report_path
        
    def run_all_tasks(self):
        """Execute all cleanup and Phase 1 tasks"""
        print("="*60)
        print("🚀 COMPREHENSIVE CLEANUP & PHASE 1 CONTINUATION")
        print("="*60)
        
        # Cleanup tasks
        self.cleanup_json_files()
        self.cleanup_old_scripts()
        self.verify_vault_consistency()
        
        # Phase 1 continuation
        self.create_phase1_31_40()
        self.create_phase1_41_50()
        self.create_phase1_51_60()
        
        # Generate report
        report_path = self.generate_cleanup_report()
        
        print("\n" + "="*60)
        print("✅ ALL TASKS COMPLETE!")
        print("="*60)
        
        print(f"\n📊 Summary:")
        print(f"  • JSON files archived: {len(self.cleanup_report['json_files_archived'])}")
        print(f"  • Scripts archived: {len(self.cleanup_report['scripts_archived'])}")
        print(f"  • Consistency issues found: {len(self.cleanup_report['consistency_issues'])}")
        print(f"  • Phase 1 files created: {len(self.cleanup_report['phase1_additions'])}")
        print(f"\n📄 Full report: {report_path.name}")
        
        print(f"\n🎯 Phase 1 Progress: 60% Complete (Steps 1-60 of 100)")
        print(f"\n💡 Next Steps:")
        print(f"  • Steps 61-70: Player-specific content views")
        print(f"  • Steps 71-80: Search shortcuts and saved queries")
        print(f"  • Steps 81-90: Bookmark collections by campaign")
        print(f"  • Steps 91-100: Mobile-optimized navigation")

def main():
    cleaner = VaultCleanupAndPhase1()
    cleaner.run_all_tasks()

if __name__ == "__main__":
    main()