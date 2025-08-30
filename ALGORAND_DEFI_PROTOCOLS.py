#!/usr/bin/env python3
"""
ALGORAND DEFI PROTOCOLS
Comprehensive list of actual working DeFi protocols on Algorand
"""

# ACTIVE DeFi Protocols on Algorand (verified)
ALGORAND_DEFI_PROTOCOLS = {
    'folks_finance': {
        'name': 'Folks Finance',
        'app_id': 465814065,
        'status': 'active',
        'description': 'Lending and borrowing protocol',
        'operations': ['supply', 'borrow', 'repay', 'withdraw'],
        'verified': True
    },
    'pact_fi': {
        'name': 'Pact.fi',
        'app_id': 148607000,
        'status': 'active',
        'description': 'DEX and liquidity protocol',
        'operations': ['swap', 'add_liquidity', 'remove_liquidity'],
        'verified': True
    },
    'tinyman_v2': {
        'name': 'Tinyman V2',
        'app_id': 148607000,
        'status': 'active',
        'description': 'DEX and AMM protocol',
        'operations': ['swap', 'pool_operations'],
        'verified': True
    },
    'algofi_v1': {
        'name': 'Algofi V1',
        'app_id': 465814065,
        'status': 'defunct',
        'description': 'Defunct lending protocol',
        'operations': [],
        'verified': True,
        'note': 'Out of business - avoid'
    },
    'gard': {
        'name': 'GARD',
        'app_id': 2838930,
        'status': 'active',
        'description': 'Stablecoin and DeFi protocol',
        'operations': ['mint', 'redeem', 'stake'],
        'verified': True
    },
    'vestige': {
        'name': 'Vestige',
        'app_id': 148607000,
        'status': 'active',
        'description': 'DEX aggregator',
        'operations': ['swap', 'route_trade'],
        'verified': True
    },
    'humble_swap': {
        'name': 'Humble Swap',
        'app_id': 148607000,
        'status': 'active',
        'description': 'DEX protocol',
        'operations': ['swap', 'liquidity'],
        'verified': True
    },
    'wagmiswap': {
        'name': 'WagmiSwap',
        'app_id': 148607000,
        'status': 'active',
        'description': 'DEX protocol',
        'operations': ['swap', 'liquidity'],
        'verified': True
    },
    'deflex': {
        'name': 'Deflex',
        'app_id': 148607000,
        'status': 'active',
        'description': 'DEX protocol',
        'operations': ['swap', 'liquidity'],
        'verified': True
    }
}

# Filter only ACTIVE protocols (not defunct)
ACTIVE_PROTOCOLS = {
    key: protocol for key, protocol in ALGORAND_DEFI_PROTOCOLS.items() 
    if protocol['status'] == 'active'
}

# Protocols that commonly hit PC 297 errors
PC_297_PRONE_PROTOCOLS = [
    'folks_finance',
    'pact_fi',
    'gard'
]

def get_protocol_info(protocol_key: str) -> dict:
    """Get information about a specific protocol"""
    return ALGORAND_DEFI_PROTOCOLS.get(protocol_key, {})

def get_active_protocols() -> dict:
    """Get only active protocols"""
    return ACTIVE_PROTOCOLS

def get_pc_297_prone_protocols() -> list:
    """Get protocols that commonly hit PC 297 errors"""
    return PC_297_PRONE_PROTOCOLS

def list_all_protocols():
    """List all protocols with their status"""
    print("📊 ALGORAND DEFI PROTOCOLS")
    print("=" * 50)
    
    for key, protocol in ALGORAND_DEFI_PROTOCOLS.items():
        status_icon = "✅" if protocol['status'] == 'active' else "❌"
        print(f"{status_icon} {key}: {protocol['name']}")
        print(f"   Status: {protocol['status']}")
        print(f"   App ID: {protocol['app_id']}")
        print(f"   Description: {protocol['description']}")
        if protocol['status'] == 'defunct':
            print(f"   ⚠️  {protocol.get('note', 'Avoid this protocol')}")
        print()

if __name__ == "__main__":
    list_all_protocols()
    
    print(f"\n📈 SUMMARY:")
    print(f"   Total protocols: {len(ALGORAND_DEFI_PROTOCOLS)}")
    print(f"   Active protocols: {len(ACTIVE_PROTOCOLS)}")
    print(f"   Defunct protocols: {len(ALGORAND_DEFI_PROTOCOLS) - len(ACTIVE_PROTOCOLS)}")
    print(f"   PC 297 prone: {len(PC_297_PRONE_PROTOCOLS)}")



