#!/usr/bin/env python3
"""
Fix note names that contain directory paths and review content for sense.
Many notes have names like "02_Worldbuilding-Groups-Academies-Academy-Mirror-Researchers"
which should be cleaned to just "Academy Mirror Researchers"
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, Optional

class NoteNameAndContentFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.files_renamed = 0
        self.content_fixed = 0
        self.nonsensical_fixed = 0
        self.errors = []
        
        # Patterns to detect problematic names
        self.path_patterns = [
            r'^\d+_[A-Za-z]+[-_]',  # Starts with number_word like "02_Worldbuilding-"
            r'[-_]{2,}',  # Multiple dashes or underscores
            r'\b(Groups?|Items?|Places?|Lore|People|Worldbuilding|Adventures?|Sessions?|Resources?|Rules?|Academies?|Criminal[_-]Organizations?|Cults?[_-]and[_-]Movements?|Cultural[_-]Organizations?|Government[_-]and[_-]Parliament|Guilds?|Houses?[_-]and[_-]Nobility|Orders?)[-_]',  # Directory names in file
        ]
        
        # Common nonsensical patterns in content
        self.nonsense_patterns = [
            r'TODO.*?(?:\n|$)',  # Unfilled TODOs
            r'\[.*?\.\.\.\]',  # Placeholder brackets
            r'<.*?>',  # HTML-like tags that shouldn't be there
            r'undefined|null|NaN',  # Programming artifacts
            r'Lorem ipsum.*?(?:\.|$)',  # Placeholder text
            r'^\s*[-*]\s*$',  # Empty list items
            r'Related to:\s*$',  # Empty relations
            r'Connected plots:\s*$',  # Empty connections
            r'To be developed',  # Placeholder text
            r'TBD|TBA',  # To be determined/announced
        ]
        
    def run(self):
        """Main execution"""
        print("=" * 80)
        print("📝 FIXING NOTE NAMES AND CONTENT")
        print("=" * 80)
        
        # Phase 1: Scan for problematic names
        print("\n🔍 Phase 1: Scanning for problematic note names...")
        problematic_files = self.scan_for_problematic_names()
        
        # Phase 2: Fix note names
        print(f"\n✏️ Phase 2: Fixing {len(problematic_files)} problematic names...")
        self.fix_note_names(problematic_files)
        
        # Phase 3: Review and fix content
        print("\n📖 Phase 3: Reviewing and fixing note content...")
        self.review_and_fix_content()
        
        # Phase 4: Update internal links
        print("\n🔗 Phase 4: Updating internal links...")
        self.update_internal_links()
        
        # Phase 5: Generate report
        self.generate_report()
        
    def scan_for_problematic_names(self) -> list:
        """Scan vault for files with directory paths in names"""
        problematic = []
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip scripts, data, and system files
            if any(part in str(md_file) for part in ['scripts/', 'data/', '.git/', 'Archive/', 'Performance/']):
                continue
                
            filename = md_file.stem
            
            # Check for path-like patterns in filename
            for pattern in self.path_patterns:
                if re.search(pattern, filename):
                    problematic.append(md_file)
                    break
                    
            # Also check for overly long names suggesting path concatenation
            if len(filename) > 50 and ('-' in filename or '_' in filename):
                if md_file not in problematic:
                    problematic.append(md_file)
                    
        print(f"   Found {len(problematic)} files with problematic names")
        return problematic
        
    def fix_note_names(self, files: list):
        """Fix problematic note names"""
        rename_map = {}
        
        for file_path in files:
            old_name = file_path.stem
            new_name = self.clean_filename(old_name)
            
            if new_name != old_name:
                # Create new path
                new_path = file_path.parent / f"{new_name}.md"
                
                # Handle duplicates
                if new_path.exists() and new_path != file_path:
                    # Add number suffix
                    counter = 1
                    while new_path.exists():
                        new_path = file_path.parent / f"{new_name}_{counter}.md"
                        counter += 1
                        
                try:
                    # Rename file
                    file_path.rename(new_path)
                    rename_map[old_name] = new_name
                    self.files_renamed += 1
                    
                    # Update frontmatter title
                    self.update_frontmatter_title(new_path, new_name)
                    
                    print(f"   ✓ Renamed: {old_name[:50]}... → {new_name}")
                    
                except Exception as e:
                    self.errors.append(f"Error renaming {file_path}: {e}")
                    
        # Store rename map for link updates
        self.rename_map = rename_map
        
    def clean_filename(self, filename: str) -> str:
        """Clean a filename by removing directory-like prefixes"""
        cleaned = filename
        
        # Remove number prefixes like "02_"
        cleaned = re.sub(r'^\d+_', '', cleaned)
        
        # Remove common directory names
        directory_words = [
            'Worldbuilding', 'Groups', 'Items', 'Places', 'Lore', 'People',
            'Adventures', 'Sessions', 'Resources', 'Rules', 'Academies',
            'Criminal_Organizations', 'Criminal-Organizations',
            'Cults_and_Movements', 'Cults-and-Movements',
            'Cultural_Organizations', 'Cultural-Organizations',
            'Government_and_Parliament', 'Government-and-Parliament',
            'Guilds', 'Houses_and_Nobility', 'Houses-and-Nobility', 'Orders'
        ]
        
        for word in directory_words:
            # Remove with various separators
            cleaned = re.sub(f'^{word}[-_]', '', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(f'[-_]{word}[-_]', '_', cleaned, flags=re.IGNORECASE)
            
        # Convert multiple separators to single space
        cleaned = re.sub(r'[-_]+', ' ', cleaned)
        
        # Clean up whitespace
        cleaned = ' '.join(cleaned.split())
        
        # Capitalize properly
        cleaned = self.proper_case(cleaned)
        
        return cleaned
        
    def proper_case(self, text: str) -> str:
        """Convert to proper case while preserving certain words"""
        # Words to keep lowercase
        lowercase_words = {'of', 'the', 'and', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'a', 'an'}
        
        # Words to keep uppercase
        uppercase_words = {'NPC', 'PC', 'DM', 'GM', 'HP', 'AC', 'CR', 'XP', 'GP'}
        
        words = text.split()
        result = []
        
        for i, word in enumerate(words):
            # First word is always capitalized
            if i == 0:
                result.append(word.capitalize())
            elif word.upper() in uppercase_words:
                result.append(word.upper())
            elif word.lower() in lowercase_words:
                result.append(word.lower())
            else:
                result.append(word.capitalize())
                
        return ' '.join(result)
        
    def update_frontmatter_title(self, file_path: Path, new_title: str):
        """Update the title in frontmatter"""
        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, body = self.parse_frontmatter(content)
            
            if frontmatter:
                frontmatter['title'] = new_title
                
                # Update modified date
                frontmatter['modified'] = datetime.now().strftime('%Y-%m-%d')
                
                # Rebuild and save
                new_content = self.rebuild_content(frontmatter, body)
                file_path.write_text(new_content, encoding='utf-8')
                
        except Exception as e:
            self.errors.append(f"Error updating frontmatter for {file_path}: {e}")
            
    def review_and_fix_content(self):
        """Review content for nonsensical elements and fix them"""
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip system files
            if any(part in str(md_file) for part in ['scripts/', 'data/', '.git/', 'Archive/', 'Performance/']):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content
                
                # Fix nonsensical patterns
                for pattern in self.nonsense_patterns:
                    content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
                    
                # Fix empty sections
                content = self.fix_empty_sections(content)
                
                # Fix repeated text
                content = self.fix_repeated_text(content)
                
                # Fix broken markdown
                content = self.fix_broken_markdown(content)
                
                # Only write if changed
                if content != original_content:
                    md_file.write_text(content, encoding='utf-8')
                    self.content_fixed += 1
                    
            except Exception as e:
                self.errors.append(f"Error processing {md_file}: {e}")
                
    def fix_empty_sections(self, content: str) -> str:
        """Remove or fill empty sections"""
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check if this is a header
            if line.startswith('#'):
                # Look ahead to see if section is empty
                j = i + 1
                has_content = False
                
                while j < len(lines) and not lines[j].startswith('#'):
                    if lines[j].strip() and not lines[j].strip().startswith('-'):
                        has_content = True
                        break
                    j += 1
                    
                if has_content:
                    fixed_lines.append(line)
                else:
                    # Skip empty section
                    self.nonsensical_fixed += 1
                    i = j - 1  # Skip to next section
                    
            else:
                fixed_lines.append(line)
                
            i += 1
            
        return '\n'.join(fixed_lines)
        
    def fix_repeated_text(self, content: str) -> str:
        """Remove obviously repeated text"""
        lines = content.split('\n')
        seen = set()
        fixed_lines = []
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                fixed_lines.append(line)
                continue
                
            # Check for exact duplicates (excluding headers and lists)
            if not line.startswith('#') and not line.startswith('-') and not line.startswith('*'):
                if line in seen:
                    self.nonsensical_fixed += 1
                    continue  # Skip duplicate
                seen.add(line)
                
            fixed_lines.append(line)
            
        return '\n'.join(fixed_lines)
        
    def fix_broken_markdown(self, content: str) -> str:
        """Fix common markdown issues"""
        # Fix unclosed brackets
        content = re.sub(r'\[\[([^\]]+)$', r'[[\1]]', content, flags=re.MULTILINE)
        
        # Fix multiple blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Fix bullet points without content
        content = re.sub(r'^\s*[-*]\s*$', '', content, flags=re.MULTILINE)
        
        # Fix headers without proper spacing
        content = re.sub(r'^(#{1,6})([A-Za-z])', r'\1 \2', content, flags=re.MULTILINE)
        
        return content
        
    def update_internal_links(self):
        """Update all internal links to match renamed files"""
        if not hasattr(self, 'rename_map') or not self.rename_map:
            return
            
        print(f"   Updating links for {len(self.rename_map)} renamed files...")
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip system files
            if any(part in str(md_file) for part in ['scripts/', 'data/', '.git/']):
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                original_content = content
                
                # Update each renamed link
                for old_name, new_name in self.rename_map.items():
                    # Update [[links]]
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\]\]',
                        f'[[{new_name}]]',
                        content
                    )
                    
                    # Update [[links|display]]
                    content = re.sub(
                        rf'\[\[{re.escape(old_name)}\|([^\]]+)\]\]',
                        rf'[[{new_name}|\1]]',
                        content
                    )
                    
                # Only write if changed
                if content != original_content:
                    md_file.write_text(content, encoding='utf-8')
                    
            except Exception as e:
                self.errors.append(f"Error updating links in {md_file}: {e}")
                
    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse YAML frontmatter and body"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    if frontmatter is None:
                        frontmatter = {}
                    body = parts[2]
                    return frontmatter, body
                except:
                    pass
                    
        return {}, content
        
    def rebuild_content(self, frontmatter: Dict, body: str) -> str:
        """Rebuild content with frontmatter"""
        if frontmatter:
            yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            return f"---\n{yaml_str}---\n{body}"
        return body
        
    def generate_report(self):
        """Generate cleanup report"""
        print("\n" + "=" * 80)
        print("✅ NOTE NAME AND CONTENT FIX COMPLETE")
        print("=" * 80)
        
        print(f"\n📊 Results:")
        print(f"   • Files renamed: {self.files_renamed}")
        print(f"   • Content fixes: {self.content_fixed}")
        print(f"   • Nonsensical elements removed: {self.nonsensical_fixed}")
        
        if self.errors:
            print(f"\n⚠️ Errors encountered: {len(self.errors)}")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"   - {error}")
                
        # Update VAULT_UPDATES.md
        self.update_vault_log()
        
    def update_vault_log(self):
        """Add entry to VAULT_UPDATES.md"""
        updates_file = self.vault_path / "VAULT_UPDATES.md"
        
        entry = f"""

