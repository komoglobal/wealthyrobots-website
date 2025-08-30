#!/usr/bin/env python3
import json
import os

def show_deployment_stats():
    if not os.path.exists('deployment_history.json'):
        print("📊 No deployment history found yet")
        return
    
    with open('deployment_history.json', 'r') as f:
        history = json.load(f)
    
    print("📊 DEPLOYMENT STATISTICS:")
    print(f"Total deployments: {len(history)}")
    
    successful = sum(1 for d in history if d.get('status') == 'deployed')
    print(f"Successful: {successful}")
    print(f"Success rate: {(successful/len(history)*100):.1f}%")
    
    print("\n📅 Recent deployments:")
    for d in history[-3:]:
        agent = d.get('agent_name', 'Unknown')
        status = d.get('status', 'Unknown')
        timestamp = d.get('timestamp', '')[:19]
        print(f"  {timestamp} | {agent} | {status}")

if __name__ == "__main__":
    show_deployment_stats()
