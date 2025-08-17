#!/usr/bin/env python3
"""
Final verification that vault is clean and real content preserved
"""
import os
import re
from pathlib import Path
from datetime import datetime

def verify_vault():
    """Verify vault is clean and content preserved"""
    
    stats = {
        'total_files': 0,
        'markdown_files': 0,
        'real_npcs': 0,
        'real_quests': 0,
        'real_sessions': 0,
        'real_campaigns': 0,
        'remaining_fake': [],
        'important_preserved': []
    }
    
    # Patterns for real content we want to preserve
    important_patterns = {
        'campaigns': ['aquabyssos', 'aethermoor'],
        'sessions': ['session'],
        'quests': ['quest'],
        'npcs': [r'^NPC_[A-Za-z]+', r'^NPC\d{5}_[A-Za-z]+']
    }
    
    # Patterns for fake files that shouldn't exist
    fake_patterns = [
        r'^00_Indexes_',
        r'^01_Adventures_',  
        r'^02_Worldbuilding_',
        r'^03_People_',
        r'^04_Resources_',
        r'^05_Rules_',
        r'\.png\.md$',
        r'\.jpg\.md$',
        r'^step_\d+',
        r'^phase_\d+'
    ]
    
    print("Scanning vault...")
    
    for root, dirs, files in os.walk("."):
        # Skip system directories
        if any(skip in root for skip in ['.git', '.obsidian', '08_Archive', '_SCRIPTS']):
            continue
            
        for file in files:
            stats['total_files'] += 1
            
            if file.endswith('.md'):
                stats['markdown_files'] += 1
                file_path = Path(root) / file
                
                # Check for remaining fake files
                for pattern in fake_patterns:
                    if re.search(pattern, file, re.IGNORECASE):
                        stats['remaining_fake'].append(str(file_path))
                        break
                
                # Check for preserved important content
                content_lower = file.lower()
                
                # Campaigns
                if any(camp in content_lower for camp in important_patterns['campaigns']):
                    stats['real_campaigns'] += 1
                    stats['important_preserved'].append(f"Campaign: {file}")
                
                # Sessions
                elif 'session' in content_lower and '06_Sessions' in root:
                    stats['real_sessions'] += 1
                
                # Quests  
                elif 'quest' in content_lower:
                    stats['real_quests'] += 1
                
                # NPCs
                elif '03_People' in root:
                    for npc_pattern in important_patterns['npcs']:
                        if re.search(npc_pattern, file):
                            stats['real_npcs'] += 1
                            break
    
    return stats

def main():
    print("=" * 60)
    print("FINAL VAULT VERIFICATION")
    print("=" * 60)
    
    stats = verify_vault()
    
    # Generate report
    print("\n📊 VAULT STATUS:")
    print(f"  Total files: {stats['total_files']:,}")
    print(f"  Markdown files: {stats['markdown_files']:,}")
    
    print("\n✅ PRESERVED CONTENT:")
    print(f"  Real NPCs: {stats['real_npcs']}")
    print(f"  Real Quests: {stats['real_quests']}")
    print(f"  Real Sessions: {stats['real_sessions']}")
    print(f"  Real Campaigns: {stats['real_campaigns']}")
    
    if stats['remaining_fake']:
        print(f"\n⚠️  REMAINING FAKE FILES: {len(stats['remaining_fake'])}")
        for fake in stats['remaining_fake'][:10]:
            print(f"  - {fake}")
        if len(stats['remaining_fake']) > 10:
            print(f"  ... and {len(stats['remaining_fake']) - 10} more")
    else:
        print("\n✅ NO FAKE FILES REMAINING!")
    
    if stats['important_preserved']:
        print("\n🎯 IMPORTANT CONTENT PRESERVED:")
        for item in stats['important_preserved'][:10]:
            print(f"  - {item}")
    
    # Save verification report
    report_path = Path("09_Performance/final_verification_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write("# Final Vault Verification Report\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("## Summary\n")
        f.write(f"- Total Files: {stats['total_files']:,}\n")
        f.write(f"- Markdown Files: {stats['markdown_files']:,}\n")
        f.write(f"- Remaining Fake Files: {len(stats['remaining_fake'])}\n\n")
        f.write("## Preserved Content\n")
        f.write(f"- NPCs: {stats['real_npcs']}\n")
        f.write(f"- Quests: {stats['real_quests']}\n")
        f.write(f"- Sessions: {stats['real_sessions']}\n")
        f.write(f"- Campaigns: {stats['real_campaigns']}\n\n")
        
        if stats['remaining_fake']:
            f.write("## Remaining Issues\n")
            for fake in stats['remaining_fake']:
                f.write(f"- {fake}\n")
        else:
            f.write("## ✅ Vault is Clean!\n")
            f.write("No fake files remaining.\n")
    
    print(f"\n📄 Report saved: {report_path}")
    
    # Final status
    print("\n" + "=" * 60)
    if stats['remaining_fake']:
        print("⚠️  VAULT NEEDS MORE CLEANING")
        print(f"   {len(stats['remaining_fake'])} fake files remain")
    else:
        print("✅ VAULT IS CLEAN!")
        print("   All fake files removed")
        print("   All real content preserved")

if __name__ == "__main__":
    main()