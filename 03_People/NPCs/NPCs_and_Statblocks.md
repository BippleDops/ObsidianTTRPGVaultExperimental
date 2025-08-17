---

title: NPCs_and_Statblocks
type: npc
tags:
- npc

created: '2025-01-15'
modified: '2025-01-15'
aliases: ["NPCs and Statblocks"]
status: active
priority: normal
category: 12 Research
subcategory: D&D Sourcebooks
related: []
cssclass: standard
publish: false

---

 # NPCs_and_Statblocks ---

## Description

Detailed description pending.
title: NPCs and Statblocks
type: NPCs
tags:
- research
- world/both
- status/active
- npcs/shadow-conspiracy
- active
- statblocks
- 5e-compatible

created: '2025-08-13'
modified: '2025-08-14'
status: active
updated: '2025-08-13T17:05:00.000000'
world: Both

--- # Shadow Conspiracy: NPCs and Statblocks

*Complete NPC Roster with 5e-Compatible Statistics* > [!info] 5e Statblock Format

> All NPCs use official D&D 5th Edition statblock format compatible with:
> - Monster Manual design principles
> - Challenge Rating calculations from DMG
> - Obsidian 5e Statblocks plugin for display
> - Initiative Tracker plugin for combat management ### Vex Shadowthorn

*Shadow Surgeon Prime*```statblock
name: Vex Shadowthorn
size: Medium
type: humanoid
subtype: (human)
alignment: lawful evil
ac: 18 (shadow-woven armor)
hp: 180 (`dice: `dice: 24d8`` + 72)
speed: 30 ft., shadow step 60 ft.
str: 12
dex: 20
con: 16
int: 22
wis: 18
cha: 16
saves: - dex: 10 - int: 11 - wis: 9
skills: - deception: 8 - insight: 9 - medicine: 14 - perception: 9 - stealth: 15
damage_resistances: necrotic, psychic
damage_immunities: poison
condition_immunities: charmed, frightened, poisoned
senses: darkvision 120 ft., truesight 30 ft., passive Perception 19
languages: Common, Deep Speech, telepathy 120 ft.
cr: 15
traits: - name: Legendary Resistance (3/Day) desc: If Vex fails a saving throw, they can choose to succeed instead. - name: Shadow Surgeon desc: Vex has advantage on Medicine checks and can perform consciousness surgery to implant shadow personalities (requires 10 minutes and incapacitated target). - name: Multiple Personalities desc: Vex contains 7 distinct shadow personalities. When reduced to 0 hit points, a new personality takes over with full hit points (once per day per personality). - name: Shadow Network desc: Vex can communicate telepathically with any shadow-touched creature within 10 miles.
actions: - name: Multiattack desc: Vex makes three attacks with their Shadow Scalpels or uses Shadow Surgery once. - name: Shadow Scalpel desc: "Melee Weapon Attack: +10 to hit, reach 5 ft., one target. Hit: 15 (`dice: `dice: 2d8`` + 6) slashing damage plus 14 (`dice: `dice: 4d6``) psychic damage. The target must succeed on a **DC 18** Wisdom saving throw or have disadvantage on Wisdom saves for 1 minute." - name: Shadow Surgery (Recharge 5-6) desc: "Vex attempts emergency consciousness manipulation on a creature within 10 feet. The target must make a **DC 19** Wisdom saving throw or be stunned for 1 minute while Vex implants a shadow command. The target can repeat the save at the end of each turn." - name: Duplicate Self desc: "Vex creates `dice: `dice: 1d4`` shadow duplicates of themselves. Each has 40 hit points, AC 15, and can make one Shadow Scalpel attack per turn. They last for 1 hour or until destroyed."
legendary_actions: - name: Legendary Actions (3) desc: Vex can take 3 legendary actions, choosing from the options below. - name: Move desc: Vex moves up to their speed without provoking opportunity attacks. - name: Attack desc: Vex makes one Shadow Scalpel attack. - name: Shadow Phase (Costs 2 Actions) desc: Vex becomes incorporeal until the start of their next turn, gaining resistance to all damage except force and radiant. - name: Consciousness Probe (Costs 3 Actions) desc: Vex reads the surface thoughts of all creatures within 30 feet and learns their current emotional state and immediate intentions.```**Personality**: Cold, clinical, genuinely believes shadow control brings peace and order. Lost family in cross-realm war, sees free will as the cause of all suffering. **Tactics**: - Uses duplicates to confuse enemies
- Targets spellcasters first to prevent magical detection
- Retreats through shadows when below 50 HP
- Always has escape route planned **Treasure**: - Shadow Surgeon's Tools (legendary item)
- Memory Crystal containing original personality
- Codex of Shadow Surgery techniques --- ### Commander Eclipse Nethermore

