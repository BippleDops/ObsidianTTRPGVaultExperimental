# GM Dashboard

## Quick Links
- [[00_GM_Resources/Quick_References/GM_Screen|GM Screen
- [00_GM_Resources/Session_Prep/Session_Template|Session Template]]
- [[00_GM_Resources/Combat_Tools/Initiative_Tracker|Initiative Tracker
- [00_GM_Resources/Random_Tables/Random_Encounters|Random Encounters]]

## Active Campaigns
- [[01_Adventures/Campaigns/Aquabyssos|Aquabyssos Campaign
- [01_Adventures/Campaigns/Aethermoor|Aethermoor Campaign]]

## Recent Sessions
```dataview
TABLE date, players, summary
FROM "06_Sessions"
SORT date DESC
LIMIT 5
WHERE file.name != ""
```

## Active Quests
```dataview
TABLE status, quest_giver, reward
FROM #quest
WHERE status = "active"
```

## Quick Tools
- `dice: `dice: 1d20`` - Roll dice inline
- [[00_GM_Resources/NPC_Tools/NPC_Generator|Generate NPC
- [00_GM_Resources/Loot_Generators/Treasure_Generator|Generate Treasure]]

## Session Checklist
- [ ] Review previous session notes
- [ ] Prepare encounters
- [ ] Update NPC notes
- [ ] Prepare handouts
- [ ] Check player inventories
- [ ] Review active quests
