#!/usr/bin/env python3
"""
Phase 1 Steps 1-30: Dynamic Navigation System
Creates auto-updating index pages for the vault
"""

from pathlib import Path
from datetime import datetime
import json

class Phase1Navigation:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.created_files = []
        
    def step_1_10_dynamic_hub(self):
        """Steps 1-10: Create main navigation hub"""
        print("📝 Steps 1-10: Creating Dynamic Navigation Hub...")
        
        content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: index
cssclass: navigation-hub
tags:
- index
- navigation
- dynamic
---

# 🗺️ Vault Navigation Hub

> *This page auto-updates to show current vault contents using Dataview queries*

## 📊 Vault Overview

### Content by Category
<!-- Dataview query to show content organized by folder -->
```dataview
TABLE WITHOUT ID
  file.folder as "📁 Category",
  length(rows) as "📄 Files"
FROM ""
WHERE file.name != this.file.name
GROUP BY file.folder
SORT length(rows) DESC
```

## 🎯 Quick Access

### Recent Sessions
```dataview
TABLE WITHOUT ID
  file.link as Session,
  campaign as Campaign,
  date as Date
FROM "01_Adventures"
WHERE type = "session" OR contains(tags, "session")
SORT file.mtime DESC
LIMIT 5
```

### Active NPCs
```dataview
TABLE WITHOUT ID
  file.link as NPC,
  faction as Faction,
  location as Location
FROM "02_Worldbuilding/People"
WHERE type = "npc" OR contains(tags, "npc")
SORT file.mtime DESC
LIMIT 10
```

### Key Locations
```dataview
TABLE WITHOUT ID
  file.link as Location,
  world as Realm,
  type as Type
FROM "02_Worldbuilding/Places"
WHERE type = "location" OR contains(tags, "location")
SORT file.mtime DESC
LIMIT 10
```

## 🔥 Recently Modified

```dataview
TABLE WITHOUT ID
  file.link as Content,
  file.folder as Category,
  file.mtime as "Last Modified"
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 15
```

## 🏷️ Popular Tags

```dataview
LIST
FROM ""
FLATTEN tags as tag
GROUP BY tag
SORT length(rows) DESC
LIMIT 20
```

## 🔍 Smart Searches

### By Status
- `status:active` - [[Active Content]]
- `status:draft` - [[Draft Content]]
- `status:complete` - [[Completed Content]]

### By World
- `world:Aquabyssos` - [[Aquabyssos Content]]
- `world:Aethermoor` - [[Aethermoor Content]]

### By Type
- `type:npc` - [[All NPCs]]
- `type:location` - [[All Locations]]
- `type:quest` - [[All Quests]]
- `type:session` - [[All Sessions]]

