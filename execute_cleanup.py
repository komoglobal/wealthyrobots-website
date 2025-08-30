#!/usr/bin/env python3
"""
Execute Cleanup - Simple script to run all cleanup operations
"""

import subprocess
import sys
import os
from pathlib import Path

def run_cleanup():
    """Run all cleanup operations"""
    print("🚀 WealthyRobot Cleanup System - Executing Now!")
    print("=" * 60)
    
    # Check current status
    base_dir = Path("/home/ubuntu/wealthyrobot")
    print(f"📍 Working directory: {base_dir}")
    
    # Count files before cleanup
    try:
        files_before = len([f for f in base_dir.iterdir() if f.is_file()])
        print(f"📁 Files before cleanup: {files_before}")
    except Exception as e:
        print(f"⚠️  Could not count files: {e}")
    
    # Run quick cleanup
    print("\n🔍 Step 1: Running Quick Cleanup...")
    try:
        result = subprocess.run([sys.executable, "quick_cleanup_now.py"], 
                              capture_output=True, text=True, cwd=base_dir)
        if result.returncode == 0:
            print("   ✅ Quick cleanup completed successfully")
            print("   📤 Output:", result.stdout[-200:] if result.stdout else "No output")
        else:
            print("   ⚠️  Quick cleanup had issues")
            print("   📤 Error:", result.stderr[-200:] if result.stderr else "No error output")
    except Exception as e:
        print(f"   ❌ Quick cleanup failed: {e}")
    
    # Check quick cleanup results
    quick_cleanup_dir = base_dir / "quick_cleanup"
    if quick_cleanup_dir.exists():
        quick_files = len(list(quick_cleanup_dir.rglob("*")))
        print(f"   📁 Quick cleanup archive: {quick_files} files")
    
    # Run comprehensive cleanup
    print("\n🔍 Step 2: Running Comprehensive Cleanup...")
    try:
        result = subprocess.run([sys.executable, "comprehensive_cleanup.py"], 
                              capture_output=True, text=True, cwd=base_dir)
        if result.returncode == 0:
            print("   ✅ Comprehensive cleanup completed successfully")
            print("   📤 Output:", result.stdout[-200:] if result.stdout else "No output")
        else:
            print("   ⚠️  Comprehensive cleanup had issues")
            print("   📤 Error:", result.stderr[-200:] if result.stderr else "No error output")
    except Exception as e:
        print(f"   ❌ Comprehensive cleanup failed: {e}")
    
    # Check comprehensive cleanup results
    cleanup_archive_dir = base_dir / "cleanup_archive"
    if cleanup_archive_dir.exists():
        archive_files = len(list(cleanup_archive_dir.rglob("*")))
        print(f"   📁 Comprehensive cleanup archive: {archive_files} files")
    
    # Show final status
    print("\n🎯 Final Status:")
    try:
        files_after = len([f for f in base_dir.iterdir() if f.is_file()])
        print(f"   📁 Files after cleanup: {files_after}")
        
        if 'files_before' in locals():
            reduction = files_before - files_after
            if reduction > 0:
                print(f"   🎉 Files reduced by: {reduction}")
            else:
                print(f"   📊 Files changed by: {reduction}")
        
        # Check logging optimization files
        logging_files = len(list(base_dir.glob("logging_optimization_*.json")))
        print(f"   🗂️  Logging optimization files remaining: {logging_files}")
        
        # Check log files
        logs_dir = base_dir / "logs"
        if logs_dir.exists():
            log_patterns = ["*.log", "*.out", "*.err", "*.jsonl"]
            log_count = 0
            for pattern in log_patterns:
                log_count += len(list(logs_dir.rglob(pattern)))
            print(f"   📝 Log files: {log_count}")
        
    except Exception as e:
        print(f"   ⚠️  Could not get final status: {e}")
    
    # Performance assessment
    print("\n📊 Performance Assessment:")
    try:
        if files_after < 100:
            print("   ✅ EXCELLENT: Root directory is clean and organized")
            print("   🚀 Performance should be dramatically improved")
        elif files_after < 200:
            print("   ✅ GOOD: Root directory is reasonably clean")
            print("   ⚡ Performance should be significantly improved")
        else:
            print("   ⚠️  WARNING: Root directory still has many files")
            print("   💡 Consider additional cleanup")
    except:
        print("   ⚠️  Could not assess performance")
    
    print("\n🎉 Cleanup execution completed!")
    print("📁 Check results in:")
    print("   • quick_cleanup/ (if created)")
    print("   • cleanup_archive/ (if created)")
    
    # Show archive contents if they exist
    for archive_name in ["quick_cleanup", "cleanup_archive"]:
        archive_path = base_dir / archive_name
        if archive_path.exists():
            print(f"\n📂 {archive_name}/ contents:")
            try:
                for item in archive_path.iterdir():
                    if item.is_dir():
                        file_count = len(list(item.rglob("*")))
                        print(f"   📁 {item.name}/ ({file_count} files)")
                    else:
                        print(f"   📄 {item.name}")
            except Exception as e:
                print(f"   ⚠️  Could not list {archive_name}: {e}")

if __name__ == "__main__":
    run_cleanup()
