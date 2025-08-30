#!/usr/bin/env python3
"""
Quick cleanup script to immediately organize existing market data files
Run this to quickly free up space and organize your data
"""

import os
import shutil
import gzip
from pathlib import Path
from datetime import datetime
import json

def quick_cleanup():
    """Quick cleanup of existing market data files"""
    base_dir = Path("/home/ubuntu/wealthyrobot")
    
    # Create organized directory structure
    data_dir = base_dir / "market_data"
    archive_dir = data_dir / "archive"
    current_dir = data_dir / "current"
    
    for directory in [data_dir, archive_dir, current_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("Created organized directory structure")
    
    # Find all market data snapshot files
    snapshot_files = list(base_dir.glob("market_data_snapshot_*.json"))
    print(f"Found {len(snapshot_files)} snapshot files to organize")
    
    if not snapshot_files:
        print("No snapshot files found")
        return
    
    # Group files by date and compress them
    files_by_date = {}
    for file_path in snapshot_files:
        try:
            # Extract date from filename
            date_str = file_path.stem.split('_')[-2]
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            date_key = date_obj.strftime("%Y-%m-%d")
            
            if date_key not in files_by_date:
                files_by_date[date_key] = []
            files_by_date[date_key].append(file_path)
        except Exception as e:
            print(f"Warning: Could not parse date from {file_path}: {e}")
            continue
    
    # Process files in batches to avoid memory issues
    batch_size = 1000
    total_processed = 0
    
    for date_key, files in files_by_date.items():
        date_dir = archive_dir / date_key
        date_dir.mkdir(exist_ok=True)
        
        print(f"Processing {len(files)} files for {date_key}")
        
        for i, file_path in enumerate(files):
            try:
                # Compress file
                compressed_path = date_dir / f"{file_path.stem}.json.gz"
                
                with open(file_path, 'rb') as source:
                    with gzip.open(compressed_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
                
                # Remove original file
                file_path.unlink()
                total_processed += 1
                
                # Progress update
                if total_processed % batch_size == 0:
                    print(f"Processed {total_processed} files...")
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    print(f"Successfully organized {total_processed} files")
    
    # Move current market data to current directory
    current_file = base_dir / "current_market_data.json"
    if current_file.exists():
        shutil.move(str(current_file), str(current_dir / "current_market_data.json"))
        print("Moved current market data to organized structure")
    
    # Calculate space saved
    original_size = sum(f.stat().st_size for f in snapshot_files if f.exists())
    compressed_size = sum(f.stat().st_size for f in archive_dir.rglob("*.gz"))
    
    print(f"Original size: {original_size / (1024*1024):.2f} MB")
    print(f"Compressed size: {compressed_size / (1024*1024):.2f} MB")
    print(f"Space saved: {(original_size - compressed_size) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    print("Starting quick cleanup of market data files...")
    quick_cleanup()
    print("Quick cleanup completed!")
