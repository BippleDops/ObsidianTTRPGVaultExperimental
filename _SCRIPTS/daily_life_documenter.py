#!/usr/bin/env python3
"""
Phase 3 Step 44: Daily Life Documentation
Documents daily routines, cultural practices, and living world details for settlements
"""

import os
import re
import json
import random
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'

# Daily life templates by world type
DAILY_LIFE_TEMPLATES = {
    'aquabyssos': {
        'daily_routines': [
            'Morning tidal prayers as currents shift with the dawn tide',
            'Pressure-glass maintenance performed during optimal depth conditions',
            'Kelp farming cycles aligned with nutrient current patterns',
            'Bioluminescent lighting adjusted for communal activities',
            'Crystal resonance tuning for communication networks',
            'Deep current navigation planning for daily travel'
        ],
        'cultural_practices': [
            'Tide ceremonies marking significant life events',
            'Pressure adaptation rituals for depth travelers',
            'Coral communion services celebrating living architecture',
            'Pearl-diving contests during seasonal celebrations',
            'Memory current sharing among community elders',
            'Shadow-touched integration ceremonies'
        ],
        'economic_activities': [
            'Dawn fish markets with fresh catches from night trawlers',
            'Crystal processing during optimal resonance hours',
            'Pressure-forged metalwork in specialized workshops',
            'Kelp textile weaving in community production centers',
            'Deep salvage operations coordinated by guild schedules',
            'Shadow portal trade managed during stable dimensional windows'
        ],
        'social_rhythms': [
            'Community gathering spaces that shift with tidal flows',
            'Storytelling circles during deep current meditations',
            'Shared meals using communal pressure cooking systems',
            'Artisan workshops teaching traditional craft techniques',
            'Youth education in depth survival and cultural heritage',
            'Elder councils meeting during the quietest tidal hours'
        ],
        'environmental_adaptations': [
            'Daily pressure suit inspections and maintenance routines',
            'Breathing apparatus filtering and replacement schedules',
            'Water current monitoring for travel and safety planning',
            'Bioluminescent creature tending for light and nutrition',
            'Magical ward maintenance protecting against depth pressure',
            'Emergency response drills for pressure failures or depth storms'
        ]
    },
    'aethermoor': {
        'daily_routines': [
            'Dawn wind readings for weather prediction and travel planning',
            'Crystal harmonics tuning with morning atmospheric conditions',
            'Sky garden tending during optimal wind-carried nutrient times',
            'Wind anchor inspections ensuring structural stability',
            'Storm watch duties rotated among community members',
            'Aerial creature care and wind-riding practice sessions'
        ],
        'cultural_practices': [
            'Wind ceremonies celebrating seasonal atmospheric changes',
            'Crystal singing performances amplified by natural acoustics',
            'Sky burial traditions honoring the deceased',
            'Storm dancing rituals during weather transitions',
            'Height acclimation ceremonies for new residents',
            'Weather prediction ceremonies led by atmospheric specialists'
        ],
        'economic_activities': [
            'Morning crystal mining during stable atmospheric pressure',
            'Wind-powered craft workshops utilizing natural energy',
            'Sky trade route planning based on seasonal wind patterns',
            'Atmospheric alchemy during optimal air current conditions',
            'Storm glass production requiring precise environmental timing',
            'Wind-message delivery services coordinated with weather patterns'
        ],
        'social_rhythms': [
            'Community wind forums for decision-making and planning',
            'Shared crafting sessions in weather-protected workshops',
            'Communal meals in structures designed for wind acoustics',
            'Teaching circles for wind-navigation and survival skills',
            'Height adaptation support groups for newcomers',
            'Weather celebration gatherings during significant atmospheric events'
        ],
        'environmental_adaptations': [
            'Daily wind anchor and structural integrity inspections',
            'Cold weather gear maintenance for high-altitude conditions',
            'Storm shelter preparation and emergency supply management',
            'Altitude sickness monitoring and treatment protocols',
            'Wind pattern documentation for community safety and planning',
            'Emergency response training for weather-related disasters'
        ]
    },
    'mixed': {
        'daily_routines': [
            'Cross-realm communication checks via magical portal networks',
            'Cultural exchange activities between world representatives',
            'Diplomatic protocol observances for inter-world relations',
            'Trade good inspection and valuation by certified assessors',
            'Environmental transition assistance for inter-world travelers',
            'Multi-cultural education programs for community integration'
        ],
        'cultural_practices': [
            'Harmony festivals celebrating both tidal and wind traditions',
            'Cultural fusion ceremonies blending aquabyssos and aethermoor customs',
            'Translation services preserving both linguistic traditions',
            'Art exhibitions showcasing techniques from both worlds',
            'Cooking traditions combining ingredients from sea and sky',
            'Storytelling sessions sharing legends from both realms'
        ],
        'economic_activities': [
            'Inter-world trade negotiations during stable portal conditions',
            'Cultural goods production requiring techniques from both worlds',
            'Transportation services specialized in cross-realm travel',
            'Exchange rate monitoring and currency conversion services',
            'Diplomatic escort services for inter-world delegations',
            'Technology adaptation workshops for cross-world innovations'
        ],
        'social_rhythms': [
            'Mixed community councils with representation from both worlds',
            'Cultural sensitivity training for community leaders',
            'Integration support groups for inter-world immigrants',
            'Collaborative projects building understanding between communities',
            'Conflict resolution services specialized in cultural differences',
            'Celebration planning incorporating traditions from both worlds'
        ],
        'environmental_adaptations': [
            'Multi-environment safety training for diverse conditions',
            'Transition facility management for world-crossing individuals',
            'Medical services trained in both pressure and altitude conditions',
            'Emergency protocols for cross-dimensional incidents',
            'Environmental monitoring systems tracking both world conditions',
            'Adaptive technology development for multi-world functionality'
        ]
    }
}

