#!/usr/bin/env python3
"""
Phase 3 Step 45: Consequence Chain Development
Creates action-consequence relationship tracking and butterfly effect systems
"""

import os
import re
import json
import random
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'

# Consequence chain templates by scope and severity
CONSEQUENCE_TEMPLATES = {
    'personal': {
        'immediate': [
            'Character reputation shifts among immediate contacts',
            'Personal relationships become strained or strengthened',
            'Individual skills or abilities are gained or lost',
            'Character resources (wealth, items, favor) change',
            'Personal secrets are revealed or concealed',
            'Character health or mental state is affected'
        ],
        'short_term': [
            'Family dynamics change due to character actions',
            'Professional opportunities open or close',
            'Personal enemies or allies are made',
            'Character living situation or status changes',
            'Personal goals become easier or harder to achieve',
            'Character worldview or beliefs shift'
        ],
        'long_term': [
            'Character legacy shapes future generations',
            'Personal choices ripple through family bloodlines',
            'Character reputation becomes historical legend',
            'Personal sacrifices or gains compound over time',
            'Character influence shapes cultural development',
            'Personal actions create lasting institutional changes'
        ]
    },
    'local': {
        'immediate': [
            'Community resources are gained, lost, or redistributed',
            'Local power structures shift or face challenges',
            'Settlement security increases or decreases',
            'Economic opportunities emerge or disappear',
            'Local tensions rise or decrease between groups',
            'Community morale and cohesion changes'
        ],
        'short_term': [
            'Trade routes change affecting local economy',
            'Population migration into or away from area',
            'Local governance adapts to new circumstances',
            'Community infrastructure improves or degrades',
            'Cultural practices evolve or face pressure',
            'Inter-community relationships strengthen or weaken'
        ],
        'long_term': [
            'Settlement growth patterns permanently altered',
            'Local culture develops unique characteristics',
            'Regional influence and importance shifts',
            'Economic specialization creates lasting identity',
            'Community becomes model for others or cautionary tale',
            'Local innovations spread to wider world'
        ]
    },
    'regional': {
        'immediate': [
            'Regional political alliances shift or form',
            'Trade networks experience disruption or expansion',
            'Military forces mobilize or stand down',
            'Resource availability changes across region',
            'Communication networks adapt to new information',
            'Regional leaders take emergency or opportunistic actions'
        ],
        'short_term': [
            'Provincial governance structures adapt or resist change',
            'Cross-regional cooperation increases or decreases',
            'Economic specialization patterns shift geographically',
            'Population centers rise or decline in importance',
            'Cultural exchange accelerates or contracts',
            'Transportation infrastructure develops or deteriorates'
        ],
        'long_term': [
            'Regional identity and character permanently shaped',
            'Geographic importance in world politics changes',
            'Economic role in inter-regional trade evolves',
            'Cultural influence spreads or diminishes globally',
            'Regional innovations become world-changing developments',
            'Historical significance establishes lasting legacy'
        ]
    },
    'world': {
        'immediate': [
            'International diplomatic relations face crisis or opportunity',
            'Global trade systems experience shock or boom',
            'World powers mobilize resources for response',
            'Information spreads rapidly through communication networks',
            'Emergency protocols activate across institutions',
            'Global markets react to new circumstances'
        ],
        'short_term': [
            'International treaties require renegotiation or enforcement',
            'World economic systems adapt to new realities',
            'Global cultural movements emerge or fragment',
            'International cooperation increases or decreases',
            'Technological development accelerates or stagnates',
            'World political balance shifts toward different powers'
        ],
        'long_term': [
            'World history divides into before and after periods',
            'Global civilization develops along different paths',
            'International system structures change permanently',
            'World culture incorporates new universal elements',
            'Global challenges require unprecedented cooperation',
            'Human development reaches new stages or faces setbacks'
        ]
    }
}

