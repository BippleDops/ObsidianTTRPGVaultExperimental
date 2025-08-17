#!/usr/bin/env python3
"""
File Naming Analysis Script for Vault Standardization
Analyzes current file naming patterns to establish standards
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
import json

def analyze_filename_patterns(vault_path):
    """Analyze filename patterns across the vault"""
    patterns = {
        'spaces': [],           # Files with spaces
        'underscores': [],      # Files with underscores
        'hyphens': [],         # Files with hyphens
        'mixed_case': [],      # Files with mixed case
        'all_caps': [],        # Files in all caps
        'all_lower': [],       # Files in all lowercase
        'numbers': [],         # Files with numbers
        'special_chars': [],   # Files with special characters
        'very_long': [],       # Files with very long names (>50 chars)
        'very_short': [],      # Files with very short names (<5 chars)
    }
    
    naming_by_directory = defaultdict(list)
    filename_lengths = []
    word_separators = Counter()
    
    for root, dirs, files in os.walk(vault_path):
        # Skip backup and script directories
        if 'backup' in root.lower() or 'script' in root.lower():
            continue
            
        relative_root = os.path.relpath(root, vault_path)
        
        for file in files:
            if file.endswith('.md'):
                # Remove .md extension for analysis
                name = file[:-3]
                naming_by_directory[relative_root].append(name)
                filename_lengths.append(len(name))
                
                # Analyze patterns
                if ' ' in name:
                    patterns['spaces'].append(os.path.join(relative_root, file))
                if '_' in name:
                    patterns['underscores'].append(os.path.join(relative_root, file))
                    word_separators['underscore'] += 1
                if '-' in name:
                    patterns['hyphens'].append(os.path.join(relative_root, file))
                    word_separators['hyphen'] += 1
                if ' ' in name:
                    word_separators['space'] += 1
                
                if name.isupper():
                    patterns['all_caps'].append(os.path.join(relative_root, file))
                elif name.islower():
                    patterns['all_lower'].append(os.path.join(relative_root, file))
                elif any(c.isupper() for c in name) and any(c.islower() for c in name):
                    patterns['mixed_case'].append(os.path.join(relative_root, file))
                
                if any(c.isdigit() for c in name):
                    patterns['numbers'].append(os.path.join(relative_root, file))
                
                if re.search(r'[^a-zA-Z0-9\s\-_]', name):
                    patterns['special_chars'].append(os.path.join(relative_root, file))
                
                if len(name) > 50:
                    patterns['very_long'].append(os.path.join(relative_root, file))
                elif len(name) < 5:
                    patterns['very_short'].append(os.path.join(relative_root, file))
    
    return patterns, naming_by_directory, filename_lengths, word_separators

def analyze_content_type_naming(vault_path):
    """Analyze naming patterns by content type"""
    content_types = {
        'adventures': '01_Adventures',
        'people': '02_Worldbuilding/People',
        'places': '02_Worldbuilding/Places',
        'groups': '02_Worldbuilding/Groups',
        'lore': '02_Worldbuilding/Lore',
        'items': '02_Worldbuilding/Items',
        'mechanics': '03_Mechanics',
        'templates': '05_Templates'
    }
    
    naming_patterns = {}
    
    for content_type, directory in content_types.items():
        full_dir = os.path.join(vault_path, directory)
        if os.path.exists(full_dir):
            files = []
            for root, dirs, filenames in os.walk(full_dir):
                for filename in filenames:
                    if filename.endswith('.md'):
                        files.append(filename[:-3])  # Remove .md
            
            naming_patterns[content_type] = {
                'count': len(files),
                'samples': files[:10],  # First 10 examples
                'patterns': analyze_naming_patterns(files)
            }
    
    return naming_patterns

def analyze_naming_patterns(filenames):
    """Analyze specific patterns in a list of filenames"""
    patterns = {
        'title_case_count': 0,
        'sentence_case_count': 0,
        'snake_case_count': 0,
        'kebab_case_count': 0,
        'space_separated_count': 0,
        'prefix_patterns': Counter(),
        'suffix_patterns': Counter(),
        'common_words': Counter()
    }
    
    for name in filenames:
        # Check casing patterns
        words = re.split(r'[\s\-_]+', name)
        
        if all(word.istitle() for word in words if word):
            patterns['title_case_count'] += 1
        elif name[0].isupper() and name[1:].islower():
            patterns['sentence_case_count'] += 1
        
        if '_' in name and ' ' not in name and '-' not in name:
            patterns['snake_case_count'] += 1
        elif '-' in name and ' ' not in name and '_' not in name:
            patterns['kebab_case_count'] += 1
        elif ' ' in name and '_' not in name and '-' not in name:
            patterns['space_separated_count'] += 1
        
        # Analyze prefixes and suffixes
        if words:
            patterns['prefix_patterns'][words[0].lower()] += 1
            if len(words) > 1:
                patterns['suffix_patterns'][words[-1].lower()] += 1
            
            # Count common words
            for word in words:
                if len(word) > 2:  # Skip short words
                    patterns['common_words'][word.lower()] += 1
    
    return patterns

def generate_naming_standards(analysis_results):
    """Generate naming standards based on analysis"""
    patterns, naming_by_directory, filename_lengths, word_separators = analysis_results
    
    # Determine most common separator
    most_common_separator = word_separators.most_common(1)[0][0] if word_separators else 'space'
    
    # Determine average filename length
    avg_length = sum(filename_lengths) / len(filename_lengths) if filename_lengths else 0
    
    standards = {
        'general_rules': [
            f"Use {most_common_separator}s as word separators",
            "Use Title Case for readability",
            f"Target filename length: 15-45 characters (current avg: {avg_length:.1f})",
            "Avoid special characters except hyphens and underscores",
            "Use descriptive, specific names",
            "Include content type indicator when helpful"
        ],
        'content_type_patterns': {
            'adventures': "Adventure_Name or Quest_Title_Chapter",
            'people': "Character_Full_Name or Title_Character_Name",
            'places': "Location_Name or Region_Specific_Place",
            'groups': "Organization_Name or Faction_Full_Title",
            'lore': "Topic_Name or Historical_Event_Name",
            'items': "Item_Name or Artifact_Title",
            'mechanics': "System_Name or Rule_Category",
            'templates': "Template_Purpose or Framework_Type"
        },
        'separator_recommendation': most_common_separator,
        'case_recommendation': 'Title Case',
        'length_recommendation': '15-45 characters',
        'examples': {
            'good': [
                "Queen_Seraphina_Lumengarde.md",
                "The_Crystal_Throne.md",
                "Port_Meridian_Districts.md",
                "Shadow_Magic_Rules.md"
            ],
            'bad': [
                "q.md",
                "VeryLongFileNameThatIsHardToReadAndNavigate.md",
                "file with lots of spaces and no structure.md",
                "File@#$%WithSpecial!Characters.md"
            ]
        }
    }
    
    return standards

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    print("File Naming Analysis")
    print("===================")
    
    # Analyze general patterns
    print("Analyzing filename patterns...")
    patterns, naming_by_directory, filename_lengths, word_separators = analyze_filename_patterns(vault_path)
    
    print(f"\nFilename Pattern Analysis:")
    print(f"Total files analyzed: {sum(len(files) for files in naming_by_directory.values())}")
    print(f"Average filename length: {sum(filename_lengths) / len(filename_lengths):.1f} characters")
    
    print(f"\nWord Separators:")
    for separator, count in word_separators.most_common():
        print(f"  {separator}: {count} files")
    
    print(f"\nPattern Distribution:")
    for pattern_name, files in patterns.items():
        if files:
            print(f"  {pattern_name}: {len(files)} files")
            if len(files) <= 5:
                for file in files:
                    print(f"    {file}")
            else:
                for file in files[:3]:
                    print(f"    {file}")
                print(f"    ... and {len(files) - 3} more")
    
    # Analyze by content type
    print(f"\nAnalyzing naming by content type...")
    content_naming = analyze_content_type_naming(vault_path)
    
    for content_type, data in content_naming.items():
        print(f"\n{content_type.upper()} ({data['count']} files):")
        patterns_data = data['patterns']
        print(f"  Title case: {patterns_data['title_case_count']}")
        print(f"  Snake case: {patterns_data['snake_case_count']}")
        print(f"  Kebab case: {patterns_data['kebab_case_count']}")
        print(f"  Space separated: {patterns_data['space_separated_count']}")
        
        if patterns_data['prefix_patterns']:
            print(f"  Common prefixes: {', '.join([f'{k}({v})' for k, v in patterns_data['prefix_patterns'].most_common(3)])}")
    
    # Generate standards
    print(f"\nGenerating naming standards...")
    standards = generate_naming_standards((patterns, naming_by_directory, filename_lengths, word_separators))
    
    print(f"\nRecommended Standards:")
    for rule in standards['general_rules']:
        print(f"  - {rule}")
    
    print(f"\nContent Type Patterns:")
    for content_type, pattern in standards['content_type_patterns'].items():
        print(f"  {content_type}: {pattern}")
    
    # Save analysis results
    analysis_file = os.path.join(vault_path, "scripts", "filename_analysis_results.json")
    analysis_data = {
        'patterns': {k: v[:50] for k, v in patterns.items()},  # Limit for file size
        'content_type_analysis': content_naming,
        'filename_lengths': {
            'average': sum(filename_lengths) / len(filename_lengths),
            'min': min(filename_lengths),
            'max': max(filename_lengths),
            'distribution': {
                'very_short': len([l for l in filename_lengths if l < 10]),
                'short': len([l for l in filename_lengths if 10 <= l < 20]),
                'medium': len([l for l in filename_lengths if 20 <= l < 40]),
                'long': len([l for l in filename_lengths if 40 <= l < 60]),
                'very_long': len([l for l in filename_lengths if l >= 60])
            }
        },
        'word_separators': dict(word_separators),
        'recommended_standards': standards
    }
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed analysis saved to: {analysis_file}")

if __name__ == "__main__":
    main()