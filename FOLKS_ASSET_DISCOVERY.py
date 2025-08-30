#!/usr/bin/env python3
"""
FOLKS ASSET DISCOVERY
Discover the exact assets required by Folks Finance protocol
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod

class FolksAssetDiscovery:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID
        self.folks_app_id = 465814065
        
        print("🔍 FOLKS ASSET DISCOVERY")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{self.wallet_address[-10:]}")
        print(f"🎯 Discovering exact assets required by Folks Finance")
    
    def discover_protocol_assets(self) -> Dict:
        """Discover the exact assets required by Folks Finance"""
        print("🔍 DISCOVERING PROTOCOL ASSETS")
        print("=" * 50)
        
        discovery_results = {}
        
        try:
            # Get app information
            print("📋 Getting Folks Finance app information...")
            app_info = self.algod_client.application_info(self.folks_app_id)
            
            # Get global state
            print("🌐 Getting global state...")
            global_state = app_info.get('params', {}).get('global-state', [])
            
            print(f"✅ Global state entries: {len(global_state)}")
            
            # Analyze global state for asset information
            asset_discovery = self._analyze_global_state(global_state)
            discovery_results['global_state_analysis'] = asset_discovery
            
            # Get app creator account
            print("👤 Getting app creator account...")
            creator_address = app_info['params']['creator']
            creator_assets = self._analyze_creator_assets(creator_address)
            discovery_results['creator_assets'] = creator_assets
            
            # Look for related apps
            print("🔗 Looking for related apps...")
            related_apps = self._find_related_apps(creator_address)
            discovery_results['related_apps'] = related_apps
            
            # Search for asset references in global state
            print("🔍 Searching for asset references...")
            asset_references = self._find_asset_references(global_state)
            discovery_results['asset_references'] = asset_references
            
        except Exception as e:
            print(f"❌ Error in asset discovery: {e}")
            discovery_results['error'] = str(e)
        
        return discovery_results
    
    def _analyze_global_state(self, global_state: List) -> Dict:
        """Analyze global state for asset information"""
        print("   📊 Analyzing global state...")
        
        analysis = {
            'total_entries': len(global_state),
            'key_value_pairs': [],
            'potential_assets': [],
            'protocol_config': {}
        }
        
        for entry in global_state:
            key = entry.get('key', '')
            value = entry.get('value', {})
            
            # Decode key if it's base64
            try:
                import base64
                decoded_key = base64.b64decode(key).decode('utf-8', errors='ignore')
            except:
                decoded_key = key
            
            analysis['key_value_pairs'].append({
                'key': key,
                'decoded_key': decoded_key,
                'value_type': value.get('type'),
                'value': value
            })
            
            # Look for asset-related keys
            if 'asset' in decoded_key.lower() or 'token' in decoded_key.lower():
                analysis['potential_assets'].append({
                    'key': decoded_key,
                    'value': value
                })
            
            # Look for configuration keys
            if 'config' in decoded_key.lower() or 'param' in decoded_key.lower():
                analysis['protocol_config'][decoded_key] = value
        
        print(f"      Found {len(analysis['potential_assets'])} potential asset references")
        print(f"      Found {len(analysis['protocol_config'])} configuration entries")
        
        return analysis
    
    def _analyze_creator_assets(self, creator_address: str) -> Dict:
        """Analyze the creator account for assets"""
        print("   👤 Analyzing creator account...")
        
        try:
            creator_info = self.algod_client.account_info(creator_address)
            
            analysis = {
                'creator_address': creator_address,
                'total_assets': len(creator_info.get('assets', [])),
                'assets': creator_info.get('assets', []),
                'created_apps': len(creator_info.get('created-apps', [])),
                'apps_local_state': len(creator_info.get('apps-local-state', []))
            }
            
            print(f"      Creator has {analysis['total_assets']} assets")
            print(f"      Creator has {analysis['created_apps']} created apps")
            
            # Look for specific asset patterns
            if analysis['assets']:
                print("      Creator assets:")
                for asset in analysis['assets'][:5]:  # Show first 5
                    asset_id = asset.get('asset-id')
                    balance = asset.get('amount', 0)
                    print(f"         Asset {asset_id}: Balance {balance}")
            
            return analysis
            
        except Exception as e:
            print(f"      ❌ Error analyzing creator: {e}")
            return {'error': str(e)}
    
    def _find_related_apps(self, creator_address: str) -> Dict:
        """Find apps related to Folks Finance"""
        print("   🔗 Finding related apps...")
        
        try:
            creator_info = self.algod_client.account_info(creator_address)
            created_apps = creator_info.get('created-apps', [])
            
            related_apps = []
            
            for app in created_apps:
                app_id = app.get('id')
                app_name = app.get('params', {}).get('name', 'Unknown')
                
                # Look for apps that might be related to Folks Finance
                if app_id != self.folks_app_id:  # Exclude the main app
                    related_apps.append({
                        'app_id': app_id,
                        'name': app_name,
                        'creator': app.get('params', {}).get('creator', 'Unknown')
                    })
            
            print(f"      Found {len(related_apps)} related apps")
            
            return {
                'total_related': len(related_apps),
                'apps': related_apps
            }
            
        except Exception as e:
            print(f"      ❌ Error finding related apps: {e}")
            return {'error': str(e)}
    
    def _find_asset_references(self, global_state: List) -> Dict:
        """Find specific asset references in global state"""
        print("   🔍 Finding asset references...")
        
        asset_refs = {
            'asset_ids': [],
            'asset_names': [],
            'market_configs': []
        }
        
        for entry in global_state:
            key = entry.get('key', '')
            value = entry.get('value', {})
            
            try:
                import base64
                decoded_key = base64.b64decode(key).decode('utf-8', errors='ignore')
            except:
                decoded_key = key
            
            # Look for specific asset ID patterns
            if 'asset' in decoded_key.lower():
                # Check if value contains an asset ID
                if value.get('type') == 1:  # uint type
                    asset_id = value.get('uint', 0)
                    if asset_id > 0:
                        asset_refs['asset_ids'].append({
                            'key': decoded_key,
                            'asset_id': asset_id
                        })
                        print(f"         Found asset ID: {asset_id} in key '{decoded_key}'")
            
            # Look for market configurations
            if 'market' in decoded_key.lower() or 'pool' in decoded_key.lower():
                asset_refs['market_configs'].append({
                    'key': decoded_key,
                    'value': value
                })
        
        return asset_refs
    
    def run_complete_discovery(self) -> Dict:
        """Run complete asset discovery"""
        print("🚀 COMPLETE ASSET DISCOVERY")
        print("=" * 60)
        
        # Run discovery
        discovery_results = self.discover_protocol_assets()
        
        # Display results
        print(f"\n📊 ASSET DISCOVERY RESULTS")
        print("=" * 40)
        
        if 'global_state_analysis' in discovery_results:
            gs_analysis = discovery_results['global_state_analysis']
            print(f"🌐 Global State Analysis:")
            print(f"   Total entries: {gs_analysis['total_entries']}")
            print(f"   Potential assets: {len(gs_analysis['potential_assets'])}")
            print(f"   Configuration entries: {len(gs_analysis['protocol_config'])}")
        
        if 'creator_assets' in discovery_results:
            creator = discovery_results['creator_assets']
            if 'error' not in creator:
                print(f"\n👤 Creator Account Analysis:")
                print(f"   Total assets: {creator['total_assets']}")
                print(f"   Created apps: {creator['created_apps']}")
        
        if 'asset_references' in discovery_results:
            asset_refs = discovery_results['asset_references']
            print(f"\n🔍 Asset References Found:")
            print(f"   Asset IDs: {len(asset_refs['asset_ids'])}")
            print(f"   Market configs: {len(asset_refs['market_configs'])}")
            
            if asset_refs['asset_ids']:
                print("   Specific Asset IDs:")
                for ref in asset_refs['asset_ids']:
                    print(f"      • {ref['asset_id']} (from '{ref['key']}')")
        
        # Save results
        with open('folks_asset_discovery.json', 'w') as f:
            json.dump(discovery_results, f, indent=2, default=str)
        
        print(f"\n📁 Asset discovery results saved to: folks_asset_discovery.json")
        
        return discovery_results

def main():
    """Test the Folks asset discovery system"""
    print("🧪 TESTING FOLKS ASSET DISCOVERY")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Folks Asset Discovery System ready!")
    print("🎯 This system will find the exact assets required!")
    print("🔗 Import this into your hybrid trading empire for protocol analysis!")

if __name__ == "__main__":
    main()
