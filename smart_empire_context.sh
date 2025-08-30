#!/bin/bash
# Smart Empire Context with Agent Coordination Awareness

echo "🏰 WEALTHYROBOT EMPIRE - INTELLIGENT CONTEXT"
echo "Generated: $(date)"
echo "==========================================================="

# Function to extract agent documentation
extract_agent_info() {
    local file="$1"
    if grep -q "EMPIRE_AGENT_INFO:" "$file" 2>/dev/null; then
        local purpose=$(grep -A10 "EMPIRE_AGENT_INFO:" "$file" | grep "PURPOSE:" | cut -d: -f2- | sed 's/^ *//')
        local status=$(grep -A10 "EMPIRE_AGENT_INFO:" "$file" | grep "STATUS:" | cut -d: -f2- | sed 's/^ *//')
        if [ -n "$purpose" ]; then
            echo "- $file: $purpose (Status: $status)"
        else
            echo "- $file: [Self-documentation incomplete]"
        fi
    else
        # Intelligent fallback based on coordination patterns
        case "$file" in
            *orchestrator*) echo "- $file: 🎛️ COORDINATOR - Master agent workflow management" ;;
            *ceo*) echo "- $file: 🎯 COORDINATOR - Strategic decisions and budget control" ;;
            *operations_manager*) echo "- $file: 📊 COORDINATOR - Operations oversight and monitoring" ;;
            *universal*coordinator*) echo "- $file: 🔄 COORDINATOR - Universal agent coordination" ;;
            *social_media*) echo "- $file: 📱 EXECUTOR - Twitter posting and engagement" ;;
            *revenue*|*money*) echo "- $file: 💰 EXECUTOR - Revenue tracking and optimization" ;;
            *visual*) echo "- $file: 🎨 EXECUTOR - Visual content and graphics creation" ;;
            *analytics*) echo "- $file: 📈 EXECUTOR - Performance analysis and insights" ;;
            *content*) echo "- $file: 📝 EXECUTOR - Content creation and optimization" ;;
            *affiliate*) echo "- $file: 💰 EXECUTOR - Affiliate link management and tracking" ;;
            *scheduler*) echo "- $file: ⏰ COORDINATOR - Task scheduling and timing" ;;
            *) echo "- $file: ❓ UNKNOWN - [Needs EMPIRE_AGENT_INFO documentation]" ;;
        esac
    fi
}

echo ""
echo "🚨 CURRENT OPERATIONAL STATUS:"
if [ -f live_config.json ] && grep -q '"emergency_mode": true' live_config.json; then
    echo "- 🚨 EMERGENCY MODE ACTIVE - Automation paused due to Twitter restrictions"
elif [ -f live_config.json ] && grep -q '"posting_enabled": false' live_config.json; then
    echo "- ⚠️ POSTING DISABLED - Manual mode required"
else
    echo "- ✅ Systems operational"
fi
echo "- Posts created today: $(ls smart_viral_thread_$(date +%Y%m%d)*.txt 2>/dev/null | wc -l)"
echo "- Active processes: $(ps aux | grep -E "(orchestrator|agent)" | grep -v grep | wc -l)"
echo "- Recent activity: $(find . -name "*.json" -o -name "*.log" -mtime -1 | wc -l) files modified in 24h"

echo ""
echo "🎛️ COORDINATION LAYER (Master Controllers):"
for agent in live_orchestrator.py ultimate_ceo_agent.py operations_manager*.py universal*coordinator*.py *scheduler*.py; do
    [ -f "$agent" ] && extract_agent_info "$agent"
done

echo ""
echo "⚡ EXECUTION LAYER (Specialized Workers):"
echo ""
echo "📱 Content & Social Media:"
for agent in social_media_agent.py content_agent.py dynamic_content_selector.py twitter_posting_agent.py content_optimizer_agent.py; do
    [ -f "$agent" ] && extract_agent_info "$agent"
done

