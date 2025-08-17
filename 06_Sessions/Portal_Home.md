---
tags: [player-portal, public, shared]
cssclass: player-view
---

# 🎭 [[Player Portal

## Welcome, Heroes!

### 📅 [Next Session]]
- **Date**: Saturday, 7 PM
- **Location**: [[The Haunted Manor
- **[Expected Duration]]**: 4 hours
- **What to Bring**: Level 4 characters

### 📜 [[Your Adventures [So Far]]

#### [[Recent Sessions
```dataview
TABLE summary as "Summary", date as "Date"
FROM "Players/Session_Recaps"
SORT date DESC
LIMIT 5
WHERE file.name != ""
```

### 🗂️ [Shared Knowledge]]

#### [[Discovered Lore
- [[Players/Lore/The_Ancient_Prophecy|[The Ancient]] Prophecy]]
- [[Players/Lore/Faction_Information|[Known Factions]]
- [[Players/Lore/World_Map|[Explored Regions]]

#### Known NPCs
```dataview
TABLE relationship as "Relationship", location as "[[Last Seen"
FROM "Players/Known_NPCs"
WHERE revealed = true
```

### 📝 [Character Journals]]

#### [[Party Members
- [Players/Journals/Warrior_Journal|Thorin's Journal]]
- [[Players/Journals/Wizard_Journal|Elara's Notes
- [Players/Journals/Rogue_Journal|Shadow's Observations]]
- [[Players/Journals/Cleric_Journal|[Father Marcus's Prayers]]

### 🎯 [[Active Quests

#### [Main Quest]]
**Save the Kingdom**
- [ ] Find the lost artifact
- [ ] Unite the three factions
- [ ] Defeat the [[Dark Lord

#### [Side Quests]]
- **[[Missing Merchant**: Last seen near the forest
- **[Strange Noises]]**: Investigate the old mill
- **[[Love Letter**: Deliver to the noble's daughter

### 📊 [Party Resources]]

#### Inventory
- **Gold**: 1,234 gp
- **Potions**: 4x Healing, 1x [[Greater Healing
- **[Special Items]]**: Map to treasure, Royal seal

#### Reputation
- **Waterdeep**: Honored (+2 to social rolls)
- **[[Thieves Guild**: Neutral (0)
- **Temple of Light**: Trusted (+1)

### 🗺️ Maps & Handouts

#### [Available Maps]]
- [[Players/Maps/Region_Map|[Regional Map]]
- [[Players/Maps/City_Map|[City Districts]]
- [[Players/Maps/Dungeon_Map|[Explored Dungeons]]

#### Handouts
- [[Players/Handouts/Mysterious_Letter|[The Mysterious Letter]]
- [[Players/Handouts/Ancient_Riddle|[The Ancient Riddle]]
- [[Players/Handouts/Wanted_Poster|[Wanted Poster]]

### 💬 [[Party Communication

#### [Message Board]]
> Leave notes for your party members here

#### [[Planning Space
- [[Players/Planning/Next_Session_Goals|[Next Session]] Goals]]
- [[Players/Planning/Shopping_List|[Shopping List]]
- [[Players/Planning/Questions_for_DM|Questions for DM

### 📚 [Rules Reference]]

#### [[Quick Links
- [[Players/Rules/Combat_Basics|[Combat Basics]]]]
- [[Players/Rules/Spell_Casting|[Spellcasting Rules]]
- [[Players/Rules/Conditions|[Status Conditions]]
- [[Players/Rules/Resting|Rest & Recovery

---
*Portal updates after each session*
*Some information hidden until discovered*

## [Session Summary]]
*Brief overview of this session*

## [[Key Events
- Event 1
- Event 2

## NPCs Encountered
- [[NPC [Name]]]] - Brief description

## [[Locations Visited
- [[[Location Name]]]] - What happened here

## [[Quest Progress
- [[[Quest Name]]]] - What was accomplished

## Notes for [[Next Session]]
- Important things to remember
- Plot threads to follow up

---
