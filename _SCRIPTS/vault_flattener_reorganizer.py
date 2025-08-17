#!/usr/bin/env python3
"""
Vault Flattener & Reorganizer
Simplifies excessive directory nesting and consolidates content
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime
import json
from collections import defaultdict

class VaultFlattenerReorganizer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.moves_log = []
        self.stats = defaultdict(int)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Simplified flat structure
        self.new_structure = {
            "System": ["indexes", "dashboards", "templates", "automation", "metadata"],
            "Adventures": ["campaigns", "sessions", "quests", "encounters"],
            "World": ["locations", "npcs", "factions", "lore", "timeline"],
            "Rules": ["mechanics", "homebrew", "quick-reference"],
            "Resources": ["maps", "assets", "handouts", "tables"],
            "Characters": ["pcs", "party", "sheets", "backstories"],
            "Archive": ["old-versions", "backups", "deprecated"]
        }
        
    def analyze_current_structure(self):
        """Analyze current vault structure"""
        print("📊 Analyzing current vault structure...")
        
        for root, dirs, files in os.walk(self.vault_path):
            level = root.replace(str(self.vault_path), '').count(os.sep)
            self.stats[f'depth_{level}'] += 1
            
            # Track deeply nested files
            if level > 3:
                self.stats['deeply_nested'] += len(files)
            
            # Track total files
            self.stats['total_files'] += len(files)
            
            # Find duplicate directory patterns
            dir_name = Path(root).name
            if re.match(r'^\d{2}_', dir_name):  # Numbered directories
                self.stats['numbered_dirs'] += 1
                
        print(f"  Total files: {self.stats['total_files']}")
        print(f"  Deeply nested files (>3 levels): {self.stats['deeply_nested']}")
        print(f"  Numbered directories: {self.stats['numbered_dirs']}")
        
    def create_flat_structure(self):
        """Create new flattened directory structure"""
        print("\n🏗️ Creating flattened structure...")
        
        for main_dir, subdirs in self.new_structure.items():
            main_path = self.vault_path / main_dir
            main_path.mkdir(exist_ok=True)
            
            for subdir in subdirs:
                sub_path = main_path / subdir
                sub_path.mkdir(exist_ok=True)
                print(f"  ✓ Created {main_dir}/{subdir}")
                
    def consolidate_similar_content(self):
        """Consolidate similar content from multiple locations"""
        print("\n🔄 Consolidating similar content...")
        
        consolidation_map = {
            # NPCs from various locations
            ("npcs", "World/npcs"): [
                "**/NPCs/**/*.md",
                "**/NPC/**/*.md", 
                "**/Characters/NPCs/**/*.md",
                "**/02_Worldbuilding/**/NPCs/**/*.md"
            ],
            
            # Locations from various places
            ("locations", "World/locations"): [
                "**/Locations/**/*.md",
                "**/Places/**/*.md",
                "**/02_Worldbuilding/Locations/**/*.md",
                "**/Cities/**/*.md",
                "**/Towns/**/*.md"
            ],
            
            # Sessions and encounters
            ("sessions", "Adventures/sessions"): [
                "**/Sessions/**/*.md",
                "**/06_Sessions/**/*.md",
                "**/Session_Notes/**/*.md"
            ],
            
            # Quests and adventures
            ("quests", "Adventures/quests"): [
                "**/Quests/**/*.md",
                "**/Adventures/**/*.md",
                "**/01_Adventures/**/*.md"
            ],
            
            # Rules and mechanics
            ("mechanics", "Rules/mechanics"): [
                "**/Mechanics/**/*.md",
                "**/Rules/**/*.md",
                "**/03_Mechanics/**/*.md",
                "**/Combat/**/*.md"
            ],
            
            # Maps and assets
            ("maps", "Resources/maps"): [
                "**/Maps/**/*",
                "**/Battle_Maps/**/*",
                "**/04_Resources/Assets/Maps/**/*"
            ],
            
            # Templates and automation
            ("templates", "System/templates"): [
                "**/Templates/**/*.md",
                "**/template*.md",
                "**/Automation/**/*.md"
            ]
        }
        
        for (content_type, target_dir), patterns in consolidation_map.items():
            target_path = self.vault_path / target_dir
            consolidated_count = 0
            
            for pattern in patterns:
                for file_path in self.vault_path.glob(pattern):
                    if file_path.is_file() and not file_path.is_relative_to(target_path):
                        # Generate unique name if file already exists
                        dest_path = target_path / file_path.name
                        if dest_path.exists():
                            stem = file_path.stem
                            suffix = file_path.suffix
                            counter = 1
                            while dest_path.exists():
                                dest_path = target_path / f"{stem}_{counter}{suffix}"
                                counter += 1
                        
                        try:
                            shutil.move(str(file_path), str(dest_path))
                            self.moves_log.append({
                                "from": str(file_path.relative_to(self.vault_path)),
                                "to": str(dest_path.relative_to(self.vault_path)),
                                "type": content_type
                            })
                            consolidated_count += 1
                        except Exception as e:
                            print(f"    ⚠️ Could not move {file_path.name}: {e}")
            
            if consolidated_count > 0:
                print(f"  ✓ Consolidated {consolidated_count} {content_type} files")
                
    def flatten_deep_nesting(self):
        """Flatten excessively nested directories"""
        print("\n📦 Flattening deep nesting...")
        
        flattened_count = 0
        
        for root, dirs, files in os.walk(self.vault_path):
            level = root.replace(str(self.vault_path), '').count(os.sep)
            
            # If directory is more than 3 levels deep
            if level > 3 and files:
                root_path = Path(root)
                
                # Determine best target location based on content
                target_dir = self.determine_target_directory(root_path, files)
                
                if target_dir:
                    for file in files:
                        source = root_path / file
                        dest = self.vault_path / target_dir / file
                        
                        # Handle naming conflicts
                        if dest.exists():
                            stem = Path(file).stem
                            suffix = Path(file).suffix
                            parent_name = root_path.parent.name
                            dest = self.vault_path / target_dir / f"{parent_name}_{stem}{suffix}"
                        
                        try:
                            shutil.move(str(source), str(dest))
                            self.moves_log.append({
                                "from": str(source.relative_to(self.vault_path)),
                                "to": str(dest.relative_to(self.vault_path)),
                                "reason": "deep_nesting"
                            })
                            flattened_count += 1
                        except Exception as e:
                            print(f"    ⚠️ Could not flatten {file}: {e}")
        
        print(f"  ✓ Flattened {flattened_count} deeply nested files")
        
    def determine_target_directory(self, path, files):
        """Determine best target directory based on content"""
        path_str = str(path).lower()
        
        # Check path components for hints
        if any(x in path_str for x in ['npc', 'character', 'people']):
            return "World/npcs"
        elif any(x in path_str for x in ['location', 'place', 'city', 'town']):
            return "World/locations"
        elif any(x in path_str for x in ['session', 'game', 'play']):
            return "Adventures/sessions"
        elif any(x in path_str for x in ['quest', 'adventure', 'mission']):
            return "Adventures/quests"
        elif any(x in path_str for x in ['rule', 'mechanic', 'combat']):
            return "Rules/mechanics"
        elif any(x in path_str for x in ['map', 'battle', 'grid']):
            return "Resources/maps"
        elif any(x in path_str for x in ['template', 'automation']):
            return "System/templates"
        elif any(x in path_str for x in ['index', 'dashboard', 'overview']):
            return "System/indexes"
        elif any(x in path_str for x in ['player', 'pc', 'party']):
            return "Characters/pcs"
        elif any(x in path_str for x in ['archive', 'old', 'backup']):
            return "Archive/old-versions"
        else:
            # Check file content for hints
            for file in files[:3]:  # Sample first 3 files
                if file.endswith('.md'):
                    try:
                        content = (path / file).read_text(encoding='utf-8')[:500]
                        if 'tags: [npc' in content:
                            return "World/npcs"
                        elif 'tags: [location' in content:
                            return "World/locations"
                        elif 'tags: [session' in content:
                            return "Adventures/sessions"
                    except:
                        pass
            
            return "Archive/old-versions"  # Default for unknown content
            
    def remove_empty_directories(self):
        """Remove empty directories after reorganization"""
        print("\n🧹 Cleaning up empty directories...")
        
        removed_count = 0
        
        # Multiple passes to catch nested empty dirs
        for _ in range(5):
            for root, dirs, files in os.walk(self.vault_path, topdown=False):
                if not files and not dirs:
                    try:
                        os.rmdir(root)
                        removed_count += 1
                    except:
                        pass
                        
        print(f"  ✓ Removed {removed_count} empty directories")
        
    def update_internal_links(self):
        """Update internal links to reflect new structure"""
        print("\n🔗 Updating internal links...")
        
        # Build mapping of old to new paths
        path_mapping = {}
        for move in self.moves_log:
            old_name = Path(move['from']).stem
            new_path = move['to']
            path_mapping[old_name] = new_path
        
        updated_files = 0
        
        for md_file in self.vault_path.glob("**/*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content
                
                # Update wiki links
                for old_name, new_path in path_mapping.items():
                    # Simple wiki link
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\]\]',
                        f'[[{Path(new_path).stem}]]',
                        content
                    )
                    # Wiki link with alias
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\|([^\]]+)\]\]',
                        rf'[[{Path(new_path).stem}|\1]]',
                        content
                    )
                
                if content != original_content:
                    md_file.write_text(content, encoding='utf-8')
                    updated_files += 1
                    
            except Exception as e:
                print(f"    ⚠️ Could not update links in {md_file.name}: {e}")
                
        print(f"  ✓ Updated links in {updated_files} files")
        
    def create_navigation_index(self):
        """Create new navigation index for flattened structure"""
        print("\n📑 Creating navigation index...")
        
        index_content = """---
