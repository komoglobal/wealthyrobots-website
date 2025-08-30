#!/usr/bin/env python3
"""
Data Management System for WealthyRobot Trading Platform
Handles market data snapshots, cleanup, archiving, and optimization
"""

import os
import json
import shutil
import gzip
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional
import threading
import schedule

class DataManager:
    def __init__(self, base_dir: str = "/home/ubuntu/wealthyrobot"):
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "market_data"
        self.archive_dir = self.data_dir / "archive"
        self.current_dir = self.data_dir / "current"
        self.logs_dir = self.base_dir / "logs"
        
        # Create necessary directories
        self._create_directories()
        
        # Configure logging
        self._setup_logging()
        
        # Data retention policies
        self.retention_policies = {
            "current": timedelta(hours=24),  # Keep current data for 24 hours
            "hourly": timedelta(days=7),     # Keep hourly snapshots for 7 days
            "daily": timedelta(days=30),     # Keep daily snapshots for 30 days
            "monthly": timedelta(days=365)   # Keep monthly snapshots for 1 year
        }
        
        # Start background cleanup thread
        self._start_cleanup_thread()
    
    def _create_directories(self):
        """Create necessary directory structure"""
        directories = [
            self.data_dir,
            self.archive_dir,
            self.current_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = self.logs_dir / "data_manager.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def organize_existing_files(self):
        """Organize existing market data snapshots into proper structure"""
        self.logger.info("Starting organization of existing market data files...")
        
        # Find all market data snapshot files
        snapshot_files = list(self.base_dir.glob("market_data_snapshot_*.json"))
        self.logger.info(f"Found {len(snapshot_files)} snapshot files to organize")
        
        if not snapshot_files:
            self.logger.info("No existing snapshot files found")
            return
        
        # Group files by date
        files_by_date = {}
        for file_path in snapshot_files:
            try:
                # Extract date from filename
                date_str = file_path.stem.split('_')[-2]  # Get date part
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                date_key = date_obj.strftime("%Y-%m-%d")
                
                if date_key not in files_by_date:
                    files_by_date[date_key] = []
                files_by_date[date_key].append(file_path)
            except Exception as e:
                self.logger.warning(f"Could not parse date from {file_path}: {e}")
                continue
        
        # Move files to appropriate directories
        moved_count = 0
        for date_key, files in files_by_date.items():
            date_dir = self.archive_dir / date_key
            date_dir.mkdir(exist_ok=True)
            
            for file_path in files:
                try:
                    # Compress and move file
                    compressed_path = date_dir / f"{file_path.stem}.json.gz"
                    self._compress_file(file_path, compressed_path)
                    
                    # Remove original file
                    file_path.unlink()
                    moved_count += 1
                    
                    if moved_count % 1000 == 0:
                        self.logger.info(f"Processed {moved_count} files...")
                        
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {e}")
        
        self.logger.info(f"Successfully organized {moved_count} files")
    
    def _compress_file(self, source_path: Path, target_path: Path):
        """Compress a JSON file using gzip"""
        with open(source_path, 'rb') as source:
            with gzip.open(target_path, 'wb') as target:
                shutil.copyfileobj(source, target)
    
    def save_market_data(self, data: Dict, snapshot_type: str = "current"):
        """Save market data with proper organization"""
        timestamp = datetime.now()
        
        if snapshot_type == "current":
            # Save to current directory (overwrite previous)
            file_path = self.current_dir / "current_market_data.json"
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Also save timestamped version for hourly archiving
            hourly_file = self.current_dir / f"hourly_{timestamp.strftime('%Y%m%d_%H')}.json"
            with open(hourly_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        elif snapshot_type == "daily":
            # Save daily snapshot to archive
            date_dir = self.archive_dir / timestamp.strftime("%Y-%m-%d")
            date_dir.mkdir(exist_ok=True)
            
            file_path = date_dir / f"daily_{timestamp.strftime('%Y%m%d')}.json"
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
    
    def cleanup_old_data(self):
        """Clean up old data based on retention policies"""
        self.logger.info("Starting data cleanup...")
        
        current_time = datetime.now()
        
        # Clean current directory (keep only last 24 hours)
        self._cleanup_directory(self.current_dir, self.retention_policies["current"])
        
        # Clean archive directories
        for archive_date_dir in self.archive_dir.iterdir():
            if not archive_date_dir.is_dir():
                continue
                
            try:
                date_obj = datetime.strptime(archive_date_dir.name, "%Y-%m-%d")
                
                # Check if directory is older than monthly retention
                if current_time - date_obj > self.retention_policies["monthly"]:
                    shutil.rmtree(archive_date_dir)
                    self.logger.info(f"Removed old archive directory: {archive_date_dir}")
                else:
                    # Clean individual files within directory
                    self._cleanup_directory(archive_date_dir, self.retention_policies["daily"])
                    
            except ValueError:
                # Skip non-date directories
                continue
        
        self.logger.info("Data cleanup completed")
    
    def _cleanup_directory(self, directory: Path, retention_period: timedelta):
        """Clean up files in a directory based on retention period"""
        current_time = datetime.now()
        
        for file_path in directory.iterdir():
            if not file_path.is_file():
                continue
                
            try:
                # Try to get file modification time
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                if current_time - mtime > retention_period:
                    file_path.unlink()
                    self.logger.debug(f"Removed old file: {file_path}")
                    
            except Exception as e:
                self.logger.warning(f"Could not process {file_path}: {e}")
    
    def get_current_market_data(self) -> Optional[Dict]:
        """Get current market data"""
        current_file = self.current_dir / "current_market_data.json"
        
        if current_file.exists():
            try:
                with open(current_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error reading current market data: {e}")
        
        return None
    
    def get_historical_data(self, start_date: str, end_date: str) -> List[Dict]:
        """Get historical market data for a date range"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        historical_data = []
        
        current = start
        while current <= end:
            date_key = current.strftime("%Y-%m-%d")
            date_dir = self.archive_dir / date_key
            
            if date_dir.exists():
                for file_path in date_dir.glob("*.json*"):
                    try:
                        if file_path.suffix == '.gz':
                            with gzip.open(file_path, 'rt') as f:
                                data = json.load(f)
                        else:
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                        
                        historical_data.append(data)
                        
                    except Exception as e:
                        self.logger.warning(f"Error reading {file_path}: {e}")
            
            current += timedelta(days=1)
        
        return historical_data
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        stats = {
            "total_files": 0,
            "total_size_mb": 0,
            "current_files": 0,
            "archive_files": 0,
            "oldest_file": None,
            "newest_file": None
        }
        
        # Count current files
        for file_path in self.current_dir.rglob("*"):
            if file_path.is_file():
                stats["current_files"] += 1
                stats["total_files"] += 1
                stats["total_size_mb"] += file_path.stat().st_size / (1024 * 1024)
        
        # Count archive files
        for file_path in self.archive_dir.rglob("*"):
            if file_path.is_file():
                stats["archive_files"] += 1
                stats["total_files"] += 1
                stats["total_size_mb"] += file_path.stat().st_size / (1024 * 1024)
        
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        
        return stats
    
    def _start_cleanup_thread(self):
        """Start background cleanup thread"""
        def cleanup_job():
            while True:
                try:
                    self.cleanup_old_data()
                    time.sleep(3600)  # Run every hour
                except Exception as e:
                    self.logger.error(f"Error in cleanup job: {e}")
                    time.sleep(300)  # Wait 5 minutes on error
        
        cleanup_thread = threading.Thread(target=cleanup_job, daemon=True)
        cleanup_thread.start()
        self.logger.info("Background cleanup thread started")

def main():
    """Main function to run data management operations"""
    data_manager = DataManager()
    
    # Organize existing files
    data_manager.organize_existing_files()
    
    # Get storage statistics
    stats = data_manager.get_storage_stats()
    print("Storage Statistics:")
    print(f"Total files: {stats['total_files']}")
    print(f"Total size: {stats['total_size_mb']} MB")
    print(f"Current files: {stats['current_files']}")
    print(f"Archive files: {stats['archive_files']}")
    
    # Schedule regular cleanup
    schedule.every().hour.do(data_manager.cleanup_old_data)
    
    print("Data management system initialized. Running scheduled cleanup...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("Data management system stopped.")

if __name__ == "__main__":
    main()
