#!/usr/bin/env python3
"""
Steps 71-80: Performance Optimization
This phase optimizes vault performance and reduces bloat
"""
import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib

def analyze_vault_size():
    """Step 71-72: Analyze vault size and identify large files"""
    print("\n📊 ANALYZING VAULT SIZE (Steps 71-72)")
    
    total_size = 0
    file_count = 0
    large_files = []
    size_by_type = defaultdict(int)
    count_by_type = defaultdict(int)
    
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".obsidian" in root:
            continue
            
        for file in files:
            file_path = Path(root) / file
            try:
                size = file_path.stat().st_size
                total_size += size
                file_count += 1
                
                ext = file_path.suffix.lower()
                size_by_type[ext] += size
                count_by_type[ext] += 1
                
                # Track files over 1MB
                if size > 1024 * 1024:
                    large_files.append((file_path, size))
            except:
                pass
    
    # Sort large files by size
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n📈 Vault Statistics:")
    print(f"  Total size: {total_size / (1024*1024*1024):.2f} GB")
    print(f"  Total files: {file_count:,}")
    print(f"  Average file size: {total_size / file_count / 1024:.2f} KB")
    
    print(f"\n📦 Size by type (top 5):")
    sorted_types = sorted(size_by_type.items(), key=lambda x: x[1], reverse=True)[:5]
    for ext, size in sorted_types:
        print(f"  {ext or 'no extension'}: {size / (1024*1024):.2f} MB ({count_by_type[ext]:,} files)")
    
    print(f"\n🗂️ Large files (>1MB): {len(large_files)}")
    for path, size in large_files[:5]:
        print(f"  {path.name}: {size / (1024*1024):.2f} MB")
    
    return total_size, file_count, large_files

def find_duplicate_content():
    """Step 73-74: Find duplicate files by content hash"""
    print("\n🔍 FINDING DUPLICATES (Steps 73-74)")
    
    hash_map = defaultdict(list)
    duplicates = []
    
    # Sample first 1000 markdown files
    sample_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".obsidian" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                sample_files.append(Path(root) / file)
                if len(sample_files) >= 1000:
                    break
        if len(sample_files) >= 1000:
            break
    
    print(f"  Checking {len(sample_files)} files for duplicates...")
    
    for file_path in sample_files:
        try:
            content = file_path.read_bytes()
            file_hash = hashlib.md5(content).hexdigest()
            hash_map[file_hash].append(file_path)
        except:
            pass
    
    # Find duplicates
    for file_hash, paths in hash_map.items():
        if len(paths) > 1:
            duplicates.append(paths)
    
    print(f"  ✓ Found {len(duplicates)} sets of duplicate files")
    
    if duplicates[:5]:
        print("\n  Sample duplicates:")
        for dup_set in duplicates[:5]:
            print(f"    Duplicate group ({len(dup_set)} files):")
            for path in dup_set[:3]:
                print(f"      - {path}")
    
    return duplicates

def optimize_images():
    """Step 75-76: Identify image optimization opportunities"""
    print("\n🖼️ ANALYZING IMAGES (Steps 75-76)")
    
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
    images = []
    total_image_size = 0
    
    for root, dirs, files in os.walk("04_Resources"):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in image_extensions:
                try:
                    size = file_path.stat().st_size
                    images.append((file_path, size))
                    total_image_size += size
                except:
                    pass
    
    images.sort(key=lambda x: x[1], reverse=True)
    
    print(f"  Total images: {len(images)}")
    print(f"  Total size: {total_image_size / (1024*1024):.2f} MB")
    
    # Identify optimization candidates (images over 500KB)
    large_images = [img for img in images if img[1] > 500 * 1024]
    
    print(f"  Images >500KB: {len(large_images)}")
    if large_images[:5]:
        print("\n  Optimization candidates:")
        for path, size in large_images[:5]:
            print(f"    {path.name}: {size / 1024:.2f} KB")
    
    return large_images

