#!/usr/bin/env python3
"""
Update Notification System
Smart notification system for vault changes and important updates
Part of Phase 4: Advanced Automation & Dynamic Systems
"""

import os
import json
import sqlite3
import smtplib
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import subprocess
import threading
import time
import yaml
import re

@dataclass
class UpdateEvent:
    event_id: str
    event_type: str
    file_path: str
    description: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False

@dataclass
class NotificationRule:
    rule_id: str
    name: str
    enabled: bool
    conditions: Dict[str, Any]
    actions: List[str]
    frequency: str  # 'immediate', 'hourly', 'daily', 'weekly'
    priority: int

@dataclass
class NotificationChannel:
    channel_id: str
    channel_type: str  # 'email', 'webhook', 'file', 'console'
    config: Dict[str, Any]
    enabled: bool

class UpdateNotificationSystem:
    """Smart notification system for vault updates."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.config = self.load_config()
        
        # Database setup
        self.db_path = self.vault_path / "scripts" / "notifications.db"
        self.init_database()
        
        # File watching
        self.file_checksums = {}
        self.watched_files = set()
        self.event_queue = deque(maxlen=1000)
        
        # Notification state
        self.last_digest_time = {}
        self.pending_notifications = defaultdict(list)
        
        # Load initial state
        self.load_file_states()
        
    def load_config(self) -> Dict:
        """Load notification configuration."""
        config_path = self.vault_path / "scripts" / "notification_config.json"
        
        default_config = {
            "monitoring": {
                "enabled": True,
                "scan_interval_seconds": 30,
                "watched_directories": [
                    "02_Worldbuilding",
                    "01_Adventures", 
                    "03_Mechanics",
                    "05_Templates"
                ],
                "watched_file_patterns": [
                    "*.md", "*.json", "*.yaml", "*.yml"
                ],
                "ignore_patterns": [
                    "*.backup", "*.tmp", "*.log", "*/.git/*"
                ]
            },
            "notification_rules": [
                {
                    "rule_id": "major_content_change",
                    "name": "Major Content Changes",
                    "enabled": True,
                    "conditions": {
                        "file_types": ["md"],
                        "directories": ["02_Worldbuilding/People", "02_Worldbuilding/Places"],
                        "change_threshold": 0.3  # 30% change
                    },
                    "actions": ["email", "digest"],
                    "frequency": "immediate",
                    "priority": 8
                },
                {
                    "rule_id": "new_npc_creation",
                    "name": "New NPC Created",
                    "enabled": True,
                    "conditions": {
                        "event_type": "file_created",
                        "directories": ["02_Worldbuilding/People"],
                        "file_types": ["md"]
                    },
                    "actions": ["email", "webhook"],
                    "frequency": "immediate", 
                    "priority": 6
                },
                {
                    "rule_id": "session_notes_update",
                    "name": "Session Notes Updated",
                    "enabled": True,
                    "conditions": {
                        "directories": ["1-Session Journals"],
                        "event_type": "file_modified"
                    },
                    "actions": ["digest"],
                    "frequency": "daily",
                    "priority": 4
                },
                {
                    "rule_id": "broken_links_detected",
                    "name": "Broken Links Detected",
                    "enabled": True,
                    "conditions": {
                        "event_type": "validation_error",
                        "error_type": "broken_link"
                    },
                    "actions": ["email"],
                    "frequency": "daily",
                    "priority": 7
                }
            ],
            "notification_channels": [
                {
                    "channel_id": "primary_email",
                    "channel_type": "email",
                    "enabled": False,
                    "config": {
                        "smtp_server": "smtp.gmail.com",
                        "smtp_port": 587,
                        "username": "",
                        "password": "",
                        "from_address": "",
                        "to_addresses": []
                    }
                },
                {
                    "channel_id": "webhook",
                    "channel_type": "webhook", 
                    "enabled": False,
                    "config": {
                        "url": "",
                        "method": "POST",
                        "headers": {},
                        "format": "json"
                    }
                },
                {
                    "channel_id": "digest_file",
                    "channel_type": "file",
                    "enabled": True,
                    "config": {
                        "file_path": "vault_updates_digest.md",
                        "format": "markdown",
                        "max_entries": 100
                    }
                }
            ],
            "digest_settings": {
                "daily_digest_hour": 9,
                "weekly_digest_day": 1,  # Monday
                "include_statistics": True,
                "include_recent_changes": True,
                "max_items_per_category": 10
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
                print(f"Error loading notification config: {e}")
                
        # Write default config
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
        
    def init_database(self):
        """Initialize SQLite database for tracking."""
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    description TEXT,
                    severity TEXT,
                    timestamp TEXT,
                    metadata TEXT,
                    acknowledged BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notifications_sent (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT,
                    FOREIGN KEY (event_id) REFERENCES events (event_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_states (
                    file_path TEXT PRIMARY KEY,
                    checksum TEXT,
                    size INTEGER,
                    modified_time REAL,
                    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS digest_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    digest_type TEXT NOT NULL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    event_count INTEGER,
                    content_hash TEXT
                )
            """)
            
            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events (timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events (event_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_file_states_modified ON file_states (modified_time)")
            
            conn.commit()
            
    def load_file_states(self):
        """Load current file states from database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT file_path, checksum, size, modified_time FROM file_states")
            
            for row in cursor.fetchall():
                file_path, checksum, size, modified_time = row
                self.file_checksums[file_path] = {
                    "checksum": checksum,
                    "size": size,
                    "modified_time": modified_time
                }
                
    def calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum of file."""
        hasher = hashlib.md5()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""
            
    def scan_for_changes(self) -> List[UpdateEvent]:
        """Scan vault for file changes."""
        events = []
        monitoring = self.config["monitoring"]
        
        if not monitoring["enabled"]:
            return events
            
        # Build list of files to watch
        files_to_check = set()
        
        for dir_name in monitoring["watched_directories"]:
            watch_dir = self.vault_path / dir_name
            if watch_dir.exists():
                for pattern in monitoring["watched_file_patterns"]:
                    files_to_check.update(watch_dir.rglob(pattern))
                    
        # Check each file
        for file_path in files_to_check:
            # Skip ignored patterns
            if self.should_ignore_file(file_path):
                continue
                
            try:
                stat = file_path.stat()
                current_checksum = self.calculate_file_checksum(file_path)
                relative_path = str(file_path.relative_to(self.vault_path))
                
                # Check if file is new or changed
                if relative_path not in self.file_checksums:
                    # New file
                    event = self.create_event(
                        event_type="file_created",
                        file_path=relative_path,
                        description=f"New file created: {file_path.name}",
                        severity="medium",
                        metadata={
                            "file_size": stat.st_size,
                            "file_type": file_path.suffix
                        }
                    )
                    events.append(event)
                    
                else:
                    # Check for changes
                    old_state = self.file_checksums[relative_path]
                    
                    if (current_checksum != old_state["checksum"] or
                        stat.st_size != old_state["size"] or
                        stat.st_mtime != old_state["modified_time"]):
                        
                        # File modified
                        change_severity = self.calculate_change_severity(
                            file_path, old_state, {"checksum": current_checksum, "size": stat.st_size}
                        )
                        
                        event = self.create_event(
                            event_type="file_modified",
                            file_path=relative_path,
                            description=f"File modified: {file_path.name}",
                            severity=change_severity,
                            metadata={
                                "old_size": old_state["size"],
                                "new_size": stat.st_size,
                                "size_change": stat.st_size - old_state["size"],
                                "file_type": file_path.suffix
                            }
                        )
                        events.append(event)
                        
                # Update file state
                self.file_checksums[relative_path] = {
                    "checksum": current_checksum,
                    "size": stat.st_size,
                    "modified_time": stat.st_mtime
                }
                
                # Update database
                self.update_file_state(relative_path, current_checksum, stat.st_size, stat.st_mtime)
                
            except Exception as e:
                print(f"Error checking file {file_path}: {e}")
                
        # Check for deleted files
        for tracked_path in list(self.file_checksums.keys()):
            full_path = self.vault_path / tracked_path
            if not full_path.exists():
                event = self.create_event(
                    event_type="file_deleted",
                    file_path=tracked_path,
                    description=f"File deleted: {Path(tracked_path).name}",
                    severity="medium"
                )
                events.append(event)
                
                # Remove from tracking
                del self.file_checksums[tracked_path]
                self.remove_file_state(tracked_path)
                
        return events
        
    def should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored based on patterns."""
        import fnmatch
        
        file_str = str(file_path)
        relative_path = str(file_path.relative_to(self.vault_path))
        
        for pattern in self.config["monitoring"]["ignore_patterns"]:
            if (fnmatch.fnmatch(file_str, pattern) or 
                fnmatch.fnmatch(relative_path, pattern)):
                return True
                
        return False
        
    def calculate_change_severity(self, file_path: Path, old_state: Dict, new_state: Dict) -> str:
        """Calculate severity of file change."""
        size_change_ratio = abs(new_state["size"] - old_state["size"]) / max(old_state["size"], 1)
        
        # Major size change
        if size_change_ratio > 0.5:
            return "high"
        elif size_change_ratio > 0.2:
            return "medium"
            
        # Check if it's an important file type
        if file_path.suffix == ".md":
            # Check content change for markdown files
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Look for indicators of major changes
                major_indicators = [
                    "status: complete", "status: archived",
                    "# IMPORTANT", "# CRITICAL", "# BREAKING",
                    "faction:", "world:", "type:"
                ]
                
                if any(indicator.lower() in content.lower() for indicator in major_indicators):
                    return "high"
                    
            except Exception:
                pass
                
        return "low"
        
    def create_event(self, event_type: str, file_path: str, description: str, 
                    severity: str, metadata: Dict = None) -> UpdateEvent:
        """Create a new update event."""
        event_id = f"{event_type}_{hashlib.md5(f'{file_path}_{datetime.now().isoformat()}'.encode()).hexdigest()[:8]}"
        
        event = UpdateEvent(
            event_id=event_id,
            event_type=event_type,
            file_path=file_path,
            description=description,
            severity=severity,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        # Store in database
        self.store_event(event)
        
        # Add to queue for processing
        self.event_queue.append(event)
        
        return event
        
    def store_event(self, event: UpdateEvent):
        """Store event in database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO events 
                (event_id, event_type, file_path, description, severity, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event.event_id, event.event_type, event.file_path,
                event.description, event.severity, event.timestamp.isoformat(),
                json.dumps(event.metadata)
            ))
            
    def update_file_state(self, file_path: str, checksum: str, size: int, modified_time: float):
        """Update file state in database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO file_states
                (file_path, checksum, size, modified_time)
                VALUES (?, ?, ?, ?)
            """, (file_path, checksum, size, modified_time))
            
    def remove_file_state(self, file_path: str):
        """Remove file state from database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM file_states WHERE file_path = ?", (file_path,))
            
    def process_events(self, events: List[UpdateEvent]):
        """Process events against notification rules."""
        for event in events:
            # Check each rule
            for rule_config in self.config["notification_rules"]:
                if not rule_config["enabled"]:
                    continue
                    
                if self.event_matches_rule(event, rule_config):
                    self.trigger_rule_actions(event, rule_config)
                    
    def event_matches_rule(self, event: UpdateEvent, rule: Dict) -> bool:
        """Check if event matches a notification rule."""
        conditions = rule["conditions"]
        
        # Check event type
        if "event_type" in conditions:
            if event.event_type != conditions["event_type"]:
                return False
                
        # Check file types
        if "file_types" in conditions:
            file_ext = Path(event.file_path).suffix.lstrip('.')
            if file_ext not in conditions["file_types"]:
                return False
                
        # Check directories
        if "directories" in conditions:
            file_dir = str(Path(event.file_path).parent)
            if not any(file_dir.startswith(dir_path) for dir_path in conditions["directories"]):
                return False
                
        # Check severity
        if "min_severity" in conditions:
            severity_levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
            event_level = severity_levels.get(event.severity, 1)
            min_level = severity_levels.get(conditions["min_severity"], 1)
            if event_level < min_level:
                return False
                
        # Check change threshold for file modifications
        if "change_threshold" in conditions and "size_change" in event.metadata:
            old_size = event.metadata.get("old_size", 0)
            change_ratio = abs(event.metadata["size_change"]) / max(old_size, 1)
            if change_ratio < conditions["change_threshold"]:
                return False
                
        return True
        
    def trigger_rule_actions(self, event: UpdateEvent, rule: Dict):
        """Trigger actions for a matched rule."""
        for action in rule["actions"]:
            frequency = rule["frequency"]
            
            if frequency == "immediate":
                self.execute_action(action, event, rule)
            else:
                # Add to pending notifications for digest
                self.pending_notifications[frequency].append({
                    "event": event,
                    "rule": rule,
                    "action": action
                })
                
    def execute_action(self, action: str, event: UpdateEvent, rule: Dict):
        """Execute a notification action."""
        if action == "email":
            self.send_email_notification(event, rule)
        elif action == "webhook":
            self.send_webhook_notification(event, rule)
        elif action == "file":
            self.write_file_notification(event, rule)
        elif action == "digest":
            # Digest notifications are handled separately
            pass
        else:
            print(f"Unknown action: {action}")
            
    def send_email_notification(self, event: UpdateEvent, rule: Dict):
        """Send email notification."""
        email_channel = next((ch for ch in self.config["notification_channels"] 
                            if ch["channel_type"] == "email" and ch["enabled"]), None)
        
        if not email_channel:
            print("Email channel not configured or disabled")
            return
            
        config = email_channel["config"]
        
        try:
            # Create message
            msg = MimeMultipart()
            msg['From'] = config["from_address"]
            msg['To'] = ", ".join(config["to_addresses"])
            msg['Subject'] = f"Vault Update: {rule['name']}"
            
            # Create email body
            body = f"""
