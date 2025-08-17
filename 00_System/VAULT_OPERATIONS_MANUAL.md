---
id: SYS0000
status: active
domain: resource
type: asset
canonical: true
critical: true
version: 1.0
created: 2025-08-17
---

# 📚 VAULT OPERATIONS MANUAL
*The Complete Guide to Your Obsidian TTRPG Vault*

> **IMPORTANT**: This is the master operations manual. Read this first before making any structural changes. Share this with any AI assistants working on the vault.

## 🎯 Quick Start for Daily Use

### Your Primary Workflows

#### 1. During Game Session
```bash
# Switch to Active Play profile
./_SCRIPTS/switch_profile.sh  # Choose option 1

# Open GM Dashboard
Navigate to: 00_System/GM_Resources/00_GM_DASHBOARD.md

# Quick capture ideas
Hotkey: Cmd+Shift+Q
```

#### 2. Between Sessions (Prep)
```bash
# Use Library profile for full access
./_SCRIPTS/switch_profile.sh  # Choose option 2

# Process inbox
Check: 00_System/Quick_Capture_Inbox/

# Run maintenance
python3 _SCRIPTS/vault_hygiene_audit.py
```

#### 3. End of Day
```bash
# Sync changes
./_SCRIPTS/git_sync.sh

# Optional: Run full maintenance
./_SCRIPTS/run_nightly_jobs.sh
```

## 🏗️ Vault Architecture

### Directory Structure (PERMANENT - DO NOT CHANGE)
```
ObsidianTTRPGVaultExperimental/
├── 00_System/           # ⚙️ System files, templates, config
├── 01_Adventures/       # ⚔️ Campaigns, quests, encounters
├── 02_Worldbuilding/    # 🌍 Locations, lore, factions  
├── 03_People/          # 👥 NPCs and characters
├── 04_Resources/       # 🗺️ Maps, handouts, assets
├── 05_Rules/           # 📖 Game mechanics, homebrew
├── 06_Sessions/        # 📝 Session notes (NEVER MOVE)
├── 07_Player_Resources/# 🎮 Player-accessible content
├── 08_Archive/         # 📦 Archived content
├── 09_Performance/     # 📊 Metrics and reports
├── _INDEXES/           # 📑 Dynamic vault indexes
├── _METADATA/          # 🔧 Vault metadata and logs
└── _SCRIPTS/           # 🤖 Automation scripts
```

### Critical Rules (LEARNED FROM EXPERIENCE)
1. **NEVER** reorganize the top-level structure
2. **NEVER** delete user content (archive instead)
3. **NEVER** move sessions from 06_Sessions
4. **NEVER** create duplicate directories
5. **ALWAYS** backup before bulk operations
6. **ALWAYS** test with --dry-run first

## 📋 Frontmatter Syntax

### Required Fields (ALL files must have these)
```yaml
---
id: XXX####          # Unique ID (see ID prefix table)
status: [status]     # Lifecycle status
domain: [domain]     # Content domain
type: [type]        # Entity type
canonical: true/false # Is this the authoritative version?
---
```

### Status Values
- `seed` - Initial idea, minimal content
- `draft` - Being written, incomplete  
- `in-progress` - Actively being developed
- `ready` - Complete and reviewed
- `active` - Currently in use during play
- `deprecated` - No longer used but kept
- `archived` - Moved to archive folder

### Domain Values
- `adventure` - Campaigns, quests, encounters
- `world` - Locations, lore, factions
- `people` - NPCs, PCs, notable figures
- `rules` - Mechanics, homebrew, references
- `session` - Session notes and prep
- `resource` - Maps, handouts, assets

### ID Prefix System
| Prefix | Type | Example | Next Available |
|--------|------|---------|----------------|
| LOC | Location | LOC0001 | Check with script |
| NPC | NPC | NPC0042 | Check with script |
| FAC | Faction | FAC0003 | Check with script |
| QST | Quest | QST0007 | Check with script |
| ITM | Item | ITM0234 | Check with script |
| SES | Session | SES0089 | Check with script |
| MAP | Map | MAP0156 | Check with script |
| CAM | Campaign | CAM0002 | Check with script |

