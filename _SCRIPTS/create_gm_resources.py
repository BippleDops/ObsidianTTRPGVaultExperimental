#!/usr/bin/env python3
"""
Create a comprehensive GM Resources folder with all necessary tools and references
"""

import os
from pathlib import Path
from datetime import datetime

def create_gm_resources():
    vault_root = Path.cwd()
    gm_dir = vault_root / "00_GM_Resources"
    gm_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    subdirs = [
        "Quick_References",
        "Random_Tables", 
        "Encounter_Tools",
        "Session_Prep",
        "Campaign_Management",
        "NPC_Tools",
        "World_Building",
        "Rules_References",
        "Combat_Tools",
        "Loot_Generators"
    ]
    
    for subdir in subdirs:
        (gm_dir / subdir).mkdir(exist_ok=True)
    
    # Create comprehensive GM files
    files_to_create = {
        "00_GM_DASHBOARD.md": """# GM Dashboard

## Quick Links
- [[00_GM_Resources/Quick_References/GM_Screen|GM Screen]]
- [[00_GM_Resources/Session_Prep/Session_Template|Session Template]]
- [[00_GM_Resources/Combat_Tools/Initiative_Tracker|Initiative Tracker]]
- [[00_GM_Resources/Random_Tables/Random_Encounters|Random Encounters]]

## Active Campaigns
- [[01_Adventures/Campaigns/Aquabyssos|Aquabyssos Campaign]]
- [[01_Adventures/Campaigns/Aethermoor|Aethermoor Campaign]]

## Recent Sessions
```dataview
TABLE date, players, summary
FROM "06_Sessions"
SORT date DESC
LIMIT 5
```

## Active Quests
```dataview
TABLE status, quest_giver, reward
FROM #quest
WHERE status = "active"
```

## Quick Tools
- `dice: 1d20` - Roll dice inline
- [[00_GM_Resources/NPC_Tools/NPC_Generator|Generate NPC]]
- [[00_GM_Resources/Loot_Generators/Treasure_Generator|Generate Treasure]]

## Session Checklist
- [ ] Review previous session notes
- [ ] Prepare encounters
- [ ] Update NPC notes
- [ ] Prepare handouts
- [ ] Check player inventories
- [ ] Review active quests
""",

        "Quick_References/GM_Screen.md": """# GM Screen

## Difficulty Classes
| Task Difficulty | DC |
|----------------|-----|
| Very Easy | 5 |
| Easy | 10 |
| Medium | 15 |
| Hard | 20 |
| Very Hard | 25 |
| Nearly Impossible | 30 |

## Ability Check DCs
| Difficulty | DC | Example |
|------------|-----|---------|
| Trivial | 5 | Notice something in plain sight |
| Easy | 10 | Climb a knotted rope |
| Moderate | 15 | Hear a conversation through a door |
| Hard | 20 | Pick a good lock |
| Very Hard | 25 | Swim in stormy waters |
| Nearly Impossible | 30 | Convince a hostile enemy to surrender |

## Conditions
- **Blinded**: Can't see, auto-fail sight checks, attacks have disadvantage
- **Charmed**: Can't attack charmer, charmer has advantage on social checks
- **Deafened**: Can't hear, auto-fail hearing checks
- **Frightened**: Disadvantage while source of fear is in sight
- **Grappled**: Speed 0, can't benefit from speed bonus
- **Incapacitated**: Can't take actions or reactions
- **Invisible**: Heavily obscured, attacks have advantage
- **Paralyzed**: Incapacitated, can't move/speak, auto-fail STR/DEX saves
- **Petrified**: Transformed to stone, weight x10, unconscious
- **Poisoned**: Disadvantage on attacks and ability checks
- **Prone**: Disadvantage on attacks, melee attacks have advantage
- **Restrained**: Speed 0, disadvantage on DEX saves
- **Stunned**: Incapacitated, can't move, can barely speak
- **Unconscious**: Incapacitated, can't move/speak, unaware

## Travel Pace
| Pace | Distance/Hour | Distance/Day | Effect |
|------|---------------|--------------|--------|
| Slow | 2 miles | 18 miles | Able to use Stealth |
| Normal | 3 miles | 24 miles | — |
| Fast | 4 miles | 30 miles | −5 to passive Perception |

## Encounter Distance
| Terrain | Encounter Distance |
|---------|-------------------|
| Arctic, desert, farmland | 6d6 × 10 feet |
| Forest, hills, swamp | 2d8 × 10 feet |
| Mountain | 4d10 × 10 feet |
| Underwater | 3d6 × 10 feet |
| Urban | 2d6 × 10 feet |

## Light & Vision
| Source | Bright Light | Dim Light | Duration |
|--------|--------------|-----------|----------|
| Candle | 5 ft. | +5 ft. | 1 hour |
| Torch | 20 ft. | +20 ft. | 1 hour |
| Lantern | 30 ft. | +30 ft. | 6 hours/flask |
| Campfire | 30 ft. | +30 ft. | — |

## Cover
| Cover | Effect |
|-------|--------|
| Half Cover | +2 AC and DEX saves |
| Three-quarters | +5 AC and DEX saves |
| Total Cover | Can't be targeted directly |

## Exhaustion Levels
1. Disadvantage on ability checks
2. Speed halved
3. Disadvantage on attacks and saves
4. Hit point maximum halved
5. Speed reduced to 0
6. Death

## Quick NPCs
`dice: 1d20` for personality trait
1-4: Argumentative
5-8: Arrogant
9-12: Friendly
13-16: Honest
17-20: Hot-tempered
""",

        "Random_Tables/Random_Encounters.md": """# Random Encounters

## Urban Encounters (d20)
`dice: 1d20`

1. **Pickpocket attempt** - DC 15 Perception to notice
2. **Street performer** - Gathering a crowd
3. **Guard patrol** - 2d4 guards on routine patrol
4. **Merchant dispute** - Two merchants arguing over territory
5. **Lost child** - Looking for parents
6. **Drunk noble** - Causing a scene
7. **Street fight** - Two gangs clashing
8. **Religious procession** - Blocking the street
9. **Mysterious stranger** - Offers information for coin
10. **Fire!** - Building catches fire nearby
11. **Wanted poster** - Party member recognized
12. **Beggar** - Has useful information
13. **Cart accident** - Blocks the road
14. **Festival** - Impromptu celebration
15. **Thieves** - 1d4+1 bandits attempt robbery
16. **Animals loose** - 2d6 animals escape
17. **Magic mishap** - Spell goes wrong nearby
18. **Noble's carriage** - Demands right of way
19. **Secret meeting** - Overheard conspiracy
20. **Special** - Roll on special encounters

## Wilderness Encounters (d20)
`dice: 1d20`

1. **Bandits** - 1d6+2 bandits demand toll
2. **Merchant caravan** - Willing to trade
3. **Wild animals** - 2d4 wolves/bears
4. **Travelers** - 1d4 friendly NPCs
5. **Abandoned camp** - Recent, still warm
6. **Hunter's trap** - DC 15 Perception to spot
7. **Lost adventurer** - Needs help
8. **Ancient ruins** - Small dungeon entrance
9. **Weather change** - Storm approaching
10. **River crossing** - Bridge out
11. **Goblin ambush** - 2d6 goblins
12. **Hermit** - Offers shelter and wisdom
13. **Mysterious fog** - Visibility 30 ft
14. **Wounded creature** - Needs healing
15. **Patrol** - Local militia checking area
16. **Hidden cache** - DC 20 Investigation
17. **Tracks** - Large creature passed recently
18. **Fairy circle** - Fey presence
19. **Landslide/hazard** - Blocks path
20. **Special** - Roll on special encounters

## Dungeon Encounters (d20)
`dice: 1d20`

1. **Trap** - Pit/dart/pressure plate
2. **Wandering monster** - Roll on monster table
3. **Strange noise** - Echoes from ahead
4. **Dead adventurer** - Loot on body
5. **Locked door** - DC 15 to pick
6. **Secret door** - DC 15 Investigation
7. **Fountain** - Magic effects possible
8. **Statue** - May be animated
9. **Inscription** - Clue or warning
10. **Gas leak** - Poisonous fumes
11. **Unstable ceiling** - Risk of collapse
12. **Vermin swarm** - Rats/spiders/bats
13. **Abandoned camp** - Previous explorers
14. **Magic mouth** - Delivers message
15. **Puzzle door** - Requires solving
16. **Illusion** - Hides true path
17. **Treasure** - Minor, but trapped
18. **NPC** - Prisoner/lost/hiding
19. **Boss patrol** - Minions of main villain
20. **Special** - Unique to dungeon

## Reaction Table (2d6)
`dice: 2d6`

2-3: Hostile
4-5: Unfriendly  
6-8: Neutral
9-10: Friendly
11-12: Helpful
""",

        "Session_Prep/Session_Template.md": """# Session [Number] - [Date]

## Pre-Session Checklist
- [ ] Review previous session notes
- [ ] Update NPC status
- [ ] Prepare combat encounters
- [ ] Gather maps/handouts
- [ ] Review player notes
- [ ] Prepare music/ambiance

## Session Plan

### Opening (15 min)
- Recap previous session
- Address downtime activities
- Set the scene

### Act 1: [Title] (45 min)


### Act 2: [Title] (45 min)


### Act 3: [Title] (45 min)


### Potential Encounters
1. 
2. 
3. 

## NPCs This Session
| Name | Role | Location | Notes |
|------|------|----------|-------|
| | | | |

## Locations
- 

## Treasure/Rewards
- 

## Contingencies
**If players go off-script:**
- 

**If combat goes too fast/slow:**
- 

**If session runs short:**
- 

## Post-Session
- [ ] Update campaign notes
- [ ] Award XP/milestone
- [ ] Note player actions
- [ ] Update NPC attitudes
- [ ] Plan next session hooks
""",

        "Combat_Tools/Initiative_Tracker.md": """# Initiative Tracker

## Quick Setup
```dataview
TABLE HP, AC, Initiative
FROM #combat-ready
SORT Initiative DESC
```

## Initiative Order

| Initiative | Name | HP | AC | Conditions | Notes |
|------------|------|----|----|------------|-------|
| | PC: | | | | |
| | PC: | | | | |
| | PC: | | | | |
| | PC: | | | | |
| | NPC: | | | | |
| | NPC: | | | | |

## Round: 1

### Environmental Effects
- 

### Lair Actions (Initiative 20)
- 

### Legendary Actions (3/round)
- [ ] Used
- [ ] Used  
- [ ] Used

## Combat Log
**Round 1:**
- 

**Round 2:**
- 

## Quick Rules
- **Surprise**: Can't move or act first turn, no reactions
- **Cover**: Half (+2 AC), 3/4 (+5 AC), Total (can't target)
- **Flanking** (optional): Advantage when opposite ally
- **Opportunity Attacks**: Leave reach without Disengage

## Concentration Tracker
| Caster | Spell | DC | Duration |
|--------|-------|-----|----------|
| | | | |

## Conditions Applied
- 

## Post-Combat
- [ ] Calculate XP
- [ ] Distribute loot
- [ ] Check for deaths/unconscious
- [ ] Update resources used
""",

        "NPC_Tools/NPC_Generator.md": """# NPC Quick Generator

## Quick NPC Builder

### Basic Info
`dice: 1d20` for each category

**Race** (d20):
1-4: Human
5-6: Elf
7-8: Dwarf
9-10: Halfling
11-12: Tiefling
13-14: Dragonborn
15-16: Half-elf
17-18: Half-orc
19: Gnome
20: Special (Genasi, Aasimar, etc.)

**Occupation** (d20):
1. Merchant
2. Guard
3. Noble
4. Thief
5. Priest
6. Soldier
7. Artisan
8. Farmer
9. Scholar
10. Entertainer
11. Sailor
12. Hunter
13. Innkeeper
14. Blacksmith
15. Healer
16. Mage
17. Beggar
18. Messenger
19. Cook
20. Special

**Personality Trait** (d20):
1. Arrogant
2. Friendly
3. Suspicious
4. Honest
5. Greedy
6. Cowardly
7. Brave
8. Funny
9. Serious
10. Flirtatious
11. Nervous
12. Confident
13. Quiet
14. Loud
15. Helpful
16. Rude
17. Curious
18. Lazy
19. Energetic
20. Mysterious

**Physical Trait** (d20):
1. Tall
2. Short
3. Fat
4. Thin
5. Muscular
6. Scarred
7. Beautiful
8. Ugly
9. Clean
10. Dirty
11. Well-dressed
12. Poorly-dressed
13. Tattoos
14. Jewelry
15. Missing limb
16. Unusual hair
17. Distinctive voice
18. Limp
19. Unusual eyes
20. Birthmark

**Secret/Hook** (d20):
1. Owes money
2. In love
3. Seeking revenge
4. Has treasure map
5. Knows secret
6. Is spy
7. Cursed
8. Blessed
9. Hiding identity
10. Seeks item
11. Lost family
12. Former adventurer
13. Criminal past
14. Royal blood
15. Knows dungeon location
16. Has magic item
17. Cult member
18. Shapeshifter
19. Prophetic dreams
20. Special knowledge

## NPC Template

```markdown
# [Name]

**Race:** 
**Class/Occupation:** 
**Alignment:** 

## Description


## Personality


## Goals & Motivations


## Secret


## Relationships


## Stats (if needed)
- **AC:** 
- **HP:** 
- **Speed:** 
- **STR:** 10 (+0) **DEX:** 10 (+0) **CON:** 10 (+0)
- **INT:** 10 (+0) **WIS:** 10 (+0) **CHA:** 10 (+0)

## Abilities


## Inventory

```
""",

        "World_Building/Settlement_Builder.md": """# Settlement Builder

## Quick Settlement Generator

### Size (d6)
`dice: 1d6`
1. Thorp (20-80)
2. Hamlet (81-400)
3. Village (401-900)
4. Small Town (901-2000)
5. Large Town (2001-5000)
6. City (5001+)

### Notable Features (d20)
`dice: 1d20`
1. Ancient ruins nearby
2. Famous inn/tavern
3. Powerful wizard tower
4. Large temple
5. Thieves' guild
6. Fighting arena
7. Great library
8. Magical academy
9. Busy marketplace
10. Castle/keep
11. Hidden cult
12. Monster problem
13. Trade hub
14. Military outpost
15. Pilgrimage site
16. Cursed location
17. Portal/gateway
18. Natural wonder
19. Dungeon entrance
20. Dragon lair nearby

### Current Problem (d12)
`dice: 1d12`
1. Plague/disease
2. Bandit raids
3. Monster attacks
4. Political upheaval
5. Natural disaster
6. Economic crisis
7. Missing people
8. Cult activity
9. Noble conflict
10. Resource shortage
11. Magical phenomenon
12. War approaching

### Government Type (d8)
`dice: 1d8`
1. Autocracy (single ruler)
2. Democracy (elected council)
3. Oligarchy (few wealthy)
4. Theocracy (religious)
5. Magocracy (mages rule)
6. Military (martial law)
7. Anarchy (no government)
8. Republic (representatives)

## Settlement Template

```markdown
# [Settlement Name]

## Overview
**Population:** 
**Size:** 
**Government:** 
**Notable Features:** 

## Description


## Districts/Areas
1. 
2. 
3. 

## Notable NPCs
- 
- 
- 

## Shops & Services
- **Inn:** 
- **Tavern:** 
- **General Store:** 
- **Blacksmith:** 
- **Temple:** 

## Current Events


## Secrets


## Plot Hooks
1. 
2. 
3. 
```
""",

        "Loot_Generators/Treasure_Generator.md": """# Treasure Generator

## Individual Treasure (by CR)

### CR 0-4
`dice: 1d100`
- 01-30: `dice: 5d6` copper pieces
- 31-60: `dice: 4d6` silver pieces
- 61-70: `dice: 3d6` electrum pieces
- 71-95: `dice: 3d6` gold pieces
- 96-100: `dice: 1d6` platinum pieces

### CR 5-10
`dice: 1d100`
- 01-30: `dice: 4d6*10` copper + `dice: 1d6*10` electrum
- 31-60: `dice: 6d6*10` silver + `dice: 2d6*10` gold
- 61-70: `dice: 3d6*10` electrum + `dice: 2d6*10` gold
- 71-95: `dice: 6d6*10` gold
- 96-100: `dice: 3d6*10` gold + `dice: 1d6*10` platinum

### CR 11-16
`dice: 1d100`
- 01-20: `dice: 4d6*100` silver + `dice: 1d6*100` gold
- 21-35: `dice: 1d6*100` electrum + `dice: 1d6*100` gold
- 36-75: `dice: 2d6*100` gold + `dice: 1d6*10` platinum
- 76-100: `dice: 2d6*100` gold + `dice: 2d6*10` platinum

### CR 17+
`dice: 1d100`
- 01-15: `dice: 2d6*1000` electrum + `dice: 8d6*100` gold
- 16-55: `dice: 1d6*1000` gold + `dice: 1d6*100` platinum
- 56-100: `dice: 1d6*1000` gold + `dice: 2d6*100` platinum

## Magic Items

### Rarity by Level
| Character Level | Rarity |
|----------------|---------|
| 1-4 | Common |
| 5-8 | Uncommon |
| 9-12 | Rare |
| 13-16 | Very Rare |
| 17+ | Legendary |

### Quick Magic Item (d100)
`dice: 1d100`

**01-50: Consumable**
- 01-15: Potion of Healing
- 16-25: Scroll (random spell)
- 26-35: Potion (random)
- 36-45: Ammunition +1 (20)
- 46-50: Other consumable

**51-80: Permanent Minor**
- 51-55: +1 Weapon
- 56-60: +1 Armor/Shield
- 61-65: Bag of Holding
- 66-70: Cloak of Elvenkind
- 71-75: Boots of Speed
- 76-80: Ring of Protection

**81-95: Permanent Major**
- 81-85: +2 Weapon
- 86-90: +2 Armor/Shield
- 91-93: Staff/Rod/Wand
- 94-95: Rare wonderous item

**96-100: Legendary**
- Roll on legendary table

## Gemstones (d12)
`dice: 1d12`

**10 gp gems:**
1. Azurite
2. Agate  
3. Quartz
4. Obsidian

**50 gp gems:**
5. Bloodstone
6. Jasper
7. Moonstone
8. Onyx

**100 gp gems:**
9. Amber
10. Jade
11. Pearl
12. Topaz

## Art Objects (d10)
`dice: 1d10`

**25 gp:**
1-2: Silver jewelry

**250 gp:**
3-4: Carved statuette
5-6: Gold jewelry

**750 gp:**
7-8: Painting/tapestry

**2500 gp:**
9-10: Jeweled crown/scepter
""",

        "Campaign_Management/Campaign_Tracker.md": """# Campaign Tracker

## Campaign Overview
**Name:** 
**Theme:** 
**Tone:** 
**Starting Level:** 
**Current Level:** 

## The Party
| Player | Character | Class | Level | Status |
|--------|-----------|-------|-------|--------|
| | | | | |
| | | | | |

## Campaign Arcs

### Current Arc: 


### Completed Arcs:
1. 
2. 

### Future Arcs:
1. 
2. 

## Major NPCs
| Name | Role | Location | Relationship | Status |
|------|------|----------|--------------|---------|
| | | | | |

## Important Locations
- 
- 
- 

## Active Quests
```dataview
TABLE status, reward, deadline
FROM #quest
WHERE campaign = "{{campaign-name}}"
WHERE status = "active"
```

## Campaign Timeline
- **Session 1:** 
- **Session 2:** 
- **Session 3:** 

## House Rules
1. 
2. 
3. 

## Player Notes
- 

## DM Secrets
- 

## Inspiration Bank
- 
- 
- 
""",

        "Rules_References/Quick_Rules.md": """# Quick Rules Reference

## Action Economy
Each turn you can:
- **Move** up to your Speed
- **Action** (one)
- **Bonus Action** (if available)
- **Reaction** (one per round)
- **Free Actions** (interact with one object)

## Actions in Combat
- **Attack**: Make one melee or ranged attack
- **Cast a Spell**: Cast time of 1 action
- **Dash**: Double movement
- **Disengage**: No opportunity attacks
- **Dodge**: Attacks have disadvantage
- **Help**: Give advantage to ally
- **Hide**: Stealth check
- **Ready**: Prepare action with trigger
- **Search**: Perception/Investigation check
- **Use an Object**: Interact with object

## Advantage/Disadvantage Sources

### Advantage
- Attacking unseen target
- Attacking prone (melee)
- Attacking restrained/paralyzed/stunned
- Help action from ally
- Flanking (optional rule)

### Disadvantage
- Attacking unseen target
- Attacking while prone
- Attacking prone (ranged)
- Attacking in darkness
- Long range attacks
- Poisoned/Frightened condition

## Saving Throws
- **STR**: Grappling, physical restraints
- **DEX**: Dodging, area effects
- **CON**: Poison, disease, endurance
- **INT**: Illusions, mental puzzles
- **WIS**: Charm, fear, insight
- **CHA**: Possession, banishment, personality

## Skills Quick Reference
**Strength:**
- Athletics

**Dexterity:**
- Acrobatics
- Sleight of Hand
- Stealth

**Intelligence:**
- Arcana
- History
- Investigation
- Nature
- Religion

**Wisdom:**
- Animal Handling
- Insight
- Medicine
- Perception
- Survival

**Charisma:**
- Deception
- Intimidation
- Performance
- Persuasion

## Death & Dying
- **0 HP**: Unconscious and dying
- **Death Saves**: DC 10 CON save
  - 3 successes = stable
  - 3 failures = death
- **Natural 20**: Regain 1 HP
- **Natural 1**: Two failures
- **Damage at 0 HP**: One failure (crit = two)
- **Massive Damage**: Instant death if damage >= max HP

## Resting
**Short Rest (1 hour):**
- Spend Hit Dice to heal
- Regain some class abilities

**Long Rest (8 hours):**
- Regain all HP
- Regain half Hit Dice
- Regain spell slots
- Reset abilities

## Common Conditions Summary
- **Grappled**: Speed 0
- **Prone**: Disadvantage on attacks
- **Restrained**: Speed 0, disadvantage on DEX
- **Incapacitated**: No actions/reactions
- **Stunned**: Incapacitated + can't move
- **Paralyzed**: Incapacitated + auto-fail STR/DEX
- **Unconscious**: Incapacitated + unaware + prone
""",

        "00_GM_Resources_README.md": """# GM Resources Guide

## Welcome to Your GM Toolkit!

This comprehensive folder contains everything you need to run successful D&D 5e sessions.

### Quick Start
1. Open [[00_GM_DASHBOARD]] for your main control panel
2. Use [[Quick_References/GM_Screen]] during play
3. Prep sessions with [[Session_Prep/Session_Template]]
4. Generate content with the various tools

### Folder Structure

#### 📋 Quick_References
Fast access to rules, conditions, and DCs during play.

#### 🎲 Random_Tables  
Encounters, loot, NPCs for improvisation.

#### ⚔️ Encounter_Tools
Combat trackers and encounter builders.

#### 📝 Session_Prep
Templates and checklists for session preparation.

#### 🏰 Campaign_Management
Track your ongoing campaigns, arcs, and player progress.

#### 👥 NPC_Tools
Quick NPC generation and management.

#### 🌍 World_Building
Settlement builders and world creation tools.

#### 📖 Rules_References
Quick access to game mechanics and rulings.

#### ⚔️ Combat_Tools
Initiative tracking and combat management.

#### 💎 Loot_Generators
Treasure and magic item generation.

### Workflow Tips

**Before Session:**
1. Review previous notes
2. Prep encounters using tools
3. Generate any needed NPCs
4. Prepare handouts

**During Session:**
1. Keep GM Screen open
2. Use Initiative Tracker for combat
3. Reference random tables as needed
4. Take quick notes

**After Session:**
1. Update campaign tracker
2. Log important events
3. Note NPC changes
4. Plan next session hooks

### Customization
All templates can be modified to fit your style. Copy and rename to create campaign-specific versions.

### Plugin Integration
- **Dice Roller**: Use `dice: XdY` syntax
- **Initiative Tracker**: Links with combat tools
- **Dataview**: Automated quest and NPC tracking
- **Templater**: Quick content generation

Happy Gaming!
"""
    }
    
    # Create all files
    created = 0
    for filename, content in files_to_create.items():
        if "/" in filename:
            parts = filename.split("/")
            subfolder = parts[0]
            fname = parts[1]
            filepath = gm_dir / subfolder / fname
        else:
            filepath = gm_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        created += 1
        print(f"Created: {filepath.relative_to(vault_root)}")
    
    print(f"\n{'='*60}")
    print(f"GM RESOURCES CREATED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"Created {created} files in 00_GM_Resources/")
    print(f"Access your GM Dashboard at: 00_GM_Resources/00_GM_DASHBOARD.md")
    print(f"{'='*60}")
    
    return created

if __name__ == "__main__":
    create_gm_resources()