---
id: IDX0001
status: active
type: index
domain: resource
canonical: true
---

# Master Index

## 📊 Vault Statistics

```dataview
TABLE WITHOUT ID
  length(rows) AS "Count"
FROM ""
WHERE file.name != this.file.name
GROUP BY type
SORT length(rows) DESC
```

## 🎮 Active Campaigns

```dataview
TABLE WITHOUT ID
  file.link AS "Campaign",
  status AS "Status",
  session_count AS "Sessions",
  player_count AS "Players"
FROM "01_Adventures"
WHERE type = "campaign" AND status = "active"
SORT file.name ASC
```

## 📅 Recent Sessions

```dataview
TABLE WITHOUT ID
  file.link AS "Session",
  campaign AS "Campaign",
  date_played AS "Date",
  session_number AS "#"
FROM "06_Sessions"
WHERE type = "session_notes"
SORT date_played DESC
LIMIT 10
```

## ⚔️ Active Quests

```dataview
TABLE WITHOUT ID
  file.link AS "Quest",
  quest_giver AS "Given By",
  campaign AS "Campaign",
  priority AS "Priority"
FROM ""
WHERE type = "quest" AND status = "active"
SORT priority DESC, file.name ASC
```

## 🌟 Featured NPCs

```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  race AS "Race",
  class AS "Class",
  faction AS "Faction",
  location AS "Location"
FROM "03_People"
WHERE type = "npc" AND (contains(tags, "major") OR contains(tags, "recurring"))
SORT file.name ASC
LIMIT 20
```

## 📍 Key Locations

```dataview
TABLE WITHOUT ID
  file.link AS "Location",
  biome AS "Type",
  parent_location AS "Region",
  campaign AS "Campaign"
FROM "02_Worldbuilding"
WHERE type = "location" AND (contains(tags, "major") OR contains(tags, "hub"))
SORT file.name ASC
```

## 🎲 Recent Encounters

```dataview
TABLE WITHOUT ID
  file.link AS "Encounter",
  difficulty AS "Difficulty",
  environment AS "Environment",
  last_used AS "Last Used"
FROM "01_Adventures"
WHERE type = "encounter"
SORT last_used DESC
LIMIT 10
```

## 🗺️ Available Maps

```dataview
TABLE WITHOUT ID
  file.link AS "Map",
  map_type AS "Type",
  grid_size AS "Grid",
  file.size AS "Size"
FROM "04_Resources/Maps"
WHERE type = "map" OR contains(file.name, "map")
SORT file.name ASC
LIMIT 20
```

## 📚 Rules Reference

```dataview
TABLE WITHOUT ID
  file.link AS "Rule",
  category AS "Category",
  source AS "Source"
FROM "05_Rules"
WHERE type = "rule" OR type = "mechanic"
SORT category ASC, file.name ASC
```

## 🔄 Recently Modified

```dataview
TABLE WITHOUT ID
  file.link AS "File",
  type AS "Type",
  file.mtime AS "Modified"
FROM ""
WHERE file.mtime > date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 20
```

## 🚨 Needs Attention

```dataview
TABLE WITHOUT ID
  file.link AS "File",
  type AS "Type",
  status AS "Status"
FROM ""
WHERE status = "draft" OR status = "incomplete" OR contains(tags, "todo") OR contains(tags, "needs-work")
SORT file.mtime DESC
LIMIT 20
```

---
*Last updated: `= dateformat(date(now), "yyyy-MM-dd HH:mm")`*