#!/bin/bash

echo "🤖 WEALTHYROBOT COMPLETE CODE INVENTORY"
echo "======================================="
echo "📅 Generated: $(date)"
echo ""

# Create inventory directory
mkdir -p code_inventory

echo "🔍 SCANNING ALL PYTHON AGENTS..."
echo ""

# Find all Python files and categorize them
echo "📁 MAIN ORCHESTRATION FILES:"
echo "----------------------------"
for file in live_orchestrator.py orchestrator.py main.py master_*.py; do
    if [[ -f "$file" ]]; then
        echo "✅ $file ($(wc -l < "$file") lines)"
        head -20 "$file" | grep -E "(class|def|import)" | head -5
        echo ""
    fi
done

echo "🤖 AGENT FILES:"
echo "---------------"
for file in *agent*.py *_agent.py; do
    if [[ -f "$file" ]]; then
        echo "✅ $file ($(wc -l < "$file") lines)"
        # Show class names and main functions
        grep -E "^class|^def " "$file" | head -5
        echo ""
    fi
done

echo "⏰ SCHEDULER FILES:"
echo "------------------"
for file in *scheduler*.py *_scheduler.py clean_empire*.py; do
    if [[ -f "$file" ]]; then
        echo "✅ $file ($(wc -l < "$file") lines)"
        grep -E "^class|^def " "$file" | head -5
        echo ""
    fi
done

echo "🎨 VISUAL/CONTENT FILES:"
echo "------------------------"
for file in visual*.py content*.py image*.py graphic*.py; do
    if [[ -f "$file" ]]; then
        echo "✅ $file ($(wc -l < "$file") lines)"
        grep -E "^class|^def " "$file" | head -3
        echo ""
    fi
done

echo "⚙️ UTILITY/CONFIG FILES:"
echo "------------------------"
for file in config*.py utils*.py helper*.py bridge*.py integration*.py; do
    if [[ -f "$file" ]]; then
        echo "✅ $file ($(wc -l < "$file") lines)"
        grep -E "^class|^def " "$file" | head -3
        echo ""
    fi
done

echo "📊 CURRENTLY RUNNING PROCESSES:"
echo "-------------------------------"
ps aux | grep python3 | grep -v grep | grep -E "(agent|scheduler|orchestrator)" || echo "❌ No active Python processes found"
echo ""

echo "📋 CONFIGURATION FILES:"
echo "-----------------------"
for file in *.json *.yaml *.yml *.cfg *.ini; do
    if [[ -f "$file" ]]; then
        echo "✅ $file ($(wc -l < "$file") lines)"
        if [[ "$file" == *.json ]]; then
            echo "   Sample: $(head -3 "$file" | tr -d '\n')"
        fi
        echo ""
    fi
done

echo "🗂️ CONTENT & OUTPUT FILES:"
echo "--------------------------"
echo "📝 Thread files: $(ls smart_viral_thread*.txt 2>/dev/null | wc -l)"
echo "🎨 Image files: $(ls *.png *.jpg *.jpeg 2>/dev/null | wc -l)"
echo "📋 Guide files: $(ls *guide*.txt 2>/dev/null | wc -l)"
echo "📊 Log files: $(ls *.log 2>/dev/null | wc -l)"
echo ""

echo "📁 ALL PYTHON FILES:"
echo "--------------------"
ls -la *.py 2>/dev/null | awk '{print $9 " (" $5 " bytes)"}' | head -20
