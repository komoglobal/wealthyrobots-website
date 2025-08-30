#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: Advanced Backtesting Agent
PURPOSE: Strategy validation, optimization, and historical performance analysis
CATEGORY: Trading & Strategy Analysis
STATUS: Active - New
FREQUENCY: On-demand
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Trade:
    """Individual trade record"""
    symbol: str
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    shares: int
    side: str  # 'long' or 'short'
    pnl: float
    commission: float
    slippage: float
    strategy: str
    confidence: float

@dataclass
class BacktestResult:
    """Complete backtest results"""
    strategy_name: str
    start_date: datetime
    end_date: datetime
    total_return: float
    annualized_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    average_win: float
    average_loss: float
    max_consecutive_losses: int
    trades: List[Trade]
    equity_curve: pd.Series
    drawdown_curve: pd.Series

class AdvancedBacktestingAgent:
    """Advanced backtesting and strategy optimization agent"""
    
    def __init__(self):
        self.agent_name = "Advanced Backtesting Agent"
        self.version = "1.0 - Strategy Validation & Optimization"
        
        # Backtesting parameters
        self.initial_capital = 100000  # $100k starting capital
        self.commission_rate = 0.005   # 0.5% commission
        self.slippage_rate = 0.001     # 0.1% slippage
        self.risk_free_rate = 0.02     # 2% risk-free rate
        
        # Strategy parameters
        self.strategies = {
            'momentum': {
                'lookback_period': 20,
                'threshold': 0.02,
                'position_size': 0.1
            },
            'mean_reversion': {
                'lookback_period': 50,
                'std_threshold': 2.0,
                'position_size': 0.15
            },
            'breakout': {
                'breakout_period': 20,
                'volume_multiplier': 1.5,
                'position_size': 0.12
            },
            'dual_moving_average': {
                'fast_period': 10,
                'slow_period': 30,
                'position_size': 0.08
            }
        }
        
        # Historical data storage
        self.historical_data = {}
        self.risk_metrics = {}
        
        print(f"📊 {self.agent_name} v{self.version} initialized")
        print("🔍 Ready for strategy validation and optimization")
        
    def load_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Load historical price data for backtesting"""
        print(f"📥 Loading historical data for {symbol}...")
        
        # Try to load from existing files first
        data_file = f"historical_data_{symbol}.csv"
        if os.path.exists(data_file):
            df = pd.read_csv(data_file, index_col=0, parse_dates=True)
            print(f"✅ Loaded {len(df)} data points from {data_file}")
            return df
        
        # Generate synthetic data for demonstration
        print("⚠️ No historical data found, generating synthetic data...")
        df = self._generate_synthetic_data(symbol, start_date, end_date)
        
        # Save for future use
        df.to_csv(data_file)
        print(f"💾 Saved synthetic data to {data_file}")
        
        return df
    
    def _generate_synthetic_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Generate realistic synthetic price data for backtesting"""
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        # Generate daily timestamps
        dates = pd.date_range(start=start, end=end, freq='D')
        
        # Start with a base price
        base_price = 100.0
        
        # Generate price movements with realistic volatility
        np.random.seed(42)  # For reproducible results
        
        # Daily returns with trend and volatility
        daily_returns = np.random.normal(0.0005, 0.02, len(dates))  # 0.05% daily drift, 2% volatility
        
        # Add some trend
        trend = np.linspace(0, 0.1, len(dates))  # 10% upward trend over period
        daily_returns += trend / len(dates)
        
        # Generate prices
        prices = [base_price]
        for ret in daily_returns[1:]:
            new_price = prices[-1] * (1 + ret)
            prices.append(new_price)
        
        # Generate volume data
        base_volume = 1000000
        volumes = np.random.lognormal(np.log(base_volume), 0.5, len(dates))
        
        # Create DataFrame
        df = pd.DataFrame({
            'open': prices,
            'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'close': prices,
            'volume': volumes
        }, index=dates)
        
        # Ensure high >= close >= low
        df['high'] = df[['open', 'close', 'high']].max(axis=1)
        df['low'] = df[['open', 'close', 'low']].min(axis=1)
        
        return df
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for strategy signals"""
        df = df.copy()
        
        # Moving averages
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # Exponential moving averages
        df['ema_10'] = df['close'].ewm(span=10).mean()
        df['ema_30'] = df['close'].ewm(span=30).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Volume indicators
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        return df
    
    def generate_signals(self, df: pd.DataFrame, strategy: str) -> pd.DataFrame:
        """Generate trading signals based on strategy"""
        df = df.copy()
        df['signal'] = 0  # 0: hold, 1: buy, -1: sell
        
        if strategy == 'momentum':
            # Momentum strategy: buy when price > SMA20 + threshold
            threshold = self.strategies['momentum']['threshold']
            df['signal'] = np.where(
                df['close'] > df['sma_20'] * (1 + threshold), 1, 0
            )
            df['signal'] = np.where(
                df['close'] < df['sma_20'] * (1 - threshold), -1, df['signal']
            )
            
        elif strategy == 'mean_reversion':
            # Mean reversion: buy when price < BB_lower, sell when > BB_upper
            std_threshold = self.strategies['mean_reversion']['std_threshold']
            df['signal'] = np.where(
                df['close'] < df['bb_lower'], 1, 0
            )
            df['signal'] = np.where(
                df['close'] > df['bb_upper'], -1, df['signal']
            )
            
        elif strategy == 'breakout':
            # Breakout: buy when price breaks above recent high with volume
            breakout_period = self.strategies['breakout']['breakout_period']
            volume_mult = self.strategies['breakout']['volume_multiplier']
            
            df['recent_high'] = df['high'].rolling(window=breakout_period).max()
            df['signal'] = np.where(
                (df['close'] > df['recent_high'].shift(1)) & 
                (df['volume'] > df['volume_sma'] * volume_mult), 1, 0
            )
            
        elif strategy == 'dual_moving_average':
            # Dual MA crossover
            fast_period = self.strategies['dual_moving_average']['fast_period']
            slow_period = self.strategies['dual_moving_average']['slow_period']
            
            df['sma_fast'] = df['close'].rolling(window=fast_period).mean()
            df['sma_slow'] = df['close'].rolling(window=slow_period).mean()
            
            df['signal'] = np.where(
                df['sma_fast'] > df['sma_slow'], 1, 0
            )
            df['signal'] = np.where(
                df['sma_fast'] < df['sma_slow'], -1, df['signal']
            )
        
        return df
    
    def execute_backtest(self, symbol: str, strategy: str, start_date: str, end_date: str) -> BacktestResult:
        """Execute complete backtest for a strategy"""
        print(f"🚀 Executing {strategy} backtest for {symbol}...")
        
        # Load and prepare data
        df = self.load_historical_data(symbol, start_date, end_date)
        df = self.calculate_technical_indicators(df)
        df = self.generate_signals(df, strategy)
        
        # Initialize backtest variables
        capital = self.initial_capital
        position = 0
        trades = []
        equity_curve = []
        drawdown_curve = []
        
        peak_capital = capital
        max_drawdown = 0
        
        # Execute backtest
        for i in range(1, len(df)):
            current_price = df['close'].iloc[i]
            signal = df['signal'].iloc[i]
            current_date = df.index[i]
            
            # Execute trades based on signals
            if signal == 1 and position == 0:  # Buy signal
                # Calculate position size
                position_size = self.strategies[strategy]['position_size']
                shares = int((capital * position_size) / current_price)
                
                if shares > 0:
                    # Calculate costs
                    commission = shares * current_price * self.commission_rate
                    slippage = shares * current_price * self.slippage_rate
                    total_cost = shares * current_price + commission + slippage
                    
                    if total_cost <= capital:
                        position = shares
                        capital -= total_cost
                        
                        # Record trade
                        trade = Trade(
                            symbol=symbol,
                            entry_time=current_date,
                            exit_time=None,
                            entry_price=current_price,
                            exit_price=None,
                            shares=shares,
                            side='long',
                            pnl=0,
                            commission=commission,
                            slippage=slippage,
                            strategy=strategy,
                            confidence=0.8
                        )
                        trades.append(trade)
                        
            elif signal == -1 and position > 0:  # Sell signal
                # Calculate proceeds
                commission = position * current_price * self.commission_rate
                slippage = position * current_price * self.slippage_rate
                total_proceeds = position * current_price - commission - slippage
                
                # Update capital
                capital += total_proceeds
                
                # Calculate P&L
                entry_price = trades[-1].entry_price
                pnl = (current_price - entry_price) * position - trades[-1].commission - commission
                
                # Update trade record
                trades[-1].exit_time = current_date
                trades[-1].exit_price = current_price
                trades[-1].pnl = pnl
                
                position = 0
            
            # Calculate current equity
            current_equity = capital + (position * current_price)
            equity_curve.append(current_equity)
            
            # Update peak and drawdown
            if current_equity > peak_capital:
                peak_capital = current_equity
            
            current_drawdown = (peak_capital - current_equity) / peak_capital
            drawdown_curve.append(current_drawdown)
            
            if current_drawdown > max_drawdown:
                max_drawdown = current_drawdown
        
        # Close any remaining position
        if position > 0:
            final_price = df['close'].iloc[-1]
            commission = position * final_price * self.commission_rate
            slippage = position * final_price * self.slippage_rate
            total_proceeds = position * final_price - commission - slippage
            capital += total_proceeds
            
            # Update final trade
            if trades:
                trades[-1].exit_time = df.index[-1]
                trades[-1].exit_price = final_price
                trades[-1].pnl = (final_price - trades[-1].entry_price) * position - trades[-1].commission - commission
        
        # Calculate final metrics
        final_equity = capital
        total_return = (final_equity - self.initial_capital) / self.initial_capital
        
        # Calculate annualized return
        days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
        annualized_return = ((1 + total_return) ** (365 / days)) - 1 if days > 0 else 0
        
        # Calculate Sharpe ratio
        returns = pd.Series(equity_curve).pct_change().dropna()
        sharpe_ratio = (returns.mean() - self.risk_free_rate/365) / returns.std() * np.sqrt(365) if returns.std() > 0 else 0
        
        # Calculate win rate and profit factor
        winning_trades = [t for t in trades if t.pnl > 0]
        losing_trades = [t for t in trades if t.pnl < 0]
        
        win_rate = len(winning_trades) / len(trades) if trades else 0
        total_wins = sum(t.pnl for t in winning_trades)
        total_losses = abs(sum(t.pnl for t in losing_trades))
        profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
        
        # Calculate average win/loss
        average_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        average_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0
        
        # Calculate max consecutive losses
        consecutive_losses = 0
        max_consecutive_losses = 0
        for trade in trades:
            if trade.pnl < 0:
                consecutive_losses += 1
                max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
            else:
                consecutive_losses = 0
        
        # Create result object
        result = BacktestResult(
            strategy_name=strategy,
            start_date=pd.to_datetime(start_date),
            end_date=pd.to_datetime(end_date),
            total_return=total_return,
            annualized_return=annualized_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            average_win=average_win,
            average_loss=average_loss,
            max_consecutive_losses=max_consecutive_losses,
            trades=trades,
            equity_curve=pd.Series(equity_curve, index=df.index[1:]),
            drawdown_curve=pd.Series(drawdown_curve, index=df.index[1:])
        )
        
        return result
    
    def optimize_strategy_parameters(self, symbol: str, strategy: str, start_date: str, end_date: str) -> Dict:
        """Optimize strategy parameters using grid search"""
        print(f"🔧 Optimizing {strategy} parameters for {symbol}...")
        
        # Define parameter ranges for optimization
        param_ranges = {
            'momentum': {
                'lookback_period': range(10, 51, 5),
                'threshold': [0.01, 0.015, 0.02, 0.025, 0.03],
                'position_size': [0.05, 0.1, 0.15, 0.2]
            },
            'mean_reversion': {
                'lookback_period': range(20, 101, 10),
                'std_threshold': [1.5, 1.8, 2.0, 2.2, 2.5],
                'position_size': [0.1, 0.15, 0.2, 0.25]
            },
            'breakout': {
                'breakout_period': range(10, 31, 5),
                'volume_multiplier': [1.2, 1.5, 1.8, 2.0, 2.5],
                'position_size': [0.08, 0.12, 0.15, 0.18]
            },
            'dual_moving_average': {
                'fast_period': range(5, 21, 2),
                'slow_period': range(20, 61, 5),
                'position_size': [0.05, 0.08, 0.1, 0.12, 0.15]
            }
        }
        
        if strategy not in param_ranges:
            print(f"❌ Strategy {strategy} not supported for optimization")
            return {}
        
        # Grid search
        best_params = {}
        best_sharpe = -float('inf')
        optimization_results = []
        
        # Generate all parameter combinations
        import itertools
        param_names = list(param_ranges[strategy].keys())
        param_values = list(param_ranges[strategy].values())
        
        total_combinations = np.prod([len(v) for v in param_values])
        print(f"🔍 Testing {total_combinations} parameter combinations...")
        
        for i, param_combo in enumerate(itertools.product(*param_values)):
            # Update strategy parameters
            for j, param_name in enumerate(param_names):
                self.strategies[strategy][param_name] = param_combo[j]
            
            # Run backtest with current parameters
            try:
                result = self.execute_backtest(symbol, strategy, start_date, end_date)
                
                optimization_results.append({
                    'parameters': dict(zip(param_names, param_combo)),
                    'sharpe_ratio': result.sharpe_ratio,
                    'total_return': result.total_return,
                    'max_drawdown': result.max_drawdown,
                    'win_rate': result.win_rate
                })
                
                # Update best parameters
                if result.sharpe_ratio > best_sharpe:
                    best_sharpe = result.sharpe_ratio
                    best_params = dict(zip(param_names, param_combo))
                
                if (i + 1) % 100 == 0:
                    print(f"   Progress: {i + 1}/{total_combinations} combinations tested")
                    
            except Exception as e:
                print(f"⚠️ Error testing parameters {param_combo}: {str(e)}")
                continue
        
        # Sort results by Sharpe ratio
        optimization_results.sort(key=lambda x: x['sharpe_ratio'], reverse=True)
        
        # Save optimization results
        optimization_file = f"optimization_results_{strategy}_{symbol}.json"
        with open(optimization_file, 'w') as f:
            json.dump({
                'strategy': strategy,
                'symbol': symbol,
                'best_parameters': best_params,
                'best_sharpe_ratio': best_sharpe,
                'top_10_results': optimization_results[:10],
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"✅ Optimization complete! Best Sharpe ratio: {best_sharpe:.3f}")
        print(f"💾 Results saved to {optimization_file}")
        
        return {
            'best_parameters': best_params,
            'best_sharpe_ratio': best_sharpe,
            'top_results': optimization_results[:10]
        }
    
    def generate_backtest_report(self, result: BacktestResult, save_path: str = None) -> str:
        """Generate comprehensive backtest report"""
        print(f"📊 Generating backtest report for {result.strategy_name}...")
        
        report = f"""
