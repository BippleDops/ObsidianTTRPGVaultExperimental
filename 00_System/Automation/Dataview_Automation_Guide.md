# Dataview Automation Workflows

## Automatic Index Generation

### NPC Auto-Index
```dataview
TABLE WITHOUT ID
  file.link as "NPC",
  race as "Race",
  class as "Class",
  location as "Location",
  campaign as "Campaign"
FROM "03_People"
WHERE type = "npc"
SORT campaign, importance DESC, file.name ASC
```

### Quest Status Dashboard
```dataview
TABLE WITHOUT ID
  file.link as "Quest",
  status as "Status",
  priority as "Priority",
  quest_giver as "Giver",
  deadline as "Deadline"
FROM ""
WHERE type = "quest" AND status != "completed"
SORT priority DESC, deadline ASC
```

### Session Timeline
```dataview
TABLE WITHOUT ID
  file.link as "Session",
  session_number as "#",
  date as "Date",
  campaign as "Campaign"
FROM "06_Sessions"
WHERE type = "session"
SORT date DESC
LIMIT 10
```

## Dynamic Content Generation

### Random Encounter List
```dataview
LIST
FROM ""
WHERE type = "encounter" AND contains(tags, "random")
SORT file.name
```

### Available Plot Hooks
```dataview
TABLE WITHOUT ID
  file.link as "Hook",
  difficulty as "Difficulty",
  campaign as "Campaign"
FROM ""
WHERE type = "quest" AND status = "available"
SORT priority DESC
```

### NPC Relationship Web
```dataview
TABLE WITHOUT ID
  file.link as "NPC",
  choice(relationships, relationships, "None listed") as "Relationships"
FROM "03_People"
WHERE type = "npc" AND relationships
```

## Automated Reminders

### Upcoming Deadlines
```dataview
TABLE WITHOUT ID
  file.link as "Item",
  deadline as "Due Date",
  choice(date(today) > date(deadline), "⚠️ OVERDUE", choice(date(deadline) - date(today) <= dur(7 days), "🔶 Soon", "📅 Scheduled")) as "Status"
FROM ""
WHERE deadline AND deadline != ""
SORT date(deadline) ASC
```

### Character Development Opportunities
```dataview
TABLE WITHOUT ID
  file.link as "Character",
  choice(character_focus_count < 3, "📈 Needs spotlight", choice(character_focus_count > 6, "✅ Well developed", "👥 Balanced")) as "Development Status"
FROM ""
WHERE type = "character"
```

## Workflow Automation Templates

### New Session Workflow
1. **Pre-Session Automation**
   ```dataview
   TASK
   FROM ""
   WHERE contains(tags, "session-prep") AND status = "pending"
   ```

2. **Post-Session Automation**
   ```dataview
   TABLE WITHOUT ID
     file.link as "Update Needed",
     "Type: " + type as "Content Type"
   FROM ""
   WHERE contains(tags, "needs-update") OR (type = "quest" AND status = "active")
   ```

### Campaign Health Check
```dataview
TABLE WITHOUT ID
  "📊 " + metric as "Metric",
  value as "Current",
  target as "Target",
  choice(value >= target, "✅", "⚠️") as "Status"
FROM ""
WHERE type = "metric"
```

## Custom Dataview Functions

### Quest Complexity Calculator
*Automatically calculate quest complexity based on steps*

### NPC Importance Ranking
*Auto-rank NPCs based on mentions and connections*

### Timeline Conflict Detection
*Identify scheduling conflicts in campaign events*

## Integration Triggers

### When Creating New NPCs
- [ ] Auto-add to appropriate campaign lists
- [ ] Generate relationship placeholders
- [ ] Add to location rosters
- [ ] Create portrait placeholder

### When Completing Quests
- [ ] Update character progression
- [ ] Modify world state
- [ ] Generate follow-up hooks
- [ ] Archive quest materials

### When Starting New Sessions
- [ ] Generate session prep checklist
- [ ] Update active quest status
- [ ] Prepare NPC quick reference
- [ ] Set up encounter tables
