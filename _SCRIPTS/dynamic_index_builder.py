#!/usr/bin/env python3
"""
Phase 1 Steps 1-10: Dynamic Index Builder
Creates auto-updating index pages with live content lists
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import json
from collections import defaultdict

class DynamicIndexBuilder:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.indexes_created = []
        
    def create_master_dynamic_index(self):
        """Step 1-3: Create the main dynamic navigation hub"""
        content = """---
created: {date}
updated: {date}
type: index
cssclass: navigation-hub
tags:
- index
- navigation
- dynamic
---

# 🗺️ Vault Navigation Hub

> *Auto-updated: This page refreshes automatically to show current vault contents*

```dataview
TABLE WITHOUT ID
  "📊 " + length(rows) + " items" as Count,
  "📁 " + file.folder as Location
FROM ""
WHERE file.name != this.file.name
GROUP BY file.folder
SORT file.folder ASC
```

## 🎯 Quick Navigation

### 🎲 Active Campaigns
```dataview
LIST
FROM "01_Adventures"
WHERE type = "campaign" OR contains(tags, "campaign")
SORT file.mtime DESC
LIMIT 10
```

### 👥 Recent NPCs
```dataview
TABLE WITHOUT ID
  file.link as NPC,
  faction as Faction,
  location as Location,
  status as Status
FROM "02_Worldbuilding/People"
WHERE type = "npc"
SORT file.mtime DESC
LIMIT 10
```

### 📍 Key Locations
```dataview
TABLE WITHOUT ID
  file.link as Location,
  world as Realm,
  danger-level as Danger
FROM "02_Worldbuilding/Places"
WHERE type = "location"
SORT file.mtime DESC
LIMIT 10
```

### 📅 Recent Sessions
```dataview
TABLE WITHOUT ID
  file.link as Session,
  campaign as Campaign,
  date as Date,
  status as Status
FROM "01_Adventures"
WHERE type = "session"
SORT date DESC
LIMIT 5
```

## 📈 Vault Statistics

```dataviewjs
// Step 4-5: Calculate vault statistics
const pages = dv.pages('""');
const campaigns = pages.where(p => p.type == "campaign").length;
const npcs = pages.where(p => p.type == "npc").length;
const locations = pages.where(p => p.type == "location").length;
const sessions = pages.where(p => p.type == "session").length;
const items = pages.where(p => p.type == "item").length;

dv.paragraph(`
| Category | Count |
|----------|-------|
| Total Files | ${pages.length} |
| Campaigns | ${campaigns} |
| NPCs | ${npcs} |
| Locations | ${locations} |
| Sessions | ${sessions} |
| Items | ${items} |
| Last Updated | ${new Date().toLocaleDateString()} |
`);
```

## 🔥 Hot Content (Recently Modified)

```dataview
TABLE WITHOUT ID
  file.link as Content,
  file.folder as Category,
  file.mtime as Modified
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 20
```

## 🏷️ Tag Cloud

```dataviewjs
// Step 6-7: Generate tag cloud
const allTags = {};
for (const page of dv.pages('""')) {
    if (page.tags) {
        const tags = Array.isArray(page.tags) ? page.tags : [page.tags];
        tags.forEach(tag => {
            allTags[tag] = (allTags[tag] || 0) + 1;
        });
    }
}

const sortedTags = Object.entries(allTags)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 30);

const tagCloud = sortedTags.map(([tag, count]) => {
    const size = Math.min(Math.max(10 + count * 2, 10), 30);
    return `<span style="font-size: ${size}px; margin: 5px;">[[${tag}]] (${count})</span>`;
}).join(' ');

dv.paragraph(tagCloud);
```

## 🔍 Smart Searches

### By Status
- [[🟢 Active Content|Active]] `status:active`
- [[🟡 Draft Content|Draft]] `status:draft`
- [[🔴 Archived Content|Archived]] `status:archived`

### By World
- [[🌊 Aquabyssos Content|Aquabyssos]] `world:Aquabyssos`
- [[☁️ Aethermoor Content|Aethermoor]] `world:Aethermoor`
- [[🌍 Both Realms|Both]] `world:Both`

### By Type
- [[⚔️ Combat Content|Combat]] `tag:combat`
- [[🎭 Social Content|Social]] `tag:social`
- [[🗺️ Exploration Content|Exploration]] `tag:exploration`

