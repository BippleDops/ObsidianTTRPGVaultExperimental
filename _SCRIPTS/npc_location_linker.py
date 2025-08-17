#!/usr/bin/env python3
"""
Phase 3 Step 46: Character-Location Linking
Links NPCs to their primary locations and creates movement tracking
"""

import os
import re
import json
import random
from datetime import datetime
from collections import defaultdict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'

# Movement patterns by NPC role/type
MOVEMENT_PATTERNS = {
    'leader': {
        'primary_location': 'headquarters/throne room/office',
        'secondary_locations': ['meeting halls', 'ceremonial spaces', 'private quarters'],
        'travel_frequency': 'scheduled/formal occasions',
        'movement_style': 'accompanied by retinue, formal protocols'
    },
    'merchant': {
        'primary_location': 'shop/trading post/market stall',
        'secondary_locations': ['warehouses', 'guild halls', 'customer locations'],
        'travel_frequency': 'daily business routes',
        'movement_style': 'practical, carrying goods or documents'
    },
    'diplomat': {
        'primary_location': 'embassy/diplomatic quarters',
        'secondary_locations': ['meeting venues', 'cultural centers', 'neutral grounds'],
        'travel_frequency': 'mission-dependent',
        'movement_style': 'formal, with diplomatic immunity and protocol'
    },
    'scholar': {
        'primary_location': 'library/research facility/academy',
        'secondary_locations': ['archives', 'field research sites', 'colleague offices'],
        'travel_frequency': 'research-driven',
        'movement_style': 'laden with books and research materials'
    },
    'artisan': {
        'primary_location': 'workshop/studio/forge',
        'secondary_locations': ['material suppliers', 'customer locations', 'guild meetings'],
        'travel_frequency': 'supply and delivery runs',
        'movement_style': 'carrying tools and materials'
    },
    'military': {
        'primary_location': 'barracks/command post/garrison',
        'secondary_locations': ['training grounds', 'patrol routes', 'strategic positions'],
        'travel_frequency': 'duty schedules and deployments',
        'movement_style': 'disciplined formations, armed and armored'
    },
    'religious': {
        'primary_location': 'temple/shrine/monastery',
        'secondary_locations': ['community centers', 'pilgrimage sites', 'homes of faithful'],
        'travel_frequency': 'ceremonial calendar and pastoral duties',
        'movement_style': 'ceremonial robes, ritual items'
    },
    'criminal': {
        'primary_location': 'hideout/safehouse/underworld venue',
        'secondary_locations': ['job sites', 'fences', 'neutral meeting places'],
        'travel_frequency': 'covert operations',
        'movement_style': 'secretive, disguised, avoiding attention'
    }
}

# Daily schedule templates
DAILY_SCHEDULES = {
    'dawn': ['personal routine', 'planning', 'quiet work'],
    'morning': ['primary work', 'meetings', 'administrative tasks'],
    'midday': ['peak activity', 'public interactions', 'important business'],
    'afternoon': ['continued work', 'appointments', 'travel'],
    'evening': ['social activities', 'meals', 'relaxation'],
    'night': ['rest', 'private time', 'special activities']
}

def find_npc_files():
    """Find all NPC files in the vault"""
    npc_files = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip certain directories
        if any(skip_dir in root for skip_dir in ['/.git', '/08_Archive', '/13_Performance', '/vault_backup']):
            continue
            
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file is an NPC
                    is_npc = (
                        re.search(r'^type:\s*(NPC|Person|Character)\s*$', content, re.MULTILINE | re.IGNORECASE) or
                        '/People/' in filepath or
                        '/NPCs/' in filepath
                    )
                    
                    if is_npc:
                        npc_files.append(filepath)
                        
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return npc_files

def find_location_files():
    """Find all location files in the vault"""
    location_files = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip certain directories
        if any(skip_dir in root for skip_dir in ['/.git', '/08_Archive', '/13_Performance', '/vault_backup']):
            continue
            
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file is a location
                    is_location = (
                        re.search(r'^type:\s*Location\s*$', content, re.MULTILINE | re.IGNORECASE) or
                        '/Places/' in filepath or
                        '/Locations/' in filepath
                    )
                    
                    if is_location:
                        location_files.append(filepath)
                        
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return location_files