*Military Shadow Infiltrator* name: Commander Eclipse Nethermore
type: aberration
subtype: (shadow-touched)
alignment: neutral evil
ac: 17 (shadow plate)
hp: 142 (`dice: `dice: 15d10`` + 60)
speed: 30 ft.
str: 18
dex: 14
con: 18
int: 15
wis: 13 - str: 8 - con: 8 - cha: 7 - athletics: 8 - intimidation: 7 - deception: 7
damage_resistances: necrotic; bludgeoning, piercing, and slashing from nonmagical attacks
senses: darkvision 60 ft., passive Perception 11
languages: Common, Aquan, Auran
cr: 12 - name: Action Surge (1/Short Rest) desc: Eclipse can take one additional action on their turn. - name: Shadow Duplicate Network desc: Eclipse has 3 shadow duplicates in different locations. When one dies, consciousness transfers to another. All duplicates must be killed to defeat Eclipse permanently. - name: Military Codes desc: Eclipse knows all military passwords and protocols for both realms' armed forces. Desc: Eclipse makes three Shadow Blade attacks or two Shadow Blade attacks and uses Command Shadows. - name: Shadow Blade desc: "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 13 (`dice: `dice: 2d8`` + 4) slashing damage plus 9 (`dice: `dice: 2d8``) necrotic damage." - name: Command Shadows desc: "Eclipse commands shadow-touched soldiers within 60 feet. Up to 3 creatures must make a **DC 15** Wisdom saving throw or follow Eclipse's orders for 1 minute." - name: Shadow Artillery (Recharge 5-6) desc: "Eclipse calls shadow bombardment in a 20-foot radius within 120 feet. Each creature must make a **DC 16** Dexterity saving throw, taking 35 (`dice: `dice: 10d6``) necrotic damage on a failed save, or half on success."
reactions: - name: Shadow Parry desc: Eclipse adds 4 to AC against one melee attack that would hit them. **Personality**: Military precision, believes in order through strength, sees democracy as weakness **Tactics**:
- Commands shadow soldiers from rear
- Uses artillery to control battlefield
- Sacrifices duplicates to escape
- Coordinates with other conspiracy members --- ### Shadow Parliament Member

*Generic Corrupted Official* name: Shadow Parliament Member
subtype: (any race)
ac: 15 (shadow-touched robes)
hp: 78 (`dice: `dice: 12d8`` + 24)
str: 10
con: 14
int: 16
wis: 12
cha: 18 - int: 6 - insight: 4 - persuasion: 7 - investigation: 6
languages: Common, any two others
cr: 8 - name: Shadow Touched desc: The parliament member has resistance to psychic damage and immunity to being charmed. - name: Unified Voting desc: When within 100 feet of other shadow parliament members, they act on the same initiative and share tactical information. - name: Political Immunity desc: The parliament member cannot be arrested or detained by normal authorities without special warrants. Desc: The parliament member makes two attacks with Shadow Gavel or casts one spell. - name: Shadow Gavel desc: "Melee Weapon Attack: +3 to hit, reach 5 ft., one target. Hit: 4 (`dice: `dice: 1d8``) bludgeoning damage plus 7 (`dice: `dice: 2d6``) psychic damage." - name: Legislative Manipulation desc: "The parliament member forces one creature within 30 feet to make a **DC 15** Wisdom saving throw. On a failure, the target is compelled to agree with the next statement made (as suggestion spell)." - name: Shadow Decree (1/Day) desc: "All creatures within 60 feet must make a **DC 15** Wisdom saving throw or be affected as if by mass suggestion spell for 1 hour."
spells: - desc: The parliament member is a 9th-level spellcaster using Charisma (spell save **DC 15**, +7 to hit) - 1st level (4 slots): charm person, disguise self, expeditious retreat - 2nd level (3 slots): detect thoughts, hold person, suggestion - 3rd level (3 slots): counterspell, fear, hypnotic pattern - 4th level (3 slots): confusion, phantasmal killer - 5th level (1 slot): dominate person, modify memory --- ### Agent Marina Deepstrike