---
*Navigation hub powered by Dataview - automatically updates with vault changes*
"""
        
        hub_path = self.vault_path / "00_Indexes" / "Navigation_Hub.md"
        hub_path.parent.mkdir(exist_ok=True)
        hub_path.write_text(content, encoding='utf-8')
        self.created_files.append(str(hub_path))
        print(f"   ✅ Created: {hub_path.name}")
        
    def step_11_20_campaign_center(self):
        """Steps 11-20: Create campaign command center"""
        print("\n📝 Steps 11-20: Creating Campaign Command Center...")
        
        content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: index
cssclass: campaign-center
tags:
- index
- campaign
- management
---

# ⚔️ Campaign Command Center

## 🎲 Active Campaigns

```dataview
TABLE WITHOUT ID
  file.link as Campaign,
  status as Status,
  sessions as "Total Sessions",
  players as Players
FROM "01_Adventures"
WHERE type = "campaign" OR contains(file.name, "Campaign")
SORT status ASC
```

## 📅 Session Planning

### Upcoming Sessions
```dataview
TABLE WITHOUT ID
  file.link as Session,
  campaign as Campaign,
  date as "Scheduled",
  status as Status
FROM "01_Adventures"
WHERE type = "session" AND status != "completed"
SORT date ASC
```

### Recent Sessions
```dataview
TABLE WITHOUT ID
  file.link as Session,
  campaign as Campaign,
  date as Date,
  recap as "Quick Recap"
FROM "01_Adventures"
WHERE type = "session" AND status = "completed"
SORT date DESC
LIMIT 5
```

## 📊 Campaign Progress

```dataview
TABLE WITHOUT ID
  file.link as Campaign,
  sessions-completed as "Completed",
  sessions-total as "Total",
  completion as "Progress %"
FROM "01_Adventures"
WHERE type = "campaign"
```

## 🎭 Campaign NPCs

### By Faction
```dataview
TABLE WITHOUT ID
  faction as Faction,
  length(rows) as "NPC Count"
FROM "02_Worldbuilding/People"
WHERE type = "npc" AND faction != null
GROUP BY faction
SORT length(rows) DESC
```

### Important NPCs
```dataview
TABLE WITHOUT ID
  file.link as NPC,
  faction as Faction,
  role as Role,
  status as Status
FROM "02_Worldbuilding/People"
WHERE importance = "major" OR contains(tags, "important")
LIMIT 10
```

## 📍 Campaign Locations

```dataview
TABLE WITHOUT ID
  file.link as Location,
  campaign as "Used In",
  visits as Visits,
  status as Status
FROM "02_Worldbuilding/Places"
WHERE campaign != null
SORT visits DESC
```

---
*Campaign management powered by Dataview*
"""
        
        campaign_path = self.vault_path / "00_Indexes" / "Campaign_Center.md"
        campaign_path.write_text(content, encoding='utf-8')
        self.created_files.append(str(campaign_path))
        print(f"   ✅ Created: {campaign_path.name}")
        
    def step_21_30_relationship_web(self):
        """Steps 21-30: Create relationship tracking"""
        print("\n📝 Steps 21-30: Creating Relationship Web...")
        
        content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: index
cssclass: relationship-web
tags:
- index
- relationships
- npcs
---

# 👥 Character Relationship Web

## 🕸️ Relationship Overview

### Faction Affiliations
```dataview
TABLE WITHOUT ID
  faction as Faction,
  length(rows) as Members,
  leader as Leader
FROM "02_Worldbuilding/People"
WHERE faction != null
GROUP BY faction
SORT length(rows) DESC
```

### Romantic Relationships
```dataview
TABLE WITHOUT ID
  file.link as Character,
  romance as "Romantic Interest",
  relationship-status as Status
FROM "02_Worldbuilding/People"
WHERE romance != null
```

### Rivalries
```dataview
TABLE WITHOUT ID
  file.link as Character,
  rival as Rival,
  conflict as "Nature of Conflict"
FROM "02_Worldbuilding/People"
WHERE rival != null
```

### Alliances
```dataview
TABLE WITHOUT ID
  file.link as Character,
  allies as Allies,
  alliance-type as "Type"
FROM "02_Worldbuilding/People"
WHERE allies != null
```

## 👑 Power Structure

### Leaders
```dataview
TABLE WITHOUT ID
  file.link as Leader,
  faction as Organization,
  location as Base,
  followers as Followers
FROM "02_Worldbuilding/People"
WHERE role = "leader" OR contains(tags, "leader")
```

### Advisors
```dataview
TABLE WITHOUT ID
  file.link as Advisor,
  advises as "Advises",
  expertise as Expertise
FROM "02_Worldbuilding/People"
WHERE role = "advisor" OR contains(tags, "advisor")
```

## 🔗 Connection Statistics

```dataview
TABLE WITHOUT ID
  "Total NPCs" as Metric,
  length(file.link) as Count
FROM "02_Worldbuilding/People"
WHERE type = "npc"

UNION ALL

TABLE WITHOUT ID
  "Has Relationships" as Metric,
  length(file.link) as Count
FROM "02_Worldbuilding/People"
WHERE relationships != null OR allies != null OR enemies != null

UNION ALL

TABLE WITHOUT ID
  "In Factions" as Metric,
  length(file.link) as Count
FROM "02_Worldbuilding/People"
WHERE faction != null
```

## 🎯 Quest Givers

```dataview
TABLE WITHOUT ID
  file.link as "Quest Giver",
  quests-given as Quests,
  location as Location,
  faction as Faction
FROM "02_Worldbuilding/People"
WHERE quests-given != null OR contains(tags, "quest-giver")
```

