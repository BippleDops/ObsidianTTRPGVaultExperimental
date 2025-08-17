---
enhanced: true
tags: [misc]
type: misc
aliases: ["Navigation Hub"]
---

# Navigation Hub

> *An opportunity for greatness awaits...* This remarkable element adds depth and intrigue to any campaign.

## Overview

Comprehensive overview of this content.

--- title: Navigation_Hub
type: note
tags:
- quest
- note created: '2025-01-15'
modified: '2025-01-15'
status: active
aliases: ["Navigation Hub"]
priority: normal
category: 00 Indexes
subcategory: Navigation Hub.Md
related: []
cssclass: standard
publish: false --- # Navigation_Hub --- ## Description

**Details**: Rich sensory elements bring this to life. {#description} Detailed description pending.
title: Navigation Hub
type: index
tags:
- active
- navigation
- index
- dynamic created: 2025-08-1
*Sounds of [relevant sounds] echo in the distance.*4
modified: '2025-08-14'
updated: 2025-08-14
cssclass: navigation-hub --- # 🗺️ Vault Navigation Hub > *This page auto-updates to show current vault contents using Dataview queries* ### Content by Category```dataview TABLE WITHOUT ID file.folder as "📁 Category", length(rows) as "📄 Files" FROM "" WHERE file.name!= this.file.name GROUP BY file.folder SORT length(rows) DESC```### Recent Sessions file.link as Session, campaign as Campaign, date as Date FROM "01_Adventures" WHERE type = "session" OR contains(tags, "session") SORT file.mtime DESC LIMIT 5 ### Active NPCs file.link as NPC, faction as Faction, location as Location FROM "02_Worldbuilding/People" WHERE type = "npc" OR contains(tags, "npc") LIMIT 10 ### Key Locations file.link as Location, world as Realm, type as Type FROM "02_Worldbuilding/Places" WHERE type = "location" OR contains(tags, "location") ## 🔥 Recently Modified file.link as Content, file.folder as Category, file.mtime as "Last Modified" WHERE file.mtime >= date(today) - dur(7 days) LIMIT 15 ## 🏷️ Popular Tags LIST FLATTEN tags as tag GROUP BY tag LIMIT 20 ### By Type -`type:npc`- [[Npc|Npc -`type:location`- [Places|Places]]
-`type:quest`- [[All Quests|All Quests
-`type:session`- [All Sessions|All Sessions]] --- *Navigation hub powered by Dataview - automatically updates with vault changes* ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:* - Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Alternate Descriptions - **First Impression**: Initial appearance
- **Closer Look**: Detailed examination
- **Hidden Details**: Secret aspects ## Random Table | d6 | Result |
|----|--------|
| 1 | Option A |
| 2 | Option B |
| 3 | Option C |
| 4 | Option D |
| 5 | Option E |
| 6 | Option F | ## Player Tips > 🎮 **Strategy**: How to approach this content > Work together and communicate ## Notes {#notes} *Additional notes* #story/story
#world/location
#world/world
#world/place
#character/npc
#gameplay/session
#gameplay/adventure
#gameplay/quest
#meta/index
#meta/hub
#meta/navigation

**Key Question**: What role will this play in the greater story?

*What happens next is up to you.*

## Visual References
![[04_Resources/Assets/Misc/aerial_navigation_guild.png
![04_Resources/Assets/Maps/World/Continents/world_assets_locations_location_city_current_navigation_techniques_current_navigation_techniques_svg_physical.png]]
![[04_Resources/Assets/Maps/World/Continents/world_current_navigation_techniques_physical.png]]
