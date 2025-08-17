# Advanced Linking & Reference System

## Standardized Link Formats

### NPC Links
- **Standard:** `[[NPC Name|Display Name]]`
- **With Icon:** `[[NPC Name|🧙 Display Name]]`
- **With Status:** `[[NPC Name|Display Name (Ally)]]`
- **Quick Reference:** `[[NPC Name|Display Name]]`

### Location Links
- **Standard:** `[[Location Name|Display Name]]`
- **With Type:** `[[Location Name|🏰 Display Name]]`
- **With Region:** `[[Location Name|Display Name (Region)]]`
- **Map Reference:** `[[Location Name|Display Name Map]]`

### Quest Links
- **Standard:** `[[Quest Name|Display Name]]`
- **With Status:** `[[Quest Name|⚔️ Display Name (Active)]]`
- **With Phase:** `[[Quest Name|Display Name Phase 2]]`

### Cross-Reference System
- **Bidirectional:** Ensure relationships are linked both ways
- **Hierarchical:** Parent → Child relationships
- **Thematic:** Group related content with common tags

## Admonition Style Guide

### Information Types
> [!info] General Information
> Basic facts that any character would know about the world.

> [!tip] Player Tip
> Helpful advice or hints for players.

> [!lore] World Lore
> Historical information, cultural details, or background knowledge.

### Game Mechanics
> [!combat] Combat Information
> Initiative, special rules, or tactical details.

> [!dice] Dice Roll Required
> When to roll and what modifiers apply.

> [!spell] Spell Effect
> Magic rules, spell descriptions, or magical phenomena.

### Story Elements
> [!plot] Plot Information
> Story hooks, adventure opportunities, or narrative developments.

> [!quest] Quest Details
> Objectives, requirements, or quest-specific information.

> [!secret] Hidden Information
> Plot twists, NPC secrets, or concealed truths.

### DM Resources
> [!dm] DM Only
> Information exclusively for the Dungeon Master.

> [!note] DM Note
> Reminders, alternatives, or additional context for the DM.

> [!rule] House Rule
> Custom rules or modifications to standard gameplay.

### Warnings & Alerts
> [!warning] Important Warning
> Critical information that affects safety or success.

> [!danger] Immediate Danger
> Threats, traps, or hazardous situations.

> [!caution] Exercise Caution
> Situations requiring careful consideration or planning.

## Advanced Linking Techniques

### Contextual Links
*Links that change meaning based on context*

#### Dynamic References
- `[[NPC Name]]` → Auto-displays appropriate info based on current file
- `[[Location#Current Events]]` → Shows current happenings
- `[[Quest#Player Status]]` → Shows personalized quest status

#### Conditional Display
```
![[NPC Name]] (only if in combat)
![[Location#Social Info]] (only if in social encounter)
```

### Cross-Campaign References
*Linking content across different campaigns*

#### Campaign Prefixes
- `[[AQ_Location_Name]]` (Aquabyssos campaign)
- `[[AE_Location_Name]]` (Aethermoor campaign)
- `[[SH_Location_Name]]` (Shared/neutral content)

#### Universal References
- `[[Rules/Combat]]` → Standard combat rules
- `[[Templates/NPC]]` → NPC creation template
- `[[Resources/Names]]` → Name generation lists

### Smart Link Automation

#### Auto-Completion Patterns
```
Type: Character Name → Suggests: [[Character Name]]
Type: @Location → Suggests: [[Location Name]]
Type: #Quest → Suggests: [[Quest Name]]
```

#### Link Validation
*Automatically check for and suggest corrections*

- Detect broken links
- Suggest similar existing files
- Propose link text improvements
- Flag missing relationships

### Embedded Content Strategy

#### Transclude Patterns
```
![[NPC Name]] → Embed appearance description
![[Location Name]] → Embed location map
![[Quest Name]] → Embed quest objectives
```

#### Conditional Embeds
```
![[Combat_Rules]] (if encounter_type = "combat")
![[Social_Rules]] (if encounter_type = "social")
```

## Link Relationship Types

### Hierarchical Relationships
- **Parent → Child:** Region → City → District → Building
- **Organization:** Faction → Division → Unit → Individual
- **Story:** Campaign → Arc → Session → Scene

### Lateral Relationships
- **Peer:** Same level in hierarchy
- **Allied:** Cooperative relationships
- **Rival:** Competitive relationships
- **Enemy:** Antagonistic relationships

### Temporal Relationships
- **Before:** Historical precedents
- **During:** Simultaneous events
- **After:** Consequences and outcomes
- **Cyclical:** Recurring patterns

### Causal Relationships
- **Cause → Effect:** Action and consequence
- **Dependency:** Required prerequisites
- **Influence:** Indirect effects
- **Correlation:** Related but not causal

## Quality Control Guidelines

### Link Hygiene
- [ ] All important NPCs linked from locations
- [ ] All locations linked from relevant quests
- [ ] All quests linked to quest-giver NPCs
- [ ] Bidirectional relationships maintained

### Admonition Consistency
- [ ] Same admonition type for same purpose
- [ ] Appropriate detail level
- [ ] Clear, concise titles
- [ ] Consistent formatting

### Regular Maintenance
- [ ] Weekly broken link check
- [ ] Monthly relationship audit
- [ ] Quarterly admonition review
- [ ] Annual linking strategy review

## Advanced Features

### Custom Link Types
*Setup specialized link behaviors*

#### Interactive Links
- Hover previews with key information
- Click actions (roll dice, open related content)
- Context menus with quick actions

#### Dynamic Links
- Change color based on relationship status
- Show recent activity indicators
- Display connection strength

### Automated Relationship Mapping
*Let the system build relationship maps*

#### Connection Detection
- Analyze co-occurrence in files
- Track mention frequency
- Identify relationship patterns

#### Visualization Integration
- Auto-generate relationship diagrams
- Update visual maps when links change
- Create interactive network views
