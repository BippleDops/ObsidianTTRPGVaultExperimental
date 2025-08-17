#!/usr/bin/env python3
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
    print("\n=== ENCOUNTER BUILDER ===\n")
    
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
        print(f"\nEncounter: {description}")
        print(f"  Total XP: {result['total_xp']}")
        print(f"  Adjusted XP: {result['adjusted_xp']}")
        print(f"  Difficulty: {result['difficulty']}")
