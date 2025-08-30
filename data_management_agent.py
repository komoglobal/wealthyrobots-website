#!/usr/bin/env python3
"""
Data Management Agent - Automated Duplicate Detection and Cleanup
Prevents file spam while preserving system-critical files
"""

import os
import json
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Tuple
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [data_management] %(message)s",
    handlers=[logging.StreamHandler()]
)

class DataManagementAgent:
    """Intelligent data management system that prevents file duplication"""
    
    def __init__(self, base_dir: str = ".", excludes: List[str] | None = None, dry_run: bool = False):
        self.base_dir = Path(base_dir)
        self.excludes = set(excludes or [])
        self.dry_run = dry_run
        self.cleanup_log = "data_cleanup_log.json"
        
        # Files that should NEVER be deleted (system critical)
        self.critical_files = {
            # Core system files
            "unified_twitter_empire.py",
            "smart_scheduler.py", 
            "revenue_tracker.py",
            "empire_schedule.json",
            "unified_empire_log.json",
            "empire_metrics.json",
            
            # Configuration files
            "algorand_defi_config.py",
            "setup_algorand_defi.py",
            "unlimited_operations_config.json",
            
            # Current/latest dashboard files
            "current_firm_dashboard.json",
            "current_risk_dashboard.json", 
            "current_trading_dashboard.json",
            "current_performance_dashboard.json",
            
            # Agent coordination files
            "deployment_coordination.json",
            "deploy_manifest.json",
            "claude_background_status.json",
            "functional_claude_log.json",
            
            # Log files (keep recent ones)
            "orchestrator_fixed.log",
            "unified_twitter_empire.log"
        }
        
        # File patterns that indicate duplicates (with timestamps)
        self.duplicate_patterns = [
            "logging_optimization_*.json",
            "trading_dashboard_*.json", 
            "risk_dashboard_*.json",
            "firm_dashboard_*.json",
            "performance_dashboard_*.json",
            "claude_solution_*.py",
            "smart_viral_thread_*.txt",
            "content_optimization_*.txt",
            "customer_service_agent_output_*.txt",
            "todo_analysis_*.md",
            "config_optimization_*.json"
        ]
        
        # File size thresholds for different types
        self.size_thresholds = {
            "dashboard": 1000,  # Files > 1KB are likely real data
            "solution": 500,     # Files > 500B are likely real solutions
            "log": 100          # Files > 100B are likely real logs
        }
        
        # Load cleanup history
        self.cleanup_history = self.load_cleanup_history()
    
    def load_cleanup_history(self) -> Dict:
        """Load cleanup history to avoid re-analyzing same files"""
        try:
            if os.path.exists(self.cleanup_log):
                with open(self.cleanup_log, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logging.warning(f"Could not load cleanup history: {e}")
        
        return {
            "last_cleanup": None,
            "files_removed": 0,
            "space_saved": 0,
            "cleanup_sessions": []
        }
    
    def save_cleanup_history(self):
        """Save cleanup history"""
        try:
            with open(self.cleanup_log, 'w') as f:
                json.dump(self.cleanup_history, f, indent=2)
        except Exception as e:
            logging.error(f"Could not save cleanup history: {e}")
    
    def is_critical_file(self, file_path: str) -> bool:
        """Check if file is system-critical and should never be deleted"""
        filename = os.path.basename(file_path)
        return filename in self.critical_files
    
    def is_recent_file(self, file_path: str, hours: int = 24) -> bool:
        """Check if file was created in the last N hours"""
        try:
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            return datetime.now() - file_time < timedelta(hours=hours)
        except Exception:
            return False
    
    def analyze_duplicate_patterns(self) -> List[Tuple[str, List[str]]]:
        """Find files matching duplicate patterns"""
        duplicates = []
        
        for pattern in self.duplicate_patterns:
            matching_files = [p for p in self.base_dir.glob(pattern) if not any(str(p).startswith(ex) for ex in self.excludes)]
            if len(matching_files) > 1:
                # Group by file size to identify true duplicates
                size_groups = {}
                for file_path in matching_files:
                    try:
                        size = os.path.getsize(file_path)
                        if size not in size_groups:
                            size_groups[size] = []
                        size_groups[size].append(str(file_path))
                    except Exception:
                        continue
                for size, files in size_groups.items():
                    if len(files) > 1:
                        duplicates.append((pattern, files))
        return duplicates
    
    def detect_content_duplicates(self, file_list: List[str]) -> List[List[str]]:
        """Group files by content hash to find exact duplicates"""
        content_groups = {}
        
        for file_path in file_list:
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    content_hash = hashlib.md5(content).hexdigest()
                    
                    if content_hash not in content_groups:
                        content_groups[content_hash] = []
                    content_groups[content_hash].append(file_path)
            except Exception as e:
                logging.warning(f"Could not read {file_path}: {e}")
                continue
        
        # Return groups with multiple files (duplicates)
        return [files for files in content_groups.values() if len(files) > 1]
    
    def calculate_cleanup_impact(self, duplicate_groups: List[List[str]]) -> Tuple[int, int]:
        """Calculate how many files would be removed and space saved"""
        total_files = 0
        total_space = 0
        
        for group in duplicate_groups:
            # Keep the most recent file, remove others
            files_to_remove = group[1:]  # All except first
            total_files += len(files_to_remove)
            
            for file_path in files_to_remove:
                try:
                    total_space += os.path.getsize(file_path)
                except Exception:
                    continue
        
        return total_files, total_space
    
    def safe_cleanup_duplicates(self, duplicate_groups: List[List[str]], max_remove: int = 2000) -> Tuple[int, int]:
        """Safely remove duplicate files, keeping the most recent (cap per-run removals)."""
        files_removed = 0
        space_saved = 0
        
        for group in duplicate_groups:
            if files_removed >= max_remove:
                break
            try:
                group.sort(key=lambda x: os.path.getctime(x), reverse=True)
                files_to_keep = group[0]
                files_to_remove = group[1:]
                for file_path in files_to_remove:
                    if files_removed >= max_remove:
                        break
                    try:
                        if not self.is_critical_file(file_path):
                            file_size = os.path.getsize(file_path)
                            if not self.dry_run:
                                os.remove(file_path)
                            files_removed += 1
                            space_saved += file_size
                            logging.info(f"Removed: {file_path} ({file_size} bytes)")
                        else:
                            logging.warning(f"Skipped critical file: {file_path}")
                    except Exception as e:
                        logging.error(f"Could not remove {file_path}: {e}")
            except Exception as e:
                logging.error(f"Error processing group {group}: {e}")
                continue
        return files_removed, space_saved
    
    def run_cleanup_cycle(self) -> Dict:
        """Run one cleanup cycle"""
        logging.info("🔍 Starting data cleanup cycle...")
        
        # Find duplicate patterns
        duplicate_patterns = self.analyze_duplicate_patterns()
        logging.info(f"Found {len(duplicate_patterns)} duplicate patterns")
        
        total_files_removed = 0
        total_space_saved = 0
        
        for pattern, files in duplicate_patterns:
            logging.info(f"Analyzing pattern: {pattern} ({len(files)} files)")
            
            # Detect content duplicates
            content_duplicates = self.detect_content_duplicates(files)
            
            if content_duplicates:
                logging.info(f"Found {len(content_duplicates)} content duplicate groups")
                
                # Calculate impact
                files_to_remove, space_to_save = self.calculate_cleanup_impact(content_duplicates)
                logging.info(f"Would remove {files_to_remove} files, save {space_to_save} bytes")
                
                # Perform cleanup
                files_removed, space_saved = self.safe_cleanup_duplicates(content_duplicates)
                total_files_removed += files_removed
                total_space_saved += space_saved
                
                logging.info(f"Actually removed {files_removed} files, saved {space_saved} bytes")
            else:
                logging.info(f"No content duplicates found for {pattern}")
        
        # Update cleanup history
        cleanup_session = {
            "timestamp": datetime.now().isoformat(),
            "files_removed": total_files_removed,
            "space_saved": total_space_saved,
            "patterns_analyzed": len(duplicate_patterns)
        }
        
        self.cleanup_history["cleanup_sessions"].append(cleanup_session)
        self.cleanup_history["last_cleanup"] = datetime.now().isoformat()
        self.cleanup_history["files_removed"] += total_files_removed
        self.cleanup_history["space_saved"] += total_space_saved
        
        self.save_cleanup_history()
        
        logging.info(f"✅ Cleanup cycle completed: {total_files_removed} files removed, {total_space_saved} bytes saved")
        
        return {
            "files_removed": total_files_removed,
            "space_saved": total_space_saved,
            "patterns_analyzed": len(duplicate_patterns),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_system_status(self) -> Dict:
        """Get current system status and cleanup recommendations"""
        total_files = len(list(self.base_dir.rglob("*")))
        total_size = sum(f.stat().st_size for f in self.base_dir.rglob("*") if f.is_file())
        
        # Check for immediate cleanup opportunities
        duplicate_patterns = self.analyze_duplicate_patterns()
        immediate_cleanup = sum(len(files) for _, files in duplicate_patterns)
        
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024*1024), 2),
            "duplicate_patterns_found": len(duplicate_patterns),
            "immediate_cleanup_opportunity": immediate_cleanup,
            "last_cleanup": self.cleanup_history.get("last_cleanup"),
            "total_cleanup_impact": {
                "files_removed": self.cleanup_history.get("files_removed", 0),
                "space_saved_mb": round(self.cleanup_history.get("space_saved", 0) / (1024*1024), 2)
            }
        }

