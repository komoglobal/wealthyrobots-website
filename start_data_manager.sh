#!/bin/bash
# Startup script for WealthyRobot Data Management System

echo "Starting WealthyRobot Data Management System..."

# Activate virtual environment
source data_env/bin/activate

# Start data management system in background
nohup python data_management_system.py > data_manager.log 2>&1 &

# Get the process ID
PID=$!
echo "Data Manager started with PID: $PID"
echo "PID saved to data_manager.pid"

# Save PID to file for easy management
echo $PID > data_manager.pid

echo "Data Manager is now running in background"
echo "Check status with: ps aux | grep data_management_system"
echo "View logs with: tail -f data_manager.log"
echo "Stop with: kill \$(cat data_manager.pid)"
