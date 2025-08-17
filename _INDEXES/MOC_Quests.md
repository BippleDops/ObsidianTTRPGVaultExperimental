---
enhanced: true
tags: [enhanced, _indexes]
created: "2025-08-15T16:41:29.303576"
modified: "2025-08-15T16:41:29.303579"
aliases: [MOC Quests]
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

# [[Quests|Quests Index

> Central hub for all Quests content

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

> [!tip] 💡 Tip
> Useful information for players

## See Also
- [[NPC00703_Elric_Dawnstrider_the_Swift]]
- [[NPC01937_Felicia_Silverleaf_the_Wanderer]]
- [[NPC01195_Gareth_Keenblade_the_Guardian]]
- [[NPC01057_Pyria_Quicksilver_the_Scholar]]
- [[NPC00761_Aldric_Moonshadow_the_Guardian]]
- [[NPC01931_Thalia_Lightbringer_the_Fallen]]
- [[NPC01812_Xander_Lightbringer_the_Swift]]
- [[NPC00415_Gareth_Winterborn_the_Bold]]
- [[NPC00599_Cedric_Lightbringer_the_Wise]]
- [[NPC01504_Erasmus_Zephyrblade_the_Strong]]
- [[NPC00812_Kaelen_Jadeclaw_the_Seeker]]
- [[MOC_Sessions]]
- [[MOC_Locations]]
-

## Game Mechanics
- **Combat**: See ACX p.189-198

## D&D 5e References

*(Combat rules: ACX p.189-198)*
*(Attack rolls: ACX p.194)*
*(Damage & Healing: ACX p.196-197)*

## Connections

- Connects to [[dire-troll-mpmm (giant)
- Affected by [Portrait NPC Captain Storm Ambushmaster V1 Captain Storm Ambushmaster.svg]]
- Leads to [[Emergency Combat Procedures]]
- Requires [[The Overflow (D&D_References)]]
- See also:
- Influences [[Surface Signals 2
- See also: [Tome of Clear Thought Xdmg]]
- Influences [[step_067 (phase_091)
- Originates from [LOC00266_Dungeons_Location_267]]
- Leads to [[The Masked Broker
- Affected by [step_085 (phase_069)]]
- Connects to [[Magic Item Special Features Magic Minor Property Xdmg
- Influences [City Council of Aquabyssos]]
- Requires [[The Coral Courts (D&D_References)
- Leads to [Holy Symbol Varies Holy Symbols Xphb]]
- Originates from [[barbarian-xphb-path-of-the-ancestral-guardian-xge
- Influences [step_040 (phase_098)]]
- Related: [[Lord Aurelius Voidcrown
- Leads to [Crystal_Corruption_Stages]]
- Influences [[Assets Locations Location City Depth Warden Patrol Depth Warden Patrol.svg
- Originates from [Location City Elder Scribe Marcus the Lost V1 Elder Scribe Marcus the Lost.svg]]
- Requires [[underdark-encounters-levels-14-xge (tables)
- See also: [04_Places_Hall_of_Mirrors]]
- Leads to [[The Sunken Library of Thalassius]]
- Requires [[Master_Campaign_Index 2
- Connects to [Location City Concierge Phillip Gracewater Concierge Phillip Gracewater.svg]]
- Related: [[Crystal Laboratory
- Compare with [Memorial Mason Kane]]
- Affected by [[QUEST00479_Side_Quest_480
- Compare with [Merged Zone Navigation]]
- Originates from [[step_059 (phase_018)
- Parallels [half-orc-names-male-xge (tables)]]
- See also: [[LOC00192_Planes_Location_193
- Affected by [item-artifact-mess-kit-v7-mess-kit.png]]
- Affected by
- Compare with [[hellish-rebuke-xphb (spells)
- Related: [Centaur Warden Xmm]]
- Connects to [[Spy-Master Nonentity (D&D_References)]]
- Parallels [[LOC0105_LowerHaven
- Related: [The Glass Twins]]
- Parallels [[Session 05 (Crystal_Plague)
- Related: [Assets Symbols Symbol Heraldry Information Exchanges Information Exchanges.svg]]
- Compare with [[Player Characters as Lycanthropes Mm]]
- Affected by [[step_085 (phase_007)
- Connects to [step_003 (phase_058)]]
- Affected by [[ITEM00101_Shadow_Staff_of_Speed
- Related: [step_072 (phase_035)]]
- Influences [[Portrait NPC Sister Thalassa the Depth Touched V2 Sister Thalassa the Depth Touched.svg_1 (Portraits)
- Compare with
- Originates from [Courier Chief Swift Currentrider]]
- Related: [[Vault Breach (D&D_References)
- Affected by [02_Worldbuilding_Items_Lightstone_Scanners]]
- Influences [[Assets Portraits Portrait NPC the Emperor S Memories the Emperor S Memories.svg
- Requires [Aethermoor Council 2]]
- Originates from [[step_100 (phase_019)
- Influences
- Connects to [LORE00157_Prophecies_Entry_158]]
- Connects to [[Prince Aurelius (D&D_References)]]
- Related: [[step_014 (phase_080)
- Parallels [step_050 (phase_081)]]
- Leads to [[Community Demonstration Sites (D&D_References)]]
- Leads to
- See also: [[Aquabyssos_1
- Parallels [step_097 (phase_059)]]
- Requires [[step_031 (phase_009)
- See also:
- Compare with [LORE00157_Legends_Entry_158]]
- Related: [[Resonance Peaks (D&D_References)]]
- Connects to [[Identity Preservation Crystal 2
- Requires
- See also: [step_037 (phase_045)]]
- Requires [[step_041 (phase_037)
- Influences [location-city-royal-quarters-royal-quarters.svg]]
- Compare with [[FAC00052_Guilds_53
- Related: [cow-xdmg (items)]]
- Originates from [[black-dragon-wyrmling-xmm (dragon)
- Leads to [DUN00062_Dungeon_63]]
- Compare with [[International Trade Agreements 2]]
- Related: [[step_007 (phase_026)
- Requires [ITEM00960_Concentrated_Herb_of_Clarity]]
- Influences [[step_028 (phase_049)
- Parallels [ITEM00384_Cursed_Staff_of_Speed]]
- Related:
- Related: [[Philter of Love Xdmg
- Affected by [Player Handouts]]
- See also: [[Assets Locations Location City the Probability Merchant the Probability Merchant.svg
- Related: [ITEM00546_Ethereal_Helm_of_Fortitude]]
- Parallels [[Community Leaders (D&D_References)]]
- See also: [[step_035 (phase_045)
- Leads to [Fangs of the Fire Snake]]