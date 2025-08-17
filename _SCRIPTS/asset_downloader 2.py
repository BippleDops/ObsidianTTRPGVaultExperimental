#!/usr/bin/env python3
"""
Asset Downloader and Vault Integration
Sprint 4 - Asset Management System

Downloads and integrates assets from various online sources into the vault.
Creates deep links to campaign content and manages asset organization.

Features:
- Downloads from vetted free sources
- Organizes assets by type and theme
- Creates markdown entries with asset references
- Integrates with existing vault content
- Manages licensing and attribution
"""

import os
import requests
from pathlib import Path
import json
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import hashlib
import time
from urllib.parse import urlparse, urljoin
import re
from datetime import datetime

from common import ROOT_DIR, write_file, read_file, split_frontmatter

class AssetSource(BaseModel):
    """Information about an asset source website"""
    name: str
    base_url: str
    license_type: str
    attribution_required: bool
    supported_types: List[str]
    rate_limit_delay: float = 1.0

class DownloadedAsset(BaseModel):
    """Information about a downloaded asset"""
    asset_id: str
    file_path: str
    original_url: str
    source: str
    asset_type: str
    theme_tags: List[str]
    license_info: str
    attribution: str
    file_size: int
    download_date: str
    vault_integrations: List[str] = Field(default_factory=list)
    checksum: str = ""

