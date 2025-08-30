#!/usr/bin/env python3
"""
Enhanced Portfolio Optimization System
Aggressive optimization with lower risk thresholds and dynamic rebalancing
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import random

class EnhancedPortfolioOptimization:
    def __init__(self):
        print("🚀 ENHANCED PORTFOLIO OPTIMIZATION - AGGRESSIVE")
        
        # Aggressive risk parameters
        self.risk_parameters = {
            'max_portfolio_risk': 0.85,  # Increased from 0.75
            'position_limit': 0.3,  # Increased from 0.25
            'sector_limit': 0.4,  # Increased from 0.35
            'correlation_threshold': 0.6,  # Lowered from 0.7
            'volatility_target': 0.25,  # Increased from 0.20
            'drawdown_limit': 0.15  # Increased from 0.10
        }
        
        # Enhanced optimization strategies
        self.optimization_strategies = {
            'risk_parity': {'enabled': True, 'weight': 0.3},
            'black_litterman': {'enabled': True, 'weight': 0.25},
            'hierarchical_risk_parity': {'enabled': True, 'weight': 0.25},
            'maximum_diversification': {'enabled': True, 'weight': 0.2}
        }
        
        # Dynamic rebalancing
        self.rebalancing = {
            'frequency': 'daily',  # More frequent than weekly
            'threshold': 0.05,  # Lower threshold for rebalancing
            'max_trades_per_rebalance': 8  # Increased from 5
        }
        
        # Market data simulation
        self.market_data = self.generate_market_data()
        self.portfolio = self.initialize_portfolio()
        
    def generate_market_data(self):
        """Generate realistic market data for portfolio optimization"""
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2025-08-09', freq='D')
        
        # Generate multiple asset classes
        n_assets = 12
        n_days = len(dates)
        
        # Different asset class characteristics
        asset_classes = {
            'stocks': {'return': 0.0008, 'vol': 0.025, 'count': 6},
            'bonds': {'return': 0.0003, 'vol': 0.015, 'count': 3},
            'commodities': {'return': 0.0002, 'vol': 0.035, 'count': 2},
            'alternatives': {'return': 0.0006, 'vol': 0.040, 'count': 1}
        }
        
        # Generate returns for each asset class
        returns = np.zeros((n_days, n_assets))
        asset_idx = 0
        
        for asset_class, params in asset_classes.items():
            for i in range(params['count']):
                # Add some idiosyncratic risk
                idiosyncratic = np.random.normal(0, params['vol'] * 0.3, n_days)
                returns[:, asset_idx] = np.random.normal(params['return'], params['vol'], n_days) + idiosyncratic
                asset_idx += 1
        
        # Add market regime changes
        regime_changes = np.random.choice([0, 1], size=n_days, p=[0.95, 0.05])
        for i in range(n_days):
            if regime_changes[i]:
                returns[i, :] *= 1.5  # Volatility spike
        
        # Convert to prices
        prices = 100 * np.exp(np.cumsum(returns, axis=0))
        
        return {
            'dates': dates,
            'prices': prices,
            'returns': returns,
            'assets': [f'ASSET_{i+1}' for i in range(n_assets)],
            'asset_classes': asset_classes
        }
    
    def initialize_portfolio(self):
        """Initialize portfolio with equal weights"""
        n_assets = len(self.market_data['assets'])
        weights = np.ones(n_assets) / n_assets
        
        return {
            'weights': weights,
            'positions': weights * 100000,  # $100k portfolio
            'last_rebalance': datetime.now(),
            'performance_history': [],
            'risk_metrics': {}
        }
    
    def calculate_portfolio_risk(self):
        """Calculate current portfolio risk metrics"""
        try:
            returns = self.market_data['returns']
            weights = self.portfolio['weights']
            
            # Calculate covariance matrix
            cov_matrix = np.cov(returns.T)
            
            # Portfolio variance
            portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
            portfolio_volatility = np.sqrt(portfolio_variance)
            
            # Value at Risk (95%)
            portfolio_returns = np.dot(returns, weights)
            var_95 = np.percentile(portfolio_returns, 5)
            
            # Maximum drawdown
            cumulative_returns = np.cumprod(1 + portfolio_returns)
            running_max = np.maximum.accumulate(cumulative_returns)
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = np.min(drawdown)
            
            # Sector concentration
            sector_concentration = self.calculate_sector_concentration()
            
            self.portfolio['risk_metrics'] = {
                'volatility': portfolio_volatility,
                'var_95': var_95,
                'max_drawdown': max_drawdown,
                'sector_concentration': sector_concentration,
                'sharpe_ratio': np.mean(portfolio_returns) / portfolio_volatility if portfolio_volatility > 0 else 0
            }
            
            return self.portfolio['risk_metrics']
            
        except Exception as e:
            print(f"Risk calculation error: {e}")
            return {}
    
    def calculate_sector_concentration(self):
        """Calculate sector concentration risk"""
        try:
            weights = self.portfolio['weights']
            asset_classes = self.market_data['asset_classes']
            
            sector_weights = {}
            asset_idx = 0
            
            for asset_class, params in asset_classes.items():
                sector_weight = np.sum(weights[asset_idx:asset_idx + params['count']])
                sector_weights[asset_class] = sector_weight
                asset_idx += params['count']
            
            # Calculate concentration risk
            concentration_risk = np.sum([w**2 for w in sector_weights.values()])
            
            return {
                'sector_weights': sector_weights,
                'concentration_risk': concentration_risk,
                'max_sector_weight': max(sector_weights.values())
            }
            
        except Exception as e:
            print(f"Sector concentration error: {e}")
            return {}
    
    def run_risk_parity_optimization(self):
        """Risk parity optimization"""
        try:
            returns = self.market_data['returns']
            cov_matrix = np.cov(returns.T)
            
            # Calculate risk contribution for each asset
            n_assets = len(returns[0])
            risk_contributions = np.zeros(n_assets)
            
            # Simple risk parity implementation
            volatilities = np.sqrt(np.diag(cov_matrix))
            target_risk = np.mean(volatilities)
            
            # Equal risk contribution
            weights = (1 / volatilities) / np.sum(1 / volatilities)
            
            return {
                'strategy': 'risk_parity',
                'weights': weights,
                'expected_risk': target_risk,
                'diversification_ratio': self.calculate_diversification_ratio(weights, cov_matrix)
            }
            
        except Exception as e:
            print(f"Risk parity optimization error: {e}")
            return {}
    
    def run_black_litterman_optimization(self):
        """Black-Litterman optimization with market views"""
        try:
            returns = self.market_data['returns']
            cov_matrix = np.cov(returns.T)
            
            # Market equilibrium returns (CAPM)
            market_returns = np.mean(returns, axis=0)
            risk_free_rate = 0.02 / 252  # Daily risk-free rate
            
            # Investor views (more aggressive than market)
            views = []
            for i in range(len(market_returns)):
                if market_returns[i] > risk_free_rate:
                    views.append({
                        'asset': i,
                        'view': market_returns[i] * 1.2,  # 20% more bullish
                        'confidence': 0.6
                    })
            
            # Simple implementation - adjust weights based on views
            weights = np.ones(len(market_returns)) / len(market_returns)
            
            for view in views:
                if view['confidence'] > 0.5:
                    weights[view['asset']] *= 1.1  # Increase weight by 10%
            
            # Normalize weights
            weights = weights / np.sum(weights)
            
            return {
                'strategy': 'black_litterman',
                'weights': weights,
                'views': views,
                'expected_return': np.dot(weights, market_returns)
            }
            
        except Exception as e:
            print(f"Black-Litterman optimization error: {e}")
            return {}
    
    def run_hierarchical_risk_parity(self):
        """Hierarchical Risk Parity optimization"""
        try:
            returns = self.market_data['returns']
            cov_matrix = np.cov(returns.T)
            
            # Calculate correlation matrix
            corr_matrix = self.cov_to_corr(cov_matrix)
            
            # Hierarchical clustering of correlations
            # Simple implementation - group by correlation similarity
            n_assets = len(returns[0])
            weights = np.ones(n_assets) / n_assets
            
            # Adjust weights based on correlation structure
            for i in range(n_assets):
                for j in range(i+1, n_assets):
                    if abs(corr_matrix[i, j]) > 0.7:  # High correlation
                        # Reduce weight of one asset to diversify
                        if weights[i] > weights[j]:
                            weights[i] *= 0.9
                        else:
                            weights[j] *= 0.9
            
            # Normalize weights
            weights = weights / np.sum(weights)
            
            return {
                'strategy': 'hierarchical_risk_parity',
                'weights': weights,
                'correlation_structure': corr_matrix
            }
            
        except Exception as e:
            print(f"Hierarchical risk parity error: {e}")
            return {}
    
    def cov_to_corr(self, cov_matrix):
        """Convert covariance matrix to correlation matrix"""
        try:
            std_devs = np.sqrt(np.diag(cov_matrix))
            corr_matrix = cov_matrix / np.outer(std_devs, std_devs)
            return corr_matrix
        except:
            return cov_matrix
    
    def calculate_diversification_ratio(self, weights, cov_matrix):
        """Calculate portfolio diversification ratio"""
        try:
            weighted_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            avg_vol = np.mean(np.sqrt(np.diag(cov_matrix)))
            return avg_vol / weighted_vol
        except:
            return 1.0
    
    def generate_rebalancing_signals(self):
        """Generate rebalancing signals based on current portfolio"""
        try:
            current_weights = self.portfolio['weights']
            risk_metrics = self.calculate_portfolio_risk()
            
            # Run all optimization strategies
            optimizations = {}
            
            if self.optimization_strategies['risk_parity']['enabled']:
                optimizations['risk_parity'] = self.run_risk_parity_optimization()
            
            if self.optimization_strategies['black_litterman']['enabled']:
                optimizations['black_litterman'] = self.run_black_litterman_optimization()
            
            if self.optimization_strategies['hierarchical_risk_parity']['enabled']:
                optimizations['hierarchical_risk_parity'] = self.run_hierarchical_risk_parity()
            
            # Combine optimizations
            target_weights = self.combine_optimizations(optimizations)
            
            # Generate rebalancing signals
            signals = []
            for i, (current, target) in enumerate(zip(current_weights, target_weights)):
                weight_diff = target - current
                
                if abs(weight_diff) > self.rebalancing['threshold']:
                    signal = {
                        'asset': self.market_data['assets'][i],
                        'action': 'buy' if weight_diff > 0 else 'sell',
                        'current_weight': current,
                        'target_weight': target,
                        'weight_change': abs(weight_diff),
                        'confidence': min(0.9, abs(weight_diff) * 5),  # Higher confidence for larger changes
                        'strategy': 'portfolio_optimization'
                    }
                    signals.append(signal)
            
            return signals
            
        except Exception as e:
            print(f"Rebalancing signal generation error: {e}")
            return []
    
    def combine_optimizations(self, optimizations):
        """Combine multiple optimization strategies"""
        try:
            n_assets = len(self.market_data['assets'])
            combined_weights = np.zeros(n_assets)
            
            for strategy_name, optimization in optimizations.items():
                if optimization and 'weights' in optimization:
                    weight = self.optimization_strategies[strategy_name]['weight']
                    combined_weights += weight * optimization['weights']
            
            # If no optimizations, use equal weights
            if np.sum(combined_weights) == 0:
                combined_weights = np.ones(n_assets) / n_assets
            
            # Normalize
            combined_weights = combined_weights / np.sum(combined_weights)
            
            return combined_weights
            
        except Exception as e:
            print(f"Optimization combination error: {e}")
            return np.ones(len(self.market_data['assets'])) / len(self.market_data['assets'])
    
    def run_portfolio_optimization(self):
        """Run complete portfolio optimization cycle"""
        print("🚀 Running enhanced portfolio optimization...")
        
        # Calculate current risk
        current_risk = self.calculate_portfolio_risk()
        print(f"📊 Current portfolio risk: Volatility {current_risk.get('volatility', 0):.4f}")
        
        # Generate rebalancing signals
        signals = self.generate_rebalancing_signals()
        
        # Filter signals based on risk limits
        filtered_signals = []
        for signal in signals:
            if signal['confidence'] > 0.4:  # Lower confidence threshold
                filtered_signals.append(signal)
        
        # Limit number of trades
        if len(filtered_signals) > self.rebalancing['max_trades_per_rebalance']:
            # Sort by confidence and weight change
            filtered_signals.sort(key=lambda x: (x['confidence'], x['weight_change']), reverse=True)
            filtered_signals = filtered_signals[:self.rebalancing['max_trades_per_rebalance']]
        
        print(f"📊 Portfolio optimization complete: {len(filtered_signals)} rebalancing signals")
        
        return {
            'signals': filtered_signals,
            'current_risk': current_risk,
            'summary': {
                'total_signals': len(filtered_signals),
                'active_signals': len([s for s in filtered_signals if s['confidence'] > 0.5]),
                'average_confidence': np.mean([s['confidence'] for s in filtered_signals]) if filtered_signals else 0,
                'timestamp': datetime.now().isoformat()
            }
        }

# Main execution
if __name__ == "__main__":
    optimizer = EnhancedPortfolioOptimization()
    results = optimizer.run_portfolio_optimization()
    print(f"\n📋 RESULTS: {results['summary']}")
