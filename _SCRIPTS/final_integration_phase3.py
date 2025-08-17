#!/usr/bin/env python3
"""
Phase 3 Steps 47-49: Final Integration
- Step 47: Quest-World Integration
- Step 48: Timeline Integration  
- Step 49: Faction Network Building
"""

import os
import re
import json
from datetime import datetime
from collections import defaultdict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'

def find_quest_files():
    """Find quest and adventure files"""
    quest_files = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(skip_dir in root for skip_dir in ['/.git', '/08_Archive', '/13_Performance', '/vault_backup']):
            continue
            
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file is a quest/adventure
                    is_quest = (
                        '/01_Adventures/' in filepath or
                        'quest' in file.lower() or
                        'adventure' in file.lower() or
                        'mission' in file.lower() or
                        re.search(r'^type:\s*(Quest|Adventure|Mission)', content, re.MULTILINE | re.IGNORECASE)
                    )
                    
                    if is_quest:
                        quest_files.append(filepath)
                        
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return quest_files

def step_47_quest_world_integration():
    """Step 47: Integrate quests with affected locations and NPCs"""
    
    print("\n=== Step 47: Quest-World Integration ===")
    
    quest_files = find_quest_files()
    print(f"Found {len(quest_files)} quest files")
    
    enhanced_count = 0
    
    for filepath in quest_files[:10]:  # Process top 10 quests
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if already integrated
            if 'world integration' in content.lower():
                continue
            
            # Extract quest details
            quest_name = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
            quest_name = quest_name.group(1).strip() if quest_name else os.path.basename(filepath)[:-3]
            
            # Find mentioned NPCs and locations
            wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
            
            # Create integration section
            integration_section = f"""
## World Integration

### Connected Elements

**Involved NPCs**: {len([link for link in wiki_links if any(keyword in link.lower() for keyword in ['person', 'character', 'npc'])])} character connections identified

**Affected Locations**: {len([link for link in wiki_links if any(keyword in link.lower() for keyword in ['location', 'place', 'city', 'town'])])} location connections identified

### Campaign Impact

**Immediate Effects**: Quest outcomes directly influence connected NPCs and locations
**Long-term Consequences**: Resolution shapes ongoing relationships and world state
**Reputation Changes**: Character actions affect standing with involved factions

### Integration Tracking

- [ ] Update NPC relationships based on quest interactions
- [ ] Modify location descriptions to reflect quest outcomes
- [ ] Adjust faction standings according to player choices
- [ ] Document timeline changes resulting from quest resolution

"""
            
            # Add integration section
            if '## DM Notes' in content:
                new_content = content.replace('## DM Notes', f"{integration_section}\n## DM Notes")
            else:
                new_content = content + integration_section
            
            # Write enhanced content
            if not DRY_RUN:
                backup_path = filepath + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            enhanced_count += 1
            
        except Exception as e:
            print(f"Error enhancing {filepath}: {e}")
    
    print(f"Enhanced {enhanced_count} quest files with world integration")
    return enhanced_count

