# CLAUDE.md - Persistent Memory for Obsidian TTRPG Vault

## 🚨 CRITICAL VAULT MANAGEMENT RULES (LEARNED 2025-08-15)

### ❌ NEVER DO THESE:

1. **NEVER REORGANIZE STRUCTURE WITHOUT PERMISSION**
   - Don't rename/move folders
   - Don't change hierarchy
   - "Reorganize" means organize files WITHIN folders, not restructure

2. **NEVER DELETE USER CONTENT**
   - Sessions stay in 06_Sessions
   - Campaigns stay in 01_Adventures/Campaigns
   - Encounters/hooks are sacred
   - Archive suspicious files, don't delete

3. **NEVER CREATE DUPLICATE DIRECTORIES**
   - Work with existing structure
   - Don't create 00_COMMAND_CENTER when 00_System exists
   - Check before creating any new root directory

4. **NEVER CREATE FILES FROM BROKEN LINKS**
   - Don't create .md files for [[broken links]]
   - Don't create step_XXX (phase_YYY).md files
   - Don't create .png.md or .svg.md files
   - Fix links by finding correct targets

5. **NEVER TRUST FILENAMES ALONE**
   - Check content before categorizing
   - Verify purpose before moving
   - Read the actual file

### ✅ ALWAYS DO THESE:

1. **ALWAYS ASK FIRST**
   - Before moving >10 files
   - Before creating directories
   - Before any structural changes

2. **ALWAYS BACKUP**
   - Use 08_Archive for removed files
   - Create recovery scripts
   - Document all changes

3. **ALWAYS TEST FIRST**
   - Run on small samples
   - Verify results
   - Count before/after

## 📁 Vault Structure (PERMANENT)

```
ObsidianTTRPGVault Experimental/
├── _INDEXES/          # Vault indexes
├── _METADATA/         # Vault metadata
├── _SCRIPTS/          # Python scripts (INCLUDING THIS RULES FILE)
├── 00_System/         # System files, templates
├── 01_Adventures/     # Campaigns, quests, encounters, hooks
├── 02_Worldbuilding/  # Locations, lore, factions
├── 03_People/         # NPCs and characters
├── 04_Resources/      # Assets, maps, handouts
├── 05_Rules/          # Game mechanics
├── 06_Sessions/       # Session notes (NEVER MOVE THESE)
├── 07_Player_Resources/
├── 08_Archive/        # Old/removed content (NOT ACTIVE)
└── 09_Performance/    # Reports only (NOT GAME CONTENT)
```

## 🎯 Patterns That Should NOT Exist

### Files to Remove on Sight:
- `*_03_Mechanics_CLI_bestiary_*.md` (outside proper location)
- `step_XXX (phase_YYY).md` (outside 09_Performance)
- `*.png.md`, `*.svg.md`, `*.json.md`
- Files with `(category)` in names
- Files starting with `#`, `$`, `%`, `<`
- Duplicate markers: `_1.md`, `_2.md`, `_Quick_Ref.md`

## 📝 Session History

### 2025-08-15: Major Improvement & Recovery
- **What Happened**:
  - Attempted 10,000+ improvements
  - Mistakenly reorganized structure (user wanted organization WITHIN folders)
  - Moved campaign/session content incorrectly
  - Created 10,000+ broken link files

- **What Was Fixed**:
  - Recovered campaign/session content
  - Removed 10,854 broken link files
  - Removed 6,042 path-pattern files
  - Created comprehensive rules to prevent recurrence

- **Lessons Learned**:
  - User's campaigns and sessions are sacred
  - "Reorganize" ≠ "restructure"
  - Always verify file content, not just names
  - Test operations on small samples first

## 🛠️ Available Recovery Scripts

Located in `_SCRIPTS/`:
- `EMERGENCY_RECOVERY.py` - Recovers moved campaign/session content
- `REMOVE_BROKEN_LINK_FILES.py` - Cleans broken link artifacts
- `intelligent_file_categorizer.py` - Categorizes based on content
- `comprehensive_link_integrator.py` - Links assets properly

## 🎲 Vault Purpose

This is a TTRPG (Tabletop RPG) vault for:
- D&D 5e campaigns (Aquabyssos, Aethermoor)
- Session management
- NPC tracking
- World building
- Player resources

Every operation should:
- Preserve campaign continuity
- Protect user content
- Maintain quick session access
- Enhance gameplay

## ⚠️ Pre-Operation Checklist

Before ANY major operation:
- [ ] Do I understand what user ACTUALLY wants?
- [ ] Will this preserve campaign/session content?
- [ ] Will this maintain existing structure?
- [ ] Have I created backup/recovery method?
- [ ] Have I tested on small sample?
- [ ] Will this create duplicate directories?
- [ ] Will this generate broken link files?

## 🚨 Emergency Procedures

If something goes wrong:
1. STOP immediately
2. Check 08_Archive for moved files
3. Run EMERGENCY_RECOVERY.py
4. Document what happened
5. Create specific recovery script
6. Apologize and explain

---

**THIS FILE MUST BE READ AT THE START OF EVERY SESSION**
**THESE RULES ARE MANDATORY**

Last Updated: 2025-08-15
Critical Session: Vault improvement with major errors and successful recovery
Total Files in Vault: 656,025 total / 51,911 markdown files
Glidepath Progress: 10/100 steps complete (Phase 1 done)