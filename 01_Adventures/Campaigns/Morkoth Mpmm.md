---

title: Morkoth Mpmm
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'

--- # Morkoth Mpmm ---

## Description

Detailed description pending.
title: Morkoth Mpmm
aliases:
- Morkoth

type: monster
tags:
- ttrpg-cli/monster/environment/coastal
- both
- world/aquabyssos
- monster
- ttrpg-cli/monster/type/aberration
- ttrpg-cli/compendium/src/5e/mpmm
- ttrpg-cli/monster/size/large
- world/both
- research
- active
- ttrpg-cli/monster/cr/11
- status/in-progress

created: 2025-08-11
modified: '2025-08-14'
status: active
cssclasses: json5e-monster
obsidian-u-i-mode: preview
statblock: inline
statblock-link: '#^statblock'
updated: '2025-08-13T12:34:05.616982+00:00'
world: Both

--- > [!figure] Creature
![](04_Resources/Assets/Creatures/creature-creature-morkoth-mpmm-morkoth-mpmm.svg) # [[Morkoth Mpmm

*Source: Mordenkainen Presents: Monsters of the Multiverse p. 186, Volo's Guide to Monsters p. 177* Ancient and devious, morkoths are voracious collectors. Each one floats through the planes on a strange, mobile island, amassing the valuables, oddities, and castoffs of the multiverse in a massive, ever-growing collection. The first morkoths arose in the Astral Plane when the [conditions#Petrified|petrified]] body of a deity of greed and strife collided with a remt of celestial matter imbued with life-giving magic. The collision released a storm of chaotic energy and sent countless islands spinning away into the void. Within some of them, bits of the god's [[conditions#Petrified|petrified flesh came back to life as morkoths: tentacled monstrosities brimming with malice and greed. Morkoths are driven by greed and selfishness mixed with a yearning for conflict. They hoard vast stores of treasure, knowledge, and captives on their islands. Some of these prisoners are the descendants of people captured generations before; they might know of no other world outside their island. A morkoth may allow a visitor to bargain for something or someone it has claimed if that visitor offers the morkoth something it desires more. It shows no mercy, however, to those who break a deal or try to steal from it. A morkoth knows every person and object in its collection. A morkoth's island has the qualities of a dreamscape. It holds a jumble of objects and creatures the morkoth has collected, some of which date from forgotten times. An island might have natural-looking illumination, but most are shrouded in twilight, and on any of them, mists and shadows can appear without notice. The environment is warm and wet, a subtropical or tropical climate that keeps the morkoth and its "guests" comfortable. Each island glides on planar currents and is safe from most harmful external effects—one could float in the skies of Avernus in the Nine Hells without harm to it or its residents. A morkoth's island might be found anywhere from the bottom of the ocean to the void of the Astral Plane. Anything on or within a certain distance of a morkoth's isle is drawn with it in its journey through the planes. Thus, people from lost civilizations and creatures or objects from bygone ages might be found within a morkoth's dominion. Some islands travel a specific route, arriving at the same destinations regularly over a cycle of years. Others are tied to a particular place or group of locales, and still others move erratically through the cosmos. Occasionally, a morkoth learns to direct its island's movement. ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## A Morkoth's Lair A morkoth claims dominion over an entire island, and it also maintains a central sanctum on that isle. This lair is most often a twisted network of narrow tunnels that connect several underground chambers, although other structural forms might be incorporated. The morkoth dwells among the creatures and objects it prizes most in a spacious vault at the center of the warren, where the celestial fragments that make up the island's core are also located. Sections of the lair and its center might be kept dry to better protect and preserve collected objects and creatures, but most of the lair is underwater. A morkoth encountered in its lair has a challenge rating of 12 (8,400 XP).```statblock

"name": "Morkoth (MPMM)"
"size": "Large"
"type": "aberration"
"alignment": "Typically Chaotic Evil"
"ac": !!int "17"
"ac_class": "natural armor"
"hp": !!int "165"
"hit_dice": "`dice: 22d10` + 44"
"modifier": !!int "2"
"stats": - !!int "14" - !!int "20" - !!int "15" - !!int "13"
"speed": "25 ft., swim 50 ft."
"saves": - "dexterity": !!int "6" - "intelligence": !!int "9" - "wisdom": !!int "6"
"skillsaves": - "name": "[skills#Arcana|Arcana]]" "desc": "+9" - "name": "[[skills#History|History" - "name": "[skills#Perception|Perception]]" "desc": "+10" - "name": "[[skills#Stealth|Stealth" "desc": "+6"
"senses": "blindsight 30 ft., darkvision 120 ft., passive Perception 20"
"languages": "telepathy 120 ft."
"cr": "11"
"traits": - "desc": "The morkoth can breathe air and water." "name": "Amphibious"
"actions": - "desc": "The morkoth makes either two Bite attacks and one Tentacles attack or\ \ three Bite attacks." "name": "Multiattack" - "desc": "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 9 (`dice: 2d6`\ \ + 2) slashing damage plus 10 (`dice: 3d6`) psychic damage." "name": "Bite" - "desc": "Melee Weapon Attack: +6 to hit, reach 15 ft., one target. Hit: 15\ \ (`dice: 3d8` + 2) bludgeoning damage, and the target is [conditions#Grappled|grappled]]\ \ (escape **DC 14**) if it is a Large or smaller creature. Until this grapple ends,\ \ the target is [[conditions#Restrained|restrained and\ \ takes 15 (`dice: 3d8` + 2) bludgeoning damage at the start of each of its turns, and\ \ the morkoth can't use its tentacles on another target." "name": "Tentacles" - "desc": "The morkoth projects a 30-foot cone of magical energy. Each creature\ \ in that area must make a **DC 17** Wisdom saving throw. On a failed save, the\ \ creature is [conditions#Charmed|charmed]] by the morkoth\ \ for 1 minute. While [[conditions#Charmed|charmed in this\ \ way, the target tries to get as close to the morkoth as possible, using its\ \ actions to [actions#Dash|Dash]] until it is within 5 feet\ \ of the morkoth. A [[conditions#Charmed|charmed target\ \ can repeat the saving throw at the end of each of its turns and whenever it\ \ takes damage, ending the effect on itself on a success. If a creature's saving\ \ throw is successful or the effect ends for it, the creature has advantage\ \ on saving throws against the morkoth's Hypnosis for 24 hours." "name": "Hypnosis" - "desc": "The morkoth casts one of the following spells, requiring no material\ \ components and using Intelligence as the spellcasting ability (spell save\ \ **DC 17**):\n\n At will: [detect-magic-xphb (spells)]],\ \ [[mage-hand-xphb (spells)\n\n3/day each:\ \ [darkness-xphb (variant-rules)]], [[Dimension Door Xphb,\ \ [dispel-magic-xphb (spells)]], [[Lightning Bolt Xphb,\ \ [Sending Xphb]]" "name": "Spellcasting"
"reactions": - "desc": "If the morkoth makes a successful saving throw against a spell or a spell\ \ attack misses it, the morkoth can choose another creature (including the spellcaster)\ \ it can see within 120 feet of it. The spell targets the chosen creature instead\ \ of the morkoth. If the spell forced a saving throw, the chosen creature makes\ \ its own save. If the spell was an attack, the attack roll is rerolled against\ \ the chosen creature." "name": "Spell Reflection"
"source": - "MPMM" - "VGM"
"image": "/03_Mechanics/CLI/bestiary/aberration/token/morkoth-mpmm.webp"```^statblock ## Environment coastal, underwater ## Player-Facing Summary Morkoth mpmm is a undersea element of the setting, known for bioluminescent glow and pressure-glass. Its presence anchors ongoing storylines and offers clear player choices. ## Lore Details Legends speak of morkoth mpmm as a nexus where past and present converge. Locals describe subtle omens—shifts in currents, a dimming of lanternfish, or whispers on the wind—that herald change around morkoth mpmm. ## DM Notes Play up tactile detail: sounds, pressure/wind changes, and meaningful symbology. Offer two clear approaches (stealth vs. Parley) and one wildcard complication tied to a faction clock. Reward scouting and map use. ## Related *Links to related content will be added here.* ## Secret Connections *[Hidden from players]* Connected to The Veiled Alliance - Manipulate succession ## Related Notes - [[Similar Topic 1

- [Contrasting Approach]]
- [[Advanced Version
- [Historical Context]] ## 12_Research Specific Content Contextual improvement based on 12_Research ## 12_Research Specific Content Contextual improvement based on 12_Research ## References - [[morkoth-mpmm (aberration)

- [3 Bestiary]]
- [[3-bestiary (volos-guide-to-monsters)]]

## Notes

*Additional notes*
