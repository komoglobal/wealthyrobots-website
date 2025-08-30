#!/usr/bin/env python3
"""
Status checker for WealthyRobot Data Management System
Quick way to see system health and storage status
"""

import os
import json
from pathlib import Path
from datetime import datetime

def check_system_status():
    """Check overall system status"""
    base_dir = Path("/home/ubuntu/wealthyrobot")
    
    print("🔍 WealthyRobot Data Management System Status")
    print("=" * 50)
    
    # Check if data manager is running
    print("\n📊 Process Status:")
    os.system("ps aux | grep data_management_system | grep -v grep")
    
    # Check directory structure
    print("\n📁 Directory Structure:")
    data_dir = base_dir / "market_data"
    if data_dir.exists():
        print(f"✅ Data directory: {data_dir}")
        
        current_dir = data_dir / "current"
        archive_dir = data_dir / "archive"
        
        if current_dir.exists():
            current_files = len(list(current_dir.glob("*")))
            print(f"✅ Current data: {current_files} files")
        
        if archive_dir.exists():
            archive_dates = len(list(archive_dir.iterdir()))
            print(f"✅ Archive dates: {archive_dates}")
            
            total_archived = 0
            for date_dir in archive_dir.iterdir():
                if date_dir.is_dir():
                    total_archived += len(list(date_dir.glob("*")))
            print(f"✅ Total archived files: {total_archived}")
    else:
        print("❌ Data directory not found")
    
    # Check for any remaining snapshot files in root
    print("\n🚨 Root Directory Check:")
    root_snapshots = list(base_dir.glob("market_data_snapshot_*.json"))
    if root_snapshots:
        print(f"⚠️  Found {len(root_snapshots)} snapshot files in root directory")
        print("   These should be cleaned up!")
    else:
        print("✅ No snapshot files in root directory")
    
    # Check disk usage
    print("\n💾 Disk Usage:")
    os.system(f"du -sh {base_dir}/market_data/ 2>/dev/null || echo 'Market data directory not found'")
    
    # Check recent logs
    print("\n📝 Recent Activity:")
    log_file = base_dir / "logs" / "data_manager.log"
    if log_file.exists():
        print("Last 5 log entries:")
        os.system(f"tail -5 {log_file}")
    else:
        print("No log file found")
    
    print("\n" + "=" * 50)
    print("✅ System check completed!")

if __name__ == "__main__":
    check_system_status()
