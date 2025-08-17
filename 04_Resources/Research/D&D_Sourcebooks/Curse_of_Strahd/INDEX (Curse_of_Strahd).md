---

title: INDEX (Curse_of_Strahd)
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'
aliases: ["INDEX (Curse of Strahd)"]
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
updated: '2025-08-13T12:48:04.960157'
world: Both
sourcebook: Curse of Strahd
abbreviation: Co S

--- ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## Overview

**Type**: Campaign **Level Range**: 1-10 **Themes**: horror, undead, gothic, mystery **Integration Status**: Available ## Description

Gothic horror campaign in Barovia ### 🎭 NPCs```dataview

TABLE WITHOUT ID file.link as "NPC", status as "Status", world as "Adapted To"

FROM "Curse_of_Strahd/NPCs"

WHERE type = "Character"

SORT file.name```### 👹 Monsters & Creatures file.link as "Monster", cr as "CR", status as "Status"

FROM "Curse_of_Strahd/Monsters" WHERE type = "Monster"

SORT cr ### 🗺️ Locations file.link as "Location", threat_level as "Danger",

FROM "Curse_of_Strahd/Locations"

WHERE type = "Location" ### ⚔️ Items & Equipment file.link as "Item", rarity as "Rarity",

FROM "Curse_of_Strahd/Items"

WHERE type = "Item"

SORT rarity ### 📜 Adventures & Scenarios file.link as "Adventure", suggested_level as "Level", status as "Status" FROM "Curse_of_Strahd/Adventures"

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
- Connections to overarching campaign themes ## Secret Connections *[Hidden from players]* Connected to The Hidden Alliance - Achieve immortality ## Plot Hooks - Someone is blackmailing a artifact for revenge

- A letter reveals a betrayal about the cult ## 12_Research Specific Content Contextual improvement based on 12_Research

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