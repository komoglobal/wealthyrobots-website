#!/usr/bin/env python3
"""
Empire Optimization System for WealthyRobot
Comprehensive cleanup and optimization of redundant files, logs, and snapshots
"""

import os
import json
import shutil
import gzip
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple, Any
import threading
import schedule

class EmpireOptimizer:
    """Comprehensive empire optimization system"""
    
    def __init__(self, base_dir: str = "/home/ubuntu/wealthyrobot"):
        self.base_dir = Path(base_dir)
        self.optimized_dir = self.base_dir / "optimized_empire"
        self.logs_dir = self.optimized_dir / "logs"
        self.reports_dir = self.optimized_dir / "reports"
        self.archives_dir = self.optimized_dir / "archives"
        
        # Create optimized directory structure
        self._create_optimized_structure()
        
        # Configure logging
        self._setup_logging()
        
        # File patterns to optimize
        self.optimization_patterns = {
            "logging_optimization": {
                "pattern": "logging_optimization_*.json",
                "retention_days": 7,
                "compress": True,
                "description": "Logging optimization reports"
            },
            "agent_coordination": {
                "pattern": "agent_coordination_log_*.json",
                "retention_days": 14,
                "compress": True,
                "description": "Agent coordination logs"
            },
            "enhanced_reports": {
                "pattern": "enhanced_visual_test_report_*.json",
                "retention_days": 30,
                "compress": True,
                "description": "Enhanced visual test reports"
            },
            "claude_optimization": {
                "pattern": "claude_content_optimization_*.json",
                "retention_days": 14,
                "compress": True,
                "description": "Claude content optimization reports"
            },
            "large_logs": {
                "pattern": "*.log",
                "retention_days": 30,
                "compress": True,
                "description": "Large log files"
            },
            "jsonl_files": {
                "pattern": "*.jsonl",
                "retention_days": 60,
                "compress": True,
                "description": "JSONL data files"
            }
        }
        
        # Start background optimization thread
        self._start_optimization_thread()
    
    def _create_optimized_structure(self):
        """Create optimized directory structure"""
        directories = [
            self.optimized_dir,
            self.logs_dir,
            self.reports_dir,
            self.archives_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = self.logs_dir / "empire_optimizer.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def analyze_empire_status(self) -> Dict[str, Any]:
        """Analyze current empire status and identify optimization opportunities"""
        self.logger.info("🔍 Analyzing Empire status...")
        
        analysis = {
            "total_files": 0,
            "total_size_mb": 0,
            "redundant_files": {},
            "optimization_opportunities": [],
            "space_savings_potential": 0
        }
        
        # Analyze each pattern
        for pattern_name, pattern_config in self.optimization_patterns.items():
            pattern = pattern_config["pattern"]
            files = list(self.base_dir.glob(pattern))
            
            if files:
                total_size = sum(f.stat().st_size for f in files)
                analysis["redundant_files"][pattern_name] = {
                    "count": len(files),
                    "size_mb": round(total_size / (1024 * 1024), 2),
                    "description": pattern_config["description"],
                    "retention_days": pattern_config["retention_days"]
                }
                
                analysis["total_files"] += len(files)
                analysis["total_size_mb"] += total_size / (1024 * 1024)
        
        # Calculate potential savings
        analysis["space_savings_potential"] = round(analysis["total_size_mb"] * 0.7, 2)  # 70% compression
        
        # Identify specific optimization opportunities
        analysis["optimization_opportunities"] = [
            "Compress and archive old optimization files",
            "Consolidate redundant logs",
            "Implement intelligent retention policies",
            "Create unified logging system",
            "Optimize large JSONL files"
        ]
        
        self.logger.info(f"Analysis complete: {analysis['total_files']} files, {analysis['total_size_mb']:.2f} MB")
        return analysis
    
    def optimize_empire(self, dry_run: bool = False) -> Dict[str, Any]:
        """Perform comprehensive empire optimization"""
        self.logger.info("🚀 Starting Empire optimization...")
        
        if dry_run:
            self.logger.info("🔍 DRY RUN MODE - No files will be modified")
        
        optimization_results = {
            "files_processed": 0,
            "files_compressed": 0,
            "files_archived": 0,
            "files_deleted": 0,
            "space_saved_mb": 0,
            "errors": []
        }
        
        try:
            # Process each pattern
            for pattern_name, pattern_config in self.optimization_patterns.items():
                self.logger.info(f"Processing {pattern_name}...")
                
                pattern = pattern_config["pattern"]
                files = list(self.base_dir.glob(pattern))
                
                if not files:
                    continue
                
                # Group files by date for intelligent retention
                files_by_date = self._group_files_by_date(files, pattern_config["retention_days"])
                
                for date_key, date_files in files_by_date.items():
                    if dry_run:
                        self.logger.info(f"  Would process {len(date_files)} files for {date_key}")
                        continue
                    
                    # Process files for this date
                    result = self._process_files_for_date(
                        date_key, date_files, pattern_config, pattern_name
                    )
                    
                    # Update results
                    optimization_results["files_processed"] += result["files_processed"]
                    optimization_results["files_compressed"] += result["files_compressed"]
                    optimization_results["files_archived"] += result["files_archived"]
                    optimization_results["files_deleted"] += result["files_deleted"]
                    optimization_results["space_saved_mb"] += result["space_saved_mb"]
                    
                    if result["errors"]:
                        optimization_results["errors"].extend(result["errors"])
        
        except Exception as e:
            error_msg = f"Error during optimization: {e}"
            self.logger.error(error_msg)
            optimization_results["errors"].append(error_msg)
        
        self.logger.info(f"Empire optimization completed: {optimization_results['files_processed']} files processed")
        return optimization_results
    
    def _group_files_by_date(self, files: List[Path], retention_days: int) -> Dict[str, List[Path]]:
        """Group files by date for intelligent retention"""
        files_by_date = {}
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        for file_path in files:
            try:
                # Try to extract date from filename
                date_str = self._extract_date_from_filename(file_path.name)
                if date_str:
                    date_obj = datetime.strptime(date_str, "%Y%m%d")
                    date_key = date_obj.strftime("%Y-%m-%d")
                    
                    if date_obj >= cutoff_date:
                        if date_key not in files_by_date:
                            files_by_date[date_key] = []
                        files_by_date[date_key].append(file_path)
                    else:
                        # File is older than retention period
                        if "old_files" not in files_by_date:
                            files_by_date["old_files"] = []
                        files_by_date["old_files"].append(file_path)
                else:
                    # Could not parse date, treat as current
                    if "current" not in files_by_date:
                        files_by_date["current"] = []
                    files_by_date["current"].append(file_path)
                    
            except Exception as e:
                self.logger.warning(f"Could not parse date from {file_path}: {e}")
                if "unparseable" not in files_by_date:
                    files_by_date["unparseable"] = []
                files_by_date["unparseable"].append(file_path)
        
        return files_by_date
    
    def _extract_date_from_filename(self, filename: str) -> Optional[str]:
        """Extract date from filename patterns"""
        import re
        
        # Try different date patterns
        patterns = [
            r'(\d{8})',  # YYYYMMDD
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{4}_\d{2}_\d{2})'   # YYYY_MM_DD
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                date_str = match.group(1)
                # Normalize to YYYYMMDD format
                if '-' in date_str:
                    date_str = date_str.replace('-', '')
                elif '_' in date_str:
                    date_str = date_str.replace('_', '')
                return date_str
        
        return None
    
    def _process_files_for_date(self, date_key: str, files: List[Path], 
                               pattern_config: Dict, pattern_name: str) -> Dict[str, Any]:
        """Process files for a specific date"""
        result = {
            "files_processed": len(files),
            "files_compressed": 0,
            "files_archived": 0,
            "files_deleted": 0,
            "space_saved_mb": 0,
            "errors": []
        }
        
        try:
            if date_key == "old_files":
                # Delete old files
                for file_path in files:
                    try:
                        file_size = file_path.stat().st_size / (1024 * 1024)
                        file_path.unlink()
                        result["files_deleted"] += 1
                        result["space_saved_mb"] += file_size
                        self.logger.debug(f"Deleted old file: {file_path}")
                    except Exception as e:
                        result["errors"].append(f"Error deleting {file_path}: {e}")
            
            else:
                # Archive and compress current files
                archive_dir = self.archives_dir / pattern_name / date_key
                archive_dir.mkdir(parents=True, exist_ok=True)
                
                for file_path in files:
                    try:
                        # Compress file
                        compressed_path = archive_dir / f"{file_path.stem}.gz"
                        self._compress_file(file_path, compressed_path)
                        
                        # Calculate space saved
                        original_size = file_path.stat().st_size / (1024 * 1024)
                        compressed_size = compressed_path.stat().st_size / (1024 * 1024)
                        space_saved = original_size - compressed_size
                        
                        # Remove original file
                        file_path.unlink()
                        
                        result["files_compressed"] += 1
                        result["space_saved_mb"] += space_saved
                        
                        self.logger.debug(f"Compressed {file_path} -> {compressed_path}")
                        
                    except Exception as e:
                        result["errors"].append(f"Error processing {file_path}: {e}")
        
        except Exception as e:
            result["errors"].append(f"Error processing date {date_key}: {e}")
        
        return result
    
    def _compress_file(self, source_path: Path, target_path: Path):
        """Compress a file using gzip"""
        with open(source_path, 'rb') as source:
            with gzip.open(target_path, 'wb') as target:
                shutil.copyfileobj(source, target)
    
    def create_unified_logging_system(self):
        """Create a unified logging system to prevent future log explosion"""
        self.logger.info("🔧 Creating unified logging system...")
        
        unified_config = {
            "log_rotation": {
                "max_size_mb": 100,
                "backup_count": 5,
                "rotation_interval": "daily"
            },
            "log_levels": {
                "console": "INFO",
                "file": "DEBUG",
                "error_file": "ERROR"
            },
            "log_categories": {
                "trading": "trading.log",
                "system": "system.log",
                "agents": "agents.log",
                "optimization": "optimization.log"
            }
        }
        
        # Create unified logging configuration
        config_file = self.optimized_dir / "unified_logging_config.json"
        with open(config_file, 'w') as f:
            json.dump(unified_config, f, indent=2)
        
        self.logger.info("✅ Unified logging system configured")
        return unified_config
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get current optimization statistics"""
        stats = {
            "optimized_files": 0,
            "total_size_mb": 0,
            "compressed_size_mb": 0,
            "space_saved_mb": 0,
            "last_optimization": None
        }
        
        # Count optimized files
        for archive_dir in self.archives_dir.rglob("*"):
            if archive_dir.is_file():
                stats["optimized_files"] += 1
                stats["compressed_size_mb"] += archive_dir.stat().st_size / (1024 * 1024)
        
        # Calculate space saved
        stats["space_saved_mb"] = round(stats["compressed_size_mb"] * 0.3, 2)  # Estimate
        
        # Check last optimization time
        log_file = self.logs_dir / "empire_optimizer.log"
        if log_file.exists():
            stats["last_optimization"] = datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
        
        return stats
    
    def _start_optimization_thread(self):
        """Start background optimization thread"""
        def optimization_job():
            while True:
                try:
                    self.logger.info("Running scheduled empire optimization...")
                    self.optimize_empire(dry_run=False)
                    time.sleep(86400)  # Run daily
                except Exception as e:
                    self.logger.error(f"Error in optimization job: {e}")
                    time.sleep(3600)  # Wait 1 hour on error
        
        optimization_thread = threading.Thread(target=optimization_job, daemon=True)
        optimization_thread.start()
        self.logger.info("Background optimization thread started")

def main():
    """Main function to run empire optimization"""
    print("🚀 WealthyRobot Empire Optimization System")
    print("=" * 50)
    
    optimizer = EmpireOptimizer()
    
    # Analyze current status
    print("\n🔍 Analyzing Empire status...")
    analysis = optimizer.analyze_empire_status()
    
    print(f"\n📊 Current Status:")
    print(f"  Total files: {analysis['total_files']}")
    print(f"  Total size: {analysis['total_size_mb']:.2f} MB")
    print(f"  Space savings potential: {analysis['space_savings_potential']:.2f} MB")
    
    print(f"\n📋 Redundant Files Found:")
    for pattern_name, info in analysis['redundant_files'].items():
        print(f"  {pattern_name}: {info['count']} files, {info['size_mb']} MB")
    
    print(f"\n🎯 Optimization Opportunities:")
    for opportunity in analysis['optimization_opportunities']:
        print(f"  • {opportunity}")
    
    # Ask user if they want to proceed
    response = input("\n🚀 Proceed with optimization? (y/n): ").strip().lower()
    
    if response == 'y':
        print("\n🚀 Starting Empire optimization...")
        results = optimizer.optimize_empire(dry_run=False)
        
        print(f"\n✅ Optimization completed!")
        print(f"  Files processed: {results['files_processed']}")
        print(f"  Files compressed: {results['files_compressed']}")
        print(f"  Files archived: {results['files_archived']}")
        print(f"  Files deleted: {results['files_deleted']}")
        print(f"  Space saved: {results['space_saved_mb']:.2f} MB")
        
        if results['errors']:
            print(f"\n⚠️ Errors encountered:")
            for error in results['errors']:
                print(f"  • {error}")
        
        # Create unified logging system
        print(f"\n🔧 Creating unified logging system...")
        optimizer.create_unified_logging_system()
        
        # Show final stats
        final_stats = optimizer.get_optimization_stats()
        print(f"\n📊 Final Statistics:")
        print(f"  Optimized files: {final_stats['optimized_files']}")
        print(f"  Compressed size: {final_stats['compressed_size_mb']:.2f} MB")
        print(f"  Space saved: {final_stats['space_saved_mb']:.2f} MB")
        
    else:
        print("⏸️ Optimization cancelled")
    
    print("\n🎉 Empire optimization system ready!")

if __name__ == "__main__":
    main()
