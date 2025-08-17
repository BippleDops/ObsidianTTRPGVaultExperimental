---
enhanced: true
tags: [enhanced, _indexes]
created: "2025-08-15T16:41:31.834082"
modified: "2025-08-15T16:41:31.834089"
aliases: [MASTER NAVIGATION]
---

## Table of Contents
- [[#✅ Reorganization Complete|✅ Reorganization Complete
- [#📊 Statistics|📊 Statistics]]
- [[#📁 Directory Structure|📁 Directory Structure
- [[#🎮 [Adventures]]|🎮 [[Adventures]]
- [[#🌍 [[World|🌍 [World]]]]
- [[#📖 [[Rules|📖 [Rules]]]]
- [[#🎨 [[Resources|🎨 [Resources]]]]
- [[#👥 [[Characters|👥 [Characters]]]]
- [[#⚙️ [[System|⚙️ [System]]]]
- [[#📦 [[Archive|📦 [Archive]]]]

-tags: [index, navigation, master, flattened, combat, magic, exploration, lore]ed]
created: 2025-08-15
---

# 🗺️ Master Navigation - Flattened Vault

## ✅ Reorganization Complete

Your vault has been successfully flattened from numbered directories to a clean topic-based structure.

### 📊 Statistics
- **Old Structure**: 20+ numbered directories (00_, 01_, etc.)
- **New Structure**: 7 main categories
- **Items Reorganized**: 201+
- **Maximum Depth**: 3 levels

## 📁 Directory Structure

### 🎮 [[Adventures
Game content and campaign materials
- `Sessions/` - Game session notes
- `Quests/` - Quest descriptions
- `Encounters/` - Combat and social encounters
- `Campaigns/` - Campaign overviews

### 🌍 [World]]
World-building content
- `NPCs/` - All non-player characters
- `Locations/` - Cities, dungeons, regions
- `Factions/` - Organizations and groups
- `Lore/` - History and mythology
- `Timeline/` - Chronological events
- `Places/` - Geographic locations
- `People/` - Notable individuals
- `Groups/` - Factions and organizations
- `Items/` - Magical items and artifacts

### 📖 [[Rules
Game mechanics and references
- `Mechanics/` - Core game rules
- `Homebrew/` - Custom content
- `References/` - Quick guides
- `Spells/` - Spell compendium
- `Calculators/` - Game calculators
- `Rules_Reference/` - Official rules
- `Transformations/` - Character transformations

### 🎨 [Resources]]
Supporting materials
- `Maps/` - Battle and world maps
- `Assets/` - Images and artwork
- `Handouts/` - Player materials
- `Research/` - Reference materials
- `Tools/` - Generators and utilities
- `References/` - External resources
- `GM_Resources/` - DM tools

### 👥 [[Characters
Character-related content
- `PCs/` - Player characters
- `Party/` - Party resources
- `Tools/` - Character tools
- `Player_Resources/` - Player aids
- `Sheets/` - Character sheets
- `Backstories/` - Character histories

### ⚙️ [System]]
Vault management
- `Indexes/` - Navigation aids
- `Metadata/` - Configuration
- `Analytics/` - Performance tracking
- `Guides/` - Master documentation
- `Templates/` - Note templates
- `Automation/` - Scripts and queries
- `Canvas_Templates/` - Visual templates

### 📦 [[Archive
Historical content
- `backups/` - Backup copies
- `Old/` - Previous versions
- `Deprecated/` - Outdated content
- `Personal/` - Personal notes

## 🔍 Quick Access

### Essential Files
- [README|Vault Overview]]
- [[System/Guides/DM_COMPLETE_GUIDE|DM Guide
- [System/Guides/PLAYER_HANDBOOK|Player Handbook]]
- [[System/Guides/WORLD_BIBLE|World Bible

### Indexes by Type
- [System/Indexes/MOC_NPCs|NPC Index]]
- [[System/Indexes/MOC_Locations|Location Index
- [System/Indexes/MOC_Quests|Quest Index]]
- [[System/Indexes/MOC_Sessions|Session Index
- [System/Indexes/MOC_Rules|Rules Index]]
- [[System/Indexes/MOC_Combat|Combat Index
- [System/Indexes/MOC_Items|Items Index]]
- [[System/Indexes/MOC_Lore|Lore Index]]

### Recent Activity
```dataview
TABLE file.mtime as "Modified"
FROM ""
WHERE file.mtime >= date(today) - dur(1 day)
SORT file.mtime DESC
LIMIT 20
```

### Largest Directories
```dataview
TABLE length(file.folder) as "Files"
FROM ""
GROUP BY file.folder
SORT length(file.folder) DESC
LIMIT 10
WHERE file.name != ""
```

## 🚀 Benefits of Flattened Structure

### ✅ Improved Navigation
- No more confusing numbered directories
- Topic-based organization is intuitive
- Maximum 3 levels deep for easy access
- Clear separation of concerns

### ✅ Better Performance
- Faster file searches
- Reduced directory traversal
- Simpler link resolution
- Cleaner vault structure

### ✅ Easier Maintenance
- Clear where new content belongs
- Simple backup strategy
- Straightforward organization
- No duplicate directory names

## 📝 Migration Notes

### From → To Mapping
- `00_Indexes` → `System/Indexes`
- `00_System` → `System`
- `01_Adventures` → `Adventures`
- `02_Worldbuilding` → `World`
- `03_People` → `World/NPCs`
- `03_Mechanics` → `Rules`
- `04_Resources` → `Resources`
- `05_Player_Characters` → `Characters`
- `05_Rules` → `Rules`
- `06_Sessions` → `Adventures/Sessions`
- `07_Player_Resources` → `Characters`
- `08_Archive` → `Archive`
- `09_Performance` → `System/Analytics`
- `12_Research` → `Resources/Research`

## 🎯 Next Steps

1. **Update Bookmarks** - Update any saved locations
2. **Check Links** - Verify internal links work
3. **Review Content** - Ensure everything is accessible
4. **Customize Further** - Adjust structure as needed

---
*Vault successfully flattened and reorganized on 2025-08-15*

> [!dm] DM Note
> This location connects to the main plot

## Campaign Connection
Has information about the party's enemies

## Recent NPCs
```dataview
TABLE file.mtime as "Modified"
FROM "03_People"
SORT file.mtime DESC
LIMIT 10
WHERE file.name != ""
```

## Active Quests
```dataview
TABLE file.link as "File"
FROM "01_Adventures"
WHERE contains(status, "active")
```

## Session Log
```dataview
TABLE date as "Date", players_present as "Players"
FROM "06_Sessions"
SORT date DESC
WHERE file.name != ""
```

## Location Network
```dataview
TABLE file.link as "File"
FROM "02_Worldbuilding"
WHERE contains(file.name, "Location") OR contains(tags, "location")
```
## See Also
- [[Guild Seal Document Silverscale Consortiu
- [Archdruid Thornweaver]]
- [[NPC01082_Fiora_Ashford_the_Fallen
- [NPC00385_Qadim_Darkwater_the_Cunning]]
- [[NPC00761_Aldric_Moonshadow_the_Guardian
- [NPC00129_Gareth_Jadeclaw]]
- [[NPC01371_Xander_Stormwind_the_Guardian
- [NPC01504_Erasmus_Zephyrblade_the_Strong]]
- [[NPC00881_Qadim_Voidwalker_the_Strong
- [NPC00707_Fiora_Oakenshield_the_Seeker]]
- [[NPC00878_Kaelen_Ironwood_the_Strong
- [NPC01931_Thalia_Lightbringer_the_Fallen]]
- [[NPC01858_Drusilla_Stormwind_the_Cunning
- [NPC00927_Aldric_Ironwood_the_Wanderer]]
- [[11 Spellcasting
- [NPC00162_Xander_Thornweave]]
- [[Calendar_Conversions_Realm_Window
- [NPC00587_Idris_Youngblood_the_Strong]]
- [[NPC01555_Branwen_Xendar_the_Seeker
- [NPC00812_Kaelen_Jadeclaw_the_Seeker]]
- [[NPC00395_Aeliana_Thornweave
- [NPC01438_Hilda_Youngblood_the_Fallen]]
- [[NPC01789_Vesper_Proudmore_the_Mystic
- [NPC01699_Orion_Oakenshield_the_Broken]]
- [[MASTER_MOC
- [Master_Narrative_Web.md]]
-

## Item Rarity & Balance
Following magic item guidelines (WWT p.135-136):
- **Rarity**: Common/Uncommon/Rare/Very Rare/Legendary
- **Attunement**: Required for powerful effects
- **Charges**: Limited uses per day (WWT p.141)
- **Curse**: Optional drawback (WWT p.138-139)

### Comparable Official Items
- Power level similar to [[Flame Tongue (WWT p.170)
- Utility comparable to [Bag of Holding]] (WWT p.153)
- Activation like [[Wand of Magic Missiles (WWT p.211)

## Source References
- Adventurer's Codex (ACX) p.76

## Related Content
- [10K_GENERATION_REPORT]]
- [[ULTIMATE_VAULT_ACHIEVEMENT
- [NEXT_LEVEL_IMPROVEMENTS]]

## Game Mechanics
- **Combat**: See ACX p.189-198

## D&D 5e References

*(Combat rules: ACX p.189-198)*
*(Attack rolls: ACX p.194)*
*(Damage & Healing: ACX p.196-197)*
*(Spellcasting: ACX p.201-205)*
*(Spell slots: ACX p.201)*
*(Ritual casting: ACX p.201-202)*
*(Character creation: ACX p.11-15)*
*(Ability scores: ACX p.12-13)*
*(Backgrounds: ACX p.125-141)*
*(Exploration: WWT p.242-243)*
*(Travel pace: ACX p.182)*
*(Wilderness survival: WWT p.109-112)*

## Connections

- Parallels [[Personal_Horror_Customization (D&D_References)
- Affected by
- Requires [Amulet of Proof Against Detection and Location Xdmg]]
- Related: [[ENC00302_Combat_Encounter_303
- Originates from [LOC00215_Dungeons_Location_216]]
- Requires [[giant-centipede-xmm (beast)
- Requires [Manacles Xphb]]
- Influences [[step_082 (phase_018)
- See also: [ENC00062_Social_Encounter_63]]
- Leads to [[Leucrotta Mpmm
- Connects to
- Requires [Location City Miranda Hopekeeper Miranda Hopekeeper.svg]]
- Influences [[NPC0064_Yorick_Ironforge
- Parallels [Spell_Slots]]
- Compare with [[step_053 (phase_045)
- Leads to [DUN00170_Dungeon_171]]
- Affected by [[step_100 (phase_085)
- Requires [Magic Item Table H]]
- Leads to [[step_027 (phase_016)
- Requires [Assets Locations Location City Chief Engineer Nereus Flowstream Chief Engineer Nereus Flowstream.svg]]
- Requires [[ioun-stone-regeneration-xdmg (items)
- Related: [Grand Engineer Prism Masterwork]]
- Requires [[Strixhaven Pennant Scc
- Originates from [Assets Locations Location City the Azure Coast V1 the Azure Coast.svg]]
- See also: [[step_011 (phase_096)
- Related: [ITEM01174_Pure_Herb_of_Fortune]]
- Affected by [[ENC00030_Environmental_Encounter_31
- Related: [Assets Locations Location City Ancient Tunnels Beneath Palace V1 Ancient Tunnels Beneath Palace.svg]]
- Parallels [[step_010 (phase_088)
- Connects to [VAULT_CLEAN_STATUS]]
- Affected by [[step_024 (phase_037)
- See also: [Assets Locations Location City Pressure Portals Pressure Portals.svg]]
- Compare with [[Location City the Whispering Depths the Whispering Depths.svg
- Leads to [step_027 (phase_025)]]
- Connects to [[Quest - Shadow Citizenship Act
- Requires [EVENT00027_Magical_Event_28]]
- Related: [[LORE00155_Legends_Entry_156
- Originates from [ITEM01306_Elegant_Tool_Kit_of_Durability]]
- Influences [[Great Reconciliatio 2
- Influences [Ambassador Marina Depthbridge]]
- Compare with [[step_094 (phase_096)
- Requires [Audit Investigator Thomas Truthseeker (D&D_References)]]
- Originates from [[Sphinx of Lore Xmm
- Parallels [#Membership]]
- Parallels
- Influences [[LORE00167_Prophecies_Entry_168
- Parallels [The Unity Crystal]]
- Parallels
- See also: [[step_090 (phase_033)
- Influences [Current Riders Union 2]]
- Originates from [[Healer Tide-Touch
- Leads to [04_Resources_Assets_Locations_location-city-archdruid-marina-kelpweaver-archdruid-marina-kelpweaver.svg]]
- Originates from [[The Bleeding Chambers (D&D_References)
- Leads to [belt-of-hill-giant-strength-xdmg (items)]]
- Connects to [[Nightmarket Plaza 2
- Leads to [CLAUDE]]
- Parallels [[Temporal Magic Research (D&D_References)
- Leads to [step_033 (phase_062)]]
- Compare with [[LOC00008_Wilderness_Location_9
- Connects to [The Parliament of Shadows Campaign]]
- Requires [[QUEST00077_Personal_Quest_78
- Requires [step_089 (phase_039)]]
- Compare with [[Location City Archaeological Discoveries Archaeological Discoveries.svg
- Parallels [step_029 (phase_066)]]
- Affected by [[Quest - The Family Reunion
- Requires [life-events-by-age-xge (tables)]]
- Influences [[Crystal Festival Grounds
- Originates from [Surface Portal Alpha]]
- Connects to
- Parallels [[SPELL00024_Arcane_Spell_25
- Connects to
- Influences [Secular Community Practices]]
- Requires [[Assets Locations Location City Innkeeper Mara Ironlung V1 Innkeeper Mara Ironlung.svg
- Affected by [The Memory Meadows Black Market (D&D_References)]]
- Compare with [[Roper Xmm
- Originates from [step_033 (phase_070)]]
- Affected by [[NPC01744_Idris_Xendar_the_Mystic
- See also: [Location City Temple of the Deep Current Temple of the Deep Current.svg]]
- Leads to [[Trade Union 2
- Influences [Portrait NPC Militant Priest Abyssal Militant Priest Abyssal.svg]]
- Related:
- Parallels [[step_073 (phase_068)
- Requires [Jet Xdmg]]
- Originates from [[NPC00085_Pyria_Xendar_the_Seeker
- Originates from [His Eternal Majesty Keeper of the Throne of]]
- Compare with [[list-optfeaturetype-fs-b#Fighting%20Style,%20Bard
- Compare with [step_055 (phase_092)]]
- Compare with [[giant-crocodile-xmm
- Leads to [Emergency Life Support Research Foundation 2]]
- Affected by [[QUEST00071_Side_Quest_72
- Connects to
- Parallels [List Spells Classes Arcane Trickster Xphb]]
- Parallels [[step_005 (phase_022)
- Affected by [step_054 (phase_045)]]
- See also: [[step_042 (phase_085)
- See also: [Kelp Forest Monasteries (D&D_References)]]
- Affected by [[Relics Very Rare Xdmg
- Originates from [MON00023_Aberrations_Creature_24]]
- Affected by [[ENC00384_Combat_Encounter_385
- Parallels [QUEST00043_Side_Quest_44]]

## Visual References
![[03_People/portrait_assets_locations_location_city_quartermaster_sterling_suppystone_quartermaster_sterling_suppystone_svg_friendly.png
![03_People/token_00_indexes_master_index_medium_normal.png]]
![[03_People/portrait_assets_locations_location_city_deep_current_flowmaster_deep_current_flowmaster_svg_standard.png]]