### Complete Example
```yaml
---
id: NPC0042
status: active
domain: people
type: npc
canonical: true
campaign: Aquabyssos
created: 2025-01-15
modified: 2025-08-17
aliases:
  - "The Shadow Broker"
  - "Whisper"
tags:
  - recurring
  - quest-giver
  - merchant
location: Waterdeep
faction: Harpers
race: Tiefling
class: Rogue
alignment: CN
---
```

## 🤖 Instructions for AI Assistants

### When Asked to Help with This Vault

1. **READ FIRST**:
   - This manual (00_System/VAULT_OPERATIONS_MANUAL.md)
   - CLAUDE.md rules in vault root
   - Recent entries in _METADATA/

2. **BEFORE ANY OPERATION**:
   ```python
   # Always run this first
   python3 _SCRIPTS/vault_hygiene_audit.py
   ```

3. **USE THESE SCRIPTS** (never recreate):
   - `vault_hygiene_audit.py` - Check vault health
   - `normalize_names.py` - Fix file naming
   - `lifecycle_enforcer.py` - Add/fix frontmatter
   - `anomalous_cleanup.py` - Remove problem files
   - `campaign_freezer.py` - Archive campaigns

4. **COMMON TASKS**:
   ```bash
   # Add missing frontmatter
   python3 _SCRIPTS/lifecycle_enforcer.py --frontmatter-only
   
   # Find broken links
   python3 _SCRIPTS/vault_hygiene_audit.py | grep "broken_links"
   
   # Archive old content
   python3 _SCRIPTS/lifecycle_enforcer.py --archive-only
   
   # Clean up weird files
   python3 _SCRIPTS/anomalous_cleanup.py --preview
   ```

### Patterns to NEVER Create
```markdown
# NEVER create these file patterns:
step_001 (phase_002).md
[anything].png.md
#broken-link.md
duplicate_name_1.md
"quoted filename".md
```

### Safe File Creation Template
```python
# When creating new files programmatically:
def create_safe_file(title, type, domain):
    # Get next ID
    id = get_next_id(type)  # e.g., "NPC0043"
    
    # Clean filename
    safe_name = title.replace("'", "").replace('"', "")
    safe_name = re.sub(r'[<>:"/\\|?*]', '-', safe_name)
    
    # Create with frontmatter
    filename = f"{id} - {safe_name}.md"
    content = f"""---
id: {id}
status: draft
domain: {domain}
type: {type}
canonical: true
created: {datetime.now():%Y-%m-%d}
---

# {title}

"""
    return filename, content
```

## 🔄 Standard Workflows

### New Content Creation Workflow
```mermaid
graph LR
    A[Idea] --> B[Quick Capture<br/>Cmd+Shift+Q]
    B --> C[Inbox]
    C --> D[Process & Expand]
    D --> E[Add Full Frontmatter]
    E --> F[Move to Correct Folder]
    F --> G[Link from Index]
```

### Session Prep Workflow
1. Review GM Dashboard for "Needs Attention"
2. Process Quick Capture Inbox
3. Update active quests/NPCs
4. Generate session outline
5. Prepare maps/handouts
6. Run `python3 _SCRIPTS/vault_hygiene_audit.py`

### Post-Session Workflow
1. Create session notes in `06_Sessions/`
2. Update NPC statuses
3. Progress quest states
4. Quick capture new ideas
5. Update campaign timeline
6. Commit to Git

### Weekly Maintenance
```bash
#!/bin/bash
# Run every Sunday

# 1. Clean up
python3 _SCRIPTS/anomalous_cleanup.py --execute --dry-run
python3 _SCRIPTS/resolve_conflicts.py

# 2. Organize
python3 _SCRIPTS/normalize_names.py --preview
python3 _SCRIPTS/lifecycle_enforcer.py --dry-run

# 3. Archive
python3 _SCRIPTS/lifecycle_enforcer.py --archive-only

# 4. Report
python3 _SCRIPTS/vault_hygiene_audit.py
python3 _SCRIPTS/rebuild_indexes.py

# 5. Backup
./_SCRIPTS/git_sync.sh
```

