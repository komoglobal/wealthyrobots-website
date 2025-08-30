#!/bin/bash
# Process Manager Service
# Monitors and optimizes system processes

while true; do
    # Run process optimization
    cd /home/ubuntu/wealthyrobot
    python3 process_optimizer.py --monitor-only

    # Wait before next check
    sleep 600  # 10 minutes
done
