#!/usr/bin/env python3
"""
Steps 81-90: Advanced Features
This phase adds advanced TTRPG features and tools
"""
import random
import json
from pathlib import Path
from datetime import datetime

def create_initiative_tracker():
    """Step 81-82: Create initiative tracker tool"""
    print("\n⚔️ CREATING INITIATIVE TRACKER (Steps 81-82)")
    
    tracker_html = """<!DOCTYPE html>
<html>
<head>
    <title>Initiative Tracker</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #2e2e2e; color: #fff; }
        .container { max-width: 600px; margin: auto; }
        .character { 
            background: #3e3e3e; 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
        }
        .current { background: #4a4a6a; border: 2px solid #7a7aaa; }
        button { 
            background: #5a5a8a; 
            color: white; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px;
            cursor: pointer;
        }
        button:hover { background: #6a6a9a; }
        input { 
            background: #4e4e4e; 
            color: white; 
            border: 1px solid #6e6e6e;
            padding: 5px;
            margin: 5px;
        }
        h1 { color: #9a9aca; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Combat Initiative Tracker</h1>
        
        <div>
            <input type="text" id="charName" placeholder="Character Name">
            <input type="number" id="initiative" placeholder="Initiative">
            <input type="number" id="hp" placeholder="HP">
            <button onclick="addCharacter()">Add</button>
        </div>
        
        <div id="tracker"></div>
        
        <div style="margin-top: 20px;">
            <button onclick="nextTurn()">Next Turn</button>
            <button onclick="sortInitiative()">Sort by Initiative</button>
            <button onclick="clearAll()">Clear All</button>
        </div>
        
        <div style="margin-top: 20px;">
            <strong>Round: <span id="round">1</span></strong>
        </div>
    </div>
    
    <script>
        let characters = [];
        let currentIndex = 0;
        let round = 1;
        
        function addCharacter() {
            const name = document.getElementById('charName').value;
            const init = parseInt(document.getElementById('initiative').value);
            const hp = parseInt(document.getElementById('hp').value);
            
            if (name && !isNaN(init)) {
                characters.push({
                    name: name,
                    initiative: init,
                    hp: hp || 0,
                    maxHp: hp || 0
                });
                
                document.getElementById('charName').value = '';
                document.getElementById('initiative').value = '';
                document.getElementById('hp').value = '';
                
                updateDisplay();
            }
        }
        
        function updateDisplay() {
            const tracker = document.getElementById('tracker');
            tracker.innerHTML = '';
            
            characters.forEach((char, index) => {
                const div = document.createElement('div');
                div.className = 'character' + (index === currentIndex ? ' current' : '');
                div.innerHTML = `
                    <span>${char.name} (Init: ${char.initiative})</span>
                    <span>HP: ${char.hp}/${char.maxHp}</span>
                    <button onclick="removeCharacter(${index})">Remove</button>
                `;
                tracker.appendChild(div);
            });
        }
        
        function nextTurn() {
            currentIndex = (currentIndex + 1) % characters.length;
            if (currentIndex === 0 && characters.length > 0) {
                round++;
                document.getElementById('round').textContent = round;
            }
            updateDisplay();
        }
        
        function sortInitiative() {
            characters.sort((a, b) => b.initiative - a.initiative);
            currentIndex = 0;
            updateDisplay();
        }
        
        function removeCharacter(index) {
            characters.splice(index, 1);
            if (currentIndex >= characters.length) {
                currentIndex = 0;
            }
            updateDisplay();
        }
        
        function clearAll() {
            characters = [];
            currentIndex = 0;
            round = 1;
            document.getElementById('round').textContent = round;
            updateDisplay();
        }
    </script>
</body>
</html>"""
    
    tracker_path = Path("00_System/Tools/initiative_tracker.html")
    tracker_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tracker_path, 'w') as f:
        f.write(tracker_html)
    
    print(f"  ✓ Created: {tracker_path}")
    return tracker_path

