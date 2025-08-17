<%*
// Advanced NPC Template with dynamic content generation
const npcName = tp.file.title;
const campaign = await tp.system.prompt("Campaign", "Aquabyssos");
const importance = await tp.system.suggester(["Major", "Minor", "Background"], ["major", "minor", "background"]);
const race = await tp.system.prompt("Race");
const profession = await tp.system.prompt("Class/Profession");

// Generate appropriate tags based on selections
let tags = ["npc"];
if (campaign) tags.push(campaign.toLowerCase());
if (importance) tags.push(importance);
if (race) tags.push(race.toLowerCase().replace(" ", "-"));

// Dynamic stat generation based on importance
let statBlock = "";
if (importance === "major") {
    statBlock = `
## Combat Statistics
- **AC:** <% tp.system.prompt("Armor Class", "12") %>
- **HP:** <% tp.system.prompt("Hit Points", "25") %>
- **Speed:** <% tp.system.prompt("Speed", "30 ft") %>
- **CR:** <% tp.system.prompt("Challenge Rating", "1/4") %>

### Ability Scores
| STR | DEX | CON | INT | WIS | CHA |
|-----|-----|-----|-----|-----|-----|
| <% tp.system.prompt("STR", "10") %> | <% tp.system.prompt("DEX", "12") %> | <% tp.system.prompt("CON", "13") %> | <% tp.system.prompt("INT", "11") %> | <% tp.system.prompt("WIS", "12") %> | <% tp.system.prompt("CHA", "14") %> |
`;
}
_%>---
type: npc
name: <% npcName %>
campaign: <% campaign %>
importance: <% importance %>
race: <% race %>
class: <% profession %>
status: active
location: <% tp.system.prompt("Current Location") %>
created: <% tp.date.now() %>
tags: <% "[" + tags.map(tag => `"${tag}"`).join(", ") + "]" %>
---

# <% npcName %>

> [!info] Quick Reference
> **Race:** <% race %> | **Class:** <% profession %> | **Location:** <% tp.system.prompt("Current Location") %>

## Basic Information
- **Full Name:** <% npcName %>
- **Race:** <% race %>
- **Class/Profession:** <% profession %>
- **Age:** <% tp.system.prompt("Age") %>
- **Alignment:** <% tp.system.prompt("Alignment", "Neutral") %>
- **Current Location:** <% tp.system.prompt("Current Location") %>

## Appearance
<% tp.system.prompt("Physical description (height, build, distinctive features)") %>

### Distinctive Features
- <% tp.system.prompt("First distinctive feature") %>
- <% tp.system.prompt("Second distinctive feature") %>

## Personality
### Core Traits
- **Personality Trait:** <% tp.system.prompt("Primary personality trait") %>
- **Ideal:** <% tp.system.prompt("What drives them?") %>
- **Bond:** <% tp.system.prompt("What do they care about most?") %>
- **Flaw:** <% tp.system.prompt("What is their weakness?") %>

### Voice & Mannerisms
- **Voice:** <% tp.system.prompt("How do they sound? (accent, tone, speed)") %>
- **Mannerisms:** <% tp.system.prompt("Gestures, habits, quirks") %>
- **Catchphrase:** <% tp.system.prompt("Something they say often (optional)", "") %>

## Background
### History
<% tp.system.prompt("Character's background and history") %>

### Current Situation
<% tp.system.prompt("What are they doing now? Current goals?") %>

## Role in Campaign
### Story Purpose
<% tp.system.prompt("Why does this NPC exist in your campaign?") %>

### Potential Hooks
- <% tp.system.prompt("First quest hook or interaction opportunity") %>
- <% tp.system.prompt("Second quest hook or interaction opportunity") %>

<% statBlock %>

## Relationships
### Family
- <% tp.system.prompt("Family member (optional)", "None known") %>

### Professional
- <% tp.system.prompt("Professional relationship", "TBD") %>

### Friends/Enemies
- <% tp.system.prompt("Important relationship", "TBD") %>

## Resources & Possessions
### Equipment
- <% tp.system.prompt("Important equipment or possessions") %>

### Wealth Level
<% tp.system.suggester(["Wealthy", "Comfortable", "Modest", "Poor"], ["wealthy", "comfortable", "modest", "poor"]) %>

## DM Notes
> [!dm] DM Only Information
> <% tp.system.prompt("Secret information about this NPC") %>

### Plot Connections
<% tp.system.prompt("How does this NPC connect to larger plot elements?") %>

### Development Opportunities
<% tp.system.prompt("How might this character grow or change?") %>

---
*Created with Advanced NPC Template on <% tp.date.now() %>*