def extract_npc_role(content):
    """Extract NPC role/profession from content"""
    content_lower = content.lower()
    
    # Role keywords mapping to movement patterns
    role_keywords = {
        'leader': ['leader', 'ruler', 'king', 'queen', 'emperor', 'empress', 'chief', 'commander', 'captain', 'mayor', 'governor'],
        'merchant': ['merchant', 'trader', 'shopkeeper', 'vendor', 'businessman', 'broker', 'dealer'],
        'diplomat': ['diplomat', 'ambassador', 'envoy', 'negotiator', 'liaison', 'representative'],
        'scholar': ['scholar', 'researcher', 'professor', 'librarian', 'sage', 'archivist', 'academic'],
        'artisan': ['artisan', 'craftsman', 'smith', 'builder', 'artist', 'engineer', 'architect'],
        'military': ['soldier', 'guard', 'knight', 'warrior', 'officer', 'sergeant', 'general'],
        'religious': ['priest', 'cleric', 'monk', 'oracle', 'chaplain', 'bishop', 'abbot'],
        'criminal': ['thief', 'assassin', 'smuggler', 'criminal', 'bandit', 'pirate', 'spy']
    }
    
    # Check for role keywords
    for role, keywords in role_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            return role
    
    # Default role based on common patterns
    if any(word in content_lower for word in ['work', 'job', 'profession', 'business']):
        return 'artisan'  # Generic worker
    else:
        return 'merchant'  # Default fallback

def extract_current_locations(content):
    """Extract currently mentioned locations from NPC content"""
    locations = []
    
    # Find all wiki links
    wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
    
    # Filter for likely location links
    location_indicators = [
        'hall', 'tower', 'district', 'quarter', 'market', 'square',
        'temple', 'palace', 'castle', 'fortress', 'academy', 'library',
        'shop', 'tavern', 'inn', 'guild', 'port', 'harbor'
    ]
    
    for link in wiki_links:
        link_lower = link.lower()
        if any(indicator in link_lower for indicator in location_indicators):
            locations.append(link)
    
    return locations

def has_location_tracking(content):
    """Check if NPC already has location/movement tracking"""
    tracking_indicators = [
        'primary location', 'movement patterns', 'daily schedule', 'typical locations',
        'can be found', 'usually located', 'movement tracking', 'location history'
    ]
    
    return any(indicator in content.lower() for indicator in tracking_indicators)

def generate_location_tracking_section(npc_name, npc_role, existing_locations):
    """Generate comprehensive location and movement tracking"""
    
    pattern = MOVEMENT_PATTERNS.get(npc_role, MOVEMENT_PATTERNS['merchant'])
    
    section_parts = []
    
    # Introduction
    section_parts.append(f"{npc_name}'s location and movement patterns reflect their role as a {npc_role}, with established routines and predictable presence in key locations.")
    section_parts.append("")
    
    # Primary location
    section_parts.append("### Primary Location")
    if existing_locations:
        primary_loc = existing_locations[0]
        section_parts.append(f"**[[{primary_loc}]]** - Main base of operations")
    else:
        section_parts.append(f"**{pattern['primary_location'].title()}** - Main base of operations")
    section_parts.append(f"- Typically found here during {pattern['travel_frequency']}")
    section_parts.append(f"- Movement style: {pattern['movement_style']}")
    section_parts.append("")
    
    # Secondary locations
    section_parts.append("### Secondary Locations")
    if len(existing_locations) > 1:
        for i, loc in enumerate(existing_locations[1:], 1):
            section_parts.append(f"**[[{loc}]]** - Regular destination {i}")
    else:
        for i, location_type in enumerate(pattern['secondary_locations'][:2], 1):
            section_parts.append(f"**{location_type.title()}** - Regular destination {i}")
    section_parts.append("")
    
    # Daily schedule
    section_parts.append("### Daily Schedule")
    section_parts.append("")
    
    schedule_activities = {
        'dawn': random.choice(DAILY_SCHEDULES['dawn']),
        'morning': random.choice(DAILY_SCHEDULES['morning']),
        'midday': random.choice(DAILY_SCHEDULES['midday']),
        'afternoon': random.choice(DAILY_SCHEDULES['afternoon']),
        'evening': random.choice(DAILY_SCHEDULES['evening']),
        'night': random.choice(DAILY_SCHEDULES['night'])
    }
    
    for time_period, activity in schedule_activities.items():
        section_parts.append(f"**{time_period.title()}**: {activity.title()}")
    
    section_parts.append("")
    
    # Movement patterns
    section_parts.append("### Movement Patterns")
    section_parts.append("")
    section_parts.append(f"**Travel Frequency**: {pattern['travel_frequency'].title()}")
    section_parts.append(f"**Movement Style**: {pattern['movement_style'].title()}")
    section_parts.append("**Predictability**: Regular patterns with occasional variations")
    section_parts.append("**Accessibility**: Varies by location and circumstances")
    section_parts.append("")
    
    # Encounter likelihood
    section_parts.append("### Encounter Likelihood")
    section_parts.append("")
    section_parts.append("**Primary Location**: High probability during business hours")
    section_parts.append("**Secondary Locations**: Medium probability during specific activities")  
    section_parts.append("**Travel Routes**: Low probability, but possible during transitions")
    section_parts.append("**Random Encounters**: Very low probability in unexpected locations")
    section_parts.append("")
    
    # Special circumstances
    section_parts.append("### Special Circumstances")
    section_parts.append("")
    section_parts.append("**Seasonal Variations**: Schedule may change with events or seasons")
    section_parts.append("**Emergency Protocols**: Alternative locations during crises")
    section_parts.append("**Social Events**: May be found at community gatherings")
    section_parts.append("**Private Time**: Limited access during personal hours")
    
    return "\n".join(section_parts)