tags: [index, navigation, reorganized]
created: {date}
---

# 🗂️ Vault Navigation (Reorganized)

## 📊 New Structure Overview

The vault has been reorganized into a flatter, more intuitive structure:

### 🎮 Adventures
- **campaigns** - Active campaigns and storylines
- **sessions** - Session notes and logs  
- **quests** - Quest descriptions and tracking
- **encounters** - Encounter designs and stats

### 🌍 World
- **locations** - All places and settings
- **npcs** - Non-player characters
- **factions** - Organizations and groups
- **lore** - World history and mythology
- **timeline** - Chronological events

### 📖 Rules  
- **mechanics** - Game rules and systems
- **homebrew** - Custom rules and content
- **quick-reference** - Fast lookup guides

### 🎨 Resources
- **maps** - Battle maps and world maps
- **assets** - Images and media
- **handouts** - Player handouts
- **tables** - Random tables and generators

### 👥 Characters
- **pcs** - Player characters
- **party** - Party resources and tracking
- **sheets** - Character sheets
- **backstories** - Character histories

### ⚙️ System
- **indexes** - Navigation and organization
- **dashboards** - Overview pages
- **templates** - Note templates
- **automation** - Scripts and queries
- **metadata** - Vault configuration

### 📦 Archive
- **old-versions** - Previous versions
- **backups** - Backup copies
- **deprecated** - Outdated content

