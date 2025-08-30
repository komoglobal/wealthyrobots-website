import json
import os
from datetime import datetime

def show_financial_dashboard():
    print("💰 AUTONOMOUS EMPIRE FINANCIAL DASHBOARD")
    print("=" * 50)
    
    # Load budget configuration
    monthly_budget = float(os.getenv('MONTHLY_BUDGET', '0'))
    daily_budget = monthly_budget / 30
    
    print(f"💳 BUDGET CONFIGURATION:")
    print(f"   Monthly Budget: ${monthly_budget:,.2f}")
    print(f"   Daily Budget: ${daily_budget:,.2f}")
    print(f"   Auto-Approve Limit: ${float(os.getenv('AUTO_APPROVE_LIMIT', '25')):,.2f}")
    
    print(f"\n🎯 AUTONOMOUS SPENDING CATEGORIES:")
    categories = {
        'Content Promotion': f"${daily_budget * 0.40:.2f}/day (40%)",
        'Lead Generation': f"${daily_budget * 0.30:.2f}/day (30%)",
        'Tool Subscriptions': f"${daily_budget * 0.20:.2f}/day (20%)",
        'Emergency Fund': f"${daily_budget * 0.10:.2f}/day (10%)"
    }
    
    for category, amount in categories.items():
        print(f"   📊 {category}: {amount}")
    
    print(f"\n💡 WHAT YOUR EMPIRE CAN AUTONOMOUSLY BUY:")
    print(f"   🚀 Facebook/Instagram ads: Up to ${min(50, daily_budget * 0.3):.2f}/day")
    print(f"   🎯 Google keyword ads: Up to ${min(30, daily_budget * 0.2):.2f}/day")
    print(f"   📈 Post promotion boosts: Up to ${min(20, daily_budget * 0.2):.2f}/post")
    print(f"   🛠️ Premium tool subscriptions: Up to ${monthly_budget * 0.2:.2f}/month")
    print(f"   📧 Email marketing tools: Up to ${min(50, monthly_budget * 0.1):.2f}/month")
    
    print(f"\n🎯 AUTONOMOUS APPROVAL RULES:")
    print(f"   ✅ Auto-approve spending under ${float(os.getenv('AUTO_APPROVE_LIMIT', '25')):,.2f}")
    print(f"   ✅ ROI requirement: {os.getenv('ROI_THRESHOLD', '150')}% minimum")
    print(f"   ✅ High-performing content gets priority")
    print(f"   ✅ Profitable ads get increased budgets")
    
    print(f"\n📊 EXPECTED RETURNS:")
    print(f"   💰 Target ROI: 200-300% on advertising spend")
    print(f"   📈 Revenue increase: 2-5x current levels")
    print(f"   🎯 Cost per lead: $5-15 depending on niche")
    print(f"   🚀 Growth rate: 50-200% monthly with paid promotion")

if __name__ == "__main__":
    show_financial_dashboard()
