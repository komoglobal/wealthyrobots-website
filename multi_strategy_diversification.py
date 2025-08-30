#!/usr/bin/env python3
"""
Multi-Strategy Diversification System
Enhanced version with lower confidence thresholds and aggressive diversification
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import random

class MultiStrategyDiversification:
    def __init__(self):
        print("🚀 MULTI-STRATEGY DIVERSIFICATION - ENHANCED")
        self.strategies = {
            'momentum': {'enabled': True, 'confidence_threshold': 0.3},  # Lowered from 0.5
            'mean_reversion': {'enabled': True, 'confidence_threshold': 0.25},  # Lowered from 0.4
            'statistical_arbitrage': {'enabled': True, 'confidence_threshold': 0.4},  # Lowered from 0.95
            'pairs_trading': {'enabled': True, 'confidence_threshold': 0.35},  # Lowered from 0.6
            'trend_following': {'enabled': True, 'confidence_threshold': 0.3},  # New strategy
            'volatility_breakout': {'enabled': True, 'confidence_threshold': 0.25},  # New strategy
            'sector_rotation': {'enabled': True, 'confidence_threshold': 0.3},  # New strategy
            'correlation_arbitrage': {'enabled': True, 'confidence_threshold': 0.35}  # New strategy
        }
        
        # Enhanced position sizing
        self.position_sizing = {
            'base_size': 0.1,  # 10% base position
            'max_size': 0.25,  # 25% max position
            'scaling_factor': 1.5  # Aggressive scaling
        }
        
        # Market data simulation
        self.market_data = self.generate_market_data()
        
    def generate_market_data(self):
        """Generate realistic market data for testing"""
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2025-08-09', freq='D')
        
        # Generate multiple asset prices with correlations
        n_assets = 8
        n_days = len(dates)
        
        # Base returns with trend and volatility
        base_returns = np.random.normal(0.0005, 0.02, (n_days, n_assets))
        
        # Add trends
        trends = np.linspace(0, 0.1, n_days).reshape(-1, 1)
        base_returns += trends
        
        # Add correlations between assets
        correlation_matrix = np.array([
            [1.0, 0.7, 0.5, 0.3, 0.2, 0.1, 0.1, 0.1],
            [0.7, 1.0, 0.6, 0.4, 0.3, 0.2, 0.2, 0.1],
            [0.5, 0.6, 1.0, 0.7, 0.5, 0.4, 0.3, 0.2],
            [0.3, 0.4, 0.7, 1.0, 0.6, 0.5, 0.4, 0.3],
            [0.2, 0.3, 0.5, 0.6, 1.0, 0.7, 0.6, 0.5],
            [0.1, 0.2, 0.4, 0.5, 0.7, 1.0, 0.8, 0.6],
            [0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 0.7],
            [0.1, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 1.0]
        ])
        
        # Apply correlations
        correlated_returns = np.dot(base_returns, np.linalg.cholesky(correlation_matrix).T)
        
        # Convert to prices
        prices = 100 * np.exp(np.cumsum(correlated_returns, axis=0))
        
        return {
            'dates': dates,
            'prices': prices,
            'returns': correlated_returns,
            'assets': [f'ASSET_{i+1}' for i in range(n_assets)]
        }
    
    def run_momentum_strategy(self):
        """Enhanced momentum strategy with lower thresholds"""
        try:
            prices = self.market_data['prices']
            returns = self.market_data['returns']
            
            # Calculate momentum indicators
            short_momentum = np.mean(returns[-5:], axis=0)  # 5-day momentum
            long_momentum = np.mean(returns[-20:], axis=0)  # 20-day momentum
            momentum_strength = short_momentum - long_momentum
            
            # Volatility adjustment
            volatility = np.std(returns[-20:], axis=0)
            volatility_filter = volatility > np.percentile(volatility, 30)  # Lower threshold
            
            # Generate signals
            signals = []
            for i in range(len(momentum_strength)):
                if momentum_strength[i] > 0.01 and volatility_filter[i]:  # Lower threshold
                    confidence = min(0.8, abs(momentum_strength[i]) * 10)
                    if confidence >= self.strategies['momentum']['confidence_threshold']:
                        position_size = min(
                            self.position_sizing['max_size'],
                            self.position_sizing['base_size'] * confidence * self.position_sizing['scaling_factor']
                        )
                        signals.append({
                            'asset': self.market_data['assets'][i],
                            'signal': 'buy',
                            'confidence': confidence,
                            'position_size': position_size,
                            'strategy': 'momentum',
                            'momentum': momentum_strength[i],
                            'volatility': volatility[i]
                        })
            
            return signals
            
        except Exception as e:
            print(f"Momentum strategy error: {e}")
            return []
    
    def run_mean_reversion_strategy(self):
        """Enhanced mean reversion with lower thresholds"""
        try:
            prices = self.market_data['prices']
            returns = self.market_data['returns']
            
            # Calculate z-scores
            lookback = 20
            if len(returns) < lookback:
                return []
            
            z_scores = []
            for i in range(len(returns[0])):
                asset_returns = returns[:, i]
                if len(asset_returns) >= lookback:
                    mean_return = np.mean(asset_returns[-lookback:])
                    std_return = np.std(asset_returns[-lookback:])
                    if std_return > 0:
                        z_score = (asset_returns[-1] - mean_return) / std_return
                        z_scores.append((i, z_score))
            
            # Generate signals
            signals = []
            for asset_idx, z_score in z_scores:
                if abs(z_score) > 1.5:  # Lower threshold from 2.0
                    confidence = min(0.8, abs(z_score) / 3.0)
                    if confidence >= self.strategies['mean_reversion']['confidence_threshold']:
                        signal = 'sell' if z_score > 0 else 'buy'
                        position_size = min(
                            self.position_sizing['max_size'],
                            self.position_sizing['base_size'] * confidence * self.position_sizing['scaling_factor']
                        )
                        signals.append({
                            'asset': self.market_data['assets'][asset_idx],
                            'signal': signal,
                            'confidence': confidence,
                            'position_size': position_size,
                            'strategy': 'mean_reversion',
                            'z_score': z_score
                        })
            
            return signals
            
        except Exception as e:
            print(f"Mean reversion strategy error: {e}")
            return []
    
    def run_statistical_arbitrage_strategy(self):
        """Enhanced statistical arbitrage with lower thresholds"""
        try:
            prices = self.market_data['prices']
            returns = self.market_data['returns']
            
            # Find cointegrated pairs
            signals = []
            for i in range(len(returns[0])):
                for j in range(i+1, len(returns[0])):
                    if len(returns) >= 30:
                        # Simple correlation-based approach
                        correlation = np.corrcoef(returns[-30:, i], returns[-30:, j])[0, 1]
                        
                        if abs(correlation) > 0.7:  # Lower threshold from 0.8
                            # Calculate spread
                            spread = returns[-1, i] - returns[-1, j]
                            spread_std = np.std(returns[-30:, i] - returns[-30:, j])
                            
                            if spread_std > 0:
                                z_score = spread / spread_std
                                
                                if abs(z_score) > 1.2:  # Lower threshold from 1.5
                                    confidence = min(0.8, abs(z_score) / 2.0)
                                    if confidence >= self.strategies['statistical_arbitrage']['confidence_threshold']:
                                        signal = 'sell' if z_score > 0 else 'buy'
                                        position_size = min(
                                            self.position_sizing['max_size'],
                                            self.position_sizing['base_size'] * confidence * self.position_sizing['scaling_factor']
                                        )
                                        signals.append({
                                            'asset': f"{self.market_data['assets'][i]}-{self.market_data['assets'][j]}",
                                            'signal': signal,
                                            'confidence': confidence,
                                            'position_size': position_size,
                                            'strategy': 'statistical_arbitrage',
                                            'z_score': z_score,
                                            'correlation': correlation
                                        })
            
            return signals
            
        except Exception as e:
            print(f"Statistical arbitrage strategy error: {e}")
            return []
    
    def run_trend_following_strategy(self):
        """New trend following strategy"""
        try:
            prices = self.market_data['prices']
            returns = self.market_data['returns']
            
            # Calculate trend indicators
            short_ma = np.mean(prices[-10:], axis=0)  # 10-day moving average
            long_ma = np.mean(prices[-30:], axis=0)  # 30-day moving average
            
            signals = []
            for i in range(len(short_ma)):
                if len(prices) >= 30:
                    trend_strength = (short_ma[i] - long_ma[i]) / long_ma[i]
                    
                    if abs(trend_strength) > 0.02:  # 2% trend threshold
                        confidence = min(0.8, abs(trend_strength) * 20)
                        if confidence >= self.strategies['trend_following']['confidence_threshold']:
                            signal = 'buy' if trend_strength > 0 else 'sell'
                            position_size = min(
                                self.position_sizing['max_size'],
                                self.position_sizing['base_size'] * confidence * self.position_sizing['scaling_factor']
                            )
                            signals.append({
                                'asset': self.market_data['assets'][i],
                                'signal': signal,
                                'confidence': confidence,
                                'position_size': position_size,
                                'strategy': 'trend_following',
                                'trend_strength': trend_strength
                            })
            
            return signals
            
        except Exception as e:
            print(f"Trend following strategy error: {e}")
            return []
    
    def run_all_strategies(self):
        """Run all enabled strategies"""
        print("🚀 Running all multi-strategy diversification strategies...")
        
        all_signals = []
        
        # Run each strategy
        if self.strategies['momentum']['enabled']:
            momentum_signals = self.run_momentum_strategy()
            all_signals.extend(momentum_signals)
            print(f"📊 Momentum: {len(momentum_signals)} signals")
        
        if self.strategies['mean_reversion']['enabled']:
            mean_rev_signals = self.run_mean_reversion_strategy()
            all_signals.extend(mean_rev_signals)
            print(f"📊 Mean Reversion: {len(mean_rev_signals)} signals")
        
        if self.strategies['statistical_arbitrage']['enabled']:
            stat_arb_signals = self.run_statistical_arbitrage_strategy()
            all_signals.extend(stat_arb_signals)
            print(f"📊 Statistical Arbitrage: {len(stat_arb_signals)} signals")
        
        if self.strategies['trend_following']['enabled']:
            trend_signals = self.run_trend_following_strategy()
            all_signals.extend(trend_signals)
            print(f"📊 Trend Following: {len(trend_signals)} signals")
        
        # Aggregate results
        total_signals = len(all_signals)
        active_signals = len([s for s in all_signals if s['confidence'] > 0.3])
        avg_confidence = np.mean([s['confidence'] for s in all_signals]) if all_signals else 0
        
        print(f"✅ Multi-strategy diversification complete: {total_signals} total signals, {active_signals} active")
        
        return {
            'signals': all_signals,
            'summary': {
                'total_strategies': len([s for s in self.strategies.values() if s['enabled']]),
                'active_signals': active_signals,
                'average_confidence': avg_confidence,
                'timestamp': datetime.now().isoformat()
            }
        }

# Main execution
if __name__ == "__main__":
    diversification = MultiStrategyDiversification()
    results = diversification.run_all_strategies()
    print(f"\n📋 RESULTS: {results['summary']}")
