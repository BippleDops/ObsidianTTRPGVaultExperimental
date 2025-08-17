---
enhanced: true
tags: [enhanced, 01_adventures]
created: "2025-08-15T12:25:38.042181"
modified: "2025-08-15T12:25:38.042187"
aliases: [Campaign Dashboard]
---

## Table of Contents
- [[#Contents|Contents
- [#Overview|Overview]]
- [[#Description|Description
- [#Background|Background]]
- [[#Notes|Notes
- [#Timeline|Timeline]]
- [[#NPCs Involved|NPCs Involved
- [#Complications|Complications]]
- [[#Alternative Solutions|Alternative Solutions
- [#Stakes|Stakes]]

---
tags: [misc]
type: misc
aliases: ["Campaign Dashboard"]
---

# Campaign Dashboard

> *What starts as simple becomes legendary...*

## Contents
- [Overview](#overview)
- [Description](#description)
- [Background](#background)
- [Notes](#notes)
- [Timeline](#timeline)
- [NPCs Involved](#npcs-involved)
- [Complications](#complications)
- [Alternative Solutions](#alternative-solutions)

## Overview

**Difficulty**: Moderate (Levels 3-5)

Comprehensive overview of this content.

---

title: [[[[[Campaign_Dashboard|Campaign_Dashboard|Campaign_Dashboard]]|Campaign_Dashboard]]
type: quest
tags:
- quest

created: '2025-01-15'
modified: '2025-01-15'
status: active
aliases: ["Campaign Dashboard"]
priority: normal
category: 01 Adventures
subcategory: Campaign Dashboard.Md
related: []
cssclass: standard
publish: false

---

 # Campaign_Dashboard ---

## Description

**Tension**: The urgency of this quest creates palpable tension in the air.

Detailed description pending.
title: Campaign Dashboard - Aquabyssos & Aethermoor
type: [[Lore|Lore]]
tags:
- dashboard
-
*The air carries the scent of [appropriate smell].* master-control
- tracking
- content/lore
- world/both
- research
- active
- campaign/arc
- status/in-progress

created: '2025-08-11'
modified: '2025-08-14'
status: complete
updated: 2025-08-13 07:59:50.494234
world: Both
timeline: current_era
chronology: active

--- # 🌊🌬️ Campaign Dashboard

*Master Control Center for the Dual Worlds*```dataview

TABLE WITHOUT ID "⚡ " + choice(reality_stability < 25, "**CRITICAL**", choice(reality_stability < 50, "**UNSTABLE**", choice(reality_stability < 75, "Wavering", "[[stable|Stable"))) AC "Reality Status", "📊 " + reality_stability + "/100" AC "Stability", "🌀 " + deep_mother_influence + "/100" AC "[Deep Mother|Deep Mother]]", "⏰ Session " + current_session AC "Progress"

FROM "Campaign_Dashboard"

WHERE file.[[Name|name = this.file.name```## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## 📊 Faction Power Tracker faction AC "Faction", "⚔️ " + military AC "Military", "💰 " + economic AC "Economic", "🏛️ " + political AC "Political", "🔍 " + information AC "Information", "✨ " + ideological AC "Ideological", "📈 " + total_power AC "Total"

FROM "[02_Worldbuilding|02_Worldbuilding]]/Groups"

WHERE contains(tags, "major-faction")

SORT total_power DESC

LIMIT 10 ### Active Conflicts

1. **Tidal Council vs [[Surface Seekers|Surface Seekers** - Open hostilities
2. Therefore, **Crystal Wardens vs Parasite Priests** - Ideological war
3. **Merchant Guilds vs Everyone** - Economic manipulation
4. **Deep Mother Cults vs Reality** - Existential threat ### Power Players

| NPC | [location|Location]] | Status | [[loyalty|Loyalty | Next Action |
|-----|----------|--------|---------|-------------|
| **Nerissa Deepcurrent** | Maelstrom Palace | Desperate | Neutral | Seeking allies |
| **Queen Seraphina** | Crystal Palace | Mad | Unstable | Festival ritual |
| **Vex Shadowthorn** | Unknown | Active | Hostile | Shadow harvest |
| **[Marina|Marina]] Coralheart** | Multiple | Fractured | Confused | Identity crisis |
| **Director Silverscale** | Consortium HQ | Plotting | Self | Economic war | ### Rising Threats

| NPC | Threat Level | Growth Rate | Counter-measures |
|-----|--------------|-------------|------------------|
| **Deep Mother** | 8/10 | Exponential | [[Reality Anchors|Reality Anchors failing |
| **The Silhouette Prime** | 7/10 | Steady | Shadow detection needed |
| **Prophet Deepest-Dream** | 6/10 | Accelerating | Prophecy interpretation |
| **Archive-Prince Mnemonic** | 5/10 | Unknown | Memory protection | ### Potential Allies

| NPC | Faction | Requirements | Benefits |
|-----|---------|--------------|----------|
| **Captain Stormcutter** | Independent | Protection | Military support |
| **Sage Lysander** | Scholars | Knowledge trade | Ancient secrets |
| **Merchant Prince Akula** | Guilds | Economic deal | Resources |
| **Sister Morwyn** | Temple | Religious quest | Divine protection | ### Party Status character_name AC "Character", player AC "Player", adaptation_points AC "AP", faction_standing AC "Primary Faction", sanity AC "Sanity", status AC "Status"

FROM "Player_Characters"

WHERE campaign = "Active" ### Instant Encounter Generator```button

name Generate Random Encounter
type command
action Dataview: Generate random encounter based on current location and threat level
color blue ### Faction Action Resolver

name Resolve Faction Turn
action Calculate and apply all faction [actions|actions]] for this turn
color green ### Reality Check

name Check Reality Stability
action Roll for reality events and apply changes
color red ### NPC Reaction

name Generate NPC Response
action Create contextual NPC reaction based on current situation
color yellow ### Player-[[facing|Facing Encounter [Handouts|Handouts]]

LIST FROM "[[04_Resources|04_Resources/Handouts/Encounters"

SORT file.name ASC ### GM Encounter Sheets

LIST FROM "06_GM_Resources/Travel/Encounter_Sheets" ### Convergence Factors

| Factor | Status | Acceleration |
|--------|--------|--------------|
| Surface Seal | Weakening | +2/session |
| Deep Mother | Awakening | +3/session |
| Reality Anchors | Failing | +1/session |
| Adaptation Spread | Increasing | +1/session |
| Prophecies | Manifesting | +2/session |
| **Total** | **Critical** | **+9/session** | ### 📝 Notes for [Next Session|Next Session]]

Key Focus Areas:
1. Marina identity crisis resolution scene
2. Parliament emergency vote on Surface Seal
3. First major reality merger event
4. Parasite outbreak containment
5. [[Crystal Festival|Crystal Festival preparations reveal Remember:

- Players have [Reality Anchor|Reality Anchor]] (2 charges left)
- Vex Shadowthorn knows party location
- Memory tide will reveal hidden truths
- Queen's [[madness|madness linked to Deep Mother
- Time loop possibility in Lighthouse ## 🔄 Auto-Update Status```dataviewjs

// This would automatically update based on session logs
const last Update = dv.page("[Session Log|Session Log]]").file.mtime;
const days Since Update = (Date.now() - last Update) / (1000 * 60 * 60 * 24); if (days Since Update > 7) { dv.paragraph("⚠️ **Dashboard needs update** - Last updated: " + days Since Update + " days ago");
} else { dv.paragraph("✅ Dashboard current - Last updated: " + days Since Update + " days ago");
} --- ## Navigation

- [[Master Index - Complete vault navigation
- [World Bible]] - Comprehensive lore reference - [[INDEX - Session archive
- [[[Quick_Start_Guide|Quick Start Guide]] (D&D_References)]] - New player onboarding
- [[GM Resource - Gamemaster tools --- *Dashboard Version 2.0 - Real-time campaign tracking and management*

*Auto-refreshes with session updates*
*Integrated with all major vault systems* ## Related *Links to [Related content|related content]] will be added here.* ## [[DM_Notes|DM Notes]] *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Plot Hooks - A journal reveals a conspiracy about a local noble

- A shipment has gone missing and evil awakens
- A letter reveals the truth about the cult

## Background

*[Adventure setup and context]* ### What Happened Before

- *[Recent events leading to this adventure]* ### Current Situation - *[What's happening now]* ### The Stakes

- *[What happens if PCs don't act]* ## Adventure Hooks

*[Ways to get PCs involved]* ### Direct Approach

- *[Straightforward hook]* ### Indirect Approach

- *[Subtle introduction]* ### Emergency Hook

- *[Urgent situation]* ## Key NPCs

*[Important characters in this adventure]* ### Allies

- *[Helpful NPCs]* ### Antagonists

- *[Opposition NPCs]* ### Neutral Parties

- *[Information sources]* ## Locations

*[Important places in this adventure]* ### Starting Location

- *[Where adventure begins]* ### Key Sites

- *[Major locations to visit]* ### Optional Areas

- *[Side locations]* ## [[rewards|Rewards]]

*[What PCs gain from completing this adventure]* ### Experience Points

- *[XP awards]* ### Treasure

- *[Gold and [[Magic [Items|Items|Magic Items]]]* ### Story Rewards

- *[Reputation, allies, information]* ## Scaling

*[How to adjust for different party levels]* ### Lower Level Parties

- *[Adjustments for weaker groups]* ### Higher Level Parties

- *[Adjustments for stronger groups]* ### Large/Small Parties

- *[Adjustments for party size]* ## DM Tips

> 💡 **Running This Content**: Advice for game masters

> Adjust difficulty based on party composition ## References - [[Topic Matrix

- [Topic_Matrix (Indexes)]]

## Notes

*Additional notes*

#mechanics/system
#story/plot
#story/story
#story/lore
#story/background
#world/location
#world/world
#world/place
#character/npc
#character/character
#gameplay/session
#gameplay/encounter
#gameplay/adventure
#gameplay/quest
#resource/item
#resource/treasure
#meta/index
#meta/navigation
#meta/reference

## Timeline
- Key events
- Deadlines

## NPCs Involved
- Quest giver
- Antagonists

## Complications
- Potential problems
- Twists

## Alternative Solutions
- Non-combat options
- Creative approaches

## Stakes
- **If Successful**: The positive outcomes that await
- **If Failed**: The dire consequences of failure
- **Time Pressure**: Why this cannot wait

**Key Question**: Will the heroes rise to the challenge?

## Related Content
*Enhanced with 3 new connections*

## Visual References
![[04_Resources/Assets/Misc/_cross_campaign_organizations.png
![04_Resources/Assets/Misc/parliament_of_shadows_campaign.png]]
![[04_Resources/Assets/Maps/World/Continents/world_cross_campaign_locations_player.png]]
