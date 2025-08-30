#!/usr/bin/env python3
"""
ENHANCED PORTFOLIO MANAGEMENT AGENT
Trading Firm Upgrade - Phase 3 Medium Priority
Advanced portfolio optimization and risk management
"""

import json
import os
import time
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from scipy import stats

@dataclass
class Portfolio:
    """Portfolio representation"""
    name: str
    assets: Dict[str, float]  # symbol: weight
    total_value: float
    cash: float
    risk_tolerance: float  # 0-1 scale
    target_return: float
    max_drawdown: float
    rebalance_frequency: str  # daily, weekly, monthly
    last_rebalance: datetime

@dataclass
class Asset:
    """Asset representation"""
    symbol: str
    name: str
    asset_class: str
    current_price: float
    volatility: float
    expected_return: float
    correlation_matrix: pd.DataFrame
    sector: str
    market_cap: float
    beta: float

@dataclass
class PortfolioOptimization:
    """Portfolio optimization result"""
    optimal_weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    max_drawdown: float
    var_95: float  # 95% Value at Risk
    cvar_95: float  # 95% Conditional Value at Risk
    diversification_ratio: float
    concentration_risk: float

class EnhancedPortfolioManagementAgent:
    def __init__(self):
        print("💼 ENHANCED PORTFOLIO MANAGEMENT AGENT - INITIALIZING...")
        print("🎯 Phase 3 Medium Priority: Portfolio optimization & risk management")
        
        # Portfolio configuration
        self.config = {
            'risk_free_rate': 0.02,  # 2% risk-free rate
            'max_position_size': 0.20,  # Maximum 20% in single asset
            'min_position_size': 0.01,  # Minimum 1% in single asset
            'target_correlation': 0.3,  # Target correlation between assets
            'rebalance_threshold': 0.05,  # 5% deviation triggers rebalance
            'max_drawdown_limit': 0.15,  # 15% maximum drawdown
            'var_confidence': 0.95,  # 95% VaR confidence level
        }
        
        # Portfolio storage
        self.portfolios = {}
        self.assets = {}
        self.asset_prices = {}
        self.correlation_matrix = pd.DataFrame()
        
        # Risk management
        self.risk_metrics = {}
        self.var_history = []
        self.drawdown_history = []
        
        # Performance tracking
        self.performance_history = []
        self.rebalance_history = []
        
        print("✅ Portfolio Management Agent initialized")
        print("💼 Portfolio optimization: ACTIVE")
        print("🛡️ Risk management: ACTIVE")
    
    async def run_portfolio_management_agent(self):
        """Run continuous portfolio management"""
        print("💼 STARTING ENHANCED PORTFOLIO MANAGEMENT...")
        print("🔄 Continuous portfolio optimization and risk monitoring")
        
        while True:
            try:
                print(f"\n💼 PORTFOLIO MANAGEMENT CYCLE - {datetime.now().strftime('%H:%M:%S')}")
                
                # 1. Update asset data
                await self.update_asset_data()
                
                # 2. Monitor portfolio performance
                await self.monitor_portfolios()
                
                # 3. Optimize portfolios
                await self.optimize_portfolios()
                
                # 4. Execute rebalancing
                await self.execute_rebalancing()
                
                # 5. Generate risk reports
                await self.generate_risk_reports()
                
                # Wait 4 hours between cycles
                print("⏳ Next portfolio management cycle in 4 hours...")
                await asyncio.sleep(14400)
                
            except KeyboardInterrupt:
                print("🛑 Portfolio Management Agent stopping...")
                break
            except Exception as e:
                print(f"⚠️ Portfolio management error: {e}")
                await asyncio.sleep(1800)
    
    async def update_asset_data(self):
        """Update asset prices and metrics"""
        print("📊 Updating asset data...")
        
        # Update asset prices (would integrate with market data agent)
        await self.fetch_asset_prices()
        
        # Update volatility and correlation estimates
        await self.update_risk_metrics()
        
        # Update expected returns
        await self.update_expected_returns()
        
        print("✅ Asset data updated")
    
    async def fetch_asset_prices(self):
        """Fetch current asset prices"""
        # This would integrate with the real-time market data agent
        # For now, simulate price updates
        
        symbols = ['BTC/USD', 'ETH/USD', 'AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'SPY', 'QQQ', 'GLD']
        
        for symbol in symbols:
            # Simulate price movement
            if symbol not in self.asset_prices:
                # Initialize with base price
                if 'BTC' in symbol:
                    base_price = 50000
                elif 'ETH' in symbol:
                    base_price = 3000
                elif symbol in ['AAPL', 'GOOGL', 'MSFT']:
                    base_price = 150
                elif symbol in ['TSLA', 'NVDA']:
                    base_price = 200
                else:  # ETFs
                    base_price = 400
                
                self.asset_prices[symbol] = base_price
            else:
                # Simulate price change
                current_price = self.asset_prices[symbol]
                change_pct = np.random.normal(0, 0.02)  # 2% daily volatility
                new_price = current_price * (1 + change_pct)
                self.asset_prices[symbol] = max(new_price, 0.01)
        
        print(f"✅ Updated prices for {len(symbols)} assets")
    
    async def update_risk_metrics(self):
        """Update volatility and correlation estimates"""
        print("📈 Updating risk metrics...")
        
        # Calculate rolling volatility (simplified)
        symbols = list(self.asset_prices.keys())
        
        # Generate correlation matrix
        n_assets = len(symbols)
        correlation_matrix = np.random.uniform(-0.3, 0.8, (n_assets, n_assets))
        
        # Ensure matrix is symmetric and diagonal is 1
        correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2
        np.fill_diagonal(correlation_matrix, 1.0)
        
        # Ensure positive definiteness
        min_eigenval = np.linalg.eigvals(correlation_matrix).min()
        if min_eigenval < 0:
            correlation_matrix += (-min_eigenval + 0.01) * np.eye(n_assets)
        
        self.correlation_matrix = pd.DataFrame(correlation_matrix, index=symbols, columns=symbols)
        
        # Update asset volatility estimates
        for symbol in symbols:
            if symbol not in self.assets:
                # Initialize asset
                asset_class = self.get_asset_class(symbol)
                sector = self.get_asset_sector(symbol)
                
                self.assets[symbol] = Asset(
                    symbol=symbol,
                    name=symbol,
                    asset_class=asset_class,
                    current_price=self.asset_prices[symbol],
                    volatility=np.random.uniform(0.15, 0.35),  # 15-35% annual volatility
                    expected_return=np.random.uniform(0.05, 0.20),  # 5-20% expected return
                    correlation_matrix=self.correlation_matrix,
                    sector=sector,
                    market_cap=np.random.uniform(1e9, 1e12),  # $1B to $1T
                    beta=np.random.uniform(0.5, 1.5)
                )
            else:
                # Update existing asset
                self.assets[symbol].current_price = self.asset_prices[symbol]
        
        print("✅ Risk metrics updated")
    
    def get_asset_class(self, symbol: str) -> str:
        """Get asset class for symbol"""
        if 'BTC' in symbol or 'ETH' in symbol:
            return 'cryptocurrency'
        elif symbol in ['GLD', 'SLV']:
            return 'commodity'
        elif symbol in ['SPY', 'QQQ']:
            return 'etf'
        else:
            return 'equity'
    
    def get_asset_sector(self, symbol: str) -> str:
        """Get sector for equity symbol"""
        if symbol in ['AAPL', 'GOOGL', 'MSFT', 'NVDA']:
            return 'technology'
        elif symbol == 'TSLA':
            return 'automotive'
        else:
            return 'general'
    
    async def update_expected_returns(self):
        """Update expected returns based on market conditions"""
        print("📊 Updating expected returns...")
        
        # Simple model: adjust returns based on market volatility
        market_volatility = np.mean([asset.volatility for asset in self.assets.values()])
        
        for symbol, asset in self.assets.items():
            # Adjust expected return based on volatility and market conditions
            base_return = asset.expected_return
            
            # Higher volatility might indicate higher expected returns (risk premium)
            volatility_adjustment = (market_volatility - 0.25) * 0.5  # 25% is baseline
            
            # Sector-specific adjustments
            sector_adjustment = 0.0
            if asset.sector == 'technology':
                sector_adjustment = 0.02  # Tech premium
            elif asset.asset_class == 'cryptocurrency':
                sector_adjustment = 0.05  # Crypto premium
            
            asset.expected_return = base_return + volatility_adjustment + sector_adjustment
            asset.expected_return = max(0.02, min(0.30, asset.expected_return))  # Clamp between 2-30%
        
        print("✅ Expected returns updated")
    
    async def monitor_portfolios(self):
        """Monitor portfolio performance and risk metrics"""
        print("📊 Monitoring portfolio performance...")
        
        for portfolio_name, portfolio in self.portfolios.items():
            try:
                # Calculate current portfolio value
                current_value = await self.calculate_portfolio_value(portfolio)
                
                # Update portfolio total value
                portfolio.total_value = current_value
                
                # Calculate risk metrics
                risk_metrics = await self.calculate_portfolio_risk(portfolio)
                self.risk_metrics[portfolio_name] = risk_metrics
                
                # Check risk limits
                await self.check_risk_limits(portfolio, risk_metrics)
                
                # Record performance
                self.record_portfolio_performance(portfolio_name, current_value, risk_metrics)
                
                print(f"✅ Monitored {portfolio_name}: ${current_value:,.0f}, Risk: {risk_metrics['var_95']:.2%}")
                
            except Exception as e:
                print(f"❌ Error monitoring {portfolio_name}: {e}")
    
    async def calculate_portfolio_value(self, portfolio: Portfolio) -> float:
        """Calculate current portfolio value"""
        total_value = portfolio.cash
        
        for symbol, weight in portfolio.assets.items():
            if symbol in self.asset_prices:
                asset_value = portfolio.total_value * weight * (self.asset_prices[symbol] / self.assets[symbol].current_price)
                total_value += asset_value
        
        return total_value
    
    async def calculate_portfolio_risk(self, portfolio: Portfolio) -> Dict:
        """Calculate comprehensive portfolio risk metrics"""
        symbols = list(portfolio.assets.keys())
        
        if not symbols:
            return {
                'volatility': 0.0,
                'var_95': 0.0,
                'cvar_95': 0.0,
                'max_drawdown': 0.0,
                'diversification_ratio': 0.0,
                'concentration_risk': 0.0
            }
        
        # Get weights and asset data
        weights = np.array([portfolio.assets[symbol] for symbol in symbols])
        
        # Calculate portfolio volatility
        volatility_matrix = np.diag([self.assets[symbol].volatility for symbol in symbols])
        correlation_subset = self.correlation_matrix.loc[symbols, symbols]
        
        portfolio_volatility = np.sqrt(weights.T @ volatility_matrix @ correlation_subset @ volatility_matrix @ weights)
        
        # Calculate Value at Risk (VaR)
        portfolio_return = np.sum(weights * [self.assets[symbol].expected_return for symbol in symbols])
        var_95 = portfolio_return - 1.645 * portfolio_volatility  # 95% confidence
        
        # Calculate Conditional Value at Risk (CVaR)
        cvar_95 = portfolio_return - 2.06 * portfolio_volatility  # 95% CVaR
        
        # Calculate diversification ratio
        individual_vol = np.sum(weights * [self.assets[symbol].volatility for symbol in symbols])
        diversification_ratio = individual_vol / portfolio_volatility if portfolio_volatility > 0 else 0
        
        # Calculate concentration risk (Herfindahl index)
        concentration_risk = np.sum(weights ** 2)
        
        return {
            'volatility': portfolio_volatility,
            'var_95': var_95,
            'cvar_95': cvar_95,
            'max_drawdown': 0.0,  # Would calculate from historical data
            'diversification_ratio': diversification_ratio,
            'concentration_risk': concentration_risk
        }
    
    async def check_risk_limits(self, portfolio: Portfolio, risk_metrics: Dict):
        """Check if portfolio exceeds risk limits"""
        violations = []
        
        # Check VaR limit
        if risk_metrics['var_95'] < -portfolio.max_drawdown:
            violations.append(f"VaR ({risk_metrics['var_95']:.2%}) exceeds drawdown limit ({portfolio.max_drawdown:.2%})")
        
        # Check concentration risk
        if risk_metrics['concentration_risk'] > 0.25:  # More than 25% concentration
            violations.append(f"High concentration risk: {risk_metrics['concentration_risk']:.2%}")
        
        # Check individual position sizes
        for symbol, weight in portfolio.assets.items():
            if weight > self.config['max_position_size']:
                violations.append(f"Position size too large: {symbol} ({weight:.2%})")
        
        if violations:
            print(f"⚠️ Risk limit violations for {portfolio.name}:")
            for violation in violations:
                print(f"  - {violation}")
            
            # Flag for rebalancing
            portfolio.last_rebalance = datetime.now() - timedelta(days=1)  # Force rebalancing
    
    def record_portfolio_performance(self, portfolio_name: str, value: float, risk_metrics: Dict):
        """Record portfolio performance metrics"""
        timestamp = datetime.now()
        
        performance_record = {
            'timestamp': timestamp,
            'portfolio': portfolio_name,
            'value': value,
            'volatility': risk_metrics['volatility'],
            'var_95': risk_metrics['var_95'],
            'cvar_95': risk_metrics['cvar_95'],
            'diversification_ratio': risk_metrics['diversification_ratio'],
            'concentration_risk': risk_metrics['concentration_risk']
        }
        
        self.performance_history.append(performance_record)
        
        # Keep only last 1000 records
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
    
    async def optimize_portfolios(self):
        """Optimize portfolio allocations"""
        print("🔧 Optimizing portfolio allocations...")
        
        for portfolio_name, portfolio in self.portfolios.items():
            try:
                print(f"🔧 Optimizing {portfolio_name}...")
                
                # Run portfolio optimization
                optimization = await self.optimize_portfolio(portfolio)
                
                # Check if rebalancing is needed
                if await self.needs_rebalancing(portfolio, optimization.optimal_weights):
                    print(f"🔄 {portfolio_name} needs rebalancing")
                    
                    # Store optimization result for rebalancing
                    portfolio.optimization_result = optimization
                
                print(f"✅ {portfolio_name} optimization complete")
                
            except Exception as e:
                print(f"❌ Error optimizing {portfolio_name}: {e}")
    
    async def optimize_portfolio(self, portfolio: Portfolio) -> PortfolioOptimization:
        """Optimize single portfolio using modern portfolio theory"""
        symbols = list(portfolio.assets.keys())
        
        if not symbols:
            return PortfolioOptimization(
                optimal_weights={},
                expected_return=0.0,
                expected_volatility=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0,
                var_95=0.0,
                cvar_95: 0.0,
                diversification_ratio=0.0,
                concentration_risk=0.0
            )
        
        # Get asset data
        returns = np.array([self.assets[symbol].expected_return for symbol in symbols])
        volatilities = np.array([self.assets[symbol].volatility for symbol in symbols])
        correlation_subset = self.correlation_matrix.loc[symbols, symbols]
        
        # Create covariance matrix
        covariance_matrix = np.outer(volatilities, volatilities) * correlation_subset
        
        # Define optimization constraints
        n_assets = len(symbols)
        
        # Weight bounds
        bounds = [(self.config['min_position_size'], self.config['max_position_size']) for _ in range(n_assets)]
        
        # Weight sum constraint
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}  # Weights sum to 1
        ]
        
        # Risk tolerance constraint
        if portfolio.risk_tolerance < 0.5:  # Conservative
            max_volatility = 0.15
        elif portfolio.risk_tolerance < 0.8:  # Moderate
            max_volatility = 0.25
        else:  # Aggressive
            max_volatility = 0.35
        
        constraints.append({
            'type': 'ineq',
            'fun': lambda x: max_volatility - np.sqrt(x.T @ covariance_matrix @ x)
        })
        
        # Initial weights (equal weight)
        initial_weights = np.ones(n_assets) / n_assets
        
        # Objective function: maximize Sharpe ratio
        def objective(weights):
            portfolio_return = np.sum(weights * returns)
            portfolio_vol = np.sqrt(weights.T @ covariance_matrix @ weights)
            
            if portfolio_vol == 0:
                return -float('inf')
            
            sharpe = (portfolio_return - self.config['risk_free_rate']) / portfolio_vol
            return -sharpe  # Minimize negative Sharpe ratio
        
        # Run optimization
        try:
            result = minimize(
                objective,
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints,
                options={'maxiter': 1000}
            )
            
            if result.success:
                optimal_weights = result.x
                
                # Calculate metrics
                portfolio_return = np.sum(optimal_weights * returns)
                portfolio_vol = np.sqrt(optimal_weights.T @ covariance_matrix @ optimal_weights)
                sharpe_ratio = (portfolio_return - self.config['risk_free_rate']) / portfolio_vol
                
                # Calculate VaR and CVaR
                var_95 = portfolio_return - 1.645 * portfolio_vol
                cvar_95 = portfolio_return - 2.06 * portfolio_vol
                
                # Calculate diversification metrics
                individual_vol = np.sum(optimal_weights * volatilities)
                diversification_ratio = individual_vol / portfolio_vol if portfolio_vol > 0 else 0
                concentration_risk = np.sum(optimal_weights ** 2)
                
                return PortfolioOptimization(
                    optimal_weights=dict(zip(symbols, optimal_weights)),
                    expected_return=portfolio_return,
                    expected_volatility=portfolio_vol,
                    sharpe_ratio=sharpe_ratio,
                    max_drawdown=0.0,  # Would calculate from historical data
                    var_95=var_95,
                    cvar_95=cvar_95,
                    diversification_ratio=diversification_ratio,
                    concentration_risk=concentration_risk
                )
            else:
                print(f"⚠️ Optimization failed for {portfolio.name}: {result.message}")
                return None
                
        except Exception as e:
            print(f"❌ Optimization error for {portfolio.name}: {e}")
            return None
    
    async def needs_rebalancing(self, portfolio: Portfolio, optimal_weights: Dict[str, float]) -> bool:
        """Check if portfolio needs rebalancing"""
        if not hasattr(portfolio, 'optimization_result'):
            return False
        
        # Check if enough time has passed since last rebalance
        days_since_rebalance = (datetime.now() - portfolio.last_rebalance).days
        
        if portfolio.rebalance_frequency == 'daily':
            min_days = 1
        elif portfolio.rebalance_frequency == 'weekly':
            min_days = 7
        elif portfolio.rebalance_frequency == 'monthly':
            min_days = 30
        else:
            min_days = 7
        
        if days_since_rebalance < min_days:
            return False
        
        # Check weight deviations
        for symbol, optimal_weight in optimal_weights.items():
            current_weight = portfolio.assets.get(symbol, 0.0)
            deviation = abs(current_weight - optimal_weight)
            
            if deviation > self.config['rebalance_threshold']:
                return True
        
        return False
    
    async def execute_rebalancing(self):
        """Execute portfolio rebalancing"""
        print("🔄 Executing portfolio rebalancing...")
        
        for portfolio_name, portfolio in self.portfolios.items():
            if hasattr(portfolio, 'optimization_result') and portfolio.optimization_result:
                try:
                    print(f"🔄 Rebalancing {portfolio_name}...")
                    
                    # Get optimal weights
                    optimal_weights = portfolio.optimization_result.optimal_weights
                    
                    # Calculate required trades
                    trades = await self.calculate_rebalancing_trades(portfolio, optimal_weights)
                    
                    # Execute trades (simulated)
                    await self.execute_trades(portfolio, trades)
                    
                    # Update portfolio
                    portfolio.assets = optimal_weights.copy()
                    portfolio.last_rebalance = datetime.now()
                    
                    # Record rebalancing
                    self.record_rebalancing(portfolio_name, trades)
                    
                    print(f"✅ {portfolio_name} rebalanced successfully")
                    
                except Exception as e:
                    print(f"❌ Error rebalancing {portfolio_name}: {e}")
    
    async def calculate_rebalancing_trades(self, portfolio: Portfolio, optimal_weights: Dict[str, float]) -> List[Dict]:
        """Calculate required trades for rebalancing"""
        trades = []
        
        # Get current portfolio value
        current_value = await self.calculate_portfolio_value(portfolio)
        
        for symbol, target_weight in optimal_weights.items():
            current_weight = portfolio.assets.get(symbol, 0.0)
            current_price = self.asset_prices.get(symbol, 0.0)
            
            if current_price > 0:
                # Calculate required position value
                target_value = current_value * target_weight
                current_value_asset = current_value * current_weight
                
                # Calculate trade size
                trade_value = target_value - current_value_asset
                
                if abs(trade_value) > current_value * 0.001:  # Minimum trade size
                    trade = {
                        'symbol': symbol,
                        'action': 'buy' if trade_value > 0 else 'sell',
                        'value': abs(trade_value),
                        'shares': abs(trade_value) / current_price,
                        'price': current_price,
                        'timestamp': datetime.now()
                    }
                    trades.append(trade)
        
        return trades
    
    async def execute_trades(self, portfolio: Portfolio, trades: List[Dict]):
        """Execute rebalancing trades (simulated)"""
        total_cost = 0.0
        
        for trade in trades:
            # Simulate trade execution
            trade_cost = trade['value'] * 0.001  # 0.1% commission
            total_cost += trade_cost
            
            print(f"  📊 {trade['action'].upper()} {trade['shares']:.2f} {trade['symbol']} @ ${trade['price']:.2f}")
        
        # Update cash
        portfolio.cash -= total_cost
        
        print(f"  💰 Total rebalancing cost: ${total_cost:.2f}")
    
    def record_rebalancing(self, portfolio_name: str, trades: List[Dict]):
        """Record rebalancing activity"""
        rebalancing_record = {
            'timestamp': datetime.now(),
            'portfolio': portfolio_name,
            'trades_count': len(trades),
            'total_value': sum(trade['value'] for trade in trades),
            'trades': trades
        }
        
        self.rebalance_history.append(rebalancing_record)
        
        # Keep only last 100 rebalancing records
        if len(self.rebalance_history) > 100:
            self.rebalance_history = self.rebalance_history[-100:]
    
    async def generate_risk_reports(self):
        """Generate comprehensive risk reports"""
        print("📊 Generating risk reports...")
        
        # Portfolio summary report
        summary_data = []
        for portfolio_name, portfolio in self.portfolios.items():
            risk_metrics = self.risk_metrics.get(portfolio_name, {})
            
            summary_data.append({
                'Portfolio': portfolio_name,
                'Total Value': f"${portfolio.total_value:,.0f}",
                'Cash': f"${portfolio.cash:,.0f}",
                'Volatility': f"{risk_metrics.get('volatility', 0):.2%}",
                'VaR (95%)': f"{risk_metrics.get('var_95', 0):.2%}",
                'CVaR (95%)': f"{risk_metrics.get('cvar_95', 0):.2%}",
                'Diversification': f"{risk_metrics.get('diversification_ratio', 0):.2f}",
                'Concentration': f"{risk_metrics.get('concentration_risk', 0):.2%}"
            })
        
        # Save summary report
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            summary_filename = f"portfolio_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            summary_df.to_csv(summary_filename, index=False)
            print(f"✅ Portfolio summary saved: {summary_filename}")
        
        # Generate risk charts
        await self.generate_risk_charts()
        
        print("✅ Risk reports generated")
    
    async def generate_risk_charts(self):
        """Generate risk visualization charts"""
        print("📈 Generating risk charts...")
        
        try:
            if not self.portfolios:
                print("⚠️ No portfolios to chart")
                return
            
            # Set style
            plt.style.use('seaborn-v0_8')
            
            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Portfolio Risk Analysis', fontsize=16)
            
            # 1. Portfolio values over time
            ax1 = axes[0, 0]
            for portfolio_name in self.portfolios.keys():
                portfolio_data = [record for record in self.performance_history if record['portfolio'] == portfolio_name]
                if portfolio_data:
                    values = [record['value'] for record in portfolio_data]
                    timestamps = [record['timestamp'] for record in portfolio_data]
                    ax1.plot(timestamps, values, label=portfolio_name, linewidth=2)
            
            ax1.set_title('Portfolio Values Over Time')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Portfolio Value ($)')
            ax1.legend()
            ax1.grid(True)
            
            # 2. Risk metrics comparison
            ax2 = axes[0, 1]
            portfolio_names = list(self.portfolios.keys())
            var_values = [self.risk_metrics.get(name, {}).get('var_95', 0) for name in portfolio_names]
            
            bars = ax2.bar(portfolio_names, var_values, alpha=0.7)
            ax2.set_title('Value at Risk (95%) Comparison')
            ax2.set_ylabel('VaR (95%)')
            ax2.grid(True, axis='y')
            
            # Add value labels on bars
            for bar, value in zip(bars, var_values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.2%}', ha='center', va='bottom')
            
            # 3. Diversification analysis
            ax3 = axes[1, 0]
            div_ratios = [self.risk_metrics.get(name, {}).get('diversification_ratio', 0) for name in portfolio_names]
            
            ax3.bar(portfolio_names, div_ratios, alpha=0.7, color='green')
            ax3.set_title('Portfolio Diversification')
            ax3.set_ylabel('Diversification Ratio')
            ax3.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='No Diversification')
            ax3.legend()
            ax3.grid(True, axis='y')
            
            # 4. Risk-return scatter
            ax4 = axes[1, 1]
            returns = []
            volatilities = []
            
            for portfolio_name in portfolio_names:
                risk_metrics = self.risk_metrics.get(portfolio_name, {})
                if 'volatility' in risk_metrics:
                    volatilities.append(risk_metrics['volatility'])
                    # Calculate return from performance history
                    portfolio_data = [record for record in self.performance_history if record['portfolio'] == portfolio_name]
                    if len(portfolio_data) > 1:
                        initial_value = portfolio_data[0]['value']
                        final_value = portfolio_data[-1]['value']
                        total_return = (final_value - initial_value) / initial_value
                        returns.append(total_return)
                    else:
                        returns.append(0.0)
                else:
                    volatilities.append(0.0)
                    returns.append(0.0)
            
            ax4.scatter(volatilities, returns, s=100, alpha=0.7)
            for i, name in enumerate(portfolio_names):
                ax4.annotate(name, (volatilities[i], returns[i]), xytext=(5, 5), textcoords='offset points')
            
            ax4.set_title('Risk-Return Profile')
            ax4.set_xlabel('Volatility')
            ax4.set_ylabel('Total Return')
            ax4.grid(True)
            
            # Adjust layout and save
            plt.tight_layout()
            chart_filename = f"portfolio_risk_charts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✅ Risk charts saved: {chart_filename}")
            
        except Exception as e:
            print(f"❌ Error generating charts: {e}")
    
    def create_sample_portfolio(self, name: str, risk_tolerance: float = 0.5) -> Portfolio:
        """Create a sample portfolio for testing"""
        # Create sample assets if none exist
        if not self.assets:
            sample_symbols = ['BTC/USD', 'ETH/USD', 'AAPL', 'GOOGL', 'SPY', 'GLD']
            for symbol in sample_symbols:
                self.assets[symbol] = Asset(
                    symbol=symbol,
                    name=symbol,
                    asset_class=self.get_asset_class(symbol),
                    current_price=50000 if 'BTC' in symbol else 3000 if 'ETH' in symbol else 150,
                    volatility=np.random.uniform(0.15, 0.35),
                    expected_return=np.random.uniform(0.05, 0.20),
                    correlation_matrix=pd.DataFrame(),
                    sector=self.get_asset_sector(symbol),
                    market_cap=np.random.uniform(1e9, 1e12),
                    beta=np.random.uniform(0.5, 1.5)
                )
        
        # Create portfolio with equal weights
        symbols = list(self.assets.keys())[:6]  # Use first 6 assets
        equal_weight = 1.0 / len(symbols)
        assets = {symbol: equal_weight for symbol in symbols}
        
        portfolio = Portfolio(
            name=name,
            assets=assets,
            total_value=100000,  # $100k starting value
            cash=10000,  # $10k cash
            risk_tolerance=risk_tolerance,
            target_return=0.10,  # 10% target return
            max_drawdown=0.15,  # 15% max drawdown
            rebalance_frequency='weekly',
            last_rebalance=datetime.now() - timedelta(days=8)  # Force rebalancing
        )
        
        self.portfolios[name] = portfolio
        return portfolio
    
    def get_portfolio_summary(self) -> Dict:
        """Get summary of all portfolios"""
        summary = {}
        
        for name, portfolio in self.portfolios.items():
            risk_metrics = self.risk_metrics.get(name, {})
            
            summary[name] = {
                'total_value': portfolio.total_value,
                'cash': portfolio.cash,
                'risk_tolerance': portfolio.risk_tolerance,
                'target_return': portfolio.target_return,
                'max_drawdown': portfolio.max_drawdown,
                'rebalance_frequency': portfolio.rebalance_frequency,
                'last_rebalance': portfolio.last_rebalance,
                'risk_metrics': risk_metrics
            }
        
        return summary
    
    def get_rebalancing_history(self) -> List[Dict]:
        """Get rebalancing history"""
        return self.rebalance_history.copy()
    
    def get_performance_history(self) -> List[Dict]:
        """Get performance history"""
        return self.performance_history.copy()

async def main():
    """Main function to run the portfolio management agent"""
    agent = EnhancedPortfolioManagementAgent()
    
    # Create sample portfolios for testing
    agent.create_sample_portfolio("Conservative Portfolio", risk_tolerance=0.3)
    agent.create_sample_portfolio("Balanced Portfolio", risk_tolerance=0.6)
    agent.create_sample_portfolio("Aggressive Portfolio", risk_tolerance=0.8)
    
    try:
        await agent.run_portfolio_management_agent()
    except KeyboardInterrupt:
        print("\n🛑 Portfolio Management Agent stopped by user")
    except Exception as e:
        print(f"❌ Portfolio Management Agent error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
