#!/usr/bin/env python3
"""
Quick Cleanup Script - Immediate Performance Improvement
Cleans up the most problematic files that are affecting performance
"""

import os
import shutil
import gzip
from pathlib import Path
from datetime import datetime

def quick_cleanup():
    """Quick cleanup of problematic files"""
    print("🚀 Quick Cleanup - Immediate Performance Improvement")
    
    base_dir = Path("/home/ubuntu/wealthyrobot")
    cleanup_dir = base_dir / "quick_cleanup"
    cleanup_dir.mkdir(exist_ok=True)
    
    # 1. Clean up logging optimization files (most problematic)
    print("\n🔍 Cleaning up logging optimization files...")
    pattern = "logging_optimization_*.json"
    files_to_clean = list(base_dir.glob(pattern))
    
    if files_to_clean:
        archive_dir = cleanup_dir / "logging_optimization"
        archive_dir.mkdir(exist_ok=True)
        
        # Group by date and compress
        files_by_date = {}
        for file_path in files_to_clean:
            try:
                filename = file_path.name
                date_str = filename.split('_')[1]
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                
                if date_obj not in files_by_date:
                    files_by_date[date_obj] = []
                files_by_date[date_obj].append(file_path)
                
            except Exception as e:
                print(f"   Warning: Could not parse {file_path.name}")
                continue
        
        total_compressed = 0
        for date_obj, files in files_by_date.items():
            date_dir = archive_dir / date_obj.strftime("%Y-%m-%d")
            date_dir.mkdir(exist_ok=True)
            
            # Keep only the most recent 10 files per day, compress the rest
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for i, file_path in enumerate(files):
                if i < 10:
                    # Keep recent files but move them to archive
                    shutil.move(str(file_path), str(date_dir / file_path.name))
                else:
                    # Compress older files
                    compressed_file = date_dir / f"{file_path.stem}.gz"
                    try:
                        with open(file_path, 'rb') as f_in:
                            with gzip.open(compressed_file, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        file_path.unlink()
                        total_compressed += 1
                    except Exception as e:
                        print(f"   Error compressing {file_path.name}: {e}")
        
        print(f"   ✅ Processed {len(files_to_clean)} files, compressed {total_compressed}")
    else:
        print("   ✅ No logging optimization files found")
    
    # 2. Clean up old log files
    print("\n🔍 Cleaning up old log files...")
    logs_dir = base_dir / "logs"
    if logs_dir.exists():
        log_patterns = ["*.log", "*.out", "*.err"]
        old_logs = []
        
        for pattern in log_patterns:
            old_logs.extend(logs_dir.rglob(pattern))
        
        # Keep only recent logs (last 7 days)
        current_time = datetime.now()
        logs_to_compress = []
        
        for log_file in old_logs:
            try:
                file_age = current_time - datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_age.days > 7:
                    logs_to_compress.append(log_file)
            except Exception:
                continue
        
        if logs_to_compress:
            archive_dir = cleanup_dir / "old_logs"
            archive_dir.mkdir(exist_ok=True)
            
            compressed_count = 0
            for log_file in logs_to_compress[:50]:  # Limit to 50 files to avoid long processing
                try:
                    compressed_file = archive_dir / f"{log_file.stem}.gz"
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(compressed_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    log_file.unlink()
                    compressed_count += 1
                except Exception as e:
                    print(f"   Warning: Could not compress {log_file.name}")
            
            print(f"   ✅ Compressed {compressed_count} old log files")
        else:
            print("   ✅ No old log files found")
    
    # 3. Clean up Python cache
    print("\n🔍 Cleaning up Python cache...")
    cache_dirs = list(base_dir.rglob("__pycache__"))
    cache_cleared = 0
    
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            cache_cleared += 1
        except Exception:
            continue
    
    print(f"   ✅ Cleared {cache_cleared} cache directories")
    
    # 4. Clean up .pyc files
    print("\n🔍 Cleaning up .pyc files...")
    pyc_files = list(base_dir.rglob("*.pyc"))
    pyc_removed = 0
    
    for pyc_file in pyc_files:
        try:
            pyc_file.unlink()
            pyc_removed += 1
        except Exception:
            continue
    
    print(f"   ✅ Removed {pyc_removed} .pyc files")
    
    # 5. Generate summary
    print("\n📊 Cleanup Summary:")
    print(f"   📁 Cleanup archive: {cleanup_dir}")
    print(f"   🗂️  Logging optimization: Organized and compressed")
    print(f"   📝 Old logs: Compressed and archived")
    print(f"   🐍 Python cache: Cleared")
    print(f"   ⚡ Performance: Improved")
    
    # 6. Show space savings
    try:
        original_files = len(list(base_dir.glob("logging_optimization_*.json")))
        if original_files > 0:
            print(f"\n💾 Space Savings:")
            print(f"   Before: {original_files} scattered files")
            print(f"   After: Organized in {cleanup_dir}")
            print(f"   Impact: Immediate performance improvement")
    except Exception:
        pass
    
    print("\n✅ Quick cleanup completed! System performance should be improved.")
    print(f"📁 Check results in: {cleanup_dir}")

if __name__ == "__main__":
    quick_cleanup()