## 📊 Content Health Check

```dataviewjs
// Step 8-10: Content health monitoring
const orphans = dv.pages('""').where(p => p.file.inlinks.length == 0 && p.file.outlinks.length == 0);
const stubs = dv.pages('""').where(p => p.file.size < 500);
const untagged = dv.pages('""').where(p => !p.tags || p.tags.length == 0);

dv.paragraph(`
### ⚠️ Maintenance Needed
- **Orphaned Pages**: ${orphans.length} pages with no links
- **Stub Articles**: ${stubs.length} pages under 500 bytes
- **Untagged Pages**: ${untagged.length} pages without tags
`);

if (orphans.length > 0) {
    dv.header(4, "Orphaned Pages (Top 5)");
    dv.list(orphans.slice(0, 5).map(p => p.file.link));
}
```

---

*This navigation hub auto-updates using Dataview. No manual maintenance required!*
""".format(date=datetime.now().strftime('%Y-%m-%d'))
        
        index_path = self.vault_path / "00_Indexes" / "Dynamic_Navigation_Hub.md"
        index_path.write_text(content, encoding='utf-8')
        self.indexes_created.append(str(index_path))
        print(f"✅ Created Dynamic Navigation Hub")
        
    def create_campaign_index(self):
        """Steps 11-15: Create campaign-specific dynamic index"""
        content = """---
created: {date}
updated: {date}
type: index
cssclass: campaign-index
tags:
- index
- campaign
- dynamic
---

# ⚔️ Campaign Command Center

## 🎯 Active Campaigns

```dataview
TABLE WITHOUT ID
  file.link as Campaign,
  status as Status,
  sessions as Sessions,
  players as Players,
  level as Level
FROM "01_Adventures"
WHERE type = "campaign"
SORT status ASC, file.mtime DESC
```

## 📅 Upcoming Sessions

```dataview
TABLE WITHOUT ID
  file.link as Session,
  campaign as Campaign,
  date as "Scheduled",
  status as Status
FROM "01_Adventures"
WHERE type = "session" AND date >= date(today)
SORT date ASC
```

## 🎭 Campaign NPCs by Faction

```dataviewjs
const npcs = dv.pages('"02_Worldbuilding/People"').where(p => p.type == "npc");
const factions = {};

npcs.forEach(npc => {
    const faction = npc.faction || "Independent";
    if (!factions[faction]) factions[faction] = [];
    factions[faction].push(npc);
});

for (const [faction, members] of Object.entries(factions)) {
    if (members.length > 0) {
        dv.header(3, `${faction} (${members.length})`);
        dv.list(members.slice(0, 5).map(m => m.file.link));
    }
}
```

## 🗺️ Campaign Locations

```dataview
TABLE WITHOUT ID
  file.link as Location,
  campaign as Campaign,
  world as Realm,
  visits as "Times Visited"
FROM "02_Worldbuilding/Places"
WHERE campaign != null
GROUP BY campaign
```

## 📜 Active Quests

```dataview
TABLE WITHOUT ID
  file.link as Quest,
  campaign as Campaign,
  status as Status,
  level as Level,
  reward as Reward
FROM #quest
WHERE status != "complete"
SORT status ASC, level ASC
```

## 📊 Campaign Progress Tracker

```dataviewjs
const campaigns = dv.pages('"01_Adventures"').where(p => p.type == "campaign");

const progress = campaigns.map(c => {
    const sessions = dv.pages('"01_Adventures"')
        .where(s => s.campaign == c.file.name && s.type == "session");
    const completed = sessions.where(s => s.status == "completed").length;
    const total = sessions.length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
    
    return {
        name: c.file.link,
        progress: `${completed}/${total} sessions (${percentage}%)`,
        bar: "█".repeat(Math.floor(percentage / 10)) + "░".repeat(10 - Math.floor(percentage / 10))
    };
});

dv.table(["Campaign", "Progress", "Visual"], 
    progress.map(p => [p.name, p.progress, p.bar]));
```

