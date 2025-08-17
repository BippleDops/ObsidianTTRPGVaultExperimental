---

title: Item Catalog Complete
type: Lore
tags:
- lore
- index
- status/complete
- report
- universal
- world/both
- active
- complete
- content/item

created: null
modified: '2025-08-14'
status: complete
obsidian UIMode: preview
updated: '2025-08-13T12:34:03.170416+00:00'
world: Universal

--- # Item Catalog Complete ## Items Overview```dataview

## Description

Detailed description pending.

TABLE WITHOUT ID link(file.name) AS "Item", item_type AS "Type", rarity AS "Rarity", cost_gp AS "Price (gp)", weight AS "Weight", Connected_Quests AS "Plot Links", My Container AS "Found/Owner"

FROM "02_Worldbuilding/Items"

WHERE status = "complete"

SORT rarity ASC, file.name ASC```## Merchant Inventories by Location```dataview

TABLE WITHOUT ID link(file.name) AS "Location", merchant_inventory AS "Inventory"

FROM "02_Worldbuilding/Places"

WHERE status = "complete" AND merchant_inventory

SORT file.name ASC```## Crafting Requirements```dataview

TABLE WITHOUT ID link(file.name) AS "Item", crafting AS "Requirements"

FROM "02_Worldbuilding/Items"

WHERE status = "complete" AND crafting

SORT file.name ASC```## Connections - See also: [[Campaign Guide

- Related: [Recent Events]]
- Connected to: [[Main Quest Line]] ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes

## Notes

*Additional notes*
