---

title: Plugin_Integration_and_Tools
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'
aliases: ["Plugin Integration and Tools"]
status: active
priority: normal
category: 12 Research
subcategory: D&D Sourcebooks
related: []
cssclass: standard
publish: false

---

 # Plugin_Integration_and_Tools ---

## Description

Detailed description pending.
title: Plugin Integration and Tools
type: Reference
tags:
- plugin-integration/seven-shards
- obsidian-tools
- initiative-tracker
- meta-bind
- world/both
- status/active
- templater
- active
- research
- dataview
- dice-roller

created: '2025-08-13'
modified: '2025-08-14'
status: active
updated: '2025-08-13T16:45:00.000000'
world: Both

--- # Seven Shards Campaign: Plugin Integration & Tools

*Complete Obsidian Plugin Integration for Enhanced Campaign Management* > [!info] Required Obsidian Plugins

> This campaign is designed to work with the following Obsidian plugins:
> - **Dataview**: Dynamic content queries and data visualization
> - **Meta-bind**: Interactive buttons and form elements
> - **Dice Roller**: Integrated dice mechanics and random tables
> - **Initiative Tracker**: Combat and encounter management
> - **Fantasy Calendar**: Timeline and event tracking
> - **Templater**: Dynamic content generation and automation
> - **Obsidian 5e Statblocks**: Monster and NPC stat management
> - **Admonitions**: Styled callout boxes for important information ### Campaign Dashboard Query Create a comprehensive campaign overview that updates automatically:```dataview

TABLE status as "Session Status", world as "World", key-npcs as "Key NPCs", major-events as "Major Events"

FROM "01_Adventures/Seven_Shards_Campaign"

WHERE contains(tags, "session")

SORT file.name ASC```### NPC Relationship Tracker Monitor relationship developments throughout the campaign: relationship-value as "Relationship", last-interaction as "Last Seen", corruption-level as "Corruption", faction as "Faction"

FROM "02_Worldbuilding"

WHERE contains(tags, "npc") AND contains(tags, "seven-shards")

SORT relationship-value DESC ### Shard Corruption Monitor Track corruption levels across the party and NPCs: character as "Character", corruption-source as "Source", corruption-level as "Level", treatment-status as "Treatment"

FROM "Seven_Shards_Campaign"

WHERE contains(tags, "corruption")

SORT corruption-level DESC ### Treasure and Rewards Overview Track campaign rewards and their distribution: item-type as "Type", rarity as "Rarity", current-owner as "Owner", session-acquired as "Session"

WHERE contains(tags, "treasure") OR contains(tags, "magic-item")

SORT rarity DESC, session-acquired ASC ### Timeline Progress Tracker Monitor campaign pacing and deadlines: date as "Date", event-type as "Type", deadline-pressure as "Urgency", consequences as "Stakes"

WHERE contains(tags, "timeline") AND date >= current-date

SORT date ASC

LIMIT 5 ### Location Discovery Status Track which locations have been explored: shard-type as "Shard", discovery-status as "Status", exploration-level as "Explored", remaining-secrets as "Secrets"

WHERE contains(tags, "location") AND contains(tags, "shard-site")

SORT discovery-status ASC ### Campaign Status Dashboard Create an interactive control panel for the GM:```meta-bind

INPUT[progress Bar(min Value(0), max Value(100)):campaign-progress]