# BACKTEST REPORT: {result.strategy_name.upper()}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 PERFORMANCE SUMMARY
- **Strategy**: {result.strategy_name}
- **Period**: {result.start_date.strftime('%Y-%m-%d')} to {result.end_date.strftime('%Y-%m-%d')}
- **Initial Capital**: ${self.initial_capital:,.2f}
- **Final Capital**: ${self.initial_capital * (1 + result.total_return):,.2f}

## 🎯 KEY METRICS
- **Total Return**: {result.total_return:.2%}
- **Annualized Return**: {result.annualized_return:.2%}
- **Sharpe Ratio**: {result.sharpe_ratio:.3f}
- **Maximum Drawdown**: {result.max_drawdown:.2%}
- **Win Rate**: {result.win_rate:.2%}
- **Profit Factor**: {result.profit_factor:.2f}

## 📊 TRADE ANALYSIS
- **Total Trades**: {result.total_trades}
- **Winning Trades**: {result.winning_trades}
- **Losing Trades**: {result.losing_trades}
- **Average Win**: ${result.average_win:.2f}
- **Average Loss**: ${result.average_loss:.2f}
- **Max Consecutive Losses**: {result.max_consecutive_losses}

## 💰 RISK METRICS
- **Risk-Adjusted Return**: {result.sharpe_ratio:.3f}
- **Downside Deviation**: {result.max_drawdown:.2%}
- **Recovery Factor**: {(result.total_return / result.max_drawdown) if result.max_drawdown > 0 else float('inf'):.2f}