Vault Update Notification

Rule: {rule['name']}
Event: {event.description}
File: {event.file_path}
Severity: {event.severity.upper()}
Time: {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

Details:
{json.dumps(event.metadata, indent=2)}

---
This is an automated notification from your TTRPG Vault.
            """.strip()
            
            msg.attach(MimeText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
            server.starttls()
            server.login(config["username"], config["password"])
            
            text = msg.as_string()
            server.sendmail(config["from_address"], config["to_addresses"], text)
            server.quit()
            
            self.log_notification_sent(event.event_id, email_channel["channel_id"], "success")
            print(f"Email sent for event: {event.event_id}")
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            self.log_notification_sent(event.event_id, email_channel["channel_id"], f"failed: {e}")
            
    def send_webhook_notification(self, event: UpdateEvent, rule: Dict):
        """Send webhook notification."""
        webhook_channel = next((ch for ch in self.config["notification_channels"] 
                              if ch["channel_type"] == "webhook" and ch["enabled"]), None)
        
        if not webhook_channel:
            print("Webhook channel not configured or disabled")
            return
            
        try:
            import requests
            
            config = webhook_channel["config"]
            
            payload = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "file_path": event.file_path,
                "description": event.description,
                "severity": event.severity,
                "timestamp": event.timestamp.isoformat(),
                "metadata": event.metadata,
                "rule_name": rule["name"]
            }
            
            response = requests.post(
                config["url"],
                json=payload,
                headers=config.get("headers", {}),
                timeout=30
            )
            
            if response.status_code == 200:
                self.log_notification_sent(event.event_id, webhook_channel["channel_id"], "success")
                print(f"Webhook sent for event: {event.event_id}")
            else:
                self.log_notification_sent(event.event_id, webhook_channel["channel_id"], 
                                        f"failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"Failed to send webhook: {e}")
            self.log_notification_sent(event.event_id, webhook_channel["channel_id"], f"failed: {e}")
            
    def write_file_notification(self, event: UpdateEvent, rule: Dict):
        """Write notification to file."""
        file_channel = next((ch for ch in self.config["notification_channels"] 
                           if ch["channel_type"] == "file" and ch["enabled"]), None)
        
        if not file_channel:
            return
            
        config = file_channel["config"]
        output_path = self.vault_path / config["file_path"]
        
        try:
            # Append notification to file
            timestamp_str = event.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            if config["format"] == "markdown":
                notification = f"""
## {event.description}
- **Time**: {timestamp_str}
- **File**: `{event.file_path}`
- **Severity**: {event.severity.upper()}
- **Rule**: {rule['name']}

"""
            else:
                notification = f"[{timestamp_str}] {event.severity.upper()}: {event.description} ({event.file_path})\n"
                
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(notification)
                
            self.log_notification_sent(event.event_id, file_channel["channel_id"], "success")
            
        except Exception as e:
            print(f"Failed to write file notification: {e}")
            self.log_notification_sent(event.event_id, file_channel["channel_id"], f"failed: {e}")
            
    def log_notification_sent(self, event_id: str, channel_id: str, status: str):
        """Log that a notification was sent."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO notifications_sent (event_id, channel_id, status)
                VALUES (?, ?, ?)
            """, (event_id, channel_id, status))
            
    def generate_digest(self, digest_type: str) -> str:
        """Generate digest of recent events."""
        now = datetime.now()
        
        if digest_type == "daily":
            since = now - timedelta(days=1)
            title = "Daily Vault Update Digest"
        elif digest_type == "weekly":
            since = now - timedelta(days=7)
            title = "Weekly Vault Update Digest"
        elif digest_type == "hourly":
            since = now - timedelta(hours=1)
            title = "Hourly Vault Update Digest"
        else:
            since = now - timedelta(days=1)
            title = "Vault Update Digest"
            
        # Get recent events
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT event_type, file_path, description, severity, timestamp, metadata
                FROM events 
                WHERE timestamp >= ? 
                ORDER BY timestamp DESC
                LIMIT 50
            """, (since.isoformat(),))
            
            events = []
            for row in cursor.fetchall():
                event_type, file_path, description, severity, timestamp, metadata = row
                events.append({
                    "event_type": event_type,
                    "file_path": file_path,
                    "description": description,
                    "severity": severity,
                    "timestamp": timestamp,
                    "metadata": json.loads(metadata or "{}")
                })
                
        if not events:
            return f"# {title}\n\nNo updates during this period."
            
        # Generate digest content
        lines = [
            f"# {title}",
            f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Period: {since.strftime('%Y-%m-%d %H:%M')} to {now.strftime('%Y-%m-%d %H:%M')}",
            f"Total Events: {len(events)}",
            ""
        ]
        
        # Group events by type
        by_type = defaultdict(list)
        by_severity = defaultdict(list)
        
        for event in events:
            by_type[event["event_type"]].append(event)
            by_severity[event["severity"]].append(event)
            
        # Summary statistics
        lines.extend([
            "## Summary",
            ""
        ])
        
        for event_type, type_events in sorted(by_type.items()):
            lines.append(f"- **{event_type.replace('_', ' ').title()}**: {len(type_events)}")
            
        lines.extend([
            "",
            "### By Severity",
            ""
        ])
        
        for severity in ["critical", "high", "medium", "low"]:
            if severity in by_severity:
                lines.append(f"- **{severity.upper()}**: {len(by_severity[severity])}")
                
        # Recent events
        lines.extend([
            "",
            "## Recent Events",
            ""
        ])
        
        for event in events[:20]:  # Show top 20
            timestamp = datetime.fromisoformat(event["timestamp"])
            lines.append(f"### {event['description']}")
            lines.append(f"- **Time**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"- **File**: `{event['file_path']}`")
            lines.append(f"- **Severity**: {event['severity'].upper()}")
            
            if event["metadata"]:
                lines.append(f"- **Details**: {event['metadata']}")
                
            lines.append("")
            
        # File activity summary
        file_activity = defaultdict(int)
        for event in events:
            file_activity[event["file_path"]] += 1
            
        if file_activity:
            lines.extend([
                "## Most Active Files",
                ""
            ])
            
            for file_path, count in sorted(file_activity.items(), key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"- `{file_path}`: {count} events")
                
        return '\n'.join(lines)
        
    def send_digest(self, digest_type: str):
        """Send digest notification."""
        digest_content = self.generate_digest(digest_type)
        
        # Create digest event
        digest_event = UpdateEvent(
            event_id=f"digest_{digest_type}_{datetime.now().strftime('%Y%m%d_%H%M')}",
            event_type="digest",
            file_path="system",
            description=f"{digest_type.title()} digest generated",
            severity="low",
            timestamp=datetime.now(),
            metadata={"digest_type": digest_type, "content": digest_content}
        )
        
        # Send via enabled channels
        for channel in self.config["notification_channels"]:
            if not channel["enabled"]:
                continue
                
            if channel["channel_type"] == "email":
                self.send_digest_email(digest_content, digest_type, channel)
            elif channel["channel_type"] == "file":
                self.write_digest_file(digest_content, digest_type, channel)
                
        # Log digest generation
        with sqlite3.connect(self.db_path) as conn:
            content_hash = hashlib.md5(digest_content.encode()).hexdigest()
            conn.execute("""
                INSERT INTO digest_history (digest_type, event_count, content_hash)
                VALUES (?, ?, ?)
            """, (digest_type, digest_content.count('\n'), content_hash))
            
    def send_digest_email(self, content: str, digest_type: str, channel: Dict):
        """Send digest via email."""
        try:
            config = channel["config"]
            
            msg = MimeMultipart()
            msg['From'] = config["from_address"]
            msg['To'] = ", ".join(config["to_addresses"])
            msg['Subject'] = f"Vault {digest_type.title()} Digest - {datetime.now().strftime('%Y-%m-%d')}"
            
            msg.attach(MimeText(content, 'plain'))
            
            server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
            server.starttls()
            server.login(config["username"], config["password"])
            
            text = msg.as_string()
            server.sendmail(config["from_address"], config["to_addresses"], text)
            server.quit()
            
            print(f"{digest_type.title()} digest sent via email")
            
        except Exception as e:
            print(f"Failed to send digest email: {e}")
            
    def write_digest_file(self, content: str, digest_type: str, channel: Dict):
        """Write digest to file."""
        try:
            config = channel["config"]
            
            # Create digest-specific filename
            timestamp = datetime.now().strftime('%Y%m%d')
            digest_filename = f"{digest_type}_digest_{timestamp}.md"
            output_path = self.vault_path / digest_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"{digest_type.title()} digest written to {output_path}")
            
        except Exception as e:
            print(f"Failed to write digest file: {e}")
            
    def run_monitoring_loop(self):
        """Main monitoring loop."""
        print("Starting vault monitoring...")
        
        scan_interval = self.config["monitoring"]["scan_interval_seconds"]
        last_daily_digest = datetime.now().date() - timedelta(days=1)
        last_weekly_digest = datetime.now().date() - timedelta(days=7)
        
        while True:
            try:
                # Scan for changes
                events = self.scan_for_changes()
                
                if events:
                    print(f"Detected {len(events)} events")
                    self.process_events(events)
                    
                # Check if it's time for digests
                now = datetime.now()
                today = now.date()
                
                # Daily digest
                if (today > last_daily_digest and 
                    now.hour >= self.config["digest_settings"]["daily_digest_hour"]):
                    print("Generating daily digest...")
                    self.send_digest("daily")
                    last_daily_digest = today
                    
                # Weekly digest
                if (today.weekday() == self.config["digest_settings"]["weekly_digest_day"] and
                    today > last_weekly_digest and
                    now.hour >= self.config["digest_settings"]["daily_digest_hour"]):
                    print("Generating weekly digest...")
                    self.send_digest("weekly")
                    last_weekly_digest = today
                    
                # Process pending notifications
                self.process_pending_notifications()
                
                time.sleep(scan_interval)
                
            except KeyboardInterrupt:
                print("Monitoring stopped")
                break
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(scan_interval)
                
    def process_pending_notifications(self):
        """Process pending digest notifications."""
        now = datetime.now()
        
        for frequency, notifications in self.pending_notifications.items():
            if not notifications:
                continue
                
            send_digest = False
            
            if frequency == "hourly":
                send_digest = True  # Send every hour
            elif frequency == "daily":
                if frequency not in self.last_digest_time:
                    send_digest = True
                else:
                    last_sent = self.last_digest_time[frequency]
                    if (now - last_sent).days >= 1:
                        send_digest = True
            elif frequency == "weekly":
                if frequency not in self.last_digest_time:
                    send_digest = True
                else:
                    last_sent = self.last_digest_time[frequency]
                    if (now - last_sent).days >= 7:
                        send_digest = True
                        
            if send_digest:
                print(f"Sending {frequency} digest with {len(notifications)} notifications")
                # Generate digest for pending notifications
                # This is a simplified version - could be expanded
                self.send_digest(frequency)
                self.last_digest_time[frequency] = now
                notifications.clear()

