# Quest Master Tracker

## Active Quests
```dataview
TABLE status, campaign, quest_giver, reward
FROM ""
WHERE type = "quest" AND status = "active"
SORT priority DESC
```

## Completed Quests
```dataview
TABLE campaign, completion_date, reward
FROM ""
WHERE type = "quest" AND status = "completed"
SORT completion_date DESC
```

## Quest Templates

### Main Quest Template
```
---
type: quest
name: Quest Name
campaign: Campaign Name
status: active
priority: high
quest_giver: [[NPC Name]]
reward: Description
created: {{date}}
tags: [quest, main]
---

# Quest Name

## Objective
*What needs to be accomplished*

## Background
*Why this quest exists*

## Steps
1. Step 1
2. Step 2
3. Step 3

## NPCs Involved
- [[Quest Giver - Role
- [Other NPC]] - Role

## Locations
- [[Location - Why relevant

## Rewards
- XP: Amount
- Gold: Amount
- Items: [Item Name]]

## Notes
*Additional quest notes*
```
