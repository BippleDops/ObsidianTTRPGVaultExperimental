# CRITICAL RULES FOR CLAUDE - VAULT MANAGEMENT

## ⚠️ NEVER DO THESE THINGS

### 1. **NEVER REORGANIZE WITHOUT EXPLICIT PERMISSION**
- ❌ NEVER rename folders
- ❌ NEVER move entire directory structures
- ❌ NEVER change the established folder hierarchy
- ❌ NEVER assume "reorganize" means "restructure"
- ✅ ONLY organize files WITHIN existing folders when asked

### 2. **NEVER DELETE CAMPAIGN/SESSION CONTENT**
- ❌ NEVER move sessions out of 06_Sessions
- ❌ NEVER move campaigns out of 01_Adventures/Campaigns
- ❌ NEVER treat user content as "duplicates"
- ❌ NEVER delete encounters, hooks, or adventure content
- ✅ ALWAYS preserve user-created game content

### 3. **NEVER CREATE DUPLICATE DIRECTORIES**
- ❌ NEVER create 00_COMMAND_CENTER when 00_System exists
- ❌ NEVER create new root directories without asking
- ❌ NEVER duplicate existing folder structures
- ✅ ALWAYS work with existing directories

### 4. **NEVER CREATE FILES FROM BROKEN LINKS**
- ❌ NEVER create .md files for broken [[Link]]
- ❌ NEVER create files like "step_001 (phase_092).md"
- ❌ NEVER create files with path patterns in names
- ❌ NEVER create .png.md or .svg.md files
- ✅ ONLY fix links by finding the correct target

### 5. **NEVER TRUST FILE NAMES ALONE**
- ❌ NEVER assume a file's category from its name
- ❌ NEVER move files based solely on filename patterns
- ✅ ALWAYS check file content before categorizing
- ✅ ALWAYS verify a file's purpose before moving

## ✅ ALWAYS DO THESE THINGS

### 1. **ALWAYS ASK BEFORE MAJOR CHANGES**
- ✅ Ask before moving more than 10 files
- ✅ Ask before creating new directories
- ✅ Ask before deleting any user content
- ✅ Ask before restructuring anything

### 2. **ALWAYS CREATE BACKUPS**
- ✅ Move files to 08_Archive instead of deleting
- ✅ Create recovery scripts for risky operations
- ✅ Document what was moved/changed
- ✅ Provide clear recovery paths

### 3. **ALWAYS PRESERVE STRUCTURE**
- ✅ Keep the numbered folder system (00-09)
- ✅ Maintain established hierarchies
- ✅ Respect special folders (_SCRIPTS, _INDEXES)
- ✅ Understand 08=Archive, 09=Performance (not content)

### 4. **ALWAYS VALIDATE OPERATIONS**
- ✅ Test scripts on small samples first
- ✅ Check results after each operation
- ✅ Verify files ended up where intended
- ✅ Count files before and after operations

### 5. **ALWAYS UNDERSTAND CONTEXT**
- ✅ Read file content, not just names
- ✅ Understand user's actual request
- ✅ Consider campaign/game context
- ✅ Respect the TTRPG vault purpose

## 🎯 SPECIFIC PATTERNS TO AVOID

### Files That Should NEVER Exist:
1. `*_03_Mechanics_CLI_bestiary_*.md` (outside proper locations)
2. `step_XXX (phase_YYY).md`
3. `*.png.md`, `*.svg.md`, `*.json.md`
4. Files with `(D&D_References)` or `(category)` in names
5. Files starting with `#`, `$`, `%`, `<`
6. Multiple versions: `_1.md`, `_2.md`, `_Quick_Ref.md`
7. Path patterns: `04_Resources_Assets_*` in filenames

### Operations That Need Confirmation:
1. Moving any session files
2. Moving any campaign files
3. Deleting more than 10 files
4. Creating new root directories
5. Renaming existing directories
6. Bulk file movements (>100 files)

## 📋 CHECKLIST BEFORE RUNNING SCRIPTS

- [ ] Did I understand what the user ACTUALLY wants?
- [ ] Will this preserve their campaign/session content?
- [ ] Will this maintain the existing structure?
- [ ] Have I created a backup/recovery method?
- [ ] Have I tested on a small sample first?
- [ ] Will this create any duplicate directories?
- [ ] Will this generate files from broken links?
- [ ] Did I check file contents, not just names?

## 🚨 EMERGENCY PROCEDURES

### If Something Goes Wrong:
1. STOP immediately
2. Document what happened
3. Create recovery script
4. Check 08_Archive for moved files
5. Restore from backup if available
6. Apologize and explain clearly

### Recovery Locations:
- `08_Archive/duplicates/` - Files marked as duplicates
- `08_Archive/removed_broken_links/` - Removed broken files
- `09_Performance/reports/` - Operation reports
- `_SCRIPTS/EMERGENCY_RECOVERY.py` - Recovery script

## 📝 LESSONS FROM THIS SESSION

1. **"Reorganize" ≠ "Restructure"** - User wanted files organized WITHIN folders, not folders renamed
2. **Campaigns are Sacred** - Never move campaign/session content without explicit permission
3. **Duplicates Need Verification** - Not all similar files are duplicates
4. **Broken Links Don't Need Files** - Don't create .md files for every [[broken link]]
5. **Test First, Execute Second** - Always test operations on small samples
6. **Archive, Don't Delete** - Move questionable files to archive for recovery

## 🎲 REMEMBER: THIS IS A TTRPG VAULT

The purpose is to support tabletop roleplaying games. Every decision should:
- Enhance the gaming experience
- Preserve campaign continuity
- Protect user-created content
- Maintain quick access during sessions
- Support both planning and play

---

**THESE RULES ARE MANDATORY FOR ALL FUTURE OPERATIONS**

Last Updated: 2025-08-15
Session: Major vault improvement with critical errors and recovery