def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Update Notification System")
    parser.add_argument("--vault-path", default=".", help="Path to vault root")
    parser.add_argument("--scan-once", action="store_true", help="Scan once and exit")
    parser.add_argument("--generate-digest", choices=["hourly", "daily", "weekly"], 
                       help="Generate specific digest")
    parser.add_argument("--test-notification", action="store_true", help="Send test notification")
    
    args = parser.parse_args()
    
    notification_system = UpdateNotificationSystem(args.vault_path)
    
    if args.scan_once:
        events = notification_system.scan_for_changes()
        print(f"Found {len(events)} events")
        
        for event in events:
            print(f"  {event.event_type}: {event.description} ({event.severity})")
            
        if events:
            notification_system.process_events(events)
            
    elif args.generate_digest:
        digest_content = notification_system.generate_digest(args.generate_digest)
        print(digest_content)
        
    elif args.test_notification:
        test_event = UpdateEvent(
            event_id="test_001",
            event_type="test",
            file_path="test_file.md",
            description="Test notification",
            severity="medium",
            timestamp=datetime.now(),
            metadata={"test": True}
        )
        
        # Test each enabled channel
        for channel in notification_system.config["notification_channels"]:
            if channel["enabled"]:
                print(f"Testing {channel['channel_type']} channel...")
                if channel["channel_type"] == "file":
                    notification_system.write_file_notification(test_event, {"name": "Test Rule"})
                    
    else:
        # Run monitoring loop
        notification_system.run_monitoring_loop()

if __name__ == "__main__":
    main()