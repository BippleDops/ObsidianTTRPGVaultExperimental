#!/usr/bin/env python3
"""
Enrich TTRPG vault notes with deeper links and expanded worldbuilding content.
Focuses on NPCs, locations, and quests that need more creative development.
"""

import os
import re
import random
from pathlib import Path
from typing import List, Dict, Set, Tuple
from datetime import datetime
import json

class WorldbuildingEnricher:
    def __init__(self, vault_root: Path):
        self.vault_root = Path(vault_root)
        self.enrichment_log = []
        self.links_added = 0
        self.content_expanded = 0
        
        # Load existing NPCs, locations, and concepts for cross-linking
        self.npcs = set()
        self.locations = set()
        self.factions = set()
        self.quests = set()
        self.scan_existing_content()
        
    def scan_existing_content(self):
        """Scan vault for existing entities to link."""
        # Scan NPCs
        npc_path = self.vault_root / "03_People"
        if npc_path.exists():
            for file in npc_path.rglob("*.md"):
                name = file.stem
                if not name.startswith("NPC"):
                    self.npcs.add(name)
                    
        # Scan locations
        world_path = self.vault_root / "02_Worldbuilding"
        if world_path.exists():
            for file in world_path.rglob("*.md"):
                self.locations.add(file.stem)
                
        # Scan quests
        quest_path = self.vault_root / "01_Adventures" / "quests"
        if quest_path.exists():
            for file in quest_path.rglob("*.md"):
                self.quests.add(file.stem)
                
    def find_enrichment_candidates(self, limit: int = 1000) -> List[Path]:
        """Find notes that would benefit from enrichment."""
        candidates = []
        priority_dirs = [
            "03_People",
            "02_Worldbuilding", 
            "01_Adventures/quests",
            "06_Sessions"
        ]
        
        for dir_path in priority_dirs:
            full_path = self.vault_root / dir_path
            if full_path.exists():
                for file in full_path.rglob("*.md"):
                    # Skip already enriched files
                    if "enriched" in file.stem.lower():
                        continue
                    
                    # Check file size - prefer smaller files that need content
                    size = file.stat().st_size
                    if size < 5000:  # Less than 5KB
                        candidates.append(file)
                        
                    if len(candidates) >= limit:
                        return candidates[:limit]
                        
        return candidates[:limit]
        
    def enrich_npc(self, file_path: Path, content: str) -> str:
        """Enrich an NPC file with relationships, motivations, and connections."""
        enriched = content
        
        # Add relationships section if missing
        if "## Relationships" not in content:
            relationships = self.generate_npc_relationships(file_path.stem)
            enriched += f"\n\n## Relationships\n{relationships}"
            
        # Add motivations if missing
        if "## Motivations" not in content:
            motivations = self.generate_npc_motivations(file_path.stem)
            enriched += f"\n\n## Motivations\n{motivations}"
            
        # Add plot hooks if missing
        if "## Plot Hooks" not in content:
            hooks = self.generate_npc_hooks(file_path.stem)
            enriched += f"\n\n## Plot Hooks\n{hooks}"
            
        # Add cross-references
        enriched = self.add_contextual_links(enriched, file_path)
        
        return enriched
        
    def enrich_location(self, file_path: Path, content: str) -> str:
        """Enrich a location with atmosphere, inhabitants, and secrets."""
        enriched = content
        
        # Add atmosphere if missing
        if "## Atmosphere" not in content:
            atmosphere = self.generate_location_atmosphere(file_path.stem)
            enriched += f"\n\n## Atmosphere\n{atmosphere}"
            
        # Add notable inhabitants if missing
        if "## Notable Inhabitants" not in content:
            inhabitants = self.generate_location_inhabitants(file_path.stem)
            enriched += f"\n\n## Notable Inhabitants\n{inhabitants}"
            
        # Add secrets if missing
        if "## Secrets" not in content:
            secrets = self.generate_location_secrets(file_path.stem)
            enriched += f"\n\n## Secrets\n{secrets}"
            
        # Add cross-references
        enriched = self.add_contextual_links(enriched, file_path)
        
        return enriched
        
    def enrich_quest(self, file_path: Path, content: str) -> str:
        """Enrich a quest with complications, rewards, and connections."""
        enriched = content
        
        # Add complications if missing
        if "## Complications" not in content:
            complications = self.generate_quest_complications(file_path.stem)
            enriched += f"\n\n## Complications\n{complications}"
            
        # Add rewards if missing
        if "## Rewards" not in content:
            rewards = self.generate_quest_rewards(file_path.stem)
            enriched += f"\n\n## Rewards\n{rewards}"
            
        # Add connections if missing
        if "## Connected Quests" not in content:
            connections = self.generate_quest_connections(file_path.stem)
            enriched += f"\n\n## Connected Quests\n{connections}"
            
        # Add cross-references
        enriched = self.add_contextual_links(enriched, file_path)
        
        return enriched
        
    def add_contextual_links(self, content: str, file_path: Path) -> str:
        """Add wiki-style links to related content."""
        enriched = content
        
        # Detect mentions of NPCs and add links
        for npc in list(self.npcs)[:20]:  # Limit to prevent over-linking
            if npc in content and f"[[{npc}]]" not in content:
                # Replace first occurrence with link
                enriched = enriched.replace(npc, f"[[{npc}]]", 1)
                self.links_added += 1
                
        # Detect mentions of locations
        for location in list(self.locations)[:20]:
            if location in content and f"[[{location}]]" not in content:
                enriched = enriched.replace(location, f"[[{location}]]", 1)
                self.links_added += 1
                
        return enriched
        
    def generate_npc_relationships(self, npc_name: str) -> str:
        """Generate relationship connections for an NPC."""
        relationships = []
        
        # Sample some existing NPCs to create relationships
        if self.npcs:
            sample_npcs = random.sample(list(self.npcs), min(3, len(self.npcs)))
            relationship_types = ["ally of", "rival to", "mentor of", "student of", 
                                 "secretly working with", "indebted to", "hunting"]
            
            for npc in sample_npcs:
                rel_type = random.choice(relationship_types)
                relationships.append(f"- {rel_type.capitalize()} [[{npc}]]")
                
        # Add faction relationships
        faction_relationships = [
            "- Member of the Shadow Parliament (secret)",
            "- Former agent of the Abyssal Trading Consortium",
            "- Informant for the Crystal Guard"
        ]
        relationships.append(random.choice(faction_relationships))
        
        return "\n".join(relationships) if relationships else "- No known relationships"
        
    def generate_npc_motivations(self, npc_name: str) -> str:
        """Generate motivations for an NPC."""
        primary_motivations = [
            "Seeks redemption for past failures in the Great Drowning",
            "Desires to uncover the truth about the Shadow Parliament",
            "Wants to restore their family's honor in the Depth Hierarchy",
            "Pursues forbidden knowledge of Void-touched magic",
            "Aims to bridge the divide between Aquabyssos and Aethermoor",
            "Searches for a cure to pressure sickness afflicting loved ones"
        ]
        
        secondary_motivations = [
            "Accumulate wealth through pearl trading",
            "Gain influence in their district",
            "Protect their community from raiders",
            "Master a forgotten combat technique",
            "Find a lost artifact from the surface world"
        ]
        
        motivations = f"""### Primary Motivation
{random.choice(primary_motivations)}

### Secondary Goals
- {random.choice(secondary_motivations)}
- {random.choice(secondary_motivations)}"""
        
        return motivations
        
    def generate_npc_hooks(self, npc_name: str) -> str:
        """Generate plot hooks involving an NPC."""
        hooks = [
            f"1. **The Missing Shipment**: {npc_name} approaches the party about a critical supply convoy that never arrived from the Bathyal Zone",
            f"2. **Blackmail Scheme**: The party discovers {npc_name} is being blackmailed by the Bloodtide Brotherhood",
            f"3. **Secret Meeting**: {npc_name} needs escorts to a clandestine meeting in the Abyssal Trenches",
            f"4. **Memory Theft**: {npc_name}'s memories have been stolen and sold on the black market",
            f"5. **Double Agent**: Evidence suggests {npc_name} is working for two opposing factions"
        ]
        
        return "\n".join(random.sample(hooks, 3))
        
    def generate_location_atmosphere(self, location_name: str) -> str:
        """Generate atmospheric description for a location."""
        if "Aquabyssos" in location_name or "Deep" in location_name:
            atmospheres = [
                "The bioluminescent algae cast an eerie blue-green glow across the carved coral walls, pulsing in rhythm with the deep currents.",
                "Pressure crystals hum with barely contained energy, their vibrations felt in the bones of all who pass through.",
                "Ancient whale songs echo through the chambers, carrying memories of the world before the drowning.",
                "The water here tastes of iron and old magic, thick with the weight of centuries."
            ]
        else:  # Aethermoor or sky-related
            atmospheres = [
                "Wind chimes of crystallized air sing in harmonious discord, predicting weather patterns days in advance.",
                "The platforms sway gently in the eternal winds, clouds passing through the walkways like curious spirits.",
                "Aether crystals float freely here, their soft glow competing with the endless sunset.",
                "The scent of ozone and distant storms permeates everything, a reminder of the void below."
            ]
            
        return random.choice(atmospheres)
        
    def generate_location_inhabitants(self, location_name: str) -> str:
        """Generate notable inhabitants for a location."""
        inhabitants = []
        
        # Generate 2-3 inhabitants with roles
        roles = [
            ("The Keeper", "maintains the sacred pressure seals"),
            ("The Merchant", "trades in memory pearls and dream silk"),
            ("The Guide", "knows secret passages through the depth zones"),
            ("The Exile", "cast out from the noble houses for forbidden research"),
            ("The Healer", "practices old medicine from before the drowning"),
            ("The Spy", "gathers information for multiple factions")
        ]
        
        for role, description in random.sample(roles, 2):
            inhabitants.append(f"- **{role}**: {description}")
            
        # Add a mysterious figure
        mysterious = [
            "- **The Whisper**: Only appears during the deep tides, speaking in ancient tongues",
            "- **The Watcher**: Never speaks, but knows everyone who passes through",
            "- **The Forgotten**: Claims to remember the surface world, but their stories change"
        ]
        inhabitants.append(random.choice(mysterious))
        
        return "\n".join(inhabitants)
        
    def generate_location_secrets(self, location_name: str) -> str:
        """Generate secrets for a location."""
        secrets = [
            "1. **Hidden Chamber**: A sealed room contains pre-drowning artifacts that could reshape understanding of history",
            "2. **Portal Network**: Secret passages connect to other depth zones, bypassing official channels",
            "3. **Corruption Source**: The location is built atop a Void-touched spring that slowly influences inhabitants",
            "4. **False Identity**: The location's official purpose masks its true function as a Shadow Parliament safehouse",
            "5. **Ancient Prison**: Deep beneath lies a prison holding something that should never be released",
            "6. **Memory Cache**: A hidden vault stores stolen memories from prominent citizens",
            "7. **Transformation Site**: Those who stay too long begin exhibiting signs of deep adaptation"
        ]
        
        return "\n".join(random.sample(secrets, 2))
        
    def generate_quest_complications(self, quest_name: str) -> str:
        """Generate complications for a quest."""
        complications = [
            "- **Rival Party**: Another group seeks the same objective with opposing methods",
            "- **Double Cross**: The quest giver has hidden motives that endanger the party",
            "- **Time Pressure**: Tidal shifts will make the objective inaccessible in 48 hours",
            "- **Moral Dilemma**: Success requires sacrificing innocent lives or principles",
            "- **Resource Scarcity**: Critical supplies are controlled by hostile factions",
            "- **Environmental Hazard**: Pressure storms make travel increasingly dangerous",
            "- **Political Ramifications**: Completing the quest will shift the balance of power"
        ]
        
        return "\n".join(random.sample(complications, 3))
        
    def generate_quest_rewards(self, quest_name: str) -> str:
        """Generate rewards for completing a quest."""
        rewards = f"""### Material Rewards
- **Gold**: {random.randint(100, 1000)} gp in mixed currencies (pearls and crystal shards)
- **Magic Item**: {random.choice(['Pressure-resistant armor', 'Breathing apparatus upgrade', 'Memory pearl (3 charges)', 'Depth compass', 'Void-touched weapon'])}

### Social Rewards
- **Reputation**: +1 standing with {random.choice(['the Merchant Guild', 'House Deepwater', 'the Shadow Parliament', 'Aquabyssos Navy'])}
- **Contact**: Gain ally in {random.choice(['the Bathyal Zone', 'Crystal Guard', 'Underground Railroad', 'Noble Houses'])}

### Information Rewards
- **Secret**: Learn the location of {random.choice(['ancient ruins', 'hidden cache', 'Shadow Parliament meeting', 'surface portal'])}
- **Map**: Receive charts of {random.choice(['uncharted trenches', 'trade routes', 'crystal deposits', 'safe passages'])}"""
        
        return rewards
        
    def generate_quest_connections(self, quest_name: str) -> str:
        """Generate connections to other quests."""
        connections = []
        
        # Link to existing quests if available
        if self.quests:
            sample_quests = random.sample(list(self.quests), min(2, len(self.quests)))
            for quest in sample_quests:
                connection_type = random.choice([
                    "leads directly to",
                    "shares NPCs with",
                    "opposes the goals of",
                    "provides information for"
                ])
                connections.append(f"- {connection_type.capitalize()} [[{quest}]]")
                
        # Add thematic connections
        connections.append("- Part of the larger Shadow Parliament conspiracy arc")
        connections.append("- Influences the Aquabyssos-Aethermoor peace negotiations")
        
        return "\n".join(connections)
        
    def enrich_file(self, file_path: Path) -> bool:
        """Enrich a single file based on its type."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_length = len(content)
            
            # Determine file type and enrich accordingly
            if "03_People" in str(file_path):
                enriched = self.enrich_npc(file_path, content)
            elif "02_Worldbuilding" in str(file_path):
                enriched = self.enrich_location(file_path, content)
            elif "01_Adventures" in str(file_path):
                enriched = self.enrich_quest(file_path, content)
            else:
                # Generic enrichment - just add links
                enriched = self.add_contextual_links(content, file_path)
                
            # Only write if actually enriched
            if len(enriched) > original_length:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(enriched)
                    
                self.content_expanded += 1
                self.enrichment_log.append({
                    'file': str(file_path.relative_to(self.vault_root)),
                    'original_size': original_length,
                    'new_size': len(enriched),
                    'expansion': len(enriched) - original_length
                })
                return True
                
        except Exception as e:
            print(f"Error enriching {file_path}: {e}")
            
        return False
        
    def run_enrichment(self, limit: int = 1000):
        """Run the enrichment process on selected files."""
        print(f"Finding {limit} candidates for enrichment...")
        candidates = self.find_enrichment_candidates(limit)
        
        print(f"Found {len(candidates)} files to enrich")
        print(f"Existing entities - NPCs: {len(self.npcs)}, Locations: {len(self.locations)}, Quests: {len(self.quests)}")
        
        enriched_count = 0
        for i, file_path in enumerate(candidates, 1):
            if i % 100 == 0:
                print(f"Progress: {i}/{len(candidates)} files processed")
                
            if self.enrich_file(file_path):
                enriched_count += 1
                
        # Save enrichment log
        log_path = self.vault_root / "09_Performance" / "enrichment_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'files_enriched': enriched_count,
                'links_added': self.links_added,
                'total_expansion': sum(e['expansion'] for e in self.enrichment_log),
                'details': self.enrichment_log[:100]  # Save first 100 for review
            }, f, indent=2)
            
        print(f"\n=== Enrichment Complete ===")
        print(f"Files enriched: {enriched_count}")
        print(f"Links added: {self.links_added}")
        print(f"Content expanded: {self.content_expanded} files")
        print(f"Log saved to: {log_path}")

def main():
    vault_root = Path.cwd()
    
    print("=== Worldbuilding Enrichment Tool ===")
    print(f"Vault root: {vault_root}")
    
    enricher = WorldbuildingEnricher(vault_root)
    enricher.run_enrichment(1000)

if __name__ == "__main__":
    main()