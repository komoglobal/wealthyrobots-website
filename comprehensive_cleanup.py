#!/usr/bin/env python3
"""
Comprehensive Cleanup Script for WealthyRobot Trading Platform
Cleans up dashboard logs, logs, and system snapshots while maintaining performance
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

class ComprehensiveCleanup:
    def __init__(self, base_dir: str = "/home/ubuntu/wealthyrobot"):
        self.base_dir = Path(base_dir)
        self.logs_dir = self.base_dir / "logs"
        self.cleanup_dir = self.base_dir / "cleanup_archive"
        self.reports_dir = self.logs_dir / "reports"
        
        # Create necessary directories
        self._create_directories()
        
        # Configure logging
        self._setup_logging()
        
        # Cleanup policies
        self.cleanup_policies = {
            "logging_optimization": {
                "retention_days": 7,
                "compress_after_days": 1,
                "max_files": 100
            },
            "log_files": {
                "retention_days": 14,
                "compress_after_days": 3,
                "max_files": 200
            },
            "system_snapshots": {
                "retention_days": 30,
                "compress_after_days": 7,
                "max_files": 50
            },
            "dashboard_logs": {
                "retention_days": 21,
                "compress_after_days": 5,
                "max_files": 150
            }
        }
    
    def _create_directories(self):
        """Create necessary directory structure"""
        directories = [
            self.cleanup_dir,
            self.reports_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = self.cleanup_dir / "cleanup.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def cleanup_logging_optimization_files(self):
        """Clean up logging optimization files from root directory"""
        self.logger.info("Cleaning up logging optimization files...")
        
        # Find all logging optimization files in root
        pattern = "logging_optimization_*.json"
        files_to_clean = list(self.base_dir.glob(pattern))
        
        if not files_to_clean:
            self.logger.info("No logging optimization files found")
            return
        
        # Create archive directory
        archive_dir = self.cleanup_dir / "logging_optimization"
        archive_dir.mkdir(exist_ok=True)
        
        # Group files by date
        files_by_date = {}
        for file_path in files_to_clean:
            try:
                # Extract date from filename
                filename = file_path.name
                date_str = filename.split('_')[1]  # Get date part
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                
                if date_obj not in files_by_date:
                    files_by_date[date_obj] = []
                files_by_date[date_obj].append(file_path)
                
            except Exception as e:
                self.logger.warning(f"Could not parse date from {file_path.name}: {e}")
                continue
        
        # Process files by date
        current_time = datetime.now()
        total_processed = 0
        total_compressed = 0
        
        for date_obj, files in sorted(files_by_date.items()):
            days_old = (current_time - date_obj).days
            
            if days_old > self.cleanup_policies["logging_optimization"]["retention_days"]:
                # Delete old files
                for file_path in files:
                    try:
                        file_path.unlink()
                        total_processed += 1
                        self.logger.info(f"Deleted old file: {file_path.name}")
                    except Exception as e:
                        self.logger.error(f"Error deleting {file_path.name}: {e}")
                        
            elif days_old > self.cleanup_policies["logging_optimization"]["compress_after_days"]:
                # Compress files
                date_dir = archive_dir / date_obj.strftime("%Y-%m-%d")
                date_dir.mkdir(exist_ok=True)
                
                for file_path in files:
                    try:
                        compressed_file = date_dir / f"{file_path.stem}.gz"
                        with open(file_path, 'rb') as f_in:
                            with gzip.open(compressed_file, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        # Delete original file
                        file_path.unlink()
                        total_compressed += 1
                        self.logger.info(f"Compressed and archived: {file_path.name}")
                        
                    except Exception as e:
                        self.logger.error(f"Error compressing {file_path.name}: {e}")
                        
            else:
                # Keep recent files but limit count
                max_files = self.cleanup_policies["logging_optimization"]["max_files"]
                if len(files) > max_files:
                    # Keep only the most recent files
                    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                    files_to_delete = files[max_files:]
                    
                    for file_path in files_to_delete:
                        try:
                            file_path.unlink()
                            total_processed += 1
                            self.logger.info(f"Deleted excess file: {file_path.name}")
                        except Exception as e:
                            self.logger.error(f"Error deleting {file_path.name}: {e}")
        
        self.logger.info(f"Logging optimization cleanup completed: {total_processed} deleted, {total_compressed} compressed")
    
    def cleanup_log_files(self):
        """Clean up log files in logs directory"""
        self.logger.info("Cleaning up log files...")
        
        if not self.logs_dir.exists():
            self.logger.info("Logs directory not found")
            return
        
        # Find all log files
        log_patterns = ["*.log", "*.out", "*.err", "*.jsonl"]
        files_to_clean = []
        
        for pattern in log_patterns:
            files_to_clean.extend(self.logs_dir.rglob(pattern))
        
        if not files_to_clean:
            self.logger.info("No log files found")
            return
        
        # Create archive directory
        archive_dir = self.cleanup_dir / "log_files"
        archive_dir.mkdir(exist_ok=True)
        
        # Process files
        current_time = datetime.now()
        total_processed = 0
        total_compressed = 0
        
        for file_path in files_to_clean:
            try:
                # Get file age
                file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                days_old = file_age.days
                
                if days_old > self.cleanup_policies["log_files"]["retention_days"]:
                    # Delete old files
                    file_path.unlink()
                    total_processed += 1
                    self.logger.info(f"Deleted old log file: {file_path.name}")
                    
                elif days_old > self.cleanup_policies["log_files"]["compress_after_days"]:
                    # Compress files
                    compressed_file = archive_dir / f"{file_path.stem}_{file_path.suffix}.gz"
                    
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(compressed_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # Delete original file
                    file_path.unlink()
                    total_compressed += 1
                    self.logger.info(f"Compressed log file: {file_path.name}")
                    
            except Exception as e:
                self.logger.error(f"Error processing log file {file_path.name}: {e}")
        
        self.logger.info(f"Log files cleanup completed: {total_processed} deleted, {total_compressed} compressed")
    
    def cleanup_system_snapshots(self):
        """Clean up system snapshot files"""
        self.logger.info("Cleaning up system snapshots...")
        
        # Find snapshot files
        snapshot_patterns = ["*_snapshot_*.json", "*_state.json", "*_metrics.json"]
        files_to_clean = []
        
        for pattern in snapshot_patterns:
            files_to_clean.extend(self.base_dir.glob(pattern))
        
        if not files_to_clean:
            self.logger.info("No system snapshot files found")
            return
        
        # Create archive directory
        archive_dir = self.cleanup_dir / "system_snapshots"
        archive_dir.mkdir(exist_ok=True)
        
        # Process files
        current_time = datetime.now()
        total_processed = 0
        total_compressed = 0
        
        for file_path in files_to_clean:
            try:
                # Get file age
                file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                days_old = file_age.days
                
                if days_old > self.cleanup_policies["system_snapshots"]["retention_days"]:
                    # Delete old files
                    file_path.unlink()
                    total_processed += 1
                    self.logger.info(f"Deleted old snapshot: {file_path.name}")
                    
                elif days_old > self.cleanup_policies["system_snapshots"]["compress_after_days"]:
                    # Compress files
                    compressed_file = archive_dir / f"{file_path.stem}.gz"
                    
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(compressed_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # Delete original file
                    file_path.unlink()
                    total_compressed += 1
                    self.logger.info(f"Compressed snapshot: {file_path.name}")
                    
            except Exception as e:
                self.logger.error(f"Error processing snapshot {file_path.name}: {e}")
        
        self.logger.info(f"System snapshots cleanup completed: {total_processed} deleted, {total_compressed} compressed")
    
    def cleanup_dashboard_logs(self):
        """Clean up dashboard and monitoring logs"""
        self.logger.info("Cleaning up dashboard logs...")
        
        # Find dashboard-related files
        dashboard_patterns = ["*_health_*.json", "*_metrics.json", "*_status.json"]
        files_to_clean = []
        
        for pattern in dashboard_patterns:
            files_to_clean.extend(self.base_dir.glob(pattern))
            files_to_clean.extend(self.logs_dir.glob(pattern))
        
        if not files_to_clean:
            self.logger.info("No dashboard log files found")
            return
        
        # Create archive directory
        archive_dir = self.cleanup_dir / "dashboard_logs"
        archive_dir.mkdir(exist_ok=True)
        
        # Process files
        current_time = datetime.now()
        total_processed = 0
        total_compressed = 0
        
        for file_path in files_to_clean:
            try:
                # Get file age
                file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                days_old = file_age.days
                
                if days_old > self.cleanup_policies["dashboard_logs"]["retention_days"]:
                    # Delete old files
                    file_path.unlink()
                    total_processed += 1
                    self.logger.info(f"Deleted old dashboard log: {file_path.name}")
                    
                elif days_old > self.cleanup_policies["dashboard_logs"]["compress_after_days"]:
                    # Compress files
                    compressed_file = archive_dir / f"{file_path.stem}.gz"
                    
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(compressed_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # Delete original file
                    file_path.unlink()
                    total_compressed += 1
                    self.logger.info(f"Compressed dashboard log: {file_path.name}")
                    
            except Exception as e:
                self.logger.error(f"Error processing dashboard log {file_path.name}: {e}")
        
        self.logger.info(f"Dashboard logs cleanup completed: {total_processed} deleted, {total_compressed} compressed")
    
    def optimize_performance(self):
        """Optimize system performance after cleanup"""
        self.logger.info("Optimizing system performance...")
        
        try:
            # Clear Python cache
            cache_dirs = list(self.base_dir.rglob("__pycache__"))
            for cache_dir in cache_dirs:
                try:
                    shutil.rmtree(cache_dir)
                    self.logger.info(f"Cleared cache: {cache_dir}")
                except Exception as e:
                    self.logger.warning(f"Could not clear cache {cache_dir}: {e}")
            
            # Clear .pyc files
            pyc_files = list(self.base_dir.rglob("*.pyc"))
            for pyc_file in pyc_files:
                try:
                    pyc_file.unlink()
                    self.logger.info(f"Removed .pyc file: {pyc_file}")
                except Exception as e:
                    self.logger.warning(f"Could not remove {pyc_file}: {e}")
            
            self.logger.info("Performance optimization completed")
            
        except Exception as e:
            self.logger.error(f"Performance optimization error: {e}")
    
    def generate_cleanup_report(self):
        """Generate cleanup report"""
        self.logger.info("Generating cleanup report...")
        
        try:
            # Calculate space savings
            original_size = 0
            final_size = 0
            
            # Count files
            total_files = len(list(self.cleanup_dir.rglob("*")))
            
            report = {
                "cleanup_timestamp": datetime.now().isoformat(),
                "total_files_processed": total_files,
                "space_saved_mb": round(original_size / (1024 * 1024), 2),
                "compression_ratio": "N/A",
                "cleanup_policies": self.cleanup_policies,
                "archive_structure": self._get_archive_structure()
            }
            
            # Save report
            report_file = self.cleanup_dir / "cleanup_report.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info(f"Cleanup report saved: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
    
    def _get_archive_structure(self):
        """Get archive directory structure"""
        structure = {}
        
        try:
            for item in self.cleanup_dir.iterdir():
                if item.is_dir():
                    structure[item.name] = len(list(item.rglob("*")))
                else:
                    structure[item.name] = "file"
        except Exception as e:
            self.logger.error(f"Error getting archive structure: {e}")
        
        return structure
    
    def run_comprehensive_cleanup(self):
        """Run all cleanup operations"""
        self.logger.info("🚀 Starting comprehensive cleanup...")
        
        start_time = time.time()
        
        try:
            # Run all cleanup operations
            self.cleanup_logging_optimization_files()
            self.cleanup_log_files()
            self.cleanup_system_snapshots()
            self.cleanup_dashboard_logs()
            
            # Optimize performance
            self.optimize_performance()
            
            # Generate report
            self.generate_cleanup_report()
            
            elapsed_time = time.time() - start_time
            self.logger.info(f"✅ Comprehensive cleanup completed in {elapsed_time:.2f} seconds")
            
        except Exception as e:
            self.logger.error(f"❌ Cleanup failed: {e}")
            raise

def main():
    """Main function"""
    print("🚀 WealthyRobot Comprehensive Cleanup System")
    print("Cleaning up dashboard logs, logs, and system snapshots...")
    
    try:
        cleanup = ComprehensiveCleanup()
        cleanup.run_comprehensive_cleanup()
        print("✅ Cleanup completed successfully!")
        print(f"📁 Check results in: {cleanup.cleanup_dir}")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
