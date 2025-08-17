---
enhanced: true
tags: [enhanced, _indexes]
created: "2025-08-15T16:41:29.291954"
modified: "2025-08-15T16:41:29.291958"
aliases: [MOC Rules]
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

# Rules Index

> Central hub for all Rules content

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

> [!tip] 💡 Tip
> Useful information for players

## See Also
- [[NPC_Relationship_Web.png_1 (03_People)
- [NPC01699_Orion_Oakenshield_the_Broken]]
- [[NPC00259_Delara_Proudmore
- [NPC01177_Thalia_Underhill_the_Fallen]]
-

## Game Mechanics
- **Combat**: See ACX p.189-198

## D&D 5e References

*(Combat rules: ACX p.189-198)*
*(Attack rolls: ACX p.194)*
*(Damage & Healing: ACX p.196-197)*

## Connections

- See also: [[NPC01436_Zephyr_Moonshadow_the_Mystic
- Related: [DUN00084_Dungeon_85]]
- See also: [[location-city-withered-court-v1-withered-court.svg
- Influences [step_078 (phase_097)]]
- Compare with [[ITEM00645_Ethereal_Leather_of_the_Guardian
- Originates from [black-pearl-xdmg (items)]]
- Leads to [[Creature Creature Githyanki Knight Xmm V3 Githyanki Knight Xmm.png
- Leads to [step_075 (phase_044)]]
- Influences [[Embassy Districts
- Originates from [Master Illusion Kyrian Mindweaver]]
- Influences [[MON00095_Constructs_Creature_96
- Parallels [ITEM0102_Glorious_Tome_of_the_Dawn]]
- Compare with [[blue-abishai-mpmm (fiend)
- Related: [Merchant Prince Goldwind Crysalborn (D&D_References)]]
- See also: [[Assets Portraits Portrait NPC Quest the Sanctuary S Secret Quest the Sanctuary S Secret.svg
- Influences [Memory of Heroes]]
- Influences [[LOC00107_Cities_Location_108
- Compare with [Krake (D&D_References)]]
- Originates from [[step_013 (phase_063)
- See also: [Assets Portraits Portrait NPC Quest the Kingpin S Fall Quest the Kingpin S Fall.svg]]
- See also: [[LOC00044_Planes_Location_45
- Influences [Stone Giant Xmm]]
- Originates from
- Leads to
- Affected by [[step_056 (phase_089)
- Related:
- Connects to [Drill Commander Titanius Ironcrystal 2]]
- Originates from [[step_094 (phase_050)
- See also:
- Leads to [step_008 (phase_009)]]
- Compare with [[step_009 (phase_097)
- Parallels [step_005 (phase_086)]]
- See also: [[step_056 (phase_068)
- Leads to
- Compare with [Quest - Succession Crisis 2]]
- Connects to [[ITEM00286_Venomous_Axe_of_Wounding
- Compare with [Dynamic_NPC_Personality_Matrix (D&D_References)]]
- See also: [[Memory Restoration Devices
- Connects to [step_019 (phase_098)]]
- Affected by [[Rapier Xphb
- Influences [Scene Scene Shadow Market Under Rain V1 Shadow Market Under Rain.svg]]
- Influences [[Wind Rider Orders (Organizations)
- Requires [Crystal Resonance (Lore)]]
- Influences [[fishing-tackle (items)
- Connects to [Chaplain Father Blessing Hopekeeper (D&D_References)]]
- Parallels [[Location City Barkeep Mira Algaebrew V1 Barkeep Mira Algaebrew.svg
- Parallels [Assets Locations Location City the Living Weapon the Living Weapon.svg]]
- Influences [[ITEM01006_Distilled_Oil_of_Healing
- Related: [Location City Current Innovator Current Innovator.svg]]
- Related: [[Template-Quest
- Influences [6-credits (volos-guide-to-monsters)]]
- Originates from [[Quest - Moral Choices
- See also: [step_069 (phase_013)]]
- See also: [[ITEM00565_Enchanted_Chain_Mail_of_Fortitude
- Related: [Ring of Telekinesis Xdmg]]
- See also: [[Assets Locations Location City Madame Whisper Madame Whisper.svg
- Compare with [skulker-xphb (feats)]]
- Leads to [[Location City the Singing Shadows the Singing Shadows.svg
- Parallels [cleaving-through-creatures (variant-rules)]]
- Parallels [[MON00024_Aberrations_Creature_25
- Related: [Royal_Academy_of_Arcane_Arts (Places)]]
- Influences [[Assets Locations Location City Temple of Justice Temple of Justice.svg
- Compare with [Assets Handouts Handout Handout Smuggler Ledger Page V1 Smuggler Ledger Page.png]]
- Requires [[Memoriam Keeper Marcus Remembrance 2
- Parallels [Political Intrigue of Meridian 2]]
- Originates from [[FAC00050_Cults_51
- Connects to [Platinum Pp]]
- Originates from [[step_042 (phase_005)
- Affected by [Border Territories]]
- Connects to [[step_089 (phase_064)
- Leads to [Random Buildings Religious Building]]
- Connects to [[Runaway_Golem_Quest
- Connects to [Quest - The Blackmail Papers]]
- Affected by [[SHOP00039_General_Shop_40
- Connects to [ENC00216_Combat_Encounter_217]]
- Leads to
- Originates from [[Foreign Shadow Syndicates
- See also: [step_075 (phase_091)]]
- Originates from [[step_042 (phase_085)
- Influences [Quest - Rescue the Originals_1 (01_Adventures)]]
- See also: [[NPC01265_Fiora_Hawthorne_the_Mystic
- Originates from [weasel-xmm (beast)]]
- See also: [[Assets Locations Location City New Tethys V1 New Tethys.svg
- Parallels [QUEST00152_Side_Quest_153]]
- Related: [[Deck of Many Things 13 Cards Xdmg
- Connects to [step_014 (phase_020)]]
- Originates from [[MON00119_Undead_Creature_120
- Originates from [Assets Vehicles Vehicle Ship Storm Borne Battleship V2 Storm Borne Battleship.svg]]
- Connects to [[EVENT00038_Political_Event_39
- Compare with [step_080 (phase_005)]]
- See also: [[The Ethical Committee 2
- Related: [step_047 (phase_072)]]
- Influences [[Molten Magma Roper Pota
- Parallels [Shadow's End]]
- Influences [[step_097 (phase_022)
- Affected by [EVENT00027_Magical_Event_28]]
- Influences [[Aethermoor - Session 05 The Queens Madness
- See also: [Session 07 (06_Sessions)]]
- Leads to [[NPC01715_Kaelen_Stormwind_the_Redeemed
- Connects to [greatsword-xphb (items)]]

## Visual References
![[02_Worldbuilding/locations/location_scream_saturation_rules_night.png
![02_Worldbuilding/locations/location_scream_saturation_rules_rain.png]]
![[02_Worldbuilding/locations/location_scream_saturation_rules_establishing.png]]
