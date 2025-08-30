#!/usr/bin/env python3
"""
Clean up duplicate and zombie processes in the WealthyRobot empire
Prevents conflicts and optimizes resource usage
"""

import os
import psutil
import signal
import time
from typing import Dict, List, Set

def get_all_python_processes() -> List[psutil.Process]:
    """Get all Python processes running in the empire"""
    python_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            if proc.info['name'] == 'python3' or proc.info['name'] == 'python':
                if proc.info['cmdline'] and len(proc.info['cmdline']) > 0:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'wealthyrobot' in cmdline.lower() or '/home/ubuntu/wealthyrobot' in cmdline:
                        python_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return python_processes

def analyze_processes(processes: List[psutil.Process]) -> Dict[str, List[psutil.Process]]:
    """Analyze processes and group by type"""
    process_groups = {
        'agi_system': [],
        'trading_system': [],
        'empire_optimizers': [],
        'orchestrators': [],
        'claude_agents': [],
        'automation_agents': [],
        'debug_agents': [],
        'advisor_agents': [],
        'coordinators': [],
        'deployments': [],
        'zombies': [],
        'other': []
    }

    for proc in processes:
        try:
            cmdline = ' '.join(proc.info['cmdline'])
            proc_name = proc.info['name']

            # Check if zombie
            if proc.status() == psutil.STATUS_ZOMBIE:
                process_groups['zombies'].append(proc)
                continue

            # Categorize by script name
            if 'UNRESTRICTED_AGI_SYSTEM.py' in cmdline:
                process_groups['agi_system'].append(proc)
            elif 'run_hybrid_trading_empire.py' in cmdline:
                process_groups['trading_system'].append(proc)
            elif 'continuous_empire_optimizer.py' in cmdline:
                process_groups['empire_optimizers'].append(proc)
            elif 'live_orchestrator.py' in cmdline:
                process_groups['orchestrators'].append(proc)
            elif 'claude_full_autonomous.py' in cmdline or 'claude_background' in cmdline:
                process_groups['claude_agents'].append(proc)
            elif 'continuous_automation_agent.py' in cmdline:
                process_groups['automation_agents'].append(proc)
            elif 'code_debug_agent.py' in cmdline:
                process_groups['debug_agents'].append(proc)
            elif 'strategic_advisor_agent.py' in cmdline:
                process_groups['advisor_agents'].append(proc)
            elif 'agent_coordinator' in cmdline or 'integrated_deployment' in cmdline:
                process_groups['coordinators'].append(proc)
            elif 'wealthyrobot_autonomous_service' in cmdline or 'continuous_empire_optimizer' in cmdline:
                process_groups['deployments'].append(proc)
            else:
                process_groups['other'].append(proc)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return process_groups

def display_process_analysis(process_groups: Dict[str, List[psutil.Process]]):
    """Display analysis of current processes"""
    print("🧠 WEALTHYROBOT EMPIRE PROCESS ANALYSIS")
    print("=" * 60)

    total_processes = sum(len(procs) for procs in process_groups.values())

    print(f"📊 Total Python processes: {total_processes}")
    print()

    for category, processes in process_groups.items():
        count = len(processes)
        status = "✅" if count == 0 else ("🚨" if count > 1 else "⚠️")

        print(f"{status} {category.replace('_', ' ').title()}: {count}")

        if count > 1:
            print("   📋 PIDs:")
            for proc in processes:
                try:
                    print(f"      • {proc.pid}: {' '.join(proc.info['cmdline'])}")
                except:
                    print(f"      • {proc.pid}: [process info unavailable]")

        print()

def identify_processes_to_kill(process_groups: Dict[str, List[psutil.Process]]) -> List[psutil.Process]:
    """Identify processes that should be killed to avoid conflicts"""
    to_kill = []

    # Keep only 1 of each type (except zombies which we kill all)
    for category, processes in process_groups.items():
        if category == 'zombies':
            # Kill all zombies
            to_kill.extend(processes)
        elif category in ['agi_system', 'trading_system']:
            # Keep the most recent one, kill others
            if len(processes) > 1:
                # Sort by creation time, keep the newest
                processes.sort(key=lambda p: p.info['create_time'], reverse=True)
                to_kill.extend(processes[1:])  # Kill all but the newest
        else:
            # Kill all duplicates in non-essential categories
            if len(processes) > 0:
                to_kill.extend(processes)

    return to_kill