---
*Auto-updating campaign tracker powered by Dataview*
""".format(date=datetime.now().strftime('%Y-%m-%d'))
        
        index_path = self.vault_path / "00_Indexes" / "Campaign_Command_Center.md"
        index_path.write_text(content, encoding='utf-8')
        self.indexes_created.append(str(index_path))
        print(f"✅ Created Campaign Command Center")
        
    def create_npc_relationship_index(self):
        """Steps 16-20: Create NPC relationship tracker"""
        content = """---
created: {date}
updated: {date}
type: index
cssclass: npc-relationships
tags:
- index
- npc
- relationships
---

# 👥 NPC Relationship Web

## 🕸️ Relationship Network

```dataviewjs
// Create relationship visualization
const npcs = dv.pages('"02_Worldbuilding/People"').where(p => p.type == "npc");
const relationships = [];

npcs.forEach(npc => {
    if (npc.relationships) {
        const rels = Array.isArray(npc.relationships) ? npc.relationships : [npc.relationships];
        rels.forEach(rel => {
            relationships.push({
                from: npc.file.name,
                to: rel,
                type: npc.relationship_type || "connected"
            });
        });
    }
});

// Group by relationship type
const grouped = {};
relationships.forEach(r => {
    if (!grouped[r.type]) grouped[r.type] = [];
    grouped[r.type].push(`${r.from} → ${r.to}`);
});

for (const [type, rels] of Object.entries(grouped)) {
    dv.header(3, `${type} (${rels.length})`);
    dv.list(rels.slice(0, 10));
}
```

## 👑 Faction Leaders

```dataview
TABLE WITHOUT ID
  file.link as NPC,
  faction as Faction,
  role as Role,
  location as Location
FROM "02_Worldbuilding/People"
WHERE role = "leader" OR contains(tags, "leader")
SORT faction ASC
```

## 💕 Romantic Relationships

```dataview
TABLE WITHOUT ID
  file.link as Character,
  romance as "Romantic Interest",
  status as "Relationship Status"
FROM "02_Worldbuilding/People"
WHERE romance != null
```

## ⚔️ Rivalries & Enemies

```dataview
TABLE WITHOUT ID
  file.link as Character,
  rival as Rival,
  enemy as Enemy,
  conflict as "Nature of Conflict"
FROM "02_Worldbuilding/People"
WHERE rival != null OR enemy != null
```

## 🤝 Alliances

```dataview
TABLE WITHOUT ID
  file.link as Character,
  allies as Allies,
  faction as Faction
FROM "02_Worldbuilding/People"
WHERE allies != null
```

## 📊 NPC Statistics

```dataviewjs
const npcs = dv.pages('"02_Worldbuilding/People"').where(p => p.type == "npc");

const stats = {
    total: npcs.length,
    alive: npcs.where(n => n.status == "alive").length,
    dead: npcs.where(n => n.status == "dead").length,
    missing: npcs.where(n => n.status == "missing").length,
    withFaction: npcs.where(n => n.faction).length,
    withRelationships: npcs.where(n => n.relationships).length
};

dv.paragraph(`
| Metric | Count | Percentage |
|--------|-------|------------|
| Total NPCs | ${stats.total} | 100% |
| Alive | ${stats.alive} | ${Math.round(stats.alive/stats.total*100)}% |
| Dead | ${stats.dead} | ${Math.round(stats.dead/stats.total*100)}% |
| Missing | ${stats.missing} | ${Math.round(stats.missing/stats.total*100)}% |
| In Factions | ${stats.withFaction} | ${Math.round(stats.withFaction/stats.total*100)}% |
| Has Relationships | ${stats.withRelationships} | ${Math.round(stats.withRelationships/stats.total*100)}% |
`);
```

---
*NPC relationship tracking powered by Dataview*
""".format(date=datetime.now().strftime('%Y-%m-%d'))
        
        index_path = self.vault_path / "00_Indexes" / "NPC_Relationship_Web.md"
        index_path.write_text(content, encoding='utf-8')
        self.indexes_created.append(str(index_path))
        print(f"✅ Created NPC Relationship Web")
        
    def create_location_explorer(self):
        """Steps 21-25: Create location exploration index"""
        content = """---
created: {date}
updated: {date}
type: index
cssclass: location-explorer
tags:
- index
- locations
- exploration
---

# 🗺️ World Explorer

## 🌍 Realm Overview