## 🔍 STRATEGY INSIGHTS
"""
        
        # Add strategy-specific insights
        if result.strategy_name == 'momentum':
            report += """
**Momentum Strategy Analysis:**
- This strategy captures trending moves in the market
- Performance is highly dependent on market conditions
- Consider adjusting lookback period based on market volatility
"""
        elif result.strategy_name == 'mean_reversion':
            report += """
**Mean Reversion Strategy Analysis:**
- Works well in sideways markets
- May underperform in strong trending markets
- Risk management is crucial due to potential large moves
"""
        
        # Add recommendations
        report += f"""
## 🚀 RECOMMENDATIONS
"""
        
        if result.sharpe_ratio < 0.5:
            report += "- **Low Sharpe ratio suggests poor risk-adjusted returns**
- Consider parameter optimization or strategy modification
- Review risk management rules
"
        
        if result.max_drawdown > 0.2:
            report += "- **High maximum drawdown indicates significant risk**
- Implement tighter stop-losses
- Consider position sizing adjustments
"
        
        if result.win_rate < 0.4:
            report += "- **Low win rate suggests poor signal quality**
- Review entry/exit criteria
- Consider additional filters or confirmation signals
"
        
        if result.profit_factor < 1.5:
            report += "- **Low profit factor indicates poor risk/reward**
- Focus on improving exit strategies
- Consider trailing stops or profit targets
"
        
        # Save report
        if save_path is None:
            save_path = f"backtest_report_{result.strategy_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(save_path, 'w') as f:
            f.write(report)
        
        print(f"💾 Report saved to {save_path}")
        return save_path
    
    def run_agent(self):
        """Main agent execution"""
        print(f"🤖 {self.agent_name} running...")
        
        # Example usage
        symbol = "AAPL"
        strategy = "momentum"
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        
        print(f"\n📊 Running example backtest: {strategy} strategy on {symbol}")
        
        # Execute backtest
        result = self.execute_backtest(symbol, strategy, start_date, end_date)
        
        # Generate report
        report_path = self.generate_backtest_report(result)
        
        # Optimize parameters
        print(f"\n🔧 Optimizing {strategy} parameters...")
        optimization = self.optimize_strategy_parameters(symbol, strategy, start_date, end_date)
        
        print(f"\n✅ {self.agent_name} completed successfully!")
        print(f"📊 Backtest report: {report_path}")
        print(f"🔧 Best parameters: {optimization.get('best_parameters', {})}")

def main():
    """Test the advanced backtesting agent"""
    agent = AdvancedBacktestingAgent()
    agent.run_agent()

if __name__ == "__main__":
    main()
