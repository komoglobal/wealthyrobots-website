#!/bin/bash
# Stop Automated TikTok System

echo "⏹️ Stopping Automated TikTok Profit System..."

# Find and kill the orchestrator process
pkill -f "automated_tiktok_orchestrator.py"

echo "✅ System stopped"
