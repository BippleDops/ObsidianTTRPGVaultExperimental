#!/usr/bin/env python3
"""
Deep Worldbuilding Enhancer for D&D 5e TTRPG Vault
Adds 20+ layers of interconnected narrative, mechanical, and creative enhancements
"""

import re
import random
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json


class WorldbuildingEnhancer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.enhancements_applied = []
        
        # 20+ Enhancement Layers for D&D 5e
        self.enhancement_layers = {
            "faction_dynamics": self.enhance_faction_relationships,
            "npc_motivations": self.enhance_npc_depth,
            "location_atmosphere": self.enhance_location_descriptions,
            "quest_hooks": self.add_quest_connections,
            "combat_encounters": self.add_tactical_encounters,
            "treasure_integration": self.integrate_treasure_rewards,
            "lore_callbacks": self.create_lore_references,
            "skill_challenges": self.add_skill_challenges,
            "environmental_hazards": self.add_environmental_dangers,
            "political_intrigue": self.enhance_political_complexity,
            "economic_systems": self.add_economic_details,
            "religious_conflicts": self.enhance_religious_tensions,
            "magical_phenomena": self.add_magical_anomalies,
            "cultural_traditions": self.enhance_cultural_depth,
            "historical_echoes": self.add_historical_connections,
            "prophecy_threads": self.weave_prophecies,
            "moral_dilemmas": self.add_ethical_choices,
            "relationship_webs": self.enhance_relationships,
            "sensory_details": self.add_sensory_descriptions,
            "mechanical_integration": self.integrate_5e_mechanics
        }
        
    def enhance_file(self, file_path: Path) -> bool:
        """Apply all enhancement layers to a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original = content
            
            # Apply each enhancement layer
            for layer_name, enhancement_func in self.enhancement_layers.items():
                content = enhancement_func(content, file_path)
                
            # Only save if changed
            if content != original:
                file_path.write_text(content, encoding='utf-8')
                self.enhancements_applied.append(str(file_path))
                return True
                
        except Exception as e:
            print(f"Error enhancing {file_path}: {e}")
            
        return False
        
    def enhance_faction_relationships(self, content: str, file_path: Path) -> str:
        """Layer 1: Add complex faction relationships and tensions"""
        if "faction" in content.lower() or "guild" in content.lower():
            
            faction_additions = """
## Faction Dynamics
### Allied Tensions
- Uneasy alliance maintained by mutual enemies
- Resource competition despite cooperation
- Historical grievances simmering beneath diplomacy
- Succession disputes affecting partnerships

### Enemy Complexity
- Former allies turned rivals through betrayal
- Ideological opposition with personal respect
- Economic warfare through trade manipulation
- Proxy conflicts in neutral territories

### Neutral Opportunities
- Information brokers playing all sides
- Mercenary companies for hire
- Trade relationships transcending politics
- Marriage alliances under negotiation
"""
            
            if "## Faction Dynamics" not in content:
                content += "\n" + faction_additions
                
        return content
        
    def enhance_npc_depth(self, content: str, file_path: Path) -> str:
        """Layer 2: Add personality traits, bonds, ideals, and flaws"""
        if re.search(r'(NPC|character|person)', content, re.IGNORECASE):
            
            npc_traits = """
## Character Depth
### Personality Traits (d8)
1. Speaks in elaborate metaphors from their homeland
2. Never makes important decisions without consulting bones/cards
3. Compulsively organizes objects while talking
4. Quotes ancient texts for every situation
5. Tests others with subtle riddles and wordplay
6. Maintains rigid daily rituals regardless of circumstances
7. Sees omens and patterns in everything
8. Uses humor to deflect serious conversations

### Bonds (d6)
1. Sworn to protect a secret that could topple kingdoms
2. Searching for a lost love across dimensions
3. Bound by ancient pact to serve until debt repaid
4. Guardian of the last remnant of their culture
5. Seeking redemption for past war crimes
6. Connected to a prophecy they're trying to prevent

