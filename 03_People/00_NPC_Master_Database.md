# NPC Master Database

*Last Updated: 2025-08-16 10:01:40*

## Quick Stats
- **Total NPCs:** 2064
- **Campaigns:** 0
- **Locations:** 1
- **Factions:** 0

## All NPCs (Dataview)
```dataview
TABLE
  race as "Race",
  class as "Class",
  location as "Location",
  campaign as "Campaign",
  faction as "Faction"
FROM "03_People"
WHERE type = "npc"
SORT file.name ASC
```

## NPCs by Campaign

## NPCs by Location

### Unknown
- [[Character Relationship Web - Core NPCs|Character Relationship Web - Core s]]
- [[Create New NPC|Create New]]
- [[NPC Cross-World Connections|Cross-World Connections]]
- [[NPC Cross-World Connections|Cross-World Connections]]
- [[NPC Development Timeline|Development Timeline]]
- [[NPC Development Timeline|Development Timeline]]
- [[Generate Campaign NPCs|Generate Campaign s]]
- [[Important NPCs|Important s]]
- [[NPC Name 1|Name 1]]
- [[NPC Name 1|Name 1]]
- [[Random NPC|Random]]
- [[NPC Reaction Matrix|Reaction Matrix]]
- [[NPC Reaction Matrix|Reaction Matrix]]
- [[NPC_Reactions|Reactions]]
- [[NPC_Reactions|Reactions]]
- [[NPC Relationship System|Relationship System]]
- [[NPC Relationship System|Relationship System]]
- [[Shadow Conspiracy NPCs|Shadow Conspiracy s]]
- [[NPCs_List|s List]]
- [[NPCs_List|s List]]

## NPCs by Faction

## Quick Actions
- [[NPC_Template|Create New NPC]]
- [[NPC_Relationship_Map|View Relationships]]
- [[NPC_Quick_Reference|Quick Reference]]

## Search Functions
```dataview
TABLE file.link as "NPC"
FROM "03_People"
WHERE type = "npc" AND contains(file.name, "")
```


## Relationships
- Hunting [[Crown Dome Conspiracy]]
- Indebted to [[Information Broker Whisper Goldtongu 2]]
- Ally of [[Void Lords]]
- Member of the Shadow Parliament (secret)

## Motivations
### Primary Motivation
Aims to bridge the divide between Aquabyssos and Aethermoor

### Secondary Goals
- Gain influence in their district
- Master a forgotten combat technique

## Plot Hooks
1. **The Missing Shipment**: 00_NPC_Master_Database approaches the party about a critical supply convoy that never arrived from the Bathyal Zone
5. **Double Agent**: Evidence suggests 00_NPC_Master_Database is working for two opposing factions
3. **Secret Meeting**: 00_NPC_Master_Database needs escorts to a clandestine meeting in the Abyssal Trenches