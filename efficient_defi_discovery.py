import asyncio
import requests
import json
from algosdk.v2client import algod

async def efficient_defi_discovery():
    print('🚀 EFFICIENT DeFi PROTOCOL DISCOVERY')
    print('=' * 40)

    # Initialize client
    algod_client = algod.AlgodClient('', 'https://mainnet-api.algonode.cloud')

    print('🔍 SEARCHING MULTIPLE SOURCES...')

    # Strategy 1: Check DeFiLlama API
    print('\n📊 STRATEGY 1: DeFiLlama API')

    try:
        # Check DeFiLlama for Algorand protocols
        defillama_url = 'https://api.llama.fi/protocols'
        response = requests.get(defillama_url, timeout=10)

        if response.status_code == 200:
            protocols = response.json()

            # Filter for Algorand protocols
            algo_protocols = [p for p in protocols if 'algorand' in p.get('chains', [])]

            folks_finance = [p for p in algo_protocols if 'folk' in p.get('name', '').lower()]
            pact_finance = [p for p in algo_protocols if 'pact' in p.get('name', '').lower()]

            if folks_finance:
                print(f'   🎯 Found Folks Finance: {folks_finance[0].get("name")}')
                print(f'      📊 TVL: ${folks_finance[0].get("tvl", 0):,.0f}')
                print(f'      🌐 URL: {folks_finance[0].get("url", "N/A")}')

            if pact_finance:
                print(f'   🎯 Found Pact Finance: {pact_finance[0].get("name")}')
                print(f'      📊 TVL: ${pact_finance[0].get("tvl", 0):,.0f}')
                print(f'      🌐 URL: {pact_finance[0].get("url", "N/A")}')

        else:
            print('   ❌ DeFiLlama API unavailable')

    except Exception as e:
        print(f'   ❌ DeFiLlama error: {e}')

    # Strategy 2: Check GitHub repositories
    print('\n📚 STRATEGY 2: GitHub Repositories')

    github_repos = [
        'https://api.github.com/repos/folks-finance/folks-finance-js-sdk',
        'https://api.github.com/repos/folks-finance/folks-finance-contracts',
        'https://api.github.com/repos/pactfi/pactfi-js-sdk',
        'https://api.github.com/repos/pactfi/pactfi-contracts'
    ]

    for repo_url in github_repos:
        try:
            response = requests.get(repo_url, timeout=10)
            if response.status_code == 200:
                repo_data = response.json()
                repo_name = repo_data.get('name', 'Unknown')
                print(f'   📚 Found {repo_name}')
                print(f'      ⭐ Stars: {repo_data.get("stargazers_count", 0)}')
                print(f'      📝 Description: {repo_data.get("description", "N/A")[:50]}...')

                # Check if there are releases with contract addresses
                releases_url = repo_data.get('releases_url', '').replace('{/id}', '')
                releases_response = requests.get(releases_url, timeout=10)

                if releases_response.status_code == 200:
                    releases = releases_response.json()
                    if releases:
                        latest_release = releases[0]
                        print(f'      🏷️ Latest Release: {latest_release.get("tag_name", "N/A")}')

        except Exception as e:
            print(f'   ❌ GitHub error for {repo_url}: {e}')

    # Strategy 3: Efficient app ID search using patterns
    print('\n🔍 STRATEGY 3: Smart App ID Search')

    # Search known DeFi app ID ranges more efficiently
    defi_ranges = [
        (971350000, 971360000, 'Folks Finance Range'),
        (1072800000, 1072900000, 'Pact Finance Range'),
        (600000, 700000, 'General DeFi Range'),
        (200000, 300000, 'Older DeFi Range')
    ]

    found_apps = []

    for start, end, range_name in defi_ranges:
        print(f'\n   🔍 Scanning {range_name}: {start}-{end}')

        # Sample every 100th app for efficiency
        for app_id in range(start, end, 100):
            try:
                app_info = algod_client.application_info(app_id)
                if app_info:
                    params = app_info.get('params', {})
                    creator = params.get('creator', '')

                    # Check for DeFi patterns
                    global_state = params.get('global-state', [])
                    approval_program = params.get('approval-program', '')

                    # Quick scoring
                    score = 0
                    if len(global_state) > 5:
                        score += 1
                    if len(approval_program) > 1000:
                        score += 1
                    if len(params.get('clear-program', '')) > 0:
                        score += 1

                    if score >= 2:
                        found_apps.append({
                            'app_id': app_id,
                            'creator': creator[:16],
                            'global_vars': len(global_state),
                            'score': score
                        })

                        print(f'      🎯 Found complex app: {app_id} (Score: {score})')
                        print(f'         👤 Creator: {creator[:16]}...')
                        print(f'         🌐 Global vars: {len(global_state)}')

                        # Limit results to avoid spam
                        if len(found_apps) >= 10:
                            break

            except:
                pass

        if len(found_apps) >= 10:
            break

    # Strategy 4: Check official documentation
    print('\n📖 STRATEGY 4: Official Documentation')

    docs_sites = [
        'https://docs.folks.finance',
        'https://docs.pact.fi',
        'https://pactfi.github.io',
        'https://folks-finance.github.io'
    ]

    for site in docs_sites:
        try:
            response = requests.get(site, timeout=5)
            if response.status_code == 200:
                print(f'   📖 Found documentation: {site}')

                # Look for contract addresses in the content
                content = response.text.lower()
                if 'app' in content and ('id' in content or 'address' in content):
                    print('      🔍 Contains contract information')

        except Exception as e:
            print(f'   ❌ Could not access {site}: {e}')

    print('\n🎯 SUMMARY OF FINDINGS:')
    print(f'   📊 Potential DeFi apps found: {len(found_apps)}')
    print('   🔍 Efficient search complete')

    if found_apps:
        print('\n🏦 TOP CANDIDATES:')
        for i, app in enumerate(found_apps[:5]):
            print(f'   {i+1}. App {app["app_id"]} - Creator: {app["creator"]} - Score: {app["score"]}')

    print('\n💡 NEXT STEPS:')
    print('   1. 🧪 Test the top candidate apps for opt-in functionality')
    print('   2. 📖 Check official documentation for contract addresses')
    print('   3. 🔍 Use blockchain explorer to verify findings')

if __name__ == '__main__':
    asyncio.run(efficient_defi_discovery())

