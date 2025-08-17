---
enhanced: true
tags: [misc]
type: misc
aliases: ["Relationship Web"]
---

# Relationship Web

> *An opportunity for greatness awaits...* This remarkable element adds depth and intrigue to any campaign.

---

title: Relationship_Web
type: note
tags:
- quest
- note

created: '2025-01-15'
modified: '2025-01-15'
status: active
aliases: ["Relationship Web"]
priority: normal
category: 00 Indexes
subcategory: Relationship Web.Md
related: []
cssclass: standard
publish: false

---

 # Relationship_Web ---

## Description

**Details**: Rich sensory elements bring this to life. {#description}

Detailed description pending.
title: Relationship Web
type: index
tags:
- relationships
- npcs
- index
- active

created: 2025-
*The [texture] surface feels [description] to the touch.*08-14
modified: '2025-08-14'
updated: 2025-08-14
cssclass: relationship-web

--- ### Faction Affiliations```dataview

TABLE WITHOUT ID faction as Faction, length(rows) as Members, leader as Leader

FROM "02_Worldbuilding/People"

WHERE faction != GROUP BY faction

SORT length(rows) DESC```### Romantic Relationships file.link as Character, romance as "Romantic Interest", relationship-status as Status

WHERE romance != ### Rivalries rival as Rival, conflict as "Nature of Conflict"

WHERE rival != ### Alliances allies as Allies, alliance-type as "Type"

WHERE allies != ### Leaders file.link as Leader, faction as Organization, location as Base, followers as Followers

WHERE role = "leader" OR contains(tags, "leader") ### Advisors file.link as Advisor, advises as "Advises", expertise as Expertise

WHERE role = "advisor" OR contains(tags, "advisor") ## 🔗 Connection Statistics "Total NPCs" as Metric, length(file.link) as Count

WHERE type = "npc" UNION ALL "Has Relationships" as Metric,

WHERE relationships != OR allies != OR enemies != "In Factions" as Metric, ## 🎯 Quest Givers file.link as "Quest Giver", quests-given as Quests, location as Location, faction as Faction

WHERE quests-given != OR contains(tags, "quest-giver") ---

*Relationship tracking powered by Dataview* ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Alternate Descriptions

- **First Impression**: Initial appearance
- **Closer Look**: Detailed examination
- **Hidden Details**: Secret aspects ## Random Table

| d6 | Result |
|----|--------|
| 1 | Option A |
| 2 | Option B |
| 3 | Option C |
| 4 | Option D |
| 5 | Option E |
| 6 | Option F | ## References - [[Update Indexes|Update Indexes

- [Update Indexes (D&D_References)|Update Indexes (D&D References)]]
- [[Update Indexes 3 (D&D_References)|Update Indexes 3 (D&D References) ## Overview *To be added* ## Goals *To be added* ## Structure *To be added* ## Members *To be added* ## Resources *To be added* ## Relationships *To be added*

## Notes {#notes}

*Additional notes*

#story/story
#world/location
#world/world
#character/npc
#character/character
#gameplay/quest
#meta/index
#meta/reference
## Secrets & Mysteries
- **Hidden Truth**: Not everything is as it appears
- **Unanswered Questions**: What remains unknown
- **Future Revelations**: Discoveries yet to be made

**Key Question**: What role will this play in the greater story?

*What happens next is up to you.*

## Visual References
![04_Resources/Assets/Portraits/NPCs/portrait_character_relationship_web_core_npcs.png]]
![[04_Resources/Assets/Portraits/NPCs/portrait_character_faction_relationship_matrix.png
![04_Resources/Assets/Portraits/NPCs/portrait_npc_relationship_system.png]]