```dataviewjs
const locations = dv.pages('"02_Worldbuilding/Places"');
const aquabyssos = locations.where(l => l.world == "Aquabyssos").length;
const aethermoor = locations.where(l => l.world == "Aethermoor").length;
const both = locations.where(l => l.world == "Both").length;

dv.paragraph(`
### Realm Distribution
- 🌊 **Aquabyssos**: ${aquabyssos} locations
- ☁️ **Aethermoor**: ${aethermoor} locations  
- 🌍 **Both Realms**: ${both} locations
`);

// Visual bar chart
const total = aquabyssos + aethermoor + both;
const aquaBar = "🟦".repeat(Math.round(aquabyssos/total*20));
const aethBar = "⬜".repeat(Math.round(aethermoor/total*20));
const bothBar = "🟩".repeat(Math.round(both/total*20));

dv.paragraph(`
\`\`\`
Aquabyssos: ${aquaBar}
Aethermoor: ${aethBar}
Both:       ${bothBar}
\`\`\`
`);
```

## 🏙️ Major Cities

```dataview
TABLE WITHOUT ID
  file.link as City,
  world as Realm,
  population as Population,
  government as Government,
  danger-level as Danger
FROM "02_Worldbuilding/Places"
WHERE type = "city" OR contains(tags, "city")
SORT population DESC
```

## ⚔️ Dungeons & Dangerous Places

```dataview
TABLE WITHOUT ID
  file.link as Location,
  danger-level as "Danger Level",
  treasures as Treasures,
  monsters as Monsters,
  explored as "Explored?"
FROM "02_Worldbuilding/Places"
WHERE danger-level = "Dangerous" OR danger-level = "Deadly" OR type = "dungeon"
SORT danger-level DESC
```

## 🏛️ Points of Interest

```dataview
TABLE WITHOUT ID
  file.link as Location,
  type as Type,
  services as Services,
  notable-npcs as "Notable NPCs"
FROM "02_Worldbuilding/Places"
WHERE type = "landmark" OR type = "temple" OR type = "guild" OR type = "shop"
GROUP BY type
```

## 🛤️ Travel Routes

```dataview
TABLE WITHOUT ID
  file.link as Route,
  from as From,
  to as To,
  distance as Distance,
  travel-time as "Travel Time",
  dangers as Dangers
FROM #travel-route OR #road OR #path
```

## 📍 Unexplored Locations

```dataview
LIST
FROM "02_Worldbuilding/Places"
WHERE explored = false OR status = "unexplored" OR contains(tags, "unexplored")
SORT file.name ASC
```

## 🗺️ Location Discovery Timeline

```dataview
TABLE WITHOUT ID
  file.link as Location,
  discovered as "Discovered",
  discovered-by as "Discovered By",
  sessions as "First Visited"
FROM "02_Worldbuilding/Places"
WHERE discovered != null
SORT discovered DESC
LIMIT 10
```

---
*Interactive world exploration powered by Dataview*
""".format(date=datetime.now().strftime('%Y-%m-%d'))
        
        index_path = self.vault_path / "00_Indexes" / "World_Explorer.md"
        index_path.write_text(content, encoding='utf-8')
        self.indexes_created.append(str(index_path))
        print(f"✅ Created World Explorer")
        
    def create_quest_tracker(self):
        """Steps 26-30: Create quest tracking system"""
        content = """---
created: {date}
updated: {date}
type: index
cssclass: quest-tracker
tags:
- index
- quests
- objectives
---

# 📜 Quest Journal

## ⚔️ Active Main Quests

```dataview
TABLE WITHOUT ID
  file.link as Quest,
  quest-giver as "Given By",
  level as Level,
  time-limit as "Time Limit",
  reward as Reward
FROM #quest
WHERE status = "active" AND type = "main"
SORT priority DESC, level ASC
```

## 🎯 Side Quests

```dataview
TABLE WITHOUT ID
  file.link as Quest,
  location as Location,
  difficulty as Difficulty,
  reward as Reward
FROM #quest
WHERE status = "active" AND type = "side"
SORT level ASC
```

## ⏰ Time-Sensitive Quests

```dataview
TABLE WITHOUT ID
  file.link as Quest,
  deadline as Deadline,
  days-remaining as "Days Left",
  consequence as "If Failed"
FROM #quest
WHERE deadline != null AND status = "active"
SORT deadline ASC
```

## ✅ Quest Progress

```dataviewjs
const quests = dv.pages("#quest").where(q => q.status == "active");

