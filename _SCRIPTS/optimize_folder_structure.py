#!/usr/bin/env python3
"""
Step 27: Optimize folder structure with flat-first architecture where appropriate
"""

import os
import shutil
from pathlib import Path
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def get_vault_root():
    """Get the vault root directory"""
    script_dir = Path(__file__).parent
    return script_dir.parent

def analyze_deeply_nested_content(vault_root):
    """Find content that's too deeply nested and could benefit from flattening"""
    logger = logging.getLogger(__name__)
    flatten_candidates = []
    
    # Look for directories more than 3 levels deep with only a few files
    for root, dirs, files in os.walk(vault_root):
        level = root.count(os.sep) - str(vault_root).count(os.sep)
        if level > 3:  # More than 3 levels deep
            md_files = [f for f in files if f.endswith('.md')]
            if len(md_files) <= 3 and len(dirs) == 0:  # Few files, no subdirs
                flatten_candidates.append({
                    'path': root,
                    'level': level,
                    'files': md_files,
                    'parent': os.path.dirname(root)
                })
    
    return flatten_candidates

def flatten_appropriate_directories(vault_root, flatten_candidates):
    """Move files from deeply nested directories to more appropriate locations"""
    logger = logging.getLogger(__name__)
    moved_files = []
    
    for candidate in flatten_candidates:
        # Skip system and backup directories
        if any(skip in candidate['path'] for skip in ['.git', '.obsidian', 'backups', 'scripts', '__pycache__']):
            continue
            
        source_dir = Path(candidate['path'])
        parent_dir = Path(candidate['parent'])
        
        # Move markdown files to parent directory with descriptive prefixes
        for md_file in candidate['files']:
            source_file = source_dir / md_file
            # Create descriptive name based on directory structure
            dir_name = source_dir.name
            new_name = f"{dir_name} - {md_file}"
            target_file = parent_dir / new_name
            
            try:
                if source_file.exists() and not target_file.exists():
                    shutil.move(str(source_file), str(target_file))
                    moved_files.append({
                        'from': str(source_file),
                        'to': str(target_file)
                    })
                    logger.info(f"Moved: {source_file} -> {target_file}")
            except Exception as e:
                logger.error(f"Error moving {source_file}: {e}")
        
        # Remove empty directory
        try:
            if source_dir.exists() and not any(source_dir.iterdir()):
                source_dir.rmdir()
                logger.info(f"Removed empty directory: {source_dir}")
        except Exception as e:
            logger.error(f"Error removing directory {source_dir}: {e}")
    
    return moved_files

def consolidate_single_file_directories(vault_root):
    """Consolidate directories that contain only one markdown file"""
    logger = logging.getLogger(__name__)
    consolidated = []
    
    for root, dirs, files in os.walk(vault_root):
        # Skip system directories
        if any(skip in root for skip in ['.git', '.obsidian', 'backups', 'scripts', '__pycache__']):
            continue
            
        md_files = [f for f in files if f.endswith('.md')]
        if len(md_files) == 1 and len(dirs) == 0:  # Single file, no subdirs
            source_dir = Path(root)
            parent_dir = source_dir.parent
            md_file = md_files[0]
            
            # Don't consolidate if already in a main category directory
            level = root.count(os.sep) - str(vault_root).count(os.sep)
            if level <= 2:
                continue
            
            source_file = source_dir / md_file
            # Use directory name as prefix if it's descriptive
            dir_name = source_dir.name
            if dir_name.lower() != md_file.lower().replace('.md', ''):
                new_name = f"{dir_name} - {md_file}"
            else:
                new_name = md_file
            
            target_file = parent_dir / new_name
            
            try:
                if source_file.exists() and not target_file.exists():
                    shutil.move(str(source_file), str(target_file))
                    consolidated.append({
                        'from': str(source_file),
                        'to': str(target_file)
                    })
                    logger.info(f"Consolidated: {source_file} -> {target_file}")
                    
                    # Remove empty directory
                    if source_dir.exists() and not any(source_dir.iterdir()):
                        source_dir.rmdir()
                        logger.info(f"Removed empty directory: {source_dir}")
                        
            except Exception as e:
                logger.error(f"Error consolidating {source_file}: {e}")
    
    return consolidated