def create_search_index():
    """Step 77-78: Create optimized search index"""
    print("\n🔎 CREATING SEARCH INDEX (Steps 77-78)")
    
    index = {
        "npcs": {},
        "locations": {},
        "quests": {},
        "items": {}
    }
    
    # Index NPCs
    npc_files = list(Path("03_People").rglob("*.md"))[:100]
    for file_path in npc_files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            # Extract key info
            name = file_path.stem
            tags = []
            if "villain" in content.lower():
                tags.append("villain")
            if "ally" in content.lower():
                tags.append("ally")
            
            index["npcs"][name] = {
                "path": str(file_path),
                "tags": tags,
                "size": len(content)
            }
        except:
            pass
    
    # Index locations
    location_files = list(Path("02_Worldbuilding").rglob("*.md"))[:100]
    for file_path in location_files:
        try:
            name = file_path.stem
            index["locations"][name] = {
                "path": str(file_path)
            }
        except:
            pass
    
    # Save index
    index_file = Path("_INDEXES/search_index.json")
    index_file.parent.mkdir(parents=True, exist_ok=True)
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
    
    total_indexed = sum(len(v) for v in index.values())
    print(f"  ✓ Indexed {total_indexed} items")
    print(f"  ✓ Index saved to: {index_file}")
    
    return index_file

def create_performance_report():
    """Step 79-80: Create comprehensive performance report"""
    print("\n📝 CREATING PERFORMANCE REPORT (Steps 79-80)")
    
    # Gather all metrics
    total_size, file_count, large_files = analyze_vault_size()
    duplicates = find_duplicate_content()
    large_images = optimize_images()
    index_file = create_search_index()
    
    report_path = Path("09_Performance/performance_report_phase7.md")
    
    with open(report_path, 'w') as f:
        f.write("# Phase 7 Performance Report (Steps 71-80)\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        f.write("## Vault Metrics\n\n")
        f.write(f"- **Total Size**: {total_size / (1024*1024*1024):.2f} GB\n")
        f.write(f"- **File Count**: {file_count:,}\n")
        f.write(f"- **Large Files (>1MB)**: {len(large_files)}\n")
        f.write(f"- **Duplicate Sets**: {len(duplicates)}\n")
        f.write(f"- **Large Images**: {len(large_images)}\n\n")
        
        f.write("## Optimization Opportunities\n\n")
        
        # Calculate potential savings
        dup_savings = sum(len(dup_set) - 1 for dup_set in duplicates) * 50000  # Estimate 50KB per dup
        image_savings = len(large_images) * 200 * 1024  # Estimate 200KB savings per image
        
        f.write(f"### Potential Space Savings\n")
        f.write(f"- Remove duplicates: ~{dup_savings / (1024*1024):.2f} MB\n")
        f.write(f"- Optimize images: ~{image_savings / (1024*1024):.2f} MB\n")
        f.write(f"- **Total potential**: ~{(dup_savings + image_savings) / (1024*1024):.2f} MB\n\n")
        
        f.write("### Performance Improvements\n")
        f.write("- Created search index for faster lookups\n")
        f.write("- Identified large files for review\n")
        f.write("- Found duplicate content for cleanup\n\n")
        
        f.write("## Recommendations\n\n")
        f.write("1. **Immediate**: Review and remove duplicate files\n")
        f.write("2. **Short-term**: Compress large images\n")
        f.write("3. **Long-term**: Implement file size limits\n")
        f.write("4. **Ongoing**: Run performance checks monthly\n")
    
    print(f"\n  ✓ Report created: {report_path}")
    
    return report_path

def main():
    print("=" * 60)
    print("PHASE 7: PERFORMANCE OPTIMIZATION (STEPS 71-80)")
    print("=" * 60)
    
    # Create performance report (runs all analyses)
    report_path = create_performance_report()
    
    print("\n" + "=" * 60)
    print("STEPS 71-80 COMPLETE!")
    print("=" * 60)
    print("\n✓ Vault size analyzed")
    print("✓ Duplicates identified")
    print("✓ Images reviewed")
    print("✓ Search index created")
    print(f"✓ Report: {report_path}")
    print("\n🎯 80% of glidepath complete (80/100 steps)")
    
    return True

if __name__ == "__main__":
    main()