---
*Relationship tracking powered by Dataview*
"""
        
        relationship_path = self.vault_path / "00_Indexes" / "Relationship_Web.md"
        relationship_path.write_text(content, encoding='utf-8')
        self.created_files.append(str(relationship_path))
        print(f"   ✅ Created: {relationship_path.name}")
        
        # Also create a Quest Tracker
        quest_content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: index
cssclass: quest-tracker
tags:
- index
- quests
- objectives
---

# 📜 Quest Tracker

## ⚔️ Active Quests

### Main Quests
```dataview
TABLE WITHOUT ID
  file.link as Quest,
  giver as "Quest Giver",
  level as Level,
  reward as Reward
FROM #quest OR "01_Adventures"
WHERE status = "active" AND type = "main"
SORT priority DESC
```

### Side Quests
```dataview
TABLE WITHOUT ID
  file.link as Quest,
  location as Location,
  difficulty as Difficulty,
  reward as Reward
FROM #quest OR "01_Adventures"
WHERE status = "active" AND type = "side"
SORT level ASC
```

## ⏰ Time-Sensitive

```dataview
TABLE WITHOUT ID
  file.link as Quest,
  deadline as Deadline,
  consequence as "If Failed"
FROM #quest OR "01_Adventures"
WHERE deadline != null AND status = "active"
SORT deadline ASC
```

## ✅ Completed Quests

```dataview
TABLE WITHOUT ID
  file.link as Quest,
  completed as "Completed Date",
  reward-received as "Rewards"
FROM #quest OR "01_Adventures"
WHERE status = "completed"
SORT completed DESC
LIMIT 10
```

## 📊 Quest Statistics

```dataview
TABLE WITHOUT ID
  status as Status,
  length(rows) as Count
FROM #quest OR "01_Adventures"
WHERE type = "quest" OR contains(tags, "quest")
GROUP BY status
```

---
*Quest tracking powered by Dataview*
"""
        
        quest_path = self.vault_path / "00_Indexes" / "Quest_Tracker.md"
        quest_path.write_text(quest_content, encoding='utf-8')
        self.created_files.append(str(quest_path))
        print(f"   ✅ Created: {quest_path.name}")
        
    def run_phase_1(self):
        """Execute Phase 1 Steps 1-30"""
        print("\n" + "="*60)
        print("🚀 PHASE 1: CORE NAVIGATION SYSTEM")
        print("="*60)
        
        # Execute steps
        self.step_1_10_dynamic_hub()
        self.step_11_20_campaign_center()
        self.step_21_30_relationship_web()
        
        # Generate report
        report = {
            "phase": "Phase 1: Core Navigation System",
            "steps_completed": "1-30 of 100",
            "timestamp": datetime.now().isoformat(),
            "files_created": self.created_files,
            "features_added": [
                "Dynamic Navigation Hub",
                "Campaign Command Center",
                "Character Relationship Web",
                "Quest Tracker"
            ],
            "next_steps": "Steps 31-40: Quick-access sidebars"
        }
        
        # Save report
        report_dir = self.vault_path / "reports"
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / f"phase1_steps_1_30_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print("\n" + "="*60)
        print("✅ PHASE 1 PROGRESS: Steps 1-30 Complete!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  • Created {len(self.created_files)} dynamic index files")
        print(f"  • Location: 00_Indexes/")
        print(f"  • Report: {report_path.name}")
        
        print(f"\n📁 Files Created:")
        for file in self.created_files:
            print(f"  • {Path(file).name}")
            
        print(f"\n🎯 Next Steps (31-40):")
        print("  • Quick-access sidebars")
        print("  • Frequently used content panels")
        print("  • Navigation shortcuts")
        
        print("\n💡 To view the new indexes:")
        print("  1. Open Obsidian")
        print("  2. Navigate to 00_Indexes folder")
        print("  3. Open any of the new index files")
        print("  4. Install/enable Dataview plugin for full functionality")
        
        return report

def main():
    navigator = Phase1Navigation()
    navigator.run_phase_1()

if __name__ == "__main__":
    main()