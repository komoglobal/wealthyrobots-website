#!/usr/bin/env python3
"""
Automated Backup System - WealthyRobot Empire
Creates comprehensive backups of system data, configurations, and logs
"""

import os
import json
import shutil
import gzip
import tarfile
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import threading
import time
import logging

class BackupType(Enum):
    FULL_SYSTEM = "full_system"
    CONFIGURATION = "configuration"
    LOGS = "logs"
    PERFORMANCE_DATA = "performance_data"
    WEBSITE_CONTENT = "website_content"
    AGENT_DATA = "agent_data"
    CUSTOM = "custom"

class BackupStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    IN_PROGRESS = "in_progress"

@dataclass
class BackupItem:
    """Represents a single backup item"""
    path: str
    backup_type: BackupType
    include_pattern: Optional[List[str]] = None
    exclude_pattern: Optional[List[str]] = None
    compression: bool = True

@dataclass
class BackupResult:
    """Result of a backup operation"""
    backup_id: str
    backup_type: BackupType
    status: BackupStatus
    timestamp: datetime
    file_path: str
    file_size: int
    items_backed_up: int
    error_message: Optional[str] = None
    checksum: Optional[str] = None

class AutomatedBackup:
    """Automated backup system for WealthyRobot"""

    def __init__(self):
        self.backup_dir = "backups"
        self.max_backups_per_type = 10
        self.compression_level = 6
        self.backup_schedule = {}

        # Setup backup directory structure
        self._setup_backup_directories()

        # Default backup items
        self.backup_items = self._get_default_backup_items()

        # Setup logging
        self.logger = logging.getLogger('AutomatedBackup')

    def _setup_backup_directories(self):
        """Setup backup directory structure"""
        directories = [
            self.backup_dir,
            os.path.join(self.backup_dir, "full_system"),
            os.path.join(self.backup_dir, "configuration"),
            os.path.join(self.backup_dir, "logs"),
            os.path.join(self.backup_dir, "performance_data"),
            os.path.join(self.backup_dir, "website_content"),
            os.path.join(self.backup_dir, "agent_data"),
            os.path.join(self.backup_dir, "archives")
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

        print(f"✅ Backup directories created in: {self.backup_dir}")

    def _get_default_backup_items(self) -> List[BackupItem]:
        """Get default backup items"""
        return [
            # Configuration files
            BackupItem(
                path="*.json",
                backup_type=BackupType.CONFIGURATION,
                include_pattern=["*.json"],
                exclude_pattern=["*backup*", "*temp*"]
            ),

            # Python agents and modules
            BackupItem(
                path="*.py",
                backup_type=BackupType.AGENT_DATA,
                include_pattern=["*agent*.py", "*system*.py", "*coordinator*.py"],
                exclude_pattern=["*__pycache__*", "*.pyc"]
            ),

            # Website content
            BackupItem(
                path="wealthyrobots_website",
                backup_type=BackupType.WEBSITE_CONTENT,
                exclude_pattern=["*__pycache__*", "*.log"]
            ),

            # Log files
            BackupItem(
                path="logs",
                backup_type=BackupType.LOGS,
                include_pattern=["*.log"],
                exclude_pattern=[]
            ),

            # Performance data
            BackupItem(
                path="performance_metrics.json",
                backup_type=BackupType.PERFORMANCE_DATA
            )
        ]

    def create_backup(self, backup_type: BackupType, custom_items: List[BackupItem] = None,
                     description: str = "") -> BackupResult:
        """Create a backup of specified type"""

        backup_id = f"{backup_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        timestamp = datetime.now()

        print(f"🔄 Starting backup: {backup_id}")
        print(f"📁 Backup type: {backup_type.value}")

        try:
            # Determine backup items
            if custom_items:
                items_to_backup = custom_items
            else:
                items_to_backup = [item for item in self.backup_items if item.backup_type == backup_type]

            if not items_to_backup:
                return BackupResult(
                    backup_id=backup_id,
                    backup_type=backup_type,
                    status=BackupStatus.FAILED,
                    timestamp=timestamp,
                    file_path="",
                    file_size=0,
                    items_backed_up=0,
                    error_message="No backup items found for this type"
                )

            # Create backup archive
            archive_path = self._create_backup_archive(backup_id, backup_type, items_to_backup, description)

            if archive_path and os.path.exists(archive_path):
                # Calculate checksum
                checksum = self._calculate_checksum(archive_path)
                file_size = os.path.getsize(archive_path)

                # Create backup metadata
                self._create_backup_metadata(backup_id, backup_type, archive_path, items_to_backup, description)

                # Cleanup old backups
                self._cleanup_old_backups(backup_type)

                result = BackupResult(
                    backup_id=backup_id,
                    backup_type=backup_type,
                    status=BackupStatus.SUCCESS,
                    timestamp=timestamp,
                    file_path=archive_path,
                    file_size=file_size,
                    items_backed_up=len(items_to_backup),
                    checksum=checksum
                )

                print(f"✅ Backup completed successfully: {archive_path}")
                print(f"📊 File size: {file_size / (1024*1024):.2f} MB")

                return result
            else:
                return BackupResult(
                    backup_id=backup_id,
                    backup_type=backup_type,
                    status=BackupStatus.FAILED,
                    timestamp=timestamp,
                    file_path="",
                    file_size=0,
                    items_backed_up=0,
                    error_message="Failed to create backup archive"
                )

        except Exception as e:
            error_msg = f"Backup failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.logger.error(error_msg, exc_info=True)

            return BackupResult(
                backup_id=backup_id,
                backup_type=backup_type,
                status=BackupStatus.FAILED,
                timestamp=timestamp,
                file_path="",
                file_size=0,
                items_backed_up=0,
                error_message=str(e)
            )

    def _create_backup_archive(self, backup_id: str, backup_type: BackupType,
                              items: List[BackupItem], description: str) -> Optional[str]:
        """Create the actual backup archive"""

        # Determine archive path
        type_dir = os.path.join(self.backup_dir, backup_type.value)
        archive_name = f"{backup_id}.tar.gz"
        archive_path = os.path.join(type_dir, archive_name)

        try:
            with tarfile.open(archive_path, "w:gz", compresslevel=self.compression_level) as tar:
                files_added = 0

                for item in items:
                    if os.path.exists(item.path):
                        if os.path.isfile(item.path):
                            # Single file
                            tar.add(item.path, arcname=os.path.basename(item.path))
                            files_added += 1
                        elif os.path.isdir(item.path):
                            # Directory - add with filtering
                            for root, dirs, files in os.walk(item.path):
                                # Apply exclude patterns
                                if item.exclude_pattern:
                                    dirs[:] = [d for d in dirs if not self._matches_pattern(d, item.exclude_pattern)]

                                for file in files:
                                    # Apply include patterns
                                    if item.include_pattern and not self._matches_pattern(file, item.include_pattern):
                                        continue

                                    # Apply exclude patterns
                                    if item.exclude_pattern and self._matches_pattern(file, item.exclude_pattern):
                                        continue

                                    file_path = os.path.join(root, file)
                                    arcname = os.path.relpath(file_path, item.path)
                                    tar.add(file_path, arcname=arcname)
                                    files_added += 1

                # Add backup metadata
                metadata = {
                    "backup_id": backup_id,
                    "backup_type": backup_type.value,
                    "timestamp": datetime.now().isoformat(),
                    "description": description,
                    "items": [
                        {
                            "path": item.path,
                            "type": item.backup_type.value,
                            "compression": item.compression
                        }
                        for item in items
                    ],
                    "files_added": files_added
                }

                # Write metadata to temporary file and add to archive
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    json.dump(metadata, f, indent=2)
                    temp_metadata_path = f.name

                try:
                    tar.add(temp_metadata_path, arcname="backup_metadata.json")
                finally:
                    os.unlink(temp_metadata_path)

                return archive_path if files_added > 0 else None

        except Exception as e:
            print(f"❌ Error creating backup archive: {e}")
            if os.path.exists(archive_path):
                os.remove(archive_path)
            return None

    def _matches_pattern(self, name: str, patterns: List[str]) -> bool:
        """Check if name matches any pattern"""
        import fnmatch
        return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)

    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA256 checksum of file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def _create_backup_metadata(self, backup_id: str, backup_type: BackupType,
                               archive_path: str, items: List[BackupItem], description: str):
        """Create backup metadata file"""
        metadata = {
            "backup_id": backup_id,
            "backup_type": backup_type.value,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "archive_path": archive_path,
            "archive_size": os.path.getsize(archive_path),
            "items_backed_up": len(items),
            "checksum": self._calculate_checksum(archive_path)
        }

        metadata_path = os.path.join(self.backup_dir, f"{backup_id}_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _cleanup_old_backups(self, backup_type: BackupType):
        """Clean up old backups, keeping only the most recent ones"""
        type_dir = os.path.join(self.backup_dir, backup_type.value)

        if not os.path.exists(type_dir):
            return

        # Get all backup files
        backup_files = []
        for file in os.listdir(type_dir):
            if file.endswith('.tar.gz'):
                file_path = os.path.join(type_dir, file)
                mtime = os.path.getmtime(file_path)
                backup_files.append((file_path, mtime))

        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)

        # Remove old backups
        if len(backup_files) > self.max_backups_per_type:
            for file_path, _ in backup_files[self.max_backups_per_type:]:
                try:
                    os.remove(file_path)
                    print(f"🗑️ Removed old backup: {os.path.basename(file_path)}")

                    # Also remove corresponding metadata file
                    metadata_path = file_path.replace('.tar.gz', '_metadata.json')
                    if os.path.exists(metadata_path):
                        os.remove(metadata_path)

                except Exception as e:
                    print(f"⚠️ Error removing old backup {file_path}: {e}")

    def restore_backup(self, backup_id: str, restore_path: str = None) -> bool:
        """Restore from a backup"""
        print(f"🔄 Starting restore: {backup_id}")

        if restore_path is None:
            restore_path = f"restore_{backup_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            # Find backup archive
            backup_path = None
            for backup_type in BackupType:
                type_dir = os.path.join(self.backup_dir, backup_type.value)
                if os.path.exists(type_dir):
                    for file in os.listdir(type_dir):
                        if file.startswith(backup_id) and file.endswith('.tar.gz'):
                            backup_path = os.path.join(type_dir, file)
                            break
                    if backup_path:
                        break

            if not backup_path:
                print(f"❌ Backup not found: {backup_id}")
                return False

            # Create restore directory
            os.makedirs(restore_path, exist_ok=True)

            # Extract backup
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(restore_path)

            print(f"✅ Restore completed: {restore_path}")
            return True

        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False

    def list_backups(self, backup_type: BackupType = None) -> List[Dict[str, Any]]:
        """List available backups"""
        backups = []

        types_to_check = [backup_type] if backup_type else list(BackupType)

        for btype in types_to_check:
            type_dir = os.path.join(self.backup_dir, btype.value)
            if not os.path.exists(type_dir):
                continue

            for file in os.listdir(type_dir):
                if file.endswith('_metadata.json'):
                    metadata_path = os.path.join(type_dir, file)
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                            backups.append(metadata)
                    except Exception as e:
                        print(f"⚠️ Error reading backup metadata {metadata_path}: {e}")

        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return backups

    def get_backup_stats(self) -> Dict[str, Any]:
        """Get backup system statistics"""
        stats = {
            "total_backups": 0,
            "backups_by_type": {},
            "total_size": 0,
            "oldest_backup": None,
            "newest_backup": None,
            "timestamp": datetime.now().isoformat()
        }

        for backup_type in BackupType:
            type_dir = os.path.join(self.backup_dir, backup_type.value)
            if not os.path.exists(type_dir):
                continue

            type_backups = []
            type_size = 0

            for file in os.listdir(type_dir):
                if file.endswith('.tar.gz'):
                    file_path = os.path.join(type_dir, file)
                    file_size = os.path.getsize(file_path)
                    mtime = os.path.getmtime(file_path)

                    type_backups.append({
                        "name": file,
                        "size": file_size,
                        "timestamp": datetime.fromtimestamp(mtime).isoformat()
                    })
                    type_size += file_size

            if type_backups:
                stats["backups_by_type"][backup_type.value] = {
                    "count": len(type_backups),
                    "total_size": type_size,
                    "total_size_mb": round(type_size / (1024 * 1024), 2)
                }
                stats["total_backups"] += len(type_backups)
                stats["total_size"] += type_size

                # Track oldest and newest
                timestamps = [b["timestamp"] for b in type_backups]
                if not stats["oldest_backup"] or min(timestamps) < stats["oldest_backup"]:
                    stats["oldest_backup"] = min(timestamps)
                if not stats["newest_backup"] or max(timestamps) > stats["newest_backup"]:
                    stats["newest_backup"] = max(timestamps)

        return stats

    def schedule_backup(self, backup_type: BackupType, interval_hours: int, description: str = ""):
        """Schedule a recurring backup"""
        def backup_worker():
            while True:
                try:
                    result = self.create_backup(backup_type, description=description)
                    if result.status == BackupStatus.SUCCESS:
                        print(f"✅ Scheduled backup completed: {result.backup_id}")
                    else:
                        print(f"❌ Scheduled backup failed: {result.error_message}")
                except Exception as e:
                    print(f"❌ Scheduled backup error: {e}")

                time.sleep(interval_hours * 3600)

        thread = threading.Thread(target=backup_worker, daemon=True)
        thread.start()

        schedule_key = f"{backup_type.value}_{interval_hours}h"
        self.backup_schedule[schedule_key] = {
            "type": backup_type,
            "interval": interval_hours,
            "description": description,
            "thread": thread
        }

        print(f"✅ Scheduled {backup_type.value} backup every {interval_hours} hours")