def enhance_npc_with_location_tracking(filepath):
    """Add location and movement tracking to an NPC file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has location tracking
        if has_location_tracking(content):
            print(f"Location tracking already present in {os.path.basename(filepath)}")
            return False
        
        # Skip very short files
        if len(content.split()) < 100:
            print(f"Skipping short file {os.path.basename(filepath)}")
            return False
        
        # Extract NPC information
        npc_name = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
        npc_name = npc_name.group(1).strip() if npc_name else os.path.basename(filepath)[:-3]
        
        npc_role = extract_npc_role(content)
        existing_locations = extract_current_locations(content)
        
        # Generate location tracking section
        tracking_content = generate_location_tracking_section(npc_name, npc_role, existing_locations)
        
        # Create the section
        tracking_section = f"\n## Location & Movement\n\n{tracking_content}\n"
        
        # Find insertion point
        insertion_patterns = [
            r'(##\s*Current\s+Role.*?)(?=##)',
            r'(##\s*Activities.*?)(?=##)',
            r'(##\s*Background.*?)(?=##)',
        ]
        
        inserted = False
        for pattern in insertion_patterns:
            if re.search(pattern, content, re.MULTILINE | re.DOTALL):
                new_content = re.sub(
                    pattern,
                    f'\\1{tracking_section}',
                    content,
                    flags=re.MULTILINE | re.DOTALL
                )
                inserted = True
                break
        
        if not inserted:
            # Insert before Adventure Hooks or Relationships
            if '## Adventure Hooks' in content:
                new_content = content.replace('## Adventure Hooks', f"{tracking_section}\n## Adventure Hooks")
            elif '## Relationships' in content:
                new_content = content.replace('## Relationships', f"{tracking_section}\n## Relationships")
            else:
                # Add before final notes or at end
                if '---' in content:
                    new_content = content.replace('---', f"{tracking_section}\n---")
                else:
                    new_content = content + tracking_section
        
        # Write enhanced content
        if not DRY_RUN:
            # Create backup
            backup_path = filepath + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Write enhanced content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error enhancing {filepath}: {e}")
        return False

def create_npc_location_matrix():
    """Create a matrix showing NPC-Location relationships"""
    
    print("Building NPC-Location relationship matrix...")
    
    npc_files = find_npc_files()
    location_files = find_location_files()
    
    # Create location name lookup
    location_names = {}
    for filepath in location_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            location_name = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
            if location_name:
                location_names[location_name.group(1).strip()] = filepath
        except:
            continue
    
    # Build NPC-Location matrix
    npc_location_matrix = {}
    
    for filepath in npc_files[:50]:  # Limit to first 50 for performance
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            npc_name = os.path.basename(filepath)[:-3]
            npc_role = extract_npc_role(content)
            linked_locations = extract_current_locations(content)
            
            if linked_locations:
                npc_location_matrix[npc_name] = {
                    'role': npc_role,
                    'locations': linked_locations,
                    'file_path': filepath
                }
                
        except Exception as e:
            print(f"Error analyzing {filepath}: {e}")
    
    return npc_location_matrix

def main():
    print("=== Phase 3 Step 46: Character-Location Linking ===")
    print(f"Working directory: {ROOT_DIR}")
    print(f"Dry run mode: {DRY_RUN}")
    
    # Find NPC and location files
    print("\nFinding NPC and location files...")
    npc_files = find_npc_files()
    location_files = find_location_files()
    print(f"Found {len(npc_files)} NPC files and {len(location_files)} location files")
    
    # Build NPC-Location matrix
    print("\nBuilding NPC-Location relationship matrix...")
    matrix = create_npc_location_matrix()
    
    print(f"Matrix includes {len(matrix)} NPCs with location connections")
    
    # Analyze role distribution
    role_counts = {}
    for npc_data in matrix.values():
        role = npc_data['role']
        role_counts[role] = role_counts.get(role, 0) + 1
    
    print(f"\nNPC role distribution:")
    for role, count in sorted(role_counts.items()):
        print(f"  {role.title()}: {count} NPCs")
    
    # Prioritize NPCs by importance (content and connections)
    prioritized_npcs = []
    for filepath in npc_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            word_count = len(content.split())
            link_count = len(re.findall(r'\[\[.*?\]\]', content))
            priority = word_count + (link_count * 8)
            
            prioritized_npcs.append((filepath, priority))
        except:
            prioritized_npcs.append((filepath, 0))
    
    # Sort by priority
    prioritized_npcs.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop 10 priority NPCs for location linking:")
    for i, (filepath, priority) in enumerate(prioritized_npcs[:10]):
        name = os.path.basename(filepath)[:-3]
        print(f"  {i+1:2d}. {name} (priority: {priority})")
    
    # Enhance NPC files
    enhanced_count = 0
    target_count = min(20, len(prioritized_npcs))
    
    print(f"\nEnhancing location tracking for top {target_count} NPCs...")
    
    for filepath, priority in prioritized_npcs[:target_count]:
        if priority > 150:  # Only process substantial NPCs
            npc_name = os.path.basename(filepath)[:-3]
            print(f"Processing {npc_name}...")
            
            if enhance_npc_with_location_tracking(filepath):
                enhanced_count += 1
    
    # Generate reports
    report_data = {
        'total_npcs': len(npc_files),
        'total_locations': len(location_files),
        'npcs_with_locations': len(matrix),
        'role_distribution': role_counts,
        'enhanced_count': enhanced_count,
        'movement_patterns': list(MOVEMENT_PATTERNS.keys()),
        'enhancement_timestamp': datetime.now().isoformat(),
        'dry_run': DRY_RUN
    }
    
    report_path = os.path.join(ROOT_DIR, 'reports', 'npc_location_linking_report.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2)
    
    # Create human-readable matrix
    matrix_path = os.path.join(ROOT_DIR, 'reports', 'npc_location_matrix.md')
    with open(matrix_path, 'w', encoding='utf-8') as f:
        f.write("# NPC-Location Relationship Matrix\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for npc_name, data in sorted(matrix.items()):
            f.write(f"## {npc_name} ({data['role']})\n\n")
            for location in data['locations']:
                f.write(f"- [[{location}]]\n")
            f.write("\n")
    
    print(f"\n=== Enhancement Report ===")
    print(f"Total NPCs found: {len(npc_files)}")
    print(f"Total locations found: {len(location_files)}")
    print(f"NPCs with location connections: {len(matrix)}")
    print(f"NPCs enhanced with location tracking: {enhanced_count}")
    print(f"Report saved to: reports/npc_location_linking_report.json")
    print(f"Matrix saved to: reports/npc_location_matrix.md")
    
    if DRY_RUN:
        print("\nDry run mode - no files were modified")
    else:
        print(f"\n{enhanced_count} NPC files enhanced with location and movement tracking")

if __name__ == '__main__':
    main()