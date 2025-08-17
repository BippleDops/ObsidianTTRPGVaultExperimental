---
id: IDX0002
status: active
type: index
domain: resource
canonical: true
---

# NPC Index

## 👑 Major NPCs by Campaign

### Aquabyssos
```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  race AS "Race",
  class AS "Class",
  faction AS "Faction",
  location AS "Location"
FROM "03_People"
WHERE type = "npc" AND campaign = "Aquabyssos"
SORT file.name ASC
```

### Aethermoor
```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  race AS "Race", 
  class AS "Class",
  faction AS "Faction",
  location AS "Location"
FROM "03_People"
WHERE type = "npc" AND campaign = "Aethermoor"
SORT file.name ASC
```

## 🏛️ NPCs by Faction

```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  race AS "Race",
  class AS "Class",
  role AS "Role",
  campaign AS "Campaign"
FROM "03_People"
WHERE type = "npc" AND faction != null
GROUP BY faction
SORT faction ASC
```

## 📍 NPCs by Location

```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  race AS "Race",
  class AS "Class",
  faction AS "Faction"
FROM "03_People"
WHERE type = "npc" AND location != null
GROUP BY location
SORT location ASC
```

## 🎭 NPCs by Role

### Leaders & Nobility
```dataview
LIST file.link
FROM "03_People"
WHERE type = "npc" AND (contains(tags, "leader") OR contains(tags, "noble") OR contains(tags, "ruler"))
```

### Merchants & Traders
```dataview
LIST file.link
FROM "03_People"
WHERE type = "npc" AND (contains(tags, "merchant") OR contains(tags, "trader") OR contains(tags, "shopkeeper"))
```

### Quest Givers
```dataview
LIST file.link
FROM "03_People"
WHERE type = "npc" AND contains(tags, "quest-giver")
```

### Antagonists
```dataview
LIST file.link
FROM "03_People"
WHERE type = "npc" AND (contains(tags, "antagonist") OR contains(tags, "villain") OR contains(tags, "enemy"))
```

## 🎲 Combat NPCs

```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  cr AS "CR",
  hp AS "HP",
  ac AS "AC",
  attacks AS "Attacks"
FROM "03_People"
WHERE type = "npc" AND cr != null
SORT cr DESC
```

## 👥 Relationship Web

```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  allies AS "Allies",
  enemies AS "Enemies",
  relationships AS "Other"
FROM "03_People"
WHERE type = "npc" AND (allies != null OR enemies != null OR relationships != null)
```

## 🆕 Recently Created NPCs

```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  race AS "Race",
  class AS "Class",
  campaign AS "Campaign",
  file.ctime AS "Created"
FROM "03_People"
WHERE type = "npc"
SORT file.ctime DESC
LIMIT 20
```

## 📝 NPCs Needing Development

```dataview
TABLE WITHOUT ID
  file.link AS "NPC",
  status AS "Status",
  file.size AS "Size"
FROM "03_People"
WHERE type = "npc" AND (status = "draft" OR status = "seed" OR file.size < 500)
SORT file.size ASC
```

---
*Last updated: `= dateformat(date(now), "yyyy-MM-dd HH:mm")`*