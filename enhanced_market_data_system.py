#!/usr/bin/env python3
"""
ENHANCED MARKET DATA INTEGRATION SYSTEM
Phase 1 Implementation - Trading Firm Upgrade
Budget: $400 (Risk Management + Market Data Integration)
"""

import json
import os
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd

class EnhancedMarketDataSystem:
    def __init__(self):
        print("📈 ENHANCED MARKET DATA INTEGRATION SYSTEM - INITIALIZING...")
        print("🎯 Phase 1: Foundation & Market Data Integration")
        print("💰 Budget Allocated: $400 (shared with Risk Management)")
        
        # Market data feeds
        self.data_feeds = {
            'equity': {},
            'options': {},
            'futures': {},
            'forex': {},
            'crypto': {},
            'commodities': {}
        }
        
        # Real-time data streams
        self.real_time_streams = {}
        self.market_indicators = {}
        self.volatility_metrics = {}
        self.correlation_matrix = {}
        
        # Data storage
        self.historical_data = {}
        self.market_sentiment = {}
        self.technical_indicators = {}
        
        # Initialize data feeds
        self.initialize_data_feeds()
        
        print("✅ Market Data System initialized")
        print("🔗 Data feeds: CONFIGURED")
        print("📊 Real-time streaming: READY")
    
    def initialize_data_feeds(self):
        """Initialize market data feeds"""
        print("🔧 Initializing market data feeds...")
        
        # Equity data feeds
        self.data_feeds['equity'] = {
            'primary': {
                'name': 'Enhanced IBKR Feed',
                'status': 'active',
                'symbols': ['SPY', 'QQQ', 'IWM', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
                'update_frequency': '1s',
                'data_types': ['price', 'volume', 'bid', 'ask', 'last']
            },
            'secondary': {
                'name': 'Alternative Data Feed',
                'status': 'backup',
                'symbols': ['SPY', 'QQQ', 'AAPL', 'MSFT'],
                'update_frequency': '5s',
                'data_types': ['price', 'volume']
            }
        }
        
        # Options data feeds
        self.data_feeds['options'] = {
            'primary': {
                'name': 'Options Chain Feed',
                'status': 'active',
                'symbols': ['SPY', 'QQQ', 'AAPL'],
                'update_frequency': '5s',
                'data_types': ['strike', 'expiry', 'bid', 'ask', 'volume', 'open_interest']
            }
        }
        
        # Market indicators
        self.market_indicators = {
            'vix': {'value': 25.5, 'change': 0.0, 'status': 'active'},
            'put_call_ratio': {'value': 0.85, 'change': 0.0, 'status': 'active'},
            'advance_decline': {'value': 1.2, 'change': 0.0, 'status': 'active'},
            'new_highs_lows': {'value': 0.65, 'change': 0.0, 'status': 'active'}
        }
        
        print("✅ Market data feeds configured")
    
    async def run_market_data_system(self):
        """Run the complete market data system"""
        print("🚀 STARTING ENHANCED MARKET DATA SYSTEM...")
        print("=" * 60)
        
        # Start multiple data collection tasks
        tasks = [
            self.collect_equity_data(),
            self.collect_market_indicators(),
            self.calculate_volatility_metrics(),
            self.update_correlation_matrix(),
            self.stream_real_time_data(),
            self.analyze_market_sentiment()
        ]
        
        try:
            # Run all tasks concurrently
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"❌ Market data system error: {e}")
    
    async def collect_equity_data(self):
        """Collect real-time equity data"""
        print("📊 Starting equity data collection...")
        
        while True:
            try:
                current_time = datetime.now()
                
                # Collect data for each symbol
                for symbol in self.data_feeds['equity']['primary']['symbols']:
                    equity_data = await self.get_equity_data(symbol)
                    
                    if equity_data:
                        self.data_feeds['equity'][symbol] = equity_data
                        
                        # Store historical data
                        if symbol not in self.historical_data:
                            self.historical_data[symbol] = []
                        
                        self.historical_data[symbol].append({
                            'timestamp': current_time.isoformat(),
                            'price': equity_data['price'],
                            'volume': equity_data['volume'],
                            'bid': equity_data['bid'],
                            'ask': equity_data['ask']
                        })
                        
                        # Keep last 1000 data points
                        if len(self.historical_data[symbol]) > 1000:
                            self.historical_data[symbol] = self.historical_data[symbol][-1000:]
                
                # Wait 1 second between updates
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Equity data collection error: {e}")
                await asyncio.sleep(5)
    
    async def get_equity_data(self, symbol: str) -> Optional[Dict]:
        """Get equity data for a symbol (simulated for now)"""
        try:
            # Simulate real-time data
            base_price = {
                'SPY': 420.50, 'QQQ': 380.25, 'IWM': 190.75,
                'AAPL': 175.80, 'MSFT': 360.40, 'GOOGL': 140.20,
                'AMZN': 180.90, 'TSLA': 250.30
            }
            
            if symbol in base_price:
                # Add some realistic price movement
                import random
                price_change = random.uniform(-0.5, 0.5)
                current_price = base_price[symbol] + price_change
                
                return {
                    'symbol': symbol,
                    'price': round(current_price, 2),
                    'volume': random.randint(1000, 10000),
                    'bid': round(current_price - 0.01, 2),
                    'ask': round(current_price + 0.01, 2),
                    'last': round(current_price, 2),
                    'timestamp': datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting equity data for {symbol}: {e}")
            return None
    
    async def collect_market_indicators(self):
        """Collect market-wide indicators"""
        print("📈 Starting market indicators collection...")
        
        while True:
            try:
                current_time = datetime.now()
                
                # Update VIX (simulated)
                import random
                vix_change = random.uniform(-1.0, 1.0)
                self.market_indicators['vix']['value'] = max(10, self.market_indicators['vix']['value'] + vix_change)
                self.market_indicators['vix']['change'] = vix_change
                
                # Update put-call ratio
                pcr_change = random.uniform(-0.05, 0.05)
                self.market_indicators['put_call_ratio']['value'] = max(0.1, min(2.0, 
                    self.market_indicators['put_call_ratio']['value'] + pcr_change))
                self.market_indicators['put_call_ratio']['change'] = pcr_change
                
                # Update advance-decline ratio
                ad_change = random.uniform(-0.1, 0.1)
                self.market_indicators['advance_decline']['value'] = max(0.1, 
                    self.market_indicators['advance_decline']['value'] + ad_change)
                self.market_indicators['advance_decline']['change'] = ad_change
                
                # Update new highs/lows ratio
                nh_change = random.uniform(-0.05, 0.05)
                self.market_indicators['new_highs_lows']['value'] = max(0.1, min(1.0,
                    self.market_indicators['new_highs_lows']['value'] + nh_change))
                self.market_indicators['new_highs_lows']['change'] = nh_change
                
                # Wait 5 seconds between updates
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"❌ Market indicators error: {e}")
                await asyncio.sleep(10)
    
    async def calculate_volatility_metrics(self):
        """Calculate real-time volatility metrics"""
        print("📊 Starting volatility calculations...")
        
        while True:
            try:
                current_time = datetime.now()
                
                # Calculate volatility for each symbol
                for symbol in self.data_feeds['equity']['primary']['symbols']:
                    if symbol in self.historical_data and len(self.historical_data[symbol]) > 20:
                        prices = [data['price'] for data in self.historical_data[symbol][-20:]]
                        
                        if len(prices) > 1:
                            # Calculate rolling volatility
                            returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
                            volatility = (sum(r**2 for r in returns) / len(returns))**0.5 * (252**0.5)  # Annualized
                            
                            self.volatility_metrics[symbol] = {
                                'symbol': symbol,
                                'volatility': round(volatility * 100, 2),  # Percentage
                                'timestamp': current_time.isoformat(),
                                'data_points': len(prices)
                            }
                
                # Wait 10 seconds between calculations
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ Volatility calculation error: {e}")
                await asyncio.sleep(15)
    
    async def update_correlation_matrix(self):
        """Update correlation matrix between assets"""
        print("🔗 Updating correlation matrix...")
        
        while True:
            try:
                current_time = datetime.now()
                
                # Get symbols with sufficient data
                symbols_with_data = [s for s in self.data_feeds['equity']['primary']['symbols'] 
                                   if s in self.historical_data and len(self.historical_data[s]) > 50]
                
                if len(symbols_with_data) > 1:
                    # Calculate correlations
                    correlations = {}
                    
                    for i, symbol1 in enumerate(symbols_with_data):
                        for j, symbol2 in enumerate(symbols_with_data):
                            if i < j:  # Only calculate upper triangle
                                corr = self.calculate_correlation(symbol1, symbol2)
                                if corr is not None:
                                    correlations[f"{symbol1}_{symbol2}"] = {
                                        'symbol1': symbol1,
                                        'symbol2': symbol2,
                                        'correlation': round(corr, 3),
                                        'timestamp': current_time.isoformat()
                                    }
                    
                    self.correlation_matrix = correlations
                
                # Wait 30 seconds between updates
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"❌ Correlation matrix error: {e}")
                await asyncio.sleep(45)
    
    def calculate_correlation(self, symbol1: str, symbol2: str) -> Optional[float]:
        """Calculate correlation between two symbols"""
        try:
            if symbol1 not in self.historical_data or symbol2 not in self.historical_data:
                return None
            
            # Get common time periods
            data1 = self.historical_data[symbol1][-50:]  # Last 50 data points
            data2 = self.historical_data[symbol2][-50:]
            
            if len(data1) < 20 or len(data2) < 20:
                return None
            
            # Calculate returns
            prices1 = [d['price'] for d in data1]
            prices2 = [d['price'] for d in data2]
            
            returns1 = [(prices1[i] - prices1[i-1]) / prices1[i-1] for i in range(1, len(prices1))]
            returns2 = [(prices2[i] - prices2[i-1]) / prices2[i-1] for i in range(1, len(prices2))]
            
            # Ensure same length
            min_len = min(len(returns1), len(returns2))
            returns1 = returns1[:min_len]
            returns2 = returns2[:min_len]
            
            if min_len < 10:
                return None
            
            # Calculate correlation
            mean1 = sum(returns1) / len(returns1)
            mean2 = sum(returns2) / len(returns2)
            
            numerator = sum((r1 - mean1) * (r2 - mean2) for r1, r2 in zip(returns1, returns2))
            denominator1 = sum((r1 - mean1) ** 2 for r1 in returns1)
            denominator2 = sum((r2 - mean2) ** 2 for r2 in returns2)
            
            if denominator1 == 0 or denominator2 == 0:
                return None
            
            correlation = numerator / (denominator1 ** 0.5 * denominator2 ** 0.5)
            return correlation
            
        except Exception as e:
            print(f"❌ Correlation calculation error for {symbol1}-{symbol2}: {e}")
            return None
    
    async def stream_real_time_data(self):
        """Stream real-time market data"""
        print("🌊 Starting real-time data streaming...")
        
        while True:
            try:
                current_time = datetime.now()
                
                # Create real-time data snapshot
                real_time_snapshot = {
                    'timestamp': current_time.isoformat(),
                    'equity_data': {},
                    'market_indicators': self.market_indicators,
                    'volatility_metrics': self.volatility_metrics,
                    'correlation_summary': self.get_correlation_summary()
                }
                
                # Add equity data
                for symbol in self.data_feeds['equity']['primary']['symbols']:
                    if symbol in self.data_feeds['equity']:
                        real_time_snapshot['equity_data'][symbol] = self.data_feeds['equity'][symbol]
                
                # Store snapshot
                self.real_time_streams[current_time.isoformat()] = real_time_snapshot
                
                # Keep only last 100 snapshots
                if len(self.real_time_streams) > 100:
                    oldest_key = min(self.real_time_streams.keys())
                    del self.real_time_streams[oldest_key]
                
                # Save current snapshot
                self.save_market_data_snapshot(real_time_snapshot)
                
                # Wait 1 second between snapshots
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Real-time streaming error: {e}")
                await asyncio.sleep(5)
    
    def get_correlation_summary(self) -> Dict:
        """Get summary of correlation matrix"""
        if not self.correlation_matrix:
            return {'total_pairs': 0, 'high_correlation_pairs': 0}
        
        high_corr_pairs = [k for k, v in self.correlation_matrix.items() if abs(v['correlation']) > 0.7]
        
        return {
            'total_pairs': len(self.correlation_matrix),
            'high_correlation_pairs': len(high_corr_pairs),
            'average_correlation': sum(abs(v['correlation']) for v in self.correlation_matrix.values()) / len(self.correlation_matrix)
        }
    
    async def analyze_market_sentiment(self):
        """Analyze overall market sentiment"""
        print("🧠 Starting market sentiment analysis...")
        
        while True:
            try:
                current_time = datetime.now()
                
                # Calculate sentiment score based on multiple factors
                sentiment_factors = []
                
                # VIX factor (lower VIX = higher sentiment)
                vix = self.market_indicators['vix']['value']
                vix_sentiment = max(0, (50 - vix) / 50)  # 0-1 scale
                sentiment_factors.append(vix_sentiment)
                
                # Put-call ratio factor (lower PCR = higher sentiment)
                pcr = self.market_indicators['put_call_ratio']['value']
                pcr_sentiment = max(0, (2.0 - pcr) / 2.0)  # 0-1 scale
                sentiment_factors.append(pcr_sentiment)
                
                # Advance-decline factor
                ad = self.market_indicators['advance_decline']['value']
                ad_sentiment = min(1.0, ad / 2.0)  # 0-1 scale
                sentiment_factors.append(ad_sentiment)
                
                # New highs/lows factor
                nh = self.market_indicators['new_highs_lows']['value']
                nh_sentiment = nh  # Already 0-1 scale
                sentiment_factors.append(nh_sentiment)
                
                # Calculate overall sentiment
                if sentiment_factors:
                    overall_sentiment = sum(sentiment_factors) / len(sentiment_factors)
                    
                    self.market_sentiment = {
                        'timestamp': current_time.isoformat(),
                        'overall_sentiment': round(overall_sentiment, 3),
                        'sentiment_level': self.get_sentiment_level(overall_sentiment),
                        'factors': {
                            'vix_sentiment': round(vix_sentiment, 3),
                            'pcr_sentiment': round(pcr_sentiment, 3),
                            'ad_sentiment': round(ad_sentiment, 3),
                            'nh_sentiment': round(nh_sentiment, 3)
                        },
                        'recommendations': self.get_sentiment_recommendations(overall_sentiment)
                    }
                
                # Wait 15 seconds between analyses
                await asyncio.sleep(15)
                
            except Exception as e:
                print(f"❌ Market sentiment error: {e}")
                await asyncio.sleep(20)
    
    def get_sentiment_level(self, sentiment_score: float) -> str:
        """Get sentiment level description"""
        if sentiment_score >= 0.7:
            return 'Very Bullish'
        elif sentiment_score >= 0.5:
            return 'Bullish'
        elif sentiment_score >= 0.3:
            return 'Neutral'
        elif sentiment_score >= 0.1:
            return 'Bearish'
        else:
            return 'Very Bearish'
    
    def get_sentiment_recommendations(self, sentiment_score: float) -> List[str]:
        """Get trading recommendations based on sentiment"""
        recommendations = []
        
        if sentiment_score >= 0.7:
            recommendations.extend([
                'Consider taking profits on long positions',
                'Look for short-term pullback opportunities',
                'Maintain stop losses on existing positions'
            ])
        elif sentiment_score >= 0.5:
            recommendations.extend([
                'Continue with current strategy',
                'Look for new long opportunities',
                'Monitor for sentiment shifts'
            ])
        elif sentiment_score >= 0.3:
            recommendations.extend([
                'Be cautious with new positions',
                'Consider defensive positioning',
                'Wait for clearer market direction'
            ])
        else:
            recommendations.extend([
                'Consider defensive strategies',
                'Look for oversold conditions',
                'Prepare for potential bounce opportunities'
            ])
        
        return recommendations
    
    def save_market_data_snapshot(self, snapshot: Dict):
        """Save market data snapshot"""
        filename = f"market_data_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        # Also save to current file
        with open('current_market_data.json', 'w') as f:
            json.dump(snapshot, f, indent=2)
    
    def get_market_data_summary(self) -> Dict:
        """Get summary of current market data"""
        return {
            'timestamp': datetime.now().isoformat(),
            'active_symbols': len(self.data_feeds['equity']['primary']['symbols']),
            'data_feeds_status': {k: v['status'] for k, v in self.data_feeds['equity'].items()},
            'market_indicators': self.market_indicators,
            'volatility_summary': len(self.volatility_metrics),
            'correlation_summary': self.get_correlation_summary(),
            'market_sentiment': self.market_sentiment
        }

async def main():
    """Run enhanced market data system"""
    print("📈 ENHANCED MARKET DATA INTEGRATION SYSTEM")
    print("=" * 60)
    print("🎯 Phase 1 Implementation: Foundation & Market Data Integration")
    print("💰 Budget: $400 (shared with Risk Management)")
    print("⏱️ Timeline: Months 1-2")
    print("=" * 60)
    
    market_data_system = EnhancedMarketDataSystem()
    
    try:
        # Start market data system
        await market_data_system.run_market_data_system()
    except KeyboardInterrupt:
        print("\n🛑 Market data system stopped by user")
    except Exception as e:
        print(f"❌ Market data system error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