# Consequence timing and escalation patterns
TIMING_PATTERNS = {
    'immediate': {
        'duration': 'minutes to hours',
        'scope': 'direct participants and witnesses',
        'reversibility': 'often reversible with quick action'
    },
    'short_term': {
        'duration': 'days to months', 
        'scope': 'extended networks and communities',
        'reversibility': 'difficult but possible to reverse'
    },
    'long_term': {
        'duration': 'years to decades',
        'scope': 'entire societies and future generations',
        'reversibility': 'permanent or requiring massive effort to change'
    }
}

# Butterfly effect multipliers
BUTTERFLY_EFFECTS = {
    'minor_action': {
        'description': 'Small personal choice with unexpectedly large consequences',
        'multiplier_examples': [
            'Casual conversation overheard by important figure',
            'Minor favor leading to major opportunity',
            'Small act of kindness creating loyal ally',
            'Brief delay preventing or enabling major event',
            'Simple purchase changing merchant destiny'
        ]
    },
    'social_interaction': {
        'description': 'Interpersonal moment that cascades through networks',
        'multiplier_examples': [
            'Introduction connecting previously separate groups',
            'Argument that splits previously united factions',
            'Romance that bridges political divides',
            'Betrayal that triggers wider distrust',
            'Reconciliation that enables larger peace'
        ]
    },
    'information_spread': {
        'description': 'Knowledge sharing that amplifies through communication',
        'multiplier_examples': [
            'Rumor that becomes accepted truth',
            'Secret revealed at crucial timing',
            'Innovation shared enabling widespread change',
            'Warning that prevents or enables catastrophe',
            'Lie that shapes false but consequential beliefs'
        ]
    },
    'resource_movement': {
        'description': 'Economic action that reshapes larger systems',
        'multiplier_examples': [
            'Investment that launches new industry',
            'Boycott that shifts market preferences',
            'Gift that establishes new trade relationship',
            'Theft that destabilizes economic system',
            'Donation that funds transformative project'
        ]
    }
}

def find_action_files():
    """Find files that describe actions, events, or decisions"""
    action_files = []
    
    # Look for quest files, session logs, and event descriptions
    search_patterns = [
        r'quest|mission|adventure',
        r'session|log|journal', 
        r'event|incident|crisis',
        r'decision|choice|action',
        r'conflict|war|battle',
        r'ceremony|ritual|celebration'
    ]
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip certain directories
        if any(skip_dir in root for skip_dir in ['/.git', '/08_Archive', '/09_Performance', '/vault_backup']):
            continue
            
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file describes actions or events
                    filename_lower = file.lower()
                    content_lower = content.lower()
                    
                    is_action_file = (
                        any(re.search(pattern, filename_lower) for pattern in search_patterns) or
                        any(keyword in content_lower for keyword in [
                            'consequence', 'result', 'outcome', 'effect', 'impact',
                            'reaction', 'response', 'ripple', 'aftermath', 'changed'
                        ]) or
                        '/01_Adventures/' in filepath or
                        '/Quests/' in filepath or
                        'Session' in file
                    )
                    
                    if is_action_file:
                        action_files.append(filepath)
                        
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return action_files

def analyze_action_scope(content, filepath):
    """Determine the scope and significance of actions described"""
    content_lower = content.lower()
    
    # Analyze scope indicators
    scope_indicators = {
        'personal': ['character', 'individual', 'personal', 'private', 'solo'],
        'local': ['community', 'town', 'village', 'local', 'neighborhood', 'district'],
        'regional': ['region', 'province', 'territory', 'kingdom', 'realm', 'nation'],
        'world': ['world', 'global', 'international', 'universal', 'cosmic', 'dimensional']
    }
    
    scope_scores = {}
    for scope, indicators in scope_indicators.items():
        score = sum(1 for indicator in indicators if indicator in content_lower)
        scope_scores[scope] = score
    
    # Determine primary scope
    primary_scope = max(scope_scores.items(), key=lambda x: x[1])
    if primary_scope[1] == 0:
        return 'local'  # Default
    else:
        return primary_scope[0]

