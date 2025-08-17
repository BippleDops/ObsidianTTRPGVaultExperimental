---

title: Link Integrity Report
type: note
tags:
- note

created: '2025-01-15'
modified: '2025-01-15'
aliases: ["Link Integrity Report"]
status: active
priority: normal
category: 12 Research
subcategory: D&D References
related: []
cssclass: standard
publish: false

---

 # Link Integrity Report ---

## Description

Detailed description pending.
title: Link Integrity Report
type: Lore
tags:
- lore
- both
- index
- status/complete
- link-analysis
- performance
- research
- world/both
- active
- complete
- importance/core

created: '2025-08-11'
modified: '2025-08-14'
status: complete
cssclasses:
- wide-page
- index-page

updated: '2025-08-13T12:34:03.175604+00:00'
world: Both

--- # 🔗 Link Integrity Report

*Tracking Unresolved Links and Orphaned Pages* ## 🔧 Deep Evaluation Improvements *20 targeted improvements identified* ### Connection Improvements - Add cross-references to related notes ### Enhancement Improvements - Add 12_Research-specific enhancement ## Overview

This dashboard monitors link health across the vault, identifying broken references and isolated pages that need connection. --- ## ⚠️ Unresolved Links (Last 30 Days)```dataview

TABLE file.link as "Source", length(file.outlinks) as "Total Links", length(filter(file.outlinks, (x) => !x.file)) as "Broken"

FROM ""

WHERE length(filter(file.outlinks, (x) => !x.file)) > 0

AND file.mtime > date(today) - dur(30 days)

SORT length(filter(file.outlinks, (x) => !x.file)) DESC

LIMIT 20```## 🏝️ Orphaned Pages (No Incoming Links) TABLE file.link as "Orphaned Page", file.mtime as "Last Modified", length(file.tags) as "Tags"

WHERE length(file.inlinks) = 0

AND !contains(file.path, "Templates")

AND !contains(file.path, "Archive")

AND file.name != this.file.name

SORT file.mtime DESC ## 📊 Link Statistics by Category TABLE length(rows.file.link) as "Total Files", sum(rows.outlinks) as "Total Outgoing", sum(rows.inlinks) as "Total Incoming", round(sum(rows.outlinks) / length(rows.file.link), 2) as "Avg Out/File"

WHERE contains(file.path, "Worldbuilding")

GROUP BY split(file.path, "/")[1] as Category

SORT sum(rows.outlinks) DESC ## 🔄 Most Connected Pages TABLE file.link as "Page", length(file.inlinks) as "Incoming", length(file.outlinks) as "Outgoing", (length(file.inlinks) + length(file.outlinks)) as "Total Connections"

WHERE (length(file.inlinks) + length(file.outlinks)) > 10

SORT (length(file.inlinks) + length(file.outlinks)) DESC

LIMIT 15 ## 🚨 Critical Missing Links These are frequently referenced but non-existent pages that should be created: LIST

WHERE any(file.outlinks, (x) => x.display = "Marina" OR x.display = "Deep Mother" OR x.display = "Seven Shards" OR x.display = "Convergence Point")

AND !x.file

LIMIT 10 ### Files Created Without Links (Last 7 Days)

TABLE file.link as "New File", file.ctime as "Created", length(file.outlinks) as "Outgoing", length(file.inlinks) as "Incoming"

WHERE file.ctime > date(today) - dur(7 days)

AND (length(file.outlinks) = 0 OR length(file.inlinks) = 0)

SORT file.ctime DESC --- ### Priority 3: Strengthen Weak Connections

- [] Pages with < 3 connections need more integration
- [] Add bidirectional links where appropriate
- [] Create hub pages for scattered topics --- *Last Updated: * ## Related *Links to related content will be added here.* ## DM Notes *Private notes for campaign integration:*

- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes ## Prophecy Connection Mentioned in The First Prophecy of Shadows ## Plot Hooks - A document has gone missing and truth emerges

- A stranger needs help delivering before dawn
- A stranger needs help delivering before winter ## 12_Research Specific Content Contextual improvement based on 12_Research

## Notes

*Additional notes*

#story/plot
#story/story
#story/lore
#world/world
#meta/index
#meta/hub
#meta/reference