#!/usr/bin/env python3
import random
from pathlib import Path

def generate_npc():
    names = ["Aeliana", "Gareth", "Lyra", "Thane", "Vera", "Darius"]
    surnames = ["Stormwind", "Brightblade", "Goldleaf", "Ironforge", "Voidwalker"]
    races = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn"]
    occupations = ["Merchant", "Guard", "Scholar", "Noble", "Artisan"]
    
    name = f"{random.choice(names)} {random.choice(surnames)}"
    race = random.choice(races)
    occupation = random.choice(occupations)
    
    content = f'''---
type: npc
tags: [character, npc, generated]
status: draft
race: {race}
occupation: {occupation}
---

# {name}

## Quick Stats
- **Race:** {race}
- **Occupation:** {occupation}

## Description
*[Add description]*

## Background
*[Add background]*
'''
    
    vault_path = Path(__file__).parent.parent.parent
    npc_file = vault_path / "03_People" / f"{name.replace(' ', '_')}.md"
    npc_file.write_text(content)
    print(f"Generated NPC: {name}")

if __name__ == "__main__":
    generate_npc()