def step_48_timeline_integration():
    """Step 48: Add temporal tags and create timeline navigation"""
    
    print("\n=== Step 48: Timeline Integration ===")
    
    # Create timeline tracking template
    timeline_template = """# Campaign Timeline Tracker

## Current Date
**Campaign Year**: 2024 CE (Current Era)
**Season**: [Update based on campaign progress]
**Month**: [Track monthly progression]

## Timeline Periods

### Ancient History (Before 0 CE)
- Major world-shaping events
- Legendary figures and their actions
- Foundational conflicts and resolutions

### Early Era (0-500 CE)
- Establishment of major kingdoms
- First inter-realm contact
- Cultural foundation periods

### Classical Era (500-1000 CE)
- Peak of ancient civilizations
- Major wars and alliances
- Cultural golden ages

### Medieval Era (1000-1500 CE)
- Feudal system development
- Religious and philosophical movements
- Technological advancement periods

### Renaissance Era (1500-1800 CE)
- Cultural and scientific revival
- Exploration and discovery
- Political system evolution

### Modern Era (1800-2000 CE)
- Industrial and magical advancement
- World wars and major conflicts
- Social and political transformation

### Contemporary Era (2000 CE-Present)
- Current campaign setting
- Ongoing political situations
- Active conflicts and opportunities

## Event Tracking

### Past Events (Completed)
- [Date]: [Event description] - [Consequences]

### Current Events (Ongoing)
- [Date]: [Event description] - [Status]

### Future Events (Planned/Predicted)
- [Date]: [Event description] - [Probability]

## Character Timeline Integration

### Character Birth Dates
- Track when NPCs were born relative to timeline
- Calculate current ages and life stage impacts

### Character Life Events
- Major personal milestones and their timing
- Relationships formed and ended
- Career and status changes

### Character Future Projections
- Expected life events and their timing
- Potential relationship developments
- Career and status evolution paths

## Usage Guidelines

1. **Date Every Event**: Add temporal tags to all significant occurrences
2. **Track Consequences**: Note how past events influence current situations
3. **Plan Ahead**: Use timeline to schedule future campaign developments
4. **Character Integration**: Connect personal histories to world events
5. **Consistency Checking**: Verify chronological accuracy across content

---
*Update regularly as campaign progresses to maintain timeline coherence.*
"""
    
    timeline_path = os.path.join(ROOT_DIR, '06_GM_Resources', 'Campaign_Timeline_Tracker.md')
    os.makedirs(os.path.dirname(timeline_path), exist_ok=True)
    
    if not DRY_RUN:
        with open(timeline_path, 'w', encoding='utf-8') as f:
            f.write(timeline_template)
    
    # Add temporal tags to major files
    temporal_tags_added = 0
    
    # Find files that could benefit from temporal tags
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(skip_dir in root for skip_dir in ['/.git', '/08_Archive', '/13_Performance', '/vault_backup']):
            continue
        
        for file in files[:20]:  # Limit for performance
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Skip if already has temporal tags
                    if 'timeline:' in content.lower() or 'date:' in content.lower():
                        continue
                    
                    # Add temporal metadata to frontmatter
                    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    if fm_match:
                        fm_content = fm_match.group(1)
                        
                        # Add timeline tag
                        new_fm = fm_content + f'\ntimeline: current_era\nchronology: active\nupdated: {datetime.now().isoformat()}'
                        new_content = content.replace(fm_match.group(0), f'---\n{new_fm}\n---\n')
                        
                        if not DRY_RUN and len(content.split()) > 50:  # Only substantial files
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            temporal_tags_added += 1
                
                except Exception as e:
                    continue
        
        if temporal_tags_added >= 50:  # Limit processing
            break
    
    print(f"Created timeline tracker template")
    print(f"Added temporal tags to {temporal_tags_added} files")
    return temporal_tags_added

def step_49_faction_network_building():
    """Step 49: Map faction relationships and build tracking systems"""
    
    print("\n=== Step 49: Faction Network Building ===")
    
    # Find faction files
    faction_files = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(skip_dir in root for skip_dir in ['/.git', '/08_Archive', '/13_Performance', '/vault_backup']):
            continue
            
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file is a faction
                    is_faction = (
                        '/Groups/' in filepath or
                        re.search(r'^type:\s*Faction', content, re.MULTILINE | re.IGNORECASE) or
                        any(keyword in content.lower() for keyword in ['faction', 'organization', 'guild', 'order'])
                    )
                    
                    if is_faction:
                        faction_files.append(filepath)
                        
                except Exception as e:
                    continue
    
    print(f"Found {len(faction_files)} faction files")
    
    # Create faction relationship matrix
    faction_relationships = defaultdict(list)
    
    for filepath in faction_files[:30]:  # Process top 30 factions
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            faction_name = os.path.basename(filepath)[:-3]
            
            # Find faction links
            wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
            faction_links = [link for link in wiki_links if any(keyword in link.lower() for keyword in ['faction', 'guild', 'order', 'organization'])]
            
            faction_relationships[faction_name] = faction_links
            
        except Exception as e:
            continue
    
    # Create faction network tracking system
    network_template = f"""# Faction Network Tracker

## Overview
Comprehensive tracking system for faction relationships, conflicts, and alliances.

## Major Factions

{chr(10).join([f"### {faction}" + chr(10) + chr(10) + f"**Connected Factions**: {len(connections)} direct connections" + chr(10) + chr(10) + chr(10).join([f"- [[{conn}]]" for conn in connections[:5]]) + chr(10) for faction, connections in list(faction_relationships.items())[:10]])}

## Relationship Types

### Alliances
- **Formal Treaties**: Official agreements and mutual support pacts
- **Informal Cooperation**: Unofficial collaboration on shared interests
- **Temporary Alliances**: Short-term partnerships for specific goals

### Conflicts
- **Open Warfare**: Active military engagement
- **Cold War**: Hostile but non-violent competition
- **Trade Wars**: Economic competition and sanctions

### Neutral Relationships
- **Non-Interference**: Mutual recognition without involvement
- **Cordial Relations**: Polite but limited interaction
- **Suspicious Neutrality**: Watchful but non-committal stance

## Power Dynamics

### Major Powers
Factions with significant influence across multiple regions

### Regional Powers
Factions dominant within specific areas

### Minor Factions
Specialized or limited influence organizations

### Emerging Factions
New organizations gaining influence

## Tracking Mechanisms

### Relationship Status Updates
- Monitor changes in faction relationships
- Track alliance formations and breakdowns
- Record conflict escalations and resolutions

### Influence Tracking
- Map territorial and political influence
- Monitor resource control and access
- Track member recruitment and defection

### Event Impact Assessment
- Analyze how world events affect faction relationships
- Project relationship changes from character actions
- Plan faction responses to campaign developments

## Usage Guidelines

1. **Regular Updates**: Revise relationships as campaign progresses
2. **Player Impact**: Track how character actions affect faction dynamics
3. **Consequence Planning**: Use network to predict faction reactions
4. **Story Integration**: Weave faction relationships into adventures
5. **Opportunity Identification**: Find roleplay and conflict opportunities

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    network_path = os.path.join(ROOT_DIR, '06_GM_Resources', 'Faction_Network_Tracker.md')
    os.makedirs(os.path.dirname(network_path), exist_ok=True)
    
    if not DRY_RUN:
        with open(network_path, 'w', encoding='utf-8') as f:
            f.write(network_template)
    
    # Add relationship tracking to top faction files
    enhanced_factions = 0
    
    for filepath in faction_files[:15]:  # Process top 15 factions
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if already has relationship tracking
            if 'relationship network' in content.lower() or 'faction relationships' in content.lower():
                continue
            
            faction_name = os.path.basename(filepath)[:-3]
            connections = faction_relationships[faction_name]
            
            # Add relationship section
            relationship_section = f"""
