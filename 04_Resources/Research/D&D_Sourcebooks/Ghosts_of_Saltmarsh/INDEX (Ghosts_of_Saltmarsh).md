---

title: INDEX (Ghosts_of_Saltmarsh)
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'
aliases: ["INDEX (Ghosts of Saltmarsh)"]
status: active
priority: normal
category: 12 Research
subcategory: D&D Sourcebooks
related: []
cssclass: standard
publish: false

---

 # INDEX ---

title: INDEX
type: Resource
tags:
- integration/available
- type/resource
- research
- status/active
- dnd/sourcebook
- active

created: '2025-08-13'
modified: '2025-08-14'
status: active
updated: '2025-08-13T12:48:04.961841'
world: Both
sourcebook: Ghosts of Saltmarsh
abbreviation: Go S

--- ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## Overview

**Type**: Campaign **Level Range**: 1-12 **Themes**: nautical, pirates, coastal, mystery **Integration Status**: Available ## Description

Maritime adventures and sea-based campaigns ### 🎭 NPCs```dataview

TABLE WITHOUT ID file.link as "NPC", status as "Status", world as "Adapted To"

FROM "Ghosts_of_Saltmarsh/NPCs"

WHERE type = "Character"

SORT file.name```### 👹 Monsters & Creatures file.link as "Monster", cr as "CR", status as "Status"

FROM "Ghosts_of_Saltmarsh/Monsters" WHERE type = "Monster"

SORT cr ### 🗺️ Locations file.link as "Location", threat_level as "Danger",

FROM "Ghosts_of_Saltmarsh/Locations"

WHERE type = "Location" ### ⚔️ Items & Equipment file.link as "Item", rarity as "Rarity",

FROM "Ghosts_of_Saltmarsh/Items"

WHERE type = "Item"

SORT rarity ### 📜 Adventures & Scenarios file.link as "Adventure", suggested_level as "Level", status as "Status" FROM "Ghosts_of_Saltmarsh/Adventures"

WHERE type = "Adventure"

SORT suggested_level ## Usage in Campaigns

This content can be used as:
- **Direct Import**: Use scenarios as-written in neutral zones
- **Realm Adaptation**: Convert for specific Aquabyssos/Aethermoor use
- **Inspiration Source**: Mine for ideas and adapt loosely
- **Crossover Events**: Bridge between D&D and Cordelia continuity ---

*Integration managed through the D&D Sourcebook Integration System* *Last updated: 2025-08-13 12:48* ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes

## Notes

*Additional notes*

#mechanics/system
#story/story
#world/location
#world/world
#character/npc
#character/character
#character/creature
#character/monster
#gameplay/adventure
#resource/item
#resource/equipment
#meta/index
#meta/reference