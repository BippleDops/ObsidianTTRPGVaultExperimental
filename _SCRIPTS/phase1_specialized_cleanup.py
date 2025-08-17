#!/usr/bin/env python3
"""
Phase 1 Specialized Cleanup Script
Advanced template cleanup, performance optimization, and structure validation
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import concurrent.futures

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Phase1SpecializedCleaner:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.results = []
        
    def advanced_template_cleanup(self) -> List[Dict]:
        """Advanced template placeholder cleanup with context awareness"""
        results = []
        
        # More sophisticated placeholder patterns
        advanced_patterns = [
            # Templater patterns
            (r'<% tp\.[^%]*%>', ''),
            (r'<%[-\s]*[^%]*[-\s]*%>', ''),
            
            # Hugo/Jekyll patterns  
            (r'\{\{<[^>]*>\}\}', ''),
            (r'\{\{%[^%]*%\}\}', ''),
            
            # Handlebars patterns
            (r'\{\{\{[^}]*\}\}\}', ''),
            (r'\{\{#[^}]*\}\}', ''),
            (r'\{\{\/[^}]*\}\}', ''),
            
            # Generic placeholders
            (r'\[PLACEHOLDER[^\]]*\]', ''),
            (r'\{TODO[^}]*\}', ''),
            (r'<INSERT[^>]*>', ''),
            
            # Empty template sections
            (r'^#+\s*Template\s*$', ''),
            (r'^#+\s*TODO\s*$', ''),
            (r'^\s*-\s*TODO:.*$', ''),
        ]
        
        md_files = list(self.vault_path.rglob("*.md"))
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                changes_made = []
                
                for pattern, replacement in advanced_patterns:
                    matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                    if matches:
                        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.IGNORECASE)
                        changes_made.extend(matches)
                
                # Clean up extra whitespace left by removals
                content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
                content = re.sub(r'^\s*\n', '', content)
                
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    results.append({
                        "action": "advanced_placeholder_cleanup",
                        "file": str(file_path.relative_to(self.vault_path)),
                        "placeholders_removed": len(changes_made),
                        "patterns_found": list(set(changes_made))
                    })
                    
            except Exception as e:
                logger.warning(f"Could not clean {file_path}: {e}")
        
        logger.info(f"Advanced cleanup completed: {len(results)} files processed")
        return results

    def fix_malformed_frontmatter(self) -> List[Dict]:
        """Fix malformed YAML frontmatter"""
        results = []
        md_files = list(self.vault_path.rglob("*.md"))
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                if not lines:
                    continue
                    
                # Check for frontmatter
                if lines[0].strip() == '---':
                    end_idx = None
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            end_idx = i
                            break
                    
                    if end_idx:
                        frontmatter_lines = lines[1:end_idx]
                        body_lines = lines[end_idx+1:]
                        
                        # Fix common YAML issues
                        fixed_frontmatter = []
                        for line in frontmatter_lines:
                            # Fix unquoted strings with colons
                            if ':' in line and not line.strip().startswith('-'):
                                key, value = line.split(':', 1)
                                value = value.strip()
                                
                                # Quote values that need it
                                if value and not (
                                    value.startswith('"') or 
                                    value.startswith("'") or
                                    value.startswith('[') or
                                    value.startswith('{') or
                                    value.isdigit() or
                                    value.lower() in ['true', 'false', 'null']
                                ):
                                    if ':' in value or '#' in value:
                                        value = f'"{value}"'
                                
                                fixed_frontmatter.append(f"{key}: {value}")
                            else:
                                fixed_frontmatter.append(line)
                        
                        # Reconstruct file
                        new_content = '---\n' + '\n'.join(fixed_frontmatter) + '\n---\n' + '\n'.join(body_lines)
                        
                        if new_content != content:
                            file_path.write_text(new_content, encoding='utf-8')
                            results.append({
                                "action": "fixed_frontmatter",
                                "file": str(file_path.relative_to(self.vault_path))
                            })
                            
            except Exception as e:
                logger.warning(f"Could not fix frontmatter in {file_path}: {e}")
        
        logger.info(f"Fixed frontmatter in {len(results)} files")
        return results

    def optimize_dataview_performance(self) -> List[Dict]:
        """Optimize dataview queries for better performance"""
        results = []
        md_files = list(self.vault_path.rglob("*.md"))
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                # Find and optimize dataview queries
                dataview_blocks = re.findall(r'```dataview\n(.*?)\n```', content, re.DOTALL)
                
                for query in dataview_blocks:
                    optimized_query = self._optimize_single_query(query)
                    if optimized_query != query:
                        content = content.replace(query, optimized_query)
                
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    results.append({
                        "action": "optimized_dataview_queries",
                        "file": str(file_path.relative_to(self.vault_path)),
                        "queries_optimized": len(dataview_blocks)
                    })
                    
            except Exception as e:
                logger.warning(f"Could not optimize dataview in {file_path}: {e}")
        
        logger.info(f"Optimized dataview queries in {len(results)} files")
        return results

    def _optimize_single_query(self, query: str) -> str:
        """Optimize a single dataview query"""
        optimized = query
        
        # Add WHERE clauses for better filtering
        if 'FROM' in query and 'WHERE' not in query:
            # Add basic file existence check
            optimized = re.sub(r'(FROM\s+[^\n]+)', r'\1\nWHERE file.name != ""', optimized)
        
        # Optimize sorting
        if 'sort' in query.lower() and 'asc' not in query.lower() and 'desc' not in query.lower():
            optimized = re.sub(r'sort\s+([^\n]+)', r'sort \1 asc', optimized, flags=re.IGNORECASE)
        
        # Add LIMIT for large datasets
        if 'LIMIT' not in query.upper() and 'LIST' in query.upper():
            optimized += '\nLIMIT 50'
        
        # Replace inefficient patterns
        replacements = [
            (r'LIST\s*$', 'TABLE file.link as "File"'),
            (r'LIST\s+file\.name', 'TABLE file.link as "File"'),
            (r'file\.path', 'file.link'),  # Links are more useful than paths
        ]
        
        for pattern, replacement in replacements:
            optimized = re.sub(pattern, replacement, optimized, flags=re.MULTILINE | re.IGNORECASE)
        
        return optimized

    def standardize_dice_notation(self) -> List[Dict]:
        """Standardize dice roller notation throughout vault"""
        results = []
        md_files = list(self.vault_path.rglob("*.md"))
        
        dice_patterns = [
            # Basic dice rolls
            (r'(\d+)d(\d+)', r'`dice: \1d\2`'),
            (r'(\d+)d(\d+)\+(\d+)', r'`dice: \1d\2+\3`'),
            (r'(\d+)d(\d+)-(\d+)', r'`dice: \1d\2-\3`'),
            
            # Advantage/disadvantage
            (r'(\d+)d(\d+)\s+(?:with\s+)?advantage', r'`dice: \1d\2kh1` (advantage)'),
            (r'(\d+)d(\d+)\s+(?:with\s+)?disadvantage', r'`dice: \1d\2kl1` (disadvantage)'),
            
            # DC checks
            (r'DC\s+(\d+)', r'**DC \1**'),
        ]
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                for pattern, replacement in dice_patterns:
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    results.append({
                        "action": "standardized_dice_notation",
                        "file": str(file_path.relative_to(self.vault_path))
                    })
                    
            except Exception as e:
                logger.warning(f"Could not standardize dice in {file_path}: {e}")
        
        logger.info(f"Standardized dice notation in {len(results)} files")
        return results

    def create_performance_optimizations(self) -> List[Dict]:
        """Create performance optimization configurations"""
        results = []
        
        # Create performance tips file
        perf_tips = """# Vault Performance Optimization