*Former Shadow Surgeon* name: Marina Deepstrike
subtype: (triton)
alignment: chaotic good
ac: 16 (studded leather)
hp: 110 (`dice: `dice: 13d8`` + 52)
speed: 30 ft., swim 30 ft.
str: 14
dex: 18
wis: 15
cha: 13 - dex: 8 - int: 7 - wis: 6 - acrobatics: 8 - insight: 6 - investigation: 7 - medicine: 10 - perception: 6 - stealth: 12
damage_resistances: psychic
senses: darkvision 60 ft., passive Perception 16
languages: Common, Primordial, Deep Speech
cr: 10 - name: Shadow Surgery Knowledge desc: Marina knows how to detect and reverse shadow surgery. She has advantage on Medicine checks related to shadow manipulation. - name: Mental Fortitude desc: Marina has advantage on saves against charm and fear effects. - name: Evasion desc: When subjected to an effect that allows a Dexterity save for half damage, Marina takes no damage on success and half on failure. Desc: Marina makes three attacks with her Reversal Blades. - name: Reversal Blade desc: "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 11 (`dice: `dice: 2d6`` + 4) slashing damage. If the target is shadow-touched, they take an additional 7 (`dice: `dice: 2d6``) radiant damage." - name: Consciousness Liberation (3/Day) desc: "Marina can free a creature from shadow control. The target makes a **DC 15** Wisdom saving throw with advantage, ending shadow control on a success." - name: Shadow Detection desc: "Marina reveals all shadow-touched creatures within 60 feet, outlining them in silver light for 1 minute." - name: Counter-Surgery desc: When a creature within 30 feet is targeted by shadow manipulation, Marina can use her reaction to grant them advantage on their save. **Personality**: Haunted by her past, determined to atone, protective of innocents, distrustful but loyal once earned **Information She Provides**:
- Shadow surgery techniques and weaknesses
- List of known shadow surgeons
- Location of hidden facilities
- Counter-shadow resistance training --- ### Lord Aurelius Goldwave

