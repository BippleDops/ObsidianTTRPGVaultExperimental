# Faction Relationship Chart

```mermaid
graph TD
    A[Player Party] --> B[Faction 1]
    A --> C[Faction 2]
    A --> D[Faction 3]
    B --> E[Allied NPCs]
    C --> F[Neutral NPCs]
    D --> G[Enemy NPCs]
    B -.->|Trade| C
    B -->|War| D
    C -.->|Uneasy Peace| D
```

## Instructions
1. Replace faction names above
2. Adjust relationship arrows
3. Use solid lines for strong relationships
4. Use dotted lines for weak/uncertain relationships
