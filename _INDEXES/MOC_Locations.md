---
enhanced: true
tags: [enhanced, _indexes]
created: "2025-08-15T16:41:29.233422"
modified: "2025-08-15T16:41:29.233428"
aliases: [MOC Locations]
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

# [[locations|Locations Index

> Central hub for all Locations content

## Quick Links
- [MASTER_MOC|← Back to Master]]

## Content
*Building index...*

> [!dm] DM Note
> This location connects to the main plot

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
## See Also
- [[MASTER_NAVIGATION
- [City_District_Map_Port_Meridian_Harbo]]
- [[NPC01552_Branwen_Lightbringer_the_Swift
- [NPC00461_Branwen_Proudmore_the_Strong]]
- [[NPC01911_Alaric_Oakenshield_the_Mystic
- [NPC01476_Qadim_Stormwind_the_Wise]]
- [[NPC01301_Jorah_Underhill_the_Broken
- [NPC00920_Malakai_Ravenheart_the_Guardian]]
- [[06 Equipment
- [NPC00469_Delara_Oakenshield_the_Seeker]]
- [[NPC00812_Kaelen_Jadeclaw_the_Seeker
- [NPC00804_Xander_Frostwhisper_the_Cunning]]
- [[NPC01892_Gareth_Xendar_the_Scholar
- [Player_Portal.md]]
- [[09 Adventuring
- [NPC00451_Malakai_Ravenheart_the_Broken]]
- [[NPC01503_Ewan_Dawnstrider_the_Redeemed
- [NPC00080_Branwen_Proudmore]]
- [[NPC00844_Cedric_Blackstone_the_Fallen
- [NPC01664_Pyria_Lightbringer_the_Redeemed]]
- [[NPC00669_Zephyr_Youngblood_the_Lost
- [NPC00207_Ysara_Ravenheart]]
- [[NPC01360_Ewan_Blackstone_the_Strong
- [NPC00324_Idris_Hawthorne_the_Strong]]
- [[10 Appendix B Creature Stat Blocks
- [11 Spellcasting]]
- [[NPC01286_Xander_Proudmore_the_Bold
- [10 Combat]]
- [[NPC01082_Fiora_Ashford_the_Fallen
- [Concept_Map]]
- [[Trade_Route_Chart_Port_Meridia
- [NPC00307_Dara_Proudmore_the_Seeker]]
- [[NPC01613_Kaelen_Voidwalker_the_Wanderer
- [NPC01312_Alaric_Darkwater_the_Fallen]]
- [[NPC00101_Caelum_Hawthorne
- [README]]
- [[NPC01761_Idris_Moonshadow_the_Broken
- [NPC00058_Elric_Nightfall]]
- [[MOC_Sessions
-

## Game Mechanics
- **Combat**: See ACX p.189-198

## D&D 5e References

*(Combat rules: ACX p.189-198)*
*(Attack rolls: ACX p.194)*
*(Damage & Healing: ACX p.196-197)*

## Connections

- Parallels [portrait-npc-the-tidecaller-v1-the-tidecaller.svg_1 (Portraits)]]
- Affected by [[All NPCs
- See also: [step_092 (phase_042)]]
- Related: [[Artificer-General Magnus Gemheart
- Leads to [NPC01228_Brenna_Crystalbrook_the_Scholar]]
- Related: [[step_066 (phase_045)
- Related: [The Crystal Renaissance 2]]
- Affected by [[Depth Enforcers
- Compare with [ITEM00327_Shadow_Dagger_of_Slaying]]
- Compare with [[QUEST0070_The_Sacred_Heir
- Leads to [ochre-jelly-xmm]]
- Requires [[step_035 (phase_053)
- Related: [Magister Voidheart]]
- Leads to [[step_023 (phase_078)
- Parallels [Assets Locations Location City Pressure Brewing Technology Pressure Brewing Technology.svg]]
- Compare with
- Connects to
- Originates from [[NPC00493_Lyanna_Proudmore_the_Wanderer
- See also: [LORE00164_Prophecies_Entry_165]]
- See also: [[arcane-eye-xphb (spells)
- Connects to [Location City Freedrift Network V1 Freedrift Network.svg]]
- Parallels [[00_Indexes_Documentation
- Parallels [LORE00247_Prophecies_Entry_248]]
- Requires [[step_095 (phase_093)
- Leads to [Assets Locations Location City Acolyte Sister Tidal Deepfaith Acolyte Sister Tidal Deepfaith.svg]]
- Originates from [[LORE00027_Prophecies_Entry_28
- See also: [Princess Luminara (D&D_References)]]
- See also: [[ITEM00923_Pure_Elixir_of_Clarity
- Influences [step_045 (phase_045)]]
- Requires [[Void Realm Territories
- Affected by [Portrait NPC Find the Shadow Cure V2 Find the Shadow Cure.svg_1 (Portraits)]]
- Compare with [[LOC00245_Planes_Location_246
- Influences [QUEST00029_Side_Quest_30]]
- See also: [[Vehicle Ship Coral Frame Diver Tender V1 Coral Frame Diver Tender.svg
- Related: [Location City the Banker Fish V1 the Banker Fish.svg]]
- Leads to [[air-elemental-xmm (elemental)
- Requires [Unified Mechanics Guide (D&D_References)]]
- Originates from [[step_083 (phase_033)
- Related: [LOC00242_Wilderness_Location_243]]
- Influences [[venomous-snake-xmm
- Requires [Madame Pearl Currentflow (D&D_References)]]
- See also: [[Assets Locations Location City Constitutional Monarchy V1 Constitutional Monarchy.svg
- Parallels [MON00133_Constructs_Creature_134]]
- Compare with [[Festival Calendar Complete
- Parallels [step_012 (phase_056)]]
- Compare with [[earthbind-xge (spells)
- Parallels [dungeon-creator-cults-and-religions (tables)]]
- Originates from [[Corruption Tracking
- Leads to [MON00136_Aberrations_Creature_137]]
- Compare with [[step_090 (phase_007)
- Requires [Ersatz Eye Xdmg]]
- Affected by [[Unicorn Xmm (legendary-group)
- Leads to [Luminous Sterling 2]]
- Originates from [[QUEST00249_Personal_Quest_250
- Connects to [Assets Locations Location City the Phosphor Markets V1 the Phosphor Markets.png]]
- Requires [[MON00043_Undead_Creature_44
- Requires [11 Chapter 11 Gravenhollow]]
- Connects to [[ITEM00919_Superior_Salve_of_Vigor
- Parallels [ITEM01059_Lesser_Elixir_of_Vigor]]
- Requires [[Location City Whisper Translation Whisper Translation.svg
- Compare with [Portrait NPC Jasper Three Eyes Flint 2 Jasper Three Eyes Flint 2.svg]]
- Connects to [[Progressive Movement Infiltration 2
- Parallels [LORE00188_Prophecies_Entry_189]]
- Related: [[step_058 (phase_056)
- Affected by [Shadow Enhancement Elixirs]]
- Compare with [[Inter-Realm Trade Protocol 2
- Influences [The Academy of Fundamental Truths]]
- Related: [[step_018 (phase_010)
- Related: [Aquatic Biology Laboratory]]
- Connects to [[Living the Giant Life Giant Life Spans Vgm
- Related: [Memory Pearls]]
- Leads to [[Crystal Palace Complex (D&D_References)
- Parallels [step_013 (phase_060)]]
- Related: [[hide-armor-xphb (items)
- See also: [step_076 (phase_076)]]
- Parallels [[sailing-ship-xphb (items)
- Leads to [Paladin Xphb Oathbreaker Dmg]]
- Influences [[QUEST00093_Personal_Quest_94
- See also: [step_077 (phase_019)]]
- See also: [[Paradox Traps
- Originates from [Location City Merchant Prince Goldwind Crysalborn V1 Merchant Prince Goldwind Crysalborn.svg]]
- Requires [[NPC_Template_1 (09_Templates)
- Influences [Duergar in the World Duergar Quirks Mtf]]
- Influences [[Locations Abyssal Forges
- Originates from [step_008 (phase_066)]]
- Compare with
- Parallels [[Diplomatic Minister Reef (D&D_References)
- See also: [ENC00073_Combat_Encounter_74]]
- Leads to [[LOC00011_Wilderness_Location_12
- See also:
- Compare with
- Originates from [Voices from Below (D&D_References)]]
- See also: [[ITEM00716_Ancient_Orb_of_Destiny
- Parallels [Abyssos Prime Upper Districts (D&D_References)]]
- Parallels [[step_023 (phase_076)
- Parallels [chamber-purpose-dungeon-maze (tables)]]
- See also: [[QUEST00461_Side_Quest_462
- Connects to [The Hammer Squad]]
- Leads to [[swarm-of-bats-xmm (beast)
- Related: [Portrait NPC the Shadow Warren V2 the Shadow Warren.svg]]

## Visual References
![[03_People/portrait_assets_locations_location_city_professor_marina_reefbuilder_professor_marina_reefbuilder_svg_standard.png
![03_People/portrait_assets_locations_location_city_quartermaster_sterling_suppystone_quartermaster_sterling_suppystone_svg_friendly.png]]
![[03_People/portrait_assets_locations_location_city_reef_guard_captain_torrent_shellborn_v1_reef_guard_captain_torrent_shellborn_svg_standard.png]]

## Plot Hooks
- A mysterious message arrives regarding this location
- Rumors speak of hidden treasures nearby
- Strange occurrences have been reported recently