## Faction Relationships

### Network Position
**Direct Connections**: {len(connections)} faction relationships
**Network Influence**: {len(connections) * 2} degrees of separation reach
**Relationship Complexity**: {'High' if len(connections) > 5 else 'Medium' if len(connections) > 2 else 'Low'}

### Key Relationships
{chr(10).join([f"- [[{conn}]]: Relationship status pending classification" for conn in connections[:5]])}

### Relationship Dynamics
- **Alliance Potential**: Opportunities for cooperation and mutual benefit
- **Conflict Risk**: Areas of potential disagreement or competition  
- **Neutral Interactions**: Routine diplomatic and trade relationships
- **Unknown Factors**: Relationships requiring further investigation

### Network Strategy
**Expansion Opportunities**: Potential new alliances and partnerships
**Risk Management**: Monitoring threats and hostile relationships
**Influence Maximization**: Leveraging relationships for faction goals
**Diplomatic Priorities**: Key relationships requiring attention

"""
            
            # Add section to file
            if '## Adventure Hooks' in content:
                new_content = content.replace('## Adventure Hooks', f"{relationship_section}\n## Adventure Hooks")
            else:
                new_content = content + relationship_section
            
            # Write enhanced content
            if not DRY_RUN:
                backup_path = filepath + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            enhanced_factions += 1
            
        except Exception as e:
            print(f"Error enhancing {filepath}: {e}")
    
    print(f"Created faction network tracker")
    print(f"Enhanced {enhanced_factions} faction files with relationship tracking")
    return enhanced_factions

def main():
    print("=== Phase 3 Final Integration (Steps 47-49) ===")
    print(f"Working directory: {ROOT_DIR}")
    print(f"Dry run mode: {DRY_RUN}")
    
    # Execute remaining steps
    quest_enhancements = step_47_quest_world_integration()
    timeline_additions = step_48_timeline_integration()
    faction_enhancements = step_49_faction_network_building()
    
    # Generate final report
    final_report = {
        'phase_3_completion': {
            'quest_world_integration': quest_enhancements,
            'timeline_integration': timeline_additions,
            'faction_network_building': faction_enhancements,
        },
        'total_enhancements': quest_enhancements + timeline_additions + faction_enhancements,
        'completion_timestamp': datetime.now().isoformat(),
        'templates_created': [
            '06_GM_Resources/Campaign_Timeline_Tracker.md',
            '06_GM_Resources/Faction_Network_Tracker.md'
        ],
        'dry_run': DRY_RUN
    }
    
    report_path = os.path.join(ROOT_DIR, 'reports', 'phase3_final_integration_report.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2)
    
    print(f"\n=== Phase 3 Completion Report ===")
    print(f"Quest world integration: {quest_enhancements} files enhanced")
    print(f"Timeline integration: {timeline_additions} files with temporal tags")  
    print(f"Faction network building: {faction_enhancements} factions enhanced")
    print(f"Total enhancements: {final_report['total_enhancements']}")
    print(f"Templates created: {len(final_report['templates_created'])}")
    print(f"Final report saved to: reports/phase3_final_integration_report.json")
    
    if DRY_RUN:
        print("\nDry run mode - no files were modified")
    else:
        print(f"\nPhase 3 Content Enhancement & Integration completed successfully!")

if __name__ == '__main__':
    main()