def create_loot_generator():
    """Step 83-84: Create random loot generator"""
    print("\n💰 CREATING LOOT GENERATOR (Steps 83-84)")
    
    generator_script = """#!/usr/bin/env python3
'''Random Loot Generator for D&D 5e'''
import random

def generate_loot(cr_level=1):
    '''Generate random loot based on CR level'''
    
    # Coin amounts by CR
    coin_tables = {
        'low': (1, 100),      # CR 0-4
        'medium': (100, 1000), # CR 5-10
        'high': (1000, 10000)  # CR 11+
    }
    
    # Common items
    common_items = [
        "Potion of Healing",
        "Rope of Climbing (50 ft)",
        "Bag of Holding",
        "Cloak of Elvenkind",
        "Boots of Speed",
        "Ring of Protection",
        "Amulet of Health"
    ]
    
    # Rare items
    rare_items = [
        "Flame Tongue Sword",
        "Staff of Power",
        "Belt of Giant Strength",
        "Armor of Invulnerability",
        "Ring of Regeneration"
    ]
    
    # Determine tier
    if cr_level <= 4:
        tier = 'low'
        item_pool = common_items
        item_chance = 0.3
    elif cr_level <= 10:
        tier = 'medium'
        item_pool = common_items + rare_items[:2]
        item_chance = 0.5
    else:
        tier = 'high'
        item_pool = common_items + rare_items
        item_chance = 0.7
    
    # Generate gold
    min_gold, max_gold = coin_tables[tier]
    gold = random.randint(min_gold, max_gold)
    
    # Generate items
    items = []
    if random.random() < item_chance:
        num_items = random.randint(1, 3)
        items = random.sample(item_pool, min(num_items, len(item_pool)))
    
    return {
        'gold': gold,
        'items': items
    }

def create_treasure_hoard(cr_level=10):
    '''Create a major treasure hoard'''
    hoard = {
        'coins': {
            'copper': random.randint(100, 10000),
            'silver': random.randint(100, 5000),
            'gold': random.randint(100, 2500),
            'platinum': random.randint(10, 100) if cr_level > 5 else 0
        },
        'gems': [],
        'art': [],
        'magic_items': []
    }
    
    # Add gems
    if cr_level > 3:
        gem_values = [10, 50, 100, 500, 1000]
        num_gems = random.randint(1, cr_level)
        for _ in range(num_gems):
            value = random.choice(gem_values[:min(cr_level//3, len(gem_values))])
            hoard['gems'].append(f"{value}gp gem")
    
    # Add magic items
    loot = generate_loot(cr_level)
    hoard['magic_items'] = loot['items']
    
    return hoard

# Example usage
if __name__ == "__main__":
    print("\\n=== LOOT GENERATOR ===\\n")
    
    # Generate for different CRs
    for cr in [1, 5, 10, 15]:
        print(f"\\nCR {cr} Loot:")
        loot = generate_loot(cr)
        print(f"  Gold: {loot['gold']} gp")
        if loot['items']:
            print(f"  Items: {', '.join(loot['items'])}")
    
    print("\\n=== TREASURE HOARD (CR 10) ===\\n")
    hoard = create_treasure_hoard(10)
    print(f"Coins: {hoard['coins']}")
    print(f"Gems: {hoard['gems']}")
    print(f"Magic Items: {hoard['magic_items']}")
"""
    
    generator_path = Path("_SCRIPTS/loot_generator.py")
    with open(generator_path, 'w') as f:
        f.write(generator_script)
    
    print(f"  ✓ Created: {generator_path}")
    return generator_path