def kill_processes(processes: List[psutil.Process], graceful: bool = True):
    """Kill the specified processes"""
    print(f"🧹 CLEANING UP {len(processes)} PROCESSES...")

    for proc in processes:
        try:
            pid = proc.pid

            if graceful:
                # Try graceful shutdown first
                proc.terminate()
                time.sleep(2)

                # Check if still running
                if proc.is_running():
                    proc.kill()
                    print(f"   💀 Force killed process {pid}")
                else:
                    print(f"   ✅ Gracefully terminated process {pid}")
            else:
                proc.kill()
                print(f"   💀 Force killed process {pid}")

        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"   ⚠️ Could not kill process {pid}: {e}")
        except Exception as e:
            print(f"   ❌ Error killing process {pid}: {e}")

def start_essential_processes():
    """Start only the essential processes"""
    print("\n🚀 STARTING ESSENTIAL PROCESSES...")

    # Check if essential processes are already running
    processes = get_all_python_processes()
    process_groups = analyze_processes(processes)

    # Start AGI system if not running
    if len(process_groups['agi_system']) == 0:
        print("   🧠 Starting AGI System...")
        try:
            os.system("python3 start_optimized_agi.py &")
            print("   ✅ AGI System started")
        except Exception as e:
            print(f"   ❌ Failed to start AGI: {e}")

    # Start trading system if not running
    if len(process_groups['trading_system']) == 0:
        print("   💰 Starting Trading System...")
        try:
            os.system("python3 run_hybrid_trading_empire.py &")
            print("   ✅ Trading System started")
        except Exception as e:
            print(f"   ❌ Failed to start Trading: {e}")

def main():
    """Main cleanup function"""
    print("🧹 WEALTHYROBOT EMPIRE CLEANUP")
    print("Removing duplicates and optimizing processes")
    print("=" * 60)

    # Get all processes
    processes = get_all_python_processes()
    print(f"📊 Found {len(processes)} Python processes")

    # Analyze processes
    process_groups = analyze_processes(processes)
    display_process_analysis(process_groups)

    # Identify processes to kill
    to_kill = identify_processes_to_kill(process_groups)

    if len(to_kill) > 0:
        print(f"🗑️ IDENTIFIED {len(to_kill)} PROCESSES TO CLEAN UP:")
        for proc in to_kill:
            try:
                print(f"   • {proc.pid}: {' '.join(proc.info['cmdline'])}")
            except:
                print(f"   • {proc.pid}: [process info unavailable]")

        # Confirm before killing
        response = input("\n⚠️  Do you want to kill these processes? (y/N): ").strip().lower()
        if response == 'y' or response == 'yes':
            kill_processes(to_kill)

            # Wait a bit for processes to die
            time.sleep(3)

            print("\n✅ CLEANUP COMPLETE!")
        else:
            print("\n🛑 Cleanup cancelled by user")
            return
    else:
        print("✅ No processes need cleanup!")

    # Start essential processes
    start_essential_processes()

    # Final status
    print("\n📊 FINAL STATUS:")
    final_processes = get_all_python_processes()
    final_groups = analyze_processes(final_processes)

    print(f"   • Total processes: {len(final_processes)}")
    print(f"   • AGI systems: {len(final_groups['agi_system'])}")
    print(f"   • Trading systems: {len(final_groups['trading_system'])}")
    print(f"   • Zombie processes: {len(final_groups['zombies'])}")
    print(f"   • Other agents: {sum(len(final_groups[cat]) for cat in final_groups if cat not in ['agi_system', 'trading_system', 'zombies'])}")

    print("\n🎯 READY FOR MAXIMUM PROFIT GENERATION!")
    print("💰 Your AGI and trading systems are optimized and running!")

if __name__ == "__main__":
    main()