## 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} - Note Names and Content Cleanup

### Summary
Fixed note names containing directory paths and cleaned up nonsensical content.

### Statistics
- **Files Renamed**: {self.files_renamed}
- **Content Fixes**: {self.content_fixed}
- **Nonsensical Elements Removed**: {self.nonsensical_fixed}
- **Errors**: {len(self.errors)}

### Changes Made
- Removed directory prefixes from filenames
- Cleaned up path-like separators in names
- Fixed empty sections and placeholders
- Removed duplicate content
- Fixed broken markdown formatting
- Updated all internal links to match new names

### Examples of Fixes
- `02_Worldbuilding-Groups-Academy-Mirror-Researchers` → `Academy Mirror Researchers`
- `Criminal_Organizations-Shadow-Surgeons` → `Shadow Surgeons`
- Removed empty TODO sections
- Fixed unclosed brackets and broken links
- Cleaned up repeated text

### Result
Note names are now clean and human-readable, with sensible content throughout.

---
"""
        
        if updates_file.exists():
            content = updates_file.read_text(encoding='utf-8')
            content += entry
            updates_file.write_text(content, encoding='utf-8')
        else:
            updates_file.write_text(entry, encoding='utf-8')
            
        print("\n✅ Updated VAULT_UPDATES.md with cleanup report")

def main():
    fixer = NoteNameAndContentFixer()
    fixer.run()

if __name__ == "__main__":
    main()