---

title: Coverage_Dashboard (D&D_References)
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'
aliases: ["Coverage Dashboard (D&D References)"]
status: active
priority: normal
category: 12 Research
subcategory: D&D References
related: []
cssclass: standard
publish: false

---

 # Coverage_Dashboard ---

## Description

Detailed description pending.
title: Content Coverage Dashboard
type: Lore
tags:
- index
- status/complete
- performance
- statistics
- research
- world/both
- coverage
- active

created: '2025-08-11'
modified: '2025-08-14'
status: complete
cssclasses:
- wide-page
- index-page

updated: '2025-08-12T23:37:33.016338'
world: Both

--- # 📊 Content Coverage Dashboard

*Tracking Vault Completion and Content Depth* ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## Overall Vault Statistics```dataview

TABLE WITHOUT ID "**Total Files**" as Metric, length(pages()) as Count

FROM ""

LIMIT 1```### Worldbuilding Coverage TABLE Category, Total, Complete, Stubs, round((Complete / Total) * 100, 1) + "%" as "Completion %"

FROM ({Category: "People", Total: 181, Complete: 102, Stubs: 79}, {Category: "Places", Total: 361, Complete: 122, Stubs: 239}, {Category: "Groups", Total: 74, Complete: 41, Stubs: 33}, {Category: "Quests", Total: 59, Complete: 51, Stubs: 8}, {Category: "Items", Total: 7, Complete: 7, Stubs: 0}, {Category: "Lore", Total: 262, Complete: 39, Stubs: 223}, {Category: "Hazards", Total: 1, Complete: 1, Stubs: 0})

SORT "Completion %" DESC ### Content Status Distribution status as "Status", length(rows) as "Count"

WHERE contains(file.path, "Worldbuilding")

GROUP BY status

SORT length(rows) DESC ### High-Priority People (Referenced but Stub)

TABLE file.link as "Character", length(file.inlinks) as "References", file.size as "Size (bytes)"

FROM "02_Worldbuilding/People"

WHERE file.size < 500

AND length(file.inlinks) > 2

SORT length(file.inlinks) DESC

LIMIT 10 ### High-Priority Places (Referenced but Stub)

TABLE file.link as "Location", length(file.inlinks) as "References", file.size as "Size (bytes)"

FROM "02_Worldbuilding/Places" ### Average File Sizes by Category split(file.path, "/")[1] as "Category", round(sum(rows.file.size) / length(rows), 0) as "Avg Size (bytes)", min(rows.file.size) as "Smallest", max(rows.file.size) as "Largest"

FROM "02_Worldbuilding"

GROUP BY split(file.path, "/")[1]

SORT "Avg Size (bytes)" DESC ### Files Updated This Week

TABLE file.link as "File", file.mtime as "Modified", file.size as "Size", status

WHERE file.mtime > date(today) - dur(7 days)

AND contains(file.path, "Worldbuilding")

SORT file.mtime DESC

LIMIT 20 ### Newly Created Content

TABLE file.link as "New File", file.ctime as "Created", split(file.path, "/")[1] as "Category"

WHERE file.ctime > date(today) - dur(7 days)

AND !contains(file.path, "Templates")

AND !contains(file.path, "Archive")

SORT file.ctime DESC

LIMIT 15 ### Adventures & Sessions Type, Count, Status {Type: "Adventures", Count: length(pages("#adventure")), Status: "✅ Ready"}, {Type: "Sessions Written", Count: length(pages("#session")), Status: "✅ Active"}, {Type: "GM Resources", Count: length(pages("#gm-resource")), Status: "✅ Available"}, {Type: "Player Handouts", Count: length(pages("#handout")), Status: "🔄 Expanding"} ### Most Used Tags tag as "Tag", length(rows) as "Uses"

FLATTEN file.tags as tag

WHERE !contains(tag, "ttrpg-cli")

GROUP BY tag ### Projected Completion

At current rate (40-60 files/session):
- **80% Complete**: ~8-10 more sessions
- **95% Complete**: ~12-15 more sessions
- **100% Complete**: ~15-20 more sessions --- *Dashboard refreshes automatically with Dataview*

*Last structural update: * ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Plot Hooks - Someone is blackmailing information for power

- The authorities needs help delivering before the new moon
- A merchant needs help finding before dawn ## 12_Research Specific Content Contextual improvement based on 12_Research ## 12_Research Specific Content Contextual improvement based on 12_Research

## Notes

*Additional notes*

#story/plot
#story/story
#story/lore
#world/location
#world/world
#world/place
#character/character
#gameplay/session
#gameplay/adventure
#gameplay/quest
#resource/item
#meta/index
#meta/reference