# Community types and their specific characteristics
COMMUNITY_TYPES = {
    'city': {
        'scale': 'large',
        'complexity': 'high',
        'focus': ['trade', 'government', 'culture', 'industry'],
        'population_activities': 'diverse professional specializations and complex social hierarchies'
    },
    'town': {
        'scale': 'medium',
        'complexity': 'moderate',
        'focus': ['commerce', 'crafts', 'regional governance'],
        'population_activities': 'mixed artisan work and local trade coordination'
    },
    'village': {
        'scale': 'small',
        'complexity': 'simple',
        'focus': ['agriculture', 'fishing', 'basic crafts'],
        'population_activities': 'subsistence activities and local resource management'
    },
    'outpost': {
        'scale': 'tiny',
        'complexity': 'basic',
        'focus': ['frontier', 'military', 'exploration'],
        'population_activities': 'survival-focused activities and specialized mission support'
    }
}

def find_settlement_files():
    """Find settlement and community location files"""
    settlement_files = []
    
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
                    
                    # Check if file represents a settlement/community
                    is_settlement = (
                        re.search(r'^type:\s*(Location|Settlement|City|Town|Village)\s*$', content, re.MULTILINE | re.IGNORECASE) or
                        any(keyword in content.lower() for keyword in ['settlement', 'city', 'town', 'village', 'district', 'quarter', 'community']) and
                        any(keyword in content.lower() for keyword in ['population', 'residents', 'inhabitants', 'citizens', 'people', 'families'])
                    )
                    
                    if is_settlement:
                        settlement_files.append(filepath)
                        
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return settlement_files

def determine_world_type(content, filepath):
    """Determine world type and community characteristics"""
    content_lower = content.lower()
    
    # Check for explicit world designation
    if re.search(r'world:\s*aquabyssos', content_lower):
        world_type = 'aquabyssos'
    elif re.search(r'world:\s*aethermoor', content_lower):
        world_type = 'aethermoor'
    elif any(word in content_lower for word in ['cross-realm', 'inter-world', 'dimensional', 'portal']):
        world_type = 'mixed'
    elif any(word in content_lower for word in ['underwater', 'depths', 'tidal', 'pressure']):
        world_type = 'aquabyssos'
    elif any(word in content_lower for word in ['sky', 'wind', 'crystal', 'heights']):
        world_type = 'aethermoor'
    else:
        world_type = 'aquabyssos'  # Default
    
    # Determine community type
    if any(word in content_lower for word in ['city', 'capital', 'metropolis']):
        community_type = 'city'
    elif any(word in content_lower for word in ['town', 'township']):
        community_type = 'town'
    elif any(word in content_lower for word in ['village', 'hamlet']):
        community_type = 'village'
    elif any(word in content_lower for word in ['outpost', 'frontier', 'garrison']):
        community_type = 'outpost'
    else:
        community_type = 'town'  # Default
    
    return world_type, community_type