## Dataview Optimization
- Use WHERE clauses to filter results
- Add LIMIT to large queries
- Prefer TABLE over LIST for better performance
- Use specific folder paths in FROM clauses

## Image Optimization
- Compress large images before embedding
- Use WebP format when possible
- Resize images to appropriate dimensions
- Consider using thumbnails for galleries

## Plugin Performance
- Disable unused plugins
- Use canvas sparingly for large graphs
- Limit real-time preview for large files
- Consider using cached views for complex queries

## File Organization
- Keep individual files under 1MB
- Limit deeply nested folder structures
- Use consistent naming conventions
- Archive old content regularly

## Indexing Optimization
```json
{
  "indexingSettings": {
    "excludePaths": [
      "08_Archive",
      "_BACKUPS",
      "09_Performance"
    ],
    "indexImages": false,
    "indexAudio": false
  }
}
```

## Memory Usage
- Close unnecessary tabs
- Restart Obsidian weekly
- Clear cache periodically
- Monitor plugin memory usage
"""
        
        perf_file = self.vault_path / "00_System" / "Performance_Optimization.md"
        perf_file.write_text(perf_tips, encoding='utf-8')
        results.append({
            "action": "created_performance_guide",
            "file": str(perf_file.relative_to(self.vault_path))
        })
        
        return results

    def validate_structure_integrity(self) -> List[Dict]:
        """Validate that the vault structure remains intact"""
        results = []
        
        expected_structure = [
            "00_System",
            "01_Adventures", 
            "02_Worldbuilding",
            "03_People",
            "04_Resources",
            "05_Rules",
            "06_Sessions",
            "07_Player_Resources",
            "08_Archive",
            "09_Performance"
        ]
        
        # Check main directories exist
        missing_dirs = []
        for dir_name in expected_structure:
            dir_path = self.vault_path / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            results.append({
                "action": "structure_validation_warning",
                "missing_directories": missing_dirs
            })
        
        # Check for campaign files in correct location
        campaign_dir = self.vault_path / "01_Adventures" / "Campaigns"
        if campaign_dir.exists():
            campaign_files = list(campaign_dir.glob("*.md"))
            results.append({
                "action": "validated_campaign_location",
                "campaign_files_found": len(campaign_files)
            })
        
        # Check for session files in correct location
        session_dir = self.vault_path / "06_Sessions"
        if session_dir.exists():
            session_files = list(session_dir.glob("*.md"))
            results.append({
                "action": "validated_session_location", 
                "session_files_found": len(session_files)
            })
        
        return results

    def run_phase1_specialized(self) -> Dict:
        """Run all specialized Phase 1 improvements"""
        logger.info("Starting Phase 1 Specialized Cleanup")
        
        all_results = []
        
        # Execute all improvements
        improvements = [
            ("Advanced Template Cleanup", self.advanced_template_cleanup),
            ("Fix Malformed Frontmatter", self.fix_malformed_frontmatter),
            ("Optimize Dataview Performance", self.optimize_dataview_performance),
            ("Standardize Dice Notation", self.standardize_dice_notation),
            ("Create Performance Optimizations", self.create_performance_optimizations),
            ("Validate Structure Integrity", self.validate_structure_integrity),
        ]
        
        for name, func in improvements:
            logger.info(f"Running: {name}")
            try:
                result = func()
                all_results.extend(result)
                logger.info(f"Completed: {name} - {len(result)} changes")
            except Exception as e:
                logger.error(f"Failed: {name} - {e}")
                all_results.append({
                    "action": "error",
                    "improvement": name,
                    "error": str(e)
                })
        
        # Create summary report
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_changes": len(all_results),
            "improvements_completed": len([r for r in all_results if r.get("action") != "error"]),
            "errors": len([r for r in all_results if r.get("action") == "error"]),
            "results": all_results
        }
        
        # Save report
        report_file = self.vault_path / "_SCRIPTS" / f"phase1_specialized_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with report_file.open('w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Phase 1 Specialized completed: {summary['total_changes']} total changes")
        return summary

def main():
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    cleaner = Phase1SpecializedCleaner(vault_path)
    result = cleaner.run_phase1_specialized()
    
    print(f"\nPhase 1 Specialized Cleanup Completed!")
    print(f"Total Changes: {result['total_changes']}")
    print(f"Improvements: {result['improvements_completed']}")
    print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    main()