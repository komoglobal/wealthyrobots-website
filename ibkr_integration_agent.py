#!/usr/bin/env python3
"""
IBKR Integration Agent - Connect WealthyRobot to Interactive Brokers
Research + Execute trades through IBKR API
"""

from ib_insync import *
import asyncio
import json
import os
from datetime import datetime, timedelta
from investment_research_agent import InvestmentResearchAgent

class IBKRIntegrationAgent:
    def __init__(self):
        print("🏦 IBKR INTEGRATION AGENT - INITIALIZING...")
        print("📡 Connecting to Interactive Brokers API")
        
        self.ib = IB()
        self.researcher = InvestmentResearchAgent()
        self.connected = False
        self.portfolio_value = 0
        self.available_funds = 0
        
        # Trading parameters
        self.max_position_size = 1000  # Max $1000 per position initially
        self.max_daily_trades = 5      # Max 5 trades per day
        self.risk_per_trade = 0.02     # 2% risk per trade
        
    async def connect_to_ibkr(self):
        """Connect to IBKR TWS or Gateway"""
        try:
            print("🔌 Connecting to IBKR...")
            
            # Connect to TWS (paper trading initially)
            await self.ib.connectAsync('127.0.0.1', 7497, clientId=1)
            self.connected = True
            
            print("✅ Connected to IBKR successfully!")
            
            # Get account info
            account_summary = self.ib.accountSummary()
            for item in account_summary:
                if item.tag == 'TotalCashValue':
                    self.available_funds = float(item.value)
                elif item.tag == 'NetLiquidation':
                    self.portfolio_value = float(item.value)
                    
            print(f"💰 Portfolio Value: ${self.portfolio_value:,.2f}")
            print(f"💵 Available Funds: ${self.available_funds:,.2f}")
            
        except Exception as e:
            print(f"❌ IBKR connection error: {e}")
            print("📋 Make sure TWS/Gateway is running on port 7497")
            self.connected = False
            
    def get_market_data(self, symbol):
        """Get real-time market data for symbol"""
        try:
            # Create contract
            if symbol in ['BTC', 'ETH']:
                # Crypto
                contract = Crypto(symbol, 'PAXOS', 'USD')
            else:
                # Stock
                contract = Stock(symbol, 'SMART', 'USD')
                
            # Get market data
            self.ib.reqMktData(contract)
            self.ib.sleep(2)  # Wait for data
            
            ticker = self.ib.ticker(contract)
            
            return {
                'symbol': symbol,
                'last_price': ticker.last,
                'bid': ticker.bid,
                'ask': ticker.ask,
                'volume': ticker.volume,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Market data error for {symbol}: {e}")
            return None
            
    def analyze_research_for_trades(self, research_report):
        """Analyze research report and identify tradeable opportunities"""
        print("🔍 Analyzing research for trading opportunities...")
        
        tradeable_opportunities = []
        
        for area in research_report['market_research']['research_areas']:
            for opp in area.get('opportunities', []):
                # Extract ticker symbol from opportunity
                ticker = self.extract_ticker(opp['opportunity'])
                
                if ticker and opp['research_confidence'] in ['High', 'Medium']:
                    tradeable_opportunities.append({
                        'ticker': ticker,
                        'direction': 'long',  # Assume long positions for now
                        'confidence': opp['research_confidence'],
                        'risk_level': opp['risk_level'],
                        'thesis': opp['thesis'],
                        'time_horizon': opp['time_horizon']
                    })
                    
        return tradeable_opportunities
        
    def extract_ticker(self, opportunity_text):
        """Extract ticker symbol from opportunity text"""
        # Simple extraction - in production would be more sophisticated
        tickers = ['NVDA', 'TSLA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'BTC', 'ETH']
        
        for ticker in tickers:
            if ticker in opportunity_text.upper():
                return ticker
        return None
        
    def calculate_position_size(self, ticker, confidence, risk_level):
        """Calculate appropriate position size based on risk management"""
        base_size = min(self.max_position_size, self.available_funds * 0.05)  # Max 5% of funds
        
        # Adjust based on confidence
        confidence_multiplier = {'High': 1.0, 'Medium': 0.7, 'Low': 0.4}
        confidence_adj = confidence_multiplier.get(confidence, 0.4)
        
        # Adjust based on risk level
        risk_multiplier = {'Low': 1.0, 'Medium': 0.8, 'High': 0.6, 'Medium-High': 0.7}
        risk_adj = risk_multiplier.get(risk_level, 0.6)
        
        position_size = base_size * confidence_adj * risk_adj
        
        return min(position_size, self.max_position_size)
        
    async def execute_trade(self, opportunity):
        """Execute trade based on research opportunity"""
        if not self.connected:
            print("❌ Not connected to IBKR")
            return None
            
        try:
            ticker = opportunity['ticker']
            
            # Get current market data
            market_data = self.get_market_data(ticker)
            if not market_data:
                print(f"❌ No market data for {ticker}")
                return None
                
            current_price = market_data['last_price']
            if not current_price:
                current_price = (market_data['bid'] + market_data['ask']) / 2
                
            # Calculate position size
            position_value = self.calculate_position_size(
                ticker, 
                opportunity['confidence'], 
                opportunity['risk_level']
            )
            
            shares = int(position_value / current_price)
            
            if shares < 1:
                print(f"⚠️ Position too small for {ticker}: ${position_value:.2f}")
                return None
                
            # Create contract
            if ticker in ['BTC', 'ETH']:
                contract = Crypto(ticker, 'PAXOS', 'USD')
            else:
                contract = Stock(ticker, 'SMART', 'USD')
                
            # Create order
            order = MarketOrder('BUY', shares)
            
            print(f"📈 EXECUTING TRADE:")
            print(f"   Ticker: {ticker}")
            print(f"   Shares: {shares}")
            print(f"   Est. Value: ${shares * current_price:.2f}")
            print(f"   Thesis: {opportunity['thesis']}")
            
            # PAPER TRADING ONLY - Remove this check for live trading
            if input("Confirm trade? (y/n): ").lower().startswith('y'):
                trade = self.ib.placeOrder(contract, order)
                
                # Wait for fill
                await asyncio.sleep(2)
                
                print(f"✅ Trade executed: {trade.orderStatus.status}")
                
                return {
                    'ticker': ticker,
                    'shares': shares,
                    'price': current_price,
                    'value': shares * current_price,
                    'status': trade.orderStatus.status,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                print("❌ Trade cancelled by user")
                return None
                
        except Exception as e:
            print(f"❌ Trade execution error: {e}")
            return None
            
    async def run_automated_trading(self):
        """Run automated research + trading cycle"""
        print("🤖 STARTING AUTOMATED TRADING SYSTEM...")
        print("🔍 Research → Analysis → Execution cycle")
        
        while True:
            try:
                print(f"\n📊 TRADING CYCLE - {datetime.now().strftime('%H:%M:%S')}")
                
                # 1. Generate research
                print("1️⃣ Generating investment research...")
                research_report = self.researcher.generate_research_report()
                
                # 2. Analyze for trades
                print("2️⃣ Analyzing research for trading opportunities...")
                opportunities = self.analyze_research_for_trades(research_report)
                
                print(f"🎯 Found {len(opportunities)} trading opportunities")
                
                # 3. Execute trades (with limits)
                trades_today = 0
                for opp in opportunities[:self.max_daily_trades]:
                    if trades_today >= self.max_daily_trades:
                        print(f"⚠️ Daily trade limit reached ({self.max_daily_trades})")
                        break
                        
                    print(f"3️⃣ Evaluating trade: {opp['ticker']}")
                    
                    # Execute trade
                    trade_result = await self.execute_trade(opp)
                    if trade_result:
                        trades_today += 1
                        print(f"✅ Trade {trades_today}: {trade_result['ticker']}")
                        
                # 4. Update portfolio
                print("4️⃣ Updating portfolio status...")
                await self.update_portfolio_status()
                
                # Wait 4 hours between cycles
                print("⏳ Next cycle in 4 hours...")
                await asyncio.sleep(14400)
                
            except KeyboardInterrupt:
                print("\n🛑 Trading system stopped by user")
                break
            except Exception as e:
                print(f"❌ Trading cycle error: {e}")
                await asyncio.sleep(1800)  # Wait 30 minutes on error
                
    async def update_portfolio_status(self):
        """Update portfolio status and performance"""
        if not self.connected:
            return
            
        try:
            # Get current positions
            positions = self.ib.positions()
            
            portfolio_status = {
                'timestamp': datetime.now().isoformat(),
                'total_value': self.portfolio_value,
                'available_funds': self.available_funds,
                'positions': []
            }
            
            for pos in positions:
                portfolio_status['positions'].append({
                    'symbol': pos.contract.symbol,
                    'quantity': pos.position,
                    'market_value': pos.marketValue,
                    'unrealized_pnl': pos.unrealizedPNL
                })
                
            # Save portfolio status
            with open(f'portfolio_status_{datetime.now().strftime("%Y%m%d_%H%M")}.json', 'w') as f:
                json.dump(portfolio_status, f, indent=2)
                
            print(f"💼 Portfolio updated: {len(positions)} positions")
            
        except Exception as e:
            print(f"❌ Portfolio update error: {e}")

if __name__ == "__main__":
    async def main():
        print("🚀 Starting IBKR Integration Agent...")
        
        agent = IBKRIntegrationAgent()
        
        # Connect to IBKR
        await agent.connect_to_ibkr()
        
        if agent.connected:
            print("✅ IBKR connection successful!")
            
            # Run automated trading
            response = input("Start automated trading? (y/n): ")
            if response.lower().startswith('y'):
                await agent.run_automated_trading()
            else:
                print("📊 Connection established. Ready for manual operations.")
        else:
            print("❌ IBKR connection failed. Check TWS/Gateway setup.")
    
    # Run the async main function
    asyncio.run(main())