def create_npc_generator():
    """Step 85-86: Create quick NPC generator"""
    print("\n👤 CREATING NPC GENERATOR (Steps 85-86)")
    
    generator = """#!/usr/bin/env python3
'''Quick NPC Generator'''
import random
from pathlib import Path
from datetime import datetime

# NPC data
RACES = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Tiefling", "Half-Orc", "Gnome"]
CLASSES = ["Fighter", "Wizard", "Cleric", "Rogue", "Ranger", "Bard", "Barbarian", "Sorcerer"]
ALIGNMENTS = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", 
              "True Neutral", "Chaotic Neutral", "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
TRAITS = ["Brave", "Cowardly", "Greedy", "Generous", "Suspicious", "Trusting", 
          "Arrogant", "Humble", "Ambitious", "Content"]
MOTIVATIONS = ["Wealth", "Power", "Knowledge", "Fame", "Family", "Revenge", 
               "Justice", "Survival", "Love", "Adventure"]

def generate_npc():
    '''Generate a random NPC'''
    
    # Basic info
    race = random.choice(RACES)
    char_class = random.choice(CLASSES)
    level = random.randint(1, 20)
    alignment = random.choice(ALIGNMENTS)
    
    # Personality
    traits = random.sample(TRAITS, 2)
    motivation = random.choice(MOTIVATIONS)
    
    # Stats (simplified)
    stats = {
        'STR': random.randint(8, 18),
        'DEX': random.randint(8, 18),
        'CON': random.randint(8, 18),
        'INT': random.randint(8, 18),
        'WIS': random.randint(8, 18),
        'CHA': random.randint(8, 18)
    }
    
    # Calculate derived stats
    hp = (random.randint(1, 10) + (stats['CON'] - 10) // 2) * level
    ac = 10 + (stats['DEX'] - 10) // 2
    
    return {
        'race': race,
        'class': char_class,
        'level': level,
        'alignment': alignment,
        'traits': traits,
        'motivation': motivation,
        'stats': stats,
        'hp': max(hp, 1),
        'ac': ac
    }

def save_npc(npc_data, name=None):
    '''Save NPC to markdown file'''
    
    if not name:
        name = f"NPC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    content = f'''# {name}

## Basic Information
- **Race**: {npc_data['race']}
- **Class**: {npc_data['class']}
- **Level**: {npc_data['level']}
- **Alignment**: {npc_data['alignment']}

## Statistics
- **HP**: {npc_data['hp']}
- **AC**: {npc_data['ac']}

### Abilities
- **STR**: {npc_data['stats']['STR']}
- **DEX**: {npc_data['stats']['DEX']}
- **CON**: {npc_data['stats']['CON']}
- **INT**: {npc_data['stats']['INT']}
- **WIS**: {npc_data['stats']['WIS']}
- **CHA**: {npc_data['stats']['CHA']}

## Personality
- **Traits**: {', '.join(npc_data['traits'])}
- **Motivation**: {npc_data['motivation']}

---
*Generated: {datetime.now().isoformat()}*
'''
    
    npc_path = Path("03_People") / f"{name}.md"
    npc_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Don't actually save in test mode
    print(f"Would save to: {npc_path}")
    return content

# Example usage
if __name__ == "__main__":
    print("\\n=== NPC GENERATOR ===\\n")
    
    for i in range(3):
        npc = generate_npc()
        print(f"\\nNPC {i+1}:")
        print(f"  {npc['race']} {npc['class']} (Level {npc['level']})")
        print(f"  Alignment: {npc['alignment']}")
        print(f"  HP: {npc['hp']}, AC: {npc['ac']}")
        print(f"  Traits: {', '.join(npc['traits'])}")
        print(f"  Motivation: {npc['motivation']}")
"""
    
    generator_path = Path("_SCRIPTS/npc_generator.py")
    with open(generator_path, 'w') as f:
        f.write(generator)
    
    print(f"  ✓ Created: {generator_path}")
    return generator_path

