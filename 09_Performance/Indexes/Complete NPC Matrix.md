---

title: Complete NPC Matrix
type: Lore
tags:
- lore
- index
- status/complete
- report
- universal
- world/both
- content/npc
- active
- complete

created: null
modified: '2025-08-14'
status: complete
obsidian UIMode: preview
updated: '2025-08-13T12:34:03.174301+00:00'
world: Universal

--- # Complete NPC Matrix ## Relationship Scores (-3..+3)```dataview

## Description

Detailed description pending.

TABLE WITHOUT ID link(file.name) AS "NPC", char_race AS "Race", char_gender AS "Gender", My Container AS "Primary Location", Connected_Groups AS "Factions", Connected_Quests AS "Quests", relationships AS "Relationships", Note Status AS "Note"

FROM "02_Worldbuilding/People"

WHERE status = "complete"

SORT file.name ASC```## Faction Affiliations```dataview

TABLE WITHOUT ID link(file.name) AS "NPC", Connected_Groups AS "Factions"

FROM "02_Worldbuilding/People"

WHERE status = "complete" AND Connected_Groups

FLATTEN Connected_Groups AS Faction

SORT Faction ASC, file.name ASC```## Location Assignments```dataview

TABLE WITHOUT ID link(file.name) AS "NPC", My Container AS "Location"

FROM "02_Worldbuilding/People"

WHERE status = "complete" AND My Container

SORT My Container ASC```## Quest Involvement```dataview

TABLE WITHOUT ID link(file.name) AS "NPC", Connected_Quests AS "Quests"

FROM "02_Worldbuilding/People"

WHERE status = "complete" AND Connected_Quests

SORT file.name ASC```## Secret Knowledge```dataview

TABLE WITHOUT ID link(file.name) AS "NPC", secret_knowledge AS "Secrets"

FROM "02_Worldbuilding/People"

WHERE status = "complete" AND secret_knowledge

SORT file.name ASC```## Connections - See also: [[Campaign Guide

- Related: [Regional Politics]]
- Connected to: [[Character Backstories]] ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes

## Notes

*Additional notes*

## Voice & Mannerisms
- Speaking style
- Common phrases

## Daily Routine
- Morning activities
- Evening habits

## Possessions
- Personal items
- Valuable objects

## Combat Tactics
- Preferred strategies
- Special moves

## Secrets
- Hidden knowledge
- Personal mysteries
