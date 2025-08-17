#!/usr/bin/env python3
"""
Vault Metrics Collector
Collects comprehensive metrics about vault health and usage using Pydantic models.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import Counter, defaultdict
import statistics

# Import our Pydantic models  
import sys
sys.path.append('../data')
from models import VaultMetrics, ContentType, ContentStatus, WorldRealm

class VaultMetricsCollector:
    """Collects comprehensive vault metrics."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.metrics = VaultMetrics()
        
    def collect_file_metrics(self) -> Dict[str, Any]:
        """Collect basic file metrics."""
        md_files = list(self.vault_path.rglob('*.md'))
        
        # Filter out system files
        content_files = [f for f in md_files if not any(skip in str(f).lower() 
                        for skip in ['.obsidian', 'readme', 'license'])]
        
        self.metrics.total_files = len(content_files)
        
        # Analyze by directory
        dir_counts = Counter()
        for file_path in content_files:
            rel_path = file_path.relative_to(self.vault_path)
            top_dir = rel_path.parts[0] if rel_path.parts else 'root'
            dir_counts[top_dir] += 1
            
        return {
            "total_files": len(content_files),
            "files_by_directory": dict(dir_counts),
            "average_files_per_directory": statistics.mean(dir_counts.values()) if dir_counts else 0
        }
        
    def collect_content_type_metrics(self) -> Dict[str, Any]:
        """Collect content type distribution metrics."""
        md_files = list(self.vault_path.rglob('*.md'))
        content_files = [f for f in md_files if not any(skip in str(f).lower() 
                        for skip in ['.obsidian', 'readme', 'license'])]
        
        type_counts = Counter()
        status_counts = Counter() 
        world_counts = Counter()
        
        for file_path in content_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
                
            # Determine content type
            content_type = self.determine_content_type(file_path, content)
            type_counts[content_type.value] += 1
            
            # Determine status
            status = self.determine_status(content)
            status_counts[status.value] += 1
            
            # Determine world
            world = self.determine_world(content)
            world_counts[world.value] += 1
            
        # Update metrics object
        self.metrics.content_by_type = {ContentType(k): v for k, v in type_counts.items()}
        self.metrics.content_by_status = {ContentStatus(k): v for k, v in status_counts.items()}
        self.metrics.content_by_realm = {WorldRealm(k): v for k, v in world_counts.items()}
        
        return {
            "content_by_type": dict(type_counts),
            "content_by_status": dict(status_counts),
            "content_by_realm": dict(world_counts)
        }
        
    def determine_content_type(self, file_path: Path, content: str) -> ContentType:
        """Determine content type from file and content analysis."""
        path_str = str(file_path).lower()
        content_lower = content.lower()
        
        # Path-based determination
        if 'adventures' in path_str or 'campaigns' in path_str:
            if 'session' in path_str:
                return ContentType.session
            else:
                return ContentType.adventure
        elif 'groups' in path_str:
            # Distinguish characters from factions
            char_indicators = ['age:', 'species:', 'personality:', 'appearance:']
            if any(indicator in content_lower for indicator in char_indicators):
                return ContentType.character
            else:
                return ContentType.faction
        elif 'places' in path_str or 'locations' in path_str:
            return ContentType.location
        elif 'items' in path_str:
            return ContentType.item
        elif 'mechanics' in path_str:
            return ContentType.mechanics
        elif 'templates' in path_str:
            return ContentType.template
        elif 'resources' in path_str:
            return ContentType.resource
        elif 'reports' in path_str:
            return ContentType.report
        else:
            return ContentType.lore
            
    def determine_status(self, content: str) -> ContentStatus:
        """Determine content status from content analysis."""
        content_upper = content.upper()
        
        if 'DEPRECATED' in content_upper or 'ARCHIVED' in content_upper:
            return ContentStatus.archived
        elif len(content.strip()) < 100:
            return ContentStatus.stub
        elif any(marker in content_upper for marker in ['TODO', 'TBD', 'DRAFT', 'WIP']):
            return ContentStatus.draft
        elif 'COMPLETE' in content_upper:
            return ContentStatus.complete
        else:
            return ContentStatus.active
            
    def determine_world(self, content: str) -> WorldRealm:
        """Determine world realm from content."""
        content_lower = content.lower()
        
        aquabyssos_indicators = ['aquabyssos', 'depth', 'pressure', 'abyssal', 'underwater', 'coral']
        aethermoor_indicators = ['aethermoor', 'sky', 'wind', 'crystal', 'altitude', 'air']
        convergence_indicators = ['convergence', 'merger', 'bridge', 'transition']
        
        aqua_score = sum(1 for word in aquabyssos_indicators if word in content_lower)
        aether_score = sum(1 for word in aethermoor_indicators if word in content_lower)
        conv_score = sum(1 for word in convergence_indicators if word in content_lower)
        
        if conv_score > 0 and (aqua_score > 0 or aether_score > 0):
            return WorldRealm.convergence
        elif aqua_score > aether_score:
            return WorldRealm.aquabyssos
        elif aether_score > aqua_score:
            return WorldRealm.aethermoor
        else:
            return WorldRealm.both
            
    def collect_link_metrics(self) -> Dict[str, Any]:
        """Collect wikilink and reference metrics."""
        md_files = list(self.vault_path.rglob('*.md'))
        content_files = [f for f in md_files if not any(skip in str(f).lower() 
                        for skip in ['.obsidian', 'readme', 'license'])]
        
        total_wikilinks = 0
        total_external_links = 0
        broken_links = 0
        link_targets = Counter()
        
        # Get all file names for link validation
        file_names = {f.stem for f in content_files}
        
        for file_path in content_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
                
            # Count wikilinks
            wikilinks = re.findall(r'\[\[([^]]+)\]\]', content)
            total_wikilinks += len(wikilinks)
            
            for link in wikilinks:
                # Clean link (remove # and | parts)
                clean_link = link.split('#')[0].split('|')[0].strip()
                link_targets[clean_link] += 1
                
                # Check if link target exists
                if clean_link not in file_names:
                    broken_links += 1
                    
            # Count external links
            external_links = re.findall(r'https?://[^\s\]]+', content)
            total_external_links += len(external_links)
            
        self.metrics.broken_links = broken_links
        
        return {
            "total_wikilinks": total_wikilinks,
            "total_external_links": total_external_links,
            "broken_links": broken_links,
            "unique_link_targets": len(link_targets),
            "most_linked_content": link_targets.most_common(10),
            "link_density": total_wikilinks / len(content_files) if content_files else 0
        }
        
    def collect_content_quality_metrics(self) -> Dict[str, Any]:
        """Collect content quality and depth metrics."""
        md_files = list(self.vault_path.rglob('*.md'))
        content_files = [f for f in md_files if not any(skip in str(f).lower() 
                        for skip in ['.obsidian', 'readme', 'license'])]
        
        word_counts = []
        paragraph_counts = []
        section_counts = []
        orphaned_files = []
        
        for file_path in content_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
                
            # Word count
            words = len(content.split())
            word_counts.append(words)
            
            # Paragraph count
            paragraphs = len([p for p in content.split('\n\n') if p.strip()])
            paragraph_counts.append(paragraphs)
            
            # Section count (headers)
            sections = len(re.findall(r'^#+\s', content, re.MULTILINE))
            section_counts.append(sections)
            
            # Check for orphaned files (no incoming links)
            file_name = file_path.stem
            is_orphaned = True
            
            # Quick check - if mentioned in other files
            for other_file in content_files:
                if other_file == file_path:
                    continue
                try:
                    with open(other_file, 'r', encoding='utf-8') as f:
                        other_content = f.read()
                    if file_name in other_content or f"[[{file_name}]]" in other_content:
                        is_orphaned = False
                        break
                except Exception:
                    continue
                    
            if is_orphaned:
                orphaned_files.append(str(file_path.relative_to(self.vault_path)))
                
        self.metrics.orphaned_content = len(orphaned_files)
        
        return {
            "word_count_stats": {
                "mean": statistics.mean(word_counts) if word_counts else 0,
                "median": statistics.median(word_counts) if word_counts else 0,
                "min": min(word_counts) if word_counts else 0,
                "max": max(word_counts) if word_counts else 0,
                "std_dev": statistics.stdev(word_counts) if len(word_counts) > 1 else 0
            },
            "paragraph_count_stats": {
                "mean": statistics.mean(paragraph_counts) if paragraph_counts else 0,
                "median": statistics.median(paragraph_counts) if paragraph_counts else 0
            },
            "section_count_stats": {
                "mean": statistics.mean(section_counts) if section_counts else 0,
                "median": statistics.median(section_counts) if section_counts else 0
            },
            "orphaned_files": orphaned_files[:20],  # Limit output
            "total_orphaned": len(orphaned_files)
        }
        
    def collect_activity_metrics(self) -> Dict[str, Any]:
        """Collect activity and update frequency metrics."""
        md_files = list(self.vault_path.rglob('*.md'))
        content_files = [f for f in md_files if not any(skip in str(f).lower() 
                        for skip in ['.obsidian', 'readme', 'license'])]
        
        now = datetime.now()
        recently_modified = []
        stale_files = []
        
        for file_path in content_files:
            try:
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                age_days = (now - mod_time).days
                
                if age_days <= 7:
                    recently_modified.append(str(file_path.relative_to(self.vault_path)))
                elif age_days > 90:
                    stale_files.append({
                        "file": str(file_path.relative_to(self.vault_path)),
                        "days_old": age_days
                    })
                    
            except Exception:
                continue
                
        return {
            "recently_modified_count": len(recently_modified),
            "recently_modified_files": recently_modified[:10],
            "stale_files_count": len(stale_files),
            "oldest_files": sorted(stale_files, key=lambda x: x['days_old'], reverse=True)[:10]
        }
        
    def collect_comprehensive_metrics(self) -> Dict[str, Any]:
        """Collect all metrics and compile comprehensive report."""
        self.metrics.last_updated = datetime.now()
        
        file_metrics = self.collect_file_metrics()
        content_metrics = self.collect_content_type_metrics()
        link_metrics = self.collect_link_metrics()
        quality_metrics = self.collect_content_quality_metrics()
        activity_metrics = self.collect_activity_metrics()
        
        # Calculate health score
        health_score = self.calculate_vault_health_score(
            file_metrics, content_metrics, link_metrics, quality_metrics
        )
        
        comprehensive_report = {
            "timestamp": datetime.now().isoformat(),
            "vault_metrics": self.metrics.dict(),
            "file_metrics": file_metrics,
            "content_metrics": content_metrics,
            "link_metrics": link_metrics,
            "quality_metrics": quality_metrics,
            "activity_metrics": activity_metrics,
            "health_score": health_score,
            "recommendations": self.generate_recommendations(
                file_metrics, content_metrics, link_metrics, quality_metrics
            )
        }
        
        return comprehensive_report
        
    def calculate_vault_health_score(self, file_metrics: Dict, content_metrics: Dict, 
                                   link_metrics: Dict, quality_metrics: Dict) -> Dict[str, Any]:
        """Calculate overall vault health score."""
        score = 0
        max_score = 100
        
        # File organization score (0-20 points)
        total_files = file_metrics["total_files"]
        if total_files >= 100:
            score += 20
        elif total_files >= 50:
            score += 15
        elif total_files >= 25:
            score += 10
        elif total_files >= 10:
            score += 5
            
        # Content diversity score (0-20 points)
        type_diversity = len(content_metrics["content_by_type"])
        score += min(type_diversity * 2.5, 20)
        
        # Link connectivity score (0-25 points)
        if link_metrics["total_wikilinks"] > 0:
            broken_link_ratio = link_metrics["broken_links"] / link_metrics["total_wikilinks"]
            connectivity_score = (1 - broken_link_ratio) * 25
            score += max(0, connectivity_score)
            
        # Content quality score (0-25 points)
        avg_word_count = quality_metrics["word_count_stats"]["mean"]
        if avg_word_count >= 500:
            score += 15
        elif avg_word_count >= 250:
            score += 10
        elif avg_word_count >= 100:
            score += 5
            
        orphan_ratio = quality_metrics["total_orphaned"] / total_files if total_files > 0 else 0
        orphan_penalty = min(orphan_ratio * 10, 10)
        score += (10 - orphan_penalty)
        
        # Development status score (0-10 points) 
        status_counts = content_metrics["content_by_status"]
        active_ratio = status_counts.get("active", 0) / total_files if total_files > 0 else 0
        score += active_ratio * 10
        
        return {
            "overall_score": min(score, max_score),
            "grade": self.score_to_grade(score),
            "breakdown": {
                "file_organization": min(20, score if total_files >= 100 else (total_files / 100) * 20),
                "content_diversity": min(type_diversity * 2.5, 20),
                "link_connectivity": max(0, (1 - (link_metrics["broken_links"] / max(1, link_metrics["total_wikilinks"]))) * 25),
                "content_quality": min(25, (avg_word_count / 500) * 15 + (10 - orphan_penalty)),
                "development_status": active_ratio * 10
            }
        }
        
    def score_to_grade(self, score: float) -> str:
        """Convert numerical score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
            
    def generate_recommendations(self, file_metrics: Dict, content_metrics: Dict,
                               link_metrics: Dict, quality_metrics: Dict) -> List[Dict[str, str]]:
        """Generate improvement recommendations."""
        recommendations = []
        
        # Check for broken links
        if link_metrics["broken_links"] > 0:
            recommendations.append({
                "priority": "high",
                "category": "connectivity",
                "issue": f"{link_metrics['broken_links']} broken links found",
                "action": "Review and fix broken wikilinks to improve content connectivity"
            })
            
        # Check for orphaned content
        if quality_metrics["total_orphaned"] > quality_metrics["total_orphaned"] * 0.2:
            recommendations.append({
                "priority": "medium",
                "category": "connectivity",
                "issue": f"{quality_metrics['total_orphaned']} orphaned files",
                "action": "Add links to orphaned content to improve discoverability"
            })
            
        # Check content quality
        avg_words = quality_metrics["word_count_stats"]["mean"]
        if avg_words < 200:
            recommendations.append({
                "priority": "medium",
                "category": "quality",
                "issue": f"Low average word count ({avg_words:.0f} words)",
                "action": "Expand stub and draft content with more details"
            })
            
        # Check for stub content
        status_counts = content_metrics["content_by_status"]
        stub_count = status_counts.get("stub", 0)
        if stub_count > 0:
            recommendations.append({
                "priority": "low",
                "category": "development",
                "issue": f"{stub_count} stub files need development",
                "action": "Prioritize expanding stub content to draft or active status"
            })
            
        return recommendations
        
    def export_metrics(self, report: Dict[str, Any], output_path: str) -> None:
        """Export comprehensive metrics report."""
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        print(f"Vault metrics exported to: {output_path}")
        
def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Collect vault metrics for Cordelia vault")
    parser.add_argument("vault_path", help="Path to vault directory")
    parser.add_argument("--output", "-o", help="Output path for metrics report", 
                       default="vault_metrics_report.json")
    
    args = parser.parse_args()
    
    collector = VaultMetricsCollector(args.vault_path)
    
    print("Collecting vault metrics...")
    report = collector.collect_comprehensive_metrics()
    
    health_score = report["health_score"]
    print(f"\nVault Health Report:")
    print(f"Overall Score: {health_score['overall_score']:.1f}/100 (Grade: {health_score['grade']})")
    print(f"Total Files: {report['file_metrics']['total_files']}")
    print(f"Broken Links: {report['link_metrics']['broken_links']}")
    print(f"Orphaned Files: {report['quality_metrics']['total_orphaned']}")
    print(f"Recommendations: {len(report['recommendations'])}")
    
    collector.export_metrics(report, args.output)
    
if __name__ == "__main__":
    main()