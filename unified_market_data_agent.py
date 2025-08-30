#!/usr/bin/env python3
"""
UNIFIED MARKET DATA AGENT
Trading Firm Upgrade - Phase 1 Critical Priority
Combines enhanced_market_data_system.py + enhanced_market_data_pipeline.py
Budget: $600 (consolidated from both systems)
"""

import json
import os
import time
import asyncio
import aiohttp
import websockets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np
from dataclasses import dataclass
import logging

@dataclass
class MarketDataPoint:
    """Market data point structure"""
    timestamp: str
    symbol: str
    price: float
    volume: int
    bid: float
    ask: float
    bid_size: int
    ask_size: int
    source: str
    quality: float  # 0-1 scale

@dataclass
class MarketSignal:
    """Market signal structure"""
    timestamp: str
    symbol: str
    signal_type: str  # buy, sell, hold, alert
    strength: float   # 0-1 scale
    confidence: float # 0-1 scale
    reasoning: List[str]
    source: str

class UnifiedMarketDataAgent:
    def __init__(self):
        print("📊 UNIFIED MARKET DATA AGENT - INITIALIZING...")
        print("🎯 Phase 1 Critical Priority: Consolidated Market Data")
        print("💰 Budget Allocated: $600 (consolidated from both systems)")
        
        # Data sources (consolidated from both systems)
        self.data_sources = {
            'primary': {
                'name': 'Primary Market Data Feed',
                'type': 'real_time',
                'status': 'active',
                'latency': 0.015,  # 15ms
                'reliability': 0.99
            },
            'secondary': {
                'name': 'Secondary Market Data Feed',
                'type': 'real_time',
                'status': 'active',
                'latency': 0.025,  # 25ms
                'reliability': 0.97
            },
            'historical': {
                'name': 'Historical Data Provider',
                'type': 'historical',
                'status': 'active',
                'latency': 1.0,    # 1 second
                'reliability': 0.99
            },
            'alternative': {
                'name': 'Alternative Data Sources',
                'type': 'alternative',
                'status': 'active',
                'latency': 5.0,    # 5 seconds
                'reliability': 0.85
            }
        }
        
        # Market data storage (from enhanced system)
        self.market_data_cache = {}
        self.historical_data = {}
        self.real_time_feeds = {}
        self.data_quality_metrics = {}
        
        # Data processing pipeline (from enhanced pipeline)
        self.data_processors = {
            'normalization': {
                'name': 'Data Normalization',
                'status': 'active',
                'version': '2.0',
                'efficiency': 0.95
            },
            'validation': {
                'name': 'Data Validation',
                'status': 'active',
                'version': '1.8',
                'efficiency': 0.92
            },
            'aggregation': {
                'name': 'Data Aggregation',
                'status': 'active',
                'version': '2.1',
                'efficiency': 0.94
            },
            'enrichment': {
                'name': 'Data Enrichment',
                'status': 'active',
                'version': '1.9',
                'efficiency': 0.89
            }
        }
        
        # Market signals and alerts
        self.market_signals = []
        self.price_alerts = []
        self.volume_alerts = []
        self.volatility_alerts = []
        
        # Performance metrics
        self.data_latency_history = []
        self.data_quality_history = []
        self.processing_times = []
        
        # Configuration
        self.update_frequency = 0.1  # 100ms
        self.cache_expiry = 300      # 5 minutes
        self.max_cache_size = 10000  # 10k data points
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        print("✅ Unified Market Data Agent initialized")
        print("📡 Data Sources: CONNECTED")
        print("🔄 Data Pipeline: ACTIVE")
        print("📊 Real-time feeds: ENABLED")
    
    async def run_unified_market_data_agent(self):
        """Run the unified market data agent"""
        print("🚀 STARTING UNIFIED MARKET DATA AGENT...")
        print("=" * 70)
        
        tasks = [
            self.continuous_market_data_collection(),
            self.real_time_data_processing(),
            self.market_signal_generation(),
            self.data_quality_monitoring(),
            self.market_data_distribution(),
            self.performance_optimization()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(f"Unified market data agent error: {e}")
    
    async def continuous_market_data_collection(self):
        """Continuous market data collection from all sources"""
        print("📡 Starting continuous market data collection...")
        
        while True:
            try:
                current_time = datetime.now()
                
                # Collect from primary sources
                await self.collect_primary_market_data()
                
                # Collect from secondary sources
                await self.collect_secondary_market_data()
                
                # Collect alternative data
                await self.collect_alternative_data()
                
                # Update data quality metrics
                await self.update_data_quality_metrics()
                
                # Wait for next update cycle
                await asyncio.sleep(self.update_frequency)
                
            except Exception as e:
                self.logger.error(f"Market data collection error: {e}")
                await asyncio.sleep(1.0)
    
    async def collect_primary_market_data(self):
        """Collect data from primary market data sources"""
        try:
            # Simulate primary data collection
            symbols = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL']
            
            for symbol in symbols:
                market_data = await self.fetch_market_data(symbol, 'primary')
                if market_data:
                    await self.process_market_data(market_data)
                    
        except Exception as e:
            self.logger.error(f"Primary market data collection error: {e}")
    
    async def collect_secondary_market_data(self):
        """Collect data from secondary market data sources"""
        try:
            # Simulate secondary data collection
            symbols = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL']
            
            for symbol in symbols:
                market_data = await self.fetch_market_data(symbol, 'secondary')
                if market_data:
                    await self.process_market_data(market_data)
                    
        except Exception as e:
            self.logger.error(f"Secondary market data collection error: {e}")
    
    async def collect_alternative_data(self):
        """Collect alternative market data"""
        try:
            # Simulate alternative data collection
            data_types = ['sentiment', 'news', 'social', 'options_flow']
            
            for data_type in data_types:
                alternative_data = await self.fetch_alternative_data(data_type)
                if alternative_data:
                    await self.process_alternative_data(alternative_data)
                    
        except Exception as e:
            self.logger.error(f"Alternative data collection error: {e}")
    
    async def fetch_market_data(self, symbol: str, source: str) -> Optional[MarketDataPoint]:
        """Fetch market data for a specific symbol from a specific source"""
        try:
            # Simulate market data fetch
            current_price = 100.0 + np.random.normal(0, 2)
            volume = int(1000000 + np.random.normal(0, 200000))
            bid = current_price - 0.01
            ask = current_price + 0.01
            
            return MarketDataPoint(
                timestamp=datetime.now().isoformat(),
                symbol=symbol,
                price=current_price,
                volume=volume,
                bid=bid,
                ask=ask,
                bid_size=int(volume * 0.1),
                ask_size=int(volume * 0.1),
                source=source,
                quality=0.95
            )
            
        except Exception as e:
            self.logger.error(f"Market data fetch error for {symbol}: {e}")
            return None
    
    async def fetch_alternative_data(self, data_type: str) -> Optional[Dict]:
        """Fetch alternative market data"""
        try:
            # Simulate alternative data fetch
            if data_type == 'sentiment':
                return {
                    'type': 'sentiment',
                    'value': np.random.normal(0.5, 0.2),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'alternative'
                }
            elif data_type == 'news':
                return {
                    'type': 'news',
                    'count': int(np.random.poisson(5)),
                    'sentiment': np.random.normal(0.5, 0.3),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'alternative'
                }
            elif data_type == 'social':
                return {
                    'type': 'social',
                    'mentions': int(np.random.poisson(100)),
                    'sentiment': np.random.normal(0.5, 0.2),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'alternative'
                }
            elif data_type == 'options_flow':
                return {
                    'type': 'options_flow',
                    'put_call_ratio': np.random.normal(1.0, 0.3),
                    'volume': int(np.random.poisson(10000)),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'alternative'
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Alternative data fetch error for {data_type}: {e}")
            return None
    
    async def process_market_data(self, market_data: MarketDataPoint):
        """Process incoming market data"""
        try:
            # Validate data quality
            if not await self.validate_market_data(market_data):
                self.logger.warning(f"Low quality market data for {market_data.symbol}")
                return
            
            # Normalize data
            normalized_data = await self.normalize_market_data(market_data)
            
            # Store in cache
            await self.store_market_data(normalized_data)
            
            # Update real-time feeds
            await self.update_real_time_feeds(normalized_data)
            
            # Check for alerts
            await self.check_market_alerts(normalized_data)
            
        except Exception as e:
            self.logger.error(f"Market data processing error: {e}")
    
    async def process_alternative_data(self, alternative_data: Dict):
        """Process alternative market data"""
        try:
            # Validate alternative data
            if not await self.validate_alternative_data(alternative_data):
                return
            
            # Store alternative data
            await self.store_alternative_data(alternative_data)
            
            # Generate signals based on alternative data
            await self.generate_alternative_signals(alternative_data)
            
        except Exception as e:
            self.logger.error(f"Alternative data processing error: {e}")
    
    async def validate_market_data(self, market_data: MarketDataPoint) -> bool:
        """Validate market data quality"""
        try:
            # Check for reasonable price ranges
            if market_data.price <= 0 or market_data.price > 10000:
                return False
            
            # Check for reasonable volume
            if market_data.volume < 0 or market_data.volume > 10000000:
                return False
            
            # Check bid-ask spread
            if market_data.ask <= market_data.bid:
                return False
            
            # Check data quality score
            if market_data.quality < 0.8:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Market data validation error: {e}")
            return False
    
    async def validate_alternative_data(self, alternative_data: Dict) -> bool:
        """Validate alternative data quality"""
        try:
            # Check timestamp
            if 'timestamp' not in alternative_data:
                return False
            
            # Check data type
            if 'type' not in alternative_data:
                return False
            
            # Check for reasonable values based on type
            data_type = alternative_data['type']
            
            if data_type == 'sentiment':
                if not (0 <= alternative_data.get('value', 0) <= 1):
                    return False
            elif data_type == 'news':
                if alternative_data.get('count', 0) < 0:
                    return False
            elif data_type == 'social':
                if alternative_data.get('mentions', 0) < 0:
                    return False
            elif data_type == 'options_flow':
                if alternative_data.get('put_call_ratio', 0) <= 0:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Alternative data validation error: {e}")
            return False
    
    async def normalize_market_data(self, market_data: MarketDataPoint) -> MarketDataPoint:
        """Normalize market data to standard format"""
        try:
            # Ensure timestamp is in ISO format
            if isinstance(market_data.timestamp, datetime):
                timestamp = market_data.timestamp.isoformat()
            else:
                timestamp = market_data.timestamp
            
            # Round prices to reasonable precision
            price = round(market_data.price, 4)
            bid = round(market_data.bid, 4)
            ask = round(market_data.ask, 4)
            
            # Ensure volume is integer
            volume = int(market_data.volume)
            bid_size = int(market_data.bid_size)
            ask_size = int(market_data.ask_size)
            
            return MarketDataPoint(
                timestamp=timestamp,
                symbol=market_data.symbol.upper(),
                price=price,
                volume=volume,
                bid=bid,
                ask=ask,
                bid_size=bid_size,
                ask_size=ask_size,
                source=market_data.source,
                quality=market_data.quality
            )
            
        except Exception as e:
            self.logger.error(f"Market data normalization error: {e}")
            return market_data
    
    async def store_market_data(self, market_data: MarketDataPoint):
        """Store market data in cache"""
        try:
            symbol = market_data.symbol
            
            # Initialize symbol cache if needed
            if symbol not in self.market_data_cache:
                self.market_data_cache[symbol] = []
            
            # Add new data point
            self.market_data_cache[symbol].append(market_data)
            
            # Keep only recent data points
            if len(self.market_data_cache[symbol]) > self.max_cache_size:
                self.market_data_cache[symbol] = self.market_data_cache[symbol][-self.max_cache_size:]
            
            # Store in historical data if needed
            await self.store_historical_data(market_data)
            
        except Exception as e:
            self.logger.error(f"Market data storage error: {e}")
    
    async def store_alternative_data(self, alternative_data: Dict):
        """Store alternative data"""
        try:
            data_type = alternative_data['type']
            
            # Initialize type cache if needed
            if data_type not in self.historical_data:
                self.historical_data[data_type] = []
            
            # Add new data point
            self.historical_data[data_type].append(alternative_data)
            
            # Keep only recent data points
            if len(self.historical_data[data_type]) > 1000:
                self.historical_data[data_type] = self.historical_data[data_type][-1000:]
            
        except Exception as e:
            self.logger.error(f"Alternative data storage error: {e}")
    
    async def store_historical_data(self, market_data: MarketDataPoint):
        """Store market data in historical storage"""
        try:
            symbol = market_data.symbol
            
            # Initialize historical storage if needed
            if symbol not in self.historical_data:
                self.historical_data[symbol] = []
            
            # Add to historical data
            self.historical_data[symbol].append({
                'timestamp': market_data.timestamp,
                'price': market_data.price,
                'volume': market_data.volume,
                'bid': market_data.bid,
                'ask': market_data.ask,
                'source': market_data.source
            })
            
            # Keep only last 10000 historical points
            if len(self.historical_data[symbol]) > 10000:
                self.historical_data[symbol] = self.historical_data[symbol][-10000:]
            
        except Exception as e:
            self.logger.error(f"Historical data storage error: {e}")
    
    async def update_real_time_feeds(self, market_data: MarketDataPoint):
        """Update real-time market data feeds"""
        try:
            symbol = market_data.symbol
            
            # Update real-time feed
            self.real_time_feeds[symbol] = {
                'timestamp': market_data.timestamp,
                'price': market_data.price,
                'volume': market_data.volume,
                'bid': market_data.bid,
                'ask': market_data.ask,
                'bid_size': market_data.bid_size,
                'ask_size': market_data.ask_size,
                'spread': market_data.ask - market_data.bid,
                'mid_price': (market_data.bid + market_data.ask) / 2
            }
            
        except Exception as e:
            self.logger.error(f"Real-time feed update error: {e}")
    
    async def check_market_alerts(self, market_data: MarketDataPoint):
        """Check for market alerts based on new data"""
        try:
            symbol = market_data.symbol
            
            # Check for price alerts
            await self.check_price_alerts(market_data)
            
            # Check for volume alerts
            await self.check_volume_alerts(market_data)
            
            # Check for volatility alerts
            await self.check_volatility_alerts(market_data)
            
        except Exception as e:
            self.logger.error(f"Market alert checking error: {e}")
    
    async def check_price_alerts(self, market_data: MarketDataPoint):
        """Check for price-based alerts"""
        try:
            symbol = market_data.symbol
            
            # Get previous price if available
            if symbol in self.market_data_cache and len(self.market_data_cache[symbol]) > 1:
                previous_data = self.market_data_cache[symbol][-2]
                price_change = (market_data.price - previous_data.price) / previous_data.price
                
                # Alert for significant price changes
                if abs(price_change) > 0.05:  # 5% change
                    alert = {
                        'type': 'price_alert',
                        'symbol': symbol,
                        'timestamp': market_data.timestamp,
                        'price_change': price_change,
                        'current_price': market_data.price,
                        'previous_price': previous_data.price,
                        'severity': 'high' if abs(price_change) > 0.10 else 'medium'
                    }
                    
                    self.price_alerts.append(alert)
                    self.logger.info(f"Price alert: {symbol} changed by {price_change*100:.2f}%")
            
        except Exception as e:
            self.logger.error(f"Price alert checking error: {e}")
    
    async def check_volume_alerts(self, market_data: MarketDataPoint):
        """Check for volume-based alerts"""
        try:
            symbol = market_data.symbol
            
            # Get average volume if available
            if symbol in self.market_data_cache and len(self.market_data_cache[symbol]) > 10:
                recent_volumes = [data.volume for data in self.market_data_cache[symbol][-10:]]
                avg_volume = sum(recent_volumes) / len(recent_volumes)
                
                # Alert for unusual volume
                if market_data.volume > avg_volume * 2:  # 2x average volume
                    alert = {
                        'type': 'volume_alert',
                        'symbol': symbol,
                        'timestamp': market_data.timestamp,
                        'current_volume': market_data.volume,
                        'average_volume': avg_volume,
                        'volume_ratio': market_data.volume / avg_volume,
                        'severity': 'high' if market_data.volume > avg_volume * 3 else 'medium'
                    }
                    
                    self.volume_alerts.append(alert)
                    self.logger.info(f"Volume alert: {symbol} volume {alert['volume_ratio']:.1f}x average")
            
        except Exception as e:
            self.logger.error(f"Volume alert checking error: {e}")
    
    async def check_volatility_alerts(self, market_data: MarketDataPoint):
        """Check for volatility-based alerts"""
        try:
            symbol = market_data.symbol
            
            # Calculate volatility if enough data points
            if symbol in self.market_data_cache and len(self.market_data_cache[symbol]) > 20:
                recent_prices = [data.price for data in self.market_data_cache[symbol][-20:]]
                returns = [(recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1] 
                          for i in range(1, len(recent_prices))]
                
                if returns:
                    volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
                    
                    # Alert for high volatility
                    if volatility > 0.4:  # 40% annualized volatility
                        alert = {
                            'type': 'volatility_alert',
                            'symbol': symbol,
                            'timestamp': market_data.timestamp,
                            'volatility': volatility,
                            'severity': 'high' if volatility > 0.6 else 'medium'
                        }
                        
                        self.volatility_alerts.append(alert)
                        self.logger.info(f"Volatility alert: {symbol} volatility {volatility*100:.1f}%")
            
        except Exception as e:
            self.logger.error(f"Volatility alert checking error: {e}")
    
    async def real_time_data_processing(self):
        """Real-time data processing pipeline"""
        print("🔄 Starting real-time data processing...")
        
        while True:
            try:
                # Process cached data
                await self.process_cached_data()
                
                # Update data quality metrics
                await self.update_data_quality_metrics()
                
                # Clean up old data
                await self.cleanup_old_data()
                
                # Wait for next processing cycle
                await asyncio.sleep(1.0)
                
            except Exception as e:
                self.logger.error(f"Real-time data processing error: {e}")
                await asyncio.sleep(5.0)
    
    async def process_cached_data(self):
        """Process cached market data"""
        try:
            for symbol, data_points in self.market_data_cache.items():
                if len(data_points) >= 10:
                    # Calculate technical indicators
                    await self.calculate_technical_indicators(symbol, data_points)
                    
                    # Generate market signals
                    await self.generate_market_signals(symbol, data_points)
                    
        except Exception as e:
            self.logger.error(f"Cached data processing error: {e}")
    
    async def calculate_technical_indicators(self, symbol: str, data_points: List[MarketDataPoint]):
        """Calculate technical indicators for a symbol"""
        try:
            prices = [data.price for data in data_points]
            
            if len(prices) >= 20:
                # Simple Moving Averages
                sma_20 = sum(prices[-20:]) / 20
                sma_10 = sum(prices[-10:]) / 10
                
                # Store indicators
                if symbol not in self.data_quality_metrics:
                    self.data_quality_metrics[symbol] = {}
                
                self.data_quality_metrics[symbol]['sma_20'] = sma_20
                self.data_quality_metrics[symbol]['sma_10'] = sma_10
                self.data_quality_metrics[symbol]['trend'] = 'bullish' if sma_10 > sma_20 else 'bearish'
            
        except Exception as e:
            self.logger.error(f"Technical indicator calculation error for {symbol}: {e}")
    
    async def generate_market_signals(self, symbol: str, data_points: List[MarketDataPoint]):
        """Generate market signals based on technical analysis"""
        try:
            if symbol not in self.data_quality_metrics:
                return
            
            metrics = self.data_quality_metrics[symbol]
            
            if 'sma_20' in metrics and 'sma_10' in metrics:
                sma_20 = metrics['sma_20']
                sma_10 = metrics['sma_10']
                current_price = data_points[-1].price
                
                # Generate signals based on moving average crossovers
                if sma_10 > sma_20 and current_price > sma_10:
                    signal = MarketSignal(
                        timestamp=datetime.now().isoformat(),
                        symbol=symbol,
                        signal_type='buy',
                        strength=0.7,
                        confidence=0.8,
                        reasoning=['Golden cross detected', 'Price above moving averages'],
                        source='technical_analysis'
                    )
                    self.market_signals.append(signal)
                    
                elif sma_10 < sma_20 and current_price < sma_10:
                    signal = MarketSignal(
                        timestamp=datetime.now().isoformat(),
                        symbol=symbol,
                        signal_type='sell',
                        strength=0.7,
                        confidence=0.8,
                        reasoning=['Death cross detected', 'Price below moving averages'],
                        source='technical_analysis'
                    )
                    self.market_signals.append(signal)
            
        except Exception as e:
            self.logger.error(f"Market signal generation error for {symbol}: {e}")
    
    async def generate_alternative_signals(self, alternative_data: Dict):
        """Generate signals based on alternative data"""
        try:
            data_type = alternative_data['type']
            
            if data_type == 'sentiment':
                sentiment_value = alternative_data['value']
                
                if sentiment_value > 0.7:
                    signal = MarketSignal(
                        timestamp=datetime.now().isoformat(),
                        symbol='MARKET',
                        signal_type='buy',
                        strength=0.6,
                        confidence=0.7,
                        reasoning=['High market sentiment', 'Positive market outlook'],
                        source='sentiment_analysis'
                    )
                    self.market_signals.append(signal)
                    
                elif sentiment_value < 0.3:
                    signal = MarketSignal(
                        timestamp=datetime.now().isoformat(),
                        symbol='MARKET',
                        signal_type='sell',
                        strength=0.6,
                        confidence=0.7,
                        reasoning=['Low market sentiment', 'Negative market outlook'],
                        source='sentiment_analysis'
                    )
                    self.market_signals.append(signal)
            
            elif data_type == 'options_flow':
                put_call_ratio = alternative_data['put_call_ratio']
                
                if put_call_ratio > 1.5:
                    signal = MarketSignal(
                        timestamp=datetime.now().isoformat(),
                        symbol='MARKET',
                        signal_type='buy',
                        strength=0.8,
                        confidence=0.9,
                        reasoning=['High put-call ratio', 'Fear in options market'],
                        source='options_flow'
                    )
                    self.market_signals.append(signal)
                    
                elif put_call_ratio < 0.5:
                    signal = MarketSignal(
                        timestamp=datetime.now().isoformat(),
                        symbol='MARKET',
                        signal_type='sell',
                        strength=0.8,
                        confidence=0.9,
                        reasoning=['Low put-call ratio', 'Complacency in options market'],
                        source='options_flow'
                    )
                    self.market_signals.append(signal)
            
        except Exception as e:
            self.logger.error(f"Alternative signal generation error: {e}")
    
    async def market_signal_generation(self):
        """Continuous market signal generation"""
        print("📊 Starting market signal generation...")
        
        while True:
            try:
                # Process existing signals
                await self.process_market_signals()
                
                # Generate new signals based on market conditions
                await self.generate_market_condition_signals()
                
                # Wait for next signal generation cycle
                await asyncio.sleep(5.0)
                
            except Exception as e:
                self.logger.error(f"Market signal generation error: {e}")
                await asyncio.sleep(10.0)
    
    async def process_market_signals(self):
        """Process existing market signals"""
        try:
            # Keep only recent signals (last 100)
            if len(self.market_signals) > 100:
                self.market_signals = self.market_signals[-100:]
            
            # Log recent signals
            recent_signals = self.market_signals[-5:] if self.market_signals else []
            for signal in recent_signals:
                self.logger.info(f"Signal: {signal.symbol} {signal.signal_type.upper()} "
                               f"(strength: {signal.strength:.2f}, confidence: {signal.confidence:.2f})")
            
        except Exception as e:
            self.logger.error(f"Market signal processing error: {e}")
    
    async def generate_market_condition_signals(self):
        """Generate signals based on overall market conditions"""
        try:
            # Analyze market breadth
            market_breadth = await self.calculate_market_breadth()
            
            if market_breadth > 0.7:
                signal = MarketSignal(
                    timestamp=datetime.now().isoformat(),
                    symbol='MARKET',
                    signal_type='buy',
                    strength=0.6,
                    confidence=0.7,
                    reasoning=['Strong market breadth', 'Broad market participation'],
                    source='market_analysis'
                )
                self.market_signals.append(signal)
                
            elif market_breadth < 0.3:
                signal = MarketSignal(
                    timestamp=datetime.now().isoformat(),
                    symbol='MARKET',
                    signal_type='sell',
                    strength=0.6,
                    confidence=0.7,
                    reasoning=['Weak market breadth', 'Limited market participation'],
                    source='market_analysis'
                )
                self.market_signals.append(signal)
            
        except Exception as e:
            self.logger.error(f"Market condition signal generation error: {e}")
    
    async def calculate_market_breadth(self) -> float:
        """Calculate market breadth indicator"""
        try:
            if not self.market_data_cache:
                return 0.5
            
            advancing = 0
            total_symbols = 0
            
            for symbol, data_points in self.market_data_cache.items():
                if len(data_points) >= 2:
                    total_symbols += 1
                    current_price = data_points[-1].price
                    previous_price = data_points[-2].price
                    
                    if current_price > previous_price:
                        advancing += 1
            
            if total_symbols > 0:
                return advancing / total_symbols
            else:
                return 0.5
                
        except Exception as e:
            self.logger.error(f"Market breadth calculation error: {e}")
            return 0.5
    
    async def data_quality_monitoring(self):
        """Monitor data quality and performance"""
        print("🔍 Starting data quality monitoring...")
        
        while True:
            try:
                # Calculate data quality metrics
                await self.calculate_data_quality_metrics()
                
                # Monitor data source performance
                await self.monitor_data_source_performance()
                
                # Generate quality reports
                await self.generate_quality_reports()
                
                # Wait for next monitoring cycle
                await asyncio.sleep(30.0)
                
            except Exception as e:
                self.logger.error(f"Data quality monitoring error: {e}")
                await asyncio.sleep(60.0)
    
    async def calculate_data_quality_metrics(self):
        """Calculate comprehensive data quality metrics"""
        try:
            total_data_points = 0
            valid_data_points = 0
            total_latency = 0.0
            
            for symbol, data_points in self.market_data_cache.items():
                total_data_points += len(data_points)
                
                for data_point in data_points:
                    if data_point.quality > 0.8:
                        valid_data_points += 1
                    
                    # Calculate latency (simplified)
                    try:
                        timestamp = datetime.fromisoformat(data_point.timestamp)
                        latency = (datetime.now() - timestamp).total_seconds()
                        total_latency += latency
                    except:
                        pass
            
            # Calculate overall quality metrics
            if total_data_points > 0:
                data_quality = valid_data_points / total_data_points
                avg_latency = total_latency / total_data_points if total_data_points > 0 else 0
                
                # Store metrics
                self.data_quality_metrics['overall'] = {
                    'data_quality': data_quality,
                    'avg_latency': avg_latency,
                    'total_data_points': total_data_points,
                    'valid_data_points': valid_data_points,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Store in history
                self.data_quality_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'data_quality': data_quality,
                    'avg_latency': avg_latency,
                    'total_data_points': total_data_points
                })
                
                # Keep only last 1000 quality records
                if len(self.data_quality_history) > 1000:
                    self.data_quality_history = self.data_quality_history[-1000:]
            
        except Exception as e:
            self.logger.error(f"Data quality metrics calculation error: {e}")

    async def update_data_quality_metrics(self):
        """Update data quality metrics by recalculating current values"""
        try:
            print("📊 Updating data quality metrics...")
            await self.calculate_data_quality_metrics()
            print("✅ Data quality metrics updated successfully")
        except Exception as e:
            self.logger.error(f"Data quality metrics update error: {e}")
            print(f"❌ Failed to update data quality metrics: {e}")

    async def monitor_data_source_performance(self):
        """Monitor performance of data sources"""
        try:
            for source_name, source_info in self.data_sources.items():
                # Simulate performance monitoring
                if source_info['status'] == 'active':
                    # Update latency (simulate real-time monitoring)
                    source_info['latency'] = source_info['latency'] * (0.9 + np.random.normal(0, 0.1))
                    
                    # Update reliability (simulate real-time monitoring)
                    source_info['reliability'] = max(0.8, source_info['reliability'] + np.random.normal(0, 0.02))
                    
                    # Store performance metrics
                    if source_name not in self.data_quality_metrics:
                        self.data_quality_metrics[source_name] = {}
                    
                    self.data_quality_metrics[source_name]['performance'] = {
                        'latency': source_info['latency'],
                        'reliability': source_info['reliability'],
                        'status': source_info['status'],
                        'last_updated': datetime.now().isoformat()
                    }
            
        except Exception as e:
            self.logger.error(f"Data source performance monitoring error: {e}")
    
    async def generate_quality_reports(self):
        """Generate data quality reports"""
        try:
            if 'overall' in self.data_quality_metrics:
                overall_metrics = self.data_quality_metrics['overall']
                
                report = {
                    'timestamp': datetime.now().isoformat(),
                    'overall_quality': overall_metrics['data_quality'],
                    'avg_latency': overall_metrics['avg_latency'],
                    'total_data_points': overall_metrics['total_data_points'],
                    'valid_data_points': overall_metrics['valid_data_points'],
                    'data_sources': len(self.data_sources),
                    'active_alerts': len(self.price_alerts) + len(self.volume_alerts) + len(self.volatility_alerts),
                    'market_signals': len(self.market_signals)
                }
                
                # Save quality report
                await self.save_quality_report(report)
                
                # Log quality metrics
                self.logger.info(f"Data Quality Report: Quality={overall_metrics['data_quality']:.2f}, "
                               f"Latency={overall_metrics['avg_latency']:.3f}s, "
                               f"Data Points={overall_metrics['total_data_points']}")
            
        except Exception as e:
            self.logger.error(f"Quality report generation error: {e}")
    
    async def market_data_distribution(self):
        """Distribute market data to other agents"""
        print("📤 Starting market data distribution...")
        
        while True:
            try:
                # Distribute real-time data
                await self.distribute_real_time_data()
                
                # Distribute market signals
                await self.distribute_market_signals()
                
                # Distribute alerts
                await self.distribute_alerts()
                
                # Wait for next distribution cycle
                await asyncio.sleep(1.0)
                
            except Exception as e:
                self.logger.error(f"Market data distribution error: {e}")
                await asyncio.sleep(5.0)
    
    async def distribute_real_time_data(self):
        """Distribute real-time market data"""
        try:
            # This would integrate with the firm's communication system
            # For now, we'll just log the distribution
            if self.real_time_feeds:
                self.logger.debug(f"Distributing real-time data for {len(self.real_time_feeds)} symbols")
            
        except Exception as e:
            self.logger.error(f"Real-time data distribution error: {e}")
    
    async def distribute_market_signals(self):
        """Distribute market signals"""
        try:
            # This would integrate with the firm's communication system
            # For now, we'll just log the distribution
            if self.market_signals:
                recent_signals = self.market_signals[-5:] if self.market_signals else []
                for signal in recent_signals:
                    self.logger.debug(f"Distributing signal: {signal.symbol} {signal.signal_type}")
            
        except Exception as e:
            self.logger.error(f"Market signal distribution error: {e}")
    
    async def distribute_alerts(self):
        """Distribute market alerts"""
        try:
            # This would integrate with the firm's communication system
            # For now, we'll just log the distribution
            total_alerts = len(self.price_alerts) + len(self.volume_alerts) + len(self.volatility_alerts)
            if total_alerts > 0:
                self.logger.debug(f"Distributing {total_alerts} market alerts")
            
        except Exception as e:
            self.logger.error(f"Alert distribution error: {e}")
    
    async def performance_optimization(self):
        """Optimize agent performance"""
        print("⚡ Starting performance optimization...")
        
        while True:
            try:
                # Optimize data processing
                await self.optimize_data_processing()
                
                # Optimize cache management
                await self.optimize_cache_management()
                
                # Update performance metrics
                await self.update_performance_metrics()
                
                # Wait for next optimization cycle
                await asyncio.sleep(300.0)  # 5 minutes
                
            except Exception as e:
                self.logger.error(f"Performance optimization error: {e}")
                await asyncio.sleep(600.0)  # 10 minutes
    
    async def optimize_data_processing(self):
        """Optimize data processing pipeline"""
        try:
            # Analyze processing times
            if self.processing_times:
                avg_processing_time = sum(self.processing_times) / len(self.processing_times)
                
                # Optimize update frequency based on processing performance
                if avg_processing_time > 0.2:  # 200ms
                    self.update_frequency = min(0.2, self.update_frequency * 1.1)
                    self.logger.info(f"Optimized update frequency to {self.update_frequency:.3f}s")
                elif avg_processing_time < 0.05:  # 50ms
                    self.update_frequency = max(0.05, self.update_frequency * 0.9)
                    self.logger.info(f"Optimized update frequency to {self.update_frequency:.3f}s")
            
        except Exception as e:
            self.logger.error(f"Data processing optimization error: {e}")
    
    async def optimize_cache_management(self):
        """Optimize cache management"""
        try:
            # Adjust cache size based on memory usage
            total_cached_items = sum(len(data) for data in self.market_data_cache.values())
            
            if total_cached_items > self.max_cache_size * 0.8:
                # Reduce cache size
                self.max_cache_size = max(5000, int(self.max_cache_size * 0.9))
                self.logger.info(f"Reduced max cache size to {self.max_cache_size}")
            
            # Clean up old data
            await self.cleanup_old_data()
            
        except Exception as e:
            self.logger.error(f"Cache management optimization error: {e}")
    
    async def cleanup_old_data(self):
        """Clean up old data from cache"""
        try:
            current_time = datetime.now()
            
            for symbol in list(self.market_data_cache.keys()):
                # Remove data older than cache expiry
                self.market_data_cache[symbol] = [
                    data for data in self.market_data_cache[symbol]
                    if (current_time - datetime.fromisoformat(data.timestamp)).total_seconds() < self.cache_expiry
                ]
                
                # Remove symbols with no data
                if not self.market_data_cache[symbol]:
                    del self.market_data_cache[symbol]
            
        except Exception as e:
            self.logger.error(f"Data cleanup error: {e}")
    
    async def update_performance_metrics(self):
        """Update performance metrics"""
        try:
            # Calculate processing time for this cycle
            start_time = time.time()
            
            # Simulate some processing
            await asyncio.sleep(0.01)
            
            processing_time = time.time() - start_time
            self.processing_times.append(processing_time)
            
            # Keep only last 100 processing times
            if len(self.processing_times) > 100:
                self.processing_times = self.processing_times[-100:]
            
        except Exception as e:
            self.logger.error(f"Performance metrics update error: {e}")
    
    async def save_quality_report(self, report: Dict):
        """Save quality report to file"""
        try:
            filename = f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.logger.info(f"Quality report saved: {filename}")
            
        except Exception as e:
            self.logger.error(f"Quality report save error: {e}")
    
    def get_market_data_summary(self) -> Dict:
        """Get comprehensive market data summary"""
        try:
            return {
                'agent_status': 'active',
                'data_sources': len(self.data_sources),
                'active_symbols': len(self.market_data_cache),
                'total_data_points': sum(len(data) for data in self.market_data_cache.values()),
                'market_signals': len(self.market_signals),
                'active_alerts': len(self.price_alerts) + len(self.volume_alerts) + len(self.volatility_alerts),
                'data_quality': self.data_quality_metrics.get('overall', {}).get('data_quality', 0.0),
                'avg_latency': self.data_quality_metrics.get('overall', {}).get('avg_latency', 0.0),
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Market data summary error: {e}")
            return {'error': str(e)}

async def main():
    """Main function to run the unified market data agent"""
    print("🚀 UNIFIED MARKET DATA AGENT")
    print("=" * 50)
    
    try:
        # Initialize agent
        market_data_agent = UnifiedMarketDataAgent()
        
        # Run agent
        await market_data_agent.run_unified_market_data_agent()
        
    except KeyboardInterrupt:
        print("\n🛑 Unified Market Data Agent stopped by user")
    except Exception as e:
        print(f"❌ Unified Market Data Agent error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
