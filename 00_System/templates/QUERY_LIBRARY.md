---
tags: [dataview, queries, reference]
created: "2025-08-15T14:13:16.715258"
---

# 📊 Dataview Query Library

## Character Queries

### All NPCs by Location
```dataview
TABLE faction as "Faction", status as "Status"
FROM "03_People"
GROUP BY location
WHERE file.name != ""
```

### Active Player Characters
```dataview
TABLE level as "Level", class as "Class", player as "Player"
FROM #pc
WHERE status = "active"
```

## Quest Queries

### Active Quests by Level
```dataview
TABLE questgiver as "Giver", reward as "Reward"
FROM #quest
WHERE status = "active"
SORT level ASC
```

### Completed Quests Timeline
```dataview
TABLE completed as "Date", outcome as "Result"
FROM #quest
WHERE status = "complete"
SORT completed DESC
```

## World Queries

### Locations by Region
```dataview
TABLE type as "Type", population as "Pop"
FROM "02_Worldbuilding/Locations"
GROUP BY region
WHERE file.name != ""
```

### Recent World Events
```dataview
TABLE file.link as "File"
FROM #event
SORT file.mtime DESC
LIMIT 10
WHERE file.name != ""
```

## Session Queries

### Session History
```dataview
TABLE date as "Date", players_present as "Players", xp_awarded as "XP"
FROM #session
SORT session_number DESC
WHERE file.name != ""
```

### Treasure Log
```dataview
TABLE session as "Session", gold as "Gold", items as "Items"
FROM #session
WHERE treasure
```

## Utility Queries

### Recently Modified
```dataview
TABLE file.mtime as "Modified"
FROM ""
SORT file.mtime DESC
LIMIT 20
WHERE file.name != ""
```

### Orphaned Notes
```dataview
TABLE file.link as "File"
FROM ""
WHERE length(file.inlinks) = 0
LIMIT 20
```

### Largest Files
```dataview
TABLE file.size as "Size"
FROM ""
SORT file.size DESC
LIMIT 10
WHERE file.name != ""
```

---
*Complete dataview query library*