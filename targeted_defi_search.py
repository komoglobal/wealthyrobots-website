import asyncio
import requests
import json
import re
from algosdk.v2client import algod, indexer
from bs4 import BeautifulSoup

async def targeted_defi_search():
    print('🎯 TARGETED DeFi PROTOCOL SEARCH')
    print('=' * 40)

    # Initialize clients
    algod_client = algod.AlgodClient('', 'https://mainnet-api.algonode.cloud')
    indexer_client = indexer.IndexerClient('', 'https://mainnet-idx.algonode.cloud')

    print('📖 EXTRACTING FROM OFFICIAL DOCUMENTATION...')

    # Strategy 1: Scrape official documentation for contract addresses
    docs_sites = {
        'Folks Finance': 'https://docs.folks.finance',
        'Pact Finance': 'https://docs.pact.fi'
    }

    found_contracts = []

    for protocol, url in docs_sites.items():
        print(f'\n🔍 Analyzing {protocol} documentation: {url}')

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text().lower()

                # Look for app IDs, contract addresses, application IDs
                patterns = [
                    r'app[_-]?id[:\s]*(\d+)',
                    r'application[_-]?id[:\s]*(\d+)',
                    r'contract[_-]?address[:\s]*([A-Z0-9]{58})',
                    r'pool[_-]?id[:\s]*(\d+)',
                    r'asset[_-]?id[:\s]*(\d+)'
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text)
                    for match in matches:
                        if match and len(str(match)) > 5:  # Filter out small numbers
                            found_contracts.append({
                                'protocol': protocol,
                                'type': 'documentation',
                                'value': match,
                                'source': url
                            })
                            print(f'   🎯 Found: {match}')

                # Also check for specific known addresses
                if '97135' in text or '97136' in text:
                    print('   🎯 Contains Folks Finance app ID range')
                if '10728' in text or '10729' in text:
                    print('   🎯 Contains Pact Finance app ID range')

        except Exception as e:
            print(f'   ❌ Error accessing {url}: {e}')

    # Strategy 2: Check GitHub repositories for addresses
    print('\n📚 SEARCHING GITHUB REPOSITORIES...')

    github_files = [
        'https://api.github.com/repos/folks-finance/folks-finance-js-sdk/contents',
        'https://api.github.com/repos/pactfi/pactfi-js-sdk/contents',
        'https://raw.githubusercontent.com/folks-finance/folks-finance-js-sdk/main/README.md',
        'https://raw.githubusercontent.com/pactfi/pactfi-js-sdk/main/README.md'
    ]

    for url in github_files:
        try:
            if 'contents' in url:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    files = response.json()
                    for file in files:
                        if file['name'].endswith(('.md', '.json', '.ts', '.js')):
                            print(f'   📄 Checking {file["name"]}...')

                            if file['download_url']:
                                file_response = requests.get(file['download_url'], timeout=10)
                                if file_response.status_code == 200:
                                    content = file_response.text.lower()

                                    # Look for contract addresses
                                    app_id_matches = re.findall(r'\b(\d{9,10})\b', content)
                                    for match in app_id_matches:
                                        if 971350000 <= int(match) <= 971360000 or 1072800000 <= int(match) <= 1072900000:
                                            found_contracts.append({
                                                'protocol': 'Unknown',
                                                'type': 'github_file',
                                                'value': match,
                                                'source': file['download_url']
                                            })
                                            print(f'      🎯 Found DeFi app ID: {match}')

            else:
                # Direct file access
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    content = response.text.lower()

                    app_id_matches = re.findall(r'\b(\d{9,10})\b', content)
                    for match in app_id_matches:
                        if 971350000 <= int(match) <= 971360000 or 1072800000 <= int(match) <= 1072900000:
                            protocol_name = 'Folks Finance' if 'folks' in url.lower() else 'Pact Finance'
                            found_contracts.append({
                                'protocol': protocol_name,
                                'type': 'github_readme',
                                'value': match,
                                'source': url
                            })
                            print(f'   🎯 Found in README: {match}')

        except Exception as e:
            print(f'   ❌ Error accessing GitHub: {e}')

    # Strategy 3: Use Indexer API for efficient searching
    print('\n🔍 USING INDEXER API FOR VERIFICATION...')

    # Search for known creators or patterns
    search_creators = [
        'OL4EMRL54OZFBMHGNJZIV5RLJ7O3VTIEWPQDMIIU26JLXZ3DDB6FC3YYIM',  # User's wallet
        'FOLKSFINANCE',  # Common naming pattern
        'PACTFINANCE'
    ]

    for creator in search_creators:
        try:
            apps = indexer_client.search_applications(creator=creator)
            for app in apps['applications']:
                app_id = app['id']
                print(f'   🎯 Found app by creator {creator[:16]}...: {app_id}')

                found_contracts.append({
                    'protocol': 'Unknown',
                    'type': 'indexer_creator',
                    'value': str(app_id),
                    'source': f'Creator search: {creator[:16]}...'
                })

        except Exception as e:
            print(f'   ❌ Indexer search error: {e}')

    # Strategy 4: Check DeFi protocol aggregators
    print('\n🌐 CHECKING DeFi AGGREGATORS...')

    aggregator_urls = [
        'https://app.folks.finance/api/v1/pools',
        'https://api.pact.fi/v1/pools',
        'https://api.algoexplorer.io/v1/applications'
    ]

    for url in aggregator_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()

                if 'pools' in str(data).lower():
                    print(f'   🎯 Found pools data at {url}')

                    # Extract app IDs from pools
                    if isinstance(data, list):
                        for pool in data[:5]:  # Check first 5
                            if isinstance(pool, dict):
                                app_id = pool.get('appId') or pool.get('application_id') or pool.get('id')
                                if app_id and isinstance(app_id, int):
                                    protocol = 'Folks Finance' if 'folks' in url else 'Pact Finance'
                                    found_contracts.append({
                                        'protocol': protocol,
                                        'type': 'aggregator_api',
                                        'value': str(app_id),
                                        'source': url
                                    })
                                    print(f'      🏦 Pool app ID: {app_id}')

        except Exception as e:
            print(f'   ❌ Aggregator error for {url}: {e}')

    # Strategy 5: Test found contracts
    print('\n🧪 TESTING FOUND CONTRACTS...')

    unique_contracts = []
    seen = set()
    for contract in found_contracts:
        if contract['value'] not in seen:
            unique_contracts.append(contract)
            seen.add(contract['value'])

    print(f'   📊 Found {len(unique_contracts)} unique potential contracts')

    for i, contract in enumerate(unique_contracts[:10]):  # Test first 10
        app_id = int(contract['value'])
        print(f'   {i+1}. Testing {contract["protocol"]} app {app_id}...')

        try:
            app_info = algod_client.application_info(app_id)
            if app_info:
                params = app_info.get('params', {})
                global_state = params.get('global-state', [])

                print(f'      ✅ Valid app with {len(global_state)} global vars')
                print(f'      👤 Creator: {params.get("creator", "")[:20]}...')

                # Check if it looks like a DeFi app
                if len(global_state) > 3:
                    print('      🎯 POTENTIAL DeFi APPLICATION')
                else:
                    print('      ❓ Simple application')

        except Exception as e:
            print(f'      ❌ Invalid or inaccessible app: {e}')

    print('\n🎯 SUMMARY:')
    print(f'   📊 Total contracts found: {len(unique_contracts)}')
    print(f'   🔍 Protocols identified: {set(c["protocol"] for c in unique_contracts)}')

    if unique_contracts:
        print('\n🏆 TOP CANDIDATES:')
        for i, contract in enumerate(unique_contracts[:5]):
            print(f'   {i+1}. {contract["protocol"]} - {contract["value"]} ({contract["type"]})')

    print('\n💡 NEXT STEPS:')
    print('   1. 🧪 Test opt-in functionality on promising candidates')
    print('   2. 📖 Manually verify contracts on blockchain explorer')
    print('   3. 🔍 Cross-reference with official documentation')

if __name__ == '__main__':
    asyncio.run(targeted_defi_search())









