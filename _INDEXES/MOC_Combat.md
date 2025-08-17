---
enhanced: true
tags: [enhanced, _indexes]
created: "2025-08-15T16:41:29.307818"
modified: "2025-08-15T16:41:29.307820"
aliases: [MOC Combat]
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

# Combat Index

> Central hub for all Combat content

## Quick Links
- [[MASTER_MOC|← Back to Master]]

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
- [[NPC00162_Xander_Thornweave
- [NPC01466_Urien_Nightfall_the_Guardian]]
- [[NPC00276_Ysara_Youngblood
- [Party_Quests]]
- [[NPC00804_Xander_Frostwhisper_the_Cunning
- [NPC00259_Delara_Proudmore]]
- [[NPC00655_Jorah_Darkwater_the_Seeker
- [Ritual_Timing_Wheel_Convergenc]]
- [[NPC00501_Orion_Nightfall_the_Broken
- [NPC00451_Malakai_Ravenheart_the_Broken]]
- [[NPC01827_Kaelen_Ironforge_the_Seeker
- [NPC00975_Lyanna_Winterborn_the_Wise]]
- [[12 Spells
- [NPC00437_Hilda_Stormwind_the_Mystic]]
- [[NPC01877_Hestara_Moonshadow_the_Mystic
- [NPC01841_Malakai_Nightfall_the_Wise]]
- [[Ceasefire_Accord_Draft.md
- [Trade_Route_Map_Aquabyssos_to_Aethermoor]]
- [[NPC00083_Vesper_Xendar_the_Lost
- [NPC00200_Faelyn_Winterborn_the_Guardian]]
- [[NPC00749_Xander_Quicksilver
- [NPC00878_Kaelen_Ironwood_the_Strong]]
- [[NPC00838_Drusilla_Proudmore_the_Risen
- [Sage Elara]]
- [[NPC01013_Corvus_Ravenheart_the_Bold
- [NPC00815_Baelor_Thornweave_the_Swift]]
- [[NPC00057_Malakai_Stormwind_the_Cunning
- [The_Corroded_Crown.png]]
- [[NPC00601_Vesper_Ironwood_the_Guardian
- [NPC01360_Ewan_Blackstone_the_Strong]]
- [[NPC01870_Lyanna_Silverleaf_the_Cunning
- [NPC01041_Thalia_Dawnstrider_the_Lost]]
- [[NPC00307_Dara_Proudmore_the_Seeker
- [10 Combat]]
- [[Combat_Encounter_Analysis
- [MOC_NPCs]]
- [[Character_Journals
- [11 Rules Glossary]]
- [[NPC_Relationship_Web.png_1 (03_People)
- [Smuggler_Route_Tally_Shee]]
- [[NPC01040_Zephyr_Lightbringer_the_Strong
- [Quick_Start_Guide]]
- [[11 Spellcasting
- [Session_Recaps]]
- [[Character_Journal_Template
- [07 Customization Options]]
- [[README
- [MOC_Sessions]]
- [[MOC_Locations
- [MOC_Lore]]
- [[MOC_Quests
-

## Game Mechanics
- **Combat**: See ACX p.189-198

## Thematic Connections
- Tactical combat using [Combat Maneuvers]]
- Environmental hazards from [[Battlefield Terrain
- Victory conditions beyond [Death and Dying]]

## D&D 5e References

*(Combat rules: ACX p.189-198)*
*(Attack rolls: ACX p.194)*
*(Damage & Healing: ACX p.196-197)*

## Connections

- Leads to [[Dr Aquarius Brightwater
- Compare with [step_050 (phase_020)]]
- Influences [[handout-handout-docking-permit-docking-permit.png
- Related: [02_Worldbuilding_Places_Thalassopolis_Ruins]]
- Compare with [[Research Director Past Future (D&D_References)
- See also:
- Affected by [NARRATIVE_DEEPENING_MASTER_PROMPT]]
- See also: [[Keeper of Secrets Whisper Darkhold
- Affected by [Pressure's End]]
- Compare with [[Deep Current Pirates
- Originates from [Assets Locations Location City Doctor Silas Voidtouch Doctor Silas Voidtouch.svg]]
- Originates from [[Instructor Combat Shadow
- See also: [portrait-npc-the-wake-v1-the-wake.svg_1 (Portraits)]]
- Originates from [[X-103_Leviathan_Mirror_Chase
- Related: [step_016 (phase_071)]]
- Related: [[SPELL0005_Celestial_Bolt
- Leads to [University Philosophy Departments]]
- Originates from [[SPELL00005_Divine_Spell_6
- Requires [Portrait NPC Sacred Healing Gardens Sacred Healing Gardens.svg]]
- Connects to [[Artificer (D&D_References)
- Compare with [QUEST00171_Personal_Quest_172]]
- Related: [[MON00087_Constructs_Creature_88
- Affected by
- Connects to [LORE0040_History_of_the_First_King]]
- Connects to [[Shadow Surgeons Collective
- Affected by [NPC00369_Alaric_Goldleaf_the_Wanderer]]
- Parallels [[ITEM00734_Divine_Mirror_of_Destiny
- Originates from [jakarions-staff-of-frost-cos (items)]]
- Influences [[step_046 (phase_076)
- Originates from [QUEST00044_Personal_Quest_45]]
- Originates from [[Cultist Leader Depth
- Leads to [step_043 (phase_008)]]
- Affected by [[step_072 (phase_092)
- Leads to [step_028 (phase_086)]]
- Affected by [[Assets Locations Location City the Vote Vault Mystery the Vote Vault Mystery.svg
- See also: [The Umbral Community Center]]
- Affected by [[Tower of Echoes (D&D_References)
- Affected by [Assets Locations Location City Ancient Treasury of Tides V1 Ancient Treasury of Tides.svg]]
- Leads to [[step_082 (phase_037)
- Influences [Concierge Phillip Gracewater (D&D_References)]]
- Connects to [[step_092 (phase_079)
- Connects to [ioun-stone-absorption-xdmg (items)]]
- Leads to [[ITEM0109_Forgotten_Gauntlet_of_the_Dawn
- Influences [Information Broker Whisper Goldtongu (D&D_References)]]
- Parallels [[Goldwave Manor 3 (D&D_References)
- Related: [step_068 (phase_015)]]
- Requires [[rewards
- Affected by [DM Screen]]
- Leads to [[Lumengarde Republi
- Compare with [step_027 (phase_060)]]
- Leads to [[QUEST00006_Main_Quest_7
- Related: [Location City Foreign Affairs V1 Foreign Affairs.svg]]
- Leads to [[NPC00161_Qadim_Winterborn
- Compare with [step_019 (phase_067)]]
- Requires [[Portrait NPC Sunk... Connected To: Regional Politics and Trade Related Locations: Nearby Settlements
- Influences [step_059 (phase_092)]]
- Influences [[step_078 (phase_073)
- See also: [agonizing-blast-xphb (optional-features)]]
- Requires [[Blink Xphb
- Influences [Symbol Heraldry Factional Conflicts Factional Conflicts.svg_1 (Symbols)]]
- Affected by [[Shadow_Separation_Syndrome
- Connects to [Protocol Specialist Sarah Ceremonial (D&D_References)]]
- Influences [[LORE00075_Prophecies_Entry_76
- Related: [step_028 (phase_089)]]
- Originates from [[step_022 (phase_094)
- Affected by [QUEST00045_Personal_Quest_46]]
- Requires [[step_067 (phase_030)
- Connects to [Assets Locations Location City Exotic Imports Market V1 Exotic Imports Market.svg]]
- Requires [[Location City Keeper Stormwall V1 Keeper Stormwall.svg
- Originates from [step_084 (phase_018)]]
- Influences [[The Seven Shards Prophecy
- Originates from [Embassy Quarter]]
- Requires [[devouring-blade-xphb (optional-features)
- Originates from [Master Tidal Engineer Coral Wavewright (D&D_References)]]
- Originates from [[Archmage Velina Duskweaver
- Requires [Scepter of Tidal Command (D&D_References)]]
- Requires [[ENC00284_Combat_Encounter_285
- Affected by [ENC00080_Combat_Encounter_81]]
- Related: [[ENC00081_Combat_Encounter_82
- Related: [ENC00031_Social_Encounter_32]]
- See also: [[LORE00292_Prophecies_Entry_293
- Connects to [QUEST00185_Side_Quest_186]]
- Compare with [[Wand of Fireballs Xdmg
- See also: [step_088 (phase_028)]]
- Requires [[Finn Goodtide
- Originates from [QUEST00071_Personal_Quest_72]]
- Originates from [[Artisan Collective
- Parallels [LORE00007_Legends_Entry_8]]
- Originates from [[step_021 (phase_090)
- Connects to [ITEM00001_Venomous_Dagger_of_the_Ancients]]
- Leads to [[QUEST00057_Personal_Quest_58
- See also: [step_066 (phase_075)]]
- Leads to [[NPC01059_Dara_Goldleaf_the_Wise
- Connects to [Cleric Xphb War Domain Xphb]]
- Related: [[Terrestrial Coalition (D&D_References)
- Influences [The Echo Chambers]]
- Originates from [[tiefling-baalzebul-mtf (races)
- Requires [International Law Enforcement]]
- Compare with [[Crystal Festival (D&D_References)
- Influences [monsters-by-habitat-mountain-monsters-xmm (tables)]]

## Visual References
![[03_People/portrait_10_combat_dropping_to_0_hit_points_death_saving_throws_standard.png
![03_People/portrait_10_combat_dropping_to_0_hit_points_death_saving_throws_dramatic.png]]
![[03_People/portrait_10_combat_dropping_to_0_hit_points_stabilizing_a_creature_standard.png]]
