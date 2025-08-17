# Campaign Timeline Visualization

## Interactive Timeline

```mermaid
gantt
    title Campaign Progress Tracker
    dateFormat YYYY-MM-DD
    section Main Story
    Campaign Start          :active, start, 2024-01-01, 7d
    Act 1: Discovery        :act1, after start, 30d
    Act 2: Conflict         :act2, after act1, 45d
    Act 3: Resolution       :act3, after act2, 30d

    section Character Arcs
    Hero's Journey          :hero, 2024-01-15, 90d
    Redemption Arc          :redemption, 2024-02-01, 75d
    Mystery Resolution      :mystery, 2024-01-30, 60d

    section World Events
    Political Crisis        :crit, 2024-02-15, 14d
    Natural Disaster        :disaster, 2024-03-01, 7d
    Festival Celebration    :fest, 2024-03-15, 3d
```

## Session-by-Session Progress

### Visual Session Tracker
| Session | Date | Main Events | Character Focus | Plot Progress |
|---------|------|-------------|-----------------|---------------|
| 1 | 2024-01-01 | Party Formation | Introductions | 🟢🟢⚪⚪⚪ |
| 2 | 2024-01-08 | First Quest | Team Building | 🟢🟢🟢⚪⚪ |
| 3 | 2024-01-15 | Major Discovery | Character A Arc | 🟢🟢🟢🟢⚪ |
| 4 | 2024-01-22 | Faction Conflict | Political Intrigue | 🟢🟢🟢🟢🟢 |

### Progress Indicators
- 🟢 **Complete:** Story element fully explored
- 🟡 **In Progress:** Currently developing
- ⚪ **Planned:** Future content prepared
- 🔴 **Blocked:** Waiting on player decisions
- 🟣 **Optional:** Side content available

## World State Tracking

### Political Climate
```mermaid
pie title Current Political Stability
    "Stable Regions" : 45
    "Contested Areas" : 30
    "Neutral Zones" : 15
    "Active Conflicts" : 10
```

### Economic Conditions
```mermaid
pie title Trade Route Status
    "Open Routes" : 60
    "Restricted Routes" : 25
    "Dangerous Routes" : 10
    "Closed Routes" : 5
```

### Military Positioning
```mermaid
graph TD
    A[Aquabyssos Forces] --> B[Northern Border]
    A --> C[Eastern Fleet]
    A --> D[Capital Guard]

    E[Aethermoor Forces] --> F[Sky Patrol]
    E --> G[Southern Outposts]
    E --> H[Mobile Reserves]

    I[Independent Forces] --> J[Mercenary Companies]
    I --> K[City Militias]
    I --> L[Rebel Groups]
```

## Dynamic Event Tracking

### Consequence Chains
*How player actions create ripple effects*

```mermaid
flowchart TD
    A[Player Action] --> B{Immediate Effect}
    B --> C[Short-term Consequence]
    B --> D[Alternative Outcome]

    C --> E[Regional Impact]
    D --> F[Different Regional Impact]

    E --> G[Long-term Campaign Change]
    F --> H[Alternative Campaign Direction]

    G --> I[End-game Implications]
    H --> J[Different End-game Scenario]
```

### Relationship Temperature
*Track how NPC relationships change over time*

| NPC Name | Initial | Session 3 | Session 6 | Session 9 | Trend |
|----------|---------|-----------|-----------|-----------|-------|
| Lord Blackwater | Neutral | Friendly | Allied | Trusted | ⬆️📈 |
| Captain Storm | Hostile | Hostile | Neutral | Friendly | ⬆️📈 |
| Madame Nightwhisper | Unknown | Suspicious | Cautious | Neutral | ⬆️📈 |

### World Events Calendar
*Upcoming events that will affect the campaign*

```mermaid
timeline
    title Upcoming World Events

    Next Week : Merchant Festival : Guild Elections : Seasonal Weather Change

    Next Month : Royal Wedding : Trade Summit : Military Exercises

    Next Season : Harvest Festival : Political Convention : Natural Phenomenon

    Next Year : Centennial Celebration : Economic Crisis : Discovery Event
```
