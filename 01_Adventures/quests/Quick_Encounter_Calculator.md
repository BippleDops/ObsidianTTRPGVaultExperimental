---
tags: [tool, calculator, encounter]
created: "2025-08-15T14:13:16.703716"
---

# ⚔️ Encounter Calculator

## Quick Balance Check

### Party Level vs Monster CR
| Party Lvl | Easy | Medium | Hard | Deadly |
|-----------|------|--------|------|--------|
| 1-2       | CR 1/4 | CR 1/2 | CR 1 | CR 2 |
| 3-4       | CR 1/2 | CR 1 | CR 2 | CR 3 |
| 5-6       | CR 1 | CR 2 | CR 4 | CR 6 |
| 7-8       | CR 2 | CR 4 | CR 6 | CR 8 |

## XP Budget (4 players)
```dataview
TABLE
  level as "Level",
  (25 * level) as "Easy",
  (50 * level) as "Medium",
  (75 * level) as "Hard",
  (100 * level) as "Deadly"
FROM "nowhere"
WHERE level <= 20
```

## Multipliers for Multiple Enemies
- 1 enemy: ×1
- 2 enemies: ×1.5
- 3-6 enemies: ×2
- 7-10 enemies: ×2.5
- 11-14 enemies: ×3
- 15+ enemies: ×4

---
*Quick encounter balancing tool*