#!/bin/bash

# WealthyRobot Real-Time Monitoring Dashboard
# Provides live updates on system status and performance

clear
echo "🚀 WEALTHYROBOT REAL-TIME MONITORING DASHBOARD"
echo "=============================================="
echo "Press Ctrl+C to exit"
echo ""

# Function to display service status with colors
display_service_status() {
    local service_name=$1
    local display_name=$2
    
    if systemctl is-active --quiet $service_name; then
        echo -e "  🟢 $display_name: RUNNING"
        
        # Get uptime
        local uptime=$(systemctl show $service_name --property=ActiveEnterTimestamp | cut -d= -f2)
        if [ ! -z "$uptime" ]; then
            local uptime_seconds=$(date -d "$uptime" +%s)
            local current_seconds=$(date +%s)
            local uptime_duration=$((current_seconds - uptime_seconds))
            local hours=$((uptime_duration / 3600))
            local minutes=$(((uptime_duration % 3600) / 60))
            echo -e "     ⏱️  Uptime: ${hours}h ${minutes}m"
        fi
        
        # Get resource usage
        local status=$(systemctl status $service_name --no-pager | head -20)
        local memory=$(echo "$status" | grep "Memory:" | awk '{print $2}')
        local cpu=$(echo "$status" | grep "CPU:" | awk '{print $2}')
        
        if [ ! -z "$memory" ]; then
            echo -e "     💾 Memory: $memory"
        fi
        if [ ! -z "$cpu" ]; then
            echo -e "     ⚡ CPU: $cpu"
        fi
        
    else
        echo -e "  🔴 $display_name: STOPPED"
    fi
}

# Function to display system resources
display_system_resources() {
    echo -e "\n💻 SYSTEM RESOURCES"
    echo -e "------------------"
    
    # CPU usage with color coding
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    local cpu_int=${cpu_usage%.*}
    
    if [ $cpu_int -lt 50 ]; then
        echo -e "  🟢 CPU Usage: ${cpu_usage}%"
    elif [ $cpu_int -lt 80 ]; then
        echo -e "  🟡 CPU Usage: ${cpu_usage}%"
    else
        echo -e "  🔴 CPU Usage: ${cpu_usage}%"
    fi
    
    # Memory usage with color coding
    local mem_info=$(free -h | grep Mem)
    local mem_total=$(echo $mem_info | awk '{print $2}')
    local mem_used=$(echo $mem_info | awk '{print $3}')
    local mem_free=$(echo $mem_info | awk '{print $4}')
    local mem_percent=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
    local mem_int=${mem_percent%.*}
    
    if [ $mem_int -lt 70 ]; then
        echo -e "  🟢 Memory: $mem_used / $mem_total (Free: $mem_free)"
    elif [ $mem_int -lt 90 ]; then
        echo -e "  🟡 Memory: $mem_used / $mem_total (Free: $mem_free)"
    else
        echo -e "  🔴 Memory: $mem_used / $mem_total (Free: $mem_free)"
    fi
    
    # Disk usage with color coding
    local disk_usage=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
    local disk_available=$(df -h / | tail -1 | awk '{print $4}')
    
    if [ $disk_usage -lt 80 ]; then
        echo -e "  🟢 Disk: ${disk_usage}% used (Available: $disk_available)"
    elif [ $disk_usage -lt 95 ]; then
        echo -e "  🟡 Disk: ${disk_usage}% used (Available: $disk_available)"
    else
        echo -e "  🔴 Disk: ${disk_usage}% used (Available: $disk_available)"
    fi
    
    # Load average
    local load_avg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    local load_float=$(echo $load_avg | awk '{print $1}')
    local load_int=${load_float%.*}
    
    if [ $load_int -lt 1 ]; then
        echo -e "  🟢 Load Average: $load_avg"
    elif [ $load_int -lt 3 ]; then
        echo -e "  🟡 Load Average: $load_avg"
    else
        echo -e "  🔴 Load Average: $load_avg"
    fi
}

