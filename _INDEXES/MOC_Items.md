---
enhanced: true
tags: [enhanced, _indexes]
created: "2025-08-15T16:41:29.321058"
modified: "2025-08-15T16:41:29.321061"
aliases: [MOC Items]
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

# [[Items|Items Index

> Central hub for all Items content

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
- [[NPC01252_Jorah_Youngblood_the_Strong
- [NPC01682_Vesper_Blackstone_the_Guardian]]
- [[NPC_Relationship_Web.png_1 (03_People)
- [NPC01781_Urien_Keenblade_the_Cunning]]
- [[Ritual_Timing_Wheel_Convergenc
- [10 Combat]]
- [[Archdruid Thornweaver
- [MOC_Rules]]
- [[Reference.md
-

## Game Mechanics
- **Combat**: See ACX p.189-198

## D&D 5e References

*(Combat rules: ACX p.189-198)*
*(Attack rolls: ACX p.194)*
*(Damage & Healing: ACX p.196-197)*

## Connections

- See also: [04_Resources_Assets_Locations_location-city-terminal-director-admiral-current-swiftflow-v1-terminal-director-admiral-current-swiftflow.svg]]
- Originates from [[Control Systems Engineer Flow Processwright
- Influences [ITEM00453_Enchanted_Gauntlets_of_Fortitude]]
- Parallels [[Dr. Torres Investigation
- Related: [Location City the Floating Market V1 the Floating Market.svg]]
- Originates from [[Neural Key
- Connects to [step_062 (phase_051)]]
- Influences [[Magmin Xmm
- Requires [United Councils of Both Worlds]]
- Influences [[Chaplain Father Blessing Hopekeeper (D&D_References)
- Leads to [Portrait NPC Memory Commerce V1 Memory Commerce.svg_1 (Portraits)]]
- Influences [[travel-xphb (tables)
- Connects to [Houses_and_Nobility___House_Brightshield]]
- Leads to [[Memory Merchant Valeria 2
- Parallels [Veiled Hierophant (D&D_References)]]
- Compare with [[LOC00106_Cities_Location_107
- Leads to [demon-customization-tables-demon-flaws-mtf (tables)]]
- Requires [[ITEM00104_Venomous_Staff_of_Slaying
- Affected by [Surface Contact Prohibition (D&D_References)]]
- Requires [[step_084 (phase_013)
- Related: [ENC00150_Combat_Encounter_151]]
- Related: [[QUEST00012_Personal_Quest_13
- Connects to [World_State]]
- Parallels [[Crystal Addiction Victims
- Parallels [ITEM00146_Venomous_Axe_of_Wounding]]
- Connects to [[greyhawk-iuz-xdmg (deities)
- Affected by [Sorrow-Root Nightbloom]]
- Compare with [[Symbol Heraldry Ste... Related To: Local Political Structure Connected Plots: to Be Developed
- Originates from [Current Solidarity (D&D_References)]]
- Influences [[Assets Locations Location City Quality Inspector Reef Perfectwright Quality Inspector Reef Perfectwright.svg
- Affected by [EVENT00067_Magical_Event_68]]
- Influences [[SPELL00067_Divine_Spell_68
- Related: [Location City the Sunken Senate the Sunken Senate.svg]]
- Affected by [[Paladin Xphb Oath of Glory Xphb
- Originates from [NPC01001_Solas_Dawnstrider_the_Redeemed]]
- Influences [[step_003 (phase_100)
- Influences [step_023 (phase_030)]]
- Requires [[Celestial Gardens
- Connects to [The Quantum Accountant (D&D_References)]]
- Requires [[step_022 (phase_009)
- Originates from
- Originates from [step_056 (phase_031)]]
- Leads to [[Assets Locations Location City Victoria Harbormane Victoria Harbormane.svg
- Parallels [location-city-the-deepmind-the-deepmind.svg]]
- Originates from [[Reputation_Tracker
- Related: [The Aether Works 2]]
- See also: [[Assets Locations Location City Conservatory of Memory Conservatory of Memory.svg
- Affected by [step_054 (phase_010)]]
- Affected by [[14 Chapter 14 the Labyrinth
- Connects to [FAC00041_Cults_42]]
- Parallels [[archive
- Parallels [step_038 (phase_081)]]
- Influences [[Outer Planes Phb
- Requires [LORE00137_Prophecies_Entry_138]]
- Connects to [[ENC00088_Environmental_Encounter_89
- Influences
- Parallels [09-adventuring#Movement#Difficult Terrain]]
- Originates from [[QUEST0073_The_Crystal_Cave_Invasion
- Parallels [The Fishing Fleets 2]]
- Related: [[LOC00253_Planes_Location_254
- Connects to [Describe Appearance and Personality Wisdom]]
- Related: [[step_014 (phase_076)
- Compare with [energy-cell-xdmg (items)]]
- Compare with [[step_041 (phase_049)
- Parallels [Portrait NPC Current Lord Triton of House Pelagios Current Lord Triton of House Pelagios.svg]]
- Compare with [[step_065 (phase_010)
- Related: [ITEM00862_Void-touched_Crown_of_Eternity]]
- Related: [[02_Worldbuilding_People_Portal_Engineer_Shade_Linkwright
- Leads to [Enfeebling Arrow Xge]]
- Connects to [[Symbol Heraldry Hea... Related To: Local Political Structure Connected Plots: to Be Developed
- Affected by [NPC01155_Drusilla_Brightblade_the_Wanderer]]
- Affected by
- See also: [[Compass Quest
- Affected by [step_078 (phase_023)]]
- Affected by [[Merchant Marine Consortium
- Parallels [Location City Freedrift Network Freedrift Network.svg]]
- Related: [[Scholar Thomas Precedent (D&D_References)
- Originates from [QUEST00205_Personal_Quest_206]]
- Parallels [[LORE00227_History_Entry_228
- See also: [NPC00358_Vesper_Lightbringer]]
- Influences [[step_051 (phase_015)
- Originates from [QUEST00404_Side_Quest_405]]
- Affected by [[Deep Mother Cult Practices (D&D_References)
- Leads to [step_069 (phase_095)]]
- Affected by [[Compass Quest 2
- Originates from [NPC00286_Zephyr_Zephyrblade]]
- Originates from [[Portrait NPC Captain Torren Stormwright V1 Captain Torren Stormwright.svg
- Leads to [ITEM0145_Blessed_Crown_of_Shadows]]
- Related: [[bard-xphb-college-of-whispers-xge (classes)
- Affected by [step_091 (phase_011)]]
- Leads to [[Risk Assessor Probability (D&D_References)
- Compare with [Shadow Integration Policy 2]]
- Related: [[coral-xdmg (items)
- See also: [Handout Handout Noble Writ with Wax Seal V2 Noble Writ with Wax Seal.png]]
- Related: [[Assets Locations Location City International Relations V1 International Relations.svg
- Related: [NPC01971_Zephyr_Grimholt_the_Strong]]
- Parallels [[Determine Your Xp Budget Xp Budget Per
- Requires [FAC00064_Guilds_65]]
- Leads to [[ITEM01351_Ornate_Lantern_of_Reliability
- Parallels [Marcus the Shade Blackwood]]

## Visual References
![[04_Resources/Assets/Placeholder Images/WeaponsArmorItemsTitleBar.png
![04_Resources/Assets/Items/items_aquabyssos_1755205562148.png]]
![[04_Resources/Assets/Items/02_worldbuilding_items_group_conference_mirrors.png]]
