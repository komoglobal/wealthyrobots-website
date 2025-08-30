import asyncio
import requests
import json
import re
from algosdk.v2client import algod, indexer
from bs4 import BeautifulSoup

async def direct_contract_search():
    print('🔍 DIRECT CONTRACT SEARCH')
    print('=' * 40)

    # Initialize clients
    algod_client = algod.AlgodClient('', 'https://mainnet-api.algonode.cloud')
    indexer_client = indexer.IndexerClient('', 'https://mainnet-idx.algonode.cloud')

    found_contracts = []

    # Strategy 1: Check specific documentation pages
    print('\n📖 CHECKING SPECIFIC DOCS PAGES...')

    specific_pages = [
        'https://docs.folks.finance/developers/smart-contracts',
        'https://docs.folks.finance/developers/integration-guide',
        'https://docs.pact.fi/developers',
        'https://docs.pact.fi/contracts',
        'https://docs.folks.finance/lending-pools',
        'https://docs.pact.fi/yield-farming'
    ]

    for url in specific_pages:
        try:
            print(f'   🔍 Checking: {url}')
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()

                # Look for app IDs in different formats
                patterns = [
                    r'(\d{9,10})',  # 9-10 digit app IDs
                    r'app[_-]?id[:\s=]*(\d+)',
                    r'application[_-]?id[:\s=]*(\d+)',
                    r'pool[_-]?id[:\s=]*(\d+)'
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text)
                    for match in matches:
                        match_str = str(match)
                        if len(match_str) >= 9:
                            # Check if it's in DeFi ranges
                            match_int = int(match_str)
                            if (971350000 <= match_int <= 971360000 or
                                1072800000 <= match_int <= 1072900000 or
                                600000 <= match_int <= 700000):

                                found_contracts.append({
                                    'protocol': 'Folks Finance' if 'folks' in url.lower() else 'Pact Finance',
                                    'type': 'documentation',
                                    'value': match_str,
                                    'source': url
                                })
                                print(f'      🎯 Found DeFi app ID: {match_str}')

        except Exception as e:
            print(f'   ❌ Error: {e}')

    # Strategy 2: Check GitHub README files directly
    print('\n📚 CHECKING GITHUB README FILES...')

    readme_urls = [
        'https://raw.githubusercontent.com/folks-finance/folks-finance-js-sdk/main/README.md',
        'https://raw.githubusercontent.com/pactfi/pactfi-js-sdk/main/README.md',
        'https://raw.githubusercontent.com/folks-finance/folks-finance-js-sdk/main/package.json',
        'https://raw.githubusercontent.com/pactfi/pactfi-js-sdk/main/package.json'
    ]

    for url in readme_urls:
        try:
            print(f'   📖 Checking: {url.split("/")[-1]}')
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                content = response.text

                # Look for app IDs
                app_matches = re.findall(r'\b(\d{9,10})\b', content)
                for match in app_matches:
                    match_int = int(match)
                    if (971350000 <= match_int <= 971360000 or
                        1072800000 <= match_int <= 1072900000):

                        protocol = 'Folks Finance' if 'folks' in url.lower() else 'Pact Finance'
                        found_contracts.append({
                            'protocol': protocol,
                            'type': 'github',
                            'value': match,
                            'source': url
                        })
                        print(f'      🎯 Found: {match}')

        except Exception as e:
            print(f'   ❌ Error: {e}')

    # Strategy 3: Check known DeFi app ranges more systematically
    print('\n🔍 SYSTEMATIC APP ID SCAN...')

    # Focus on smaller, more targeted ranges
    targeted_ranges = [
        (971350072, 971350280, 'Folks Finance Known Range'),
        (1072800000, 1072801000, 'Pact Finance Known Range'),
        (971353536, 971353536, 'Folks Management Contract'),
        (971350278, 971350278, 'Previously Tested App')
    ]

    for start, end, range_name in targeted_ranges:
        print(f'   🔍 Scanning {range_name}: {start}-{end}')

        for app_id in range(start, end + 1):
            try:
                app_info = algod_client.application_info(app_id)
                if app_info:
                    params = app_info.get('params', {})
                    global_state = params.get('global-state', [])

                    if len(global_state) > 2:  # Likely a DeFi app
                        found_contracts.append({
                            'protocol': 'Unknown',
                            'type': 'systematic_scan',
                            'value': str(app_id),
                            'source': f'Systematic scan: {range_name}'
                        })

                        print(f'      🎯 Found complex app: {app_id} ({len(global_state)} vars)')

                        # Analyze global state for DeFi patterns
                        lending_indicators = ['pool', 'lend', 'borrow', 'supply', 'reserve']
                        has_lending = False

                        for state_var in global_state[:5]:  # Check first 5
                            try:
                                import base64
                                key_b64 = state_var.get('key', '')
                                key = base64.b64decode(key_b64).decode('utf-8').lower()
                                if any(indicator in key for indicator in lending_indicators):
                                    has_lending = True
                                    break
                            except:
                                continue

                        if has_lending:
                            print('         💰 LIKELY LENDING POOL')
                        else:
                            print('         🤔 COMPLEX APPLICATION')

            except Exception as e:
                if 'not found' not in str(e).lower():
                    print(f'      ❌ Error checking {app_id}: {e}')

    # Strategy 4: Check real DeFi APIs
    print('\n🌐 CHECKING LIVE DeFi APIs...')

    api_endpoints = [
        'https://app.folks.finance/api/v1/config',
        'https://app.pact.fi/api/v1/config',
        'https://api.algoexplorer.io/v1/dapps/folks-finance',
        'https://api.algoexplorer.io/v1/dapps/pact'
    ]

    for url in api_endpoints:
        try:
            print(f'   🌐 Checking: {url}')
            response = requests.get(url, timeout=15)

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f'      ✅ Got API response')

                    # Look for app IDs in JSON structure
                    def find_app_ids(obj, path=''):
                        if isinstance(obj, dict):
                            for key, value in obj.items():
                                current_path = f'{path}.{key}' if path else key

                                if isinstance(value, (str, int)):
                                    value_str = str(value)
                                    if re.match(r'^\d{9,10}$', value_str):
                                        value_int = int(value_str)
                                        if (971350000 <= value_int <= 971360000 or
                                            1072800000 <= value_int <= 1072900000):

                                            protocol = 'Folks Finance' if 'folks' in url.lower() else 'Pact Finance'
                                            found_contracts.append({
                                                'protocol': protocol,
                                                'type': 'api_response',
                                                'value': value_str,
                                                'source': f'{url} -> {current_path}'
                                            })
                                            print(f'         🎯 Found app ID: {value_str}')

                                else:
                                    find_app_ids(value, current_path)

                        elif isinstance(obj, list):
                            for i, item in enumerate(obj):
                                find_app_ids(item, f'{path}[{i}]')

                    find_app_ids(data)

                except json.JSONDecodeError:
                    print('         ❌ Not JSON response')
            else:
                print(f'         ❌ Status: {response.status_code}')

        except Exception as e:
            print(f'         ❌ Error: {e}')

    # Remove duplicates
    unique_contracts = []
    seen = set()
    for contract in found_contracts:
        if contract['value'] not in seen:
            unique_contracts.append(contract)
            seen.add(contract['value'])

    print(f'\n🎯 SUMMARY:')
    print(f'   📊 Total unique contracts found: {len(unique_contracts)}')

    if unique_contracts:
        print('\n🏆 FOUND CONTRACTS:')
        for i, contract in enumerate(unique_contracts):
            print(f'   {i+1}. {contract["protocol"]} - App {contract["value"]} ({contract["type"]})')
            print(f'      📍 Source: {contract["source"]}')

    print('\n💡 NEXT STEPS:')
    print('   1. 🧪 Test the found contracts for opt-in functionality')
    print('   2. 📊 Analyze which ones are actually lending/farming pools')
    print('   3. 🔍 Verify on blockchain explorer')

    return unique_contracts

if __name__ == '__main__':
    asyncio.run(direct_contract_search())