## 🗺️ Navigating the Connected Vault

### Primary Entry Points

#### For Game Sessions
1. **GM Dashboard** (`00_System/GM_Resources/00_GM_DASHBOARD.md`)
   - Real-time status of all active content
   - Quick links to current campaign materials
   - "Needs attention" panels

#### For World Building
1. **Master Index** (`_INDEXES/INDEX_Master.md`)
   - Complete vault statistics
   - Links to all specialized indexes
   
2. **Specialized Indexes**:
   - `INDEX_Locations.md` - All locations by campaign/biome
   - `INDEX_NPCs.md` - NPCs by faction/location
   - `INDEX_Quests.md` - Active/available quests

#### For Maintenance
1. **Hygiene Report** (`_METADATA/hygiene_report.md`)
   - Latest vault health check
   - Issues to address
   
2. **Archive Index** (`08_Archive/README.md`)
   - What's been archived
   - Recovery instructions

### Navigation Patterns

#### Follow the Campaign Thread
```
Campaign Hub (01_Adventures/Campaigns/[Name]/)
    ├→ Current Session (06_Sessions/[Latest])
    ├→ Active Quests (via Dataview)
    ├→ Party Location (02_Worldbuilding/[Current])
    ├→ Local NPCs (03_People/[Filtered])
    └→ Available Resources (04_Resources/[Tagged])
```

#### Follow the Location Thread
```
Location (02_Worldbuilding/[Location])
    ├→ Parent Location (via frontmatter)
    ├→ Child Locations (via backlinks)
    ├→ Local NPCs (via location field)
    ├→ Related Quests (via Dataview)
    └→ Maps (04_Resources/Maps/[Location])
```

#### Follow the NPC Thread
```
NPC (03_People/[Name])
    ├→ Faction (via frontmatter)
    ├→ Location (via frontmatter)
    ├→ Relationships (via links)
    ├→ Quest Given (via quest_giver field)
    └→ Session Appearances (via backlinks)
```

### Smart Searches

#### Using Dataview Queries
```dataview
// Find all active content for Aquabyssos
FROM "" 
WHERE campaign = "Aquabyssos" AND status = "active"

// Find orphaned NPCs
FROM "03_People"
WHERE !location OR !faction

// Find recent changes
FROM ""
WHERE (date(today) - date(modified)).days <= 7

// Find everything about Waterdeep
FROM ""
WHERE contains(file.name, "Waterdeep") 
   OR contains(location, "Waterdeep")
   OR contains(parent_location, "Waterdeep")
```

#### Using Obsidian Search
```
// Status-based searches
status:active
status:draft
status:archived

// Type-based searches  
type:npc
type:location
type:quest

// Campaign-specific
campaign:Aquabyssos
campaign:Aethermoor

// Combination searches
status:active type:quest campaign:Aquabyssos
```

## 🛠️ Troubleshooting Guide

### Common Issues & Solutions

#### "Vault is slow"
```bash
# 1. Switch to Active Play profile
./_SCRIPTS/switch_profile.sh

# 2. Clean up large files
find 04_Resources -size +8M -type f

# 3. Archive old content
python3 _SCRIPTS/lifecycle_enforcer.py --archive-only
```

#### "Can't find content"
```bash
# 1. Rebuild indexes
python3 _SCRIPTS/rebuild_indexes.py

# 2. Check archive
ls 08_Archive/by_domain/

# 3. Search by ID
grep -r "NPC0042" . --include="*.md"
```

#### "Broken links everywhere"
```bash
# 1. Find broken links
python3 _SCRIPTS/vault_hygiene_audit.py

# 2. Fix naming
python3 _SCRIPTS/normalize_names.py --apply

# 3. Update links
# Manual review required
```

#### "Sync conflicts"
```bash
# Automatic resolution
python3 _SCRIPTS/resolve_conflicts.py --strategy newest
```

## 📊 Key Metrics to Monitor

### Daily
- Active quest count
- Unprocessed inbox items
- Orphaned files created

### Weekly  
- Total file count
- Archive growth
- Broken link count

### Monthly
- Media folder size
- Campaign progress
- System performance

## 🚀 Advanced Operations

