---
enhanced: true
tags: [enhanced, 01_adventures]
created: "2025-08-15T12:25:47.075913"
modified: "2025-08-15T12:25:47.075917"
aliases: [Campaign Center]
---

## Table of Contents
- [[#Contents|Contents
- [#Overview|Overview]]
- [[#Description|Description
- [#Notes|Notes]]
- [[#Timeline|Timeline
- [#NPCs Involved|NPCs Involved]]
- [[#Complications|Complications
- [#Alternative Solutions|Alternative Solutions]]
- [[#Visual References|Visual References]]

---
tags: [misc]
type: misc
aliases: ["Campaign Center"]
---

# Campaign Center

## Contents
- [Overview](#overview)
- [Description](#description)
- [Notes](#notes)
- [Timeline](#timeline)
- [NPCs Involved](#npcs-involved)
- [Complications](#complications)
- [Alternative Solutions](#alternative-solutions)

## Overview

**Difficulty**: Moderate (Levels 3-5)

Comprehensive overview of this content.

---

title: Campaign_Center
type: quest
tags:
- quest

created: '2025-01-15'
modified: '2025-01-15'
status: active
aliases: ["Campaign Center"]
priority: normal
category: 01 Adventures
subcategory: Campaign Center.Md
related: []
cssclass: standard
publish: false

---

 # Campaign_Center ---

## Description

**Tension**: The urgency of this quest creates palpable tension in the air.

Detailed description pending.
title: Campaign Center
type: index
tags:
- management
- index
- active
- campaign

created:
*The air carries the scent of [appropriate smell].* 2025-08-14
modified: '2025-08-14'
updated: 2025-08-14
cssclass: campaign-center

--- ## 🎲 Active Campaigns```dataview

TABLE WITHOUT ID file.link as Campaign, status as Status, sessions as "Total Sessions", players as Players

FROM "01_Adventures"

WHERE type = "campaign" OR contains(file.name, "Campaign")

SORT status ASC```### Upcoming Sessions file.link as Session, campaign as Campaign, date as "Scheduled", status as Status

WHERE type = "session" AND status != "completed"

SORT date ASC ### Recent Sessions date as Date, recap as "Quick Recap"

WHERE type = "session" AND status = "completed"

SORT date DESC

LIMIT 5 ## 📊 Campaign Progress sessions-completed as "Completed", sessions-total as "Total", completion as "Progress %"

WHERE type = "campaign" ### By Faction faction as Faction, length(rows) as "NPC Count"

FROM "02_Worldbuilding/People"

WHERE type = "npc" AND faction != GROUP BY faction

SORT length(rows) DESC ### Important NPCs file.link as NPC, role as Role,

WHERE importance = "major" OR contains(tags, "important")

LIMIT 10 ## 📍 Campaign Locations file.link as Location, campaign as "Used In", visits as Visits,

FROM "02_Worldbuilding/Places"

WHERE campaign != SORT visits DESC ---

*Campaign management powered by Dataview* ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Background

*[Adventure setup and context]* ### What Happened Before

- *[Recent events leading to this adventure]* ### Current Situation - *[What's happening now]* ### The Stakes

- *[What happens if PCs don't act]* ## Adventure Hooks

*[Ways to get PCs involved]* ### Direct Approach

- *[Straightforward hook]* ### Indirect Approach

- *[Subtle introduction]* ### Emergency Hook

- *[Urgent situation]* ## Key NPCs

*[Important characters in this adventure]* ### Allies

- *[Helpful NPCs]* ### Antagonists

- *[Opposition NPCs]* ### Neutral Parties

- *[Information sources]* ## Locations

*[Important places in this adventure]* ### Starting Location

- *[Where adventure begins]* ### Key Sites

- *[Major locations to visit]* ### Optional Areas

- *[Side locations]* ## Rewards

**Experience Points**: 500 XP per character

*[What PCs gain from completing this adventure]* ### Experience Points

- *[XP awards]* ### Treasure

- *[Gold and magic items]* ### Story Rewards

- *[Reputation, allies, information]* ## Scaling

*[How to adjust for different party levels]* ### Lower Level Parties

- *[Adjustments for weaker groups]* ### Higher Level Parties

- *[Adjustments for stronger groups]* ### Large/Small Parties

- *[Adjustments for party size]* ## Player Tips

> 🎮 **Strategy**: How to approach this content

> Work together and communicate

## Notes

*Additional notes*

#story/story
#story/background
#world/location
#world/world
#world/place
#character/npc
#character/character
#gameplay/session
#gameplay/adventure
#gameplay/quest
#resource/item
#resource/treasure
#meta/index

## Timeline
- Key events
- Deadlines

## NPCs Involved
- Quest giver
- Antagonists

## Complications
- Potential problems
- Twists

## Alternative Solutions
- Non-combat options
- Creative approaches

## Visual References
![[04_Resources/Assets/Misc/_cross_campaign_organizations.png
![04_Resources/Assets/Misc/parliament_of_shadows_campaign.png]]
![[04_Resources/Assets/Maps/World/Continents/world_cross_campaign_locations_player.png]]
