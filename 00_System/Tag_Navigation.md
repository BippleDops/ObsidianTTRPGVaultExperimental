---
enhanced: true
tags: [misc]
type: misc
aliases: ["Tag Navigation"]
---

# Tag Navigation

> *An opportunity for greatness awaits...* This remarkable element adds depth and intrigue to any campaign.

---

title: Tag_Navigation
type: note
tags:
- combat
- quest
- shadow-touched
- note

created: '2025-01-15'
modified: '2025-01-15'
status: active
aliases: ["Tag Navigation"]
priority: normal
category: 00 Indexes
subcategory: Tag Navigation.Md
related: []
cssclass: standard
publish: false

---

 # Tag_Navigation ---

## Description

**Details**: Rich sensory elements bring this to life. {#description}

Detailed description pending.
title: Tag Navigation
type: navigation
tags:
- navigation
- index
- active
- tags
- hierarchy

cr
*The [texture] surface feels [description] to the touch.*eated: 2025-08-14
modified: '2025-08-14'
updated: 2025-08-14
cssclass: tag-hierarchy

--- ### Find by Single Tag```dataview

TABLE WITHOUT ID file.link as Content, file.folder as Location

FROM # combat LIMIT 10```### Find by Multiple Tags tags as Tags

FROM #npc AND #aquabyssos ### Tag Combinations status as Status

FROM (#quest OR #adventure) AND #active ## 📈 Tag Statistics tag as Tag, length(rows) as "Usage Count"

FROM ""

FLATTEN tags as tag

WHERE tag != GROUP BY tag

SORT length(rows) DESC

LIMIT 20 ### Campaign Tags LIST

FROM # campaign OR #seven-shards OR #shadow-conspiracy GROUP BY file.folder ### Faction Tags FROM # faction OR #guild OR #organization GROUP BY tags ### Danger Level Tags danger-level as "Danger"

FROM # dangerous OR #deadly OR #safe SORT danger-level DESC ### Recently Tagged file.tags as Tags, file.mtime as Modified

WHERE file.mtime >= date(today) - dur(3 days) AND tags != SORT file.mtime DESC ### Untagged Content WHERE !tags OR tags = ---

*Tag-based navigation powered by Dataview* ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

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
| 6 | Option F | ## Overview *To be added* ## Goals *To be added* ## Structure *To be added* ## Members *To be added* ## Resources *To be added* ## Relationships *To be added*

## Notes {#notes}

*Additional notes*

#mechanics/combat
#story/story
#world/location
#character/npc
#gameplay/adventure
#gameplay/quest
#meta/index
#meta/navigation

**Key Question**: What role will this play in the greater story?

*Every story needs its heroes.*

## Visual References
![[04_Resources/Assets/Misc/aerial_navigation_guild.png
![04_Resources/Assets/Maps/World/Continents/world_assets_locations_location_city_current_navigation_techniques_current_navigation_techniques_svg_physical.png]]
![[04_Resources/Assets/Maps/World/Continents/world_current_navigation_techniques_physical.png]]
