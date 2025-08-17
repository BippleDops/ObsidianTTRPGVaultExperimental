---
enhanced: true

title: DM_Session_Navigator
type: session
tags:
- combat
- session

created: '2025-01-15'
modified: '2025-01-15'
status: active
aliases: ["DM Session Navigator"]
priority: normal
category: 00 Indexes
subcategory: Dm Session Navigator.Md
related: []
cssclass: standard
publish: false

---

 # DM_Session_Navigator ---

## Description

**Details**: Rich sensory elements bring this to life. {#description}

Detailed description pending.
title: DM Session Navigator
type: dm-tool
tags:
- navigation
- index
- session
- dm-tool
- active
*The [texture] surface feels [description] to the touch.*

created: 2025-08-14
modified: '2025-08-14'
updated: 2025-08-14
cssclass: session-navigator

--- ### Next Session```dataview

TABLE WITHOUT ID file.link as Session, campaign as Campaign, date as Date, prep-status as "Prep Status"

FROM "01_Adventures"

WHERE type = "session" AND date >= date(today)

SORT date ASC

LIMIT 1```### Session History players as Players, xp-awarded as XP

WHERE type = "session" AND status = "completed"

SORT date DESC

LIMIT 5 ### Required NPCs file.link as NPC, faction as Faction, location as Location, stat-block as "Stats Ready?"

FROM "02_Worldbuilding/People"

WHERE session-appearance = this.file.name OR contains(tags, "next-session") ### Required Locations file.link as Location, type as Type, map as "Map Ready?", description as "Description"

FROM "02_Worldbuilding/Places" ### Player Attendance player as Player, length(rows) as "Sessions Attended", last-session as "Last Seen"

WHERE type = "session" AND players

FLATTEN players as player

GROUP BY player ### Session Pacing combat-time as "Combat %", rp-time as "RP %", exploration-time as "Exploration %" ## 📝 Session Notes Template```markdown
# Session [Number]: [Title] Date: [Date] {#session-[number]:-[title]-date:-[date]}

Players: [List]

Level: [X] ## Recap [Previous session summary] ## Events [What happened] ## XP Awarded [Amount and reason] ## Notes for Next Session [Hooks and reminders] ## 🔮 Upcoming Plot Points LIST

FROM ""

WHERE contains(tags, "plot-point") AND status = "pending"

SORT priority DESC ---

*DM session navigation and management toolkit* ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Alternate Descriptions

- **First Impression**: Initial appearance
- **Closer Look**: Detailed examination
- **Hidden Details**: Secret aspects ## DM Tips

> 💡 **Running This Content**: Advice for game masters

> Adjust difficulty based on party composition ## Player Tips

> 🎮 **Strategy**: How to approach this content

> Work together and communicate
#mechanics/combat
#story/plot
#story/story
#world/location
#world/world
#world/place
#character/npc
#gameplay/session
#gameplay/adventure
#meta/index
#meta/navigation
## Session Prep
- **Read Aloud Text**: Prepared descriptions for key moments
- **Key NPCs**: Important characters for this content
- **Props Needed**: Physical or digital aids to enhance play
- **Estimated Time**: How long this typically takes to run

*Adventure awaits those brave enough to seek it.*

## Thematic Elements
This content explores themes of revenge, adding narrative depth to your campaign.

## Visual References
![[04_Resources/Assets/Portraits/NPCs/portrait_session_4.png
![04_Resources/Assets/Portraits/NPCs/Minor/portrait_session_4_people_dramatic.png]]
![[04_Resources/Assets/Portraits/NPCs/Minor/portrait_session_4_people_standard.png]]