echo ""
echo "💰 Revenue & Affiliate:"
for agent in smart_affiliate_agent.py real_money_agent.py revenue_booster_agent.py conversion_tracker_agent.py; do
    [ -f "$agent" ] && extract_agent_info "$agent"
done

echo ""
echo "🎨 Visual & Creative:"
for agent in visual_affiliate_agent.py visual_content_agent.py ai_image_generator_agent.py twitter_visual_enhancement.py; do
    [ -f "$agent" ] && extract_agent_info "$agent"
done

echo ""
echo "📈 Analytics & Intelligence:"
for agent in data_analytics_agent.py real_time_analytics_agent.py market_research_agent.py competitor_analysis_agent.py; do
    [ -f "$agent" ] && extract_agent_info "$agent"
done

echo ""
echo "👥 Customer & Engagement:"
for agent in customer_service_agent.py lead_generation_agent.py influencer_outreach_agent.py; do
    [ -f "$agent" ] && extract_agent_info "$agent"
done

echo ""
echo "🔧 Technical & Infrastructure:"
for agent in code_debug_agent.py payment_integration_agent.py seo_optimizer_agent.py email_marketing_agent.py; do
    [ -f "$agent" ] && extract_agent_info "$agent"
done

echo ""
echo "🔄 AGENT COORDINATION STATUS:"
if [ -f live_orchestrator.py ] && ps aux | grep -q "live_orchestrator.py"; then
    echo "✅ Master Orchestrator: RUNNING"
else
    echo "❌ Master Orchestrator: STOPPED"
fi

if [ -f ultimate_ceo_agent.py ]; then
    echo "✅ CEO Agent: Available for strategic decisions"
else
    echo "❌ CEO Agent: Missing"
fi

# Check for coordination health
coordination_health="Good"
if [ $(ps aux | grep -E "(orchestrator|ceo)" | grep -v grep | wc -l) -eq 0 ]; then
    coordination_health="CRITICAL - No coordination agents running"
elif [ ! -f live_config.json ]; then
    coordination_health="WARNING - Missing configuration"
fi

echo "🏥 Coordination Health: $coordination_health"

echo ""
echo "💰 BUSINESS MODEL:"
echo "- Platform: Twitter (@WealthyRobot)"
echo "- Strategy: Autonomous affiliate marketing empire"
echo "- Content Ratio: 80% educational value, 20% affiliate promotion"
echo "- Target Product: 'The AI Advantage' book ($19.99)"
echo "- Amazon Affiliate ID: wealthyrobot-20"
echo "- Commission Rate: 8% per sale"

echo ""
echo "📝 LATEST CONTENT CREATED:"
ls -lt smart_viral_thread*.txt 2>/dev/null | head -3 | awk '{print "- " $9 " (created " $6 " " $7 " " $8 ")"}'

echo ""
echo "🎯 IMMEDIATE PRIORITIES FOR CLAUDE:"
if grep -q "emergency_mode.*true\|posting_enabled.*false" live_config.json 2>/dev/null; then
    echo "1. 🚨 URGENT: Address Twitter restrictions & account recovery"
    echo "2. 📝 Switch to manual posting strategy"
    echo "3. 🔍 Analyze what triggered platform manipulation flag"
    echo "4. 🛠️ Implement compliant automation approach"
else
    echo "1. 📊 Analyze recent performance and optimize top-performing content"
    echo "2. 💰 Review revenue generation and conversion rates"
    echo "3. 🎯 Enhance content strategy based on engagement data"
    echo "4. 🔧 Check for any system errors or optimization opportunities"
fi

echo ""
echo "🔧 QUICK DIAGNOSTICS:"
echo "- Check orchestrator status: python3 live_orchestrator.py --status"
echo "- View live config: cat live_config.json | jq"
echo "- Recent system logs: tail -20 *.log"
echo "- Active processes: ps aux | grep -E '(orchestrator|agent)'"
echo "- Recent content: ls -lt smart_viral_thread*.txt | head -5"

echo ""
echo "=========================================================="
echo "💡 This intelligent context shows coordination hierarchy,"
echo "   agent self-documentation, and real-time system status"