def has_consequence_tracking(content):
    """Check if file already has consequence chain documentation"""
    consequence_indicators = [
        'consequences', 'consequence chain', 'ripple effects', 'butterfly effect',
        'immediate effects', 'long-term impact', 'short-term consequences',
        'action-consequence', 'cause and effect', 'ramifications'
    ]
    
    return any(indicator in content.lower() for indicator in consequence_indicators)

def generate_consequence_chain(action_scope, action_title, content):
    """Generate comprehensive consequence chain documentation"""
    template = CONSEQUENCE_TEMPLATES[action_scope]
    
    chain_parts = []
    
    # Introduction
    chain_parts.append(f"The actions and decisions involving {action_title} create cascading effects across multiple levels of society and time.")
    chain_parts.append("")
    
    # Immediate consequences
    immediate_items = random.sample(template['immediate'], min(2, len(template['immediate'])))
    chain_parts.append("### Immediate Consequences")
    chain_parts.append(f"*{TIMING_PATTERNS['immediate']['duration']} - {TIMING_PATTERNS['immediate']['scope']}*")
    chain_parts.append("")
    
    for item in immediate_items:
        chain_parts.append(f"- **Direct Impact**: {item}")
    chain_parts.append("")
    chain_parts.append(f"*{TIMING_PATTERNS['immediate']['reversibility']}*")
    chain_parts.append("")
    
    # Short-term consequences
    short_term_items = random.sample(template['short_term'], min(2, len(template['short_term'])))
    chain_parts.append("### Short-term Consequences")
    chain_parts.append(f"*{TIMING_PATTERNS['short_term']['duration']} - {TIMING_PATTERNS['short_term']['scope']}*")
    chain_parts.append("")
    
    for item in short_term_items:
        chain_parts.append(f"- **Extended Impact**: {item}")
    chain_parts.append("")
    chain_parts.append(f"*{TIMING_PATTERNS['short_term']['reversibility']}*")
    chain_parts.append("")
    
    # Long-term consequences
    long_term_items = random.sample(template['long_term'], min(2, len(template['long_term'])))
    chain_parts.append("### Long-term Consequences")
    chain_parts.append(f"*{TIMING_PATTERNS['long_term']['duration']} - {TIMING_PATTERNS['long_term']['scope']}*")
    chain_parts.append("")
    
    for item in long_term_items:
        chain_parts.append(f"- **Lasting Impact**: {item}")
    chain_parts.append("")
    chain_parts.append(f"*{TIMING_PATTERNS['long_term']['reversibility']}*")
    chain_parts.append("")
    
    # Butterfly effect potential
    butterfly_type = random.choice(list(BUTTERFLY_EFFECTS.keys()))
    butterfly_data = BUTTERFLY_EFFECTS[butterfly_type]
    multiplier_example = random.choice(butterfly_data['multiplier_examples'])
    
    chain_parts.append("### Butterfly Effect Potential")
    chain_parts.append("")
    chain_parts.append(f"**{butterfly_data['description']}**")
    chain_parts.append("")
    chain_parts.append(f"*Example Multiplier*: {multiplier_example}")
    chain_parts.append("")
    
    # Tracking mechanisms
    chain_parts.append("### Consequence Tracking")
    chain_parts.append("")
    chain_parts.append("**Status Monitoring**: Track immediate visible effects and stakeholder reactions")
    chain_parts.append("**Network Analysis**: Monitor how effects spread through relationship networks")
    chain_parts.append("**Timeline Tracking**: Record when different consequence levels manifest")
    chain_parts.append("**Mitigation Options**: Identify intervention points where consequences can be modified")
    chain_parts.append("**Amplification Factors**: Recognize conditions that might intensify effects")
    
    return "\n".join(chain_parts)

