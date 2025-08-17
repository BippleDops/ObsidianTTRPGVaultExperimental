---

title: Aboleth Xmm
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'

--- # Aboleth Xmm ---

## Description

Detailed description pending.
title: Aboleth Xmm
aliases:
- Aboleth

type: monster
tags:
- both
- ttrpg-cli/compendium/src/5e/xmm
- ttrpg-cli/monster/cr/10
- world/aquabyssos
- monster
- ttrpg-cli/monster/environment/underdark
- ttrpg-cli/monster/type/aberration
- research
- ttrpg-cli/monster/size/large
- world/both
- active
- status/in-progress

created: 2025-08-11
modified: '2025-08-14'
status: active
cssclasses: json5e-monster
obsidian-u-i-mode: preview
statblock: inline
statblock-link: '#^statblock'
updated: '2025-08-13T12:34:05.564434+00:00'
world: Both

--- > [!figure] Creature
![](04_Resources/Assets/Creatures/creature-creature-aboleth-xmm-aboleth-xmm.svg) # [[Aboleth Xmm]]

*Source: Monster Manual (2024) p. 12. Available in the SRD and the Free Rules (2024)* ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## Aboleth *Ageless Alien Mastermind* - **Habitat.** Underdark, Underwater - **Treasure.** Relics In aquatic abysses, aboleths dream of dead empires and orchestrate plots that unfold across ages. These elusive, amphibious immortals physically and mentally overwhelm their victims and transform creatures with a slimy, aberrant infection, reshaping other beings to serve them beneath the waves. Aboleths possess terrifying intellects and have alien mindsets. These creatures possess perfect memories of proto-worlds and incomprehensible dominions from the multiverse's earliest eons. Their secrets are innumerable and unfathomable. Aboleths lurk in places awash in primordial mysteries: the ruins of aquatic empires, hidden magical nexuses, or weak places between planes of existence. In these lairs, aboleths dream of epochs past, collect throngs of psychically dominated servants, consume the minds of unwitting victims, and prepare for their return to power. Aboleths' alien goals and methods are often mysterious to other creatures. Roll on or choose a result from the Aboleth Schemes table to inspire an aboleth's schemes. > [!quote] A quote from Evard > > The lies we call reason are fragile things, vulnerable and raw on the shores of eons. But in the dream-vaults of dread ancients roil seas of terrifying truth. Our age is an island, and the ebb of primordial tides avows the Stygian wave. **Aboleth Schemes**`dice: [](aboleth-xmm.md#^aboleth-schemes)`| dice: `dice: 1d6` | The Aboleth Seeks To... |

|-----------|-------------------------|
| 1 | Accomplish incomprehensible plans that lead it to act in seemingly random ways. |
| 2 | Learn more of the world by kidnapping people and consuming their minds. |
| 3 | Manipulate innocents into worshiping it as a god by using its telepathy from hiding. |
| 4 | Open a gate to the distant past or future, releasing an invasion from another time. |
| 5 | Rouse a dragon turtle, a kraken, or another sea monster to flood a coastal city. |
| 6 | Trick treasure hunters into recovering relics from its long-fallen empire. |

^aboleth-schemes ### Aboleth Lairs Aboleths usually dwell in submerged ruins and caverns. They keep air-filled spaces for their terrestrial servants and to hold treasures that would be damaged by water.```statblock

