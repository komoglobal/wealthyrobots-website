#!/usr/bin/env python3
"""
Test API Integrations - Wealthy Robot Empire
Tests all DeFi protocol API endpoints and app IDs
"""

import asyncio
import aiohttp
import json
from datetime import datetime

class APIIntegrationTester:
    """Test all DeFi protocol API integrations"""
    
    def __init__(self):
        self.results = {}
        
    async def test_tinyman_apis(self):
        """Test Tinyman V2 API endpoints"""
        print("🔍 Testing Tinyman V2 APIs...")
        
        endpoints = [
            "https://mainnet.analytics.tinyman.org/api/v1/pools",
            "https://mainnet.analytics.tinyman.org/api/v1/pools/",
            "https://router.tinyman.org/pools",
            "https://mainnet-idx.algonode.cloud/v2/applications/1002541853/boxes"
        ]
        
        tinyman_results = {}
        for endpoint in endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            tinyman_results[endpoint] = {
                                'status': 'success',
                                'data_length': len(data) if isinstance(data, list) else 1,
                                'response_time': response.headers.get('x-response-time', 'unknown')
                            }
                        else:
                            tinyman_results[endpoint] = {
                                'status': 'failed',
                                'status_code': response.status,
                                'error': f"HTTP {response.status}"
                            }
            except Exception as e:
                tinyman_results[endpoint] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        self.results['tinyman'] = tinyman_results
        print(f"✅ Tinyman APIs tested: {len([r for r in tinyman_results.values() if r['status'] == 'success'])}/{len(endpoints)} working")
        
    async def test_pact_finance_apis(self):
        """Test Pact Finance API endpoints"""
        print("🌾 Testing Pact Finance APIs...")
        
        endpoints = [
            "https://api.pact.fi/pools",
            "https://api.pact.fi/farms",
            "https://api.pact.fi/stats"
        ]
        
        pact_results = {}
        for endpoint in endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            pact_results[endpoint] = {
                                'status': 'success',
                                'data_length': len(data) if isinstance(data, list) else 1,
                                'response_time': response.headers.get('x-response-time', 'unknown')
                            }
                        else:
                            pact_results[endpoint] = {
                                'status': 'failed',
                                'status_code': response.status,
                                'error': f"HTTP {response.status}"
                            }
            except Exception as e:
                pact_results[endpoint] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        self.results['pact_finance'] = pact_results
        print(f"✅ Pact Finance APIs tested: {len([r for r in pact_results.values() if r['status'] == 'success'])}/{len(endpoints)} working")
        
    async def test_folks_finance_apis(self):
        """Test Folks Finance API endpoints"""
        print("💰 Testing Folks Finance APIs...")
        
        endpoints = [
            "https://api.folks.finance/pools",
            "https://api.folks.finance/lending-pools",
            "https://api.folks.finance/api/pools"
        ]
        
        folks_results = {}
        for endpoint in endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            folks_results[endpoint] = {
                                'status': 'success',
                                'data_length': len(data) if isinstance(data, list) else 1,
                                'response_time': response.headers.get('x-response-time', 'unknown')
                            }
                        else:
                            folks_results[endpoint] = {
                                'status': 'failed',
                                'status_code': response.status,
                                'error': f"HTTP {response.status}"
                            }
            except Exception as e:
                folks_results[endpoint] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        self.results['folks_finance'] = folks_results
        print(f"✅ Folks Finance APIs tested: {len([r for r in folks_results.values() if r['status'] == 'success'])}/{len(endpoints)} working")
        
    async def test_app_ids(self):
        """Test all application IDs on the blockchain"""
        print("🔗 Testing Application IDs...")
        
        app_ids = {
            'tinyman_v2': 1002541853,
            'pact_factory': 1072843805,
            'pact_gas_station': 1027956681,
            'pact_folks_adapter': 1123472996,
            'pact_nft_factory': 1076423760,
            'folks_pool_manager': 971350278,
            'folks_deposit': 971353536,
            'folks_staking': 1093729103,
            'folks_algo_pool': 971368268,
            'folks_galgo_pool': 971370097
        }
        
        app_results = {}
        for name, app_id in app_ids.items():
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"https://mainnet-api.algonode.cloud/v2/applications/{app_id}"
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            app_results[name] = {
                                'status': 'exists',
                                'app_id': app_id,
                                'creator': data.get('params', {}).get('creator', 'unknown'),
                                'name': data.get('params', {}).get('name', 'unknown')
                            }
                        else:
                            app_results[name] = {
                                'status': 'not_found',
                                'app_id': app_id,
                                'error': f"HTTP {response.status}"
                            }
            except Exception as e:
                app_results[name] = {
                    'status': 'error',
                    'app_id': app_id,
                    'error': str(e)
                }
        
        self.results['app_ids'] = app_results
        working_apps = len([r for r in app_results.values() if r['status'] == 'exists'])
        print(f"✅ Application IDs tested: {working_apps}/{len(app_ids)} exist on blockchain")
        
    async def run_all_tests(self):
        """Run all API integration tests"""
        print("🚀 Starting API Integration Tests...")
        print("=" * 60)
        
        await self.test_tinyman_apis()
        await self.test_pact_finance_apis()
        await self.test_folks_finance_apis()
        await self.test_app_ids()
        
        print("=" * 60)
        print("📊 Test Results Summary:")
        self.print_summary()
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"api_test_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to: {filename}")
        
    def print_summary(self):
        """Print a summary of all test results"""
        for category, results in self.results.items():
            print(f"\n📋 {category.replace('_', ' ').title()}:")
            
            if category == 'app_ids':
                working = len([r for r in results.values() if r['status'] == 'exists'])
                total = len(results)
                print(f"   ✅ Working: {working}/{total}")
                
                # Show failed app IDs
                failed = [name for name, result in results.items() if result['status'] != 'exists']
                if failed:
                    print(f"   ❌ Failed: {', '.join(failed)}")
            else:
                working = len([r for r in results.values() if r['status'] == 'success'])
                total = len(results)
                print(f"   ✅ Working: {working}/{total}")
                
                # Show failed endpoints
                failed = [endpoint for endpoint, result in results.items() if result['status'] != 'success']
                if failed:
                    print(f"   ❌ Failed: {len(failed)} endpoints")

async def main():
    """Main test function"""
    tester = APIIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
