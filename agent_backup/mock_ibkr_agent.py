#!/usr/bin/env python3
"""
Mock IBKR Agent - Test your trading logic without actual IBKR connection
Simulates paper trading for development
"""

import json
import asyncio
import time
from datetime import datetime

class MockIBKRAgent:
    def __init__(self):
        print("📊 MOCK IBKR AGENT - PAPER TRADING SIMULATION")
        print("🎯 Testing trading logic without real broker connection")
        
        self.portfolio_value = 10000  # Start with $10k paper money
        self.available_funds = 10000
        self.positions = {}
        self.trade_history = []
        
    def generate_mock_research(self):
        """Generate mock research opportunities"""
        return {
            'opportunities': [
                {
                    'ticker': 'NVDA',
                    'opportunity': 'NVDA - AI chip demand surge',
                    'thesis': 'Continued AI infrastructure buildout driving demand',
                    'research_confidence': 'High',
                    'risk_level': 'Medium'
                },
                {
                    'ticker': 'TSLA', 
                    'opportunity': 'TSLA - EV market expansion',
                    'thesis': 'Global EV adoption accelerating, production scaling',
                    'research_confidence': 'Medium',
                    'risk_level': 'High'
                },
                {
                    'ticker': 'BTC',
                    'opportunity': 'BTC - Institutional adoption',
                    'thesis': 'ETF approvals driving institutional inflows',
                    'research_confidence': 'High',
                    'risk_level': 'Medium-High'
                }
            ]
        }
        
    def get_mock_price(self, ticker):
        """Get mock market prices for testing"""
        mock_prices = {
            'NVDA': 850.00,
            'TSLA': 248.50,
            'AAPL': 192.75,
            'MSFT': 415.20,
            'BTC': 67234.50,
            'ETH': 3456.78
        }
        return mock_prices.get(ticker, 100.00)
        
    def calculate_position_size(self, ticker, confidence, risk_level):
        """Calculate position size with risk management"""
        base_size = min(1000, self.available_funds * 0.05)  # Max 5% of funds
        
        # Adjust based on confidence
        confidence_multiplier = {'High': 1.0, 'Medium': 0.7, 'Low': 0.4}
        confidence_adj = confidence_multiplier.get(confidence, 0.4)
        
        # Adjust based on risk level
        risk_multiplier = {
            'Low': 1.0, 
            'Medium': 0.8, 
            'High': 0.6, 
            'Medium-High': 0.7
        }
        risk_adj = risk_multiplier.get(risk_level, 0.6)
        
        position_size = base_size * confidence_adj * risk_adj
        return min(position_size, 1000)  # Max $1000 per position
        
    async def execute_mock_trade(self, opportunity):
        """Execute simulated trade"""
        ticker = opportunity['ticker']
        current_price = self.get_mock_price(ticker)
        
        # Calculate position size
        position_value = self.calculate_position_size(
            ticker, 
            opportunity['research_confidence'], 
            opportunity['risk_level']
        )
        
        # Special handling for crypto (fractional shares)
        if ticker in ['BTC', 'ETH']:
            shares = position_value / current_price  # Fractional crypto
        else:
            shares = int(position_value / current_price)  # Whole shares for stocks
        
        if (ticker in ['BTC', 'ETH'] and shares < 0.001) or (ticker not in ['BTC', 'ETH'] and shares < 1):
            print(f"⚠️ Position too small for {ticker}: ${position_value:.2f}")
            return None
            
        # Calculate actual trade value
        trade_value = shares * current_price
        
        if trade_value > self.available_funds:
            print(f"❌ Insufficient funds for {ticker}: Need ${trade_value:.2f}, have ${self.available_funds:.2f}")
            return None
            
        # Execute mock trade
        self.available_funds -= trade_value
        if ticker in self.positions:
            self.positions[ticker] += shares
        else:
            self.positions[ticker] = shares
            
        trade_record = {
            'ticker': ticker,
            'shares': shares,
            'price': current_price,
            'value': trade_value,
            'timestamp': datetime.now().isoformat(),
            'thesis': opportunity['thesis']
        }
        
        self.trade_history.append(trade_record)
        
        print(f"✅ MOCK TRADE EXECUTED:")
        print(f"   {ticker}: {shares:.4f} shares @ ${current_price:.2f}")
        print(f"   Value: ${trade_value:.2f}")
        print(f"   Thesis: {opportunity['thesis']}")
        print(f"   Remaining funds: ${self.available_funds:.2f}")
        
        return trade_record
        
    async def run_mock_trading_cycle(self):
        """Run one complete trading cycle"""
        print("\n🔄 MOCK TRADING CYCLE STARTING...")
        print("=" * 50)
        
        # 1. Generate research
        print("1️⃣ Generating investment research...")
        research_data = self.generate_mock_research()
        opportunities = research_data['opportunities']
        
        print(f"2️⃣ Found {len(opportunities)} trading opportunities:")
        for i, opp in enumerate(opportunities, 1):
            print(f"   {i}. {opp['ticker']} - {opp['research_confidence']} confidence")
            
        # 3. Execute mock trades
        executed_trades = 0
        max_trades = 3  # Limit trades per cycle
        
        for opp in opportunities[:max_trades]:
            print(f"\n3️⃣ Evaluating trade: {opp['ticker']}")
            print(f"   Confidence: {opp['research_confidence']}")
            print(f"   Risk Level: {opp['risk_level']}")
            
            trade_result = await self.execute_mock_trade(opp)
            if trade_result:
                executed_trades += 1
                
            # Small delay between trades
            await asyncio.sleep(1)
                
        # 4. Portfolio summary
        print(f"\n📊 PORTFOLIO SUMMARY:")
        print("=" * 30)
        print(f"💰 Portfolio Value: ${self.portfolio_value:.2f}")
        print(f"💵 Available Funds: ${self.available_funds:.2f}")
        print(f"📈 Active Positions: {len(self.positions)}")
        print(f"🔄 Trades Executed: {executed_trades}")
        
        if self.positions:
            print(f"\n📋 CURRENT POSITIONS:")
            for ticker, shares in self.positions.items():
                current_price = self.get_mock_price(ticker)
                market_value = shares * current_price
                print(f"   {ticker}: {shares:.4f} shares (${market_value:.2f})")
        
        # 5. Save mock portfolio
        portfolio_data = {
            'timestamp': datetime.now().isoformat(),
            'portfolio_value': self.portfolio_value,
            'available_funds': self.available_funds,
            'positions': self.positions,
            'trade_history': self.trade_history,
            'total_trades': len(self.trade_history)
        }
        
        filename = f'mock_portfolio_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(portfolio_data, f, indent=2)
            
        print(f"\n💾 Portfolio saved to: {filename}")
        
        return executed_trades

if __name__ == "__main__":
    async def main():
        print("🚀 STARTING MOCK IBKR TRADING AGENT...")
        print("🤖 WealthyRobot Investment Division - Paper Trading Test")
        print("")
        
        agent = MockIBKRAgent()
        
        # Run trading cycle
        trades_executed = await agent.run_mock_trading_cycle()
        
        print(f"\n✅ MOCK TRADING CYCLE COMPLETE!")
        print(f"🎯 Result: {trades_executed} trades executed")
        print(f"💡 This shows exactly how your AI would trade with real IBKR!")
        print("")
        print("🔄 Next steps:")
        print("1. Install IB Gateway")
        print("2. Replace with real IBKR integration")
        print("3. Start paper trading on IBKR")
        print("4. Graduate to live trading")
        
    asyncio.run(main())