## 🔄 Reorganization Summary

- **Files Moved**: {total_moves}
- **Directories Flattened**: {dirs_flattened}  
- **Empty Directories Removed**: {empty_removed}
- **Links Updated**: {links_updated}

## 🎯 Quick Access

### Most Used
```dataview
TABLE file.folder as "Location"
FROM ""
SORT file.mtime DESC
LIMIT 10
```

### Recently Modified
```dataview
TABLE file.mtime as "Modified"
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```

### By Category
- [[World/npcs]] - All NPCs
- [[World/locations]] - All Locations
- [[Adventures/quests]] - Active Quests
- [[Adventures/sessions]] - Session Notes
- [[Rules/mechanics]] - Game Rules

---
*Vault reorganized on {date}*
""".format(
            date=datetime.now().strftime("%Y-%m-%d"),
            total_moves=len(self.moves_log),
            dirs_flattened=self.stats['deeply_nested'],
            empty_removed=self.stats.get('empty_removed', 0),
            links_updated=self.stats.get('links_updated', 0)
        )
        
        index_path = self.vault_path / "System" / "indexes" / "VAULT_NAVIGATION.md"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(index_content, encoding='utf-8')
        
        print(f"  ✓ Created navigation index at {index_path.relative_to(self.vault_path)}")
        
    def save_reorganization_log(self):
        """Save detailed log of all reorganization actions"""
        print("\n💾 Saving reorganization log...")
        
        log_path = self.vault_path / "System" / "metadata" / f"reorganization_log_{self.timestamp}.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        log_data = {
            "timestamp": self.timestamp,
            "stats": dict(self.stats),
            "moves": self.moves_log,
            "new_structure": self.new_structure
        }
        
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
            
        print(f"  ✓ Saved log to {log_path.relative_to(self.vault_path)}")
        
    def run(self):
        """Execute complete vault reorganization"""
        print("=" * 60)
        print("🔧 VAULT FLATTENER & REORGANIZER")
        print("=" * 60)
        
        # Phase 1: Analysis
        self.analyze_current_structure()
        
        # Phase 2: Create new structure
        self.create_flat_structure()
        
        # Phase 3: Consolidate content
        self.consolidate_similar_content()
        
        # Phase 4: Flatten deep nesting
        self.flatten_deep_nesting()
        
        # Phase 5: Clean up
        self.remove_empty_directories()
        self.stats['empty_removed'] = self.stats.get('empty_removed', 0)
        
        # Phase 6: Update links
        self.update_internal_links()
        
        # Phase 7: Create navigation
        self.create_navigation_index()
        
        # Phase 8: Save log
        self.save_reorganization_log()
        
        print("\n" + "=" * 60)
        print("✅ REORGANIZATION COMPLETE!")
        print("=" * 60)
        print(f"📊 Final Statistics:")
        print(f"  • Files reorganized: {len(self.moves_log)}")
        print(f"  • New structure created with {len(self.new_structure)} main categories")
        print(f"  • Vault is now flatter and more organized!")
        print("\n📍 Next steps:")
        print("  1. Review System/indexes/VAULT_NAVIGATION.md")
        print("  2. Check that all important files are accessible")
        print("  3. Update any bookmarks or saved searches")
        print("  4. Enjoy your simplified vault structure!")
        

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    reorganizer = VaultFlattenerReorganizer(vault_path)
    reorganizer.run()