def generate_daily_life_section(world_type, community_type, location_name):
    """Generate comprehensive daily life documentation"""
    template = DAILY_LIFE_TEMPLATES.get(world_type, DAILY_LIFE_TEMPLATES['aquabyssos'])
    community_info = COMMUNITY_TYPES[community_type]
    
    section_parts = []
    
    # Opening description
    section_parts.append(f"Life in {location_name} follows the rhythms of {world_type} culture, with the community's {community_info['scale']} scale creating {community_info['population_activities']}.")
    section_parts.append("")
    
    # Daily routines
    routine_items = random.sample(template['daily_routines'], min(3, len(template['daily_routines'])))
    section_parts.append("### Daily Rhythms")
    section_parts.append("")
    for routine in routine_items:
        section_parts.append(f"- **{routine.split(' ')[0].title()} Activities**: {routine}")
    section_parts.append("")
    
    # Cultural practices
    cultural_items = random.sample(template['cultural_practices'], min(2, len(template['cultural_practices'])))
    section_parts.append("### Cultural Practices")
    section_parts.append("")
    for practice in cultural_items:
        section_parts.append(f"- **{practice.split(' ')[0].title()}**: {practice}")
    section_parts.append("")
    
    # Economic activities
    economic_items = random.sample(template['economic_activities'], min(3, len(template['economic_activities'])))
    section_parts.append("### Economic Life")
    section_parts.append("")
    for activity in economic_items:
        section_parts.append(f"- **{activity.split(' ')[0].title()}**: {activity}")
    section_parts.append("")
    
    # Social structures
    social_items = random.sample(template['social_rhythms'], min(2, len(template['social_rhythms'])))
    section_parts.append("### Social Organization")
    section_parts.append("")
    for social in social_items:
        section_parts.append(f"- **Community Interaction**: {social}")
    section_parts.append("")
    
    # Environmental considerations
    environmental_items = random.sample(template['environmental_adaptations'], min(2, len(template['environmental_adaptations'])))
    section_parts.append("### Environmental Adaptation")
    section_parts.append("")
    for adaptation in environmental_items:
        section_parts.append(f"- **Survival Practice**: {adaptation}")
    section_parts.append("")
    
    # Community calendar
    section_parts.append("### Community Calendar")
    section_parts.append("")
    section_parts.append("**Daily Cycle**: Community activities follow natural rhythms with peak activity periods and rest times")
    section_parts.append("**Weekly Patterns**: Regular market days, cultural events, and community gatherings")
    section_parts.append("**Seasonal Celebrations**: Traditional festivals and ceremonies marking significant periods")
    section_parts.append("**Special Events**: Unique local celebrations and important community milestones")
    
    return "\n".join(section_parts)

def has_daily_life_section(content):
    """Check if location already has daily life documentation"""
    daily_life_indicators = [
        'daily life', 'daily rhythms', 'cultural practices', 'community calendar',
        'daily routines', 'social organization', 'economic life', 'environmental adaptation',
        'morning tidal', 'dawn wind', 'community gathering', 'cultural ceremonies'
    ]
    
    return any(indicator in content.lower() for indicator in daily_life_indicators)