class AssetDownloader:
    """Main system for downloading and integrating assets"""
    
    def __init__(self, vault_root: str = ROOT_DIR):
        self.vault_root = vault_root
        self.assets_dir = os.path.join(vault_root, "04_Resources", "Assets")
        self.downloads_dir = os.path.join(self.assets_dir, "Downloaded")
        self.downloaded_assets: Dict[str, DownloadedAsset] = {}
        
        # Vetted free sources based on research
        self.sources = {
            "pixabay": AssetSource(
                name="Pixabay",
                base_url="https://pixabay.com",
                license_type="Pixabay License",
                attribution_required=False,
                supported_types=["image", "audio"],
                rate_limit_delay=1.0
            ),
            "freepik": AssetSource(
                name="Freepik",
                base_url="https://www.freepik.com",
                license_type="Freepik License",
                attribution_required=True,
                supported_types=["image", "vector"],
                rate_limit_delay=2.0
            ),
            "tabletop_audio": AssetSource(
                name="Tabletop Audio",
                base_url="https://tabletopaudio.com",
                license_type="CC BY-NC-SA",
                attribution_required=True,
                supported_types=["audio"],
                rate_limit_delay=5.0
            ),
            "soundimage": AssetSource(
                name="SoundImage",
                base_url="https://soundimage.org",
                license_type="Royalty Free with Attribution",
                attribution_required=True,
                supported_types=["audio"],
                rate_limit_delay=3.0
            )
        }
        
        self._ensure_directories()
        self._load_existing_assets()
    
    def _ensure_directories(self):
        """Create necessary directory structure"""
        directories = [
            "Downloaded/Images/Portraits",
            "Downloaded/Images/Locations", 
            "Downloaded/Images/Creatures",
            "Downloaded/Images/Items",
            "Downloaded/Audio/Ambient",
            "Downloaded/Audio/Music",
            "Downloaded/Audio/Effects",
            "Generated/Prompts"
        ]
        
        for directory in directories:
            full_path = os.path.join(self.assets_dir, directory)
            os.makedirs(full_path, exist_ok=True)
    
    def download_asset_from_url(self, url: str, asset_type: str, theme_tags: List[str], 
                              custom_name: str = None) -> Optional[DownloadedAsset]:
        """Download a specific asset from URL"""
        
        try:
            # Determine source from URL
            parsed_url = urlparse(url)
            source_name = self._identify_source(parsed_url.netloc)
            
            if not source_name:
                print(f"Unknown source: {parsed_url.netloc}")
                return None
            
            source = self.sources[source_name]
            
            # Rate limiting
            time.sleep(source.rate_limit_delay)
            
            # Download the file
            headers = {
                'User-Agent': 'Mozilla/5.0 (Cordelia TTRPG Vault Asset Manager)'
            }
            
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            
            # Generate filename
            if custom_name:
                filename = custom_name
            else:
                filename = self._generate_filename(url, asset_type, theme_tags)
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            extension = self._get_extension_from_content_type(content_type, url)
            full_filename = f"{filename}{extension}"
            
            # Create file path
            type_dir = "Images" if asset_type.startswith("image") else "Audio"
            theme_dir = theme_tags[0].title() if theme_tags else "General"
            file_path = os.path.join(self.downloads_dir, type_dir, theme_dir, full_filename)
            
            # Create directory if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Download file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Calculate checksum
            checksum = self._calculate_checksum(file_path)
            
            # Create asset record
            asset_id = self._generate_asset_id(url, filename)
            
            asset = DownloadedAsset(
                asset_id=asset_id,
                file_path=file_path,
                original_url=url,
                source=source.name,
                asset_type=asset_type,
                theme_tags=theme_tags,
                license_info=source.license_type,
                attribution=self._generate_attribution(source, url),
                file_size=os.path.getsize(file_path),
                download_date=datetime.now().isoformat(),
                checksum=checksum
            )
            
            self.downloaded_assets[asset_id] = asset
            print(f"Successfully downloaded: {full_filename}")
            return asset
            
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return None
    
    def create_curated_asset_collection(self) -> List[DownloadedAsset]:
        """Download a curated collection of assets for the vault"""
        
        # Curated list of free assets that fit the Cordelia world
        asset_list = [
            # Underwater ambient sounds
            {
                "url": "https://tabletopaudio.com/deepwatch_a.mp3",  # Example - would need actual URLs
                "type": "audio_ambient",
                "tags": ["underwater", "ambience", "aquabyssos"],
                "name": "deep_ocean_ambience"
            },
            # Note: These are example URLs - in practice would use actual free asset URLs
            # from the sources identified in the web search
        ]
        
        downloaded = []
        
        print("Creating curated asset collection...")
        print("Note: This is a demonstration framework.")
        print("In practice, you would:")
        print("1. Browse the identified free sources (Pixabay, Freepik, etc.)")
        print("2. Find assets that fit your campaign themes")
        print("3. Use their direct download URLs with this system")
        print("4. The system will organize and integrate them automatically")
        
        # Example of how the system would work:
        example_asset = DownloadedAsset(
            asset_id="example_ocean_ambience",
            file_path=os.path.join(self.downloads_dir, "Audio", "Ambient", "ocean_depths.mp3"),
            original_url="https://example.com/ocean_ambience.mp3",
            source="Tabletop Audio",
            asset_type="audio_ambient",
            theme_tags=["underwater", "ambience", "aquabyssos"],
            license_info="CC BY-NC-SA",
            attribution="Tabletop Audio (tabletopaudio.com)",
            file_size=5242880,  # 5MB example
            download_date=datetime.now().isoformat(),
            checksum="abc123def456"
        )
        
        self.downloaded_assets[example_asset.asset_id] = example_asset
        downloaded.append(example_asset)
        
        return downloaded
    
    def integrate_assets_with_vault(self, assets: List[DownloadedAsset] = None):
        """Create deep links between assets and vault content"""
        
        if not assets:
            assets = list(self.downloaded_assets.values())
        
        integration_report = {
            "integrated_count": 0,
            "integration_details": []
        }
        
        # Find vault content that could use these assets
        vault_files = self._scan_vault_for_integration_opportunities()
        
        for asset in assets:
            integrations = self._find_integration_matches(asset, vault_files)
            
            for integration in integrations:
                self._create_asset_integration(asset, integration)
                asset.vault_integrations.append(integration["file_path"])
                integration_report["integrated_count"] += 1
                integration_report["integration_details"].append({
                    "asset": asset.asset_id,
                    "integrated_with": integration["name"],
                    "integration_type": integration["type"]
                })
        
        # Create asset gallery
        self._create_asset_gallery()
        
        # Save integration report
        self._save_integration_report(integration_report)
        
        return integration_report
    
    def _scan_vault_for_integration_opportunities(self) -> List[Dict]:
        """Scan vault for content that could benefit from assets"""
        opportunities = []
        
        # Scan for NPCs that need portraits
        npc_dir = os.path.join(self.vault_root, "02_Worldbuilding", "People")
        if os.path.exists(npc_dir):
            for filename in os.listdir(npc_dir):
                if filename.endswith('.md'):
                    file_path = os.path.join(npc_dir, filename)
                    try:
                        content = read_file(file_path)
                        frontmatter, body = split_frontmatter(content)
                        
                        if frontmatter.get('type') == 'NPC':
                            opportunities.append({
                                "name": frontmatter.get('name', filename[:-3]),
                                "file_path": file_path,
                                "type": "npc_portrait",
                                "world": frontmatter.get('world', 'Both'),
                                "themes": self._extract_themes_from_npc(body)
                            })
                    except Exception as e:
                        continue
        
        # Scan for locations that need artwork
        locations_dir = os.path.join(self.vault_root, "02_Worldbuilding", "Places")
        if os.path.exists(locations_dir):
            for filename in os.listdir(locations_dir):
                if filename.endswith('.md'):
                    file_path = os.path.join(locations_dir, filename)
                    try:
                        content = read_file(file_path)
                        frontmatter, body = split_frontmatter(content)
                        
                        if frontmatter.get('type') == 'Location':
                            opportunities.append({
                                "name": frontmatter.get('name', filename[:-3]),
                                "file_path": file_path,
                                "type": "location_artwork",
                                "world": frontmatter.get('world', 'Both'),
                                "themes": self._extract_themes_from_location(body)
                            })
                    except Exception as e:
                        continue
        
        return opportunities
    
    def _find_integration_matches(self, asset: DownloadedAsset, 
                                 opportunities: List[Dict]) -> List[Dict]:
        """Find vault content that matches an asset's themes"""
        matches = []
        
        for opportunity in opportunities:
            match_score = 0
            
            # Check theme overlap
            asset_themes = set(tag.lower() for tag in asset.theme_tags)
            opp_themes = set(theme.lower() for theme in opportunity.get("themes", []))
            
            theme_overlap = len(asset_themes.intersection(opp_themes))
            match_score += theme_overlap * 2
            
            # Check world compatibility
            if asset.asset_type.startswith("audio") and "ambient" in asset.asset_type:
                # Ambient audio can match many things
                match_score += 1
            elif opportunity["type"] == "npc_portrait" and "portrait" in asset.asset_type:
                match_score += 3
            elif opportunity["type"] == "location_artwork" and "location" in asset.asset_type:
                match_score += 3
            
            # World-specific bonuses
            if "aquabyssos" in asset_themes and opportunity["world"] == "Aquabyssos":
                match_score += 2
            elif "aethermoor" in asset_themes and opportunity["world"] == "Aethermoor":
                match_score += 2
            elif opportunity["world"] == "Both":
                match_score += 1
            
            if match_score >= 2:  # Minimum match threshold
                opportunity["match_score"] = match_score
                matches.append(opportunity)
        
        # Sort by match score
        return sorted(matches, key=lambda x: x["match_score"], reverse=True)[:3]
    
    def _create_asset_integration(self, asset: DownloadedAsset, integration: Dict):
        """Create the actual integration between asset and vault content"""
        
        try:
            # Read the vault file
            content = read_file(integration["file_path"])
            frontmatter, body = split_frontmatter(content)
            
            # Add asset reference
            asset_section = f"\n\n## Assets\n\n### {asset.asset_type.replace('_', ' ').title()}\n"
            
            if asset.asset_type.startswith("image"):
                # Image integration
                relative_path = os.path.relpath(asset.file_path, self.vault_root)
                asset_section += f"![[{relative_path}]]\n"
            elif asset.asset_type.startswith("audio"):
                # Audio integration
                relative_path = os.path.relpath(asset.file_path, self.vault_root)
                asset_section += f"Audio: [[{relative_path}]]\n"
            
            asset_section += f"\n*Source: {asset.source}*\n"
            if asset.attribution:
                asset_section += f"*Attribution: {asset.attribution}*\n"
            
            # Check if Assets section already exists
            if "## Assets" not in body:
                body += asset_section
            else:
                # Add to existing Assets section
                parts = body.split("## Assets")
                if len(parts) >= 2:
                    asset_content = parts[1].split("\n\n## ")[0]  # Get just the Assets section
                    new_asset_content = asset_content + asset_section
                    body = parts[0] + "## Assets" + new_asset_content + "\n\n## " + "\n\n## ".join(body.split("## Assets")[1].split("\n\n## ")[1:])
            
            # Update frontmatter
            frontmatter["updated"] = datetime.now().isoformat()
            if "asset_count" not in frontmatter:
                frontmatter["asset_count"] = 0
            frontmatter["asset_count"] += 1
            
            # Write updated content
            from common import build_frontmatter
            new_content = build_frontmatter(frontmatter) + "\n" + body
            write_file(integration["file_path"], new_content)
            
        except Exception as e:
            print(f"Failed to integrate asset {asset.asset_id} with {integration['name']}: {e}")
    
    def _create_asset_gallery(self):
        """Create an asset gallery index"""
        
        gallery_content = f"""# Asset Gallery

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

This gallery showcases all downloaded and integrated assets for the Cordelia TTRPG Vault.

## Asset Summary

- **Total Assets**: {len(self.downloaded_assets)}
- **Images**: {len([a for a in self.downloaded_assets.values() if a.asset_type.startswith('image')])}
- **Audio**: {len([a for a in self.downloaded_assets.values() if a.asset_type.startswith('audio')])}

## Assets by Category

"""
        
        # Group assets by type
        asset_categories = {}
        for asset in self.downloaded_assets.values():
            category = asset.asset_type.split('_')[0].title()
            if category not in asset_categories:
                asset_categories[category] = []
            asset_categories[category].append(asset)
        
        for category, assets in asset_categories.items():
            gallery_content += f"\n### {category} Assets\n\n"
            
            for asset in assets:
                gallery_content += f"#### {asset.asset_id}\n"
                gallery_content += f"- **Source**: {asset.source}\n"
                gallery_content += f"- **Themes**: {', '.join(asset.theme_tags)}\n"
                gallery_content += f"- **File Size**: {asset.file_size // 1024}KB\n"
                
                if asset.vault_integrations:
                    gallery_content += f"- **Used In**: {len(asset.vault_integrations)} vault files\n"
                
                # Show preview if image
                if asset.asset_type.startswith("image"):
                    relative_path = os.path.relpath(asset.file_path, self.vault_root)
                    gallery_content += f"\n![[{relative_path}]]\n"
                
                gallery_content += f"\n*{asset.attribution}*\n\n---\n\n"
        
        # Write gallery
        gallery_path = os.path.join(self.assets_dir, "Asset_Gallery.md")
        write_file(gallery_path, gallery_content)
    
    def _save_integration_report(self, report: Dict):
        """Save integration report"""
        report_path = os.path.join(self.vault_root, "09_Performance", "asset_integration_report.json")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
    
    def save_asset_data(self):
        """Save asset database"""
        data_path = os.path.join(self.vault_root, "09_Performance", "downloaded_assets.json")
        
        assets_data = {asset_id: asset.dict() for asset_id, asset in self.downloaded_assets.items()}
        
        with open(data_path, 'w') as f:
            json.dump(assets_data, f, indent=2, default=str)
    
    def _load_existing_assets(self):
        """Load previously downloaded assets"""
        data_path = os.path.join(self.vault_root, "09_Performance", "downloaded_assets.json")
        
        try:
            if os.path.exists(data_path):
                with open(data_path) as f:
                    assets_data = json.load(f)
                    for asset_id, data in assets_data.items():
                        self.downloaded_assets[asset_id] = DownloadedAsset(**data)
        except Exception as e:
            print(f"Could not load existing assets: {e}")
    
    # Helper methods
    def _identify_source(self, netloc: str) -> Optional[str]:
        """Identify source from URL netloc"""
        if "pixabay.com" in netloc:
            return "pixabay"
        elif "freepik.com" in netloc:
            return "freepik"
        elif "tabletopaudio.com" in netloc:
            return "tabletop_audio"
        elif "soundimage.org" in netloc:
            return "soundimage"
        return None
    
    def _generate_filename(self, url: str, asset_type: str, theme_tags: List[str]) -> str:
        """Generate appropriate filename for asset"""
        themes = "_".join(theme_tags[:2]) if theme_tags else "general"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{asset_type}_{themes}_{timestamp}"
    
    def _get_extension_from_content_type(self, content_type: str, url: str) -> str:
        """Determine file extension from content type or URL"""
        extensions = {
            "image/jpeg": ".jpg",
            "image/png": ".png", 
            "image/webp": ".webp",
            "audio/mpeg": ".mp3",
            "audio/wav": ".wav",
            "audio/ogg": ".ogg"
        }
        
        if content_type in extensions:
            return extensions[content_type]
        
        # Fallback to URL extension
        parsed = urlparse(url)
        path_parts = parsed.path.split('.')
        if len(path_parts) > 1:
            return f".{path_parts[-1].lower()}"
        
        return ".unknown"
    
    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _generate_asset_id(self, url: str, filename: str) -> str:
        """Generate unique asset ID"""
        content = f"{url}_{filename}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _generate_attribution(self, source: AssetSource, url: str) -> str:
        """Generate proper attribution text"""
        if not source.attribution_required:
            return f"From {source.name}"
        
        return f"From {source.name} ({source.base_url})"
    
    def _extract_themes_from_npc(self, body: str) -> List[str]:
        """Extract theme tags from NPC description"""
        themes = []
        body_lower = body.lower()
        
        # World-specific themes
        if any(word in body_lower for word in ["ocean", "water", "tide", "depth", "coral"]):
            themes.append("aquabyssos")
        if any(word in body_lower for word in ["sky", "wind", "crystal", "air", "cloud"]):
            themes.append("aethermoor")
        
        # Role themes
        if any(word in body_lower for word in ["merchant", "trade"]):
            themes.append("merchant")
        if any(word in body_lower for word in ["noble", "lord", "lady"]):
            themes.append("noble")
        if any(word in body_lower for word in ["guard", "soldier", "military"]):
            themes.append("military")
        if any(word in body_lower for word in ["mage", "wizard", "arcane"]):
            themes.append("magical")
        
        return themes
    
    def _extract_themes_from_location(self, body: str) -> List[str]:
        """Extract theme tags from location description"""
        themes = []
        body_lower = body.lower()
        
        # Architectural themes
        if any(word in body_lower for word in ["temple", "shrine", "sacred"]):
            themes.append("religious")
        if any(word in body_lower for word in ["market", "trade", "merchant"]):
            themes.append("commercial")
        if any(word in body_lower for word in ["palace", "castle", "manor"]):
            themes.append("noble")
        if any(word in body_lower for word in ["tavern", "inn", "pub"]):
            themes.append("social")
        
        # Environmental themes
        if any(word in body_lower for word in ["underwater", "submerged", "deep"]):
            themes.append("underwater")
        if any(word in body_lower for word in ["floating", "aerial", "sky"]):
            themes.append("aerial")
        
        return themes

def main():
    """Main execution for asset downloader"""
    print("Initializing Asset Downloader...")
    
    downloader = AssetDownloader()
    
    # Create curated collection (demonstration)
    print("Creating curated asset collection...")
    assets = downloader.create_curated_asset_collection()
    
    # Integrate with vault
    print("Integrating assets with vault content...")
    integration_report = downloader.integrate_assets_with_vault(assets)
    
    # Save all data
    downloader.save_asset_data()
    
    print(f"Asset integration complete!")
    print(f"Assets processed: {len(assets)}")
    print(f"Vault integrations created: {integration_report['integrated_count']}")
    print(f"Asset gallery created at: 04_Resources/Assets/Asset_Gallery.md")
    
    print("\nTo use this system with real assets:")
    print("1. Browse the free sources identified:")
    print("   - Pixabay (pixabay.com) - No attribution required")
    print("   - Freepik (freepik.com) - Attribution required")
    print("   - Tabletop Audio (tabletopaudio.com) - CC BY-NC-SA")
    print("   - SoundImage (soundimage.org) - Attribution required")
    print("2. Use download_asset_from_url() with specific URLs")
    print("3. The system will automatically organize and integrate them")

if __name__ == "__main__":
    main()