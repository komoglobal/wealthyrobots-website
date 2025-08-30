import asyncio
import requests
import json
import re
from algosdk.v2client import algod

async def known_defi_search():
    print('🔍 KNOWN DeFi PROTOCOL SEARCH')
    print('=' * 40)

    # Initialize client
    algod_client = algod.AlgodClient('', 'https://mainnet-api.algonode.cloud')

    # Known DeFi protocols on Algorand
    known_protocols = {
        'Folks Finance': {
            'docs': 'https://docs.folks.finance',
            'pools': [
                'https://app.folks.finance/lending',
                'https://app.folks.finance/liquidation-protection'
            ],
            'expected_range': (971350000, 971360000)
        },
        'Pact Finance': {
            'docs': 'https://docs.pact.fi',
            'pools': [
                'https://app.pact.fi',
                'https://app.pact.fi/pools'
            ],
            'expected_range': (1072800000, 1072900000)
        },
        'Tinyman': {
            'docs': 'https://docs.tinyman.org',
            'pools': [
                'https://app.tinyman.org',
                'https://app.tinyman.org/pools'
            ],
            'expected_range': (600000, 700000)
        },
        'Humble': {
            'docs': 'https://docs.humble.sh',
            'pools': [
                'https://humble.sh',
                'https://app.humble.sh/pools'
            ],
            'expected_range': (500000, 600000)
        },
        'Yieldly': {
            'docs': 'https://docs.yieldly.finance',
            'pools': [
                'https://app.yieldly.finance',
                'https://app.yieldly.finance/stake'
            ],
            'expected_range': (300000, 400000)
        }
    }

    found_contracts = []

    print('📖 CHECKING OFFICIAL DOCUMENTATION...')

    for protocol_name, protocol_info in known_protocols.items():
        print(f'\n🔍 Analyzing {protocol_name}...')

        # Check documentation for contract addresses
        try:
            response = requests.get(protocol_info['docs'], timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()

                # Look for app IDs
                app_matches = re.findall(r'\b(\d{9,10})\b', text)
                for match in app_matches:
                    match_int = int(match)
                    if (protocol_info['expected_range'][0] <= match_int <= protocol_info['expected_range'][1] or
                        600000 <= match_int <= 700000):  # General DeFi range

                        found_contracts.append({
                            'protocol': protocol_name,
                            'type': 'documentation',
                            'value': match,
                            'source': protocol_info['docs']
                        })
                        print(f'   🎯 Found potential app ID: {match}')

        except Exception as e:
            print(f'   ❌ Error checking docs: {e}')

        # Check live app for contract info
        for pool_url in protocol_info['pools']:
            try:
                print(f'   🌐 Checking {pool_url}...')
                response = requests.get(pool_url, timeout=10)

                if response.status_code == 200:
                    text = response.text.lower()

                    # Look for app IDs in JavaScript or API calls
                    app_matches = re.findall(r'app[_-]?id["\s:]*(\d{9,10})', text)
                    for match in app_matches:
                        match_int = int(match)
                        if (protocol_info['expected_range'][0] <= match_int <= protocol_info['expected_range'][1] or
                            600000 <= match_int <= 700000):

                            found_contracts.append({
                                'protocol': protocol_name,
                                'type': 'web_app',
                                'value': match,
                                'source': pool_url
                            })
                            print(f'      🎯 Found app ID: {match}')

                    # Look for API endpoints that might contain contract info
                    api_matches = re.findall(r'api\.[a-zA-Z0-9.-]+\.[a-z]+/v\d+/([a-zA-Z0-9/_-]+)', text)
                    for match in api_matches:
                        if 'pool' in match or 'app' in match or 'contract' in match:
                            print(f'      📡 Found API endpoint: {match}')

            except Exception as e:
                print(f'   ❌ Error checking {pool_url}: {e}')

    # Search blockchain for active DeFi applications
    print('\n🔍 BLOCKCHAIN ANALYSIS...')

    # Search ranges known to contain DeFi apps
    search_ranges = [
        (971350072, 971350280, 'Folks Finance Range'),
        (1072800000, 1072800100, 'Pact Finance Range'),
        (653000000, 654000000, 'General DeFi Range'),
        (580000, 620000, 'Older DeFi Range')
    ]

    for start, end, range_name in search_ranges:
        print(f'   🔍 Scanning {range_name}: {start}-{end}')

        for app_id in range(start, end + 1, 10):  # Sample every 10th app
            try:
                app_info = algod_client.application_info(app_id)
                if app_info:
                    params = app_info.get('params', {})
                    global_state = params.get('global-state', [])

                    if len(global_state) >= 5:  # Likely DeFi app
                        # Determine protocol based on creator or range
                        protocol = 'Unknown'
                        if 971350000 <= app_id <= 971360000:
                            protocol = 'Folks Finance'
                        elif 1072800000 <= app_id <= 1072900000:
                            protocol = 'Pact Finance'
                        elif 653000000 <= app_id <= 654000000:
                            protocol = 'General DeFi'
                        elif 580000 <= app_id <= 620000:
                            protocol = 'Older DeFi'

                        found_contracts.append({
                            'protocol': protocol,
                            'type': 'blockchain_scan',
                            'value': str(app_id),
                            'source': f'{range_name} scan'
                        })

                        print(f'      🎯 Found complex app: {app_id} ({len(global_state)} vars) - {protocol}')

                        # Limit results
                        if len([c for c in found_contracts if c['type'] == 'blockchain_scan']) >= 5:
                            break

            except Exception as e:
                if 'not found' not in str(e).lower():
                    print(f'      ❌ Error checking {app_id}: {e}')

        if len([c for c in found_contracts if c['type'] == 'blockchain_scan']) >= 5:
            break

    # Check for known working apps from successful transactions
    print('\n📊 CHECKING FOR WORKING DeFi APPS...')

    # Test some known potential DeFi apps
    potential_apps = [
        971350072,  # Known Folks app
        653000000,  # Known DeFi app
        1072800000, # Known Pact app
        971353536,  # Management contract
        600000,     # General DeFi
    ]

    for app_id in potential_apps:
        try:
            app_info = algod_client.application_info(app_id)
            if app_info:
                params = app_info.get('params', {})
                global_state = params.get('global-state', [])

                print(f'   🧪 Testing known app {app_id}...')

                if len(global_state) > 0:
                    print(f'      ✅ Valid app with {len(global_state)} vars')

                    # Try to determine if it's a working DeFi app
                    creator = params.get('creator', '')
                    print(f'      👤 Creator: {creator[:20]}...')

                    found_contracts.append({
                        'protocol': 'Known Working',
                        'type': 'known_app',
                        'value': str(app_id),
                        'source': 'Known app test'
                    })

        except Exception as e:
            print(f'   ❌ App {app_id} not accessible: {e}')

    # Remove duplicates and sort by protocol
    unique_contracts = []
    seen = set()
    for contract in found_contracts:
        key = f"{contract['protocol']}_{contract['value']}"
        if key not in seen:
            unique_contracts.append(contract)
            seen.add(key)

    # Sort by protocol and type
    unique_contracts.sort(key=lambda x: (x['protocol'], x['type']))

    print(f'\n🎯 SUMMARY:')
    print(f'   📊 Total unique contracts found: {len(unique_contracts)}')

    if unique_contracts:
        print('\n🏆 FOUND CONTRACTS BY PROTOCOL:')
        current_protocol = None
        for contract in unique_contracts:
            if contract['protocol'] != current_protocol:
                current_protocol = contract['protocol']
                print(f'\n   📚 {current_protocol}:')

            print(f'      {contract["value"]} ({contract["type"]}) - {contract["source"]}')

    print('\n💡 NEXT STEPS:')
    print('   1. 🧪 Test the found contracts for opt-in functionality')
    print('   2. 📊 Focus on contracts from official documentation first')
    print('   3. 🔍 Cross-reference with working DeFi applications')

    return unique_contracts

if __name__ == '__main__':
    asyncio.run(known_defi_search())