def optimize_content_type_groupings(vault_root):
    """Optimize groupings within content type directories"""
    logger = logging.getLogger(__name__)
    optimizations = []
    
    # Define content type directories that benefit from flat structure
    flat_directories = [
        '02_Worldbuilding/Items',
        '02_Worldbuilding/People', 
        '03_Mechanics',
        '05_Templates'
    ]
    
    for flat_dir in flat_directories:
        full_path = vault_root / flat_dir
        if not full_path.exists():
            continue
            
        # Move files from subdirectories to main directory
        for subdir in full_path.iterdir():
            if subdir.is_dir() and subdir.name not in ['.git', '.obsidian']:
                for file_path in subdir.rglob('*.md'):
                    # Create descriptive name
                    relative_path = file_path.relative_to(subdir)
                    if len(relative_path.parts) > 1:
                        # File is in nested structure
                        new_name = f"{subdir.name} - {' - '.join(relative_path.parts[:-1])} - {relative_path.name}"
                    else:
                        new_name = f"{subdir.name} - {relative_path.name}"
                    
                    target_file = full_path / new_name
                    
                    try:
                        if not target_file.exists():
                            shutil.move(str(file_path), str(target_file))
                            optimizations.append({
                                'from': str(file_path),
                                'to': str(target_file)
                            })
                            logger.info(f"Flattened: {file_path} -> {target_file}")
                    except Exception as e:
                        logger.error(f"Error flattening {file_path}: {e}")
                
                # Remove empty subdirectories
                for empty_dir in subdir.rglob('*'):
                    if empty_dir.is_dir() and not any(empty_dir.iterdir()):
                        try:
                            empty_dir.rmdir()
                            logger.info(f"Removed empty directory: {empty_dir}")
                        except Exception as e:
                            logger.error(f"Error removing directory {empty_dir}: {e}")
    
    return optimizations

def main():
    logger = setup_logging()
    vault_root = get_vault_root()
    
    logger.info("Starting folder structure optimization...")
    
    # Step 1: Analyze deeply nested content
    flatten_candidates = analyze_deeply_nested_content(vault_root)
    logger.info(f"Found {len(flatten_candidates)} deeply nested directories")
    
    # Step 2: Flatten appropriate directories
    moved_files = flatten_appropriate_directories(vault_root, flatten_candidates)
    logger.info(f"Moved {len(moved_files)} files from deeply nested directories")
    
    # Step 3: Consolidate single-file directories
    consolidated = consolidate_single_file_directories(vault_root)
    logger.info(f"Consolidated {len(consolidated)} single-file directories")
    
    # Step 4: Optimize content type groupings
    optimizations = optimize_content_type_groupings(vault_root)
    logger.info(f"Applied {len(optimizations)} content type optimizations")
    
    # Generate report
    total_changes = len(moved_files) + len(consolidated) + len(optimizations)
    logger.info(f"Folder structure optimization complete. Total changes: {total_changes}")
    
    # Write detailed report
    report_path = vault_root / "reports" / "folder_structure_optimization.md"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write("# Folder Structure Optimization Report\n\n")
        f.write(f"Total changes made: {total_changes}\n\n")
        
        f.write("## Deeply Nested Files Moved\n\n")
        for item in moved_files:
            f.write(f"- `{item['from']}` → `{item['to']}`\n")
        
        f.write("\n## Single-File Directories Consolidated\n\n")
        for item in consolidated:
            f.write(f"- `{item['from']}` → `{item['to']}`\n")
        
        f.write("\n## Content Type Optimizations\n\n")
        for item in optimizations:
            f.write(f"- `{item['from']}` → `{item['to']}`\n")
    
    logger.info(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()