# Encounter Management System

## Random Encounters by Region
```dataview
TABLE difficulty, environment, encounter_type
FROM ""
WHERE type = "encounter"
SORT difficulty ASC
```

## Encounter Templates

### Combat Encounter Template
```
---
type: encounter
name: Encounter Name
difficulty: medium
environment: forest
encounter_type: combat
cr: 3
created: {{date}}
tags: [encounter, combat]
---

# Encounter Name

## Setup
*Scene description and context*

## Creatures
- **Creature Name** (CR X) - Quantity: X
  - HP: X
  - AC: X
  - Special abilities

## Terrain
*Map description and special features*

## Tactics
*How creatures fight*

## Treasure
*Loot and rewards*

## Scaling
- **Easy:** Reduce creature count
- **Hard:** Add creatures or hazards
```
