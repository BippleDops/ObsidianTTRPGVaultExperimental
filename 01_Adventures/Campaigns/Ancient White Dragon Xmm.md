---

title: Ancient White Dragon Xmm
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'

--- # Ancient White Dragon Xmm ---

## Description

Detailed description pending.
title: Ancient White Dragon Xmm
aliases:
- Ancient White Dragon

type: monster
tags:
- both
- ttrpg-cli/compendium/src/5e/xmm
- ttrpg-cli/monster/size/gargantuan
- monster
- ttrpg-cli/monster/type/dragon/chromatic
- research
- world/both
- active
- campaign/arc
- status/in-progress
- ttrpg-cli/monster/cr/20

created: modified: '2025-08-14'
status: active
cssclasses: json5e-monster
obsidian-u-i-mode: preview
statblock: inline
statblock-link: '#^statblock'
updated: '2025-08-13T12:34:05.989233+00:00'
world: Both

--- > [!figure] Creature
![](04_Resources/Assets/Creatures/creature-creature-ancient-white-dragon-xmm-ancient-white-dragon-xmm.svg) # [[ancient-white-dragon-xmm

*Source: Monster Manual (2024) p. 330. Available in the SRD and the Free Rules (2024)* Like arctic storms, ancient white dragons threaten icy realms. They emerge from their frozen lairs to indulge their hungers for food or treasure, menacing other creatures with lethal cold. While they might ignore animals or small groups of polar wanderers, these dragons are quick to challenge other dragons and creatures wielding powerful magic, hoping to add their foes' skulls and magic items to their own hoards. ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## White Dragons *Dragons of Cold and Cruelty* - **Habitat.** Arctic - **Treasure.** Arcana Among the most primal chromatic dragons, white dragons prioritize survival over all. Life is harsh and uncertain in the arctic expanses, glacial heights, and frozen seas where these dragons dwell. White dragons fiercely protect their territories, scouring the frigid regions for food and evidence of trespassers. Most white dragons ignore the plots of smaller creatures and other dragons, concerning themselves only with their own survival. White dragons create lairs to defend themselves from other deadly arctic creatures and from dangerous natural conditions. Within these shelters, white dragons hoard testaments to their superiority, such as monstrous skulls, the gear of defeated rivals, and curiosities that capture their interest. To protect such treasure, white dragons coax ice to form over their hoards or sink their wealth in frigid pools. For white dragons, each piece of treasure embodies a victory—the details of which inflate as these dragons age. ### White Dragon Lairs White dragons brood in bitterly cold lairs clawed from stone and ice.```statblock

"name": "Ancient White Dragon (XMM)"
"size": "Gargantuan"
"type": "dragon"
"subtype": "chromatic"
"alignment": "Chaotic Evil"
"ac": !!int "20"
"hp": !!int "333"
"hit_dice": "`dice: 18d20` + 144"
"modifier": !!int "12"
"stats": - !!int "26" - !!int "10" - !!int "13" - !!int "18"
"speed": "40 ft., burrow 40 ft., fly 80 ft., swim 40 ft."
"saves": - "dexterity": !!int "6" - "wisdom": !!int "7"
"skillsaves": - "name": "[skills#Perception|Perception]]" "desc": "+13" - "name": "[[skills#Stealth|Stealth" "desc": "+6"
"damage_immunities": "cold"
"senses": "blindsight 60 ft., darkvision 120 ft., passive Perception 23"
"languages": "Common, Draconic"
"cr": "20"
"traits": - "desc": "The dragon can move across and climb icy surfaces without needing to\ \ make an ability check. Additionally, [Difficult Terrain Xphb]]\ \ composed of ice or snow doesn't cost it extra movement." "name": "Ice Walk" - "desc": "If the dragon fails a saving throw, it can choose to succeed instead." "name": "Legendary Resistance (4/Day, or 5/Day in Lair)"
"actions": - "desc": "The dragon makes three Rend attacks." "name": "Multiattack" - "desc": "Melee Attack Roll: +14, reach 15 ft. Hit: 17 (`dice: 2d8` + 8) Slashing damage\ \ plus 7 (`dice: 2d6`) Cold damage." "name": "Rend" - "desc": "Constitution Saving Throw: **DC 22**, each creature in a 90-foot [[Area of Effect Xphb.\ \ Failure: 63 (`dice: 14d8`) Cold damage. Success: Half damage." "name": "Cold Breath (Recharge 5-6)"
"legendary_actions": - "desc": "Constitution Saving Throw: **DC 20**, each creature in a 30-foot-radius\ \ [Area of Effect Xphb]] centered\ \ on a point the dragon can see within 120 feet. Failure: 14 (`dice: 4d6`) Cold damage,\ \ and the target's [[Fly Speed Xphb is\ \ 0 until the end of the target's next turn. Failure or Success: The dragon\ \ can't take this action again until the start of its next turn." "name": "Freezing Burst" - "desc": "The dragon moves up to half its [Fly Speed Xphb]],\ \ and it makes one Rend attack." "name": "Pounce" - "desc": "The dragon casts [[Fear Xphb, requiring\ \ no Material components and using Charisma as the spellcasting ability (spell\ \ save **DC 18**). The dragon can't take this action again until the start of its\ \ next turn.\n" "name": "Frightful Presence"
"regional_effects": - "desc": "The region containing an adult or ancient white dragon's lair is affected\ \ by its presence, creating the following effects:" "name": "" - "desc": "- Frigid Cold. The area within 1 mile of the lair is an area of [extreme-cold-xdmg (traps-hazards)]] \ cold]]. Any water in that\ \ area is [[Frigid Water Xdmg.\ \ See the \"Dungeon Master's Guide\" for rules on extreme cold and frigid water.\ \ \n- Glacial Gloom. The area within 1 mile of the lair is [lightly-obscured-xphb (variant-rules)]]\ \ by chilly fog. Whenever a creature other than the dragon or one of its allies\ \ finishes a [[long-rest-xphb in\ \ that area, that creature must succeed on a **DC 15** Constitution saving throw\ \ or have its [Fly Speed Xphb]] reduced\ \ by 10 feet for 1 hour. " - "desc": "If the dragon dies or moves its lair elsewhere, these effects end immediately."
"source": - "XMM"
"image": "/03_Mechanics/CLI/bestiary/dragon/token/ancient-white-dragon-xmm.webp"```^statblock ## Environment arctic ## Player-Facing Summary Ancient white dragon xmm is a undersea element of the setting, known for bioluminescent glow and pressure-glass. Its presence anchors ongoing storylines and offers clear player choices. ## Lore Details Legends speak of ancient white dragon xmm as a nexus where past and present converge. Locals describe subtle omens—shifts in currents, a dimming of lanternfish, or whispers on the wind—that herald change around ancient white dragon xmm. ## DM Notes Play up tactile detail: sounds, pressure/wind changes, and meaningful symbology. Offer two clear approaches (stealth vs. Parley) and one wildcard complication tied to a faction clock. Reward scouting and map use. ## Related *Links to related content will be added here.*

## Notes

*Additional notes*