def create_encounter_builder():
    """Step 87-88: Create encounter difficulty calculator"""
    print("\n📊 CREATING ENCOUNTER BUILDER (Steps 87-88)")
    
    builder = """#!/usr/bin/env python3
'''D&D 5e Encounter Builder'''

# XP thresholds by character level
XP_THRESHOLDS = {
    1: {'easy': 25, 'medium': 50, 'hard': 75, 'deadly': 100},
    2: {'easy': 50, 'medium': 100, 'hard': 150, 'deadly': 200},
    3: {'easy': 75, 'medium': 150, 'hard': 225, 'deadly': 400},
    4: {'easy': 125, 'medium': 250, 'hard': 375, 'deadly': 500},
    5: {'easy': 250, 'medium': 500, 'hard': 750, 'deadly': 1100},
    6: {'easy': 300, 'medium': 600, 'hard': 900, 'deadly': 1400},
    7: {'easy': 350, 'medium': 750, 'hard': 1100, 'deadly': 1700},
    8: {'easy': 450, 'medium': 900, 'hard': 1400, 'deadly': 2100},
    9: {'easy': 550, 'medium': 1100, 'hard': 1600, 'deadly': 2400},
    10: {'easy': 600, 'medium': 1200, 'hard': 1900, 'deadly': 2800},
}

# Encounter multipliers
MULTIPLIERS = {
    1: 1.0,
    2: 1.5,
    3: 2.0,
    4: 2.0,
    5: 2.5,
    6: 2.5,
    7: 3.0,
    8: 3.0
}

def calculate_encounter_difficulty(party_levels, monster_xp_values):
    '''Calculate encounter difficulty'''
    
    # Calculate party thresholds
    thresholds = {'easy': 0, 'medium': 0, 'hard': 0, 'deadly': 0}
    
    for level in party_levels:
        if level in XP_THRESHOLDS:
            for difficulty in thresholds:
                thresholds[difficulty] += XP_THRESHOLDS[level][difficulty]
    
    # Calculate encounter XP
    total_xp = sum(monster_xp_values)
    num_monsters = len(monster_xp_values)
    
    # Apply multiplier
    multiplier = MULTIPLIERS.get(min(num_monsters, 8), 4.0)
    adjusted_xp = int(total_xp * multiplier)
    
    # Determine difficulty
    if adjusted_xp < thresholds['easy']:
        difficulty = "Trivial"
    elif adjusted_xp < thresholds['medium']:
        difficulty = "Easy"
    elif adjusted_xp < thresholds['hard']:
        difficulty = "Medium"
    elif adjusted_xp < thresholds['deadly']:
        difficulty = "Hard"
    else:
        difficulty = "Deadly"
    
    return {
        'total_xp': total_xp,
        'adjusted_xp': adjusted_xp,
        'difficulty': difficulty,
        'thresholds': thresholds
    }

# Example usage
if __name__ == "__main__":
    print("\\n=== ENCOUNTER BUILDER ===\\n")
    
    # Example party: 4 level 5 characters
    party = [5, 5, 5, 5]
    
    # Example encounters
    encounters = [
        ([450], "1 Brown Bear (CR 1)"),
        ([450, 450], "2 Brown Bears"),
        ([450, 100, 100], "1 Brown Bear + 2 Wolves"),
        ([1800], "1 Young Red Dragon (CR 10)")
    ]
    
    for monster_xp, description in encounters:
        result = calculate_encounter_difficulty(party, monster_xp)
        print(f"\\nEncounter: {description}")
        print(f"  Total XP: {result['total_xp']}")
        print(f"  Adjusted XP: {result['adjusted_xp']}")
        print(f"  Difficulty: {result['difficulty']}")
"""
    
    builder_path = Path("_SCRIPTS/encounter_builder.py")
    with open(builder_path, 'w') as f:
        f.write(builder)
    
    print(f"  ✓ Created: {builder_path}")
    return builder_path

