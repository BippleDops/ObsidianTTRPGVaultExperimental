#!/usr/bin/env python3
"""
Backup Automation System
Comprehensive backup and versioning system for TTRPG vault
Part of Phase 4: Advanced Automation & Dynamic Systems
"""

import os
import json
import shutil
import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import subprocess
import tempfile
import tarfile
import gzip
import threading
import time
from collections import defaultdict

@dataclass
class BackupMetadata:
    timestamp: str
    backup_id: str
    backup_type: str  # 'full', 'incremental', 'snapshot'
    file_count: int
    total_size: int
    compression: str
    checksum: str
    previous_backup: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    notes: str = ""

@dataclass
class FileSnapshot:
    path: str
    size: int
    modified_time: float
    checksum: str
    backup_id: str

class BackupAutomationSystem:
    """Automated backup system with versioning and recovery."""
    
    def __init__(self, vault_path: str, backup_root: str = None):
        self.vault_path = Path(vault_path)
        self.backup_root = Path(backup_root) if backup_root else self.vault_path / "08_Archive" / "backups"
        self.backup_root.mkdir(parents=True, exist_ok=True)
        
        # Initialize backup database
        self.db_path = self.backup_root / "backup_metadata.db"
        self.init_backup_database()
        
        # Load configuration
        self.config = self.load_backup_config()
        
        # File tracking for incremental backups
        self.file_tracker = {}
        self.load_file_tracker()
        
    def load_backup_config(self) -> Dict:
        """Load backup configuration."""
        config_path = self.vault_path / "scripts" / "backup_config.json"
        
        default_config = {
            "backup_schedule": {
                "full_backup_days": 7,      # Weekly full backups
                "incremental_hours": 6,     # Every 6 hours incremental
                "snapshot_hours": 1         # Hourly snapshots
            },
            "retention_policy": {
                "keep_daily": 30,           # Keep daily backups for 30 days
                "keep_weekly": 12,          # Keep weekly backups for 12 weeks  
                "keep_monthly": 12,         # Keep monthly backups for 1 year
                "keep_full_always": True    # Never delete full backups
            },
            "compression": {
                "enabled": True,
                "level": 6,                 # gzip compression level
                "algorithm": "gzip"
            },
            "exclusions": [
                "*.tmp", "*.log", "*.backup", "*/.git/*", 
                "*/node_modules/*", "*/__pycache__/*",
                ".DS_Store", "Thumbs.db"
            ],
            "notifications": {
                "backup_complete": True,
                "backup_failed": True,
                "cleanup_complete": False
            },
            "integrity_checks": {
                "verify_after_backup": True,
                "deep_check_interval_days": 7,
                "checksum_algorithm": "sha256"
            },
            "remote_sync": {
                "enabled": False,
                "provider": "none",  # 'rsync', 's3', 'gdrive'
                "config": {}
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in loaded_config:
                        loaded_config[key] = value
                    elif isinstance(value, dict) and isinstance(loaded_config[key], dict):
                        for subkey, subvalue in value.items():
                            if subkey not in loaded_config[key]:
                                loaded_config[key][subkey] = subvalue
                return loaded_config
            except Exception as e:
                print(f"Error loading backup config: {e}")
                
        # Write default config
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
        
    def init_backup_database(self):
        """Initialize SQLite database for backup metadata."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS backups (
                    backup_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    backup_type TEXT NOT NULL,
                    file_count INTEGER,
                    total_size INTEGER,
                    compression TEXT,
                    checksum TEXT,
                    previous_backup TEXT,
                    tags TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (previous_backup) REFERENCES backups (backup_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    backup_id TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size INTEGER,
                    modified_time REAL,
                    checksum TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (backup_id) REFERENCES backups (backup_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS backup_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    backup_id TEXT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (backup_id) REFERENCES backups (backup_id)
                )
            """)
            
            # Create indexes for performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_backups_timestamp ON backups (timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_file_snapshots_backup ON file_snapshots (backup_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_file_snapshots_path ON file_snapshots (file_path)")
            
            conn.commit()
            
    def load_file_tracker(self):
        """Load file tracking data for incremental backups."""
        tracker_path = self.backup_root / "file_tracker.json"
        
        if tracker_path.exists():
            try:
                with open(tracker_path, 'r') as f:
                    self.file_tracker = json.load(f)
            except Exception as e:
                print(f"Error loading file tracker: {e}")
                self.file_tracker = {}
                
    def save_file_tracker(self):
        """Save file tracking data."""
        tracker_path = self.backup_root / "file_tracker.json"
        
        try:
            with open(tracker_path, 'w') as f:
                json.dump(self.file_tracker, f, indent=2)
        except Exception as e:
            print(f"Error saving file tracker: {e}")
            
    def calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate checksum for a file."""
        algorithm = self.config["integrity_checks"]["checksum_algorithm"]
        hasher = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error calculating checksum for {file_path}: {e}")
            return ""
            
    def get_files_to_backup(self, backup_type: str = "full") -> List[Path]:
        """Get list of files to backup based on type."""
        all_files = []
        
        # Walk through vault directory
        for root, dirs, files in os.walk(self.vault_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not self.is_excluded(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                if self.is_excluded(file_path):
                    continue
                    
                # For incremental backups, check if file changed
                if backup_type == "incremental":
                    if not self.has_file_changed(file_path):
                        continue
                        
                all_files.append(file_path)
                
        return sorted(all_files)
        
    def is_excluded(self, path: Path) -> bool:
        """Check if path matches exclusion patterns."""
        path_str = str(path)
        relative_path = str(path.relative_to(self.vault_path)) if path.is_relative_to(self.vault_path) else path_str
        
        import fnmatch
        
        for pattern in self.config["exclusions"]:
            if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(relative_path, pattern):
                return True
                
        return False
        
    def has_file_changed(self, file_path: Path) -> bool:
        """Check if file has changed since last backup."""
        try:
            stat = file_path.stat()
            relative_path = str(file_path.relative_to(self.vault_path))
            
            if relative_path not in self.file_tracker:
                return True
                
            tracked = self.file_tracker[relative_path]
            
            # Check modification time and size
            if (stat.st_mtime != tracked.get("mtime", 0) or
                stat.st_size != tracked.get("size", 0)):
                return True
                
            return False
            
        except Exception:
            return True  # If we can't check, assume it changed
            
    def update_file_tracker(self, files: List[Path], backup_id: str):
        """Update file tracker with current file states."""
        for file_path in files:
            try:
                stat = file_path.stat()
                relative_path = str(file_path.relative_to(self.vault_path))
                
                self.file_tracker[relative_path] = {
                    "mtime": stat.st_mtime,
                    "size": stat.st_size,
                    "backup_id": backup_id,
                    "checksum": self.calculate_file_checksum(file_path) if self.config["integrity_checks"]["verify_after_backup"] else ""
                }
            except Exception as e:
                print(f"Error updating tracker for {file_path}: {e}")
                
        self.save_file_tracker()
        
    def create_backup(self, backup_type: str = "full", tags: List[str] = None, 
                     notes: str = "") -> str:
        """Create a backup of the vault."""
        backup_id = f"{backup_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        timestamp = datetime.now().isoformat()
        
        print(f"Starting {backup_type} backup: {backup_id}")
        self.log_backup(backup_id, "INFO", f"Starting {backup_type} backup")
        
        try:
            # Get files to backup
            files_to_backup = self.get_files_to_backup(backup_type)
            
            if not files_to_backup:
                print("No files to backup")
                self.log_backup(backup_id, "INFO", "No files to backup")
                return backup_id
                
            # Create backup directory
            backup_dir = self.backup_root / backup_id
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine compression
            use_compression = self.config["compression"]["enabled"]
            compression_ext = ".tar.gz" if use_compression else ".tar"
            backup_archive = backup_dir / f"vault_backup{compression_ext}"
            
            # Create archive
            total_size = 0
            mode = "w:gz" if use_compression else "w"
            
            with tarfile.open(backup_archive, mode) as tar:
                for file_path in files_to_backup:
                    try:
                        # Calculate relative path for archive
                        arcname = str(file_path.relative_to(self.vault_path))
                        tar.add(file_path, arcname=arcname)
                        
                        total_size += file_path.stat().st_size
                        
                        # Store file snapshot info
                        self.store_file_snapshot(backup_id, file_path)
                        
                    except Exception as e:
                        self.log_backup(backup_id, "ERROR", f"Failed to backup {file_path}: {e}")
                        
            # Calculate archive checksum
            archive_checksum = self.calculate_file_checksum(backup_archive)
            
            # Update file tracker
            self.update_file_tracker(files_to_backup, backup_id)
            
            # Store backup metadata
            metadata = BackupMetadata(
                timestamp=timestamp,
                backup_id=backup_id,
                backup_type=backup_type,
                file_count=len(files_to_backup),
                total_size=total_size,
                compression=self.config["compression"]["algorithm"] if use_compression else "none",
                checksum=archive_checksum,
                tags=tags or [],
                notes=notes
            )
            
            self.store_backup_metadata(metadata)
            
            # Create manifest file
            manifest_path = backup_dir / "manifest.json"
            manifest_data = {
                "backup_id": backup_id,
                "timestamp": timestamp,
                "type": backup_type,
                "file_count": len(files_to_backup),
                "total_size": total_size,
                "files": [str(f.relative_to(self.vault_path)) for f in files_to_backup],
                "checksum": archive_checksum
            }
            
            with open(manifest_path, 'w') as f:
                json.dump(manifest_data, f, indent=2)
                
            # Verify backup if enabled
            if self.config["integrity_checks"]["verify_after_backup"]:
                if self.verify_backup(backup_id):
                    self.log_backup(backup_id, "INFO", "Backup verification successful")
                else:
                    self.log_backup(backup_id, "ERROR", "Backup verification failed")
                    
            print(f"Backup completed: {backup_id}")
            print(f"  Files: {len(files_to_backup)}")
            print(f"  Size: {self.format_size(total_size)}")
            print(f"  Archive: {backup_archive}")
            
            self.log_backup(backup_id, "INFO", f"Backup completed successfully - {len(files_to_backup)} files, {self.format_size(total_size)}")
            
            # Remote sync if configured
            if self.config["remote_sync"]["enabled"]:
                self.sync_to_remote(backup_id)
                
            return backup_id
            
        except Exception as e:
            error_msg = f"Backup failed: {e}"
            print(error_msg)
            self.log_backup(backup_id, "ERROR", error_msg)
            raise
            
    def store_file_snapshot(self, backup_id: str, file_path: Path):
        """Store file snapshot information."""
        try:
            stat = file_path.stat()
            checksum = self.calculate_file_checksum(file_path) if self.config["integrity_checks"]["verify_after_backup"] else ""
            relative_path = str(file_path.relative_to(self.vault_path))
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO file_snapshots 
                    (backup_id, file_path, file_size, modified_time, checksum)
                    VALUES (?, ?, ?, ?, ?)
                """, (backup_id, relative_path, stat.st_size, stat.st_mtime, checksum))
                
        except Exception as e:
            print(f"Error storing file snapshot for {file_path}: {e}")
            
    def store_backup_metadata(self, metadata: BackupMetadata):
        """Store backup metadata in database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO backups 
                (backup_id, timestamp, backup_type, file_count, total_size, 
                 compression, checksum, previous_backup, tags, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                metadata.backup_id, metadata.timestamp, metadata.backup_type,
                metadata.file_count, metadata.total_size, metadata.compression,
                metadata.checksum, metadata.previous_backup,
                json.dumps(metadata.tags), metadata.notes
            ))
            
    def log_backup(self, backup_id: str, level: str, message: str):
        """Log backup operation."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO backup_logs (backup_id, level, message)
                VALUES (?, ?, ?)
            """, (backup_id, level, message))
            
        # Also log to console if verbose
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def verify_backup(self, backup_id: str) -> bool:
        """Verify integrity of a backup."""
        try:
            backup_dir = self.backup_root / backup_id
            
            # Load manifest
            manifest_path = backup_dir / "manifest.json"
            if not manifest_path.exists():
                return False
                
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                
            # Find archive file
            archive_files = list(backup_dir.glob("vault_backup.*"))
            if not archive_files:
                return False
                
            archive_path = archive_files[0]
            
            # Verify archive checksum
            current_checksum = self.calculate_file_checksum(archive_path)
            if current_checksum != manifest.get("checksum", ""):
                print(f"Checksum mismatch for {backup_id}")
                return False
                
            # Verify archive can be opened
            mode = "r:gz" if archive_path.suffix == ".gz" else "r"
            with tarfile.open(archive_path, mode) as tar:
                # Check that all expected files are present
                archive_files = set(tar.getnames())
                expected_files = set(manifest["files"])
                
                if archive_files != expected_files:
                    print(f"File list mismatch for {backup_id}")
                    return False
                    
            return True
            
        except Exception as e:
            print(f"Backup verification failed for {backup_id}: {e}")
            return False
            
    def list_backups(self, backup_type: str = None, limit: int = None) -> List[Dict]:
        """List available backups."""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT * FROM backups"
            params = []
            
            if backup_type:
                query += " WHERE backup_type = ?"
                params.append(backup_type)
                
            query += " ORDER BY timestamp DESC"
            
            if limit:
                query += f" LIMIT {limit}"
                
            cursor = conn.execute(query, params)
            columns = [description[0] for description in cursor.description]
            
            backups = []
            for row in cursor.fetchall():
                backup_data = dict(zip(columns, row))
                backup_data['tags'] = json.loads(backup_data['tags'] or '[]')
                backups.append(backup_data)
                
            return backups
            
    def restore_backup(self, backup_id: str, target_path: str = None, 
                      file_patterns: List[str] = None) -> bool:
        """Restore files from a backup."""
        if not target_path:
            target_path = str(self.vault_path)
            
        target_dir = Path(target_path)
        backup_dir = self.backup_root / backup_id
        
        if not backup_dir.exists():
            print(f"Backup {backup_id} not found")
            return False
            
        print(f"Restoring backup {backup_id} to {target_path}")
        
        try:
            # Find archive file
            archive_files = list(backup_dir.glob("vault_backup.*"))
            if not archive_files:
                print("No archive file found in backup")
                return False
                
            archive_path = archive_files[0]
            mode = "r:gz" if archive_path.suffix == ".gz" else "r"
            
            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)
            
            restored_count = 0
            
            with tarfile.open(archive_path, mode) as tar:
                for member in tar.getmembers():
                    # Apply file pattern filters if specified
                    if file_patterns:
                        import fnmatch
                        if not any(fnmatch.fnmatch(member.name, pattern) for pattern in file_patterns):
                            continue
                            
                    try:
                        tar.extract(member, target_dir)
                        restored_count += 1
                        
                        if restored_count % 100 == 0:
                            print(f"Restored {restored_count} files...")
                            
                    except Exception as e:
                        print(f"Error restoring {member.name}: {e}")
                        
            print(f"Restore completed: {restored_count} files restored")
            self.log_backup(backup_id, "INFO", f"Restore completed - {restored_count} files to {target_path}")
            
            return True
            
        except Exception as e:
            print(f"Restore failed: {e}")
            self.log_backup(backup_id, "ERROR", f"Restore failed: {e}")
            return False
            
    def cleanup_old_backups(self) -> Dict[str, int]:
        """Clean up old backups according to retention policy."""
        policy = self.config["retention_policy"]
        now = datetime.now()
        
        backups = self.list_backups()
        to_delete = []
        kept = {"daily": 0, "weekly": 0, "monthly": 0, "full": 0}
        
        # Group backups by age categories
        daily_cutoff = now - timedelta(days=policy["keep_daily"])
        weekly_cutoff = now - timedelta(weeks=policy["keep_weekly"])
        monthly_cutoff = now - timedelta(days=policy["keep_monthly"] * 30)
        
        for backup in backups:
            backup_time = datetime.fromisoformat(backup["timestamp"])
            backup_age = now - backup_time
            
            # Never delete full backups if policy says so
            if policy["keep_full_always"] and backup["backup_type"] == "full":
                kept["full"] += 1
                continue
                
            # Apply retention rules
            delete_backup = False
            
            if backup_time < monthly_cutoff:
                # Very old - delete unless it's a monthly keeper
                if backup_time.day != 1 or backup["backup_type"] != "full":
                    delete_backup = True
            elif backup_time < weekly_cutoff:
                # Old - keep weekly full backups
                if backup["backup_type"] != "full" or backup_time.weekday() != 6:  # Sunday
                    delete_backup = True
                else:
                    kept["weekly"] += 1
            elif backup_time < daily_cutoff:
                # Recent - keep daily backups
                kept["daily"] += 1
            else:
                # Very recent - keep all
                pass
                
            if delete_backup:
                to_delete.append(backup)
                
        # Delete marked backups
        deleted_count = 0
        for backup in to_delete:
            if self.delete_backup(backup["backup_id"]):
                deleted_count += 1
                
        print(f"Cleanup completed: {deleted_count} backups deleted")
        print(f"Kept: {kept['daily']} daily, {kept['weekly']} weekly, {kept['full']} full backups")
        
        return {"deleted": deleted_count, "kept": sum(kept.values())}
        
    def delete_backup(self, backup_id: str) -> bool:
        """Delete a specific backup."""
        try:
            backup_dir = self.backup_root / backup_id
            
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
                
            # Remove from database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM backups WHERE backup_id = ?", (backup_id,))
                conn.execute("DELETE FROM file_snapshots WHERE backup_id = ?", (backup_id,))
                conn.execute("DELETE FROM backup_logs WHERE backup_id = ?", (backup_id,))
                
            print(f"Deleted backup: {backup_id}")
            return True
            
        except Exception as e:
            print(f"Error deleting backup {backup_id}: {e}")
            return False
            
    def sync_to_remote(self, backup_id: str):
        """Sync backup to remote storage."""
        remote_config = self.config["remote_sync"]
        
        if not remote_config["enabled"]:
            return
            
        provider = remote_config["provider"]
        print(f"Syncing {backup_id} to {provider}...")
        
        # This is a placeholder - actual implementation would depend on provider
        if provider == "rsync":
            self.sync_via_rsync(backup_id, remote_config["config"])
        elif provider == "s3":
            self.sync_via_s3(backup_id, remote_config["config"])
        else:
            print(f"Remote sync provider {provider} not implemented")
            
    def sync_via_rsync(self, backup_id: str, config: Dict):
        """Sync via rsync."""
        # Placeholder implementation
        pass
        
    def sync_via_s3(self, backup_id: str, config: Dict):
        """Sync via AWS S3."""
        # Placeholder implementation
        pass
        
    def generate_backup_report(self) -> str:
        """Generate comprehensive backup report."""
        backups = self.list_backups(limit=50)
        
        if not backups:
            return "No backups found."
            
        # Calculate statistics
        total_backups = len(backups)
        total_size = sum(b["total_size"] or 0 for b in backups)
        backup_types = defaultdict(int)
        
        for backup in backups:
            backup_types[backup["backup_type"]] += 1
            
        # Recent backup status
        latest_backup = backups[0] if backups else None
        latest_time = datetime.fromisoformat(latest_backup["timestamp"]) if latest_backup else None
        
        lines = [
            "# Backup System Report",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Summary",
            f"- **Total backups**: {total_backups}",
            f"- **Total size**: {self.format_size(total_size)}",
            f"- **Backup types**: {dict(backup_types)}",
            ""
        ]
        
        if latest_backup:
            age = datetime.now() - latest_time
            lines.extend([
                "## Latest Backup",
                f"- **ID**: {latest_backup['backup_id']}",
                f"- **Type**: {latest_backup['backup_type']}", 
                f"- **Created**: {latest_backup['timestamp']} ({age.days} days ago)",
                f"- **Files**: {latest_backup['file_count']}",
                f"- **Size**: {self.format_size(latest_backup['total_size'] or 0)}",
                ""
            ])
            
        # Recent backups list
        lines.extend([
            "## Recent Backups",
            ""
        ])
        
        for backup in backups[:10]:
            backup_time = datetime.fromisoformat(backup["timestamp"])
            age = datetime.now() - backup_time
            
            lines.append(f"- **{backup['backup_id']}** ({backup['backup_type']}) - "
                        f"{backup_time.strftime('%Y-%m-%d %H:%M')} "
                        f"({age.days}d ago) - "
                        f"{backup['file_count']} files, "
                        f"{self.format_size(backup['total_size'] or 0)}")
                        
        return '\n'.join(lines)
        
    def format_size(self, size: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
        
    def schedule_backups(self):
        """Run scheduled backup daemon."""
        print("Starting backup scheduler...")
        
        last_full = datetime.min
        last_incremental = datetime.min
        last_snapshot = datetime.min
        
        schedule = self.config["backup_schedule"]
        
        while True:
            try:
                now = datetime.now()
                
                # Check if full backup is due
                if (now - last_full).days >= schedule["full_backup_days"]:
                    print("Running scheduled full backup...")
                    self.create_backup("full", tags=["scheduled"])
                    last_full = now
                    
                # Check if incremental backup is due  
                elif (now - last_incremental).seconds >= schedule["incremental_hours"] * 3600:
                    print("Running scheduled incremental backup...")
                    self.create_backup("incremental", tags=["scheduled"])
                    last_incremental = now
                    
                # Check if snapshot is due
                elif (now - last_snapshot).seconds >= schedule["snapshot_hours"] * 3600:
                    print("Running scheduled snapshot...")
                    self.create_backup("snapshot", tags=["scheduled"])
                    last_snapshot = now
                    
                # Run cleanup weekly
                if now.weekday() == 0 and now.hour == 2:  # Monday 2 AM
                    self.cleanup_old_backups()
                    
                # Wait before next check
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                print("Backup scheduler stopped")
                break
            except Exception as e:
                print(f"Error in backup scheduler: {e}")
                time.sleep(60)

def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Backup Automation System")
    parser.add_argument("--vault-path", default=".", help="Path to vault root")
    parser.add_argument("--backup-root", help="Path to backup storage directory")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create backup")
    backup_parser.add_argument("--type", choices=["full", "incremental", "snapshot"], 
                              default="full", help="Backup type")
    backup_parser.add_argument("--tags", nargs="*", help="Tags for backup")
    backup_parser.add_argument("--notes", help="Notes for backup")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List backups")
    list_parser.add_argument("--type", help="Filter by backup type")
    list_parser.add_argument("--limit", type=int, default=20, help="Limit results")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore backup")
    restore_parser.add_argument("backup_id", help="Backup ID to restore")
    restore_parser.add_argument("--target", help="Target directory for restore")
    restore_parser.add_argument("--files", nargs="*", help="File patterns to restore")
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify backup")
    verify_parser.add_argument("backup_id", help="Backup ID to verify")
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up old backups")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate backup report")
    
    # Schedule command
    schedule_parser = subparsers.add_parser("schedule", help="Run backup scheduler")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    backup_system = BackupAutomationSystem(args.vault_path, args.backup_root)
    
    if args.command == "backup":
        backup_id = backup_system.create_backup(
            backup_type=args.type,
            tags=args.tags,
            notes=args.notes or ""
        )
        print(f"Backup created: {backup_id}")
        
    elif args.command == "list":
        backups = backup_system.list_backups(args.type, args.limit)
        
        print(f"{'Backup ID':<30} {'Type':<12} {'Date':<20} {'Files':<8} {'Size':<10}")
        print("-" * 80)
        
        for backup in backups:
            backup_time = datetime.fromisoformat(backup["timestamp"])
            size_str = backup_system.format_size(backup["total_size"] or 0)
            
            print(f"{backup['backup_id']:<30} "
                  f"{backup['backup_type']:<12} "
                  f"{backup_time.strftime('%Y-%m-%d %H:%M'):<20} "
                  f"{backup['file_count'] or 0:<8} "
                  f"{size_str:<10}")
                  
    elif args.command == "restore":
        success = backup_system.restore_backup(
            args.backup_id, 
            args.target,
            args.files
        )
        print("Restore completed successfully" if success else "Restore failed")
        
    elif args.command == "verify":
        valid = backup_system.verify_backup(args.backup_id)
        print("Backup is valid" if valid else "Backup is invalid or corrupted")
        
    elif args.command == "cleanup":
        results = backup_system.cleanup_old_backups()
        print(f"Cleanup completed: {results}")
        
    elif args.command == "report":
        report = backup_system.generate_backup_report()
        print(report)
        
    elif args.command == "schedule":
        backup_system.schedule_backups()

if __name__ == "__main__":
    main()