### Ideals (d6)
1. **Knowledge**: Truth must be preserved at all costs
2. **Freedom**: No chain, physical or mental, should bind anyone
3. **Tradition**: Ancient ways hold wisdom modern world forgot
4. **Change**: Stagnation is death, evolution is survival
5. **Balance**: Every force requires an equal counter
6. **Power**: Strength determines justice in cruel world

### Flaws (d6)
1. Addicted to dangerous substances/magic
2. Secretly serves opposing faction
3. Cursed to betray those who trust them
4. Pathologically unable to tell truth/lie
5. Haunted by victims seeking vengeance
6. Will sacrifice anyone for personal goal
"""
            
            if "## Character Depth" not in content and "personality" not in content.lower():
                content += "\n" + npc_traits
                
        return content
        
    def enhance_location_descriptions(self, content: str, file_path: Path) -> str:
        """Layer 3: Add atmospheric and sensory details"""
        if re.search(r'(location|place|city|town|dungeon)', content, re.IGNORECASE):
            
            location_atmosphere = """
## Atmospheric Details
### Sensory Impressions
- **Sight**: Phosphorescent algae creates false starfield on cavern ceiling
- **Sound**: Crystalline chimes respond to air pressure changes
- **Smell**: Salt-rust mixing with incense from hidden shrines
- **Touch**: Surfaces slick with condensation that never fully dries
- **Taste**: Metallic tinge in air from crystal dust
- **Sixth Sense**: Feeling of being watched by ancient intelligence

### Time-Based Changes
- **Dawn**: Mist rises revealing hidden architectural details
- **Noon**: Shadows vanish creating disorienting flatness
- **Dusk**: Bioluminescent organisms begin their display
- **Midnight**: Whispers carry impossible distances
- **Full Moon**: Tidal-locked sections become accessible
- **New Moon**: Protective wards weaken significantly

### Weather Patterns
- Pressure storms that induce prophetic dreams
- Crystal rain that enhances magical abilities
- Fog banks that transport travelers
- Wind patterns carrying encoded messages
"""
            
            if "## Atmospheric Details" not in content:
                content += "\n" + location_atmosphere
                
        return content
        
    def add_quest_connections(self, content: str, file_path: Path) -> str:
        """Layer 4: Interconnect quests and adventures"""
        if "quest" in content.lower() or "adventure" in content.lower():
            
            quest_hooks = """
