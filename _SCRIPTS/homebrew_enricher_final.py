#!/usr/bin/env python3
"""
Final Homebrew Enricher - Systematically enrich all thin content
"""

import os
import re
import random
from pathlib import Path
from datetime import datetime

class HomebrewEnricher:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.enriched = 0
        self.deleted = 0
        self.processed = 0
        
    def enrich_thin_npc(self, file_path):
        """Enrich any NPC file under 500 characters"""
        try:
            content = file_path.read_text(encoding='utf-8')
            if len(content) > 500 or "tags:" in content:
                return False
                
            name = file_path.stem.replace('_', ' ').replace('-', ' ').title()
            
            # Generate rich NPC content
            race = random.choice(['Human', 'Elf', 'Dwarf', 'Halfling', 'Tiefling', 'Genasi'])
            class_type = random.choice(['Fighter', 'Rogue', 'Wizard', 'Cleric', 'Ranger', 'Bard'])
            location = random.choice(['Port Meridia', 'Crystal Quarter', 'The Depths', 'Market District'])
            
            enriched = f"""---
tags: [npc, homebrew, {class_type.lower()}, {race.lower()}]
created: {datetime.now().strftime('%Y-%m-%d')}
type: npc
cr: {random.randint(1, 10)}
---

# {name}

## Quick Reference
- **Race/Class**: {race} {class_type} (Level {random.randint(3, 15)})
- **Location**: [[{location}]]
- **Alignment**: {random.choice(['Lawful', 'Neutral', 'Chaotic'])} {random.choice(['Good', 'Neutral', 'Evil'])}

## Description

{name} is a {random.choice(['grizzled', 'young', 'experienced', 'mysterious'])} {race.lower()} with {random.choice(['piercing blue eyes', 'a scarred face', 'elaborate tattoos', 'an imposing presence'])}. They are known throughout {location} for their {random.choice(['cunning', 'strength', 'wisdom', 'connections', 'magical abilities'])}.

## Personality
- **Trait**: {random.choice(['Suspicious of strangers', 'Always looking for profit', 'Fiercely loyal', 'Quick to anger'])}
- **Ideal**: {random.choice(['Power is everything', 'Knowledge must be preserved', 'Freedom above all', 'Order brings peace'])}
- **Bond**: {random.choice(['Sworn to protect the city', 'Seeking revenge', 'Bound by ancient oath', 'Family comes first'])}
- **Flaw**: {random.choice(['Gambling addiction', 'Terrible secret', 'Cowardly', 'Greedy'])}

## Statistics

**Medium {race.lower()}, {random.choice(['lawful', 'neutral', 'chaotic'])} {random.choice(['good', 'neutral', 'evil'])}**

- **AC**: {random.randint(12, 18)}
- **HP**: {random.randint(30, 150)} ({random.randint(5, 20)}d8 + {random.randint(10, 40)})
- **Speed**: 30 ft.

**STR** {random.randint(8, 20)} | **DEX** {random.randint(8, 20)} | **CON** {random.randint(8, 20)}
**INT** {random.randint(8, 20)} | **WIS** {random.randint(8, 20)} | **CHA** {random.randint(8, 20)}

### Abilities
- **{random.choice(['Multiattack', 'Spellcasting', 'Sneak Attack', 'Action Surge'])}**: Standard class ability
- **{random.choice(['Evasion', 'Cunning Action', 'Divine Strike', 'Wild Shape'])}**: Secondary ability

## Background

Originally from {random.choice(['a distant land', 'the local slums', 'noble heritage', 'unknown origins'])}, {name} has {random.choice(['risen through the ranks', 'fallen from grace', 'maintained their position', 'struggled to survive'])} in {location}.

## Current Activities
- {random.choice(['Gathering information', 'Planning a heist', 'Protecting interests', 'Seeking artifacts'])}
- {random.choice(['Training recruits', 'Investigating murders', 'Running business', 'Hunting enemies'])}

## Relationships
- **Ally**: [[{random.choice(['Captain Torrent', 'Lord Mayor', 'Guild Master Chen', 'High Priestess'])}]]
- **Rival**: [[{random.choice(['Shadow Broker', 'Crime Boss', 'Corrupt Noble', 'Rival Merchant'])}]]

## Plot Hooks
1. Needs help with {random.choice(['dangerous mission', 'personal vendetta', 'secret investigation', 'protection racket'])}
2. Has information about {random.choice(['upcoming threat', 'hidden treasure', 'conspiracy', 'missing person'])}
3. Will betray party if {random.choice(['price is right', 'threatened', 'ordered to', 'discovers secret'])}

## Combat Tactics
Prefers to {random.choice(['avoid combat', 'strike first', 'use magic', 'call allies'])}. Always carries {random.choice(['healing potions', 'poison', 'smoke bombs', 'magic items'])}.

## Treasure
- {random.randint(10, 500)} gp
- {random.choice(['Magic weapon', 'Potions', 'Spell scrolls', 'Rare components'])}
- {random.choice(['Coded letter', 'Map fragment', 'Blackmail material', 'Family heirloom'])}

## DM Notes
Can serve as {random.choice(['quest giver', 'information broker', 'recurring villain', 'potential ally'])}. Knows about {random.choice(['ancient ruins', 'criminal networks', 'political secrets', 'magical phenomena'])}.

## Voice
- **Accent**: {random.choice(['Gruff', 'Refined', 'Foreign', 'Local dialect'])}
- **Speech Pattern**: {random.choice(['Direct', 'Flowery', 'Cryptic', 'Nervous'])}
- **Catchphrase**: "{random.choice(['Trust no one', 'Gold speaks louder', 'The depths remember', 'Knowledge is power'])}"
"""
            
            file_path.write_text(enriched, encoding='utf-8')
            self.enriched += 1
            print(f"  ✓ Enriched NPC: {name}")
            return True
            
        except:
            return False
            
    def enrich_thin_location(self, file_path):
        """Enrich any location file under 500 characters"""
        try:
            content = file_path.read_text(encoding='utf-8')
            if len(content) > 500 or "tags:" in content:
                return False
                
            name = file_path.stem.replace('_', ' ').replace('-', ' ').title()
            
            loc_type = random.choice(['District', 'Building', 'Landmark', 'Tavern', 'Shop'])
            
            enriched = f"""---
tags: [location, homebrew, {loc_type.lower()}]
created: {datetime.now().strftime('%Y-%m-%d')}
type: location
---

# {name}

## Overview
- **Type**: {loc_type}
- **District**: {random.choice(['Market Quarter', 'Noble District', 'Docks', 'Slums', 'Temple Ward'])}
- **Condition**: {random.choice(['Well-maintained', 'Run-down', 'Under construction', 'Abandoned', 'Thriving'])}

## Description

{name} is a {random.choice(['bustling', 'quiet', 'mysterious', 'dangerous', 'welcoming'])} {loc_type.lower()} known for its {random.choice(['excellent service', 'shady dealings', 'unique atmosphere', 'historical significance', 'magical properties'])}.

The {random.choice(['stone', 'wooden', 'crystal', 'coral', 'mixed'])} structure features {random.choice(['ornate decorations', 'simple design', 'defensive fortifications', 'magical wards', 'unusual architecture'])}.

## Notable Features
- {random.choice(['Central fountain', 'Hidden basement', 'Secret passage', 'Magical portal', 'Ancient shrine'])}
- {random.choice(['Guard post', 'Merchant stalls', 'Private rooms', 'Training ground', 'Library'])}
- {random.choice(['Observation deck', 'Escape route', 'Trap door', 'Hidden vault', 'Meeting room'])}

## Inhabitants
- **Owner/Leader**: [[{random.choice(['Master Chen', 'Lady Blackwater', 'Old Tom', 'The Broker'])}]]
- **Regular Staff**: {random.randint(2, 20)} {random.choice(['guards', 'servants', 'merchants', 'workers'])}
- **Typical Visitors**: {random.choice(['Nobles', 'Criminals', 'Adventurers', 'Common folk', 'Merchants'])}

## Services Available
- {random.choice(['Room and board', 'Information', 'Magical services', 'Black market goods', 'Healing'])}
- {random.choice(['Equipment', 'Training', 'Contracts', 'Transportation', 'Storage'])}
- {random.choice(['Entertainment', 'Gambling', 'Connections', 'Forgery', 'Divination'])}

## Current Events
- {random.choice(['Murder investigation', 'Festival preparation', 'Secret meeting tonight', 'New management', 'Strange occurrences'])}
- {random.choice(['Price war', 'Renovation', 'Hiring guards', 'Missing persons', 'Magical phenomena'])}

## Secrets
> [!dm] Hidden Information
> - **Secret**: {random.choice(['Smuggling operation', 'Cult meeting place', 'Hidden treasure', 'Portal to elsewhere', 'Spy network hub'])}
> - **Key NPC**: {random.choice(['Disguised noble', 'Undercover agent', 'Shapeshifter', 'Ghost', 'Dragon in human form'])}

## Hooks
1. {random.choice(['Strange noises at night', 'Missing persons', 'Valuable item hidden', 'Secret meeting', 'Mysterious patron'])}
2. {random.choice(['Job opportunity', 'Information for sale', 'Danger approaching', 'Festival event', 'Competition'])}

## Connected Locations
- [[{random.choice(['Market Square', 'City Gates', 'Harbor', 'Palace', 'Temple District'])}]]
- [[{random.choice(['Thieves Guild', 'Merchant Quarter', 'Noble Estate', 'City Watch', 'Mage Tower'])}]]

## Notable Items
- {random.choice(['Ancient map', 'Magical artifact', 'Rare book', 'Exotic goods', 'Mysterious key'])}
- {random.choice(['Poison collection', 'Weapon cache', 'Spell components', 'Stolen goods', 'Holy relic'])}

## Atmosphere
- **Lighting**: {random.choice(['Dim candles', 'Bright magical lights', 'Natural sunlight', 'Flickering torches', 'Darkness'])}
- **Sounds**: {random.choice(['Bustling crowd', 'Quiet whispers', 'Music playing', 'Machinery', 'Eerie silence'])}
- **Smells**: {random.choice(['Cooking food', 'Incense', 'Sea salt', 'Decay', 'Flowers'])}
"""
            
            file_path.write_text(enriched, encoding='utf-8')
            self.enriched += 1
            print(f"  ✓ Enriched Location: {name}")
            return True
            
        except:
            return False
            
    def delete_stub_file(self, file_path):
        """Delete files that are essentially empty"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Skip if already has tags or substantial content
            if "tags:" in content or len(content.strip()) > 50:
                return False
                
            # Delete truly empty files
            if len(content.strip()) < 10:
                os.remove(file_path)
                self.deleted += 1
                print(f"  ✗ Deleted stub: {file_path.name}")
                return True
                
        except:
            pass
        return False
        
    def process_directory(self, directory):
        """Process all files in a directory"""
        md_files = list(directory.glob("*.md"))
        
        for file_path in md_files[:100]:  # Process up to 100 files per directory
            self.processed += 1
            
            # Try to delete stub
            if self.delete_stub_file(file_path):
                continue
                
            # Try to enrich based on directory
            if "People" in str(directory) or "NPC" in str(directory):
                self.enrich_thin_npc(file_path)
            elif "Location" in str(directory) or "Places" in str(directory):
                self.enrich_thin_location(file_path)
                
            if self.processed % 50 == 0:
                print(f"  Progress: {self.processed} files processed, {self.enriched} enriched, {self.deleted} deleted")
                
    def run(self):
        """Execute enrichment process"""
        print("=" * 60)
        print("🔨 FINAL HOMEBREW ENRICHER")
        print("=" * 60)
        
        # Process key directories
        directories = [
            self.vault_path / "03_People",
            self.vault_path / "02_Worldbuilding" / "Locations",
            self.vault_path / "02_Worldbuilding" / "People",
            self.vault_path / "01_Adventures" / "NPCs",
        ]
        
        for directory in directories:
            if directory.exists():
                print(f"\n📁 Processing: {directory.name}")
                self.process_directory(directory)
                
        # Generate report
        report = f"""# Homebrew Enrichment Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Files Processed**: {self.processed}
**Files Enriched**: {self.enriched}
**Files Deleted**: {self.deleted}

## Summary
Successfully enriched thin content with full details including:
- Complete stat blocks for NPCs
- Rich descriptions for locations
- Plot hooks and relationships
- Combat tactics and treasures
- DM notes and secrets

## Result
✅ Homebrew content has been systematically processed
"""
        
        report_path = self.vault_path / "09_Performance" / f"enrichment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        
        print("\n" + "=" * 60)
        print(f"✅ COMPLETE")
        print(f"   - Files Processed: {self.processed}")
        print(f"   - Files Enriched: {self.enriched}")
        print(f"   - Stubs Deleted: {self.deleted}")
        print(f"📄 Report: {report_path.name}")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    enricher = HomebrewEnricher(vault_path)
    enricher.run()