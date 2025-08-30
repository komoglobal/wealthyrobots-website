#!/bin/bash

echo "🚀 WealthyRobot Cleanup System - Starting Now!"
echo "================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python3 first."
    exit 1
fi

# Check current directory
echo "📍 Current directory: $(pwd)"
echo "📁 Files before cleanup: $(ls -1 | wc -l | tr -d ' ')"

# Run quick cleanup
echo ""
echo "🔍 Running Quick Cleanup..."
python3 quick_cleanup_now.py

# Check results
echo ""
echo "📊 Quick Cleanup Results:"
if [ -d "quick_cleanup" ]; then
    echo "   ✅ Quick cleanup completed"
    echo "   📁 Archive created: quick_cleanup/"
    echo "   📊 Files processed: $(find quick_cleanup -type f | wc -l)"
else
    echo "   ⚠️  Quick cleanup may not have completed"
fi

# Run comprehensive cleanup
echo ""
echo "🔍 Running Comprehensive Cleanup..."
python3 comprehensive_cleanup.py

# Check results
echo ""
echo "📊 Comprehensive Cleanup Results:"
if [ -d "cleanup_archive" ]; then
    echo "   ✅ Comprehensive cleanup completed"
    echo "   📁 Archive created: cleanup_archive/"
    echo "   📊 Files processed: $(find cleanup_archive -type f | wc -l)"
else
    echo "   ⚠️  Comprehensive cleanup may not have completed"
fi

# Show final status
echo ""
echo "🎯 Final Status:"
echo "   📁 Files in root directory: $(ls -1 | wc -l | tr -d ' ')"
echo "   🗂️  Logging optimization files: $(ls -1 logging_optimization_*.json 2>/dev/null | wc -l | tr -d ' ' || echo "0")"
echo "   📝 Log files: $(find logs -name "*.log" -o -name "*.out" -o -name "*.err" 2>/dev/null | wc -l | tr -d ' ' || echo "0")"

# Performance assessment
echo ""
echo "📊 Performance Assessment:"
if [ $(ls -1 | wc -l | tr -d ' ') -lt 100 ]; then
    echo "   ✅ EXCELLENT: Root directory is clean and organized"
elif [ $(ls -1 | wc -l | tr -d ' ') -lt 200 ]; then
    echo "   ✅ GOOD: Root directory is reasonably clean"
else
    echo "   ⚠️  WARNING: Root directory still has many files"
fi

echo ""
echo "🎉 Cleanup completed! Check the archive directories for results."
echo "📁 Quick cleanup: quick_cleanup/"
echo "📁 Comprehensive cleanup: cleanup_archive/"
