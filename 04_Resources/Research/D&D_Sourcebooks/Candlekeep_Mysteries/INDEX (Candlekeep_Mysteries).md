---

title: INDEX (Candlekeep_Mysteries)
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'
aliases: ["INDEX (Candlekeep Mysteries)"]
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
updated: '2025-08-13T12:48:04.963113'
world: Both
sourcebook: Candlekeep Mysteries
abbreviation: CM

--- ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## Overview

**Type**: Adventure **Level Range**: 1-16 **Themes**: mystery, investigation, magic, knowledge **Integration Status**: Available ## Description

Collection of book-based mystery adventures ### 🎭 NPCs```dataview

TABLE WITHOUT ID file.link as "NPC", status as "Status", world as "Adapted To"

FROM "Candlekeep_Mysteries/NPCs"

WHERE type = "Character"

SORT file.name```### 👹 Monsters & Creatures file.link as "Monster", cr as "CR", status as "Status"

FROM "Candlekeep_Mysteries/Monsters" WHERE type = "Monster"

SORT cr ### 🗺️ Locations file.link as "Location", threat_level as "Danger",

FROM "Candlekeep_Mysteries/Locations"

WHERE type = "Location" ### ⚔️ Items & Equipment file.link as "Item", rarity as "Rarity",

FROM "Candlekeep_Mysteries/Items"

WHERE type = "Item"

SORT rarity ### 📜 Adventures & Scenarios file.link as "Adventure", suggested_level as "Level", status as "Status" FROM "Candlekeep_Mysteries/Adventures"

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
- Connections to overarching campaign themes ## Prophecy Connection Mentioned in The First Prophecy of Winds ## Plot Hooks - A stranger needs help stealing before the festival

- Strange dreams suggest a conspiracy
- A merchant needs help delivering before winter
- Strange dreams suggest a curse ## 12_Research Specific Content Contextual improvement based on 12_Research ## 12_Research Specific Content Contextual improvement based on 12_Research

## Notes

*Additional notes*

#mechanics/system
#story/plot
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