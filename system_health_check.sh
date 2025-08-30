#!/bin/bash

# WealthyRobot System Health Check Script
# Monitors all services and provides comprehensive system status

echo "🏥 WEALTHYROBOT SYSTEM HEALTH CHECK"
echo "=================================="
echo "Timestamp: $(date)"
echo ""

# Function to check service status
check_service() {
    local service_name=$1
    local display_name=$2
    
    echo "🔍 Checking $display_name..."
    if systemctl is-active --quiet $service_name; then
        echo "  ✅ Status: ACTIVE"
        
        # Get service details
        local status=$(systemctl status $service_name --no-pager | head -20)
        local pid=$(echo "$status" | grep "Main PID:" | awk '{print $3}')
        local memory=$(echo "$status" | grep "Memory:" | awk '{print $2}')
        local cpu=$(echo "$status" | grep "CPU:" | awk '{print $2}')
        
        echo "  📊 PID: $pid"
        echo "  💾 Memory: $memory"
        echo "  ⚡ CPU: $cpu"
        
        # Check recent logs
        echo "  📝 Recent Activity:"
        journalctl -u $service_name -n 3 --no-pager | grep -E "(INFO|ERROR|WARNING)" | tail -3 | while read line; do
            echo "    $line"
        done
        
    else
        echo "  ❌ Status: INACTIVE"
        echo "  🔧 Attempting to start..."
        sudo systemctl start $service_name
        sleep 2
        
        if systemctl is-active --quiet $service_name; then
            echo "  ✅ Service started successfully"
        else
            echo "  ❌ Failed to start service"
        fi
    fi
    echo ""
}

# Function to check system resources
check_system_resources() {
    echo "💻 SYSTEM RESOURCES"
    echo "------------------"
    
    # CPU usage
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    echo "  ⚡ CPU Usage: ${cpu_usage}%"
    
    # Memory usage
    local mem_info=$(free -h | grep Mem)
    local mem_total=$(echo $mem_info | awk '{print $2}')
    local mem_used=$(echo $mem_info | awk '{print $3}')
    local mem_free=$(echo $mem_info | awk '{print $4}')
    echo "  💾 Memory: $mem_used / $mem_total (Free: $mem_free)"
    
    # Disk usage
    local disk_usage=$(df -h / | tail -1 | awk '{print $5}')
    local disk_available=$(df -h / | tail -1 | awk '{print $4}')
    echo "  💿 Disk Usage: $disk_usage (Available: $disk_available)"
    
    # Load average
    local load_avg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}')
    echo "  📈 Load Average: $load_avg"
    echo ""
}

# Function to check trading system logs
check_trading_logs() {
    echo "📊 TRADING SYSTEM LOGS"
    echo "---------------------"
    
    # Check recent trading activity
    if [ -f "logs/autonomous_trading_fund_$(date +%Y%m%d).log" ]; then
        echo "  📝 Recent Trading Activity:"
        tail -5 "logs/autonomous_trading_fund_$(date +%Y%m%d).log" | while read line; do
            echo "    $line"
        done
    else
        echo "  ⚠️  No trading logs found for today"
    fi
    
    # Check agent bridge logs
    if [ -f "logs/agent_bridge_$(date +%Y%m%d).log" ]; then
        echo "  🌉 Recent Agent Bridge Activity:"
        tail -3 "logs/agent_bridge_$(date +%Y%m%d).log" | while read line; do
            echo "    $line"
        done
    else
        echo "  ⚠️  No agent bridge logs found for today"
    fi
    echo ""
}

# Function to check agent status
check_agent_status() {
    echo "🤖 AGENT STATUS OVERVIEW"
    echo "-----------------------"
    
    # Count Python processes
    local python_processes=$(ps aux | grep python | grep -v grep | wc -l)
    echo "  🐍 Python Processes: $python_processes"
    
    # Check for specific agent files
    local agent_files=$(find . -name "*_agent.py" -o -name "*_system.py" | wc -l)
    echo "  📁 Agent Files: $agent_files"
    
    # Check recent agent health status
    if [ -f "logs/bridge_health_$(date +%Y%m%d).json" ]; then
        echo "  🏥 Recent Health Check:"
        tail -1 "logs/bridge_health_$(date +%Y%m%d).json" | python3 -m json.tool 2>/dev/null | grep -E "(healthy_agents|unhealthy_agents)" | while read line; do
            echo "    $line"
        done
    fi
    echo ""
}

# Function to check network connectivity
check_network() {
    echo "🌐 NETWORK CONNECTIVITY"
    echo "----------------------"
    
    # Check internet connectivity
    if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
        echo "  ✅ Internet: Connected"
    else
        echo "  ❌ Internet: Disconnected"
    fi
    
    # Check local network
    if ping -c 1 127.0.0.1 >/dev/null 2>&1; then
        echo "  ✅ Local Network: Active"
    else
        echo "  ❌ Local Network: Inactive"
    fi
    
    # Check listening ports
    echo "  🔌 Listening Ports:"
    netstat -tlnp 2>/dev/null | grep LISTEN | head -5 | while read line; do
        echo "    $line"
    done
    echo ""
}

# Function to check file system
check_file_system() {
    echo "📁 FILE SYSTEM STATUS"
    echo "-------------------"
    
    # Check log directory
    if [ -d "logs" ]; then
        local log_count=$(find logs -name "*.log" | wc -l)
        local log_size=$(du -sh logs 2>/dev/null | awk '{print $1}')
        echo "  📝 Logs: $log_count files, $log_size"
    else
        echo "  ⚠️  Logs directory not found"
    fi
    
    # Check data directory
    if [ -d "data" ]; then
        local data_size=$(du -sh data 2>/dev/null | awk '{print $1}')
        echo "  💾 Data: $data_size"
    else
        echo "  ⚠️  Data directory not found"
    fi
    
    # Check backup directory
    if [ -d "backups" ]; then
        local backup_count=$(find backups -type f | wc -l)
        local backup_size=$(du -sh backups 2>/dev/null | awk '{print $1}')
        echo "  💿 Backups: $backup_count files, $backup_size"
    else
        echo "  ⚠️  Backups directory not found"
    fi
    echo ""
}

# Function to generate summary
generate_summary() {
    echo "📋 SYSTEM SUMMARY"
    echo "----------------"
    
    local total_services=2
    local active_services=0
    
    if systemctl is-active --quiet unified-trading-system.service; then
        ((active_services++))
    fi
    
    if systemctl is-active --quiet agent-bridge.service; then
        ((active_services++))
    fi
    
    echo "  🚀 Services: $active_services/$total_services active"
    
    # Check overall system health
    if [ $active_services -eq $total_services ]; then
        echo "  🟢 Overall Status: HEALTHY"
    elif [ $active_services -gt 0 ]; then
        echo "  🟡 Overall Status: PARTIALLY HEALTHY"
    else
        echo "  🔴 Overall Status: UNHEALTHY"
    fi
    
    echo "  ⏰ Last Check: $(date)"
    echo ""
}

# Main execution
main() {
    echo "Starting comprehensive system health check..."
    echo ""
    
    # Check all services
    check_service "unified-trading-system.service" "Unified Trading System"
    check_service "agent-bridge.service" "Agent Integration Bridge"
    
    # Check system resources
    check_system_resources
    
    # Check trading logs
    check_trading_logs
    
    # Check agent status
    check_agent_status
    
    # Check network
    check_network
    
    # Check file system
    check_file_system
    
    # Generate summary
    generate_summary
    
    echo "✅ Health check completed!"
}

# Run main function
main "$@"


