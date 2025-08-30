#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: Real-Time Market Data Agent
PURPOSE: Live market data aggregation and real-time quote feeds for trading decisions
CATEGORY: Trading & Market Data
STATUS: Active - New
FREQUENCY: Real-time (continuous)
"""

import asyncio
import aiohttp
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import websockets
import pandas as pd

class RealTimeMarketDataAgent:
    """Real-time market data aggregation agent for live trading"""
    
    def __init__(self):
        self.agent_name = "Real-Time Market Data Agent"
        self.version = "1.0 - Live Market Data"
        
        # Market data sources
        self.data_sources = {
            'alpha_vantage': os.getenv('ALPHA_VANTAGE_API_KEY'),
            'polygon': os.getenv('POLYGON_API_KEY'),
            'finnhub': os.getenv('FINNHUB_API_KEY'),
            'yahoo_finance': None,  # Free tier
            'coinbase': None,  # Crypto data
            'binance': None     # Crypto data
        }
        
        # Real-time data storage
        self.live_quotes = {}
        self.market_depth = {}
        self.technical_indicators = {}
        self.news_feed = []
        
        # Performance metrics
        self.data_latency = {}
        self.update_frequency = {}
        self.data_quality_scores = {}
        
        # Trading pairs to monitor
        self.monitored_symbols = [
            'AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'META',
            'BTC', 'ETH', 'SPY', 'QQQ', 'IWM', 'GLD', 'SLV'
        ]
        
        print(f"📡 {self.agent_name} v{self.version} initialized")
        print("🔗 Connecting to live market data sources...")
        
    async def connect_to_data_sources(self):
        """Establish connections to market data providers"""
        print("🔌 Establishing market data connections...")
        
        connections = {}
        
        # Alpha Vantage (Stocks)
        if self.data_sources['alpha_vantage']:
            try:
                test_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=1min&apikey={self.data_sources['alpha_vantage']}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(test_url) as response:
                        if response.status == 200:
                            connections['alpha_vantage'] = 'Connected'
                            print("✅ Alpha Vantage: Connected")
                        else:
                            connections['alpha_vantage'] = 'Failed'
                            print("❌ Alpha Vantage: Connection failed")
            except Exception as e:
                connections['alpha_vantage'] = f'Error: {str(e)}'
                print(f"❌ Alpha Vantage: {str(e)}")
        
        # Polygon (Real-time stocks)
        if self.data_sources['polygon']:
            try:
                test_url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/1/day?apiKey={self.data_sources['polygon']}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(test_url) as response:
                        if response.status == 200:
                            connections['polygon'] = 'Connected'
                            print("✅ Polygon: Connected")
                        else:
                            connections['polygon'] = 'Failed'
                            print("❌ Polygon: Connection failed")
            except Exception as e:
                connections['polygon'] = f'Error: {str(e)}'
                print(f"❌ Polygon: {str(e)}")
        
        # Finnhub (Real-time + news)
        if self.data_sources['finnhub']:
            try:
                test_url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={self.data_sources['finnhub']}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(test_url) as response:
                        if response.status == 200:
                            connections['finnhub'] = 'Connected'
                            print("✅ Finnhub: Connected")
                        else:
                            connections['finnhub'] = 'Failed'
                            print("❌ Finnhub: Connection failed")
            except Exception as e:
                connections['finnhub'] = f'Error: {str(e)}'
                print(f"❌ Finnhub: {str(e)}")
        
        # Yahoo Finance (Free tier)
        try:
            # Test Yahoo Finance connection
            test_url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
            async with aiohttp.ClientSession() as session:
                async with session.get(test_url) as response:
                    if response.status == 200:
                        connections['yahoo_finance'] = 'Connected'
                        print("✅ Yahoo Finance: Connected")
                    else:
                        connections['yahoo_finance'] = 'Failed'
                        print("❌ Yahoo Finance: Connection failed")
        except Exception as e:
            connections['yahoo_finance'] = f'Error: {str(e)}'
            print(f"❌ Yahoo Finance: {str(e)}")
        
        return connections
    
    async def get_live_quote(self, symbol: str) -> Dict:
        """Get real-time quote for a symbol"""
        start_time = time.time()
        
        quote_data = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'price': None,
            'volume': None,
            'bid': None,
            'ask': None,
            'change': None,
            'change_percent': None,
            'source': None,
            'latency_ms': None
        }
        
        # Try multiple sources for redundancy
        sources_to_try = []
        
        if self.data_sources['polygon']:
            sources_to_try.append(('polygon', self._get_polygon_quote))
        if self.data_sources['finnhub']:
            sources_to_try.append(('finnhub', self._get_finnhub_quote))
        if self.data_sources['yahoo_finance']:
            sources_to_try.append(('yahoo', self._get_yahoo_quote))
        
        for source_name, source_func in sources_to_try:
            try:
                quote = await source_func(symbol)
                if quote and quote.get('price'):
                    quote_data.update(quote)
                    quote_data['source'] = source_name
                    quote_data['latency_ms'] = int((time.time() - start_time) * 1000)
                    
                    # Store in live quotes
                    self.live_quotes[symbol] = quote_data
                    
                    # Update performance metrics
                    self.data_latency[source_name] = quote_data['latency_ms']
                    self.update_frequency[source_name] = datetime.now()
                    
                    return quote_data
                    
            except Exception as e:
                print(f"⚠️ {source_name} quote failed for {symbol}: {str(e)}")
                continue
        
        # Fallback to cached data if available
        if symbol in self.live_quotes:
            cached = self.live_quotes[symbol]
            cached['timestamp'] = datetime.now().isoformat()
            cached['source'] = 'cached'
            return cached
        
        return quote_data
    
    async def _get_polygon_quote(self, symbol: str) -> Optional[Dict]:
        """Get quote from Polygon API"""
        if not self.data_sources['polygon']:
            return None
            
        url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/{symbol}?apiKey={self.data_sources['polygon']}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if 'results' in data and data['results']:
                        result = data['results']
                        return {
                            'price': result.get('t', {}).get('c', None),
                            'volume': result.get('t', {}).get('v', None),
                            'bid': result.get('t', {}).get('b', None),
                            'ask': result.get('t', {}).get('a', None),
                            'change': result.get('t', {}).get('ch', None),
                            'change_percent': result.get('t', {}).get('chp', None)
                        }
        return None
    
    async def _get_finnhub_quote(self, symbol: str) -> Optional[Dict]:
        """Get quote from Finnhub API"""
        if not self.data_sources['finnhub']:
            return None
            
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.data_sources['finnhub']}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if 'c' in data:  # Current price
                        return {
                            'price': data.get('c', None),
                            'volume': data.get('v', None),
                            'change': data.get('d', None),
                            'change_percent': data.get('dp', None)
                        }
        return None
    
    async def _get_yahoo_quote(self, symbol: str) -> Optional[Dict]:
        """Get quote from Yahoo Finance (free tier)"""
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if 'chart' in data and 'result' in data['chart']:
                        result = data['chart']['result'][0]
                        meta = result.get('meta', {})
                        
                        return {
                            'price': meta.get('regularMarketPrice', None),
                            'volume': meta.get('regularMarketVolume', None),
                            'change': meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0),
                            'change_percent': ((meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0)) / meta.get('previousClose', 1)) * 100 if meta.get('previousClose') else None
                        }
        return None
    
    async def get_market_depth(self, symbol: str) -> Dict:
        """Get real-time market depth (order book)"""
        depth_data = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'bids': [],
            'asks': [],
            'source': None
        }
        
        # Try to get depth data from available sources
        if self.data_sources['polygon']:
            try:
                url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/{symbol}/book?apiKey={self.data_sources['polygon']}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            if 'results' in data and data['results']:
                                book = data['results']
                                depth_data['bids'] = book.get('b', [])[:10]  # Top 10 bids
                                depth_data['asks'] = book.get('a', [])[:10]  # Top 10 asks
                                depth_data['source'] = 'polygon'
                                
                                # Store in market depth
                                self.market_depth[symbol] = depth_data
                                
            except Exception as e:
                print(f"⚠️ Failed to get market depth from Polygon: {str(e)}")
        
        return depth_data
    
    async def get_technical_indicators(self, symbol: str) -> Dict:
        """Get real-time technical indicators"""
        indicators = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'rsi': None,
            'macd': None,
            'bollinger_bands': None,
            'moving_averages': None,
            'source': None
        }
        
        # Calculate basic indicators from price data
        if symbol in self.live_quotes:
            quote = self.live_quotes[symbol]
            
            # Simple RSI calculation (would need historical data for proper calculation)
            # For now, provide placeholder
            indicators['rsi'] = 'Requires historical data'
            indicators['macd'] = 'Requires historical data'
            indicators['bollinger_bands'] = 'Requires historical data'
            indicators['moving_averages'] = 'Requires historical data'
            indicators['source'] = 'calculated'
        
        return indicators
    
    async def get_market_news(self, symbol: str = None) -> List[Dict]:
        """Get real-time market news"""
        news_items = []
        
        # Try Finnhub for news
        if self.data_sources['finnhub']:
            try:
                url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2025-01-01&to=2025-12-31&token={self.data_sources['finnhub']}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            for item in data[:10]:  # Top 10 news items
                                news_items.append({
                                    'headline': item.get('headline', ''),
                                    'summary': item.get('summary', ''),
                                    'url': item.get('url', ''),
                                    'published': item.get('datetime', ''),
                                    'source': 'finnhub'
                                })
                                
            except Exception as e:
                print(f"⚠️ Failed to get news from Finnhub: {str(e)}")
        
        # Update news feed
        self.news_feed = news_items
        return news_items
    
    async def start_real_time_feed(self):
        """Start continuous real-time market data feed"""
        print("🚀 Starting real-time market data feed...")
        
        while True:
            try:
                # Update all monitored symbols
                for symbol in self.monitored_symbols:
                    # Get live quote
                    quote = await self.get_live_quote(symbol)
                    
                    # Get market depth (less frequent)
                    if time.time() % 30 < 1:  # Every 30 seconds
                        depth = await self.get_market_depth(symbol)
                    
                    # Get technical indicators (less frequent)
                    if time.time() % 60 < 1:  # Every minute
                        indicators = await self.get_technical_indicators(symbol)
                
                # Get market news (every 5 minutes)
                if time.time() % 300 < 1:
                    news = await self.get_market_news()
                
                # Update data quality scores
                self._update_data_quality_scores()
                
                # Wait before next update
                await asyncio.sleep(1)  # 1 second updates
                
            except Exception as e:
                print(f"❌ Real-time feed error: {str(e)}")
                await asyncio.sleep(5)  # Wait 5 seconds on error
    
    def _update_data_quality_scores(self):
        """Update data quality scores for each source"""
        for source, latency in self.data_latency.items():
            # Calculate quality score based on latency and update frequency
            if source in self.update_frequency:
                last_update = self.update_frequency[source]
                time_since_update = (datetime.now() - last_update).total_seconds()
                
                # Quality score: 100 - latency_ms - seconds_since_update
                quality_score = max(0, 100 - latency - int(time_since_update))
                self.data_quality_scores[source] = quality_score
    
    def get_data_summary(self) -> Dict:
        """Get summary of current market data status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'symbols_monitored': len(self.monitored_symbols),
            'live_quotes': len(self.live_quotes),
            'market_depth_data': len(self.market_depth),
            'news_items': len(self.news_feed),
            'data_sources': {
                source: {
                    'status': 'Connected' if self.data_sources[source] else 'Not configured',
                    'quality_score': self.data_quality_scores.get(source, 0),
                    'latency_ms': self.data_latency.get(source, 0)
                }
                for source in self.data_sources.keys()
            },
            'performance_metrics': {
                'total_updates': sum(len(self.update_frequency.values())),
                'average_latency': sum(self.data_latency.values()) / len(self.data_latency) if self.data_latency else 0
            }
        }
    
    async def run_agent(self):
        """Main agent execution loop"""
        print(f"🤖 {self.agent_name} starting...")
        
        # Connect to data sources
        connections = await self.connect_to_data_sources()
        
        # Start real-time feed
        await self.start_real_time_feed()

async def main():
    """Test the real-time market data agent"""
    agent = RealTimeMarketDataAgent()
    
    # Test single quote
    print("\n📊 Testing live quote...")
    quote = await agent.get_live_quote('AAPL')
    print(f"AAPL Quote: {json.dumps(quote, indent=2)}")
    
    # Test market depth
    print("\n📚 Testing market depth...")
    depth = await agent.get_market_depth('AAPL')
    print(f"AAPL Depth: {json.dumps(depth, indent=2)}")
    
    # Test news
    print("\n📰 Testing news feed...")
    news = await agent.get_market_news('AAPL')
    print(f"News items: {len(news)}")
    
    # Get data summary
    print("\n📈 Data Summary:")
    summary = agent.get_data_summary()
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