LABEL[Campaign Progress] INPUT[slider(min Value(1), max Value(10):threat-level]

LABEL[Current Threat Level] INPUT[slider(min Value(0), max Value(7):shards-discovered]

LABEL[Shards Discovered] INPUT[progress Bar(min Value(0), max Value(100):reality-stability]

LABEL[Reality Stability] ### Character Corruption Trackers Individual corruption monitors for each party member: INPUT[progress Bar(min Value(0), max Value(10):pc1-corruption]

LABEL[Character 1 Corruption Level] INPUT[select(option(none), option(consciousness), option(crystal), option(storm), option(shadow), option(void), option(life), option(unity)):pc1-corruption-source]

LABEL[Character 1 Corruption Source] ### Quick Action Buttons Essential campaign management tools:```meta-bind-button

label: Roll Random Encounter
id: random-encounter
action: type: command command: dice-roller
args: ["`dice: `dice: 1d20``"] label: Generate Shard Resoce
id: shard-resoce args: ["`dice: `dice: 7d20``"] label: Check Environmental Effects
id: environmental-check
args: ["`dice: `dice: 1d12``"] label: Advance Timeline 1 Week
id: timeline-advance type: templater command: tp-obsidian://advance-timeline ### NPC Mood and Status Trackers Dynamic NPC state management: INPUT[slider(min Value(-10), max Value(10):seraphina-mood]

LABEL[Queen Seraphina Mood] INPUT[progress Bar(min Value(0), max Value(100):seraphina-corruption]

LABEL[Queen Seraphina Corruption] INPUT[select(option(ally), option(neutral), option(hostile), option(unknown)):aurelius-status]

LABEL[Lord Aurelius Relationship] ### Session Preparation Tools Interactive session setup and management: INPUT[text]:session-date

LABEL[Session Date] INPUT[multi Select(option(combat), option(social), option(exploration), option(investigation)):session-focus]

LABEL[Session Focus Areas] INPUT[number]:expected-duration

LABEL[Expected Session Duration (hours)] ### Core Campaign Tables Essential random generation tools for the Seven Shards campaign: #### Shard Activity Check```dice-roller

dice: `dice: `dice: 7d20``

| Shard | Activity Level |
|-------|---------------|
| Consciousness | {1} |
| Crystal | {2} |
| Storm | {3} |
| Shadow | {4} |
| Void | {5} |
| Life | {6} |
| Unity | {7} | #### Random Encounter Generation

dice: `dice: `dice: 1d20``

| d20 | Encounter Type |
|-----|---------------|
| 1-3 | Shard-corrupted creature |
| 4-6 | Faction agents investigating |
| 7-9 | Reality distortion event |
| 10-12 | Memory-affected NPC |
| 13-15 | Political complication |
| 16-18 | Environmental hazard |
| 19-20 | Unexpected ally or opportunity | #### Corruption Progression

dice: `dice: `dice: 1d20``+0

Corruption Resistance Check

DC varies by shard exposure level #### Weather and Environmental Effects

dice: `dice: `dice: 2d12``

| `dice: `dice: 2d12`` | Effect |
|------|--------|
| 2-3 | Extreme weather from Storm Shard |
| 4-5 | Memory fog from Consciousness Shard |
| 6-7 | Crystal growth acceleration |
| 8-9 | Shadow manipulation increased |
| 10-11 | Reality fluctuations from Void Shard |
| 12-13 | Life energy surge |
| 14-15 | Dimensional barriers weakening |
| 16+ | Multiple shard effects combine | #### Session 1: Festival Complications

dice: `dice: `dice: 1d10``

| d10 | Festival Complication |
|-----|---------------------|
| 1-2 | Pickpockets target the party |
| 3-4 | Religious ceremony goes wrong |
| 5-6 | Merchant dispute blocks progress |
| 7-8 | Lost child needs help |
| 9-10 | Sudden weather change | #### Session 2: Mining Hazards

dice: `dice: `dice: 1d8``

| d8 | Mining Hazard |
|----|--------------|
| 1-2 | Cave-in blocks passage |
| 3-4 | Crystal dust causes illness |
| 5-6 | Equipment malfunction |
| 7-8 | Corrupted miner attacks | #### Session 9: Reality Distortions

dice: `dice: `dice: 1d12``

| d12 | Reality Distortion |
|-----|-------------------|
| 1 | Gravity reverses for 1 minute |
| 2 | Time moves backward 30 seconds |
| 3 | Everyone swaps positions |
| 4 | Magic items activate randomly |
| 5 | Languages become incomprehensible |
| 6 | Physical laws from other world apply |
| 7 | Memories become shared |
| 8 | Emotions become visible |
| 9 | Past and future overlap |
| 10 | Parallel selves appear |
| 11 | Thoughts become audible |
| 12 | Reality splits into multiple versions | #### NPC Disposition

dice: `dice: `dice: 2d6``+6

NPC Charisma for social encounters
(8-10: Hostile, 11-13: Neutral, 14-16: Friendly, 17+: Helpful) #### Environmental Challenge DCs

dice: `dice: `dice: 1d6``+10

Base DC for environmental challenges

Modified by character level and circumstances ### Standard Combat Template```initiative-tracker

- name: Primary Enemy hp: [Variable by CR] ac: [Variable by type] initiative: [High] tags: ["boss", "shard-related"]
- name: Lieutet (2) hp: [Medium HP] ac: [Medium AC] initiative: [Medium] tags: ["minion", "coordinated"]
- name: Environmental Hazard hp: --- ac: --- initiative: 20 tags: ["hazard", "ongoing"] ### Social Encounter Template

- name: Primary Speaker hp: 3 (Social Arguments) ac: [Persuasion DC] initiative: [Charisma Modifier] tags: ["social", "primary"]
- name: Supporting Voice hp: 2 (Social Arguments) tags: ["social", "support"]
- name: Opposition ac: [Deception DC] tags: ["social", "opposition"] ### Exploration Challenge Template

- name: Primary Obstacle hp: [Challenge Progress] ac: [Challenge DC] initiative: [Priority Level] tags: ["exploration", "skill-challenge"]
- name: Time Pressure hp: [Rounds Remaining] initiative: 10 tags: ["timer", "pressure"]
- name: Complications hp: [Failure Threshold] initiative: 5 tags: ["complications", "consequences"] ### Boss Fight Phases Template

- name: Boss Phase 1 hp: [33% of total] ac: [Base AC] tags: ["boss", "phase-1"]
- name: Boss Phase 2 ac: [Base AC + 2] initiative: [Higher] tags: ["boss", "phase-2"]
- name: Boss Phase 3 ac: [Base AC + 4] initiative: [Highest] tags: ["boss", "phase-3", "desperate"] ### Session Preparation Template```templater

 ### NPC Interaction Template const npc Name = await tp.system.prompt("NPC Name:");

const relationship = await tp.system.prompt("Current Relationship Level (-10 to +10):");
const corruption Level = await tp.system.prompt("Corruption Level (0-10):"); const template =`## ${npc Name} Interaction **Relationship**: ${relationship}/10

**Corruption Level**: ${corruption Level}/10
**Last Interaction**: ### Current Status

[NPC's current situation and concerns] ### Goals and Motivations

[What the NPC wants and why] ### Interaction Notes

[How the conversation goes] ### Relationship Changes

[Any changes in relationship or corruption] ### Encounter Generation Template const encounter Type = await tp.system.suggester(["Combat", "Social", "Exploration", "Environmental"], ["combat", "social", "exploration", "environmental"], "Encounter Type:" const difficulty = await tp.system.suggester(["Easy", "Medium", "Hard", "Deadly"], ["easy", "medium", "hard", "deadly"], "Encounter Difficulty:" const shard Influence = await tp.system.suggester(["None", "Consciousness", "Crystal", "Storm", "Shadow", "Void", "Life", "Unity"], ["none", "consciousness", "crystal", "storm", "shadow", "void", "life", "unity"], "Shard Influence:" ## ${encounter Type} Encounter (${difficulty}) **Shard Influence**: ${shard Influence}

**Created**: ### Setup

[Encounter description and setup] ### Mechanics

[Specific rules and challenges] ### Resolution

[Possible outcomes and consequences] ### Shard Effects

[How shard influence manifests] #### Shard Warnings

> [!danger] Shard Corruption Warning

> Prolonged exposure to shard energy requires Constitution saves or risk permanent corruption effects. #### Reality Distortions

> [!warning] Reality Distortion Active

> Normal physical laws may not apply in this area. Proceed with caution. #### Time Pressure

> [!clock] Timeline Pressure

> This decision must be made before the next shard resoce pulse in 3 days. #### Secret Information

> [!secret] GM Only Information

> This information is for the GM only and should not be shared with players until revealed through gameplay. #### Player Handouts

> [!note] Player Handout

> This information can be shared directly with players. #### Combat Tactics

> [!battle] Tactical Information

> Optimal combat strategies and environmental considerations for this encounter. #### Roleplay Guidance

> [!actor] Roleplay Notes

> NPC personality traits, speech patterns, and motivation guidelines. ### Location Descriptions > [!location] Shard Location Template

> **Name**: [Location Name]

> **Shard**: [Which shard is here]
> **Threat Level**: [Environmental danger rating]
> **Special Features**: [Unique properties and hazards] ### NPC Quick Reference > [!person] NPC Quick Reference

> **Name**: [NPC Name]

> **Role**: [Position/Function]
> **Relationship**: [Current standing with party]
> **Corruption**: [Shard influence level]
> **Key Info**: [Most important details for quick reference] ### Campaign Calendar Setup```fantasy-calendar

calendar-id: seven-shards-campaign
name: "Seven Shards Timeline"
description: "Complete campaign timeline with events and milestones"
date-format: "YYYY-MM-DD" ### Recurring Events recurring-event: name: "Shard Resoce Pulse" frequency: "every-28-days" category: "supernatural" effects: "All shards pulse simultaneously, reality distortions increase" name: "Trade Council Meeting" frequency: "weekly" category: "faction" effects: "Economic decisions affecting both worlds" ### Comprehensive Encounter Setup 1. **Dataview**: Query relevant NPCs and locations

2. **Meta-bind**: Set encounter parameters (difficulty, focus)
3. **Dice Roller**: Generate random complications
4. **Initiative Tracker**: Set up combat order
5. **Templater**: Generate encounter notes automatically
6. **Fantasy Calendar**: Mark encounter date and consequences ### Dynamic Story Tracking 1. **Dataview**: Monitor relationship changes across sessions

2. **Meta-bind**: Update relationship sliders in real-time
3. **Fantasy Calendar**: Track when relationships changed
4. **Templater**: Generate relationship summary reports ### Automated Session Prep 1. **Fantasy Calendar**: Check upcoming deadlines and events

2. **Dataview**: Review session prerequisites and NPC states
3. **Meta-bind**: Set session parameters and difficulty
4. **Templater**: Generate session outline with current information
5. **Dice Roller**: Pre-roll random encounters and complications ### Obsidian Mobile Compatibility **Fully Compatible**:

- Dataview queries (read-only)
- Basic Meta-bind elements
- Fantasy Calendar viewing
- Admonitions display **Limited Functionality**:
- Complex Meta-bind interactions
- Templater automation
- Dice Roller integration **Workarounds for Mobile**:
- Pre-generate random tables as static content
- Use simple markdown tables for mobile reference
- Sync changes back to desktop for full functionality ### Sync Setup Recommendations 1. Use Obsidian Sync or reliable cloud storage

2. Test plugin functionality across devices
3. Keep backup copies of critical campaign data
4. Use mobile for reference, desktop for management --- ## Setup Instructions for New GMs 1. **Install Required Plugins**: Follow installation guides for each plugin

2. **Configure Settings**: Set up plugin preferences for optimal performance 3. **Test Integration**: Verify all interactive elements work correctly
4. **Customize Templates**: Adapt templates to your GMing style
5. **Practice Usage**: Familiarize yourself with all tools before first session
6. **Create Backups**: Establish backup procedures for campaign data ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## 12_Research Specific Content Contextual improvement based on 12_Research ## 12_Research Specific Content Contextual improvement based on 12_Research

#mechanics/combat
#mechanics/rules
#mechanics/mechanics
#mechanics/system
#mechanics/dice
#story/story
#story/lore
#world/location
#world/world
#world/setting
#character/npc
#character/character
#character/person
#character/creature
#character/monster
#gameplay/session
#gameplay/encounter
#gameplay/adventure
#resource/item
#resource/equipment
#resource/treasure
#meta/reference