def create_consequence_system_template():
    """Create a master consequence tracking template"""
    
    template_content = """# Consequence Chain Tracking System

## Overview
This system tracks how character actions and campaign events create cascading effects across different levels of society and time periods.

## Scope Levels

### Personal Consequences
- **Immediate**: Character-focused effects visible within scenes
- **Short-term**: Individual and family impacts over sessions
- **Long-term**: Character legacy and bloodline effects

### Local Consequences  
- **Immediate**: Community-level changes within adventures
- **Short-term**: Settlement and regional adaptations
- **Long-term**: Cultural and economic transformation

### Regional Consequences
- **Immediate**: Province-wide reactions to events
- **Short-term**: Political and economic restructuring
- **Long-term**: Regional character and identity evolution

### World Consequences
- **Immediate**: International diplomatic and economic responses
- **Short-term**: Global system adaptations
- **Long-term**: Civilizational development paths

## Timing Framework

### Immediate (Minutes to Hours)
- Direct participants and witnesses affected
- Often reversible with quick action
- High emotional intensity, low complexity

### Short-term (Days to Months)
- Extended networks and communities involved
- Difficult but possible to reverse
- Medium complexity, adaptation required

### Long-term (Years to Decades)
- Entire societies and future generations
- Permanent or requiring massive effort to change
- High complexity, systemic transformation

## Butterfly Effect Multipliers

### Minor Action Cascades
Small personal choices with unexpectedly large consequences

### Social Network Cascades
Interpersonal moments that spread through relationship networks

### Information Cascades
Knowledge sharing that amplifies through communication systems

### Resource Cascades
Economic actions that reshape larger market and social systems

## Tracking Methods

### Immediate Response Log
- Who reacts and how
- Visible changes in environment/situation
- Stakeholder positions and statements

### Network Effect Map
- Which relationships are affected
- How information and influence spread
- Key connection points and influencers

### Timeline Projection
- When different effects are likely to manifest
- Critical decision points for intervention
- Long-term trend trajectories

### Mitigation/Amplification Analysis
- Ways consequences could be reduced or prevented
- Conditions that might intensify effects
- Intervention opportunities and costs

## Usage Guidelines

1. **Assess Scope**: Determine primary level of impact
2. **Map Immediate**: Identify direct effects and reactions  
3. **Project Timeline**: Estimate when consequences will manifest
4. **Track Networks**: Follow how effects spread through relationships
5. **Identify Interventions**: Find opportunities to modify outcomes
6. **Document Evolution**: Record how consequences actually develop

---
*Use this framework to create living, reactive world where player actions have meaningful and trackable consequences.*
"""
    
    template_path = os.path.join(ROOT_DIR, '05_Templates', 'Consequence_Chain_Template.md')
    os.makedirs(os.path.dirname(template_path), exist_ok=True)
    
    if not DRY_RUN:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
    
    return template_path

