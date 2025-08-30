#!/usr/bin/env python3
"""
Show the detailed AGI response with all strategies and their ethical status
"""

import json
from datetime import datetime

def main():
    print("🔍 SHOWING DETAILED AGI RESPONSE ANALYSIS")
    print("=" * 80)
    
    # Load the latest AGI response
    try:
        with open('agi_live_chat_responses.json', 'r') as f:
            responses = json.load(f)
        
        if responses:
            latest_response = responses[-1]  # Get the most recent response
            print(f"📅 Latest Response: {latest_response.get('timestamp', 'Unknown')}")
            print(f"❓ Question: {latest_response.get('question', 'Unknown')}")
            print()
            
            # Show the full intelligence analysis
            intelligence_data = latest_response.get('intelligence_analysis', {})
            if intelligence_data:
                print("🧠 INTELLIGENCE ANALYSIS:")
                print(f"   Intelligence Level: {intelligence_data.get('current_level', 'Unknown')}")
                print(f"   WHY Questions Generated: {intelligence_data.get('why_questions_generated', 0)}")
                print(f"   Insights Gained: {intelligence_data.get('insights_gained', 0)}")
                print(f"   Strategies Generated: {len(intelligence_data.get('evolved_strategies', []))}")
                print()
                
                # Show all strategies and their ethical status
                strategies = intelligence_data.get('evolved_strategies', [])
                if strategies:
                    print("🎯 ALL GENERATED STRATEGIES:")
                    print("-" * 50)
                    for i, strategy in enumerate(strategies, 1):
                        print(f"{i}. {strategy.get('name', 'Unknown')}")
                        print(f"   Type: {strategy.get('type', 'Unknown')}")
                        print(f"   Efficiency Gain: {strategy.get('efficiency_gain', 'Unknown')}")
                        print(f"   Business Optimized: {strategy.get('business_optimized', False)}")
                        print(f"   Risk Adjusted: {strategy.get('risk_adjusted', False)}")
                        print()
                
                # Show ethical evaluations
                ethical_reasoning = intelligence_data.get('ethical_reasoning', {})
                if ethical_reasoning:
                    strategy_evaluations = ethical_reasoning.get('strategy_evaluations', [])
                    print("⚖️ ETHICAL EVALUATIONS:")
                    print("-" * 50)
                    for i, eval in enumerate(strategy_evaluations, 1):
                        strategy_name = eval.get('strategy', {}).get('name', 'Unknown')
                        ethical_score = eval.get('ethical_assessment', {}).get('ethical_score', 0.0)
                        approved = eval.get('approved', False)
                        status = "✅ APPROVED" if approved else "❌ REJECTED"
                        print(f"{i}. {strategy_name}: {ethical_score:.2f} - {status}")
                    print()
                    
                    print(f"📊 SUMMARY:")
                    print(f"   Approved Strategies: {ethical_reasoning.get('approved_strategies_count', 0)}")
                    print(f"   Rejected Strategies: {ethical_reasoning.get('rejected_strategies_count', 0)}")
                    print()
                
                # Show actionable choices
                actionable_choices = latest_response.get('actionable_choices', [])
                if actionable_choices:
                    print("🎯 ACTIONABLE CHOICES:")
                    print("-" * 50)
                    for i, choice in enumerate(actionable_choices, 1):
                        print(f"{i}. {choice.get('description', 'Unknown')}")
                        print(f"   Type: {choice.get('type', 'Unknown')}")
                        print(f"   Priority: {choice.get('priority', 'Unknown')}")
                        if 'implementation_details' in choice:
                            print(f"   Implementation: {choice.get('implementation_details', 'None')}")
                        print()
                else:
                    print("🎯 ACTIONABLE CHOICES: NONE (All rejected by ethics)")
                    print()
                
            else:
                print("❌ No intelligence analysis found in response")
        else:
            print("❌ No responses found")
            
    except FileNotFoundError:
        print("❌ No AGI response file found")
        print("💡 Try running the AGI Live Chat first to generate responses")
    except Exception as e:
        print(f"❌ Error reading responses: {e}")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
