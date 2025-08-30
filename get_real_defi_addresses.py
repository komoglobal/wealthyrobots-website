#!/usr/bin/env python3
"""
Get Real DeFi Protocol Addresses on Algorand Mainnet
"""

import requests
import json

def get_tinyman_v2_addresses():
    """Get Tinyman V2 addresses from their API"""
    try:
        # Tinyman V2 API endpoint
        url = "https://mainnet.analytics.tinyman.org/api/v1/pools"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Tinyman V2 API response received")
            print(f"   Found {len(data)} pools")
            
            # Extract router address from first pool
            if data and len(data) > 0:
                first_pool = data[0]
                if 'router_address' in first_pool:
                    print(f"   Router address: {first_pool['router_address']}")
                    return first_pool['router_address']
                else:
                    print("   No router address found in pool data")
            else:
                print("   No pools found")
        else:
            print(f"❌ Tinyman API failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting Tinyman addresses: {e}")
    
    return None

def get_pact_finance_addresses():
    """Get Pact Finance addresses"""
    try:
        # Pact Finance API endpoint
        url = "https://api.pact.fi/api/pools"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Pact Finance API response received")
            print(f"   Found {len(data)} pools")
            
            # Look for router or contract addresses
            if data and len(data) > 0:
                first_pool = data[0]
                print(f"   First pool data keys: {list(first_pool.keys())}")
                
        else:
            print(f"❌ Pact Finance API failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting Pact Finance addresses: {e}")
    
    return None

def get_folks_finance_addresses():
    """Get Folks Finance addresses"""
    try:
        # Folks Finance API endpoint
        url = "https://api.folks.finance/api/v1/pools"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Folks Finance API response received")
            print(f"   Found {len(data)} pools")
            
        else:
            print(f"❌ Folks Finance API failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting Folks Finance addresses: {e}")
    
    return None

def get_known_defi_addresses():
    """Get known DeFi protocol addresses from documentation"""
    known_addresses = {
        "tinyman_v2_router": "TINYMAN_V2_ROUTER_MAINNET",  # Need to find real address
        "pact_finance_router": "PACT_FINANCE_ROUTER_MAINNET",  # Need to find real address
        "folks_finance_router": "FOLKS_FINANCE_ROUTER_MAINNET",  # Need to find real address
        "algofi_lending": "465814065",  # App ID for lending
        "tinyman_v1_router": "1002541853",  # App ID for V1
    }
    
    print("📋 Known DeFi Protocol Addresses:")
    for protocol, address in known_addresses.items():
        print(f"   {protocol}: {address}")
    
    return known_addresses

def main():
    """Main function to get all DeFi addresses"""
    print("🔍 GETTING REAL DEFI PROTOCOL ADDRESSES")
    print("=" * 50)
    
    print("\n🔍 Querying Tinyman V2...")
    tinyman_router = get_tinyman_v2_addresses()
    
    print("\n🔍 Querying Pact Finance...")
    pact_router = get_pact_finance_addresses()
    
    print("\n🔍 Querying Folks Finance...")
    folks_router = get_folks_finance_addresses()
    
    print("\n📋 Known addresses:")
    known = get_known_defi_addresses()
    
    print("\n🎯 SUMMARY:")
    if tinyman_router:
        print(f"   ✅ Tinyman V2 Router: {tinyman_router}")
    else:
        print("   ❌ Tinyman V2 Router: Not found")
    
    if pact_router:
        print(f"   ✅ Pact Finance Router: {pact_router}")
    else:
        print("   ❌ Pact Finance Router: Not found")
    
    if folks_router:
        print(f"   ✅ Folks Finance Router: {folks_router}")
    else:
        print("   ❌ Folks Finance Router: Not found")

if __name__ == "__main__":
    main()
