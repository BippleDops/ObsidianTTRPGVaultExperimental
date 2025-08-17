# Location Master Index

## All Locations
```dataview
TABLE type, region, campaign, description
FROM "02_Worldbuilding"
WHERE type = "location" OR contains(file.name, "place") OR contains(file.name, "location")
SORT file.name
```

## By Region
