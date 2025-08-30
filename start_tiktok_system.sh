#!/bin/bash
# Start Automated TikTok System

echo "🎬 Starting Automated TikTok Profit System..."
echo "============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking required packages..."
python3 -c "import schedule, cv2, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required packages..."
    pip3 install schedule opencv-python pillow requests
fi

# Start the system
echo "🚀 Starting automation..."
python3 automated_tiktok_orchestrator.py
