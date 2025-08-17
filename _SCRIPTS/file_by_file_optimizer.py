#!/usr/bin/env python3
"""
File-by-file vault optimizer following safe principles:
- Only remove 99%+ duplicates
- Preserve all D&D 5e content
- Add enhancements without deletion
- Fix links and formatting
"""

import re
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
import json
from collections import defaultdict
import difflib

class FileOptimizer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.optimizations = []
        self.preserved_dnd = []
        self.enhanced_files = []
        self.duplicate_groups = defaultdict(list)
        
        # D&D 5e patterns to preserve
        self.dnd_patterns = [
            r'\bCR\s+\d+',
            r'Challenge Rating',
            r'\bAC\s+\d+',
            r'Hit Points?',
            r'\bHP\s+\d+',
            r'd\d+\s*([\+\-]\s*\d+)?',
            r'(PHB|DMG|MM|XGE|TCE|VGM|MTF)',
            r'(STR|DEX|CON|INT|WIS|CHA)\s*\d+',
            r'spell slot',
            r'saving throw',
            r'ability check',
            r'(advantage|disadvantage)',
            r'proficiency bonus',
            r'DC\s+\d+',
            r'damage type',
            r'condition',
            r'(Action|Bonus Action|Reaction)',
            r'5e|5th edition|D&D'
        ]
        
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity ratio between two texts (must be 99%+ to be duplicate)"""
        # Normalize for comparison
        norm1 = re.sub(r'\s+', ' ', text1).strip().lower()
        norm2 = re.sub(r'\s+', ' ', text2).strip().lower()
        
        # Use difflib for accurate similarity
        return difflib.SequenceMatcher(None, norm1, norm2).ratio()
        
    def is_dnd_content(self, content: str) -> bool:
        """Check if content contains D&D 5e material"""
        for pattern in self.dnd_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
        
    def optimize_file(self, file_path: Path) -> Dict:
        """Optimize a single file"""
        result = {
            "file": str(file_path.relative_to(self.vault_path)),
            "actions": [],
            "preserved": False,
            "enhanced": False
        }
        
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # 1. Check if D&D content (always preserve)
            if self.is_dnd_content(content):
                result["preserved"] = True
                result["actions"].append("Preserved: D&D 5e content")
                self.preserved_dnd.append(str(file_path))
                
            # 2. Fix formatting issues
            content = self.fix_formatting(content, file_path)
            if content != original_content:
                result["actions"].append("Fixed: Formatting issues")
                
            # 3. Fix broken links
            content = self.fix_links(content, file_path)
            if content != original_content:
                result["actions"].append("Fixed: Broken wikilinks")
                
            # 4. Add metadata if missing
            content = self.ensure_metadata(content, file_path)
            if content != original_content:
                result["actions"].append("Added: Missing metadata")
                
            # 5. Add cross-references
            content = self.add_cross_references(content, file_path)
            if content != original_content:
                result["actions"].append("Enhanced: Cross-references")
                result["enhanced"] = True
                
            # 6. Add semantic tags
            content = self.add_semantic_tags(content, file_path)
            if content != original_content:
                result["actions"].append("Enhanced: Semantic tags")
                result["enhanced"] = True
                
            # Save if changed
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                self.enhanced_files.append(str(file_path))
                
            # Track for duplicate detection (but don't delete yet)
            content_hash = hashlib.md5(content.encode()).hexdigest()
            self.duplicate_groups[content_hash].append(file_path)
            
        except Exception as e:
            result["actions"].append(f"Error: {e}")
            
        return result
        
    def fix_formatting(self, content: str, file_path: Path) -> str:
        """Fix common formatting issues"""
        
        # Fix multiple blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        # Fix heading spacing
        content = re.sub(r'(#+)\s*([^\n]+)\n(?!\n)', r'\1 \2\n\n', content)
        
        # Fix list formatting
        content = re.sub(r'^(\s*)-\s+', r'\1- ', content, flags=re.MULTILINE)
        content = re.sub(r'^(\s*)\*\s+', r'\1- ', content, flags=re.MULTILINE)
        
        # Fix code block formatting
        content = re.sub(r'```\n\n', '```\n', content)
        content = re.sub(r'\n\n```', '\n```', content)
        
        return content
        
    def fix_links(self, content: str, file_path: Path) -> str:
        """Fix broken wikilinks"""
        
        # Find all wikilinks
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
        
        for link in wikilinks:
            # Skip if link has pipe
            if '|' in link:
                continue
                
            # Try to find the target file
            target = self.find_link_target(link)
            if target and target != link:
                # Replace with correct link
                content = content.replace(f'[[{link}]]', f'[[{target}]]')
                
        return content
        
    def find_link_target(self, link: str) -> Optional[str]:
        """Find the correct target for a wikilink"""
        
        # Clean the link
        clean_link = link.strip().replace('_', ' ')
        
        # Search for matching files
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.stem.lower() == clean_link.lower():
                # Return relative path without extension
                relative = md_file.relative_to(self.vault_path)
                return str(relative).replace('.md', '')
                
        return None
        
    def ensure_metadata(self, content: str, file_path: Path) -> str:
        """Ensure file has proper metadata"""
        
        # Check if has frontmatter
        if not content.startswith('---\n'):
            # Add basic frontmatter
            metadata = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: {self.determine_type(file_path)}
status: active
tags:
- {self.determine_tag(file_path)}
---

"""
            content = metadata + content
            
        return content
        
    def determine_type(self, file_path: Path) -> str:
        """Determine content type from path"""
        path_str = str(file_path).lower()
        
        if 'adventure' in path_str or 'campaign' in path_str or 'session' in path_str:
            return 'adventure'
        elif 'npc' in path_str or 'people' in path_str:
            return 'npc'
        elif 'place' in path_str or 'location' in path_str:
            return 'location'
        elif 'group' in path_str or 'faction' in path_str or 'organization' in path_str:
            return 'faction'
        elif 'item' in path_str or 'treasure' in path_str:
            return 'item'
        elif 'mechanic' in path_str or 'rule' in path_str:
            return 'mechanic'
        elif 'lore' in path_str or 'history' in path_str:
            return 'lore'
        else:
            return 'note'
            
    def determine_tag(self, file_path: Path) -> str:
        """Determine primary tag from path"""
        parts = file_path.parts
        
        if '00_Indexes' in parts:
            return 'index'
        elif '01_Adventures' in parts:
            return 'adventure'
        elif '02_Worldbuilding' in parts:
            return 'worldbuilding'
        elif '03_Mechanics' in parts:
            return 'mechanics'
        elif '04_Resources' in parts:
            return 'resource'
        elif '12_Research' in parts:
            return 'dnd5e'
        else:
            return 'general'
            
    def add_cross_references(self, content: str, file_path: Path) -> str:
        """Add intelligent cross-references"""
        
        # Don't add to D&D sourcebook content
        if '12_Research' in str(file_path):
            return content
            
        # Look for keywords to link
        keywords_to_link = {
            'Aquabyssos': '[[02_Worldbuilding/Lore/Aquabyssos World Guide]]',
            'Aethermoor': '[[02_Worldbuilding/Lore/Aethermoor World Guide]]',
            'Shadow Conspiracy': '[[02_Worldbuilding/Groups/Criminal_Organizations/The Shadow Conspiracy]]',
            'Crystal Wardens': '[[02_Worldbuilding/Groups/Crystal Wardens]]',
            'Seven Shards': '[[01_Adventures/Seven_Shards_Campaign/Campaign_Overview]]',
            'Parliament of Echoes': '[[02_Worldbuilding/Groups/Government_and_Parliament/Parliament of Echoes]]',
            'Deep Mother': '[[02_Worldbuilding/Groups/Cults_and_Movements/Cult of the Deep Mother]]'
        }
        
        # Add cross-reference section if keywords found
        found_refs = []
        for keyword, link in keywords_to_link.items():
            if keyword in content and link not in content:
                found_refs.append(link)
                
        if found_refs and '## Related' not in content:
            content += '\n\n## Related\n'
            for ref in found_refs[:5]:  # Max 5 references
                content += f'- {ref}\n'
                
        return content
        
    def add_semantic_tags(self, content: str, file_path: Path) -> str:
        """Add semantic tags based on content"""
        
        # Check if has frontmatter with tags
        if content.startswith('---\n'):
            # Find tags section
            frontmatter_end = content.find('---\n', 4)
            if frontmatter_end != -1:
                frontmatter = content[:frontmatter_end]
                
                # Determine additional tags
                new_tags = []
                
                if 'underwater' in content.lower() or 'aquatic' in content.lower():
                    new_tags.append('aquatic')
                if 'aerial' in content.lower() or 'sky' in content.lower():
                    new_tags.append('aerial')
                if 'shadow' in content.lower():
                    new_tags.append('shadow-touched')
                if 'crystal' in content.lower():
                    new_tags.append('crystal-enhanced')
                if re.search(r'session\s+\d+', content, re.IGNORECASE):
                    new_tags.append('session-notes')
                if 'quest' in content.lower():
                    new_tags.append('quest')
                if 'combat' in content.lower() or 'encounter' in content.lower():
                    new_tags.append('combat')
                    
                # Add new tags to frontmatter
                if new_tags and 'tags:' in frontmatter:
                    for tag in new_tags:
                        if f'- {tag}' not in frontmatter:
                            frontmatter = frontmatter.replace('tags:', f'tags:\n- {tag}', 1)
                            
                    content = frontmatter + content[frontmatter_end:]
                    
        return content
        
    def process_duplicates(self):
        """Process duplicate groups (only remove 99%+ similar)"""
        removed_count = 0
        
        for content_hash, file_list in self.duplicate_groups.items():
            if len(file_list) <= 1:
                continue
                
            # Sort by path depth (keep files in better locations)
            file_list.sort(key=lambda p: (len(p.parts), str(p)))
            
            # Keep the first file
            keeper = file_list[0]
            keeper_content = keeper.read_text(encoding='utf-8')
            
            # Check each duplicate
            for duplicate in file_list[1:]:
                # Skip if D&D content
                if str(duplicate) in self.preserved_dnd:
                    continue
                    
                # Check similarity
                dup_content = duplicate.read_text(encoding='utf-8')
                similarity = self.calculate_similarity(keeper_content, dup_content)
                
                # Only remove if 99%+ similar
                if similarity >= 0.99:
                    # Move to duplicates folder
                    dup_folder = self.vault_path / "08_Archive" / "Duplicates"
                    dup_folder.mkdir(parents=True, exist_ok=True)
                    
                    new_path = dup_folder / duplicate.name
                    if new_path.exists():
                        new_path = dup_folder / f"{duplicate.stem}_{content_hash[:8]}{duplicate.suffix}"
                        
                    duplicate.rename(new_path)
                    removed_count += 1
                    
                    self.optimizations.append({
                        "action": "removed_duplicate",
                        "file": str(duplicate.relative_to(self.vault_path)),
                        "similarity": f"{similarity:.1%}",
                        "kept": str(keeper.relative_to(self.vault_path))
                    })
                    
        return removed_count
        
    def optimize_directory(self, directory: Path):
        """Optimize all files in a directory"""
        print(f"\n📁 Optimizing {directory.name}...")
        
        md_files = list(directory.rglob("*.md"))
        print(f"   Found {len(md_files)} markdown files")
        
        optimized = 0
        for i, md_file in enumerate(md_files):
            # Skip archive and research directories
            if '08_Archive' in str(md_file) or '12_Research/D&D_Sourcebooks' in str(md_file):
                continue
                
            result = self.optimize_file(md_file)
            
            if result["actions"]:
                optimized += 1
                
            # Progress indicator
            if (i + 1) % 50 == 0:
                print(f"   Processed {i + 1}/{len(md_files)} files...")
                
        print(f"   ✅ Optimized {optimized} files")
        
        return optimized
        
    def run_full_optimization(self):
        """Run complete file-by-file optimization"""
        print("🔧 Starting File-by-File Vault Optimization")
        print("="*60)
        print("Principles:")
        print("  • Only remove 99%+ duplicates")
        print("  • Preserve all D&D 5e content")
        print("  • Add enhancements without deletion")
        print("  • Fix links and formatting")
        print("="*60)
        
        # Process each directory in order
        directories = [
            "00_Indexes",
            "01_Adventures", 
            "02_Worldbuilding",
            "03_Mechanics",
            "04_Resources",
            "05_Player_Resources",
            "06_GM_Resources"
        ]
        
        total_optimized = 0
        
        for dir_name in directories:
            dir_path = self.vault_path / dir_name
            if dir_path.exists():
                total_optimized += self.optimize_directory(dir_path)
                
        # Process duplicates
        print("\n🔍 Processing duplicates (99%+ similarity only)...")
        removed = self.process_duplicates()
        print(f"   Removed {removed} true duplicates")
        
        # Generate report
        self.generate_report(total_optimized, removed)
        
    def generate_report(self, total_optimized: int, duplicates_removed: int):
        """Generate optimization report"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "files_optimized": total_optimized,
                "duplicates_removed": duplicates_removed,
                "dnd_content_preserved": len(self.preserved_dnd),
                "files_enhanced": len(self.enhanced_files)
            },
            "preserved_dnd_files": self.preserved_dnd[:100],  # First 100
            "enhanced_files": self.enhanced_files[:100],  # First 100
            "optimizations": self.optimizations[:100]  # First 100
        }
        
        # Save report
        report_dir = self.vault_path / "reports"
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / f"file_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print("\n" + "="*60)
        print("✅ FILE-BY-FILE OPTIMIZATION COMPLETE")
        print("="*60)
        print(f"Files optimized: {total_optimized}")
        print(f"Duplicates removed: {duplicates_removed}")
        print(f"D&D content preserved: {len(self.preserved_dnd)}")
        print(f"Files enhanced: {len(self.enhanced_files)}")
        print(f"\n📄 Report saved: {report_path}")

def main():
    optimizer = FileOptimizer()
    optimizer.run_full_optimization()

if __name__ == "__main__":
    main()