"name": "Aboleth (XMM)"
"size": "Large"
"type": "aberration"
"alignment": "Lawful Evil"
"ac": !!int "17"
"hp": !!int "150"
"hit_dice": "`dice: 20d10` + 40"
"modifier": !!int "7"
"stats": - !!int "21" - !!int "9" - !!int "15" - !!int "18"
"speed": "10 ft., swim 40 ft."
"saves": - "dexterity": !!int "3" - "constitution": !!int "6" - "intelligence": !!int "8" - "wisdom": !!int "6"
"skillsaves": - "name": "[[skills#History|History" "desc": "+12" - "name": "[skills#Perception|Perception]]" "desc": "+10"
"senses": "darkvision 120 ft., passive Perception 20"
"languages": "Deep Speech; telepathy 120 ft."
"cr": "10"
"traits": - "desc": "The aboleth can breathe air and water." "name": "Amphibious" - "desc": "If destroyed, the aboleth gains a new body in `dice: 5d10` days, reviving with\ \ all its [[hit-points-xphb (variant-rules) in\ \ the Far Realm or another location chosen by the DM." "name": "Eldritch Restoration" - "desc": "If the aboleth fails a saving throw, it can choose to succeed instead." "name": "Legendary Resistance (3/Day, or 4/Day in Lair)" - "desc": "While underwater, the aboleth is surrounded by mucus. Constitution Saving\ \ Throw: **DC 14**, each creature in a 5-foot [Area of Effect Xphb]]\ \ originating from the aboleth at the end of the aboleth's turn. Failure:\ \ The target is cursed. Until the curse ends, the target's skin becomes slimy,\ \ the target can breathe air and water, and it can't regain [[hit-points-xphb (variant-rules)\ \ unless it is underwater.\n\n While the cursed creature is outside a body of\ \ water, the creature takes 6 (d12) Acid damage at the end of every 10 minutes\ \ unless moisture is applied to its skin before those minutes have passed." "name": "Mucus Cloud" - "desc": "If a creature the aboleth can see communicates telepathically with the\ \ aboleth, the aboleth learns the creature's greatest desires." "name": "Probing Telepathy"
"actions": - "desc": "The aboleth makes two Tentacle attacks and uses either Consume Memories\ \ or Dominate Mind if available." "name": "Multiattack" - "desc": "Melee Attack Roll: +9, reach 15 ft. Hit: 12 (`dice: 2d6` + 5) Bludgeoning\ \ damage. If the target is a Large or smaller creature, it has the [conditions#Grappled|Grappled]]\ \ condition (escape **DC 14**) from one of four tentacles." "name": "Tentacle" - "desc": "Intelligence Saving Throw: **DC 16**, one creature within 30 feet that\ \ is [[conditions#Charmed|Charmed or [conditions#Grappled|Grappled]]\ \ by the aboleth. Failure: 10 (`dice: 3d6`) Psychic damage. Success: Half damage.\ \ Failure or Success: The aboleth gains the target's memories if the target\ \ is a Humanoid and is reduced to 0 [[hit-points-xphb (variant-rules)\ \ by this action." "name": "Consume Memories" - "desc": "Wisdom Saving Throw: **DC 16**, one creature the aboleth can see within\ \ 30 feet. Failure: The target has the [conditions#Charmed|Charmed]]\ \ condition until the aboleth dies or is on a different plane of existence from\ \ the target. While [[conditions#Charmed|Charmed, the target\ \ acts as an ally to the aboleth and is under its control while within 60 feet\ \ of it. In addition, the aboleth and the target can communicate telepathically\ \ with each other over any distance.\n\n The target repeats the save whenever\ \ it takes damage as well as after every 24 hours it spends at least 1 mile\ \ away from the aboleth, ending the effect on itself on a success." "name": "Dominate Mind (2/Day)"
"legendary_actions": - "desc": "The aboleth makes one Tentacle attack." "name": "Lash" - "desc": "If the aboleth has at least one creature [conditions#Charmed|Charmed]]\ \ or [[conditions#Grappled|Grappled, it uses Consume Memories\ \ and regains 5 (d10) [hit-points-xphb (variant-rules)]]." "name": "Psychic Drain"
"regional_effects": - "desc": "The region containing an aboleth's lair is warped by it, creating the\ \ following effects:" "name": "" - "desc": "- Foul Water. Water sources within 1 mile of the lair are supernaturally\ \ fouled. Creatures other than the aboleth and its allies that drink such water\ \ must succeed on a **DC 15** Constitution saving throw or have the [[conditions#Poisoned|Poisoned\ \ condition for 1 hour. \n- Psionic Projection. While in its lair, the\ \ aboleth can cast [Project Image Xphb]],\ \ requiring no spell components and using Intelligence as the spellcasting ability\ \ (spell save **DC 16**). When casting the spell this way, the spell's range is\ \ 1 mile, and the aboleth can use its telepathy as if it were in the illusion's\ \ space. " - "desc": "If the aboleth dies or moves its lair elsewhere, these effects end immediately."
"source": - "XMM"
"image": "/03_Mechanics/CLI/bestiary/aberration/token/aboleth-xmm.webp"```^statblock ## Environment underdark, underwater ## Player-Facing Summary Aboleth xmm is a undersea element of the setting, known for bioluminescent glow and pressure-glass. Its presence anchors ongoing storylines and offers clear player choices. ## Lore Details Legends speak of aboleth xmm as a nexus where past and present converge. Locals describe subtle omens—shifts in currents, a dimming of lanternfish, or whispers on the wind—that herald change around aboleth xmm. ## DM Notes Play up tactile detail: sounds, pressure/wind changes, and meaningful symbology. Offer two clear approaches (stealth vs. Parley) and one wildcard complication tied to a faction clock. Reward scouting and map use. ## Related *Links to related content will be added here.* ## Plot Hooks - A map reveals a conspiracy about the government

- A prisoner has gone missing and chaos spreads
- Someone is searching for a witness for love
- A noble needs help investigating before dawn ## 12_Research Specific Content Contextual improvement based on 12_Research ## References - [[aboleth-xmm (aberration)

- [Monsters by Habitat Underdark Monsters Xmm]]
- [[Monsters by Habitat Underwater Monsters Xmm
- [Underdark Encounters Levels 1116 Xge]]
- [[Underdark Encounters Levels 1720 Xge
- [monsters-by-habitat-underdark-monsters-xmm (tables)]]
- [[monsters-by-habitat-underwater-monsters-xmm (tables)
- [underdark-encounters-levels-1116-xge (tables)]]
- [[underdark-encounters-levels-1720-xge (tables)]]

## Notes

*Additional notes*