*Reformed Conspirator* name: Lord Aurelius Goldwave
alignment: lawful neutral
ac: 15 (noble's attire with hidden armor)
hp: 65 (`dice: `dice: 10d8`` + 20)
str: 11
int: 17 - cha: 6 - deception: 6 - persuasion: 9
senses: passive Perception 11
languages: Common, Draconic, Elvish
cr: 5 - name: Economic Mastery desc: Aurelius has advantage on Intelligence checks related to economics, trade, and fice. - name: Noble Privilege desc: Aurelius can secure audiences with nobility and has diplomatic immunity in most regions. - name: Reformed Shadow desc: Aurelius retains some shadow abilities but uses them for good. He has resistance to psychic damage. Desc: Aurelius makes two attacks with his Hidden Blade or uses Economic Warfare. - name: Hidden Blade desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 6 (`dice: `dice: 1d6`` + 3) piercing damage plus 3 (`dice: `dice: 1d6``) poison damage." - name: Economic Warfare desc: "Aurelius manipulates markets to harm enemies. One organization must make a **DC 15** Wisdom saving throw or lose `dice: `dice: 10d100`` gold pieces in value over the next week." - name: Shadow Confession (1/Day) desc: "Aurelius reveals conspiracy secrets, granting allies advantage on Investigation and Insight checks related to the Shadow Conspiracy for 24 hours." - name: Defensive Accounting desc: When targeted by an attack, Aurelius can use economic knowledge to predict patterns, adding +3 to AC against that attack. **Personality**: Guilt-ridden, seeking redemption, brilliant economist, protective of family legacy **Resources He Provides**:
- Conspiracy ficial records
- Safe houses and hidden vaults
- Bribery funds (10,000 gp)
- Trade route intelligence --- ### Archivist Supreme Indexa

*Leader of Memory Keepers* name: Archivist Supreme Indexa
subtype: (elf)
alignment: lawful good
ac: 12 (15 with mage armor)
hp: 99 (`dice: `dice: 18d8`` + 18)
str: 9
con: 12
int: 20
cha: 14 - int: 9 - wis: 8 - arcana: 9 - history: 13 - insight: 8 - investigation: 13
senses: darkvision 60 ft., passive Perception 14
languages: All - name: Perfect Memory desc: Indexa remembers everything she has ever experienced and has advantage on all Intelligence checks. - name: Memory Magic desc: Indexa can cast spells related to memory and consciousness without using spell slots (3/day each). - name: Archive Access desc: Indexa can summon any information from the Memory Keeper archives as an action. - desc: Indexa is an 18th-level wizard (spell save **DC 17**, +9 to hit) - Cantrips (at will): mage hand, minor illusion, prestidigitation, mending - 1st level (4 slots): detect magic, identify, mage armor, shield - 2nd level (3 slots): detect thoughts, locate object, see invisibility - 3rd level (3 slots): clairvoyance, dispel magic, nondetection - 4th level (3 slots): arcane eye, locate creature, divination - 5th level (3 slots): contact other plane, legend lore, modify memory - 6th level (1 slot): true seeing, contingency - 7th level (1 slot): plane shift, project image - 8th level (1 slot): mind blank, antipathy/sympathy - 9th level (1 slot): foresight, time stop - name: Memory Restoration desc: "Indexa restores a creature's true memories, removing all shadow manipulation and false memories. The process takes 10 minutes." - name: Archive Summoning desc: "Indexa calls upon the collective knowledge of the Memory Keepers, gaining advantage on all ability checks for 1 minute." - name: Consciousness Shield (3/Day) desc: "Indexa creates a protective barrier around up to 6 creatures within 30 feet, granting immunity to psychic damage and charm effects for 1 hour." **Personality**: Ancient wisdom, protective of knowledge, believes information should be free, opposes all forms of mind control **Resources She Provides**:
- True history of the conspiracy
- Memory restoration services
- Consciousness protection training
- Ancient knowledge and prophecies --- ### Shadow Surgeon Apprentice

*Generic Enemy Medic* name: Shadow Surgeon Apprentice
subtype: (any)
ac: 14 (leather armor)
hp: 45 (`dice: `dice: 7d8`` + 14)
dex: 15
wis: 14
cha: 12 - medicine: 8 - deception: 4 - stealth: 5
senses: darkvision 30 ft., passive Perception 12
languages: Common, Deep Speech
cr: 3 - name: Surgical Precision desc: The apprentice has advantage on Medicine checks and deals an extra `dice: `dice: 2d6`` damage on critical hits. Desc: The apprentice makes two scalpel attacks. Desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 5 (`dice: `dice: 1d4`` + 3) slashing damage plus 3 (`dice: `dice: 1d6``) psychic damage." - name: Quick Surgery (Recharge 5-6) desc: "The apprentice attempts minor shadow surgery. One creature within 5 feet must make a **DC 13** Wisdom saving throw or be stunned until the end of the apprentice's next turn." --- ### Memory Keeper Guardian

*Ally Temple Defender* name: Memory Keeper Guardian
type: construct
subtype: ac: 18 (natural armor)
hp: 85 (`dice: `dice: 10d10`` + 30)
str: 16
dex: 10
int: 10
wis: 16
cha: 8
damage_immunities: poison, psychic
condition_immunities: charmed, exhaustion, frightened, paralyzed, petrified, poisoned
senses: darkvision 60 ft., passive Perception 13
languages: understands Common but can't speak
cr: 6 - name: Memory Core desc: The guardian contains archived memories. If destroyed, these memories are released to all creatures within 30 feet. - name: Consciousness Shield desc: Allies within 10 feet have advantage on saves against psychic damage and mind-affecting abilities. Desc: The guardian makes two slam attacks. - name: Slam desc: "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 12 (`dice: `dice: 2d8`` + 3) bludgeoning damage." - name: Memory Pulse (Recharge 5-6) desc: "The guardian releases a wave of memories. All creatures within 30 feet must make a **DC 14** Wisdom saving throw or be incapacitated for 1 turn as they process the memories." --- ### Quick Shadow Operative`dice: `dice: `dice: 1d12```| d12 | Role | CR | Special Ability |

|-----|------|----|-----------------| | 1-2 | Shadow Spy | 2 | Invisibility 1/day |
| 3-4 | Corrupted Guard | 3 | False memories |
| 5-6 | Shadow Merchant | 4 | Economic manipulation |
| 7-8 | Mind Thief | 5 | Steal memories |
| 9-10 | Consciousness Broker | 6 | Trade personalities |
| 11-12 | Shadow Enforcer | 7 | Command duplicates | ### Ally Contact Types`dice: `dice: `dice: 1d10```| d10 | Contact Type | Information Provided |

|-----|--------------|---------------------|
| 1-2 | Whistleblower | Conspiracy evidence |
| 3-4 | Double Agent | Enemy movements |
| 5-6 | Victim's Family | Personal stakes |
| 7-8 | Investigator | Case files |
| 9-10 | Reformed Shadow | Inside knowledge | --- ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Secret Connections *[Hidden from players]* Connected to The Hidden Covenant - Control trade routes ## Plot Hooks - Strange sightings suggest a conspiracy

- An heirloom has gone missing and war looms ## 12_Research Specific Content Contextual improvement based on 12_Research ## 12_Research Specific Content Contextual improvement based on 12_Research

## Notes

*Additional notes*

#mechanics/combat
#mechanics/dice
#story/plot
#story/story
#story/lore
#world/location
#world/world
#character/npc
#character/person
#character/creature
#character/monster
#resource/item
#resource/treasure
#meta/index
#meta/moc
#meta/reference

## Voice & Mannerisms
- Speaking style
- Common phrases

## Daily Routine
- Morning activities
- Evening habits

## Possessions
- Personal items
- Valuable objects

## Combat Tactics
- Preferred strategies
- Special moves

## Secrets
- Hidden knowledge
- Personal mysteries