# Function to display agent status
display_agent_status() {
    echo -e "\n🤖 AGENT STATUS"
    echo -e "---------------"
    
    # Count Python processes
    local python_processes=$(ps aux | grep python | grep -v grep | wc -l)
    echo -e "  🐍 Python Processes: $python_processes"
    
    # Check agent bridge health
    if [ -f "logs/bridge_health_$(date +%Y%m%d).json" ]; then
        local last_health=$(tail -1 "logs/bridge_health_$(date +%Y%m%d).json" 2>/dev/null)
        if [ ! -z "$last_health" ]; then
            local healthy_agents=$(echo "$last_health" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('healthy_agents', 0))" 2>/dev/null)
            local unhealthy_agents=$(echo "$last_health" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('unhealthy_agents', 0))" 2>/dev/null)
            
            if [ ! -z "$healthy_agents" ] && [ ! -z "$unhealthy_agents" ]; then
                local total_agents=$((healthy_agents + unhealthy_agents))
                local health_percent=$((healthy_agents * 100 / total_agents))
                
                if [ $health_percent -gt 80 ]; then
                    echo -e "  🟢 Agent Health: $healthy_agents/$total_agents healthy ($health_percent%)"
                elif [ $health_percent -gt 50 ]; then
                    echo -e "  🟡 Agent Health: $healthy_agents/$total_agents healthy ($health_percent%)"
                else
                    echo -e "  🔴 Agent Health: $healthy_agents/$total_agents healthy ($health_percent%)"
                fi
            fi
        fi
    fi
    
    # Check for recent agent activity
    if [ -f "logs/agent_bridge_$(date +%Y%m%d).log" ]; then
        local last_activity=$(tail -1 "logs/agent_bridge_$(date +%Y%m%d).log" 2>/dev/null)
        if [ ! -z "$last_activity" ]; then
            local timestamp=$(echo "$last_activity" | awk '{print $1, $2}')
            echo -e "  📝 Last Activity: $timestamp"
        fi
    fi
}

# Function to display recent logs
display_recent_logs() {
    echo -e "\n📝 RECENT ACTIVITY"
    echo -e "-----------------"
    
    # Get recent trading fund logs
    local trading_logs=$(journalctl -u autonomous-trading-fund.service -n 2 --no-pager 2>/dev/null | grep -E "(INFO|ERROR|WARNING)" | tail -2)
    if [ ! -z "$trading_logs" ]; then
        echo -e "  🚀 Trading Fund:"
        echo "$trading_logs" | while read line; do
            echo -e "     $line"
        done
    fi
    
    # Get recent agent bridge logs
    local bridge_logs=$(journalctl -u agent-bridge.service -n 2 --no-pager 2>/dev/null | grep -E "(INFO|ERROR|WARNING)" | tail -2)
    if [ ! -z "$bridge_logs" ]; then
        echo -e "  🌉 Agent Bridge:"
        echo "$bridge_logs" | while read line; do
            echo -e "     $line"
        done
    fi
}

# Function to display network status
display_network_status() {
    echo -e "\n🌐 NETWORK STATUS"
    echo -e "-----------------"
    
    # Check internet connectivity
    if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
        echo -e "  🟢 Internet: Connected"
    else
        echo -e "  🔴 Internet: Disconnected"
    fi
    
    # Check local network
    if ping -c 1 127.0.0.1 >/dev/null 2>&1; then
        echo -e "  🟢 Local Network: Active"
    else
        echo -e "  🔴 Local Network: Inactive"
    fi
    
    # Check if services are listening
    local trading_port=$(netstat -tlnp 2>/dev/null | grep python | grep -E "(trading|fund)" | head -1)
    if [ ! -z "$trading_port" ]; then
        echo -e "  🔌 Trading Service: Active"
    fi
}

# Function to display summary
display_summary() {
    echo -e "\n📋 SYSTEM SUMMARY"
    echo -e "----------------"
    
    local total_services=2
    local active_services=0
    
    if systemctl is-active --quiet unified-trading-system.service; then
        ((active_services++))
    fi
    
    if systemctl is-active --quiet agent-bridge.service; then
        ((active_services++))
    fi
    
    if [ $active_services -eq $total_services ]; then
        echo -e "  🟢 Overall Status: HEALTHY"
    elif [ $active_services -gt 0 ]; then
        echo -e "  🟡 Overall Status: PARTIALLY HEALTHY"
    else
        echo -e "  🔴 Overall Status: UNHEALTHY"
    fi
    
    echo -e "  🚀 Services: $active_services/$total_services active"
    echo -e "  ⏰ Last Update: $(date '+%H:%M:%S')"
}

# Main dashboard loop
main() {
    while true; do
        # Clear screen and show header
        clear
        echo -e "🚀 WEALTHYROBOT REAL-TIME MONITORING DASHBOARD"
        echo -e "=============================================="
        echo -e "Press Ctrl+C to exit | Auto-refresh every 10 seconds"
        echo -e ""
        
        # Display service status
        echo -e "🔧 SERVICE STATUS"
        echo -e "----------------"
        display_service_status "unified-trading-system.service" "Unified Trading System"
        display_service_status "agent-bridge.service" "Agent Integration Bridge"
        
        # Display system resources
        display_system_resources
        
        # Display agent status
        display_agent_status
        
        # Display network status
        display_network_status
        
        # Display recent logs
        display_recent_logs
        
        # Display summary
        display_summary
        
        # Wait before next update
        sleep 10
    done
}

# Handle Ctrl+C gracefully
trap 'echo -e "\n\n🛑 Dashboard stopped. Goodbye!"; exit 0' INT

# Start the dashboard
main "$@"
