---
tags: [moc, index, navigation]
created: "2025-08-15T14:04:34.377233"
---

# [[Session Archive

## [Quick Navigation]]
- [[00_Indexes/Quick_Access_Sidebar|← Back to Index
- [[00_System/MASTER_CONTROL|🎮 [Master Control]]]]

## [[Content Directory

### [By Category]]
```dataview
TABLE file.folder as "Location", file.size as "Size"
FROM ""
WHERE contains(file.link, "session")
sort file.name asc
LIMIT 20
```

### [[Recently Updated
```dataview
TABLE file.link as "File"
FROM ""
WHERE contains(file.link, "session")
SORT file.mtime DESC
LIMIT 10
```

### [Orphaned Sessions]]
```dataview
TABLE file.link as "File"
FROM ""
WHERE contains(file.link, "session") AND length(file.inlinks) = 0
LIMIT 10
```

---
*Auto-generated MOC for better navigation*

## [[Session Summary
*Brief overview of this session*

## [Key Events]]
- Event 1
- Event 2

## NPCs Encountered
- [[Name]] - Brief description

## [[Locations Visited
- [[[Location Name]]]] - What happened here

## [[Quest Progress
- [[[Quest Name]]]] - What was accomplished

## Notes for [[Next Session]]
- Important things to remember
- Plot threads to follow up

---