def enhance_action_with_consequences(filepath):
    """Add consequence chain tracking to an action/event file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has consequence tracking
        if has_consequence_tracking(content):
            print(f"Consequence tracking already present in {os.path.basename(filepath)}")
            return False
        
        # Skip very short files
        if len(content.split()) < 100:
            print(f"Skipping short file {os.path.basename(filepath)}")
            return False
        
        # Determine action scope and title
        action_scope = analyze_action_scope(content, filepath)
        action_title = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
        action_title = action_title.group(1).strip() if action_title else os.path.basename(filepath)[:-3]
        
        # Generate consequence chain
        consequence_content = generate_consequence_chain(action_scope, action_title, content)
        
        # Create consequence section
        consequence_section = f"\n## Consequence Chains\n\n{consequence_content}\n"
        
        # Find insertion point
        insertion_patterns = [
            r'(##\s*Aftermath.*?)(?=##)',
            r'(##\s*Results.*?)(?=##)',
            r'(##\s*Outcomes.*?)(?=##)',
            r'(##\s*Effects.*?)(?=##)',
        ]
        
        inserted = False
        for pattern in insertion_patterns:
            if re.search(pattern, content, re.MULTILINE | re.DOTALL):
                new_content = re.sub(
                    pattern,
                    f'\\1{consequence_section}',
                    content,
                    flags=re.MULTILINE | re.DOTALL
                )
                inserted = True
                break
        
        if not inserted:
            # Insert before DM Notes or at end
            if '## DM Notes' in content:
                new_content = content.replace('## DM Notes', f"{consequence_section}\n## DM Notes")
            elif '---' in content:
                new_content = content.replace('---', f"{consequence_section}\n---")
            else:
                new_content = content + consequence_section
        
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
    print("=== Phase 3 Step 45: Consequence Chain Development ===")
    print(f"Working directory: {ROOT_DIR}")
    print(f"Dry run mode: {DRY_RUN}")
    
    # Create consequence tracking template
    print("\nCreating consequence chain tracking template...")
    template_path = create_consequence_system_template()
    print(f"Template created at: {os.path.relpath(template_path, ROOT_DIR)}")
    
    # Find action files
    print("\nFinding action/event files...")
    action_files = find_action_files()
    print(f"Found {len(action_files)} action/event files")
    
    # Analyze scope distribution
    scope_counts = {}
    for filepath in action_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            scope = analyze_action_scope(content, filepath)
            scope_counts[scope] = scope_counts.get(scope, 0) + 1
        except:
            continue
    
    print("\nAction scope distribution:")
    for scope, count in sorted(scope_counts.items()):
        print(f"  {scope.title()}: {count} files")
    
    # Prioritize files by importance (content length and connections)
    prioritized_actions = []
    for filepath in action_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            word_count = len(content.split())
            link_count = len(re.findall(r'\[\[.*?\]\]', content))
            consequence_mentions = len(re.findall(r'\b(effect|impact|consequence|result|outcome)\b', content.lower()))
            priority = word_count + (link_count * 10) + (consequence_mentions * 5)
            
            prioritized_actions.append((filepath, priority))
        except:
            prioritized_actions.append((filepath, 0))
    
    # Sort by priority
    prioritized_actions.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop 10 priority actions for consequence tracking:")
    for i, (filepath, priority) in enumerate(prioritized_actions[:10]):
        name = os.path.basename(filepath)[:-3]
        print(f"  {i+1:2d}. {name} (priority: {priority})")
    
    # Enhance action files
    enhanced_count = 0
    target_count = min(15, len(prioritized_actions))
    
    print(f"\nEnhancing consequence chains for top {target_count} actions...")
    
    for filepath, priority in prioritized_actions[:target_count]:
        if priority > 100:  # Only process substantial files
            action_name = os.path.basename(filepath)[:-3]
            print(f"Processing {action_name}...")
            
            if enhance_action_with_consequences(filepath):
                enhanced_count += 1
    
    # Generate report
    report_data = {
        'total_action_files': len(action_files),
        'scope_distribution': scope_counts,
        'enhanced_count': enhanced_count,
        'template_created': os.path.relpath(template_path, ROOT_DIR),
        'enhancement_timestamp': datetime.now().isoformat(),
        'consequence_levels': list(CONSEQUENCE_TEMPLATES.keys()),
        'timing_patterns': list(TIMING_PATTERNS.keys()),
        'butterfly_effects': list(BUTTERFLY_EFFECTS.keys()),
        'dry_run': DRY_RUN
    }
    
    report_path = os.path.join(ROOT_DIR, 'reports', 'consequence_chain_report.json')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n=== Enhancement Report ===")
    print(f"Total action files found: {len(action_files)}")
    print(f"Files enhanced with consequence chains: {enhanced_count}")
    print(f"Consequence tracking template created")
    print(f"Report saved to: reports/consequence_chain_report.json")
    
    if DRY_RUN:
        print("\nDry run mode - no files were modified")
    else:
        print(f"\n{enhanced_count} action files enhanced with consequence chain tracking")

if __name__ == '__main__':
    main()