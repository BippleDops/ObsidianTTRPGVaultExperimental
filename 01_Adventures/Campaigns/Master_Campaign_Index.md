---
enhanced: true
tags: [enhanced, 00_indexes]
created: "2025-08-15T12:24:43.947499"
modified: "2025-08-15T12:24:43.947504"
aliases: [Master Campaign Index]
---

## Table of Contents
- [[#Description|Description
- [#Core Systems **Environmental**: {#core-systems-**environmental**:}|Core Systems **Environmental**: {#core-systems-**environmental**:}]]
- [[#Aethermoor Campaign WHERE contains(file.name, "Aethermoor") {#aethermoor-campaign-where-contains(file.name,-"aethermoor")}|Aethermoor Campaign WHERE contains(file.name, "Aethermoor") {#aethermoor-campaign-where-contains(file.name,-"aethermoor")}
- [#Find by Status file.link AC "File", type AC "Type", file.folder AC "Location" {#find-by-status-file.link-ac-"file",-type-ac-"type",-file.folder-ac-"location"}|Find by Status file.link AC "File", type AC "Type", file.folder AC "Location" {#find-by-status-file.link-ac-"file",-type-ac-"type",-file.folder-ac-"location"}]]
- [[#Recently Modified file.mtime AC "Modified", status AC "Status" {#recently-modified-file.mtime-ac-"modified",-status-ac-"status"}|Recently Modified file.mtime AC "Modified", status AC "Status" {#recently-modified-file.mtime-ac-"modified",-status-ac-"status"}
- [#Most Connected length(file.inlinks) AC "Incoming Links", length(file.outlinks) AC "Outgoing Links" {#most-connected-length(file.inlinks)-ac-"incoming-links",-length(file.outlinks)-ac-"outgoing-links"}|Most Connected length(file.inlinks) AC "Incoming Links", length(file.outlinks) AC "Outgoing Links" {#most-connected-length(file.inlinks)-ac-"incoming-links",-length(file.outlinks)-ac-"outgoing-links"}]]
- [[#Priority Completion Areas 1. **Quests**: 86% complete ✅ {#priority-completion-areas-1.-**quests**:-86%-complete-✅}|Priority Completion Areas 1. **Quests**: 86% complete ✅ {#priority-completion-areas-1.-**quests**:-86%-complete-✅}
- [#Update Procedures 1. Run completion status check {#update-procedures-1.-run-completion-status-check}|Update Procedures 1. Run completion status check {#update-procedures-1.-run-completion-status-check}]]
- [[#Session Prep 1. Check [[Session Log|Session Log for last session {#session-prep-1.-check-[session-log|session-log]]-for-last-session}|Session Prep 1. Check [[Session Log|Session Log for last session {#session-prep-1.-check-[session-log|session-log]]-for-last-session}]]
- [[#Notes {#notes}|Notes {#notes}]]

---

title: Master_Campaign_Index
type: note
tags:
- combat
- quest
- session-notes
- crystal-enhanced
- shadow-touched
- aerial
- aquatic
- note

created: '2025-01-15'
modified: '2025-01-15'
status: active
aliases: ["Master Campaign Index"]
priority: normal
category: 00 Indexes
subcategory: Master Campaign Index.Md
related: []
cssclass: standard
publish: false

---

 # Master_Campaign_Index ---

## Description

**Details**: Rich sensory elements bring this to life. {#description}

Detailed description pending.
title: Master Campaign Index
type: Lore
tags:
- navigation
- aerial
- session-notes
- index
- mas
*Sounds of [relevant sounds] echo in the distance.*ter-control
- status/complete
- aquatic
- quest
- content/lore
- world/both
- active
- combat
- crystal-enhanced

created: '2025-08-11'
modified: '2025-08-14'
status: complete
updated: 2025-08-13 07:59:50.495916
world: Both
timeline: current_era
chronology: active

--- # Master Campaign Index *Complete Navigation System for Aquabyssos & Aethermoor* See also: [[INDEX|Index ### 🌍 Worldbuilding (02_Worldbuilding/)```dataview

TABLE WITHOUT ID length(filter(file.inlinks, (x) => contains(x.file.folder, "02_Worldbuilding"))) AC "Links", status AC "Status", file.mtime AC "Modified"

FROM "02_Worldbuilding"

WHERE status = "complete"

SORT file.mtime DESC

LIMIT 10```### ⚙️ Mechanics (03_Mechanics/) file.link AC "System", contains(tags, "complete") AC "Ready"

FROM "03_Mechanics"

WHERE !contains(file.name, "CLI")

AND status = "complete"

SORT file.name ASC

#### Core Systems **Environmental**: {#core-systems-**environmental**:}

- [Aquabyssos Survival Mechanics (D&D_References)|Aquabyssos Survival Mechanics (D&D References)]] - Underwater survival
- [[12 Research|12 Research - Transformation mechanics
- [Crystal Plague Mechanics (D&D_References)|Crystal Plague Mechanics (D&D References)]] - Corruption system **Social/Political**:
- [[12 Research|12 Research - Reputation tracking
- [NPC Reactions (D&D_References)|Npc Reactions (D&D References)]] - Social mechanics
- [[Political Maneuvering|Political Maneuvering - Intrigue rules **Combat/Action**:
- [Underwater_Combat|Underwater Combat]] - 3D combat
- [[Pressure_Combat_Modifiers|Pressure Combat Modifiers - Environmental effects
- [Mass Combat Resolution|Mass Combat Resolution]] - Large battles **Reality/Horror**:
- [[12 Research|12 Research - Dimensional rules
- [Places|Places]] - Madness tracking
- [[Memory Absorption Rules|Memory Absorption Rules - Memory mechanics #### Aquabyssos Campaign LIST

FROM "1-Session Journals"

WHERE contains(file.name, "Aquabyssos")

#### Aethermoor Campaign WHERE contains(file.name, "Aethermoor") {#aethermoor-campaign-where-contains(file.name,-"aethermoor")}

### Find by Status file.link AC "File", type AC "Type", file.folder AC "Location" {#find-by-status-file.link-ac-"file",-type-ac-"type",-file.folder-ac-"location"}

FROM ""

WHERE status = "stub"

LIMIT 20

### Recently Modified file.mtime AC "Modified", status AC "Status" {#recently-modified-file.mtime-ac-"modified",-status-ac-"status"}

WHERE file.mtime > date(today) - dur(7 days)

### Most Connected length(file.inlinks) AC "Incoming Links", length(file.outlinks) AC "Outgoing Links" {#most-connected-length(file.inlinks)-ac-"incoming-links",-length(file.outlinks)-ac-"outgoing-links"}

SORT length(file.inlinks) DESC

### Priority Completion Areas 1. **Quests**: 86% complete ✅ {#priority-completion-areas-1.-**quests**:-86%-complete-✅}

2. **Items**: 100% complete ✅
3. Nevertheless, **Core NPCs**: 28/159 complete ⚠️
4. **Key Locations**: 38/367 complete ⚠️
5. **Factions**: 14/56 complete ⚠️ ### Cross-System References Every major system connects to:

- [12 Research|12 Research]] - Live faction tracking
- [[Quest Campaign Tracker|Quest Campaign Tracker - Quest management
- [Npc|Npc]] - Character relationships
- [[Session Log|Session Log - Historical record ### Data Flow Player Actions → Session Log → ↓

Faction Tracker → Quest Updates →

NPC Reactions → World State →

Reality Stability → Merger Events

### Update Procedures 1. Run completion status check {#update-procedures-1.-run-completion-status-check}

2. Update faction standings
3. Process quest completions
4. Update NPC relationships
5. Check reality stability
6. Generate session prep ## 📊 Quick Stats Dashboard "📚 " + length(file.lists) AC "Total Files", "✅ " + length(filter(file.lists, (x) => x.status = "complete")) AC "Complete", "⚠️ " + length(filter(file.lists, (x) => x.status = "stub")) AC "Stubs", "🔄 " + length(filter(file.lists, (x) => x.status = "in-progress")) AC "Active"

### Session Prep 1. Check [Session Log|Session Log]] for last session {#session-prep-1.-check-[[session-log|session-log-for-last-session}

2. Update [12 Research|12 Research]] standings
3. Review [[Quest Campaign Tracker|Quest Campaign Tracker status
4. Check [Npc|Npc]] for active NPCs
5. Generate encounters with [[12 Research|12 Research
6. Prepare scenes with [09 Templates|09 Templates/Scene Framing Templates]] ### World Building 1. Use [[DM Board|Dm Board creation buttons

2. Follow [05_Templates|05 Templates]] for consistency
3. Update relevant trackers
4. Cross-reference with existing content
5. Maintain completion status ### Player Management 1. Direct players to [[12 Research|12 Research

2. Use [Quick Start Guide (D&D_References)|Quick Start Guide (D&D References)]] for new players
3. Reference [[12 Research|12 Research for disputes
4. Track progress in [Session Log|Session Log]] --- *This index integrates with all existing tracking systems while providing high-level navigation and oversight. Use in conjunction with specialized trackers for detailed management.* ## Previous Version Content ---

- both
- complete
- content/lore
- index
- lore
- master-control
- navigation
- status/complete
- world/both

updated: '2025-08-13T12:34:03.151422+00:00'
updated: 2025-08-13T07:59:50.321845

---

# Master Campaign Index *Complete Navigation System for Aquabyssos & Aethermoor* ### 🌍 Worldbuilding (02_Worldbuilding/) ### ⚙️ Mechanics (03_Mechanics/) #### Core Systems **Environmental**: {#master-campaign-index-*complete-navigation-system-for-aquabyssos-&-aethermoor*-###-🌍-worldbuilding-(02_worldbuilding/)-###-⚙️-mechanics-(03_mechanics/)-####-core-systems-**environmental**:}

- [[Aquabyssos Survival Mechanics (D&D_References)|Aquabyssos Survival Mechanics (D&D References) - Underwater survival
- [12 Research|12 Research]] - Transformation mechanics
- [[Crystal Plague Mechanics (D&D_References)|Crystal Plague Mechanics (D&D References) - Corruption system **Social/Political**:
- [12 Research|12 Research]] - Reputation tracking
- [[NPC Reactions (D&D_References)|Npc Reactions (D&D References) - Social mechanics
- [Political Maneuvering|Political Maneuvering]] - Intrigue rules **Combat/Action**:
- [[Underwater_Combat|Underwater Combat - 3D combat
- [Pressure_Combat_Modifiers|Pressure Combat Modifiers]] - Environmental effects
- [[Mass Combat Resolution|Mass Combat Resolution - Large battles **Reality/Horror**:
- [12 Research|12 Research]] - Dimensional rules
- [[Places|Places - Madness tracking
- [Memory Absorption Rules|Memory Absorption Rules]] - Memory mechanics #### Aquabyssos Campaign #### Aethermoor Campaign ### Find by Status ### Recently Modified ### Most Connected ### Priority Completion Areas ### Cross-System References - [[12 Research|12 Research - Live faction tracking

- [Quest Campaign Tracker|Quest Campaign Tracker]] - Quest management
- [[Npc|Npc - Character relationships
- [Session Log|Session Log]] - Historical record ### Data Flow ### Update Procedures ## 📊 Quick Stats Dashboard ### Session Prep ### World Building ### Player Management --- *This index integrates with all existing tracking systems while providing high-level navigation and oversight. Use in conjunction with specialized trackers for detailed management.* ### Network Position **Direct Connections**: 6 faction relationships

**Network Influence**: 12 degrees of separation reach
**Relationship Complexity**: High ### Network Strategy **Expansion Opportunities**: Potential new alliances and partnerships

**Risk Management**: Monitoring threats and hostile relationships
**Influence Maximization**: Leveraging relationships for faction goals
**Diplomatic Priorities**: Key relationships requiring attention ## Semantic Connections *Related concepts and locations:*

- [[Insect Plague Xphb|Insect Plague Xphb
- [Secondary Tables Arcane Matters Xge|Secondary Tables Arcane Matters Xge]]
- [[Wizard Xphb School of Enchantment|Wizard Xphb School Of Enchantment
- [Groups|Groups]]
- [[Trade_Goods|Trade Goods
- [Optional Features|Optional Features]]
- [[Shadow Broker Maximian Darkmarket|Shadow Broker Maximian Darkmarket
- [Groups|Groups]]
- [[12 Research|12 Research
- [Groups|Groups]] ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Related

- [[Aquabyssos World Guide|Aquabyssos World Guide
- [Aethermoor World Guide|Aethermoor World Guide]] ## Alternate Descriptions

- **First Impression**: Initial appearance
- **Closer Look**: Detailed examination
- **Hidden Details**: Secret aspects ## Player Tips

> 🎮 **Strategy**: How to approach this content

> Work together and communicate

## Notes {#notes}

*Additional notes*

#mechanics/combat
#mechanics/rules
#mechanics/mechanics
#mechanics/system
#story/story
#story/lore
#world/location
#world/world
#world/place
#character/npc
#character/character
#gameplay/session
#gameplay/encounter
#gameplay/quest
#resource/item
#meta/index
#meta/navigation
#meta/reference

**Key Question**: What role will this play in the greater story?

**Balance Note**: Adjust creature numbers based on party size and level.

*The dice will decide the fate.*

## Visual References
![[04_Resources/Assets/Locations/location-city-guildmaster-harwick-v1-guildmaster-harwick.png
![04_Resources/Assets/Locations/location-city-surge-mixmaster-v1-surge-mixmaster.png]]
![[04_Resources/Assets/Locations/location-city-master-archivist-thomas-scrollkeeper-v1-master-archivist-thomas-scrollkeeper.png]]
