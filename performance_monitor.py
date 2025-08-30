#!/usr/bin/env python3
"""
Performance Monitor - Shows impact of cleanup operations
"""

import os
import time
from pathlib import Path
from datetime import datetime

def get_system_stats():
    """Get current system statistics"""
    base_dir = Path("/home/ubuntu/wealthyrobot")
    
    stats = {
        "timestamp": datetime.now().isoformat(),
        "root_files": 0,
        "logging_optimization_files": 0,
        "log_files": 0,
        "cache_dirs": 0,
        "pyc_files": 0,
        "total_size_mb": 0
    }
    
    try:
        # Count files in root directory
        root_files = list(base_dir.iterdir())
        stats["root_files"] = len([f for f in root_files if f.is_file()])
        
        # Count logging optimization files
        logging_files = list(base_dir.glob("logging_optimization_*.json"))
        stats["logging_optimization_files"] = len(logging_files)
        
        # Count log files
        logs_dir = base_dir / "logs"
        if logs_dir.exists():
            log_patterns = ["*.log", "*.out", "*.err", "*.jsonl"]
            log_count = 0
            for pattern in log_patterns:
                log_count += len(list(logs_dir.rglob(pattern)))
            stats["log_files"] = log_count
        
        # Count cache directories
        cache_dirs = list(base_dir.rglob("__pycache__"))
        stats["cache_dirs"] = len(cache_dirs)
        
        # Count .pyc files
        pyc_files = list(base_dir.rglob("*.pyc"))
        stats["pyc_files"] = len(pyc_files)
        
        # Calculate total size
        total_size = 0
        for file_path in base_dir.rglob("*"):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except:
                    continue
        
        stats["total_size_mb"] = round(total_size / (1024 * 1024), 2)
        
    except Exception as e:
        print(f"Error getting stats: {e}")
    
    return stats

def show_performance_impact():
    """Show performance impact of cleanup"""
    print("📊 WealthyRobot Performance Monitor")
    print("=" * 50)
    
    # Get current stats
    current_stats = get_system_stats()
    
    print(f"\n🕐 Current Status: {current_stats['timestamp']}")
    print(f"📁 Root Directory Files: {current_stats['root_files']}")
    print(f"🗂️  Logging Optimization Files: {current_stats['logging_optimization_files']}")
    print(f"📝 Log Files: {current_stats['log_files']}")
    print(f"🐍 Python Cache Directories: {current_stats['cache_dirs']}")
    print(f"⚡ .pyc Files: {current_stats['pyc_files']}")
    print(f"💾 Total Size: {current_stats['total_size_mb']} MB")
    
    # Performance assessment
    print("\n🎯 Performance Assessment:")
    
    if current_stats['logging_optimization_files'] > 100:
        print("   ❌ CRITICAL: Too many logging files - causing performance issues")
        print("   💡 Action: Run cleanup immediately")
    elif current_stats['logging_optimization_files'] > 50:
        print("   ⚠️  WARNING: Many logging files - performance may be affected")
        print("   💡 Action: Consider cleanup")
    else:
        print("   ✅ GOOD: Logging files are under control")
    
    if current_stats['cache_dirs'] > 10:
        print("   ⚠️  WARNING: Many cache directories - may slow down operations")
        print("   💡 Action: Clear Python cache")
    else:
        print("   ✅ GOOD: Cache directories are reasonable")
    
    if current_stats['root_files'] > 200:
        print("   ❌ CRITICAL: Too many files in root - causing Cursor freezing")
        print("   💡 Action: Immediate cleanup required")
    elif current_stats['root_files'] > 100:
        print("   ⚠️  WARNING: Many files in root - may affect performance")
        print("   💡 Action: Consider cleanup")
    else:
        print("   ✅ GOOD: Root directory is clean")
    
    # Recommendations
    print("\n💡 Recommendations:")
    
    if current_stats['logging_optimization_files'] > 0:
        print("   1. Run: python3 quick_cleanup_now.py")
        print("      - Immediate performance improvement")
        print("      - Organizes scattered files")
    
    if current_stats['cache_dirs'] > 5:
        print("   2. Clear Python cache for faster operations")
    
    if current_stats['root_files'] > 150:
        print("   3. Comprehensive cleanup needed")
        print("      - Run: python3 comprehensive_cleanup.py")
        print("      - Full system optimization")
    
    print("\n🚀 Quick Actions:")
    print("   • Quick cleanup: python3 quick_cleanup_now.py")
    print("   • Full cleanup: python3 comprehensive_cleanup.py")
    print("   • Monitor: python3 performance_monitor.py")

def main():
    """Main function"""
    show_performance_impact()

if __name__ == "__main__":
    main()
