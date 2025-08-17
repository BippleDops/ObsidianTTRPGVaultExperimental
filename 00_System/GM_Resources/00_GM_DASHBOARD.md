---
id: SYS0005
status: active
domain: resource
type: asset
canonical: true
cssclass: dashboard
---

# 🎲 GM Dashboard

## ⚡ Quick Actions

- [[00_System/Quick_Capture_Inbox/README|📥 Quick Capture]]
- [[_INDEXES/INDEX_Master|📊 Master Index]]
- [[06_Sessions/Session_Template|📝 New Session]]
- [[01_Adventures/Encounter_Builder|⚔️ Build Encounter]]

## 🎮 Active Campaign: Aquabyssos

### 📅 Next Session
```dataview
TABLE WITHOUT ID
  file.link AS "Session",
  date_planned AS "Date",
  session_number AS "Number",
  status AS "Status"
FROM "06_Sessions"
WHERE campaign = "Aquabyssos" AND status = "planned"
SORT date_planned ASC
LIMIT 1
```

### 📜 Last Session
```dataview
TABLE WITHOUT ID
  file.link AS "Session",
  date_played AS "Date",
  session_number AS "Number"
FROM "06_Sessions"
WHERE campaign = "Aquabyssos" AND status = "completed"
SORT date_played DESC
LIMIT 1
```

### ⚔️ Active Quests
```dataview
TABLE WITHOUT ID
  file.link AS "Quest",
  quest_giver AS "Giver",
  priority AS "Priority"
FROM ""
WHERE type = "quest" AND campaign = "Aquabyssos" AND status = "active"
SORT priority DESC
```

### 🎯 Session Prep Checklist
- [ ] Review last session notes
- [ ] Check active quests
- [ ] Prepare NPCs for session
- [ ] Ready encounter maps
- [ ] Update initiative tracker
- [ ] Prepare loot/rewards
- [ ] Review player notes

## 🌍 World State

### 📍 Party Location
```dataview
TABLE WITHOUT ID
  file.link AS "Location",
  biome AS "Type",
  parent_location AS "Region"
FROM "02_Worldbuilding"
WHERE contains(tags, "party-location")
LIMIT 1
```

### 👥 Recent NPCs
```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  location AS "Location",
  faction AS "Faction"
FROM "03_People"
WHERE type = "npc" AND contains(tags, "recently-met")
SORT file.mtime DESC
LIMIT 5
```

### 🏛️ Active Factions
```dataview
TABLE WITHOUT ID
  file.link AS "Faction",
  reputation AS "Party Rep",
  status AS "Status"
FROM "02_Worldbuilding"
WHERE type = "faction" AND status = "active"
```

## 🎲 Quick References

### 🎯 DC Guidelines
- **Very Easy**: DC 5
- **Easy**: DC 10
- **Medium**: DC 15
- **Hard**: DC 20
- **Very Hard**: DC 25
- **Nearly Impossible**: DC 30

### ⚔️ Encounter Difficulty
| Level | Easy | Medium | Hard | Deadly |
|-------|------|---------|-------|---------|
| 1     | 25   | 50      | 75    | 100     |
| 2     | 50   | 100     | 150   | 200     |
| 3     | 75   | 150     | 225   | 400     |
| 4     | 125  | 250     | 375   | 500     |
| 5     | 250  | 500     | 750   | 1100    |

### 🎁 Treasure by CR
| CR    | Individual | Hoard    |
|-------|------------|----------|
| 0-4   | 2d6 gp     | 6d6×10 gp |
| 5-10  | 2d6×10 gp  | 2d6×100 gp |
| 11-16 | 2d6×100 gp | 2d6×1000 gp |
| 17+   | 2d6×1000 gp| 2d6×10000 gp |

## 📊 Vault Health

```dataview
TABLE WITHOUT ID
  "Markdown Files" AS "Type",
  length(rows) AS "Count"
FROM ""
WHERE file.extension = "md"
GROUP BY true
```

```dataview
TABLE WITHOUT ID
  status AS "Status",
  length(rows) AS "Count"
FROM ""
WHERE status != null
GROUP BY status
```

## 🔧 GM Tools

### Scripts
- [[_SCRIPTS/vault_hygiene_audit.py|🧹 Hygiene Audit]]
- [[_SCRIPTS/session_prep.py|📅 Session Prep]]
- [[_SCRIPTS/npc_generator.py|👤 Generate NPC]]
- [[_SCRIPTS/encounter_builder.py|⚔️ Build Encounter]]

### Templates
- [[00_System/Templates/npc_template|NPC Template]]
- [[00_System/Templates/location_template|Location Template]]
- [[00_System/Templates/quest_template|Quest Template]]
- [[00_System/Templates/session_template|Session Template]]

## 📝 Quick Notes
```
Quick notes area - edit this section freely for temporary notes during session
---





---
```

## 🔄 Recent Changes

```dataview
TABLE WITHOUT ID
  file.link AS "File",
  type AS "Type",
  file.mtime AS "Modified"
FROM ""
WHERE file.mtime > date(today) - dur(3 days)
SORT file.mtime DESC
LIMIT 10
```

---
*Dashboard refreshes automatically with Dataview*
*Last manual update: `= dateformat(date(now), "yyyy-MM-dd HH:mm")`*