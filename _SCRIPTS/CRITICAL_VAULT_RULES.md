# 🚨 CRITICAL VAULT MANAGEMENT RULES

**Created**: 2025-08-15
**Purpose**: Prevent catastrophic vault damage
**Status**: MANDATORY - NEVER VIOLATE THESE RULES

---

## ⚠️ THE 10 COMMANDMENTS OF VAULT MANAGEMENT

### 1. ❌ NEVER reorganize structure without permission
- DO NOT rename folders
- DO NOT move directory structures
- DO NOT change folder hierarchy
- ONLY organize files WITHIN existing folders

### 2. ❌ NEVER delete campaign/session content
- Campaigns in `01_Adventures/Campaigns` are SACRED
- Sessions in `06_Sessions` are SACRED
- Aquabyssos content is PROTECTED
- Aethermoor content is PROTECTED
- When in doubt, ARCHIVE don't DELETE

### 3. ❌ NEVER create duplicate directories
- Check if directory exists BEFORE creating
- Work WITH existing structure
- Don't create parallel hierarchies
- One folder per purpose

### 4. ❌ NEVER create files from broken links
- Broken [[Link]] should be FIXED not CREATED
- Don't generate .md files for missing targets
- Don't create step_XXX or phase_XXX files
- Don't create .png.md or .json.md files

### 5. ✅ ALWAYS check content, not just filenames
- READ file content before categorizing
- Verify purpose before moving
- Check file size and substance
- Don't trust names alone

### 6. ✅ ALWAYS create backups before major operations
- Backup critical content first
- Create recovery scripts
- Document what was changed
- Test restoration process

### 7. ✅ ALWAYS preserve existing structure
- Keep numbered folders (00-09)
- Maintain established hierarchies
- Respect special folders (_SCRIPTS, _INDEXES)
- Understand: 08=Archive, 09=Performance

### 8. ✅ ALWAYS validate operations
- Test on 5-10 files first
- Check results after each step
- Verify files ended up correctly
- Count before and after

### 9. ✅ ALWAYS understand context
- This is a TTRPG vault for gaming
- Campaigns and sessions are gameplay records
- NPCs, locations, quests are game content
- Everything serves the game

### 10. ✅ ALWAYS test on small samples first
- Run on 5 files before 5000
- Check output before full execution
- Verify logic is correct
- Stop if anything seems wrong

---

## 📋 PREFLIGHT CHECKLIST

Before ANY script execution:

- [ ] Do I understand what the user ACTUALLY wants?
- [ ] Will this preserve campaign/session content?
- [ ] Will this maintain existing structure?
- [ ] Have I created a backup/recovery method?
- [ ] Have I tested on a small sample?
- [ ] Am I creating any duplicate directories?
- [ ] Am I generating files from broken links?
- [ ] Did I check file contents, not just names?

---

## 🚫 PATTERNS TO NEVER CREATE

### Files that should NEVER exist:
- `*_03_Mechanics_CLI_bestiary_*.md` (scattered)
- `step_XXX (phase_YYY).md`
- `*.png.md`, `*.svg.md`, `*.json.md`
- Files with `(D&D_References)` in names
- Files starting with `#`, `$`, `%`, `<`
- Multiple versions: `_1.md`, `_2.md`, `_Quick_Ref.md`

### Operations that NEED permission:
- Moving ANY session files
- Moving ANY campaign files
- Deleting more than 10 files
- Creating new root directories
- Renaming existing directories
- Bulk movements (>100 files)

---

## 🛡️ PROTECTED ZONES

### NEVER modify without explicit permission:
1. `01_Adventures/Campaigns/` - User's campaigns
2. `06_Sessions/` - Game session records
3. `*/Aquabyssos/*` - Aquabyssos campaign
4. `*/Aethermoor/*` - Aethermoor campaign
5. Character sheets
6. Player notes

---

## 🔄 RECOVERY PROCEDURES

### If something goes wrong:
1. **STOP** immediately
2. **Document** what happened
3. **Create** recovery script
4. **Check** `08_Archive/` for moved files
5. **Restore** from backup if available
6. **Apologize** and explain clearly
7. **Learn** and update these rules

### Standard recovery locations:
- `08_Archive/duplicates/` - Suspected duplicates
- `08_Archive/broken_references/` - Broken link files
- `08_Archive/test_files/` - Test/temp files
- `09_Performance/backups/` - Full backups

---

## 💡 GOLDEN PRINCIPLES

1. **Preservation over Perfection** - Better messy than missing
2. **Archive over Delete** - Can always recover archived
3. **Test before Execute** - Small samples prevent disasters
4. **Structure is Sacred** - Don't reorganize without permission
5. **Content is King** - User's content > organizational beauty

---

## 📝 LESSONS LEARNED

1. **"Reorganize"** means organize WITHIN, not restructure
2. **Campaigns/Sessions** are the heart of the vault
3. **Duplicates** need content verification, not name matching
4. **Broken links** need fixing, not file creation
5. **Testing** prevents disasters

---

## ⚡ QUICK REFERENCE

### Safe Operations:
- ✅ Enhance content within files
- ✅ Add tags and metadata
- ✅ Create indexes and summaries
- ✅ Fix typos and formatting
- ✅ Archive obvious junk

### Dangerous Operations:
- ⚠️ Moving files between directories
- ⚠️ Renaming folders
- ⚠️ Deleting anything
- ⚠️ Creating new structure
- ⚠️ Bulk operations

---

## 🎯 REMEMBER THE PURPOSE

This is a **TTRPG Vault** for:
- Running game sessions
- Managing campaigns
- Tracking characters
- Building worlds
- Having fun

Every action should **enhance the gaming experience**, not disrupt it.

---

**THESE RULES ARE MANDATORY**
**VIOLATING THEM CAUSES VAULT DAMAGE**
**WHEN IN DOUBT, ASK FIRST**

---

*Last Updated: 2025-08-15*
*Status: ACTIVE AND ENFORCED*
*Priority: MAXIMUM*