### Bulk Operations Safety Protocol
```bash
# ALWAYS follow this sequence:
1. Backup
   cp -r . ../vault_backup_$(date +%Y%m%d)

2. Dry run
   python3 [script].py --dry-run > preview.txt

3. Review
   less preview.txt

4. Execute
   python3 [script].py --execute

5. Verify
   python3 _SCRIPTS/vault_hygiene_audit.py
```

### Creating New Automation
```python
# Template for new scripts
#!/usr/bin/env python3
"""
Script purpose and description
"""

from pathlib import Path
import yaml
import argparse

class VaultProcessor:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        
    def process(self, dry_run: bool = True):
        # ALWAYS have dry_run mode
        if dry_run:
            print("DRY RUN - No changes")
        
        # Process files
        for file in self.vault_path.rglob("*.md"):
            # Skip system files
            if any(skip in str(file) for skip in 
                   ['.obsidian', '08_Archive', '_SCRIPTS']):
                continue
            
            # Your logic here
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    processor = VaultProcessor(vault_path)
    processor.process(dry_run=args.dry_run)
```

## 📚 Appendix: Complete Command Reference

### Quick Commands
```bash
# Maintenance
python3 _SCRIPTS/vault_hygiene_audit.py         # Health check
python3 _SCRIPTS/lifecycle_enforcer.py --dry-run # Fix frontmatter
python3 _SCRIPTS/anomalous_cleanup.py --preview  # Find weird files
python3 _SCRIPTS/rebuild_indexes.py              # Refresh indexes

# Organization  
python3 _SCRIPTS/normalize_names.py --preview    # Fix names
python3 _SCRIPTS/resolve_conflicts.py            # Fix conflicts
python3 _SCRIPTS/campaign_freezer.py [name]      # Archive campaign

# Git Operations
./_SCRIPTS/git_sync.sh                          # Sync to Git
git status                                       # Check changes
git log --oneline -10                          # Recent commits

# Profile Switching
./_SCRIPTS/switch_profile.sh                    # Interactive switch
ln -sf .obsidian-active-play .obsidian         # Quick play mode
ln -sf .obsidian-library .obsidian             # Quick library mode

# Finding Things
find . -name "*NPC*" -type f                   # Find by name
grep -r "Waterdeep" . --include="*.md"         # Search content
find . -mtime -7 -name "*.md"                  # Recent files

# Checking Size
du -sh 04_Resources/Maps                       # Folder size
find . -size +8M -type f                       # Large files
df -h .                                         # Disk space
```

### Emergency Procedures
```bash
# PANIC BUTTON - Restore from backup
cp -r ../vault_backup_[date]/* .

# Remove all broken link files
python3 -c "
import os
for root, dirs, files in os.walk('.'):
    for f in files:
        if '[' in f or ']' in f:
            print(f'Removing {f}')
            os.remove(os.path.join(root, f))
"

# Reset all frontmatter
python3 _SCRIPTS/lifecycle_enforcer.py --frontmatter-only

# Archive everything old
find . -mtime +180 -name "*.md" -exec python3 -c "
import sys
# Archive logic here
" {} \;
```

## 🎯 Remember: The Prime Directives

1. **Preserve User Content** - Never delete, always archive
2. **Maintain Structure** - The folder hierarchy is sacred
3. **Test First** - Always dry-run before execution
4. **Document Changes** - Log what you do
5. **Respect the Campaign** - Sessions and campaigns are the heart

## 📝 Version History

- **v1.0** (2025-08-17): Initial comprehensive setup by Claude Opus 4.1
  - Implemented 16-point optimization plan
  - Created all automation scripts
  - Established organizational principles

## 🆘 Getting Help

1. **Check this manual first**
2. **Run hygiene audit** for diagnostics
3. **Review _METADATA/** for logs
4. **Share this manual** with any AI assistant
5. **Backup before experiments**

---

*This manual is the authoritative guide for vault operations. Keep it updated as the vault evolves.*

**Remember:** This vault contains your creative work and gaming memories. Treat it with care, maintain it regularly, and it will serve you well through many adventures.

🎲 *May your rolls be high and your vault organized!*