def main():
    """Run data management agent"""
    print("🧹 DATA MANAGEMENT AGENT STARTING")
    print("=" * 40)
    
    agent = DataManagementAgent()
    
    # Show current status
    status = agent.get_system_status()
    print(f"📊 Current System Status:")
    print(f"   Total files: {status['total_files']:,}")
    print(f"   Total size: {status['total_size_mb']} MB")
    print(f"   Duplicate patterns: {status['duplicate_patterns_found']}")
    print(f"   Cleanup opportunity: {status['immediate_cleanup_opportunity']} files")
    
    if status['last_cleanup']:
        print(f"   Last cleanup: {status['last_cleanup']}")
        print(f"   Total impact: {status['total_cleanup_impact']['files_removed']} files, {status['total_cleanup_impact']['space_saved_mb']} MB")
    
    # Run cleanup if there are opportunities
    if status['immediate_cleanup_opportunity'] > 0:
        print(f"\n🚀 Running cleanup cycle...")
        results = agent.run_cleanup_cycle()
        
        print(f"\n✅ Cleanup Results:")
        print(f"   Files removed: {results['files_removed']}")
        print(f"   Space saved: {results['space_saved']} bytes")
        print(f"   Patterns analyzed: {results['patterns_analyzed']}")
    else:
        print(f"\n✨ No immediate cleanup needed - system is clean!")
    
    # Show updated status
    updated_status = agent.get_system_status()
    print(f"\n📊 Updated System Status:")
    print(f"   Total files: {updated_status['total_files']:,}")
    print(f"   Total size: {updated_status['total_size_mb']} MB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WealthyRobot Data Management Agent")
    parser.add_argument("--root", default=".", help="Root directory to scan (default: current directory)")
    parser.add_argument("--exclude", action="append", default=[], help="Exclude prefix (can be given multiple times)")
    parser.add_argument("--dry-run", action="store_true", help="Scan and report without deleting")
    parser.add_argument("--max-remove", type=int, default=2000, help="Max files to remove in one run (default: 2000)")
    args = parser.parse_args()

    print("🧹 DATA MANAGEMENT AGENT STARTING")
    print("=" * 40)
    agent = DataManagementAgent(base_dir=args.root, excludes=args.exclude, dry_run=args.dry_run)

    status = agent.get_system_status()
    print(f"📊 Current System Status:")
    print(f"   Total files: {status['total_files']:,}")
    print(f"   Total size: {status['total_size_mb']} MB")
    print(f"   Duplicate patterns: {status['duplicate_patterns_found']}")
    print(f"   Cleanup opportunity: {status['immediate_cleanup_opportunity']} files")

    if status['immediate_cleanup_opportunity'] > 0 and not args.dry_run:
        print(f"\n🚀 Running cleanup cycle (max_remove={args.max_remove})...")
        duplicates = agent.analyze_duplicate_patterns()
        # Flatten candidate groups from file list
        content_dups = []
        for _, files in duplicates:
            content_dups.extend(agent.detect_content_duplicates(files))
        files_removed, space_saved = agent.safe_cleanup_duplicates(content_dups, max_remove=args.max_remove)
        print(f"\n✅ Cleanup Results:")
        print(f"   Files removed: {files_removed}")
        print(f"   Space saved: {space_saved} bytes")
    else:
        print("\n✨ No cleanup performed (either clean or dry-run)")

    updated = agent.get_system_status()
    print(f"\n📊 Updated System Status:")
    print(f"   Total files: {updated['total_files']:,}")
    print(f"   Total size: {updated['total_size_mb']} MB")
