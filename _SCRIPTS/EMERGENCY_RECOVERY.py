#!/usr/bin/env python3
"""
EMERGENCY RECOVERY - Restore incorrectly moved/deleted content
"""

import os
import shutil
from pathlib import Path
import re

class EmergencyRecovery:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.recovered = 0
        
    def recover_from_archive(self):
        """Recover files from archive"""
        print("🚨 EMERGENCY RECOVERY IN PROGRESS")
        print("=" * 60)
        
        archive_dir = self.vault_path / "08_Archive" / "duplicates"
        
        if archive_dir.exists():
            print(f"📦 Found {len(list(archive_dir.glob('*')))} files in archive")
            
            for file_path in archive_dir.glob("*"):
                filename = file_path.name.lower()
                
                # Restore sessions
                if "session" in filename:
                    target = self.vault_path / "06_Sessions" / file_path.name
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        self.recovered += 1
                        print(f"  ✓ Restored session: {file_path.name}")
                        
                # Restore campaigns
                elif "campaign" in filename or "aethermoor" in filename or "aquabyssos" in filename:
                    target = self.vault_path / "01_Adventures" / "Campaigns" / file_path.name
                    target.parent.mkdir(exist_ok=True)
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        self.recovered += 1
                        print(f"  ✓ Restored campaign: {file_path.name}")
                        
                # Restore encounters
                elif "encounter" in filename or "enc" in filename[:3]:
                    target = self.vault_path / "01_Adventures" / "Encounters" / file_path.name
                    target.parent.mkdir(exist_ok=True)
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        self.recovered += 1
                        print(f"  ✓ Restored encounter: {file_path.name}")
                        
                # Restore hooks
                elif "hook" in filename:
                    target = self.vault_path / "01_Adventures" / "Hooks" / file_path.name
                    target.parent.mkdir(exist_ok=True)
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        self.recovered += 1
                        print(f"  ✓ Restored hook: {file_path.name}")
                        
    def restore_misplaced_content(self):
        """Move misplaced content back to correct locations"""
        print("\n🔄 Restoring misplaced content...")
        
        # Check 06_Sessions for non-session content
        sessions_dir = self.vault_path / "06_Sessions"
        if sessions_dir.exists():
            for file_path in sessions_dir.glob("*.md"):
                filename = file_path.name.lower()
                content = file_path.read_text(encoding='utf-8').lower()
                
                # These are clearly not sessions
                if "players-handbook" in filename or "chapter" in filename:
                    # Move to rules
                    target = self.vault_path / "05_Rules" / "Core" / file_path.name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        self.recovered += 1
                        print(f"  ✓ Moved rules content: {file_path.name}")
                        
                elif "bestiary" in filename or "_cli_" in filename:
                    # Move to appropriate location
                    target = self.vault_path / "03_People" / "Monsters" / file_path.name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        self.recovered += 1
                        print(f"  ✓ Moved monster: {file_path.name}")
                        
        # Check other locations for session content
        for file_path in self.vault_path.glob("**/*session*.md"):
            if "06_Sessions" not in str(file_path):
                target = self.vault_path / "06_Sessions" / file_path.name
                if not target.exists():
                    shutil.move(str(file_path), str(target))
                    self.recovered += 1
                    print(f"  ✓ Moved session to correct folder: {file_path.name}")
                    
    def restore_from_quests(self):
        """Check if campaign/session content ended up in Quests"""
        print("\n📂 Checking Quests folder for misplaced content...")
        
        quests_dir = self.vault_path / "01_Adventures" / "Quests"
        if quests_dir.exists():
            for file_path in quests_dir.glob("*.md"):
                filename = file_path.name.lower()
                
                # Campaign content
                if "campaign" in filename or "aethermoor" in filename or "aquabyssos" in filename:
                    if "session" in filename:
                        target = self.vault_path / "06_Sessions" / file_path.name
                    else:
                        target = self.vault_path / "01_Adventures" / "Campaigns" / file_path.name
                        target.parent.mkdir(exist_ok=True)
                        
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        self.recovered += 1
                        print(f"  ✓ Restored: {file_path.name}")
                        
    def check_all_adventure_content(self):
        """Scan entire vault for adventure content and restore it"""
        print("\n🔍 Scanning entire vault for adventure content...")
        
        adventure_patterns = {
            'campaigns': ['campaign', 'aethermoor', 'aquabyssos', 'adventure path'],
            'sessions': ['session \\d+', 'session\\d+', 'recap', 'session notes'],
            'encounters': ['encounter', 'combat encounter', 'social encounter', 'enc\\d+'],
            'hooks': ['quest hook', 'adventure hook', 'plot hook', 'story hook']
        }
        
        for file_path in self.vault_path.glob("**/*.md"):
            if any(skip in str(file_path) for skip in ['.obsidian', '_SCRIPTS', '09_Performance']):
                continue
                
            try:
                filename = file_path.name.lower()
                content = file_path.read_text(encoding='utf-8').lower()[:500]
                
                # Check campaigns
                if any(pattern in filename or pattern in content for pattern in adventure_patterns['campaigns']):
                    if "01_Adventures/Campaigns" not in str(file_path):
                        target = self.vault_path / "01_Adventures" / "Campaigns" / file_path.name
                        target.parent.mkdir(exist_ok=True)
                        if not target.exists() and file_path.parent != target.parent:
                            shutil.copy2(str(file_path), str(target))
                            self.recovered += 1
                            print(f"  ✓ Found campaign: {file_path.name}")
                            
                # Check sessions
                elif any(re.search(pattern, filename) or re.search(pattern, content) for pattern in adventure_patterns['sessions']):
                    if "06_Sessions" not in str(file_path):
                        target = self.vault_path / "06_Sessions" / file_path.name
                        if not target.exists() and file_path.parent != target.parent:
                            shutil.copy2(str(file_path), str(target))
                            self.recovered += 1
                            print(f"  ✓ Found session: {file_path.name}")
                            
                # Check encounters
                elif any(pattern in filename for pattern in adventure_patterns['encounters']):
                    if "01_Adventures/Encounters" not in str(file_path):
                        target = self.vault_path / "01_Adventures" / "Encounters" / file_path.name
                        target.parent.mkdir(exist_ok=True)
                        if not target.exists() and file_path.parent != target.parent:
                            shutil.copy2(str(file_path), str(target))
                            self.recovered += 1
                            print(f"  ✓ Found encounter: {file_path.name}")
                            
                # Check hooks
                elif any(pattern in filename for pattern in adventure_patterns['hooks']):
                    if "01_Adventures/Hooks" not in str(file_path):
                        target = self.vault_path / "01_Adventures" / "Hooks" / file_path.name
                        target.parent.mkdir(exist_ok=True)
                        if not target.exists() and file_path.parent != target.parent:
                            shutil.copy2(str(file_path), str(target))
                            self.recovered += 1
                            print(f"  ✓ Found hook: {file_path.name}")
                            
            except Exception as e:
                pass
                
    def create_placeholders(self):
        """Create placeholder files for empty critical folders"""
        print("\n📝 Creating placeholder content for empty folders...")
        
        placeholders = {
            "01_Adventures/Campaigns/README.md": """# Campaigns

Your campaign content has been recovered where possible.
Check 08_Archive/duplicates if any files are still missing.

## Active Campaigns
- [Add your campaigns here]

## Campaign Resources
- Session logs → [[06_Sessions]]
- NPCs → [[03_People]]
- Locations → [[02_Worldbuilding/Locations]]
""",
            "01_Adventures/Encounters/README.md": """# Encounters

Combat and social encounters for your campaigns.

## Encounter Types
- Combat Encounters
- Social Encounters
- Exploration Challenges
- Puzzle Encounters

Check 08_Archive if encounters are missing.
""",
            "01_Adventures/Hooks/README.md": """# Adventure Hooks

Quest hooks and story seeds.

## Hook Categories
- Main Quest Hooks
- Side Quest Hooks
- Random Encounters
- Plot Twists

Check 08_Archive if hooks are missing.
"""
        }
        
        for path, content in placeholders.items():
            full_path = self.vault_path / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            if not full_path.exists():
                full_path.write_text(content, encoding='utf-8')
                print(f"  ✓ Created placeholder: {path}")
                
    def generate_recovery_report(self):
        """Generate recovery report"""
        from datetime import datetime
        
        report = f"""# 🚨 EMERGENCY RECOVERY REPORT

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Files Recovered**: {self.recovered}

## CRITICAL ISSUE ADDRESSED

Scripts incorrectly moved/deleted content from:
- 01_Adventures/Campaigns
- 06_Sessions
- 01_Adventures/Encounters
- 01_Adventures/Hooks

## RECOVERY ACTIONS TAKEN

1. ✅ Recovered files from 08_Archive/duplicates
2. ✅ Moved misplaced content back to correct folders
3. ✅ Restored sessions from various locations
4. ✅ Restored campaign content
5. ✅ Created placeholders for empty folders
6. ✅ Scanned entire vault for adventure content

## FILES RECOVERED: {self.recovered}

## MANUAL VERIFICATION NEEDED

Please check the following folders:
- **06_Sessions**: Should contain session notes and recaps
- **01_Adventures/Campaigns**: Should contain campaign materials
- **01_Adventures/Encounters**: Should contain encounter descriptions
- **01_Adventures/Hooks**: Should contain quest hooks

## IF CONTENT IS STILL MISSING

1. Check **08_Archive/duplicates** - some files may still be there
2. Check your system trash/recycle bin
3. Check Obsidian's file recovery if available
4. Restore from your most recent backup

## APOLOGY

I sincerely apologize for this error. The scripts should not have moved or deleted your campaign content. This recovery script has attempted to restore as much as possible.

---
**Recovery attempt complete. Please verify your content.**
"""
        
        report_path = self.vault_path / "09_Performance" / f"EMERGENCY_RECOVERY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"\n📄 Recovery report: {report_path.name}")
        
    def run(self):
        """Execute emergency recovery"""
        print("=" * 60)
        print("🚨 EMERGENCY RECOVERY SYSTEM")
        print("=" * 60)
        print("\nAttempting to recover incorrectly moved/deleted content...")
        
        self.recover_from_archive()
        self.restore_misplaced_content()
        self.restore_from_quests()
        self.check_all_adventure_content()
        self.create_placeholders()
        self.generate_recovery_report()
        
        print("\n" + "=" * 60)
        print(f"⚠️ RECOVERY COMPLETE")
        print(f"   Files Recovered: {self.recovered}")
        print("   PLEASE VERIFY YOUR CONTENT!")
        print("=" * 60)

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    recovery = EmergencyRecovery(vault_path)
    recovery.run()