def enhance_settlement_with_daily_life(filepath):
    """Add daily life documentation to a settlement file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has daily life content
        if has_daily_life_section(content):
            print(f"Daily life documentation already present in {os.path.basename(filepath)}")
            return False
        
        # Skip very short files (likely stubs)
        if len(content.split()) < 200:
            print(f"Skipping short file {os.path.basename(filepath)} - needs basic content first")
            return False
        
        # Determine world type and community characteristics
        world_type, community_type = determine_world_type(content, filepath)
        location_name = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
        location_name = location_name.group(1).strip() if location_name else os.path.basename(filepath)[:-3]
        
        # Generate daily life section
        daily_life_content = generate_daily_life_section(world_type, community_type, location_name)
        
        # Create the section
        daily_life_section = f"\n## Culture & Daily Life\n\n{daily_life_content}\n"
        
        # Find appropriate insertion point
        insertion_patterns = [
            r'(##\s*Culture\s*$.*?)(?=##)',
            r'(##\s*Society\s*$.*?)(?=##)',
            r'(##\s*Government\s*$.*?)(?=##)',
            r'(##\s*Economy\s*$.*?)(?=##)',
        ]
        
        inserted = False
        for pattern in insertion_patterns:
            if re.search(pattern, content, re.MULTILINE | re.DOTALL):
                new_content = re.sub(
                    pattern,
                    f'\\1{daily_life_section}',
                    content,
                    flags=re.MULTILINE | re.DOTALL
                )
                inserted = True
                break
        
        if not inserted:
            # Insert before Adventure Hooks or Notable Features
            if '## Adventure Hooks' in content:
                new_content = content.replace('## Adventure Hooks', f"{daily_life_section}\n## Adventure Hooks")
            elif '## Notable Features' in content:
                new_content = content.replace('## Notable Features', f"{daily_life_section}\n## Notable Features")
            else:
                # Add before final notes or at end
                if '---' in content:
                    new_content = content.replace('---', f"{daily_life_section}\n---")
                else:
                    new_content = content + daily_life_section
        else:
            # Use the modified content from pattern replacement
            pass
        
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

def main():
    print("=== Phase 3 Step 44: Daily Life Documentation ===")
    print(f"Working directory: {ROOT_DIR}")
    print(f"Dry run mode: {DRY_RUN}")
    
    # Find settlement files
    print("\nFinding settlement files...")
    settlement_files = find_settlement_files()
    print(f"Found {len(settlement_files)} settlement files")
    
    # Analyze world and community type distribution
    world_counts = {}
    community_counts = {}
    
    for filepath in settlement_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            world_type, community_type = determine_world_type(content, filepath)
            world_counts[world_type] = world_counts.get(world_type, 0) + 1
            community_counts[community_type] = community_counts.get(community_type, 0) + 1
        except:
            continue
    
    print("\nWorld distribution:")
    for world_type, count in sorted(world_counts.items()):
        print(f"  {world_type.title()}: {count} settlements")
    
    print("\nCommunity type distribution:")
    for community_type, count in sorted(community_counts.items()):
        print(f"  {community_type.title()}: {count} settlements")
    
    # Prioritize settlements by importance (content length and connections)
    prioritized_settlements = []
    for filepath in settlement_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            word_count = len(content.split())
            link_count = len(re.findall(r'\[\[.*?\]\]', content))
            priority = word_count + (link_count * 15)
            
            prioritized_settlements.append((filepath, priority))
        except:
            prioritized_settlements.append((filepath, 0))
    
    # Sort by priority
    prioritized_settlements.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop 10 priority settlements for daily life documentation:")
    for i, (filepath, priority) in enumerate(prioritized_settlements[:10]):
        name = os.path.basename(filepath)[:-3]
        print(f"  {i+1:2d}. {name} (priority: {priority})")
    
    # Enhance settlements
    enhanced_count = 0
    target_count = min(20, len(prioritized_settlements))
    
    print(f"\nEnhancing daily life documentation for top {target_count} settlements...")
    
    for filepath, priority in prioritized_settlements[:target_count]:
        if priority > 200:  # Only process substantial settlements
            settlement_name = os.path.basename(filepath)[:-3]
            print(f"Processing {settlement_name}...")
            
            if enhance_settlement_with_daily_life(filepath):
                enhanced_count += 1
    
    # Generate report
    report_data = {
        'total_settlements': len(settlement_files),
        'world_distribution': world_counts,
        'community_distribution': community_counts,
        'enhanced_count': enhanced_count,
        'enhancement_timestamp': datetime.now().isoformat(),
        'templates_available': list(DAILY_LIFE_TEMPLATES.keys()),
        'community_types': list(COMMUNITY_TYPES.keys()),
        'dry_run': DRY_RUN
    }
    
    report_path = os.path.join(ROOT_DIR, 'reports', 'daily_life_documentation_report.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n=== Enhancement Report ===")
    print(f"Total settlements found: {len(settlement_files)}")
    print(f"Settlements enhanced: {enhanced_count}")
    print(f"Report saved to: reports/daily_life_documentation_report.json")
    
    if DRY_RUN:
        print("\nDry run mode - no files were modified")
    else:
        print(f"\n{enhanced_count} settlement files enhanced with daily life documentation")

if __name__ == '__main__':
    main()