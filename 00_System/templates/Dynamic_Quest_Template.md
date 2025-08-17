<%*
// Dynamic Quest Template
const questName = tp.file.title;
const campaign = await tp.system.prompt("Campaign");
const questType = await tp.system.suggester(
    ["Main Story", "Side Quest", "Personal Quest", "Faction Quest", "Random Encounter"],
    ["main", "side", "personal", "faction", "random"]
);
const priority = await tp.system.suggester(["High", "Medium", "Low"], ["high", "medium", "low"]);
const complexity = await tp.system.suggester(["Simple", "Complex", "Epic"], ["simple", "complex", "epic"]);

// Generate quest structure based on type and complexity
let questStructure = "";
if (complexity === "epic") {
    questStructure = `
## Act Structure
### Act I: Setup
- [ ] <% tp.system.prompt("Act 1 objective") %>
- [ ] <% tp.system.prompt("Act 1 complication") %>

### Act II: Development
- [ ] <% tp.system.prompt("Act 2 objective") %>
- [ ] <% tp.system.prompt("Act 2 twist") %>

### Act III: Resolution
- [ ] <% tp.system.prompt("Act 3 climax") %>
- [ ] <% tp.system.prompt("Act 3 resolution") %>
`;
} else if (complexity === "complex") {
    questStructure = `
## Quest Phases
### Phase 1: Investigation
- [ ] <% tp.system.prompt("Investigation step") %>

### Phase 2: Action
- [ ] <% tp.system.prompt("Action step") %>

### Phase 3: Resolution
- [ ] <% tp.system.prompt("Resolution step") %>
`;
} else {
    questStructure = `
## Quest Steps
1. [ ] <% tp.system.prompt("First step") %>
2. [ ] <% tp.system.prompt("Second step") %>
3. [ ] <% tp.system.prompt("Third step") %>
`;
}

// Dynamic rewards based on quest type
let rewardStructure = "";
if (questType === "main") {
    rewardStructure = `
### Major Rewards
- **XP:** <% tp.system.prompt("XP Reward", "500") %>
- **Story Progress:** <% tp.system.prompt("How does this advance the main story?") %>
- **Character Development:** <% tp.system.prompt("Character growth opportunity") %>
`;
} else {
    rewardStructure = `
### Rewards
- **XP:** <% tp.system.prompt("XP Reward", "200") %>
- **Gold:** <% tp.system.prompt("Gold Reward", "100") %> gp
- **Items:** <% tp.system.prompt("Item rewards", "None") %>
`;
}
_%>---
type: quest
name: <% questName %>
campaign: <% campaign %>
quest_type: <% questType %>
status: available
priority: <% priority %>
complexity: <% complexity %>
quest_giver: [[<% tp.system.prompt("Quest Giver NPC") %>]]
location: [[<% tp.system.prompt("Primary Location") %>]]
estimated_duration: <% tp.system.prompt("Estimated sessions", "1-2") %> sessions
deadline: <% tp.system.prompt("Deadline (if any)", "None") %>
created: <% tp.date.now() %>
tags: [quest, <% questType %>, <% priority %>-priority]
---

# <% questName %>

> [!quest] Quest Summary
> <% tp.system.prompt("One-sentence quest summary") %>

## Objective
<% tp.system.prompt("What needs to be accomplished?") %>

## Background
### Why This Quest Exists
<% tp.system.prompt("What created this situation?") %>

### Urgency Factor
<% tp.system.prompt("Why does this need to be done now?") %>

<% questStructure %>

## Key NPCs
### Quest Giver
- **[[<% tp.system.prompt("Quest Giver NPC") %>]]** - <% tp.system.prompt("Their motivation for giving this quest") %>

### Supporting NPCs
- **[[<% tp.system.prompt("Supporting NPC 1", "TBD") %>]]** - <% tp.system.prompt("Their role", "TBD") %>
- **[[<% tp.system.prompt("Supporting NPC 2", "TBD") %>]]** - <% tp.system.prompt("Their role", "TBD") %>

### Potential Opposition
- **<% tp.system.prompt("Antagonist/Obstacle", "TBD") %>** - <% tp.system.prompt("Why they oppose the quest", "TBD") %>

## Locations
### Primary Location
- **[[<% tp.system.prompt("Primary Location") %>]]** - <% tp.system.prompt("Why this location is important") %>

### Additional Locations
- **[[<% tp.system.prompt("Secondary Location", "TBD") %>]]** - <% tp.system.prompt("Purpose", "TBD") %>

## Challenges & Obstacles
### Primary Challenge
<% tp.system.prompt("Main obstacle to overcome") %>

### Secondary Challenges
- <% tp.system.prompt("Challenge 1") %>
- <% tp.system.prompt("Challenge 2") %>

### Skill Challenges
- **<% tp.system.prompt("Skill 1", "Investigation") %>** (DC <% tp.system.prompt("DC", "15") %>): <% tp.system.prompt("What this accomplishes") %>
- **<% tp.system.prompt("Skill 2", "Persuasion") %>** (DC <% tp.system.prompt("DC", "12") %>): <% tp.system.prompt("What this accomplishes") %>

<% rewardStructure %>

## Possible Outcomes
### Complete Success
<% tp.system.prompt("What happens with complete success?") %>

### Partial Success
<% tp.system.prompt("What happens with partial success?") %>

### Failure
<% tp.system.prompt("What happens if they fail?") %>

## Quest Hooks
### Introduction Methods
- <% tp.system.prompt("How might players first encounter this quest?") %>
- <% tp.system.prompt("Alternative introduction method") %>

### Player Motivation
<% tp.system.prompt("Why would the players want to do this quest?") %>

## DM Notes
> [!dm] DM Information
> <% tp.system.prompt("Secret information or hidden agenda") %>

### Scaling Options
- **Easier:** <% tp.system.prompt("How to make this easier") %>
- **Harder:** <% tp.system.prompt("How to make this harder") %>

### Connection to Larger Plot
<% tp.system.prompt("How does this connect to the main campaign?") %>

---
*Created with Dynamic Quest Template on <% tp.date.now() %>*
