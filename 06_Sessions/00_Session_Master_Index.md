# Session Master Index

*Last Updated: 2025-08-16 10:01:40*

## All Sessions
```dataview
TABLE
  session_number as "Session",
  campaign as "Campaign",
  date as "Date",
  status as "Status"
FROM "06_Sessions"
WHERE type = "session"
SORT campaign, session_number ASC
```

## Recent Sessions
```dataview
TABLE
  file.link as "Session",
  campaign as "Campaign",
  session_number as "#"
FROM "06_Sessions"
WHERE type = "session"
SORT date DESC
LIMIT 10
```

## Sessions by Campaign
```dataview
TABLE
  session_number as "#",
  date as "Date",
  status as "Status"
FROM "06_Sessions"
WHERE type = "session"
GROUP BY campaign
SORT campaign, session_number ASC
```

## Session Statistics
- **Total Sessions:** 219
- **Campaigns Active:** *Count from dataview*
- **Average Session Length:** *Calculate from content*

## Quick Actions
- [[Session_Template|Create New Session]]
- [[Session_Prep_Checklist|Prep Next Session]]
- [[Campaign_Timeline|View Timeline]]

## Session Analysis
### Attendance Tracking
*Track which players attended which sessions*

### Plot Thread Tracking
*Monitor ongoing storylines across sessions*

### XP and Milestone Tracking
*Character progression through sessions*
