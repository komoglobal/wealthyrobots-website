#!/usr/bin/env python3
"""
Quick Empire Analysis - Shows redundant files and optimization potential
"""

import os
from pathlib import Path
from datetime import datetime

def quick_empire_analysis():
    """Quick analysis of empire redundancy"""
    base_dir = Path("/home/ubuntu/wealthyrobot")
    
    print("🔍 QUICK EMPIRE ANALYSIS")
    print("=" * 50)
    
    # File patterns to check
    patterns = {
        "logging_optimization": "logging_optimization_*.json",
        "agent_coordination": "agent_coordination_log_*.json", 
        "enhanced_reports": "enhanced_visual_test_report_*.json",
        "claude_optimization": "claude_content_optimization_*.json",
        "large_logs": "*.log",
        "jsonl_files": "*.jsonl"
    }
    
    total_files = 0
    total_size_mb = 0
    redundancy_analysis = {}
    
    for pattern_name, pattern in patterns.items():
        files = list(base_dir.glob(pattern))
        if files:
            total_size = sum(f.stat().st_size for f in files)
            size_mb = total_size / (1024 * 1024)
            
            redundancy_analysis[pattern_name] = {
                "count": len(files),
                "size_mb": round(size_mb, 2),
                "files": files[:5]  # Show first 5 files as examples
            }
            
            total_files += len(files)
            total_size_mb += size_mb
    
    print(f"\n📊 REDUNDANCY SUMMARY:")
    print(f"  Total redundant files: {total_files}")
    print(f"  Total size: {total_size_mb:.2f} MB")
    print(f"  Estimated space savings: {total_size_mb * 0.7:.2f} MB (70% compression)")
    
    print(f"\n📋 DETAILED BREAKDOWN:")
    for pattern_name, info in redundancy_analysis.items():
        print(f"\n🔴 {pattern_name.upper()}:")
        print(f"  Count: {info['count']} files")
        print(f"  Size: {info['size_mb']} MB")
        print(f"  Examples:")
        for file_path in info['files']:
            file_size = file_path.stat().st_size / 1024  # KB
            print(f"    • {file_path.name} ({file_size:.1f} KB)")
        if info['count'] > 5:
            print(f"    ... and {info['count'] - 5} more files")
    
    # Show specific optimization recommendations
    print(f"\n🎯 OPTIMIZATION RECOMMENDATIONS:")
    
    if redundancy_analysis.get("logging_optimization", {}).get("count", 0) > 100:
        print(f"  🚨 LOGGING OPTIMIZATION: {redundancy_analysis['logging_optimization']['count']} files")
        print(f"     → These are created every 30 minutes - reduce frequency!")
    
    if redundancy_analysis.get("agent_coordination", {}).get("count", 0) > 100:
        print(f"  🚨 AGENT COORDINATION: {redundancy_analysis['agent_coordination']['count']} files")
        print(f"     → These are created every 30 minutes - reduce frequency!")
    
    if redundancy_analysis.get("large_logs", {}).get("size_mb", 0) > 10:
        print(f"  🚨 LARGE LOGS: {redundancy_analysis['large_logs']['size_mb']} MB")
        print(f"     → Implement log rotation and compression!")
    
    if redundancy_analysis.get("jsonl_files", {}).get("size_mb", 0) > 20:
        print(f"  🚨 JSONL FILES: {redundancy_analysis['jsonl_files']['size_mb']} MB")
        print(f"     → These can be compressed significantly!")
    
    print(f"\n💡 IMMEDIATE ACTIONS:")
    print(f"  1. Run: python empire_optimization_system.py")
    print(f"  2. This will compress and archive redundant files")
    print(f"  3. Create unified logging system")
    print(f"  4. Implement intelligent retention policies")
    
    print(f"\n🚀 PERFORMANCE IMPACT:")
    print(f"  • Cursor will be much more responsive")
    print(f"  • System performance will improve")
    print(f"  • File operations will be faster")
    print(f"  • Trading system will run smoother")
    
    return {
        "total_files": total_files,
        "total_size_mb": total_size_mb,
        "space_savings_potential": total_size_mb * 0.7,
        "redundancy_analysis": redundancy_analysis
    }

if __name__ == "__main__":
    analysis = quick_empire_analysis()
    print(f"\n📋 Analysis Summary: {analysis['total_files']} redundant files, {analysis['total_size_mb']:.2f} MB total")
