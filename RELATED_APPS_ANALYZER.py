#!/usr/bin/env python3
"""
RELATED APPS ANALYZER
Analyze the 8 related apps created by Folks Finance creator
Find the exact assets required by the protocol
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod

class RelatedAppsAnalyzer:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID
        self.folks_app_id = 465814065
        
        # Folks Finance creator
        self.folks_creator = "3EPGHSNBBN5M2LD6V7A63EHZQQLATVQHDBYJQIZ6BLCBTIXA5XR7ZOZEB4"
        
        print("🔍 RELATED APPS ANALYZER")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{self.wallet_address[-10:]}")
        print(f"🎯 Analyzing 8 related apps to find required assets")
    
    def analyze_related_apps(self) -> Dict:
        """Analyze all related apps created by Folks Finance creator"""
        print("🔍 ANALYZING RELATED APPS")
        print("=" * 50)
        
        analysis_results = {}
        
        try:
            # Get creator account info
            print("👤 Getting creator account information...")
            creator_info = self.algod_client.account_info(self.folks_creator)
            created_apps = creator_info.get('created-apps', [])
            
            print(f"✅ Creator has {len(created_apps)} created apps")
            
            # Filter out the main Folks Finance app
            related_apps = [app for app in created_apps if app.get('id') != self.folks_app_id]
            
            print(f"🔗 Found {len(related_apps)} related apps to analyze")
            
            # Analyze each related app
            app_analyses = {}
            
            for i, app in enumerate(related_apps):
                app_id = app.get('id')
                app_name = app.get('params', {}).get('name', f'App_{app_id}')
                
                print(f"\n   🔍 Analyzing App {i+1}/{len(related_apps)}: {app_name}")
                print(f"      App ID: {app_id}")
                
                try:
                    app_analysis = self._analyze_single_app(app_id, app_name)
                    app_analyses[app_id] = app_analysis
                    
                    if app_analysis.get('asset_discovery'):
                        assets = app_analysis['asset_discovery']
                        print(f"      🎯 Found {len(assets.get('asset_ids', []))} asset references!")
                        
                except Exception as e:
                    print(f"      ❌ Error analyzing app: {e}")
                    app_analyses[app_id] = {'error': str(e)}
                
                time.sleep(1)  # Wait between app analyses
            
            analysis_results['related_apps'] = app_analyses
            analysis_results['total_related'] = len(related_apps)
            
            # Compile all discovered assets
            all_discovered_assets = self._compile_discovered_assets(app_analyses)
            analysis_results['all_discovered_assets'] = all_discovered_assets
            
        except Exception as e:
            print(f"❌ Error analyzing related apps: {e}")
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    def _analyze_single_app(self, app_id: int, app_name: str) -> Dict:
        """Analyze a single related app"""
        try:
            # Get app information
            app_info = self.algod_client.application_info(app_id)
            
            analysis = {
                'app_id': app_id,
                'app_name': app_name,
                'creator': app_info['params']['creator'],
                'global_state_schema': app_info['params']['global-state-schema'],
                'local_state_schema': app_info['params']['local-state-schema']
            }
            
            # Get global state
            global_state = app_info.get('params', {}).get('global-state', [])
            analysis['global_state_size'] = len(global_state)
            
            # Look for asset references in global state
            asset_discovery = self._find_assets_in_app_state(global_state, app_name)
            analysis['asset_discovery'] = asset_discovery
            
            # Look for specific patterns
            if global_state:
                # Check for common DeFi patterns
                patterns = self._find_defi_patterns(global_state)
                analysis['defi_patterns'] = patterns
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _find_assets_in_app_state(self, global_state: List, app_name: str) -> Dict:
        """Find assets in app global state"""
        asset_discovery = {
            'asset_ids': [],
            'asset_names': [],
            'market_configs': [],
            'pool_configs': []
        }
        
        for entry in global_state:
            key = entry.get('key', '')
            value = entry.get('value', {})
            
            try:
                import base64
                decoded_key = base64.b64decode(key).decode('utf-8', errors='ignore')
            except:
                decoded_key = key
            
            # Look for asset ID patterns
            if 'asset' in decoded_key.lower():
                if value.get('type') == 1:  # uint type
                    asset_id = value.get('uint', 0)
                    if asset_id > 0:
                        asset_discovery['asset_ids'].append({
                            'key': decoded_key,
                            'asset_id': asset_id,
                            'app_name': app_name
                        })
            
            # Look for market configurations
            if 'market' in decoded_key.lower():
                asset_discovery['market_configs'].append({
                    'key': decoded_key,
                    'value': value,
                    'app_name': app_name
                })
            
            # Look for pool configurations
            if 'pool' in decoded_key.lower():
                asset_discovery['pool_configs'].append({
                    'key': decoded_key,
                    'value': value,
                    'app_name': app_name
                })
        
        return asset_discovery
    
    def _find_defi_patterns(self, global_state: List) -> Dict:
        """Find DeFi-specific patterns in global state"""
        patterns = {
            'lending_patterns': [],
            'borrowing_patterns': [],
            'yield_patterns': [],
            'collateral_patterns': []
        }
        
        for entry in global_state:
            key = entry.get('key', '')
            value = entry.get('value', {})
            
            try:
                import base64
                decoded_key = base64.b64decode(key).decode('utf-8', errors='ignore')
            except:
                decoded_key = key
            
            # Look for lending patterns
            if any(word in decoded_key.lower() for word in ['lend', 'supply', 'deposit']):
                patterns['lending_patterns'].append({
                    'key': decoded_key,
                    'value': value
                })
            
            # Look for borrowing patterns
            if any(word in decoded_key.lower() for word in ['borrow', 'loan', 'debt']):
                patterns['borrowing_patterns'].append({
                    'key': decoded_key,
                    'value': value
                })
            
            # Look for yield patterns
            if any(word in decoded_key.lower() for word in ['yield', 'apy', 'rate']):
                patterns['yield_patterns'].append({
                    'key': decoded_key,
                    'value': value
                })
            
            # Look for collateral patterns
            if any(word in decoded_key.lower() for word in ['collateral', 'collat', 'ratio']):
                patterns['collateral_patterns'].append({
                    'key': decoded_key,
                    'value': value
                })
        
        return patterns
    
    def _compile_discovered_assets(self, app_analyses: Dict) -> Dict:
        """Compile all discovered assets from all apps"""
        print("   📊 Compiling all discovered assets...")
        
        all_assets = {
            'unique_asset_ids': set(),
            'asset_details': [],
            'market_configs': [],
            'pool_configs': []
        }
        
        for app_id, analysis in app_analyses.items():
            if 'asset_discovery' in analysis:
                asset_discovery = analysis['asset_discovery']
                
                # Collect asset IDs
                for asset_ref in asset_discovery.get('asset_ids', []):
                    asset_id = asset_ref['asset_id']
                    all_assets['unique_asset_ids'].add(asset_id)
                    all_assets['asset_details'].append(asset_ref)
                
                # Collect market configs
                all_assets['market_configs'].extend(asset_discovery.get('market_configs', []))
                
                # Collect pool configs
                all_assets['pool_configs'].extend(asset_discovery.get('pool_configs', []))
        
        # Convert set to list for JSON serialization
        all_assets['unique_asset_ids'] = list(all_assets['unique_asset_ids'])
        
        print(f"      Found {len(all_assets['unique_asset_ids'])} unique asset IDs")
        print(f"      Found {len(all_assets['market_configs'])} market configurations")
        print(f"      Found {len(all_assets['pool_configs'])} pool configurations")
        
        return all_assets
    
    def run_complete_analysis(self) -> Dict:
        """Run complete analysis of related apps"""
        print("🚀 COMPLETE RELATED APPS ANALYSIS")
        print("=" * 60)
        
        # Run analysis
        analysis_results = self.analyze_related_apps()
        
        # Display results
        print(f"\n📊 RELATED APPS ANALYSIS RESULTS")
        print("=" * 40)
        
        if 'related_apps' in analysis_results:
            related_apps = analysis_results['related_apps']
            print(f"🔗 Related Apps Analyzed: {len(related_apps)}")
            
            for app_id, analysis in related_apps.items():
                if 'error' not in analysis:
                    app_name = analysis.get('app_name', 'Unknown')
                    asset_count = len(analysis.get('asset_discovery', {}).get('asset_ids', []))
                    print(f"   • {app_name}: {asset_count} asset references")
        
        if 'all_discovered_assets' in analysis_results:
            all_assets = analysis_results['all_discovered_assets']
            print(f"\n🎯 TOTAL ASSETS DISCOVERED:")
            print(f"   Unique Asset IDs: {len(all_assets['unique_asset_ids'])}")
            print(f"   Market Configs: {len(all_assets['market_configs'])}")
            print(f"   Pool Configs: {len(all_assets['pool_configs'])}")
            
            if all_assets['unique_asset_ids']:
                print(f"\n🔍 SPECIFIC ASSET IDs FOUND:")
                for asset_id in all_assets['unique_asset_ids']:
                    print(f"   • {asset_id}")
                
                print(f"\n🚀 NEXT STEP: Opt into these specific assets!")
                print("💰 This should solve the PC 297 validation issue!")
            else:
                print(f"\n🔍 No specific asset IDs found in related apps")
                print("📊 Need to analyze other protocol aspects")
        
        # Save results
        with open('related_apps_analysis.json', 'w') as f:
            json.dump(analysis_results, f, indent=2, default=str)
        
        print(f"\n📁 Related apps analysis saved to: related_apps_analysis.json")
        
        return analysis_results

def main():
    """Test the related apps analyzer"""
    print("🧪 TESTING RELATED APPS ANALYZER")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Related Apps Analyzer ready!")
    print("🎯 This system will analyze related apps to find required assets!")
    print("🔗 Import this into your hybrid trading empire for protocol analysis!")

if __name__ == "__main__":
    main()
