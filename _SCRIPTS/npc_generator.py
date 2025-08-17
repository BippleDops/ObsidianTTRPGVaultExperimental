#!/usr/bin/env python3
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
    print("\n=== NPC GENERATOR ===\n")
    
    for i in range(3):
        npc = generate_npc()
        print(f"\nNPC {i+1}:")
        print(f"  {npc['race']} {npc['class']} (Level {npc['level']})")
        print(f"  Alignment: {npc['alignment']}")
        print(f"  HP: {npc['hp']}, AC: {npc['ac']}")
        print(f"  Traits: {', '.join(npc['traits'])}")
        print(f"  Motivation: {npc['motivation']}")
