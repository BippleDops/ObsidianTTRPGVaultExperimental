#!/usr/bin/env python3
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
    print("\n=== LOOT GENERATOR ===\n")
    
    # Generate for different CRs
    for cr in [1, 5, 10, 15]:
        print(f"\nCR {cr} Loot:")
        loot = generate_loot(cr)
        print(f"  Gold: {loot['gold']} gp")
        if loot['items']:
            print(f"  Items: {', '.join(loot['items'])}")
    
    print("\n=== TREASURE HOARD (CR 10) ===\n")
    hoard = create_treasure_hoard(10)
    print(f"Coins: {hoard['coins']}")
    print(f"Gems: {hoard['gems']}")
    print(f"Magic Items: {hoard['magic_items']}")
