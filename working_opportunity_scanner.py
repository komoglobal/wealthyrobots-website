#!/usr/bin/env python3
"""
Working Opportunity Scanner - WealthyRobot
Scans working APIs for real trading opportunities
"""

import os
import json
import time
import asyncio
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from decimal import Decimal

class WorkingOpportunityScanner:
    """Scans working APIs for trading opportunities"""
    
    def __init__(self):
        self.name = "Working Opportunity Scanner"
        self.version = "1.0.0"
        self.logger = self._setup_logging()
        
        # Working data sources
        self.data_sources = {
            'tinyman': {
                'enabled': True,
                'base_url': 'https://mainnet.analytics.tinyman.org/api/v1',
                'endpoints': {
                    'pools': '/pools',
                    'quote': '/quote'
                }
            },
            'algo_explorer': {
                'enabled': True,
                'base_url': 'https://algoexplorer.io/api/v1',
                'endpoints': {
                    'assets': '/assets',
                    'transactions': '/transactions'
                }
            }
        }
        
        # Opportunity storage
        self.opportunities = []
        self.last_scan = None
        self.scan_interval = 300  # 5 minutes
        
        # Performance metrics
        self.total_scans = 0
        self.total_opportunities_found = 0
        self.start_time = datetime.now()
    
    def _setup_logging(self):
        """Setup logging"""
        os.makedirs('logs', exist_ok=True)
        
        log_file = f'logs/working_scanner_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger('WorkingOpportunityScanner')
    
    async def scan_tinyman_working(self) -> List[Dict[str, Any]]:
        """Scan Tinyman for working opportunities"""
        opportunities = []
        
        try:
            self.logger.info("🔍 Scanning Tinyman for working opportunities...")
            
            # Get Tinyman pools
            pools_url = f"{self.data_sources['tinyman']['base_url']}/pools"
            response = requests.get(pools_url, timeout=15)
            
            if response.status_code == 200:
                try:
                    pools_data = response.json()
                    
                    # Handle different response formats
                    if isinstance(pools_data, list):
                        pools = pools_data
                    elif isinstance(pools_data, dict) and 'data' in pools_data:
                        pools = pools_data['data']
                    else:
                        pools = []
                    
                    self.logger.info(f"✅ Found {len(pools)} Tinyman pools")
                    
                    for pool in pools:
                        if isinstance(pool, dict):
                            opportunity = self._analyze_tinyman_pool_working(pool)
                            if opportunity:
                                opportunities.append(opportunity)
                
                except json.JSONDecodeError as e:
                    self.logger.error(f"❌ JSON decode error: {e}")
                    self.logger.error(f"Response content: {response.text[:200]}")
                except Exception as e:
                    self.logger.error(f"❌ Error parsing Tinyman response: {e}")
            
            else:
                self.logger.warning(f"⚠️ Tinyman API failed: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"❌ Error scanning Tinyman: {e}")
        
        return opportunities
    
    def _analyze_tinyman_pool_working(self, pool: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a Tinyman pool for opportunities"""
        try:
            # Extract pool information safely
            asset1_name = pool.get('asset1_name', pool.get('asset1Name', 'Unknown'))
            asset2_name = pool.get('asset2_name', pool.get('asset2Name', 'Unknown'))
            
            # Try different possible keys for liquidity
            liquidity = 0
            if 'liquidity' in pool:
                liquidity = float(pool['liquidity'])
            elif 'liquidity_usd' in pool:
                liquidity = float(pool['liquidity_usd'])
            elif 'tvl' in pool:
                liquidity = float(pool['tvl'])
            
            # Try different possible keys for volume
            volume_24h = 0
            if 'volume_24h' in pool:
                volume_24h = float(pool['volume_24h'])
            elif 'volume24h' in pool:
                volume_24h = float(pool['volume24h'])
            elif 'volume' in pool:
                volume_24h = float(pool['volume'])
            
            # Try different possible keys for APY
            apy = 0
            if 'apy' in pool:
                apy = float(pool['apy'])
            elif 'yield' in pool:
                apy = float(pool['yield'])
            
            # Calculate opportunity score
            score = 0
            
            # Liquidity score (0-25 points)
            if liquidity > 100000:  # > $100k liquidity
                score += 25
            elif liquidity > 50000:  # > $50k liquidity
                score += 20
            elif liquidity > 10000:  # > $10k liquidity
                score += 15
            
            # Volume score (0-25 points)
            if volume_24h > 10000:  # > $10k daily volume
                score += 25
            elif volume_24h > 5000:  # > $5k daily volume
                score += 20
            elif volume_24h > 1000:  # > $1k daily volume
                score += 15
            
            # APY score (0-50 points)
            if apy > 20:  # > 20% APY
                score += 50
            elif apy > 10:  # > 10% APY
                score += 40
            elif apy > 5:   # > 5% APY
                score += 30
            
            # Only return if score is high enough and we have valid data
            if score >= 30 and asset1_name != 'Unknown' and asset2_name != 'Unknown':
                return {
                    'source': 'tinyman',
                    'pool_name': f"{asset1_name}-{asset2_name}",
                    'liquidity': liquidity,
                    'volume_24h': volume_24h,
                    'apy': apy,
                    'opportunity_score': score,
                    'opportunity_type': 'liquidity_provision',
                    'timestamp': datetime.now().isoformat(),
                    'metadata': pool
                }
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing Tinyman pool: {e}")
        
        return None
    
    async def scan_algo_explorer_assets(self) -> List[Dict[str, Any]]:
        """Scan AlgoExplorer for asset opportunities"""
        opportunities = []
        
        try:
            self.logger.info("🔍 Scanning AlgoExplorer for asset opportunities...")
            
            # Get top assets by market cap
            assets_url = f"{self.data_sources['algo_explorer']['base_url']}/assets"
            params = {
                'limit': 100,
                'sort': 'market_cap'
            }
            
            response = requests.get(assets_url, params=params, timeout=15)
            
            if response.status_code == 200:
                try:
                    assets_data = response.json()
                    
                    if isinstance(assets_data, list):
                        assets = assets_data
                    elif isinstance(assets_data, dict) and 'data' in assets_data:
                        assets = assets_data['data']
                    else:
                        assets = []
                    
                    self.logger.info(f"✅ Found {len(assets)} assets on AlgoExplorer")
                    
                    for asset in assets:
                        if isinstance(asset, dict):
                            opportunity = self._analyze_algo_explorer_asset(asset)
                            if opportunity:
                                opportunities.append(opportunity)
                
                except json.JSONDecodeError as e:
                    self.logger.error(f"❌ JSON decode error: {e}")
                except Exception as e:
                    self.logger.error(f"❌ Error parsing AlgoExplorer response: {e}")
            
            else:
                self.logger.warning(f"⚠️ AlgoExplorer API failed: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"❌ Error scanning AlgoExplorer: {e}")
        
        return opportunities
    
    def _analyze_algo_explorer_asset(self, asset: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze an AlgoExplorer asset for opportunities"""
        try:
            # Extract asset information safely
            name = asset.get('name', asset.get('asset_name', 'Unknown'))
            symbol = asset.get('symbol', asset.get('asset_symbol', 'Unknown'))
            
            # Try different possible keys for market cap
            market_cap = 0
            if 'market_cap' in asset:
                market_cap = float(asset['market_cap'])
            elif 'marketCap' in asset:
                market_cap = float(asset['marketCap'])
            
            # Try different possible keys for price
            price = 0
            if 'price' in asset:
                price = float(asset['price'])
            elif 'current_price' in asset:
                price = float(asset['current_price'])
            
            # Try different possible keys for volume
            volume_24h = 0
            if 'volume_24h' in asset:
                volume_24h = float(asset['volume_24h'])
            elif 'volume24h' in asset:
                volume_24h = float(asset['volume24h'])
            
            # Calculate opportunity score
            score = 0
            
            # Market cap score (0-30 points)
            if market_cap > 1000000:  # > $1M market cap
                score += 30
            elif market_cap > 100000:  # > $100k market cap
                score += 25
            elif market_cap > 10000:   # > $10k market cap
                score += 20
            
            # Volume score (0-40 points)
            if volume_24h > 10000:  # > $10k daily volume
                score += 40
            elif volume_24h > 5000:  # > $5k daily volume
                score += 30
            elif volume_24h > 1000:  # > $1k daily volume
                score += 20
            
            # Price stability score (0-30 points)
            if price > 0.01:  # Price > $0.01
                score += 30
            elif price > 0.001:  # Price > $0.001
                score += 20
            
            # Only return if score is high enough and we have valid data
            if score >= 40 and name != 'Unknown' and symbol != 'Unknown':
                return {
                    'source': 'algo_explorer',
                    'asset_name': name,
                    'symbol': symbol,
                    'market_cap': market_cap,
                    'price': price,
                    'volume_24h': volume_24h,
                    'opportunity_score': score,
                    'opportunity_type': 'asset_trading',
                    'timestamp': datetime.now().isoformat(),
                    'metadata': asset
                }
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing AlgoExplorer asset: {e}")
        
        return None
    
    async def scan_manual_opportunities(self) -> List[Dict[str, Any]]:
        """Scan for manually identified opportunities"""
        opportunities = []
        
        try:
            self.logger.info("🔍 Scanning for manually identified opportunities...")
            
            # Manual opportunities based on known Algorand ecosystem
            manual_opps = [
                {
                    'source': 'manual_analysis',
                    'protocol_name': 'Tinyman V2',
                    'opportunity_type': 'dex_trading',
                    'description': 'Major DEX with high liquidity pools',
                    'opportunity_score': 85,
                    'risk_level': 'low',
                    'estimated_apy': 15.0,
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'source': 'manual_analysis',
                    'protocol_name': 'Pact Finance',
                    'opportunity_type': 'yield_farming',
                    'description': 'Yield farming with stable returns',
                    'opportunity_score': 75,
                    'risk_level': 'medium',
                    'estimated_apy': 12.0,
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'source': 'manual_analysis',
                    'protocol_name': 'Folks Finance',
                    'opportunity_type': 'lending',
                    'description': 'Lending protocol with competitive rates',
                    'opportunity_score': 70,
                    'risk_level': 'medium',
                    'estimated_apy': 8.0,
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'source': 'manual_analysis',
                    'protocol_name': 'AlgoFi',
                    'opportunity_type': 'defi_protocol',
                    'description': 'Comprehensive DeFi protocol',
                    'opportunity_score': 80,
                    'risk_level': 'low',
                    'estimated_apy': 10.0,
                    'timestamp': datetime.now().isoformat()
                }
            ]
            
            opportunities.extend(manual_opps)
            self.logger.info(f"✅ Found {len(manual_opps)} manual opportunities")
            
        except Exception as e:
            self.logger.error(f"❌ Error scanning manual opportunities: {e}")
        
        return opportunities
    
    async def scan_all_opportunities(self) -> List[Dict[str, Any]]:
        """Scan all working sources for opportunities"""
        try:
            self.logger.info("🚀 Starting working opportunity scan...")
            
            # Scan all working sources concurrently
            tasks = [
                self.scan_tinyman_working(),
                self.scan_algo_explorer_assets(),
                self.scan_manual_opportunities()
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            all_opportunities = []
            
            for result in results:
                if isinstance(result, list):
                    all_opportunities.extend(result)
                else:
                    self.logger.error(f"Scan failed: {result}")
            
            # Sort by opportunity score
            all_opportunities.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
            
            # Store opportunities
            self.opportunities = all_opportunities
            self.last_scan = datetime.now()
            self.total_scans += 1
            self.total_opportunities_found += len(all_opportunities)
            
            self.logger.info(f"✅ Scan complete: {len(all_opportunities)} opportunities found")
            
            # Save opportunities to file
            self._save_opportunities()
            
            return all_opportunities
            
        except Exception as e:
            self.logger.error(f"❌ Error in working scan: {e}")
            return []
    
    def _save_opportunities(self):
        """Save opportunities to file"""
        try:
            os.makedirs('data', exist_ok=True)
            
            opportunities_file = f'data/working_opportunities_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            with open(opportunities_file, 'w') as f:
                json.dump({
                    'scan_timestamp': datetime.now().isoformat(),
                    'total_opportunities': len(self.opportunities),
                    'opportunities': self.opportunities
                }, f, indent=2)
            
            self.logger.info(f"📁 Opportunities saved to {opportunities_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving opportunities: {e}")
    
    def get_top_opportunities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top opportunities by score"""
        if not self.opportunities:
            return []
        
        return self.opportunities[:limit]
    
    def get_opportunities_by_type(self, opportunity_type: str) -> List[Dict[str, Any]]:
        """Get opportunities by type"""
        return [op for op in self.opportunities if op.get('opportunity_type') == opportunity_type]
    
    def get_opportunities_by_source(self, source: str) -> List[Dict[str, Any]]:
        """Get opportunities by source"""
        return [op for op in self.opportunities if op.get('source') == source]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get scanner system status"""
        return {
            'name': self.name,
            'version': self.version,
            'status': 'running',
            'uptime': str(datetime.now() - self.start_time),
            'total_scans': self.total_scans,
            'total_opportunities_found': self.total_opportunities_found,
            'current_opportunities': len(self.opportunities),
            'last_scan': self.last_scan.isoformat() if self.last_scan else None,
            'data_sources': {name: {'enabled': info['enabled']} for name, info in self.data_sources.items()}
        }

async def main():
    """Test the working opportunity scanner"""
    scanner = WorkingOpportunityScanner()
    
    try:
        # Run working scan
        opportunities = await scanner.scan_all_opportunities()
        
        print(f"\n🎯 Scan Results:")
        print(f"Total opportunities found: {len(opportunities)}")
        
        # Show top opportunities
        top_opps = scanner.get_top_opportunities(10)
        print(f"\n🏆 Top Opportunities:")
        
        for i, opp in enumerate(top_opps, 1):
            print(f"{i}. {opp.get('source', 'Unknown')} - {opp.get('opportunity_type', 'Unknown')}")
            print(f"   Score: {opp.get('opportunity_score', 0)}")
            
            # Show relevant details based on source
            if opp.get('source') == 'tinyman':
                print(f"   Pool: {opp.get('pool_name', 'Unknown')}")
                print(f"   Liquidity: ${opp.get('liquidity', 0):,.0f}")
                print(f"   Volume 24h: ${opp.get('volume_24h', 0):,.0f}")
                print(f"   APY: {opp.get('apy', 0):.1f}%")
            elif opp.get('source') == 'algo_explorer':
                print(f"   Asset: {opp.get('asset_name', 'Unknown')} ({opp.get('symbol', 'Unknown')})")
                print(f"   Market Cap: ${opp.get('market_cap', 0):,.0f}")
                print(f"   Price: ${opp.get('price', 0):.6f}")
                print(f"   Volume 24h: ${opp.get('volume_24h', 0):,.0f}")
            elif opp.get('source') == 'manual_analysis':
                print(f"   Protocol: {opp.get('protocol_name', 'Unknown')}")
                print(f"   Description: {opp.get('description', 'Unknown')}")
                print(f"   Risk Level: {opp.get('risk_level', 'Unknown')}")
                print(f"   Estimated APY: {opp.get('estimated_apy', 0):.1f}%")
            
            print()
        
        # Show system status
        status = scanner.get_system_status()
        print(f"📊 System Status: {status}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
