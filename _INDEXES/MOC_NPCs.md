---
enhanced: true
tags: [enhanced, _indexes]
created: "2025-08-15T16:41:29.316644"
modified: "2025-08-15T16:41:29.316649"
aliases: [MOC NPCs]
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
- [[#Thematic Connections|Thematic Connections
- [#D&D 5e References|D&D 5e References]]

-tags: [moc, index, combat]ex]
created: 2025-08-15
---

# NPCs [[Index|Index

> Central hub for all NPCs content

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

> [!info] ℹ️ Info
> Additional context or lore

## See Also
- [[NPC00872_Thalia_Ironwood_the_Broken
- [NPC01951_Gavril_Xendar_the_Swift]]
- [[World_Primer.md
- [NPC01348_Xander_Zephyrblade_the_Wise]]
- [[NPC00373_Wynne_Frostwhisper_the_Strong
- [Sanity_Quick_Reference.md]]
- [[NPC00200_Faelyn_Winterborn_the_Guardian
- [Faction_Guide.md]]
- [[NPC00469_Delara_Oakenshield_the_Seeker
- [NPC00281_Hestara_Nightfall_the_Cunning]]
- [[NPC01568_Lyanna_Winterborn_the_Strong
- [NPC00058_Elric_Nightfall]]
- [[NPC00969_Zephyr_Keenblade_the_Wise
- [Combat_Encounter_Analysis]]
- [[NPC00069_Thalia_Brightblade_the_Guardian
- [NPC00080_Branwen_Proudmore]]
- [[Ship_Schematic_The_Seahawk.md
- [NPC00881_Qadim_Voidwalker_the_Strong]]
- [[NPC00587_Idris_Youngblood_the_Strong
- [NPC01252_Jorah_Youngblood_the_Strong]]
- [[08 Using Ability Scores
- [NPC00285_Xander_Goldleaf_the_Mystic]]
- [[Emergency_Evacuation_Map_Stormglass_Riot
- [NPC00878_Kaelen_Ironwood_the_Strong]]
- [[NPC00812_Kaelen_Jadeclaw_the_Seeker
- [Parliament of Shadows Player Guide.md]]
- [[Measurement_Guide_Depth_and_Pressur
- [NPC00133_Lyanna_Oakenshield_the_Seeker]]
- [[Archdruid Thornweaver
- [NPC01371_Xander_Stormwind_the_Guardian]]
- [[NPC01041_Thalia_Dawnstrider_the_Lost
- [MOC_Quests]]
- [[README
-

## Game Mechanics
- **Combat**: See ACX p.189-198

## Thematic Connections
- Character development and
- Social encounters and
- Faction relationships with

## D&D 5e References

*(Combat rules: ACX p.189-198)*
*(Attack rolls: ACX p.194)*
*(Damage & Healing: ACX p.196-197)*
*(Character creation: ACX p.11-15)*
*(Ability scores: ACX p.12-13)*
*(Backgrounds: ACX p.125-141)*

## Connections

- Parallels [Etheric Currents (D&D_References)]]
- Influences [[step_037 (phase_043)
- See also: [Advanced Combat Training Methods]]
- Influences [[scholars-pack-xphb (items)
- Parallels [Anchor Fortress Player]]
- Parallels [[Eldritch Mind Xphb
- Affected by [Community Integration Leader Echo Bridgewright]]
- Related: [[MON00033_Constructs_Creature_34
- Originates from [Elven Naralis Analor Mtf]]
- See also: [[Harmonic_Resonance_Evolution
- Originates from [Portrait NPC the Resonance Prophet V1 the Resonance Prophet.svg]]
- Affected by [[step_082 (phase_035)
- Compare with [Royal Government 2]]
- Leads to [[QUEST00275_Side_Quest_276
- Originates from [ITEM00359_Venomous_Sword_of_Wounding]]
- Requires [[ITEM01429_Ornate_Lantern_of_Convenience
- Compare with [04_Resources_Assets_Portraits_portrait-npc-lord-marcus-goldweaver-lord-marcus-goldweaver.svg_Quick_Ref]]
- Influences [[neogi-mpmm (aberration)
- Influences [NPC00722_Ysara_Frostwhisper_the_Scholar]]
- Influences [[LORE00158_History_Entry_159
- Parallels [mouth-of-grolantor-mpmm (giant)]]
- Compare with [[Crystal Harmony Faith
- Influences [ITEM00176_Blazing_Sword_of_Power]]
- Related: [[ENC00397_Combat_Encounter_398
- Connects to [Guardian Isolation Syndrom 2]]
- Related: [[LORE00318_Legends_Entry_319
- Connects to [Assets Locations Location City the Archive Keepers V1 the Archive Keepers.svg]]
- Related: [[Arcane Broker Void-Touch Mystic
- Influences [LORE00081_Legends_Entry_82]]
- Originates from [[The Transcended
- Influences [step_068 (phase_056)]]
- Requires [[Living Systems Suppliers
- Leads to [ring-of-elemental-command-water-xdmg (items)]]
- Connects to [[02_Worldbuilding_Items_Lightstone_Scanners
- See also: [Brightward Security Solutions (D&D_References)]]
- Influences [[Symbol Heraldry Tem... Related To: Local Political Structure Connected Plots: to Be Developed
- Connects to [Cross-Realm Research Coalition (Groups)]]
- Parallels [[step_088 (phase_080)
- See also: [Mage Hand Xphb]]
- Originates from [[awakened-tree-xmm (plant)
- Leads to [step_078 (phase_013)]]
- Originates from [[step_061 (phase_068)
- See also: [Current Harvestsage]]
- Parallels [[Assets Locations Location City Memory Thief Memory Thief.svg
- Requires [SHOP00060_General_Shop_61]]
- Connects to [[Disinformation Specialists
- Originates from [step_024 (phase_023)]]
- Connects to [[Assets Locations Location City Coral Vortextrader V1 Coral Vortextrader.svg
- Related: [Assets Locations Location City Current Harvestsage Current Harvestsage.svg]]
- Requires [[NPC01363_Elric_Oakenshield_the_Lost
- See also: [step_033 (phase_065)]]
- Leads to [[rat-xmm (beast)
- Connects to [The Crystal Watchers]]
- Affected by [[barrack
- Influences [NPC00683_Cedric_Underhill_the_Lost]]
- Parallels [[step_069 (phase_068)
- Parallels [Height and Weight Vgm]]
- Parallels [[Merchant Prince Marcus Goldflow (D&D_References)
- Parallels [Creature Creature Goblin Warrior Xmm V4 Goblin Warrior Xmm.png]]
- Parallels [[ENC00426_Combat_Encounter_427
- Requires [ENC00207_Social_Encounter_208]]
- Connects to [[LORE00242_History_Entry_243
- See also: [Weapons Trader Gareth Steelmerchant]]
- Parallels [[stench-kow-mpmm (fiend)
- See also: [QUEST00063_Side_Quest_64]]
- See also: [[SPELL00075_Nature_Spell_76
- Parallels [Crystal Wardens Order]]
- Related: [[SPELL0042_Eldritch_Wave
- Leads to
- Related:
- Originates from [Interfaith Community Centers]]
- Parallels [[step_083 (phase_032)
- Connects to [The Sunken Cathedral of Perfect Order (D&D_References)]]
- Originates from [[candle-of-invocation-xdmg (items)
- Connects to [Scroll Mishaps]]
- Requires [[step_051 (phase_061)
- Originates from [SPELL0027_Mystic_Blessing]]
- Affected by [[Assets Locations Location City Secondary Education V1 Secondary Education.svg
- Related: [Merged Magic 2]]
- Originates from [[Evidence Types Guide
- Influences [Magnus Ledgerkeep]]
- See also: [[Portrait NPC the Heart of Oceanus the Heart of Oceanus.svg
- Parallels [LOC00131_Cities_Location_132]]
- Originates from [[step_046 (phase_066)
- Affected by [death-saving-throw-xphb (variant-rules)]]
- Related: [[Paper Whirlwind Rot
- Compare with [Ring of Three Wishes Xdmg]]
- Connects to [[step_049 (phase_085)
- Requires [ITEM01231_Refined_Potion_of_Healing]]
- Parallels
- Parallels
- Compare with [[LORE00251_Legends_Entry_252
- Leads to [step_086 (phase_098)]]
- Affected by [[Sentient Magic Item Senses
- Requires [The Nexus of All Possibilities]]
- See also: [[The Prismatic Order
- Requires [Deep Stone Eaters (D&D_References)]]
- Related: [[step_033 (phase_064)
- Parallels [Location City Lady Vivienne the Unfrozen Lady Vivienne the Unfrozen.svg]]
- Influences [[Dwarven Valkauna Mtf

## Visual References
![03_People/portrait_important_npcs_standard.png]]
![[03_People/portrait_character_relationship_web_core_npcs.png
![03_People/portrait_important_npcs_dramatic.png]]

## Plot Hooks
- A mysterious message arrives regarding this location
- Rumors speak of hidden treasures nearby
- Strange occurrences have been reported recently