# Global backup system instance
backup_system = AutomatedBackup()

# Convenience functions
def create_full_backup(description: str = ""):
    """Create a full system backup"""
    return backup_system.create_backup(BackupType.FULL_SYSTEM, description=description)

def create_config_backup(description: str = ""):
    """Create a configuration backup"""
    return backup_system.create_backup(BackupType.CONFIGURATION, description=description)

def create_logs_backup(description: str = ""):
    """Create a logs backup"""
    return backup_system.create_backup(BackupType.LOGS, description=description)

def list_available_backups(backup_type: BackupType = None):
    """List available backups"""
    return backup_system.list_backups(backup_type)

def restore_from_backup(backup_id: str, restore_path: str = None):
    """Restore from a specific backup"""
    return backup_system.restore_backup(backup_id, restore_path)

if __name__ == "__main__":
    # Test the backup system
    print("🧪 Testing Automated Backup System")
    print("=" * 40)

    # Create different types of backups
    backup_types = [
        (BackupType.CONFIGURATION, "Test configuration backup"),
        (BackupType.LOGS, "Test logs backup"),
        (BackupType.PERFORMANCE_DATA, "Test performance data backup")
    ]

    for backup_type, description in backup_types:
        print(f"\n📦 Creating {backup_type.value} backup...")
        result = backup_system.create_backup(backup_type, description=description)

        if result.status == BackupStatus.SUCCESS:
            print(f"✅ {backup_type.value} backup successful")
            print(f"   File: {result.file_path}")
            print(f"   Size: {result.file_size / (1024*1024):.2f} MB")
            print(f"   Items: {result.items_backed_up}")
        else:
            print(f"❌ {backup_type.value} backup failed: {result.error_message}")

    # List backups
    print("\n📋 Available backups:")
    backups = backup_system.list_backups()
    for backup in backups[:5]:  # Show first 5
        print(f"   {backup['backup_id']} - {backup['backup_type']} ({backup['timestamp']})")

    # Get backup statistics
    stats = backup_system.get_backup_stats()
    print("\n📊 Backup Statistics:")
    print(f"   Total backups: {stats['total_backups']}")
    print(f"   Total size: {stats['total_size'] / (1024*1024):.2f} MB")
    print(f"   By type: {stats['backups_by_type']}")

    print("\n✅ Automated backup system test complete!")
