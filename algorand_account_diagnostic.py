#!/usr/bin/env python3
"""
ALGORAND ACCOUNT DIAGNOSTIC TOOL
Quick check of account balance and DEX integration status
"""
import subprocess
import json
import os
from datetime import datetime

def run_command(cmd):
    """Run a command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), -1

def check_account_balance():
    """Check the current account balance"""
    print("🔍 CHECKING ACCOUNT BALANCE")
    print("-" * 40)
    
    # Check algofund logs for current balance
    cmd = "tail -100 logs/algofund-live.out | grep -E 'balance|BALANCE|NAV' | tail -5"
    stdout, stderr, code = run_command(cmd)
    
    if stdout:
        print("📊 Recent Balance Information:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("❌ No balance information found in recent logs")
    
    print()

def check_dex_errors():
    """Check for recent DEX errors"""
    print("🚨 CHECKING DEX INTEGRATION ERRORS")
    print("-" * 40)
    
    # Check Tinyman errors
    cmd = "tail -1000 logs/algofund-live.out | grep 'LIVE_ERROR_TINYMAN' | tail -5"
    stdout, stderr, code = run_command(cmd)
    
    if stdout:
        print("🔴 Tinyman DEX Errors:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("✅ No recent Tinyman errors")
    
    print()
    
    # Check Pact errors
    cmd = "tail -1000 logs/algofund-live.out | grep 'LIVE_ERROR_PACT' | tail -5"
    stdout, stderr, code = run_command(cmd)
    
    if stdout:
        print("🔴 Pact DEX Errors:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("✅ No recent Pact errors")
    
    print()

def check_trading_status():
    """Check current trading status"""
    print("📈 CHECKING TRADING STATUS")
    print("-" * 40)
    
    # Check for recent successful trades
    cmd = "tail -500 logs/algofund-live.out | grep -E 'LIVE_EXECUTE_TXNS|SWAP.*SUCCESS|TRADE.*COMPLETED' | tail -5"
    stdout, stderr, code = run_command(cmd)
    
    if stdout:
        print("✅ Recent Successful Trades:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("❌ No recent successful trades found")
    
    print()
    
    # Check for opportunity scanning
    cmd = "tail -1000 logs/algofund-live.out | grep -E 'OPPORTUNITIES|SCANNING|MARKET_MAKING|ARBITRAGE' | tail -5"
    stdout, stderr, code = run_command(cmd)
    
    if stdout:
        print("🔍 Recent Opportunity Activity:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
    else:
        print("❌ No recent opportunity activity found")
    
    print()

def check_system_health():
    """Check overall system health"""
    print("🏥 SYSTEM HEALTH CHECK")
    print("-" * 40)
    
    # Check if algofund services are running
    cmd = "systemctl is-active algofund-live.service"
    stdout, stderr, code = run_command(cmd)
    
    if stdout == "active":
        print("✅ Live Trading Service: ACTIVE")
    else:
        print(f"❌ Live Trading Service: {stdout}")
    
    cmd = "systemctl is-active algofund-paper.service"
    stdout, stderr, code = run_command(cmd)
    
    if stdout == "active":
        print("✅ Paper Trading Service: ACTIVE")
    else:
        print(f"❌ Paper Trading Service: {stdout}")
    
    # Check recent log activity
    cmd = "tail -1 logs/algofund-live.out | grep -o '\\d\\{4\\}-\\d\\{2\\}-\\d\\{2\\} \\d\\{2\\}:\\d\\{2\\}:\\d\\{2\\}'"
    stdout, stderr, code = run_command(cmd)
    
    if stdout:
        print(f"📅 Last Live Log Entry: {stdout}")
    else:
        print("❌ No recent live log activity")
    
    print()

def generate_recommendations():
    """Generate immediate recommendations"""
    print("💡 IMMEDIATE RECOMMENDATIONS")
    print("-" * 40)
    
    print("🚨 CRITICAL ACTIONS REQUIRED:")
    print("1. FUND ACCOUNT: Add ALGO to reach minimum 300,000 microALGO balance")
    print("2. STOP TRADING: Prevent further gas fee losses")
    print("3. FIX DEX INTEGRATIONS: Resolve Tinyman and Pact errors")
    
    print("\n🔧 TECHNICAL PRIORITIES:")
    print("1. Update tinyman package to compatible version")
    print("2. Fix Pact API authentication issues")
    print("3. Implement proper error handling and recovery")
    
    print("\n📊 MONITORING:")
    print("1. Set up balance threshold alerts")
    print("2. Monitor DEX integration health")
    print("3. Track successful vs failed transaction ratios")
    
    print()

def main():
    """Main diagnostic function"""
    print("🔍 ALGORAND ACCOUNT DIAGNOSTIC REPORT")
    print("=" * 60)
    print(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    check_account_balance()
    check_dex_errors()
    check_trading_status()
    check_system_health()
    generate_recommendations()
    
    print("=" * 60)
    print("🎯 Diagnostic Complete - Review recommendations above")
    print("=" * 60)

if __name__ == "__main__":
    main()
