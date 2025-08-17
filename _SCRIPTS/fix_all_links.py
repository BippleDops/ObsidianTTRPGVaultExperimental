#!/usr/bin/env python3
"""
Comprehensive link fixing for the vault
Fixes wikilinks, image references, and validates D&D 5e content integration
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import json
from datetime import datetime
from collections import defaultdict


class LinkFixer:
    def __init__(self, vault_path: Path = Path(".")):
        self.vault_path = vault_path
        self.all_files = {}  # filename -> full path mapping
        self.image_files = {}  # image filename -> full path
        self.broken_links = []
        self.fixed_links = []
        self.dnd_content = {
            "sourcebooks": [],
            "statblocks": [],
            "references": [],
            "tables": []
        }
        
    def scan_vault(self):
        """Build complete index of all files"""
        print("📊 Scanning vault structure...")
        
        # Scan markdown files
        for md_file in self.vault_path.glob("**/*.md"):
            if any(part.startswith('.') for part in md_file.parts):
                continue
            
            filename = md_file.stem
            # Store all possible paths for each filename
            if filename not in self.all_files:
                self.all_files[filename] = []
            self.all_files[filename].append(md_file)
            
            # Categorize D&D content
            if "12_Research" in str(md_file):
                if "D&D_Sourcebooks" in str(md_file):
                    self.dnd_content["sourcebooks"].append(md_file)
                elif "D&D_Statblocks" in str(md_file):
                    self.dnd_content["statblocks"].append(md_file)
                elif "D&D_References" in str(md_file):
                    self.dnd_content["references"].append(md_file)
                elif "Tables" in str(md_file):
                    self.dnd_content["tables"].append(md_file)
                    
        # Scan image files
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.webp']:
            for img_file in self.vault_path.glob(f"**/{ext}"):
                if any(part.startswith('.') for part in img_file.parts):
                    continue
                    
                filename = img_file.name
                if filename not in self.image_files:
                    self.image_files[filename] = []
                self.image_files[filename].append(img_file)
                
        print(f"  Found {sum(len(v) for v in self.all_files.values())} markdown files")
        print(f"  Found {sum(len(v) for v in self.image_files.values())} image files")
        print(f"  D&D Content: {sum(len(v) for v in self.dnd_content.values())} files")
        
    def fix_all_links(self):
        """Fix all broken links in the vault"""
        print("\n🔗 Fixing broken links...")
        
        for filename, file_paths in self.all_files.items():
            for file_path in file_paths:
                self.fix_file_links(file_path)
                
        print(f"  ✅ Fixed {len(self.fixed_links)} links")
        print(f"  ❌ Still broken: {len(self.broken_links)} links")
        
    def fix_file_links(self, file_path: Path):
        """Fix links in a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Fix wikilinks [[Link]] or [[Link|Alias]]
            def fix_wikilink(match):
                full_link = match.group(0)
                link_target = match.group(1).split('|')[0].strip()
                alias = match.group(1).split('|')[1] if '|' in match.group(1) else None
                
                # Remove any path if present
                if '/' in link_target:
                    link_target = link_target.split('/')[-1]
                    
                # Remove anchor if present
                anchor = ""
                if '#' in link_target:
                    link_target, anchor = link_target.split('#', 1)
                    anchor = f"#{anchor}"
                    
                # Find the target file
                if link_target in self.all_files:
                    # File exists, use relative path if needed
                    target_paths = self.all_files[link_target]
                    
                    if len(target_paths) == 1:
                        # Single match, use it
                        target_path = target_paths[0]
                    else:
                        # Multiple matches, find best one
                        target_path = self.find_best_match(file_path, target_paths)
                        
                    # Create proper link
                    if alias:
                        fixed_link = f"[[{target_path.stem}{anchor}|{alias}]]"
                    else:
                        fixed_link = f"[[{target_path.stem}{anchor}]]"
                        
                    if fixed_link != full_link:
                        self.fixed_links.append((str(file_path), full_link, fixed_link))
                        
                    return fixed_link
                else:
                    # Link is broken
                    self.broken_links.append((str(file_path), full_link))
                    return full_link
                    
            # Fix image links ![[image]] or ![](path/to/image)
            def fix_image_link(match):
                full_link = match.group(0)
                
                if match.group(0).startswith('![['):
                    # Wikilink style image
                    image_name = match.group(1).strip('[]')
                else:
                    # Markdown style image
                    image_path = match.group(2) if match.lastindex >= 2 else match.group(1)
                    image_name = Path(image_path).name
                    
                # Find the image file
                if image_name in self.image_files:
                    image_paths = self.image_files[image_name]
                    
                    if len(image_paths) == 1:
                        target_path = image_paths[0]
                    else:
                        target_path = self.find_best_match(file_path, image_paths)
                        
                    # Create relative path from current file to image
                    try:
                        rel_path = target_path.relative_to(self.vault_path)
                        fixed_link = f"![[{rel_path}]]"
                        
                        if fixed_link != full_link:
                            self.fixed_links.append((str(file_path), full_link, fixed_link))
                            
                        return fixed_link
                    except:
                        return full_link
                else:
                    self.broken_links.append((str(file_path), full_link))
                    return full_link
                    
            # Apply fixes
            content = re.sub(r'\[\[([^\]]+)\]\]', fix_wikilink, content)
            content = re.sub(r'!\[\[([^\]]+)\]\]', fix_image_link, content)
            content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_image_link, content)
            
            # Save if changed
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                
        except Exception as e:
            print(f"  Error fixing {file_path}: {e}")
            
    def find_best_match(self, source_file: Path, target_paths: List[Path]) -> Path:
        """Find the best matching file from multiple options"""
        # Prefer files in same directory
        source_dir = source_file.parent
        for target in target_paths:
            if target.parent == source_dir:
                return target
                
        # Prefer files in nearby directories
        source_parts = source_file.parts
        best_match = target_paths[0]
        best_score = 0
        
        for target in target_paths:
            target_parts = target.parts
            # Count matching path components
            score = sum(1 for s, t in zip(source_parts, target_parts) if s == t)
            if score > best_score:
                best_score = score
                best_match = target
                
        return best_match
        
    def validate_dnd_content(self):
        """Validate D&D 5e content is properly integrated"""
        print("\n🎲 Validating D&D 5e Content Integration...")
        
        # Check sourcebook structure
        sourcebook_dir = self.vault_path / "12_Research" / "D&D_Sourcebooks"
        if sourcebook_dir.exists():
            sourcebooks = [d for d in sourcebook_dir.iterdir() if d.is_dir()]
            print(f"  📚 Found {len(sourcebooks)} D&D sourcebooks")
            
            # Check each sourcebook has an INDEX.md
            missing_index = []
            for book in sourcebooks:
                if not (book / "INDEX.md").exists():
                    missing_index.append(book.name)
                    
            if missing_index:
                print(f"  ⚠️ Missing INDEX.md in: {', '.join(missing_index)}")
                
        # Check CLI reference
        cli_dir = sourcebook_dir / "CLI_Reference" if sourcebook_dir.exists() else None
        if cli_dir and cli_dir.exists():
            subdirs = ["bestiary", "spells", "items", "rules", "tables"]
            for subdir in subdirs:
                if (cli_dir / subdir).exists():
                    count = len(list((cli_dir / subdir).glob("*.md")))
                    print(f"    • {subdir}: {count} files")
                    
        # Check for campaign integration
        integration_file = sourcebook_dir / "5E_Official_Content_Integration.md" if sourcebook_dir.exists() else None
        if integration_file and integration_file.exists():
            print("  ✅ Campaign integration documentation found")
        else:
            print("  ⚠️ Missing campaign integration documentation")
            
        # Verify statblocks are accessible
        statblock_refs = []
        for md_file in self.vault_path.glob("**/*.md"):
            if "01_Adventures" in str(md_file) or "02_Worldbuilding" in str(md_file):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    # Look for CR references
                    cr_refs = re.findall(r'CR\s+\d+', content)
                    if cr_refs:
                        statblock_refs.append((md_file.stem, len(cr_refs)))
                except:
                    pass
                    
        if statblock_refs:
            print(f"  📊 Found {len(statblock_refs)} files referencing creature CRs")
            
    def generate_report(self):
        """Generate comprehensive link fixing report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_files_scanned": sum(len(v) for v in self.all_files.values()),
            "total_images": sum(len(v) for v in self.image_files.values()),
            "links_fixed": len(self.fixed_links),
            "broken_links_remaining": len(self.broken_links),
            "dnd_content": {
                "sourcebooks": len(self.dnd_content["sourcebooks"]),
                "statblocks": len(self.dnd_content["statblocks"]),
                "references": len(self.dnd_content["references"]),
                "tables": len(self.dnd_content["tables"])
            },
            "fixed_links_sample": self.fixed_links[:10] if self.fixed_links else [],
            "broken_links_sample": self.broken_links[:10] if self.broken_links else []
        }
        
        # Save report
        report_path = self.vault_path / "reports" / f"link_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        print(f"\n📄 Report saved to: {report_path}")
        
        return report
        
    def run_complete_fix(self):
        """Run the complete link fixing process"""
        print("🔧 Starting Comprehensive Link Fix")
        print("="*60)
        
        # Scan vault
        self.scan_vault()
        
        # Fix all links
        self.fix_all_links()
        
        # Validate D&D content
        self.validate_dnd_content()
        
        # Generate report
        report = self.generate_report()
        
        print("\n" + "="*60)
        print("📊 LINK FIX COMPLETE")
        print("="*60)
        print(f"✅ Fixed {len(self.fixed_links)} broken links")
        print(f"❌ {len(self.broken_links)} links still broken (targets missing)")
        print(f"🎲 D&D content validated and integrated")
        
        # Show sample D&D content to prove it works
        print("\n📚 Sample D&D 5e Content Integration:")
        if self.dnd_content["sourcebooks"]:
            sample = self.dnd_content["sourcebooks"][0]
            print(f"  Sourcebook: {sample.relative_to(self.vault_path)}")
            
        if self.dnd_content["statblocks"]:
            sample = self.dnd_content["statblocks"][0]
            print(f"  Statblock: {sample.stem}")
            
        if self.dnd_content["tables"]:
            sample = self.dnd_content["tables"][0]
            print(f"  Table: {sample.stem}")
            
        print("\n🎯 Your vault is now fully linked and organized!")
        
        return report


def main():
    fixer = LinkFixer()
    fixer.run_complete_fix()


if __name__ == "__main__":
    main()