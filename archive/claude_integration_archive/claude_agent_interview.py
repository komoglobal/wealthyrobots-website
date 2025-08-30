#!/usr/bin/env python3
import json
import subprocess
import os
import glob
from datetime import datetime

def interview_claude_agent():
   print("🎤 INTERVIEWING CLAUDE AGENT")
   print("=" * 40)
   
   questions = [
       "What is blocking your revenue optimization?",
       "What tools or APIs do you need access to?", 
       "What manual data would help you optimize better?",
       "What new agents should be created next?",
       "What external services should be integrated?",
       "What is your current biggest limitation?",
       "What would 10x your effectiveness?"
   ]
   
   # Create interview request
   interview_request = {
       "timestamp": datetime.now().isoformat(),
       "type": "agent_interview",
       "questions": questions,
       "priority": "immediate",
       "response_format": "json",
       "interviewer": "human_operator"
   }
   
   with open('claude_agent_interview.json', 'w') as f:
       json.dump(interview_request, f, indent=2)
   
   print("📝 Interview questions sent to CLAUDE agent:")
   for i, q in enumerate(questions, 1):
       print(f"  {i}. {q}")
   
   print(f"\n🔍 Checking current agent status...")
   
   # Check latest autonomous log
   log_files = sorted(glob.glob("claude_autonomous_log_*.json"), key=os.path.getmtime, reverse=True)
   if log_files:
       try:
           with open(log_files[0], "r") as f:
               data = json.load(f)
           
           print("🤖 CLAUDE Agent Current Status:")
           print(f"   Cycle: {data.get('cycle', 'unknown')}")
           print(f"   Status: {data.get('status', 'unknown')}")
           
           if 'implementations' in data and data['implementations']:
               latest = data['implementations'][-1]
               if 'solution' in latest:
                   problem = latest['solution'].get('problem', 'unknown')
                   print(f"   Current Problem: {problem}")
           
           if 'optimizations' in data:
               print(f"   Recent Optimizations: {len(data['optimizations'])}")
               for opt in data['optimizations'][-3:]:
                   print(f"     • {opt.get('type', 'unknown')}: {opt.get('status', 'unknown')}")
       except Exception as e:
           print(f"Error reading log: {e}")
   
   # Check recent activity
   print(f"\n📊 Recent CLAUDE Agent Activity:")
   solution_files = sorted(glob.glob("claude_solution_*.py"), key=os.path.getmtime, reverse=True)
   if solution_files:
       print("Last 3 problems worked on:")
       for i, file in enumerate(solution_files[:3], 1):
           try:
               with open(file, 'r') as f:
                   content = f.read()
               for line in content.split('\n'):
                   if 'Problem:' in line:
                       problem = line.split('Problem:')[-1].strip()
                       timestamp = file.split('_')[2] + '_' + file.split('_')[3].replace('.py', '')
                       print(f"  {i}. {timestamp}: {problem}")
                       break
           except:
               continue
   
   print(f"\n💡 Monitoring for CLAUDE agent response...")
   print("Files created:")
   print("- claude_agent_interview.json (questions)")
   print("- Watch for: claude_agent_response.json")
   
if __name__ == "__main__":
   interview_claude_agent()
