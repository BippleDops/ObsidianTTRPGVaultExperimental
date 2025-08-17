---
enhanced: true
tags: [enhanced, _indexes]
created: "2025-08-15T16:41:29.330730"
modified: "2025-08-15T16:41:29.330734"
aliases: [MOC Lore]
---

## Table of Contents
- [[#Quick Links|Quick Links
- [#Content|Content]]
- [[#Recent NPCs|Recent NPCs
- [#Active Quests|Active Quests]]
- [[#Session Log|Session Log
- [#Location Network|Location Network]]
- [[#See Also|See Also
- [#Game Mechanics|Game Mechanics]]
- [[#D&D 5e References|D&D 5e References
- [#Connections|Connections]]

-tags: [moc, index, combat]ex]
created: 2025-08-15
---

# [[Lore|Lore Index

> Central hub for all Lore content

## Quick Links
- [MASTER_MOC|← Back to Master]]

## Content
*Building index...*

## Recent NPCs
```dataview
TABLE file.mtime as "Modified"
FROM "03_People"
SORT file.mtime DESC
LIMIT 10
WHERE file.name != ""
```

## Active Quests
```dataview
TABLE file.link as "File"
FROM "01_Adventures"
WHERE contains(status, "active")
```

## Session Log
```dataview
TABLE date as "Date", players_present as "Players"
FROM "06_Sessions"
SORT date DESC
WHERE file.name != ""
```

## Location Network
```dataview
TABLE file.link as "File"
FROM "02_Worldbuilding"
WHERE contains(file.name, "Location") OR contains(tags, "location")
```

> [!warning] ⚠️ Warning
> Important safety or rule information

## See Also
- [[NPC01664_Pyria_Lightbringer_the_Redeemed]]
- [[NPC01041_Thalia_Dawnstrider_the_Lost]]
- [[Submersible_Schematic_Pressure_Gate_Scou]]
- [[NPC01360_Ewan_Blackstone_the_Strong]]
- [[NPC01177_Thalia_Underhill_the_Fallen]]
- [[NPC00663_Alaric_Dawnstrider_the_Strong]]
- [[NPC00872_Thalia_Ironwood_the_Broken]]
- [[NPC00069_Thalia_Brightblade_the_Guardian]]
- [[NPC01290_Pyria_Ashford_the_Broken]]
- [[NPC01012_Solas_Darkwater_the_Strong]]
- [[Session 0 - Aquabyssos]]
- [[MOC_Locations]]
-

## Game Mechanics
- **Combat**: See ACX p.189-198

## D&D 5e References

*(Combat rules: ACX p.189-198)*
*(Attack rolls: ACX p.194)*
*(Damage & Healing: ACX p.196-197)*

## Connections

- Affected by [[Item Artifact Explorers Pack Xphb Explorers Pack Xphb.png
- Requires [step_015 (phase_025)]]
- See also: [[Shadow Operations Base 2
- Influences [step_040 (phase_008)]]
- See also: [[Viscountess Helena Saltmere (D&D_References)]]
- Originates from [[Enterprise Director Duskwork
- Parallels [Portrait NPC the Azure Prophet Nerissa V2 the Azure Prophet Nerissa.svg_1 (Portraits)]]
- See also: [[QUEST0067_In_Search_of_Redemption]]
- Connects to [[step_048 (phase_090)
- Influences [Elder Stormcalle]]
- Influences [[LOC00131_Dungeons_Location_132]]
- Requires [[Fire Casting Statue Xdmg
- Connects to [step_085 (phase_061)]]
- See also: [[Leviathan Shrines
- Leads to [location-city-the-deepmind-the-deepmind.svg]]
- Influences [[QUEST00105_Personal_Quest_106]]
- Connects to
- Requires [[location-city-aethermoor-aethermoor.svg
- Connects to [Lady Penelope Procedure (D&D_References)]]
- Requires [[Vault Backup 20250813 073007 07 Player Session Summaries Session Zero Universal Guide]]
- Affected by [[Royal Intelligence (D&D_References)
- Parallels [Assets Locations Location City Commercial District V1 Commercial District.svg]]
- Affected by
- Requires [[step_001 (phase_035)
- Connects to [Trade Representatives 2]]
- See also: [[Ethereal Anchors (D&D_References)
- Requires [location-city-crystal-palace-v1-crystal-palace.svg]]
- See also: [[Archivist Memory Bank (D&D_References)
- See also: [Creature Creature Nightwalker Mpmm V1 Nightwalker Mpmm.png]]
- See also: [[step_043 (phase_009)
- Connects to [LOC0142_Watchhollow]]
- Compare with [[Royal Bloodline Codex (D&D_References)]]
- Connects to [[Ambassador Lysandra Silvertonge 2
- Related:
- Parallels
- Requires
- Related: [FAC00007_Orders_8]]
- See also: [[QUEST00304_Side_Quest_305]]
- Affected by [[step_015 (phase_071)
- See also:
- Compare with [ITEM00624_Enchanted_Gauntlets_of_Protection]]
- Affected by [[The Crystal Cathedral of Pure Light 2
- Connects to [Location City Master Goldwin Ledgerkeeper Master Goldwin Ledgerkeeper.svg]]
- Connects to [[LOC00075_Dungeons_Location_76]]
- Related: [[NPC01184_Ewan_Ironwood_the_Guardian]]
- Requires [[Assets Locations Location City Deep Stone Eaters V1 Deep Stone Eaters.svg
- See also: [NPC00858_Zephyr_Silverleaf_the_Wanderer]]
- Connects to [[Economic Pressure
- Related: [step_045 (phase_018)]]
- Leads to [[step_093 (phase_079)
- Influences [portrait-npc-the-schooling-v2-the-schooling.svg]]
- Influences [[NPC01196_Brenna_Underhill_the_Wise
- Connects to [Assets Locations Location City Portal Network Portal Network.svg]]
- See also: [[Portrait NPC Captain Blackwater Captain Blackwater.svg
- Connects to [Historian Kelp Chronicler]]
- Compare with [[LOC00272_Wilderness_Location_273
- Related: [dungeons-dungeon-quirks-xdmg (tables)]]
- Affected by [[Assets Portraits Portrait NPC the Crimson Pearl the Crimson Pearl.svg
- Parallels [step_100 (phase_065)]]
- Influences [[ITEM00460_Enchanted_Shield_of_Protection
- Requires [Assets Locations Location City Senator Bartholomew Bonewright V1 Senator Bartholomew Bonewright.svg]]
- Related: [[MON00127_Aberrations_Creature_128
- Influences [location-city-crystalhaven-v1-crystalhaven.svg]]
- Requires [[NPC01135_Thalia_Proudmore_the_Broken
- Influences [ITEM01359_Sturdy_Tool_Kit_of_Convenience]]
- Requires [[02_Worldbuilding_Items_Elemental_Air_Filter
- Related: [step_091 (phase_100)]]
- Originates from [[Assets Locations Location City the Integration Temple the Integration Temple.svg
- Requires [SHOP00011_General_Shop_12]]
- Originates from [[Entertainment Industry]]
- Related: [[Captain Zara Stormwind
- Requires [Resonant_Crystals (Items)]]
- Affected by [[The Collector 2
- See also: [Dark Gift of Vaund the Evasive Cos]]
- Connects to [[trade-goods-xdmg (tables)
- Originates from [LORE00067_Legends_Entry_68]]
- Compare with [[Order of Azure Flame (Orders)
- Compare with
- Leads to [Gith Githzerai Mtf]]
- Compare with [[Law Enforcement (02_Worldbuilding)
- See also: [Map Map Aethermoor Harbor Skirmish V2 Aethermoor Harbor Skirmish.png]]
- See also: [[Assets Locations Location City Thorek Crystalhammer Thorek Crystalhammer.png
- Influences [Piercing Arrow Xge]]
- See also: [[INV 008
- Influences [synaptic-static-xphb (spells)]]
- Originates from [[Multi-Phase Boss Fights 2
- Compare with [step_013 (phase_082)]]
- Influences [[The_Verdant_Accord.png
- Originates from [ITEM01138_Lesser_Salve_of_Healing]]
- Related: [[LOC00223_Dungeons_Location_224

## Visual References
![03_People/portrait_deep_sea_explorer_captain_abyss_friendly.png]]
![[03_People/token_02_worldbuilding_lore_the_dream_shard_medium_normal.png
![03_People/portrait_02_worldbuilding_lore_the_dream_shard_standard.png]]
