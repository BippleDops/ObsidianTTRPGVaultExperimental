---
tags: [tool, generator, npc]
created: "2025-08-15T14:13:16.703710"
---

# 🎭 Quick NPC Generator

## Instant NPC
```dataview
TABLE
  choice(["Human", "Elf", "Dwarf", "Halfling", "Dragonborn"]) as Race,
  choice(["Fighter", "Wizard", "Rogue", "Cleric", "Ranger"]) as Class,
  choice(["Friendly", "Neutral", "Hostile", "Suspicious"]) as Attitude,
  choice(["Gruff", "Cheerful", "Mysterious", "Nervous"]) as Personality
LIMIT 1
```

## Name Generator
- **Male**: Gareth, Marcus, Aldric, Finn, Thorin
- **Female**: Elara, Lyra, Mira, Kessa, Brynn
- **Surnames**: Ironforge, Moonwhisper, Stormwind, Goldleaf

## Quick Traits
Roll `dice: `dice: 1d20`` for each:

### Appearance
1-5: Scar
6-10: Unusual hair
11-15: Missing limb
16-20: Distinctive clothing

### Motivation
1-5: Gold
6-10: Power
11-15: Knowledge
16-20: Revenge

## Stat Block Template
```
**Name** - Race Class
AC: 10+mod | HP: Level×HD | Speed: 30ft
STR: 10 | DEX: 10 | CON: 10 | INT: 10 | WIS: 10 | CHA: 10
```

---
*Quick NPC generation for instant gameplay*