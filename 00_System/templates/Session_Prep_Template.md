<%*
// Automated Session Prep Template
const sessionNum = await tp.system.prompt("Session Number");
const campaign = await tp.system.prompt("Campaign");
const lastSession = await tp.system.prompt("Last Session Summary");

// Auto-generate session date (next week from today)
const nextWeek = new Date();
nextWeek.setDate(nextWeek.getDate() + 7);
const sessionDate = tp.date.now("YYYY-MM-DD", 0, nextWeek);
_%>---
type: session
session_type: prep
campaign: <% campaign %>
session_number: <% sessionNum %>
planned_date: <% sessionDate %>
status: planning
created: <% tp.date.now() %>
tags: [session, prep, <% campaign.toLowerCase() %>]
---

# Session <% sessionNum %> Prep - <% tp.system.prompt("Session Title") %>

> [!info] Session Overview
> **Campaign:** <% campaign %> | **Date:** <% sessionDate %> | **Duration:** <% tp.system.prompt("Expected Duration", "3-4 hours") %>

## Pre-Session Checklist
- [ ] Review last session notes
- [ ] Prepare NPC voices and mannerisms
- [ ] Set up virtual tabletop/maps
- [ ] Review active quest status
- [ ] Prepare random encounter table
- [ ] Check character sheet updates
- [ ] Prepare handouts/props
- [ ] Set up music/ambience

## Last Session Recap
<% lastSession %>

### Cliffhangers to Resolve
- <% tp.system.prompt("Cliffhanger 1", "None") %>
- <% tp.system.prompt("Cliffhanger 2", "None") %>

## This Session's Plan

### Opening Scene
<% tp.system.prompt("How does the session begin?") %>

### Key Scenes
1. **<% tp.system.prompt("Scene 1 Title") %>**
   - Location: [[<% tp.system.prompt("Scene 1 Location") %>]]
   - Purpose: <% tp.system.prompt("Scene 1 Purpose") %>
   - NPCs: <% tp.system.prompt("Scene 1 NPCs") %>

2. **<% tp.system.prompt("Scene 2 Title") %>**
   - Location: [[<% tp.system.prompt("Scene 2 Location") %>]]
   - Purpose: <% tp.system.prompt("Scene 2 Purpose") %>
   - NPCs: <% tp.system.prompt("Scene 2 NPCs") %>

3. **<% tp.system.prompt("Scene 3 Title") %>**
   - Location: [[<% tp.system.prompt("Scene 3 Location") %>]]
   - Purpose: <% tp.system.prompt("Scene 3 Purpose") %>
   - NPCs: <% tp.system.prompt("Scene 3 NPCs") %>

### Potential Conclusion
<% tp.system.prompt("Where might the session end?") %>

## NPCs This Session
### Primary NPCs
- **[[<% tp.system.prompt("Primary NPC 1") %>]]**
  - Voice: <% tp.system.prompt("Voice description") %>
  - Goal: <% tp.system.prompt("What they want this session") %>
  - Info: <% tp.system.prompt("Key information they have") %>

- **[[<% tp.system.prompt("Primary NPC 2", "None") %>]]**
  - Voice: <% tp.system.prompt("Voice description", "N/A") %>
  - Goal: <% tp.system.prompt("What they want this session", "N/A") %>
  - Info: <% tp.system.prompt("Key information they have", "N/A") %>

### Background NPCs
- <% tp.system.prompt("Background NPC 1", "Various townspeople") %>
- <% tp.system.prompt("Background NPC 2", "Guards, merchants, etc.") %>

## Encounters Prepared

### Combat Encounters
1. **<% tp.system.prompt("Combat 1 Name", "None planned") %>**
   - Enemies: <% tp.system.prompt("Enemy types and numbers", "N/A") %>
   - Location: <% tp.system.prompt("Combat location", "N/A") %>
   - Trigger: <% tp.system.prompt("What triggers this combat", "N/A") %>

### Social Encounters
1. **<% tp.system.prompt("Social encounter", "Negotiation with local official") %>**
   - NPCs involved: <% tp.system.prompt("Social NPCs") %>
   - Goal: <% tp.system.prompt("What can be achieved") %>
   - Complications: <% tp.system.prompt("Potential problems") %>

### Exploration Encounters
1. **<% tp.system.prompt("Exploration encounter", "Investigating mysterious location") %>**
   - Discovery: <% tp.system.prompt("What can be found") %>
   - Challenges: <% tp.system.prompt("Obstacles to overcome") %>

## Random Tables for This Session

### Random Events (d6)
| Roll | Event |
|------|--------|
| 1 | <% tp.system.prompt("Random event 1") %> |
| 2 | <% tp.system.prompt("Random event 2") %> |
| 3 | <% tp.system.prompt("Random event 3") %> |
| 4 | <% tp.system.prompt("Random event 4") %> |
| 5 | <% tp.system.prompt("Random event 5") %> |
| 6 | <% tp.system.prompt("Random event 6") %> |

### NPC Names (if needed)
- <% tp.system.prompt("Random name 1") %>
- <% tp.system.prompt("Random name 2") %>
- <% tp.system.prompt("Random name 3") %>

## Quest Progress Tracking
### Active Quests
- **[[<% tp.system.prompt("Active quest 1") %>]]** - <% tp.system.prompt("Expected progress") %>
- **[[<% tp.system.prompt("Active quest 2", "None") %>]]** - <% tp.system.prompt("Expected progress", "N/A") %>

### New Quest Opportunities
- <% tp.system.prompt("New quest opportunity", "None planned") %>

## Props & Handouts
### Physical Props
- <% tp.system.prompt("Props needed", "None") %>

### Digital Handouts
- <% tp.system.prompt("Handouts to prepare", "None") %>

### Maps Required
- <% tp.system.prompt("Maps needed", "Battle maps, location maps") %>

## Contingency Plans

### If Session Runs Short
<% tp.system.prompt("Backup content if session ends early") %>

### If Players Go Off-Track
<% tp.system.prompt("How to handle unexpected player actions") %>

### If Dice Are Hot/Cold
- **Players rolling well:** <% tp.system.prompt("How to handle easy success") %>
- **Players rolling poorly:** <% tp.system.prompt("How to handle repeated failure") %>

## Post-Session Notes Section
*Fill out during/after the session*

### What Actually Happened
*Brief summary of actual events*

### Player Choices
*Important decisions made by players*

### XP Awarded
*Experience points given*

### Loot Distributed
*Items, gold, or other rewards*

### Next Session Hooks
*Cliffhangers or setup for next time*

### DM Self-Evaluation
*What went well, what to improve*

---
*Session prep completed on <% tp.date.now() %>*