def create_dm_screen():
    """Step 89-90: Create digital DM screen"""
    print("\n📋 CREATING DM SCREEN (Steps 89-90)")
    
    dm_screen = """# Digital DM Screen

## Quick References

### Difficulty Classes
- **Very Easy**: DC 5
- **Easy**: DC 10
- **Medium**: DC 15
- **Hard**: DC 20
- **Very Hard**: DC 25
- **Nearly Impossible**: DC 30

### Advantage/Disadvantage
- **Advantage**: Roll twice, take higher
- **Disadvantage**: Roll twice, take lower
- Don't stack - either have it or don't

### Conditions
- **Blinded**: Auto-fail sight checks, attacks have disadvantage, attackers have advantage
- **Charmed**: Can't attack charmer, charmer has advantage on social checks
- **Frightened**: Disadvantage while source in sight, can't willingly move closer
- **Grappled**: Speed 0, ends if grappler incapacitated
- **Paralyzed**: Incapacitated, auto-fail STR/DEX saves, attacks have advantage, hits are crits
- **Poisoned**: Disadvantage on attacks and ability checks
- **Prone**: Disadvantage on attacks, melee attacks have advantage, ranged have disadvantage
- **Restrained**: Speed 0, disadvantage on attacks/DEX saves, attackers have advantage
- **Stunned**: Incapacitated, auto-fail STR/DEX saves, attackers have advantage
- **Unconscious**: Incapacitated, prone, auto-fail STR/DEX saves, attacks have advantage

### Actions in Combat
- **Attack**: Make one melee or ranged attack
- **Cast a Spell**: Cast time of 1 action
- **Dash**: Double movement speed
- **Disengage**: Movement doesn't provoke opportunity attacks
- **Dodge**: Attacks have disadvantage, DEX saves have advantage
- **Help**: Give ally advantage on next check/attack
- **Hide**: Make Stealth check
- **Ready**: Prepare action with trigger
- **Search**: Make Perception/Investigation check
- **Use an Object**: Interact with object

### Cover
- **Half Cover (+2 AC)**: Low wall, furniture, creature
- **3/4 Cover (+5 AC)**: Arrow slit, thick tree
- **Full Cover**: Can't be targeted directly

### Travel Pace
| Pace | Distance/Hour | Distance/Day | Effect |
|------|--------------|--------------|---------|
| Slow | 2 miles | 18 miles | Can stealth |
| Normal | 3 miles | 24 miles | - |
| Fast | 4 miles | 30 miles | -5 to passive Perception |

### Random Names
**Male**: Gareth, Theron, Marcus, Aldric, Finn
**Female**: Lyra, Asha, Mira, Elara, Sage
**Surnames**: Stormwind, Ironforge, Brightblade, Shadowmere

### Quick NPCs
Roll d6 for trait:
1. Nervous - wrings hands, stutters
2. Gruff - short answers, scowls
3. Friendly - smiles, chatty
4. Suspicious - narrow eyes, questions
5. Tired - yawns, slouches
6. Energetic - animated, loud

### Improvised Damage
- **1d10**: Burned by coals, hit by falling bookcase
- **2d10**: Struck by lightning, stumbling into fire pit
- **4d10**: Hit by falling rubble, crushed by rocks
- **10d10**: Crushed by compacting walls, lava
- **18d10**: Submerged in lava, hit by flying fortress
- **24d10**: Tumbling into vortex to Elemental Chaos

## Session Tools
- [[initiative_tracker.html|Initiative Tracker]]
- [[_SCRIPTS/loot_generator.py|Loot Generator]]
- [[_SCRIPTS/npc_generator.py|NPC Generator]]
- [[_SCRIPTS/encounter_builder.py|Encounter Builder]]

---
*Your complete DM reference*
"""
    
    screen_path = Path("00_System/DM_Screen.md")
    with open(screen_path, 'w') as f:
        f.write(dm_screen)
    
    print(f"  ✓ Created: {screen_path}")
    
    # Create summary
    summary_path = Path("09_Performance/advanced_features_phase8.md")
    with open(summary_path, 'w') as f:
        f.write("# Phase 8 Advanced Features (Steps 81-90)\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("## Tools Created\n\n")
        f.write("- **Initiative Tracker**: Interactive HTML combat tracker\n")
        f.write("- **Loot Generator**: Random treasure generation\n")
        f.write("- **NPC Generator**: Quick NPC creation\n")
        f.write("- **Encounter Builder**: Difficulty calculator\n")
        f.write("- **DM Screen**: Quick reference guide\n\n")
        f.write("## Files\n")
        f.write("- `00_System/Tools/initiative_tracker.html`\n")
        f.write("- `_SCRIPTS/loot_generator.py`\n")
        f.write("- `_SCRIPTS/npc_generator.py`\n")
        f.write("- `_SCRIPTS/encounter_builder.py`\n")
        f.write("- `00_System/DM_Screen.md`\n")
    
    print(f"  ✓ Summary: {summary_path}")
    
    return screen_path

def main():
    print("=" * 60)
    print("PHASE 8: ADVANCED FEATURES (STEPS 81-90)")
    print("=" * 60)
    
    # Create all tools
    create_initiative_tracker()
    create_loot_generator()
    create_npc_generator()
    create_encounter_builder()
    create_dm_screen()
    
    print("\n" + "=" * 60)
    print("STEPS 81-90 COMPLETE!")
    print("=" * 60)
    print("\n✓ Initiative tracker created")
    print("✓ Loot generator ready")
    print("✓ NPC generator built")
    print("✓ Encounter builder complete")
    print("✓ DM screen assembled")
    print("\n🎯 90% of glidepath complete (90/100 steps)")
    
    return True

if __name__ == "__main__":
    main()