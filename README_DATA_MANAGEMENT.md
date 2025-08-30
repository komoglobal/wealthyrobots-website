# Data Management System for WealthyRobot

## Problem Solved
Your trading system was creating over 100,000 market data snapshot files, causing Cursor to freeze due to file system overload. This system organizes, compresses, and manages your data efficiently.

## Quick Fix (Run Immediately)
```bash
python3 quick_cleanup.py
```

This will:
- Organize existing files into proper directories
- Compress files to save space
- Remove the 100,000+ files from your root directory
- Free up Cursor immediately

## Full System Setup
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the full data management system
python3 data_management_system.py
```

## What This System Does

### 1. **Immediate Relief**
- Moves 100,000+ files from root directory to organized structure
- Compresses files to save 60-80% of disk space
- Creates proper directory hierarchy

### 2. **Prevents Future Problems**
- Limits snapshot frequency (configurable in `data_config.json`)
- Automatic cleanup of old data
- Compression of historical data
- Storage limits and monitoring

### 3. **Organized Structure**
```
market_data/
├── current/           # Latest market data (overwrites)
├── archive/           # Historical data by date
│   ├── 2025-08-11/   # Daily snapshots
│   ├── 2025-08-10/
│   └── ...
└── logs/              # System logs
```

## Configuration

Edit `data_config.json` to control:
- **Snapshot frequency**: How often to save data (default: every 5 minutes)
- **Retention policies**: How long to keep different types of data
- **Storage limits**: Maximum disk usage and file counts
- **Auto-cleanup**: Automatic removal of old data

## Key Features

### Automatic Cleanup
- Runs every hour in background
- Removes files older than retention policy
- Compresses historical data
- Monitors disk usage

### Smart Data Management
- Current data: Always available, overwrites previous
- Hourly snapshots: Kept for 7 days
- Daily snapshots: Kept for 30 days
- Monthly snapshots: Kept for 1 year

### Performance Optimization
- Compressed storage (gzip)
- Batch processing for large file operations
- Background cleanup threads
- Efficient file organization

## Usage Examples

### Get Current Market Data
```python
from data_management_system import DataManager

dm = DataManager()
current_data = dm.get_current_market_data()
```

### Get Historical Data
```python
historical_data = dm.get_historical_data("2025-08-01", "2025-08-10")
```

### Check Storage Stats
```python
stats = dm.get_storage_stats()
print(f"Total files: {stats['total_files']}")
print(f"Total size: {stats['total_size_mb']} MB")
```

## Preventing Future Issues

1. **Run quick_cleanup.py immediately** to fix current problem
2. **Use DataManager.save_market_data()** instead of direct file creation
3. **Set appropriate snapshot frequency** in config (not every second!)
4. **Enable auto-cleanup** to prevent accumulation
5. **Monitor storage stats** regularly

## Emergency Commands

If you need to quickly free space:
```bash
# Find all snapshot files
find . -name "market_data_snapshot_*.json" | wc -l

# Quick cleanup
python3 quick_cleanup.py

# Check space saved
du -sh market_data/
```

## Integration with Trading System

Replace your current file creation code with:
```python
from data_management_system import DataManager

dm = DataManager()

# Instead of creating individual files
dm.save_market_data(market_data, "current")
```

This will prevent the file explosion that was causing Cursor to freeze.
