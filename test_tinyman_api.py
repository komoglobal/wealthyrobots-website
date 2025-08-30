#!/usr/bin/env python3
"""Test Tinyman API response format"""

import asyncio
import aiohttp
import json

async def test_tinyman_api():
    """Test Tinyman API response"""
    url = "https://mainnet.analytics.tinyman.org/api/v1/pools"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API Response Status: {response.status}")
                    print(f"📊 Data type: {type(data)}")
                    print(f"📊 Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    
                    if data:
                        if isinstance(data, dict):
                            # Check if results key exists
                            if 'results' in data and data['results']:
                                first_pool = data['results'][0]
                                print(f"🔍 First pool data (from results):")
                                print(f"Type: {type(first_pool)}")
                                print(f"Raw: {first_pool}")
                                
                                if isinstance(first_pool, dict):
                                    print(f"\n📋 Available fields in first pool:")
                                    for key, value in first_pool.items():
                                        print(f"  {key}: {type(value).__name__} = {value}")
                                else:
                                    print(f"⚠️ First pool is not a dict: {type(first_pool)}")
                            else:
                                print(f"⚠️ No results found in API response")
                                print(f"Available keys: {list(data.keys())}")
                        else:
                            print(f"⚠️ Data is not a dict: {type(data)}")
                    else:
                        print("❌ No data returned from API")
                else:
                    print(f"❌ API Error: {response.status}")
                    
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tinyman_api())