const progress = quests.map(q => {
    const objectives = q.objectives || [];
    const completed = objectives.filter(o => o.completed).length;
    const total = objectives.length;
    const percentage = total > 0 ? Math.round((completed/total) * 100) : 0;
    
    return {
        quest: q.file.link,
        progress: `${completed}/${total}`,
        bar: "█".repeat(Math.floor(percentage/10)) + "░".repeat(10 - Math.floor(percentage/10)),
        percentage: percentage + "%"
    };
});

dv.table(
    ["Quest", "Objectives", "Progress", "Completion"],
    progress.map(p => [p.quest, p.progress, p.bar, p.percentage])
);
```

## 🏆 Completed Quests

```dataview
TABLE WITHOUT ID
  file.link as Quest,
  completed-date as "Completed",
  reward-received as "Reward Received",
  impact as Impact
FROM #quest
WHERE status = "completed"
SORT completed-date DESC
LIMIT 10
```

## ❌ Failed Quests

```dataview
TABLE WITHOUT ID
  file.link as Quest,
  failed-date as "Failed",
  reason as Reason,
  consequences as Consequences
FROM #quest
WHERE status = "failed"
```

## 🎲 Quest Hooks Available

```dataview
LIST
FROM #quest-hook OR #rumor
WHERE status = "available" OR status = null
SORT file.mtime DESC
```

## 📊 Quest Statistics

```dataviewjs
const allQuests = dv.pages("#quest");

const stats = {
    total: allQuests.length,
    active: allQuests.where(q => q.status == "active").length,
    completed: allQuests.where(q => q.status == "completed").length,
    failed: allQuests.where(q => q.status == "failed").length,
    available: allQuests.where(q => q.status == "available").length
};

const avgReward = allQuests
    .where(q => q.reward_gold)
    .map(q => q.reward_gold)
    .reduce((a, b) => a + b, 0) / allQuests.where(q => q.reward_gold).length || 0;

dv.paragraph(`
| Metric | Value |
|--------|-------|
| Total Quests | ${stats.total} |
| Active | ${stats.active} |
| Completed | ${stats.completed} |
| Failed | ${stats.failed} |
| Available | ${stats.available} |
| Success Rate | ${Math.round(stats.completed/(stats.completed+stats.failed)*100)}% |
| Average Gold Reward | ${Math.round(avgReward)} gp |
`);
```

---
*Quest tracking and management powered by Dataview*
""".format(date=datetime.now().strftime('%Y-%m-%d'))
        
        index_path = self.vault_path / "00_Indexes" / "Quest_Journal.md"
        index_path.write_text(content, encoding='utf-8')
        self.indexes_created.append(str(index_path))
        print(f"✅ Created Quest Journal")
        
    def create_all_indexes(self):
        """Execute all index creation steps"""
        print("\n🚀 PHASE 1: Building Dynamic Navigation System")
        print("="*60)
        
        # Steps 1-10
        print("\n📝 Steps 1-10: Core Dynamic Indexes")
        self.create_master_dynamic_index()
        
        # Steps 11-20  
        print("\n📝 Steps 11-20: Campaign & NPC Indexes")
        self.create_campaign_index()
        self.create_npc_relationship_index()
        
        # Steps 21-30
        print("\n📝 Steps 21-30: Location & Quest Indexes")
        self.create_location_explorer()
        self.create_quest_tracker()
        
        # Generate report
        report = {
            "phase": "Phase 1: Core Navigation System",
            "steps_completed": "1-30",
            "timestamp": datetime.now().isoformat(),
            "indexes_created": self.indexes_created,
            "next_steps": "Steps 31-40: Quick-access sidebars"
        }
        
        report_path = self.vault_path / "reports" / f"phase1_navigation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print("\n" + "="*60)
        print("✅ PHASE 1 PROGRESS: Steps 1-30 Complete!")
        print("="*60)
        print(f"Created {len(self.indexes_created)} dynamic indexes")
        print(f"Report saved: {report_path}")
        print("\nNext: Steps 31-40 - Quick-access sidebars")
        
        return report

def main():
    builder = DynamicIndexBuilder()
    builder.create_all_indexes()

if __name__ == "__main__":
    main()