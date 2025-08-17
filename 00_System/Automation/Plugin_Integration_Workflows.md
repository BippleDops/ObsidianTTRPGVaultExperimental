# Plugin Integration Workflows

## Templater Advanced Usage

### Context-Aware Templates
*Templates that adapt based on existing vault content*

#### Smart NPC Template
```javascript
<%*
// Check for existing NPCs in same location
const currentLocation = await tp.system.prompt("Location");
const existingNPCs = app.vault.getMarkdownFiles()
  .filter(file => file.path.includes("03_People"))
  .map(file => file.basename);

// Suggest relationships with existing NPCs
if (existingNPCs.length > 0) {
  const relatedNPC = await tp.system.suggester(
    existingNPCs, existingNPCs,
    false,
    "Related to existing NPC?"
  );
}
%>
```

#### Campaign-Aware Quest Template
```javascript
<%*
// Auto-detect campaign based on active files
const recentFiles = app.workspace.getRecentFiles()
  .filter(file => file.includes("01_Adventures"))
  .map(file => file.split("/").pop().replace(".md", ""));

const campaign = recentFiles.length > 0 ?
  await tp.system.suggester(["Auto-detect: " + recentFiles[0], "Choose different"], [recentFiles[0], "other"]) :
  await tp.system.prompt("Campaign");
%>
```

## Kanban Plugin Automation

### Auto-Moving Cards
*Set up rules for automatic card movement*

#### Quest Progression Rules
- When quest status changes to "active" → Move to "In Progress"
- When session date passes → Move session prep to "Completed"
- When deadline approaches → Add urgency emoji

#### Campaign Phase Rules
- Act completion → Auto-archive related cards
- Character milestones → Move development cards
- Plot resolution → Generate follow-up cards

### Smart Card Creation
*Templates for quick card creation*

```javascript
// Quick NPC card
Name: {{character name}}
Type: {{major/minor/background}}
Campaign: {{auto-detect from context}}
Next appearance: {{session + 1}}
```

## Calendar Integration

### Automated Event Tracking
*Link campaign events to calendar system*

#### Session Scheduling
- Auto-create calendar events for sessions
- Set reminders for session prep
- Track player availability

#### World Event Calendar
- In-game seasonal events
- NPC birthday and important dates
- Political and economic cycles

### Timeline Synchronization
*Keep game time and real time aligned*

## Advanced Search & Navigation

### Smart Search Queries
```
tag:#npc location:"Aquabyssos" campaign:"Current"
```

### Quick Navigation Setup
*Hotkeys and shortcuts for common operations*

- `Ctrl+N+P` → New NPC template
- `Ctrl+N+Q` → New Quest template
- `Ctrl+N+S` → New Session template
- `Ctrl+N+L` → New Location template

### Context-Sensitive Links
*Links that adapt based on current file context*

## Data Validation Workflows

### Consistency Checking
*Automated checks for data integrity*

#### Link Validation
- Check for broken NPC references
- Verify location exists before linking
- Validate quest dependencies

#### Metadata Validation
- Required fields completion
- Date format consistency
- Tag standardization

### Quality Assurance
*Automated content quality checks*

#### Content Completeness
- NPCs have minimum required fields
- Quests have clear objectives
- Sessions have proper structure

## Backup and Version Control

### Automated Backup Triggers
*When to create automatic backups*

- Before major campaign milestones
- After significant world changes
- Weekly scheduled backups
- Before experimental features

### Change Tracking
*Monitor important content changes*

- Track quest status modifications
- Log NPC relationship changes
- Monitor location updates
- Record session outcomes

## Performance Optimization

### Query Optimization
*Make dataview queries run faster*

#### Efficient Patterns
```dataview
// Good: Specific folder targeting
FROM "03_People"
WHERE type = "npc"

// Avoid: Broad searches
FROM ""
WHERE contains(file.path, "People")
```

#### Caching Strategies
*Minimize repeated calculations*

### File Organization
*Optimize vault structure for plugin performance*

#### Folder Strategy
- Separate active from archived content
- Use consistent naming conventions
- Limit deeply nested structures

#### File Size Management
- Split large files into smaller components
- Use includes for repeated content
- Archive old session notes

## Troubleshooting Common Issues

### Plugin Conflicts
*Identify and resolve plugin conflicts*

### Performance Problems
*Diagnose and fix slow performance*

### Data Corruption
*Prevent and recover from data issues*

### Template Errors
*Debug common template problems*
