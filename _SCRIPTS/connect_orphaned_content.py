#!/usr/bin/env python3
"""
Add connections to orphaned content by creating strategic links
"""

import os
import json
import re
from pathlib import Path

def add_to_index_file(index_path, new_entry, section="Additional Content"):
    """Add a new entry to an index file"""
    if not index_path.exists():
        return False
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for a section to add to, or create one
        if f"## {section}" in content:
            # Add to existing section
            section_pattern = f"(## {section}.*?)(\n## |\n---|\nZ)"
            match = re.search(section_pattern, content, re.DOTALL)
            if match:
                new_content = content[:match.end(1)] + f"\n- {new_entry}" + content[match.end(1):]
            else:
                # Add at end of section
                new_content = content + f"\n- {new_entry}"
        else:
            # Create new section
            new_content = content + f"\n\n## {section}\n\n- {new_entry}"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {index_path}: {e}")
        return False

def connect_orphaned_files():
    vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")
    
    # Load orphaned files data
    with open(vault_path / "broken_links_analysis.json", 'r') as f:
        data = json.load(f)
    
    orphaned_files = data['orphaned_files'][:100]  # Process first 100 for efficiency
    connections_made = 0
    
    # Define index files and their target directories
    indexes = {
        "02_Worldbuilding/Groups": "Master_Groups_Index.md",
        "02_Worldbuilding/People": "Master_People_Index.md", 
        "02_Worldbuilding/Places": "Master_Places_Index.md",
        "02_Worldbuilding/Lore": "Master_Lore_Index.md",
        "01_Adventures": "Master_Campaign_Index.md"
    }
    
    for orphan_file in orphaned_files:
        try:
            # Determine which index this file should be added to
            for directory, index_file in indexes.items():
                if orphan_file.startswith(directory):
                    file_name = Path(orphan_file).stem
                    index_path = vault_path / index_file
                    
                    # Create a link entry
                    link_entry = f"[[{orphan_file}|{file_name}]]"
                    
                    if add_to_index_file(index_path, link_entry, "Orphaned Content"):
                        print(f"Added {file_name} to {index_file}")
                        connections_made += 1
                    break
            
            # Also add backlinks to the orphaned file itself
            orphan_path = vault_path / orphan_file
            if orphan_path.exists():
                try:
                    with open(orphan_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add links to relevant index files if not present
                    if "[[Master_" not in content and "## Related" in content:
                        # Find appropriate index to link to
                        for directory, index_file in indexes.items():
                            if orphan_file.startswith(directory):
                                index_link = f"- [[{index_file}]]"
                                # Add to Related section
                                content = content.replace(
                                    "## Related Concepts", 
                                    f"## Related Concepts\n\n{index_link}"
                                )
                                break
                        
                        with open(orphan_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        connections_made += 1
                
                except Exception as e:
                    print(f"Error updating orphan file {orphan_file}: {e}")
                    
        except Exception as e:
            print(f"Error processing {orphan_file}: {e}")
    
    print(f"\nConnections made: {connections_made}")
    return connections_made

def create_cross_references():
    """Create cross-references between related files"""
    vault_path = Path("/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental")
    
    # Common cross-reference patterns
    cross_refs = [
        # Link Adventures to relevant worldbuilding
        ("01_Adventures", "02_Worldbuilding/Places"),
        ("01_Adventures", "02_Worldbuilding/Groups"),
        ("01_Adventures", "02_Worldbuilding/People"),
        
        # Link mechanics to lore
        ("03_Mechanics", "02_Worldbuilding/Lore"),
    ]
    
    refs_created = 0
    
    for source_dir, target_dir in cross_refs:
        source_files = list((vault_path / source_dir).rglob("*.md"))[:10]  # Limit for efficiency
        
        for source_file in source_files:
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # If file has very few links, add some related content
                link_count = content.count("[[")
                if link_count < 3:
                    # Add a "See Also" section
                    if "## See Also" not in content:
                        see_also = f"\n\n## See Also\n\n- [[{target_dir}]] - Related content\n- [[Master_Campaign_Index]] - Campaign overview"
                        
                        # Add before any existing reference section or at end
                        if "## References" in content:
                            content = content.replace("## References", see_also + "\n\n## References")
                        else:
                            content += see_also
                        
                        with open(source_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        refs_created += 1
                        
            except Exception as e:
                print(f"Error creating cross-ref for {source_file}: {e}")
    
    print(f"Cross-references created: {refs_created}")
    return refs_created

def main():
    print("Connecting orphaned content...")
    connections = connect_orphaned_files()
    
    print("\nCreating cross-references...")
    cross_refs = create_cross_references()
    
    print(f"\nTotal improvements: {connections + cross_refs}")

if __name__ == "__main__":
    main()