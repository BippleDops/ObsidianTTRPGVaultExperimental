#!/usr/bin/env python3
"""
Map Optimization Script
Optimizes map images for better vault performance.
"""

import os
import shutil
from pathlib import Path
from PIL import Image
import hashlib
from typing import Dict, List, Tuple

class MapOptimizer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.maps_path = self.vault_path / '04_Resources' / 'Maps'
        self.thumbnails_path = self.maps_path / '_Thumbnails'
        self.archive_path = self.maps_path / '_Archive'
        self.featured_path = self.maps_path / '_Featured'
        
        self.stats = {
            'total_maps': 0,
            'optimized': 0,
            'duplicates': 0,
            'thumbnails_created': 0,
            'space_saved_mb': 0
        }
        
        # Size thresholds
        self.MAX_SIZE = (3840, 2160)  # 4K max
        self.THUMBNAIL_SIZE = (400, 400)
        self.MAX_FILE_SIZE_MB = 8
        
    def optimize(self, dry_run: bool = False):
        """Run map optimization"""
        print("=" * 50)
        print("MAP OPTIMIZATION")
        print("=" * 50)
        
        # Create directories
        self.thumbnails_path.mkdir(exist_ok=True)
        self.archive_path.mkdir(exist_ok=True)
        self.featured_path.mkdir(exist_ok=True)
        
        # Find all map images
        map_files = self.find_maps()
        print(f"\nFound {len(map_files)} map files")
        
        if dry_run:
            print("\n🔍 DRY RUN MODE - No changes will be made")
            self.analyze_maps(map_files)
            return
            
        # Process maps
        print("\n🗺️ Processing maps...")
        
        # Find and remove duplicates
        self.remove_duplicates(map_files)
        
        # Optimize large images
        for map_file in map_files:
            if map_file.exists():  # May have been removed as duplicate
                self.optimize_image(map_file)
                
        # Create thumbnails
        self.create_thumbnails(map_files)
        
        # Generate index
        self.generate_map_index()
        
        # Report
        self.print_report()
        
    def find_maps(self) -> List[Path]:
        """Find all map image files"""
        extensions = ['.png', '.jpg', '.jpeg', '.webp']
        map_files = []
        
        for ext in extensions:
            map_files.extend(self.maps_path.rglob(f'*{ext}'))
            
        # Exclude thumbnails and archives
        map_files = [f for f in map_files 
                    if '_Thumbnails' not in str(f) 
                    and '_Archive' not in str(f)]
        
        self.stats['total_maps'] = len(map_files)
        return map_files
        
    def get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
        
    def remove_duplicates(self, map_files: List[Path]):
        """Find and remove duplicate maps"""
        print("\n🔍 Checking for duplicates...")
        
        hash_map = {}
        duplicates = []
        
        for map_file in map_files:
            try:
                file_hash = self.get_file_hash(map_file)
                
                if file_hash in hash_map:
                    # Duplicate found
                    original = hash_map[file_hash]
                    
                    # Keep the one with better name or in better location
                    if self.is_better_name(map_file, original):
                        # New one is better, archive old
                        duplicates.append((original, map_file))
                        hash_map[file_hash] = map_file
                    else:
                        # Original is better, archive new
                        duplicates.append((map_file, original))
                else:
                    hash_map[file_hash] = map_file
                    
            except Exception as e:
                print(f"  Error hashing {map_file.name}: {e}")
                
        # Remove duplicates
        for duplicate, original in duplicates:
            print(f"  Duplicate: {duplicate.name} -> keeping {original.name}")
            
            # Archive the duplicate
            archive_dest = self.archive_path / 'duplicates' / duplicate.name
            archive_dest.parent.mkdir(exist_ok=True)
            
            try:
                shutil.move(str(duplicate), str(archive_dest))
                self.stats['duplicates'] += 1
            except:
                pass
                
    def is_better_name(self, file1: Path, file2: Path) -> bool:
        """Determine which filename is better"""
        name1 = file1.stem.lower()
        name2 = file2.stem.lower()
        
        # Prefer names without numbers at end
        if name1[-1].isdigit() and not name2[-1].isdigit():
            return False
        if not name1[-1].isdigit() and name2[-1].isdigit():
            return True
            
        # Prefer shorter names
        if len(name1) < len(name2):
            return True
            
        # Prefer featured directory
        if '_Featured' in str(file1) and '_Featured' not in str(file2):
            return True
            
        return False
        
    def optimize_image(self, image_path: Path):
        """Optimize a single image"""
        try:
            # Check file size
            size_mb = image_path.stat().st_size / (1024 * 1024)
            
            if size_mb <= self.MAX_FILE_SIZE_MB:
                return  # Already optimized
                
            print(f"  Optimizing {image_path.name} ({size_mb:.1f} MB)...")
            
            # Open and resize
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if needed
                if img.mode == 'RGBA':
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                    img = rgb_img
                    
                # Resize if too large
                if img.size[0] > self.MAX_SIZE[0] or img.size[1] > self.MAX_SIZE[1]:
                    img.thumbnail(self.MAX_SIZE, Image.Resampling.LANCZOS)
                    
                # Archive original
                archive_dest = self.archive_path / 'originals' / image_path.name
                archive_dest.parent.mkdir(exist_ok=True)
                shutil.copy2(image_path, archive_dest)
                
                # Save optimized
                img.save(image_path, 'JPEG', quality=85, optimize=True)
                
                new_size_mb = image_path.stat().st_size / (1024 * 1024)
                saved_mb = size_mb - new_size_mb
                
                self.stats['optimized'] += 1
                self.stats['space_saved_mb'] += saved_mb
                
                print(f"    Saved {saved_mb:.1f} MB")
                
        except Exception as e:
            print(f"  Error optimizing {image_path.name}: {e}")
            
    def create_thumbnails(self, map_files: List[Path]):
        """Create thumbnails for all maps"""
        print("\n📸 Creating thumbnails...")
        
        for map_file in map_files:
            if not map_file.exists():
                continue
                
            thumbnail_path = self.thumbnails_path / f"{map_file.stem}_thumb.jpg"
            
            if thumbnail_path.exists():
                continue  # Thumbnail already exists
                
            try:
                with Image.open(map_file) as img:
                    # Create thumbnail
                    img.thumbnail(self.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                    
                    # Convert to RGB if needed
                    if img.mode == 'RGBA':
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        rgb_img.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                        img = rgb_img
                        
                    # Save thumbnail
                    img.save(thumbnail_path, 'JPEG', quality=75)
                    self.stats['thumbnails_created'] += 1
                    
            except Exception as e:
                print(f"  Error creating thumbnail for {map_file.name}: {e}")
                
    def analyze_maps(self, map_files: List[Path]):
        """Analyze maps without making changes"""
        total_size_mb = 0
        large_files = []
        potential_duplicates = {}
        
        for map_file in map_files:
            size_mb = map_file.stat().st_size / (1024 * 1024)
            total_size_mb += size_mb
            
            if size_mb > self.MAX_FILE_SIZE_MB:
                large_files.append((map_file, size_mb))
                
            # Check for potential duplicates by size
            size_key = map_file.stat().st_size
            if size_key in potential_duplicates:
                potential_duplicates[size_key].append(map_file)
            else:
                potential_duplicates[size_key] = [map_file]
                
        print(f"\n📊 Analysis Results:")
        print(f"  Total maps: {len(map_files)}")
        print(f"  Total size: {total_size_mb:.1f} MB")
        print(f"  Average size: {total_size_mb/len(map_files):.1f} MB")
        print(f"  Large files (>{self.MAX_FILE_SIZE_MB} MB): {len(large_files)}")
        
        # Count potential duplicates
        duplicate_count = sum(len(files) - 1 for files in potential_duplicates.values() if len(files) > 1)
        print(f"  Potential duplicates: {duplicate_count}")
        
        if large_files:
            print(f"\n  Largest files:")
            for f, size in sorted(large_files, key=lambda x: x[1], reverse=True)[:5]:
                print(f"    {f.name}: {size:.1f} MB")
                
    def generate_map_index(self):
        """Generate a map index file"""
        index_path = self.maps_path / 'MAP_INDEX.md'
        
        content = """---
id: MAP_INDEX
type: index
domain: resource
---

# Map Index

## 🌟 Featured Maps
"""
        
        # Add featured maps
        featured = list(self.featured_path.glob('*'))
        for map_file in featured[:20]:
            if map_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                content += f"- [[{map_file.stem}|{map_file.stem.replace('_', ' ').title()}]]\n"
                
        content += """

## 🗺️ All Maps by Category

### Battle Maps
```dataview
TABLE WITHOUT ID
  file.link AS "Map",
  file.size AS "Size"
FROM "04_Resources/Maps"
WHERE contains(file.name, "battle") OR contains(file.name, "combat")
SORT file.name ASC
```

### City Maps
```dataview
TABLE WITHOUT ID
  file.link AS "Map",
  file.size AS "Size"
FROM "04_Resources/Maps"
WHERE contains(file.name, "city") OR contains(file.name, "town") OR contains(file.name, "village")
SORT file.name ASC
```

### Dungeon Maps
```dataview
TABLE WITHOUT ID
  file.link AS "Map",
  file.size AS "Size"
FROM "04_Resources/Maps"
WHERE contains(file.name, "dungeon") OR contains(file.name, "cave") OR contains(file.name, "cavern")
SORT file.name ASC
```

### World Maps
```dataview
TABLE WITHOUT ID
  file.link AS "Map",
  file.size AS "Size"
FROM "04_Resources/Maps"
WHERE contains(file.name, "world") OR contains(file.name, "region") OR contains(file.name, "continent")
SORT file.name ASC
```

## 📸 Thumbnails
Thumbnails available in: `04_Resources/Maps/_Thumbnails/`

---
*Generated by map optimization script*
"""
        
        with open(index_path, 'w') as f:
            f.write(content)
            
    def print_report(self):
        """Print optimization report"""
        print("\n" + "=" * 50)
        print("MAP OPTIMIZATION COMPLETE")
        print("=" * 50)
        print(f"Maps processed: {self.stats['total_maps']}")
        print(f"Maps optimized: {self.stats['optimized']}")
        print(f"Duplicates removed: {self.stats['duplicates']}")
        print(f"Thumbnails created: {self.stats['thumbnails_created']}")
        print(f"Space saved: {self.stats['space_saved_mb']:.1f} MB")
        
        if self.stats['optimized'] > 0:
            print(f"\n✓ Originals backed up to: {self.archive_path / 'originals'}")
        if self.stats['duplicates'] > 0:
            print(f"✓ Duplicates moved to: {self.archive_path / 'duplicates'}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Optimize map images in vault')
    parser.add_argument('--vault',
                       default="/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVaultExperimental",
                       help='Path to vault')
    parser.add_argument('--dry-run', action='store_true',
                       help='Analyze without making changes')
    
    args = parser.parse_args()
    
    # Check for PIL
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow library required. Install with: pip3 install Pillow")
        return
        
    optimizer = MapOptimizer(args.vault)
    optimizer.optimize(dry_run=args.dry_run)

if __name__ == "__main__":
    main()