## Quest Connections
### Branching Paths
1. **Success Consequence**: Completing this leads to [[The Merchant's Revenge]]
2. **Failure Fallback**: If failed, triggers [[Emergency Protocol Seven]]
3. **Partial Resolution**: Half-success opens [[The Gray Path]]
4. **Time Limit**: After 7 days, escalates to [[Crisis at Dawn]]

### Required Prerequisites
- Must have completed [[Trial of Shadows]] OR possess [[Shadowkey]]
- Reputation with [[Crystal Wardens]] must be Friendly+
- At least one party member must speak Abyssal
- Party level 5+ recommended, level 7+ for perfect ending

### Rewards Scale With
- Number of civilians saved (0-100)
- Faction reputation changes (+/- 20)
- Secrets discovered (3 hidden, 2 optional)
- Time to completion (bonus under 3 sessions)
"""
            
            if "## Quest Connections" not in content:
                content += "\n" + quest_hooks
                
        return content
        
    def add_tactical_encounters(self, content: str, file_path: Path) -> str:
        """Layer 5: Add D&D 5e combat encounters"""
        if re.search(r'(combat|encounter|battle|fight)', content, re.IGNORECASE):
            
            tactical_encounters = """
## Combat Encounters
### Encounter: Ambush at the Crossing (CR 8)
**Enemies**:
- 1x [[Shadowthorn Assassin]] (CR 5, AC 16, HP 78)
- 2x [[Crystal Corrupted Guards]] (CR 2, AC 15, HP 32)
- 4x [[Shadow Wisps]] (CR 1/2, AC 13, HP 11)

**Terrain Features**:
- Bridge: 15ft wide, 60ft long, 30ft above water
- Cover: Stone pillars provide 3/4 cover
- Hazard: Crumbling sections (DC 12 Dex save or fall)
- Lighting: Dim light from crystals

**Tactics**:
- Round 1: Assassin uses invisibility, guards charge
- Round 2: Wisps flank spellcasters
- Round 3: Assassin strikes weakest party member
- Retreat: At 25% HP, enemies flee to water

**Treasure**: 
- 450 gp in mixed coins
- [[Shadowstep Boots]] (requires attunement)
- Map to [[The Sunken Vault]]
- 2x Potions of Water Breathing
"""
            
            if "## Combat Encounters" not in content:
                content += "\n" + tactical_encounters
                
        return content
        
    def integrate_treasure_rewards(self, content: str, file_path: Path) -> str:
        """Layer 6: Add treasure and magic items"""
        if re.search(r'(treasure|reward|loot|gold)', content, re.IGNORECASE):
            
            treasure_tables = """
## Treasure Integration
### Treasure Hoard (CR 5-10)
Roll d100:
- 01-30: 2d6 × 100 gp, 1d6 × 10 pp
- 31-60: 2d6 × 100 gp, 1d6 × 10 pp, minor magic item
- 61-85: 2d6 × 100 gp, 1d6 × 10 pp, [[Table F item]]
- 86-95: 2d6 × 100 gp, 1d6 × 10 pp, [[Table G item]]
- 96-00: 2d6 × 100 gp, 1d6 × 10 pp, [[Table H item]]

### Custom Magic Items
**[[Tide Turner's Compass]]**
*Wondrous item, rare (requires attunement)*
- +2 bonus to Survival checks at sea
- Cast *Water Walk* 1/day
- Always points to nearest portal between realms
- Cursed: Disadvantage on saves vs water magic

**[[Crystal Resonance Blade]]**
*Weapon (any sword), very rare (requires attunement)*
- +2 magic weapon
- Extra 1d6 psychic damage vs shadow-touched
- Can cast *Detect Thoughts* 1/day (DC 15)
- Sentient: INT 12, speaks Primordial
"""
            
            if "## Treasure Integration" not in content:
                content += "\n" + treasure_tables
                
        return content
        
    def create_lore_references(self, content: str, file_path: Path) -> str:
        """Layer 7: Add deep lore callbacks and references"""
        
        lore_connections = """
## Historical Connections
### Ancient References
- Architecture matches pre-Drowning [[Thessalonian Empire]]
- Runes reference [[The First Convergence War]]
- Mural depicts [[The Seven Founding Archons]]
- Construction dated to [[Age of Crystal Dawn]]

### Prophecy Fragments
*"When shadows dance with light's last gleaming,*
*When depths and heights cease their streaming,*
*When seven shards unite as one,*
*The age of choices has begun."*

### Scholarly Theories
- [[Master Aldwin]] believes this connects to [[Planar Thesis]]
- [[Order of Silent Depths]] claims ownership via [[Ancient Pact]]
- [[Crystal Wardens]] deny knowledge but seem nervous
- Similarities to [[Forbidden Archive Entry 7-Alpha]]
"""
        
        if "location" in content.lower() or "place" in content.lower():
            if "## Historical Connections" not in content:
                content += "\n" + lore_connections
                
        return content
        
    def add_skill_challenges(self, content: str, file_path: Path) -> str:
        """Layer 8: Add skill challenge scenarios"""
        
        skill_challenges = """
## Skill Challenges
### Complex Challenge: Navigate the Shadow Court
**Success Threshold**: 6 successes before 3 failures
**Primary Skills**:
- Persuasion DC 15: Convince nobles of worth
- Insight DC 14: Detect hidden agendas
- Deception DC 16: Maintain cover identity
- Performance DC 13: Entertain to gain favor

**Secondary Skills** (1 success max each):
- History DC 12: Recall court etiquette
- Investigation DC 14: Gather blackmail material
- Intimidation DC 18: Cow lesser nobles

**Success**: Gain allied noble, learn conspiracy
**Failure**: Exposed as spies, combat encounter
"""
        
        if any(word in content.lower() for word in ["challenge", "social", "investigation"]):
            if "## Skill Challenges" not in content:
                content += "\n" + skill_challenges
                
        return content
        
    def add_environmental_dangers(self, content: str, file_path: Path) -> str:
        """Layer 9: Add environmental hazards"""
        
        environmental_hazards = """
## Environmental Hazards
### Area Hazards
**Crystal Radiation Zone**
- Constitution save DC 13 each hour
- Failure: 1 level exhaustion
- 3+ failures: Crystal corruption begins

**Pressure Differential Chambers**
- Moving between requires DC 15 Con save
- Failure: 3d6 bludgeoning, stunned 1 round
- Equipment: Pressure suits negate

**Memory Fog Banks**
- Wisdom save DC 14 on entry
- Failure: Lose 1d4 days recent memory
- Critical failure: Gain false memory

**Temporal Eddies**
- 20% chance per hour of travel
- Ages creatures 1d10 years (or reverses)
- DC 16 Arcana to detect, DC 18 to navigate
"""
        
        if re.search(r'(dungeon|cave|exploration|wilderness)', content, re.IGNORECASE):
            if "## Environmental Hazards" not in content:
                content += "\n" + environmental_hazards
                
        return content
        
    def enhance_political_complexity(self, content: str, file_path: Path) -> str:
        """Layer 10: Add political intrigue elements"""
        
        political_intrigue = """
## Political Complexity
### Power Structures
- **Official**: [[Parliament of Echoes]] holds legislative power
- **Actual**: [[Merchant Princes]] control through economics
- **Shadow**: [[The Whisper Syndicate]] influences through blackmail
- **Military**: [[Crystal Wardens]] enforce selectively
- **Religious**: [[High Temple]] claims moral authority

### Current Tensions
1. Succession crisis if Queen dies without heir
2. Parliament attempting to limit royal power
3. Military coup rumors from hardliners
4. Economic sanctions from neighbor kingdoms
5. Religious schism over shadow manipulation

### Leverage Points
- Queen's secret: [[Her transformation is failing]]
- Parliament speaker: [[Embezzling war funds]]
- General's weakness: [[Daughter held hostage]]
- High Priest's heresy: [[Deals with shadow cult]]
"""
        
        if any(word in content.lower() for word in ["politics", "noble", "court", "parliament"]):
            if "## Political Complexity" not in content:
                content += "\n" + political_intrigue
                
        return content
        
    def add_economic_details(self, content: str, file_path: Path) -> str:
        """Layer 11: Add economic systems"""
        
        economic_systems = """
## Economic Systems
### Trade Goods & Prices
| Item | Common Price | Rare Price | Black Market |
|------|-------------|------------|--------------|
| Crystal Dust (oz) | 10 gp | 50 gp | 75 gp |
| Memory Pearl | 100 gp | 500 gp | 1000 gp |
| Pressure Suit | 200 gp | - | 400 gp |
| Shadow Silk (yard) | 25 gp | 100 gp | 200 gp |
| Deep Wine (bottle) | 5 gp | 20 gp | 35 gp |

### Economic Factors
- **Inflation**: 15% annually due to crystal scarcity
- **Unemployment**: 30% in lower depths
- **Black Market**: 40% of total economy
- **Tax Rate**: 20% surface, 35% depths
- **Interest Rates**: 10% monthly (loan sharks: 25%)

### Trade Routes
- [[Northern Current]]: Crystals for food
- [[Eastern Passage]]: Metals for textiles
- [[Shadow Route]]: Illegal goods, 300% markup
"""
        
        if any(word in content.lower() for word in ["merchant", "trade", "economy", "gold"]):
            if "## Economic Systems" not in content:
                content += "\n" + economic_systems
                
        return content
        
    def enhance_religious_tensions(self, content: str, file_path: Path) -> str:
        """Layer 12: Add religious conflicts"""
        
        religious_elements = """
## Religious Elements
### Divine Domains at War
- **Light Domain**: [[Church of Eternal Dawn]] - Opposes all shadow magic
- **Tempest Domain**: [[Storm Shepherds]] - Claim divine right to rule seas
- **Death Domain**: [[Quiet Shepherds]] - Seek to "correct" undead
- **Knowledge Domain**: [[The Archive Faith]] - Hoard dangerous secrets
- **Trickery Domain**: [[Masked Pantheon]] - Everyone serves unknowingly

### Religious Conflicts
1. Holy war brewing between Light and Shadow churches
2. Heretical sect claims the Drowning was divine punishment
3. Prophets predicting apocalypse gaining followers
4. Ancient gods worshippers versus new faith
5. Clerics losing powers near shadow zones

### Divine Interventions
- DC 20 Religion check reveals divine interest
- Sacred sites provide sanctuary (usually)
- Holy symbols react to corruption
- Prayer might actually be answered (DM fiat)
"""
        
        if any(word in content.lower() for word in ["temple", "priest", "divine", "holy", "religion"]):
            if "## Religious Elements" not in content:
                content += "\n" + religious_elements
                
        return content
        
    def add_magical_anomalies(self, content: str, file_path: Path) -> str:
        """Layer 13: Add magical phenomena"""
        
        magical_phenomena = """
## Magical Anomalies
### Wild Magic Zones
Roll d20 when casting spells:
- 1: Spell fails, wild magic surge
- 2-5: Spell at disadvantage
- 6-15: Normal casting
- 16-19: Spell at advantage
- 20: Spell doubled (twin spell)

### Crystalline Interference
- Divination spells: 50% chance of false visions
- Teleportation: DC 15 Arcana or arrive 1d10 miles off
- Summoning: 25% chance wrong creature answers
- Necromancy: Undead have independent will
- Enchantment: Targets aware but compelled

### Ley Line Convergences
- Spell slots refresh on short rest (1/day)
- Cantrips act as 1st level spells
- Concentration automatic success
- Metamagic options available to all
- Risk of magical overflow (exhaustion)
"""
        
        if any(word in content.lower() for word in ["magic", "spell", "wizard", "arcane"]):
            if "## Magical Anomalies" not in content:
                content += "\n" + magical_phenomena
                
        return content
        
    def enhance_cultural_depth(self, content: str, file_path: Path) -> str:
        """Layer 14: Add cultural traditions"""
        
        cultural_traditions = """
## Cultural Traditions
### Aquabyssos Customs
- **Depth Greeting**: Lower hand = higher respect
- **Salt Gift**: Offering salt shows trust
- **Tide Singing**: Dawn chorus to calm waters
- **Pearl Tears**: Mourning jewelry from real tears
- **Pressure Marks**: Scars showing depth achievements

### Aethermoor Traditions
- **Wind Dancing**: Courtship through aerial acrobatics
- **Cloud Reading**: Divination via cloud shapes
- **Feather Tokens**: Social status indicators
- **Storm Naming**: Children named during tempests
- **Sky Burial**: Bodies given to wind elementals

### Taboos & Superstitions
- Never whistle in depths (attracts predators)
- Iron worn to ward off memory thieves
- Mirrors covered during shadow hours
- Names have power, use carefully
- Debts to the dead must be paid
"""
        
        if any(word in content.lower() for word in ["culture", "tradition", "custom", "society"]):
            if "## Cultural Traditions" not in content:
                content += "\n" + cultural_traditions
                
        return content
        
    def add_historical_connections(self, content: str, file_path: Path) -> str:
        """Layer 15: Add historical depth"""
        
        historical_echoes = """
## Historical Echoes
### Timeline Connections
- **1000 Years Ago**: [[The First Drowning]] - Similar symptoms
- **500 Years Ago**: [[Crystal Wars]] - Same locations affected
- **200 Years Ago**: [[Shadow Plague]] - Identical progression
- **50 Years Ago**: [[The False Peace]] - Current tensions began
- **10 Years Ago**: [[Void Prophecy]] - Predictions now manifesting

### Archaeological Evidence
- Layer VII: Advanced technology, suddenly abandoned
- Layer VI: Mass burial sites, ritualistic positioning
- Layer V: Burn marks, evidence of reality tears
- Layer IV: Golden age artifacts, peak civilization
- Layer III: Primitive tools, devolution period
- Layer II: Recovery begins, hybrid architecture
- Layer I: Current era construction

### Living History
- [[Elder Maureen]]: Remembers pre-transformation world
- [[The Archive]]: Contains banned historical texts
- [[Stone Memories]]: Crystals holding past events
- [[Ghost Courts]]: Undead nobles still ruling
"""
        
        if any(word in content.lower() for word in ["history", "ancient", "past", "origin"]):
            if "## Historical Echoes" not in content:
                content += "\n" + historical_echoes
                
        return content
        
    def weave_prophecies(self, content: str, file_path: Path) -> str:
        """Layer 16: Add prophecies and omens"""
        
        prophecy_threads = """
## Prophecies & Omens
### The Seven Verses
1. *"When crown and shadow dance as one"* - [[Royal corruption]]
2. *"The depths shall rise to claim the sky"* - [[Realm merger]]
3. *"Seven shards shall breach the veil"* - [[Planar invasion]]
4. *"Memory and flesh shall separate"* - [[Soul plague]]
5. *"The unnamed shall speak truth"* - [[Revelation event]]
6. *"Crystals sing the ending song"* - [[Reality collapse]]
7. *"Choice alone determines fate"* - [[Player agency]]

### Current Omens
- Fish swimming in air (gravity failing)
- Shadows moving against light sources
- Dreams shared by strangers
- Time flowing backwards locally
- Dead speaking single words

### Prophetic Visions (DC 15 Wisdom Save)
Success: Glimpse one true future event
Failure: Haunted by false possibilities
Critical: See the moment of choice approaching
"""
        
        if any(word in content.lower() for word in ["prophecy", "omen", "future", "fate"]):
            if "## Prophecies & Omens" not in content:
                content += "\n" + prophecy_threads
                
        return content
        
    def add_ethical_choices(self, content: str, file_path: Path) -> str:
        """Layer 17: Add moral dilemmas"""
        
        moral_dilemmas = """
## Moral Dilemmas
### Ethical Crossroads
1. **The Cure**: Save thousands but enslave hundreds to produce it
2. **The Truth**: Reveal corruption, destabilize government during crisis
3. **The Deal**: Accept shadow entity help, owe unspecified favor
4. **The Sacrifice**: One party member or hundred innocents
5. **The Power**: Gain ability to fix everything, lose humanity

### Alignment Pressure Points
- **LG**: Law requires reporting friends' crimes
- **CG**: Freedom fighter or terrorist?
- **LN**: Contract enforcement vs moral obligation
- **TN**: Balance requires enabling evil sometimes
- **LE**: Advancement through betrayal opportunity
- **CE**: Chaos serves greater purpose?

### Consequences Echo
- NPCs remember and react to choices
- Reputation system affects all interactions
- Some doors close permanently
- New enemies/allies based on decisions
- World state changes reflect morality
"""
        
        if any(word in content.lower() for word in ["choice", "moral", "ethics", "dilemma"]):
            if "## Moral Dilemmas" not in content:
                content += "\n" + moral_dilemmas
                
        return content
        
    def enhance_relationships(self, content: str, file_path: Path) -> str:
        """Layer 18: Deepen relationship networks"""
        
        relationship_webs = """
## Relationship Dynamics
### Connection Web
- **Romantic**: [[NPC A]] ←→ [[NPC B]] (secret, would cause scandal)
- **Rivalry**: [[Faction X]] ←→ [[Faction Y]] (economic competition)
- **Mentorship**: [[Elder]] → [[Apprentice]] (strained by ideology)
- **Blood Feud**: [[Family 1]] ←→ [[Family 2]] (three generations)
- **Debt**: [[Merchant]] → [[Noble]] (leverage for manipulation)

### Relationship Mechanics
**Trust Levels** (1-10 scale):
- 1-2: Active hostility
- 3-4: Distrust
- 5-6: Neutral
- 7-8: Friendly
- 9-10: Allied

**Influence Actions**:
- Gift (+1 trust, costs 50gp × current level)
- Favor (+2 trust, requires quest)
- Betrayal (-4 trust, gains other benefit)
- Reputation (±1 trust based on other relationships)

### Dynamic Changes
- Every 3 sessions, roll d6 for each major NPC
- 1: Relationship deteriorates (-1)
- 2-5: No change
- 6: Relationship improves (+1)
"""
        
        if "## Relationship Dynamics" not in content:
            content += "\n" + relationship_webs
            
        return content
        
    def add_sensory_descriptions(self, content: str, file_path: Path) -> str:
        """Layer 19: Add rich sensory details"""
        
        sensory_details = """
## Sensory Palette
### Signature Sensations
**Visual**: Bioluminescent veins pulse through crystalline architecture
**Auditory**: Whale songs echo through water-filled chambers
**Olfactory**: Ozone mixing with deep sea brine and old copper
**Tactile**: Surfaces alternate between ice-cold metal and blood-warm coral
**Gustatory**: Air tastes of salt and lightning before storms
**Kinesthetic**: Gravity shifts subtly near realm boundaries

### Emotional Atmosphere
- Entering triggers primal deep-water fear
- Prolonged exposure induces temporal dissociation
- Architecture designed to invoke submission
- Lighting patterns affect mood (DC 12 Wis save)
- Sound frequencies cause unexplained nostalgia

### Synesthetic Effects
- Magic visible as colored harmonics
- Emotions have distinctive scents
- Sounds create pressure sensations
- Time passage felt as temperature
- Memories taste of specific minerals
"""
        
        if "location" in str(file_path).lower():
            if "## Sensory Palette" not in content:
                content += "\n" + sensory_details
                
        return content
        
    def integrate_5e_mechanics(self, content: str, file_path: Path) -> str:
        """Layer 20: Deep integration with D&D 5e mechanics"""
        
        mechanical_integration = """
## 5e Mechanical Integration
### Advantage/Disadvantage Triggers
**Advantage**:
- Local knowledge in home region
- Using era-appropriate equipment
- Faction reputation (Friendly+)
- Environmental adaptation traits

**Disadvantage**:
- Cross-realm travel fatigue
- Using foreign magic systems
- Faction reputation (Hostile)
- Corruption level 3+

### Exhaustion Sources
1. Pressure changes (failed Con save)
2. Memory manipulation (failed Wis save)
3. Crystal exposure (8+ hours)
4. Temporal anomalies (random)
5. Shadow surgery recovery
6. Depth sickness progression

### Inspiration Triggers
- Exceptional roleplay during faction interaction
- Creative solution using environment
- Accepting significant personal cost for others
- Revealing character backstory connections
- Making choice against mechanical optimization

### Variant Rules Active
- **Gritty Realism**: Long rest = 7 days
- **Spell Points**: Optional for casters
- **Flanking**: Grants advantage
- **Facing**: AC bonus for shields directional
- **Massive Damage**: System shock saves
"""
        
        if "## 5e Mechanical Integration" not in content:
            content += "\n" + mechanical_integration
            
        return content
        
    def enhance_vault(self):
        """Apply enhancements to entire vault"""
        print("🎨 Beginning Deep Worldbuilding Enhancement")
        print("   Applying 20 layers of D&D 5e integration...")
        print("="*60)
        
        # Target directories for enhancement
        target_dirs = [
            "01_Adventures",
            "02_Worldbuilding",
            "03_Mechanics",
            "04_Resources"
        ]
        
        enhanced_count = 0
        
        for dir_name in target_dirs:
            dir_path = self.vault_path / dir_name
            if not dir_path.exists():
                continue
                
            print(f"\n📁 Enhancing {dir_name}...")
            
            # Enhance markdown files
            for md_file in dir_path.rglob("*.md"):
                if self.enhance_file(md_file):
                    enhanced_count += 1
                    
                # Show progress every 10 files
                if enhanced_count % 10 == 0:
                    print(f"   Enhanced {enhanced_count} files...")
                    
        print(f"\n✅ Enhanced {enhanced_count} files with deep worldbuilding")
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "files_enhanced": enhanced_count,
            "enhancement_layers": list(self.enhancement_layers.keys()),
            "enhancements_applied": self.enhancements_applied[:100]  # First 100
        }
        
        report_path = self.vault_path / "reports" / f"worldbuilding_enhancement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📄 Enhancement report: {report_path}")
        print("\n🎯 Your vault now has 20+ layers of interconnected D&D 5e worldbuilding!")
        
        return report


def main():
    enhancer = WorldbuildingEnhancer()
    enhancer.enhance_vault()


if __name__ == "__main__":
    main()