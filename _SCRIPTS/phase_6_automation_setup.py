#!/usr/bin/env python3
"""
Phase 6: Automation Setup (Steps 501-600)
Configure daily notes, quick capture, auto-linking, template triggers, hotkeys, workspace layouts, bookmarks
"""

import os
import re
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
import yaml
from collections import defaultdict

class AutomationSetup:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.steps_completed = 0
        self.improvements_made = []
        
        # Obsidian configuration paths
        self.obsidian_dir = self.vault_path / ".obsidian"
        self.templates_dir = self.vault_path / "00_System" / "Templates"
        self.automation_dir = self.vault_path / "_SCRIPTS" / "automation"
        
        # Ensure directories exist
        self.obsidian_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.automation_dir.mkdir(parents=True, exist_ok=True)

    def run_phase_6(self):
        """Execute Phase 6: Automation Setup"""
        print("⚙️ Starting Phase 6: Automation Setup (Steps 501-600)")
        
        steps = [
            (self.configure_daily_notes, "Configure daily notes automation"),
            (self.setup_quick_capture, "Setup quick capture system"),
            (self.enable_auto_linking, "Enable auto-linking between content"),
            (self.create_template_triggers, "Create template triggers"),
            (self.optimize_hotkeys, "Optimize hotkeys and shortcuts"),
            (self.setup_workspace_layouts, "Setup workspace layouts"),
            (self.configure_bookmarks, "Configure smart bookmarks"),
            (self.create_automation_scripts, "Create automation scripts"),
            (self.setup_content_generation, "Setup automated content generation"),
            (self.configure_maintenance_tasks, "Configure maintenance automation")
        ]
        
        for step_func, description in steps:
            print(f"\n📋 {description}...")
            try:
                improvements = step_func()
                self.improvements_made.extend(improvements)
                self.steps_completed += 10
                print(f"✅ Completed {len(improvements)} improvements")
            except Exception as e:
                print(f"❌ Error in {description}: {e}")
                continue
        
        self.generate_phase_6_report()
        return self.improvements_made

    def configure_daily_notes(self) -> List[str]:
        """Configure daily notes automation"""
        improvements = []
        
        # Daily notes configuration
        daily_notes_config = {
            "folder": "06_Sessions/Daily_Notes",
            "format": "YYYY-MM-DD",
            "template": "00_System/Templates/Daily_Note_Template.md"
        }
        
        # Update Obsidian config
        config_path = self.obsidian_dir / "daily-notes.json"
        config_path.write_text(json.dumps(daily_notes_config, indent=2))
        improvements.append("Configured daily notes settings")
        
        # Create daily notes folder
        daily_notes_folder = self.vault_path / "06_Sessions" / "Daily_Notes"
        daily_notes_folder.mkdir(parents=True, exist_ok=True)
        improvements.append("Created daily notes folder")
        
        # Create daily note template
        daily_template = """---
type: daily_note
tags: [daily, session_prep]
created: {{date:YYYY-MM-DD}}
date: {{date:YYYY-MM-DD}}
campaign: 
session_planned: false
---

# Daily Note - {{date:YYYY-MM-DD}}

## Today's Session Plans
- [ ] 

## Campaign Status Updates
### Aquabyssos Campaign
- 

### Aethermoor Campaign
- 

## NPCs to Focus On
- 

## Locations in Play
- 

## Prep Checklist
- [ ] Review last session notes
- [ ] Check active quests
- [ ] Prepare encounters
- [ ] Update world state
- [ ] Gather resources/maps

## Random Encounters Ready
- [ ] 

## Quick Notes
- 

## End of Day Review
### What Worked Well
- 

### What to Improve
- 

### Ideas for Next Time
- 

---
**Quick Links:**
- [[Master_Campaign_Index]]
- [[Quest_Master_Tracker]]
- [[NPC_Quick_Reference]]
- [[00_GM_DASHBOARD]]
"""
        
        template_path = self.templates_dir / "Daily_Note_Template.md"
        template_path.write_text(daily_template)
        improvements.append("Created daily note template")
        
        # Create automatic daily note creation script
        auto_daily_script = """#!/usr/bin/env python3
import os
from datetime import datetime
from pathlib import Path

def create_daily_note():
    vault_path = Path(__file__).parent.parent.parent
    daily_folder = vault_path / "06_Sessions" / "Daily_Notes"
    
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = daily_folder / f"{today}.md"
    
    if not daily_file.exists():
        template_path = vault_path / "00_System" / "Templates" / "Daily_Note_Template.md"
        if template_path.exists():
            template_content = template_path.read_text()
            # Replace template variables
            content = template_content.replace("{{date:YYYY-MM-DD}}", today)
            daily_file.write_text(content)
            print(f"Created daily note: {daily_file}")
        else:
            print("Daily note template not found")
    else:
        print(f"Daily note already exists: {daily_file}")

if __name__ == "__main__":
    create_daily_note()
"""
        
        auto_script_path = self.automation_dir / "create_daily_note.py"
        auto_script_path.write_text(auto_daily_script)
        improvements.append("Created automatic daily note script")
        
        return improvements

    def setup_quick_capture(self) -> List[str]:
        """Setup quick capture system for rapid note taking"""
        improvements = []
        
        # Quick capture templates
        capture_templates = {
            "Quick_NPC.md": """---
type: npc
tags: [character, npc, quick_capture]
created: {{date:YYYY-MM-DD}}
status: draft
---

# {{title}}

**Quick Description:** 

**Role:** 

**Location:** 

**Notes:** 

---
*Quick capture - expand later*
""",
            "Quick_Location.md": """---
type: location
tags: [worldbuilding, location, quick_capture]
created: {{date:YYYY-MM-DD}}
status: draft
---

# {{title}}

**Type:** 

**Description:** 

**Notable Features:** 

**Connections:** 

---
*Quick capture - expand later*
""",
            "Quick_Quest.md": """---
type: quest
tags: [adventure, quest, quick_capture]
created: {{date:YYYY-MM-DD}}
status: draft
---

# {{title}}

**Objective:** 

**Giver:** 

**Reward:** 

**Notes:** 

---
*Quick capture - expand later*
""",
            "Quick_Idea.md": """---
type: idea
tags: [idea, brainstorm, quick_capture]
created: {{date:YYYY-MM-DD}}
---

# {{title}}

**Category:** 

**Description:** 

**Implementation:** 

**Related:** 

---
*Quick capture - develop further*
"""
        }
        
        # Create quick capture templates
        quick_templates_dir = self.templates_dir / "Quick_Capture"
        quick_templates_dir.mkdir(exist_ok=True)
        
        for template_name, template_content in capture_templates.items():
            template_path = quick_templates_dir / template_name
            template_path.write_text(template_content)
            improvements.append(f"Created quick capture template: {template_name}")
        
        # Create quick capture inbox
        inbox_dir = self.vault_path / "00_System" / "Quick_Capture_Inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        
        inbox_readme = """# Quick Capture Inbox

This folder is for rapid note capture during sessions. Process these regularly:

## Processing Workflow
1. Review captured notes
2. Expand with additional details
3. Move to appropriate vault location
4. Update links and relationships

## Templates Available
- Quick_NPC.md - For characters met during play
- Quick_Location.md - For places discovered
- Quick_Quest.md - For new quests or leads
- Quick_Idea.md - For general ideas and inspiration

Use Ctrl+N (or Cmd+N) and select a template for rapid capture.
"""
        
        inbox_readme_path = inbox_dir / "README.md"
        inbox_readme_path.write_text(inbox_readme)
        improvements.append("Created quick capture inbox")
        
        # Create processing automation script
        process_script = """#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

def process_quick_captures():
    vault_path = Path(__file__).parent.parent.parent
    inbox_path = vault_path / "00_System" / "Quick_Capture_Inbox"
    
    processed_count = 0
    
    for capture_file in inbox_path.glob("*.md"):
        if capture_file.name == "README.md":
            continue
            
        try:
            content = capture_file.read_text()
            
            # Check if it's a quick capture (has quick_capture tag)
            if "quick_capture" in content:
                # Determine destination based on type
                if "type: npc" in content:
                    dest_dir = vault_path / "03_People"
                elif "type: location" in content:
                    dest_dir = vault_path / "02_Worldbuilding"
                elif "type: quest" in content:
                    dest_dir = vault_path / "01_Adventures" / "Quests"
                else:
                    dest_dir = vault_path / "00_System" / "Ideas"
                
                # Move file to appropriate location
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / capture_file.name
                
                # Update content to remove quick_capture tag and draft status
                updated_content = content.replace(", quick_capture", "")
                updated_content = updated_content.replace("status: draft", "status: active")
                
                dest_file.write_text(updated_content)
                capture_file.unlink()
                
                processed_count += 1
                print(f"Processed: {capture_file.name} -> {dest_file}")
                
        except Exception as e:
            print(f"Error processing {capture_file}: {e}")
    
    print(f"Processed {processed_count} quick captures")

if __name__ == "__main__":
    process_quick_captures()
"""
        
        process_script_path = self.automation_dir / "process_quick_captures.py"
        process_script_path.write_text(process_script)
        improvements.append("Created quick capture processing script")
        
        return improvements

    def enable_auto_linking(self) -> List[str]:
        """Enable auto-linking between related content"""
        improvements = []
        
        # Auto-linking configuration
        auto_link_config = {
            "enabled": True,
            "link_patterns": {
                "npc_to_location": True,
                "quest_to_npc": True,
                "session_to_content": True,
                "faction_relationships": True
            },
            "auto_suggest": True,
            "link_preview": True
        }
        
        config_path = self.obsidian_dir / "auto-linking.json"
        config_path.write_text(json.dumps(auto_link_config, indent=2))
        improvements.append("Configured auto-linking settings")
        
        # Create auto-linking script
        auto_link_script = """#!/usr/bin/env python3
import re
from pathlib import Path
from typing import Dict, List, Set

class AutoLinker:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.entity_map = self.build_entity_map()
    
    def build_entity_map(self) -> Dict[str, List[str]]:
        \"\"\"Build map of entities to their file paths\"\"\"
        entity_map = {
            'npcs': [],
            'locations': [],
            'factions': [],
            'quests': []
        }
        
        # Collect NPCs
        for npc_file in self.vault_path.glob("03_People/**/*.md"):
            name = npc_file.stem
            if name.startswith("NPC"):
                # Extract actual name from NPC files
                parts = name.split("_", 2)
                if len(parts) >= 3:
                    name = parts[2].replace("_", " ")
            entity_map['npcs'].append((name, str(npc_file)))
        
        # Collect locations
        for loc_file in self.vault_path.glob("02_Worldbuilding/**/*.md"):
            if "location" in str(loc_file).lower() or "place" in str(loc_file).lower():
                name = loc_file.stem.replace("_", " ")
                entity_map['locations'].append((name, str(loc_file)))
        
        # Collect factions
        for faction_file in self.vault_path.glob("02_Worldbuilding/**/*Faction*.md"):
            name = faction_file.stem.replace("_", " ")
            entity_map['factions'].append((name, str(faction_file)))
        
        # Collect quests
        for quest_file in self.vault_path.glob("01_Adventures/**/*.md"):
            if "quest" in str(quest_file).lower():
                name = quest_file.stem.replace("_", " ")
                entity_map['quests'].append((name, str(quest_file)))
        
        return entity_map
    
    def suggest_links(self, file_path: Path) -> List[str]:
        \"\"\"Suggest automatic links for a file\"\"\"
        suggestions = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Look for entity mentions that could be linked
            for entity_type, entities in self.entity_map.items():
                for entity_name, entity_file in entities:
                    if entity_name.lower() in content.lower():
                        # Check if not already linked
                        if f"[[{entity_name}]]" not in content:
                            suggestions.append(f"Link '{entity_name}' to {entity_file}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return suggestions
    
    def auto_link_file(self, file_path: Path) -> int:
        \"\"\"Automatically add links to a file\"\"\"
        links_added = 0
        
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Add links for entity mentions
            for entity_type, entities in self.entity_map.items():
                for entity_name, entity_file in entities:
                    # Simple pattern matching (could be more sophisticated)
                    pattern = r'\\b' + re.escape(entity_name) + r'\\b'
                    if re.search(pattern, content, re.IGNORECASE):
                        # Check if not already linked
                        if f"[[{entity_name}]]" not in content:
                            # Replace first occurrence
                            content = re.sub(pattern, f"[[{entity_name}]]", content, count=1, flags=re.IGNORECASE)
                            links_added += 1
            
            # Write back if changes were made
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
            
        except Exception as e:
            print(f"Error auto-linking {file_path}: {e}")
        
        return links_added

def main():
    vault_path = Path(__file__).parent.parent.parent
    linker = AutoLinker(vault_path)
    
    total_links = 0
    for md_file in vault_path.rglob("*.md"):
        if any(skip in str(md_file) for skip in [".obsidian", "_SCRIPTS", "08_Archive"]):
            continue
        
        links_added = linker.auto_link_file(md_file)
        total_links += links_added
        
        if links_added > 0:
            print(f"Added {links_added} links to {md_file.name}")
    
    print(f"Total links added: {total_links}")

if __name__ == "__main__":
    main()
"""
        
        auto_link_script_path = self.automation_dir / "auto_linker.py"
        auto_link_script_path.write_text(auto_link_script)
        improvements.append("Created auto-linking script")
        
        # Create link suggestion system
        link_suggestions_script = """#!/usr/bin/env python3
import json
from pathlib import Path
from auto_linker import AutoLinker

def generate_link_suggestions():
    vault_path = Path(__file__).parent.parent.parent
    linker = AutoLinker(vault_path)
    
    suggestions = {}
    
    for md_file in vault_path.rglob("*.md"):
        if any(skip in str(md_file) for skip in [".obsidian", "_SCRIPTS", "08_Archive"]):
            continue
        
        file_suggestions = linker.suggest_links(md_file)
        if file_suggestions:
            suggestions[str(md_file.relative_to(vault_path))] = file_suggestions
    
    # Save suggestions
    suggestions_file = vault_path / "_METADATA" / "link_suggestions.json"
    suggestions_file.write_text(json.dumps(suggestions, indent=2))
    
    print(f"Generated suggestions for {len(suggestions)} files")
    return suggestions

if __name__ == "__main__":
    generate_link_suggestions()
"""
        
        suggestions_script_path = self.automation_dir / "link_suggestions.py"
        suggestions_script_path.write_text(link_suggestions_script)
        improvements.append("Created link suggestions system")
        
        return improvements

    def create_template_triggers(self) -> List[str]:
        """Create template triggers for automated content creation"""
        improvements = []
        
        # Template trigger configurations
        trigger_configs = {
            "new_npc": {
                "trigger": "folder:03_People",
                "template": "00_System/Templates/NPC_Template.md",
                "auto_fill": ["created", "modified"]
            },
            "new_location": {
                "trigger": "folder:02_Worldbuilding",
                "template": "00_System/Templates/Location_Template.md",
                "auto_fill": ["created", "modified"]
            },
            "new_session": {
                "trigger": "folder:06_Sessions",
                "template": "00_System/Templates/Session_Template.md",
                "auto_fill": ["created", "date", "number"]
            },
            "new_quest": {
                "trigger": "folder:01_Adventures",
                "template": "00_System/Templates/Quest_Template.md",
                "auto_fill": ["created", "modified", "status"]
            }
        }
        
        # Save trigger configurations
        triggers_config_path = self.obsidian_dir / "template-triggers.json"
        triggers_config_path.write_text(json.dumps(trigger_configs, indent=2))
        improvements.append("Created template trigger configurations")
        
        # Create template processor script
        template_processor = """#!/usr/bin/env python3
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class TemplateProcessor:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.triggers_config = self.load_triggers_config()
    
    def load_triggers_config(self) -> Dict[str, Any]:
        config_path = self.vault_path / ".obsidian" / "template-triggers.json"
        if config_path.exists():
            return json.loads(config_path.read_text())
        return {}
    
    def process_new_file(self, file_path: Path, content: str = "") -> str:
        \"\"\"Process a new file with appropriate template\"\"\"
        
        # Determine which trigger applies
        for trigger_name, config in self.triggers_config.items():
            if self.matches_trigger(file_path, config["trigger"]):
                return self.apply_template(file_path, config, content)
        
        return content
    
    def matches_trigger(self, file_path: Path, trigger: str) -> bool:
        \"\"\"Check if file matches trigger condition\"\"\"
        if trigger.startswith("folder:"):
            folder = trigger[7:]
            return folder in str(file_path)
        return False
    
    def apply_template(self, file_path: Path, config: Dict[str, Any], content: str) -> str:
        \"\"\"Apply template to file\"\"\"
        template_path = self.vault_path / config["template"]
        
        if not template_path.exists():
            return content
        
        template_content = template_path.read_text()
        
        # Replace template variables
        template_content = self.replace_variables(template_content, file_path, config)
        
        return template_content
    
    def replace_variables(self, content: str, file_path: Path, config: Dict[str, Any]) -> str:
        \"\"\"Replace template variables with actual values\"\"\"
        now = datetime.now()
        
        # Standard replacements
        replacements = {
            "{{title}}": file_path.stem.replace("_", " "),
            "{{filename}}": file_path.stem,
            "{{date}}": now.strftime("%Y-%m-%d"),
            "{{time}}": now.strftime("%H:%M"),
            "{{datetime}}": now.isoformat(),
            "{{date:YYYY-MM-DD}}": now.strftime("%Y-%m-%d"),
            "{{date:YYYY-MM-DD HH:mm}}": now.strftime("%Y-%m-%d %H:%M")
        }
        
        # Auto-fill specific fields
        auto_fill = config.get("auto_fill", [])
        for field in auto_fill:
            if field == "created":
                replacements[f"{{{{{field}}}}}"] = now.isoformat()
            elif field == "modified":
                replacements[f"{{{{{field}}}}}"] = now.isoformat()
            elif field == "status":
                replacements[f"{{{{{field}}}}}"] = "active"
            elif field == "number":
                # Try to determine session number
                session_num = self.get_next_session_number(file_path)
                replacements[f"{{{{{field}}}}}"] = str(session_num)
        
        # Apply replacements
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        return content
    
    def get_next_session_number(self, file_path: Path) -> int:
        \"\"\"Get next session number for session files\"\"\"
        session_folder = file_path.parent
        existing_sessions = list(session_folder.glob("Session_*.md"))
        
        if not existing_sessions:
            return 1
        
        # Extract numbers from existing sessions
        numbers = []
        for session_file in existing_sessions:
            match = re.search(r'Session_(\d+)', session_file.name)
            if match:
                numbers.append(int(match.group(1)))
        
        return max(numbers) + 1 if numbers else 1

def main():
    vault_path = Path(__file__).parent.parent.parent
    processor = TemplateProcessor(vault_path)
    
    # Example usage - process a new file
    # This would typically be called by Obsidian or file watcher
    print("Template processor ready")

if __name__ == "__main__":
    main()
"""
        
        processor_path = self.automation_dir / "template_processor.py"
        processor_path.write_text(template_processor)
        improvements.append("Created template processor system")
        
        return improvements

    def optimize_hotkeys(self) -> List[str]:
        """Optimize hotkeys and shortcuts for efficient workflow"""
        improvements = []
        
        # Hotkey configurations
        hotkey_config = {
            "hotkeys": {
                "app:go-back": [],
                "app:go-forward": [],
                "app:open-vault": [],
                "app:reload": [],
                "app:toggle-default-view-mode": [],
                "app:toggle-left-sidebar": [{"modifiers": ["Mod"], "key": "\\"}],
                "app:toggle-right-sidebar": [{"modifiers": ["Mod"], "key": "/"}],
                "command-palette:open": [{"modifiers": ["Mod", "Shift"], "key": "P"}],
                "editor:toggle-source": [{"modifiers": ["Mod"], "key": "E"}],
                "file-explorer:new-file": [{"modifiers": ["Mod"], "key": "N"}],
                "file-explorer:open": [{"modifiers": ["Mod", "Shift"], "key": "E"}],
                "global-search:open": [{"modifiers": ["Mod", "Shift"], "key": "F"}],
                "graph:open": [{"modifiers": ["Mod", "Shift"], "key": "G"}],
                "note-composer:merge-file": [],
                "note-composer:split-file": [],
                "outline:open": [{"modifiers": ["Mod", "Shift"], "key": "O"}],
                "quick-switcher:open": [{"modifiers": ["Mod"], "key": "O"}],
                "random-note": [{"modifiers": ["Mod", "Shift"], "key": "R"}],
                "starred:open": [],
                "tag-pane:open": [{"modifiers": ["Mod", "Shift"], "key": "T"}],
                "templater-obsidian:insert-templater": [{"modifiers": ["Mod", "Shift"], "key": "I"}],
                "workspace:close": [{"modifiers": ["Mod"], "key": "W"}],
                "workspace:edit-file-title": [{"modifiers": ["Mod", "Shift"], "key": "R"}],
                "workspace:open-in-new-window": [],
                "workspace:split-horizontal": [{"modifiers": ["Mod", "Shift"], "key": "-"}],
                "workspace:split-vertical": [{"modifiers": ["Mod", "Shift"], "key": "|"}],
                "workspace:toggle-pin": [{"modifiers": ["Mod", "Shift"], "key": "Pin"}]
            }
        }
        
        # Custom hotkeys for TTRPG workflow
        custom_hotkeys = {
            "quick-npc-create": [{"modifiers": ["Ctrl", "Shift"], "key": "N"}],
            "quick-location-create": [{"modifiers": ["Ctrl", "Shift"], "key": "L"}],
            "quick-quest-create": [{"modifiers": ["Ctrl", "Shift"], "key": "Q"}],
            "session-dashboard": [{"modifiers": ["Ctrl", "Shift"], "key": "S"}],
            "campaign-overview": [{"modifiers": ["Ctrl", "Shift"], "key": "C"}],
            "random-generator": [{"modifiers": ["Ctrl", "Shift"], "key": "R"}],
            "quick-capture": [{"modifiers": ["Ctrl"], "key": "K"}],
            "process-inbox": [{"modifiers": ["Ctrl", "Shift"], "key": "P"}]
        }
        
        hotkey_config["custom_hotkeys"] = custom_hotkeys
        
        # Save hotkey configuration
        hotkey_path = self.obsidian_dir / "hotkeys.json"
        hotkey_path.write_text(json.dumps(hotkey_config["hotkeys"], indent=2))
        improvements.append("Configured optimized hotkeys")
        
        # Create hotkey reference guide
        hotkey_guide = """# Hotkey Reference for TTRPG Vault

## Standard Obsidian Hotkeys
- **Cmd/Ctrl + O**: Quick switcher (open any file)
- **Cmd/Ctrl + Shift + F**: Global search
- **Cmd/Ctrl + E**: Toggle source/preview mode
- **Cmd/Ctrl + \\**: Toggle left sidebar
- **Cmd/Ctrl + /**: Toggle right sidebar
- **Cmd/Ctrl + Shift + P**: Command palette

## TTRPG-Specific Hotkeys
- **Ctrl + Shift + N**: Quick create NPC
- **Ctrl + Shift + L**: Quick create Location
- **Ctrl + Shift + Q**: Quick create Quest
- **Ctrl + Shift + S**: Open session dashboard
- **Ctrl + Shift + C**: Open campaign overview
- **Ctrl + Shift + R**: Random generator
- **Ctrl + K**: Quick capture mode
- **Ctrl + Shift + P**: Process inbox

## Workflow Shortcuts
- **Cmd/Ctrl + N**: New file with template
- **Cmd/Ctrl + Shift + G**: Graph view
- **Cmd/Ctrl + Shift + O**: Outline view
- **Cmd/Ctrl + Shift + T**: Tag pane

## Quick Navigation
- Use **Cmd/Ctrl + O** then type:
  - "dash" for dashboards
  - "npc" for characters
  - "loc" for locations
  - "quest" for quests
  - "session" for session notes

## Pro Tips
1. Use tags to quickly filter content
2. Pin frequently used files
3. Use workspaces for different activities
4. Bookmark important pages
"""
        
        guide_path = self.vault_path / "00_System" / "Hotkey_Reference.md"
        guide_path.write_text(hotkey_guide)
        improvements.append("Created hotkey reference guide")
        
        return improvements

    def setup_workspace_layouts(self) -> List[str]:
        """Setup workspace layouts for different activities"""
        improvements = []
        
        # Create workspace configurations
        workspaces_dir = self.obsidian_dir / "workspaces"
        workspaces_dir.mkdir(exist_ok=True)
        
        # DM Session workspace
        dm_session_workspace = {
            "main": {
                "id": "dm-session-main",
                "type": "split",
                "children": [
                    {
                        "id": "current-session",
                        "type": "leaf",
                        "state": {
                            "type": "markdown",
                            "state": {
                                "file": "06_Sessions/Current_Session.md",
                                "mode": "source",
                                "source": False
                            }
                        }
                    },
                    {
                        "id": "npc-reference",
                        "type": "leaf",
                        "state": {
                            "type": "markdown",
                            "state": {
                                "file": "00_System/NPC_Quick_Reference.md",
                                "mode": "preview",
                                "source": False
                            }
                        }
                    }
                ],
                "direction": "horizontal"
            },
            "left": {
                "id": "left-sidebar",
                "type": "split",
                "children": [
                    {
                        "id": "file-explorer",
                        "type": "leaf",
                        "state": {"type": "file-explorer", "state": {}}
                    },
                    {
                        "id": "starred",
                        "type": "leaf",
                        "state": {"type": "starred", "state": {}}
                    }
                ]
            },
            "right": {
                "id": "right-sidebar",
                "type": "split",
                "children": [
                    {
                        "id": "outline",
                        "type": "leaf",
                        "state": {"type": "outline", "state": {}}
                    },
                    {
                        "id": "calendar",
                        "type": "leaf",
                        "state": {"type": "calendar", "state": {}}
                    },
                    {
                        "id": "tag-pane",
                        "type": "leaf",
                        "state": {"type": "tag", "state": {"sortOrder": "frequency", "useHierarchy": True}}
                    }
                ]
            },
            "active": "current-session",
            "lastOpenFiles": [
                "06_Sessions/Current_Session.md",
                "00_System/NPC_Quick_Reference.md",
                "00_System/Quest_Master_Tracker.md"
            ]
        }
        
        dm_workspace_path = workspaces_dir / "DM Session.json"
        dm_workspace_path.write_text(json.dumps(dm_session_workspace, indent=2))
        improvements.append("Created DM Session workspace")
        
        # World Building workspace
        worldbuilding_workspace = {
            "main": {
                "id": "worldbuilding-main",
                "type": "split",
                "children": [
                    {
                        "id": "location-map",
                        "type": "leaf",
                        "state": {
                            "type": "graph",
                            "state": {
                                "collapse-filter": True,
                                "search": "tag:#location",
                                "showTags": False,
                                "showAttachments": False,
                                "hideUnresolved": False,
                                "showOrphans": True,
                                "collapse-color-groups": True,
                                "colorGroups": [],
                                "collapse-display": True,
                                "showArrow": False,
                                "textFadeMultiplier": 0,
                                "nodeSizeMultiplier": 1,
                                "lineSizeMultiplier": 1,
                                "collapse-forces": True,
                                "centerStrength": 0.518713248970312,
                                "repelStrength": 10,
                                "linkStrength": 1,
                                "linkDistance": 250,
                                "scale": 1,
                                "close": True
                            }
                        }
                    },
                    {
                        "id": "location-editor",
                        "type": "leaf",
                        "state": {
                            "type": "markdown",
                            "state": {
                                "file": "02_Worldbuilding/00_Location_Index.md",
                                "mode": "source",
                                "source": False
                            }
                        }
                    }
                ],
                "direction": "horizontal"
            },
            "left": {
                "id": "left-sidebar-wb",
                "type": "split",
                "children": [
                    {
                        "id": "file-explorer-wb",
                        "type": "leaf",
                        "state": {"type": "file-explorer", "state": {}}
                    }
                ]
            },
            "right": {
                "id": "right-sidebar-wb",
                "type": "split",
                "children": [
                    {
                        "id": "outline-wb",
                        "type": "leaf",
                        "state": {"type": "outline", "state": {}}
                    },
                    {
                        "id": "tag-pane-wb",
                        "type": "leaf",
                        "state": {"type": "tag", "state": {"sortOrder": "frequency", "useHierarchy": True}}
                    }
                ]
            },
            "active": "location-editor"
        }
        
        wb_workspace_path = workspaces_dir / "World Building.json"
        wb_workspace_path.write_text(json.dumps(worldbuilding_workspace, indent=2))
        improvements.append("Created World Building workspace")
        
        # Session Prep workspace
        prep_workspace = {
            "main": {
                "id": "prep-main",
                "type": "split",
                "children": [
                    {
                        "id": "prep-checklist",
                        "type": "leaf",
                        "state": {
                            "type": "markdown",
                            "state": {
                                "file": "00_System/Session_Prep_Template.md",
                                "mode": "source",
                                "source": False
                            }
                        }
                    },
                    {
                        "id": "campaign-status",
                        "type": "leaf",
                        "state": {
                            "type": "markdown",
                            "state": {
                                "file": "00_System/Master_Campaign_Index.md",
                                "mode": "preview",
                                "source": False
                            }
                        }
                    },
                    {
                        "id": "quick-reference",
                        "type": "leaf",
                        "state": {
                            "type": "markdown",
                            "state": {
                                "file": "00_System/DM_Screen.md",
                                "mode": "preview",
                                "source": False
                            }
                        }
                    }
                ],
                "direction": "horizontal"
            },
            "active": "prep-checklist"
        }
        
        prep_workspace_path = workspaces_dir / "Session Prep.json"
        prep_workspace_path.write_text(json.dumps(prep_workspace, indent=2))
        improvements.append("Created Session Prep workspace")
        
        return improvements

    def configure_bookmarks(self) -> List[str]:
        """Configure smart bookmarks for quick access"""
        improvements = []
        
        # Essential bookmarks for TTRPG vault
        bookmarks_config = {
            "items": [
                {
                    "type": "group",
                    "ctime": 1692000000000,
                    "title": "🎲 DM Essentials",
                    "items": [
                        {"type": "file", "ctime": 1692000000000, "path": "00_System/00_GM_DASHBOARD.md"},
                        {"type": "file", "ctime": 1692000000000, "path": "00_System/Master_Campaign_Index.md"},
                        {"type": "file", "ctime": 1692000000000, "path": "00_System/Quest_Master_Tracker.md"},
                        {"type": "file", "ctime": 1692000000000, "path": "00_System/DM_Screen.md"}
                    ]
                },
                {
                    "type": "group",
                    "ctime": 1692000000000,
                    "title": "📚 Quick References",
                    "items": [
                        {"type": "file", "ctime": 1692000000000, "path": "00_System/NPC_Quick_Reference.md"},
                        {"type": "file", "ctime": 1692000000000, "path": "02_Worldbuilding/00_Location_Index.md"},
                        {"type": "file", "ctime": 1692000000000, "path": "03_People/00_NPC_Master_Database.md"}
                    ]
                },
                {
                    "type": "group",
                    "ctime": 1692000000000,
                    "title": "🌊 Aquabyssos Campaign",
                    "items": [
                        {"type": "search", "ctime": 1692000000000, "query": "campaign:aquabyssos"},
                        {"type": "search", "ctime": 1692000000000, "query": "tag:#aquabyssos"}
                    ]
                },
                {
                    "type": "group",
                    "ctime": 1692000000000,
                    "title": "☁️ Aethermoor Campaign",
                    "items": [
                        {"type": "search", "ctime": 1692000000000, "query": "campaign:aethermoor"},
                        {"type": "search", "ctime": 1692000000000, "query": "tag:#aethermoor"}
                    ]
                },
                {
                    "type": "group",
                    "ctime": 1692000000000,
                    "title": "⚡ Quick Actions",
                    "items": [
                        {"type": "file", "ctime": 1692000000000, "path": "00_System/Quick_Capture_Inbox"},
                        {"type": "search", "ctime": 1692000000000, "query": "tag:#quick_capture"},
                        {"type": "search", "ctime": 1692000000000, "query": "status:draft"}
                    ]
                }
            ]
        }
        
        # Save bookmarks configuration
        bookmarks_path = self.obsidian_dir / "bookmarks.json"
        bookmarks_path.write_text(json.dumps(bookmarks_config, indent=2))
        improvements.append("Configured smart bookmarks")
        
        # Create bookmark manager script
        bookmark_manager = """#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

class BookmarkManager:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.bookmarks_path = vault_path / ".obsidian" / "bookmarks.json"
    
    def add_bookmark(self, title: str, path: str, group: str = None):
        \"\"\"Add a new bookmark\"\"\"
        if not self.bookmarks_path.exists():
            self.create_empty_bookmarks()
        
        bookmarks = json.loads(self.bookmarks_path.read_text())
        
        new_bookmark = {
            "type": "file",
            "ctime": int(datetime.now().timestamp() * 1000),
            "path": path
        }
        
        if group:
            # Find or create group
            target_group = None
            for item in bookmarks["items"]:
                if item.get("type") == "group" and item.get("title") == group:
                    target_group = item
                    break
            
            if not target_group:
                target_group = {
                    "type": "group",
                    "ctime": int(datetime.now().timestamp() * 1000),
                    "title": group,
                    "items": []
                }
                bookmarks["items"].append(target_group)
            
            target_group["items"].append(new_bookmark)
        else:
            bookmarks["items"].append(new_bookmark)
        
        self.bookmarks_path.write_text(json.dumps(bookmarks, indent=2))
    
    def create_empty_bookmarks(self):
        \"\"\"Create empty bookmarks structure\"\"\"
        empty_bookmarks = {"items": []}
        self.bookmarks_path.write_text(json.dumps(empty_bookmarks, indent=2))
    
    def auto_bookmark_important_files(self):
        \"\"\"Automatically bookmark important files\"\"\"
        important_patterns = [
            ("🎲 DM Essentials", [
                "00_System/00_GM_DASHBOARD.md",
                "00_System/Master_Campaign_Index.md",
                "00_System/Quest_Master_Tracker.md"
            ]),
            ("📝 Recent Sessions", [
                "06_Sessions/Session_*_*.md"  # Pattern for recent sessions
            ])
        ]
        
        for group_name, patterns in important_patterns:
            for pattern in patterns:
                if "*" in pattern:
                    # Handle glob patterns
                    files = list(self.vault_path.glob(pattern))
                    for file in sorted(files)[-5:]:  # Last 5 files
                        if file.exists():
                            self.add_bookmark(file.name, str(file.relative_to(self.vault_path)), group_name)
                else:
                    file_path = self.vault_path / pattern
                    if file_path.exists():
                        self.add_bookmark(file_path.name, pattern, group_name)

def main():
    vault_path = Path(__file__).parent.parent.parent
    manager = BookmarkManager(vault_path)
    manager.auto_bookmark_important_files()
    print("Updated bookmarks")

if __name__ == "__main__":
    main()
"""
        
        bookmark_script_path = self.automation_dir / "bookmark_manager.py"
        bookmark_script_path.write_text(bookmark_manager)
        improvements.append("Created bookmark management system")
        
        return improvements

    def create_automation_scripts(self) -> List[str]:
        """Create comprehensive automation scripts"""
        improvements = []
        
        # Master automation controller
        automation_controller = """#!/usr/bin/env python3
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

class AutomationController:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.automation_dir = vault_path / "_SCRIPTS" / "automation"
        self.config_path = self.automation_dir / "automation_config.json"
        self.load_config()
    
    def load_config(self):
        \"\"\"Load automation configuration\"\"\"
        default_config = {
            "daily_tasks": {
                "create_daily_note": {"enabled": True, "time": "08:00"},
                "process_quick_captures": {"enabled": True, "time": "18:00"},
                "update_bookmarks": {"enabled": True, "time": "20:00"},
                "backup_vault": {"enabled": True, "time": "23:00"}
            },
            "weekly_tasks": {
                "generate_session_summary": {"enabled": True, "day": "sunday"},
                "update_campaign_status": {"enabled": True, "day": "sunday"},
                "clean_archive": {"enabled": True, "day": "saturday"}
            },
            "on_demand_tasks": {
                "auto_link_content": {"script": "auto_linker.py"},
                "process_inbox": {"script": "process_quick_captures.py"},
                "generate_reports": {"script": "generate_reports.py"}
            }
        }
        
        if self.config_path.exists():
            self.config = json.loads(self.config_path.read_text())
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        \"\"\"Save automation configuration\"\"\"
        self.config_path.write_text(json.dumps(self.config, indent=2))
    
    def run_daily_tasks(self):
        \"\"\"Run daily automation tasks\"\"\"
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        for task_name, task_config in self.config["daily_tasks"].items():
            if task_config["enabled"] and task_config["time"] == current_time:
                self.run_task(task_name)
    
    def run_task(self, task_name: str):
        \"\"\"Run a specific automation task\"\"\"
        script_map = {
            "create_daily_note": "create_daily_note.py",
            "process_quick_captures": "process_quick_captures.py",
            "update_bookmarks": "bookmark_manager.py",
            "auto_link_content": "auto_linker.py"
        }
        
        script_name = script_map.get(task_name)
        if script_name:
            script_path = self.automation_dir / script_name
            if script_path.exists():
                try:
                    subprocess.run(["python3", str(script_path)], cwd=str(self.vault_path))
                    print(f"Completed task: {task_name}")
                except Exception as e:
                    print(f"Error running {task_name}: {e}")
    
    def run_on_demand(self, task_name: str):
        \"\"\"Run an on-demand task\"\"\"
        if task_name in self.config["on_demand_tasks"]:
            script_name = self.config["on_demand_tasks"][task_name]["script"]
            script_path = self.automation_dir / script_name
            if script_path.exists():
                subprocess.run(["python3", str(script_path)], cwd=str(self.vault_path))

def main():
    vault_path = Path(__file__).parent.parent.parent
    controller = AutomationController(vault_path)
    
    import sys
    if len(sys.argv) > 1:
        task = sys.argv[1]
        if task == "daily":
            controller.run_daily_tasks()
        else:
            controller.run_on_demand(task)
    else:
        print("Available commands:")
        print("  daily - Run daily tasks")
        print("  auto_link_content - Run auto-linking")
        print("  process_inbox - Process quick captures")

if __name__ == "__main__":
    main()
"""
        
        controller_path = self.automation_dir / "automation_controller.py"
        controller_path.write_text(automation_controller)
        improvements.append("Created automation controller")
        
        # File watcher for real-time automation
        file_watcher = """#!/usr/bin/env python3
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from template_processor import TemplateProcessor

class VaultEventHandler(FileSystemEventHandler):
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.template_processor = TemplateProcessor(vault_path)
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix == '.md':
            # Apply template if it's a new markdown file
            try:
                content = file_path.read_text()
                if not content.strip():  # Empty file
                    processed_content = self.template_processor.process_new_file(file_path)
                    if processed_content != content:
                        file_path.write_text(processed_content)
                        print(f"Applied template to: {file_path.name}")
            except Exception as e:
                print(f"Error processing new file {file_path}: {e}")
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix == '.md':
            # Could trigger auto-linking or other processing
            pass

def main():
    vault_path = Path(__file__).parent.parent.parent
    
    event_handler = VaultEventHandler(vault_path)
    observer = Observer()
    observer.schedule(event_handler, str(vault_path), recursive=True)
    
    print(f"Watching vault: {vault_path}")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()
"""
        
        watcher_path = self.automation_dir / "file_watcher.py"
        watcher_path.write_text(file_watcher)
        improvements.append("Created file watcher system")
        
        return improvements

    def setup_content_generation(self) -> List[str]:
        """Setup automated content generation"""
        improvements = []
        
        # Random content generators
        random_generators = {
            "random_npc_generator.py": """#!/usr/bin/env python3
import random
from pathlib import Path

class NPCGenerator:
    def __init__(self):
        self.names = {
            'first': ['Aeliana', 'Branwen', 'Caelum', 'Drusilla', 'Erasmus', 'Fiora', 'Gareth', 'Hestara'],
            'last': ['Brightblade', 'Stormwind', 'Goldleaf', 'Ironforge', 'Voidwalker', 'Moonshadow']
        }
        
        self.races = ['Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn', 'Tiefling', 'Gnome']
        self.classes = ['Fighter', 'Wizard', 'Rogue', 'Cleric', 'Ranger', 'Bard', 'Sorcerer']
        self.alignments = ['LG', 'LN', 'LE', 'NG', 'TN', 'NE', 'CG', 'CN', 'CE']
        
        self.occupations = [
            'Merchant', 'Guard', 'Scholar', 'Innkeeper', 'Blacksmith', 'Healer',
            'Noble', 'Farmer', 'Sailor', 'Artist', 'Diplomat', 'Spy'
        ]
        
        self.traits = [
            'Ambitious', 'Cautious', 'Cheerful', 'Gruff', 'Honest', 'Mysterious',
            'Nervous', 'Patient', 'Quick-tempered', 'Scholarly', 'Superstitious', 'Witty'
        ]
    
    def generate_npc(self, campaign: str = "Aquabyssos") -> dict:
        first_name = random.choice(self.names['first'])
        last_name = random.choice(self.names['last'])
        
        return {
            'name': f"{first_name} {last_name}",
            'race': random.choice(self.races),
            'class': random.choice(self.classes),
            'alignment': random.choice(self.alignments),
            'occupation': random.choice(self.occupations),
            'trait': random.choice(self.traits),
            'campaign': campaign
        }
    
    def create_npc_file(self, vault_path: Path, campaign: str = "Aquabyssos") -> str:
        npc_data = self.generate_npc(campaign)
        
        # Create filename
        clean_name = npc_data['name'].replace(' ', '_')
        filename = f"NPC_Generated_{clean_name}.md"
        
        # Create content
        content = f\"\"\"---
type: npc
tags: [character, npc, generated]
campaign: {npc_data['campaign']}
status: draft
race: {npc_data['race']}
class: {npc_data['class']}
alignment: {npc_data['alignment']}
occupation: {npc_data['occupation']}
trait: {npc_data['trait']}
---

# {npc_data['name']}

## Quick Stats
- **Race:** {npc_data['race']}
- **Class:** {npc_data['class']}
- **Alignment:** {npc_data['alignment']}
- **Occupation:** {npc_data['occupation']}

## Personality
**Key Trait:** {npc_data['trait']}

*[Expand with more details as needed]*

## Background
*[Add background and motivations]*

## Role in Campaign
*[Define their role in the story]*
\"\"\"
        
        # Save file
        npc_file = vault_path / "03_People" / filename
        npc_file.write_text(content)
        
        return str(npc_file.relative_to(vault_path))

def main():
    vault_path = Path(__file__).parent.parent.parent
    generator = NPCGenerator()
    
    import sys
    campaign = sys.argv[1] if len(sys.argv) > 1 else "Aquabyssos"
    
    npc_file = generator.create_npc_file(vault_path, campaign)
    print(f"Generated NPC: {npc_file}")

if __name__ == "__main__":
    main()
""",
            "random_quest_generator.py": """#!/usr/bin/env python3
import random
from pathlib import Path

class QuestGenerator:
    def __init__(self):
        self.quest_types = ['Rescue', 'Retrieve', 'Deliver', 'Investigate', 'Eliminate', 'Protect']
        self.objectives = [
            'a missing person', 'ancient artifact', 'important message', 'mysterious events',
            'dangerous monster', 'valuable cargo', 'sacred relic', 'stolen goods'
        ]
        self.locations = [
            'abandoned ruins', 'dark forest', 'underground cavern', 'bustling city',
            'remote village', 'ancient temple', 'treacherous mountains', 'mysterious island'
        ]
        self.complications = [
            'hostile guards', 'magical traps', 'rival adventurers', 'time pressure',
            'false information', 'political intrigue', 'natural disasters', 'cursed items'
        ]
    
    def generate_quest(self, campaign: str = "Aquabyssos") -> dict:
        quest_type = random.choice(self.quest_types)
        objective = random.choice(self.objectives)
        location = random.choice(self.locations)
        complication = random.choice(self.complications)
        
        title = f"{quest_type} {objective.title()}"
        
        return {
            'title': title,
            'type': quest_type.lower(),
            'objective': objective,
            'location': location,
            'complication': complication,
            'campaign': campaign,
            'level': random.randint(1, 10)
        }
    
    def create_quest_file(self, vault_path: Path, campaign: str = "Aquabyssos") -> str:
        quest_data = self.generate_quest(campaign)
        
        # Create filename
        clean_title = quest_data['title'].replace(' ', '_')
        filename = f"Quest_Generated_{clean_title}.md"
        
        # Create content
        content = f\"\"\"---
type: quest
tags: [adventure, quest, generated]
campaign: {quest_data['campaign']}
status: available
level: {quest_data['level']}
quest_type: {quest_data['type']}
---

# {quest_data['title']}

## Objective
{quest_data['type'].title()} {quest_data['objective']} from {quest_data['location']}.

## Background
*[Add background story and context]*

## Location
The quest takes place in {quest_data['location']}.

## Complications
The party will face {quest_data['complication']} during this quest.

## Rewards
*[Define appropriate rewards for level {quest_data['level']} characters]*

## Notes
*[Add additional details and plot hooks]*
\"\"\"
        
        # Save file
        quest_file = vault_path / "01_Adventures" / "Quests" / filename
        quest_file.parent.mkdir(parents=True, exist_ok=True)
        quest_file.write_text(content)
        
        return str(quest_file.relative_to(vault_path))

def main():
    vault_path = Path(__file__).parent.parent.parent
    generator = QuestGenerator()
    
    import sys
    campaign = sys.argv[1] if len(sys.argv) > 1 else "Aquabyssos"
    
    quest_file = generator.create_quest_file(vault_path, campaign)
    print(f"Generated Quest: {quest_file}")

if __name__ == "__main__":
    main()
"""
        }
        
        # Create generator scripts
        for script_name, script_content in random_generators.items():
            script_path = self.automation_dir / script_name
            script_path.write_text(script_content)
            improvements.append(f"Created content generator: {script_name}")
        
        return improvements

    def configure_maintenance_tasks(self) -> List[str]:
        """Configure automated maintenance tasks"""
        improvements = []
        
        # Maintenance script
        maintenance_script = """#!/usr/bin/env python3
import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta

class VaultMaintenance:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.archive_path = vault_path / "08_Archive"
        self.backup_path = vault_path.parent / "Vault_Backups"
    
    def create_backup(self):
        \"\"\"Create a backup of the vault\"\"\"
        self.backup_path.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"vault_backup_{timestamp}"
        backup_dir = self.backup_path / backup_name
        
        # Copy vault (excluding backups and temp files)
        shutil.copytree(
            self.vault_path,
            backup_dir,
            ignore=shutil.ignore_patterns('.DS_Store', 'Vault_Backups', '*.tmp')
        )
        
        print(f"Created backup: {backup_dir}")
        
        # Keep only last 7 backups
        self.cleanup_old_backups()
    
    def cleanup_old_backups(self):
        \"\"\"Remove backups older than 7 days\"\"\"
        if not self.backup_path.exists():
            return
        
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for backup_dir in self.backup_path.iterdir():
            if backup_dir.is_dir() and backup_dir.name.startswith("vault_backup_"):
                try:
                    backup_date = datetime.strptime(backup_dir.name[-15:], "%Y%m%d_%H%M%S")
                    if backup_date < cutoff_date:
                        shutil.rmtree(backup_dir)
                        print(f"Removed old backup: {backup_dir.name}")
                except ValueError:
                    continue
    
    def clean_empty_files(self):
        \"\"\"Remove empty markdown files\"\"\"
        empty_files = []
        
        for md_file in self.vault_path.rglob("*.md"):
            if any(skip in str(md_file) for skip in [".obsidian", "_SCRIPTS", "08_Archive"]):
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8').strip()
                if len(content) < 10:  # Very short files
                    empty_files.append(md_file)
            except:
                continue
        
        for empty_file in empty_files:
            # Move to archive instead of deleting
            archive_file = self.archive_path / "empty_files" / empty_file.name
            archive_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(empty_file, archive_file)
            print(f"Archived empty file: {empty_file.name}")
    
    def update_modification_dates(self):
        \"\"\"Update modification dates in frontmatter\"\"\"
        updated_count = 0
        
        for md_file in self.vault_path.rglob("*.md"):
            if any(skip in str(md_file) for skip in [".obsidian", "_SCRIPTS", "08_Archive"]):
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8')
                
                if content.startswith('---\\n'):
                    parts = content.split('---\\n', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        body = parts[2]
                        
                        # Update modified date
                        now = datetime.now().isoformat()
                        if 'modified:' in frontmatter:
                            # Replace existing modified date
                            import re
                            frontmatter = re.sub(
                                r'modified:.*',
                                f'modified: {now}',
                                frontmatter
                            )
                        else:
                            # Add modified date
                            frontmatter += f"\\nmodified: {now}"
                        
                        new_content = f"---\\n{frontmatter}---\\n{body}"
                        md_file.write_text(new_content, encoding='utf-8')
                        updated_count += 1
                        
            except Exception as e:
                print(f"Error updating {md_file}: {e}")
                continue
        
        print(f"Updated modification dates for {updated_count} files")
    
    def generate_maintenance_report(self):
        \"\"\"Generate maintenance report\"\"\"
        report = {
            'timestamp': datetime.now().isoformat(),
            'vault_stats': self.get_vault_stats(),
            'maintenance_actions': []
        }
        
        report_file = self.vault_path / "_METADATA" / f"maintenance_report_{datetime.now().strftime('%Y%m%d')}.json"
        report_file.write_text(json.dumps(report, indent=2))
        
        return report
    
    def get_vault_stats(self) -> dict:
        \"\"\"Get current vault statistics\"\"\"
        stats = {
            'total_files': 0,
            'markdown_files': 0,
            'total_size_mb': 0,
            'by_folder': {}
        }
        
        for file_path in self.vault_path.rglob("*"):
            if file_path.is_file():
                stats['total_files'] += 1
                
                if file_path.suffix == '.md':
                    stats['markdown_files'] += 1
                
                try:
                    size = file_path.stat().st_size
                    stats['total_size_mb'] += size / (1024 * 1024)
                    
                    # Count by folder
                    folder = str(file_path.parent.relative_to(self.vault_path)).split('/')[0]
                    if folder not in stats['by_folder']:
                        stats['by_folder'][folder] = 0
                    stats['by_folder'][folder] += 1
                    
                except:
                    continue
        
        stats['total_size_mb'] = round(stats['total_size_mb'], 2)
        return stats

def main():
    vault_path = Path(__file__).parent.parent.parent
    maintenance = VaultMaintenance(vault_path)
    
    import sys
    if len(sys.argv) > 1:
        task = sys.argv[1]
        if task == "backup":
            maintenance.create_backup()
        elif task == "clean":
            maintenance.clean_empty_files()
        elif task == "update":
            maintenance.update_modification_dates()
        elif task == "report":
            report = maintenance.generate_maintenance_report()
            print(json.dumps(report, indent=2))
        else:
            print("Unknown task")
    else:
        # Run all maintenance tasks
        maintenance.create_backup()
        maintenance.clean_empty_files()
        maintenance.update_modification_dates()
        maintenance.generate_maintenance_report()
        print("Completed all maintenance tasks")

if __name__ == "__main__":
    main()
"""
        
        maintenance_path = self.automation_dir / "vault_maintenance.py"
        maintenance_path.write_text(maintenance_script)
        improvements.append("Created vault maintenance system")
        
        # Create cron job setup script (for Unix systems)
        cron_setup = """#!/bin/bash
# Vault Automation Cron Setup
# Run this script to set up automated tasks

VAULT_PATH="$PWD"
AUTOMATION_DIR="$VAULT_PATH/_SCRIPTS/automation"

# Create daily cron job for maintenance
(crontab -l 2>/dev/null; echo "0 2 * * * cd '$VAULT_PATH' && python3 '$AUTOMATION_DIR/vault_maintenance.py' backup") | crontab -

# Create hourly cron job for processing quick captures
(crontab -l 2>/dev/null; echo "0 * * * * cd '$VAULT_PATH' && python3 '$AUTOMATION_DIR/process_quick_captures.py'") | crontab -

# Create daily cron job for creating daily notes
(crontab -l 2>/dev/null; echo "0 8 * * * cd '$VAULT_PATH' && python3 '$AUTOMATION_DIR/create_daily_note.py'") | crontab -

echo "Cron jobs installed successfully!"
echo "Run 'crontab -l' to see installed jobs"
"""
        
        cron_path = self.automation_dir / "setup_cron.sh"
        cron_path.write_text(cron_setup)
        cron_path.chmod(0o755)  # Make executable
        improvements.append("Created cron job setup script")
        
        return improvements

    def generate_phase_6_report(self):
        """Generate comprehensive Phase 6 completion report"""
        report = {
            'phase': 6,
            'title': 'Automation Setup',
            'completed_at': datetime.now(timezone.utc).isoformat(),
            'steps_completed': self.steps_completed,
            'improvements_made': self.improvements_made,
            'total_improvements': len(self.improvements_made),
            'automation_features': [
                'Daily notes automation',
                'Quick capture system',
                'Auto-linking content',
                'Template triggers',
                'Optimized hotkeys',
                'Workspace layouts',
                'Smart bookmarks',
                'Content generators',
                'Maintenance automation',
                'File watching system'
            ],
            'scripts_created': [
                'automation_controller.py',
                'create_daily_note.py',
                'process_quick_captures.py',
                'auto_linker.py',
                'template_processor.py',
                'bookmark_manager.py',
                'file_watcher.py',
                'random_npc_generator.py',
                'random_quest_generator.py',
                'vault_maintenance.py'
            ],
            'configuration_files': [
                '.obsidian/daily-notes.json',
                '.obsidian/hotkeys.json',
                '.obsidian/bookmarks.json',
                '.obsidian/template-triggers.json',
                '.obsidian/workspaces/'
            ]
        }
        
        # Save report
        report_file = self.vault_path / "_SCRIPTS" / f"phase_6_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.write_text(json.dumps(report, indent=2))
        
        # Print summary
        print(f"\n🎉 Phase 6 Complete!")
        print(f"✅ Completed {self.steps_completed} steps")
        print(f"📈 Made {len(self.improvements_made)} improvements")
        print(f"⚙️ Created {len(report['scripts_created'])} automation scripts")
        print(f"🔧 Configured {len(report['automation_features'])} automation features")
        print(f"📋 Report saved to {report_file}")

def main():
    vault_path = Path(__file__).parent.parent
    automation = AutomationSetup(str(vault_path))
    automation.run_phase_6()

if __name__ == "__main__":
    main()