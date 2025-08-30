#!/usr/bin/env python3
"""
ENHANCED PORTFOLIO OPTIMIZATION SYSTEM
Modern Portfolio Theory, Risk Parity, and Dynamic Asset Allocation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
import json
from scipy.optimize import minimize

class EnhancedPortfolioOptimizationSystem:
    def __init__(self):
        print("📊 ENHANCED PORTFOLIO OPTIMIZATION SYSTEM - INITIALIZING...")
        print("🎯 Implementing MPT, Risk Parity & Dynamic Asset Allocation")
        
        # Portfolio configuration
        self.portfolio_config = {
            'risk_free_rate': 0.02,  # 2% risk-free rate
            'target_volatility': 0.15,  # 15% target volatility
            'max_position_size': 0.25,  # 25% max position size
            'rebalancing_frequency': 'daily',
            'optimization_method': 'sharpe_ratio'
        }
        
        # Asset classes and their characteristics
        self.asset_classes = {
            'equities': {
                'expected_return': 0.10,
                'volatility': 0.20,
                'correlation_matrix': None
            },
            'bonds': {
                'expected_return': 0.05,
                'volatility': 0.08,
                'correlation_matrix': None
            },
            'commodities': {
                'expected_return': 0.08,
                'volatility': 0.25,
                'correlation_matrix': None
            },
            'real_estate': {
                'expected_return': 0.09,
                'volatility': 0.18,
                'correlation_matrix': None
            },
            'alternatives': {
                'expected_return': 0.12,
                'volatility': 0.30,
                'correlation_matrix': None
            }
        }
        
        # Current portfolio state
        self.current_portfolio = {
            'total_value': 1000000.0,  # $1M starting portfolio
            'positions': {},
            'allocation': {},
            'risk_metrics': {},
            'performance_history': []
        }
        
        # Optimization results
        self.optimization_results = {
            'optimal_weights': {},
            'expected_return': 0.0,
            'expected_volatility': 0.0,
            'sharpe_ratio': 0.0,
            'last_optimization': None
        }
        
        print("✅ Enhanced Portfolio Optimization System initialized")
    
    async def run_portfolio_optimization(self, market_data: Dict) -> Dict:
        """Run comprehensive portfolio optimization"""
        print("🚀 RUNNING PORTFOLIO OPTIMIZATION...")
        
        try:
            # 1. Update market data and correlations
            await self.update_market_data(market_data)
            
            # 2. Run Modern Portfolio Theory optimization
            mpt_result = await self.run_mpt_optimization()
            
            # 3. Run Risk Parity optimization
            risk_parity_result = await self.run_risk_parity_optimization()
            
            # 4. Run Dynamic Asset Allocation
            dynamic_allocation_result = await self.run_dynamic_asset_allocation()
            
            # 5. Combine and select optimal portfolio
            optimal_portfolio = await self.select_optimal_portfolio(
                mpt_result, risk_parity_result, dynamic_allocation_result
            )
            
            # 6. Generate rebalancing recommendations
            rebalancing_recommendations = await self.generate_rebalancing_recommendations(
                optimal_portfolio
            )
            
            # 7. Update portfolio state
            await self.update_portfolio_state(optimal_portfolio, rebalancing_recommendations)
            
            optimization_summary = {
                'mpt_optimization': mpt_result,
                'risk_parity_optimization': risk_parity_result,
                'dynamic_allocation': dynamic_allocation_result,
                'optimal_portfolio': optimal_portfolio,
                'rebalancing_recommendations': rebalancing_recommendations,
                'timestamp': datetime.now().isoformat()
            }
            
            print("✅ Portfolio optimization completed successfully")
            return optimization_summary
            
        except Exception as e:
            print(f"❌ Portfolio optimization error: {e}")
            return {'error': str(e)}
    
    async def update_market_data(self, market_data: Dict):
        """Update market data and correlations"""
        print("📊 Updating market data and correlations...")
        
        try:
            # Update expected returns based on recent performance
            for asset_class in self.asset_classes:
                if asset_class in market_data:
                    recent_return = market_data[asset_class].get('recent_return', 0)
                    # Blend historical and recent data
                    self.asset_classes[asset_class]['expected_return'] = (
                        0.7 * self.asset_classes[asset_class]['expected_return'] +
                        0.3 * recent_return
                    )
            
            # Update correlation matrix if available
            if 'correlation_matrix' in market_data:
                self.update_correlation_matrix(market_data['correlation_matrix'])
            
            print("   ✅ Market data updated")
            
        except Exception as e:
            print(f"   ⚠️ Market data update warning: {e}")
    
    def update_correlation_matrix(self, correlation_data: Dict):
        """Update correlation matrix for asset classes"""
        try:
            # Create correlation matrix
            asset_names = list(self.asset_classes.keys())
            correlation_matrix = np.zeros((len(asset_names), len(asset_names)))
            
            for i, asset1 in enumerate(asset_names):
                for j, asset2 in enumerate(asset_names):
                    if asset1 == asset2:
                        correlation_matrix[i, j] = 1.0
                    elif f"{asset1}_{asset2}" in correlation_data:
                        correlation_matrix[i, j] = correlation_data[f"{asset1}_{asset2}"]
                    elif f"{asset2}_{asset1}" in correlation_data:
                        correlation_matrix[i, j] = correlation_data[f"{asset2}_{asset1}"]
                    else:
                        # Use default correlations
                        correlation_matrix[i, j] = 0.3 if asset1 != asset2 else 1.0
            
            # Update asset classes with correlation matrix
            for i, asset_name in enumerate(asset_names):
                self.asset_classes[asset_name]['correlation_matrix'] = correlation_matrix[i, :]
            
        except Exception as e:
            print(f"   ⚠️ Correlation matrix update warning: {e}")
    
    async def run_mpt_optimization(self) -> Dict:
        """Run Modern Portfolio Theory optimization"""
        print("📊 Running MPT Optimization...")
        
        try:
            # Get asset class data
            asset_names = list(self.asset_classes.keys())
            expected_returns = [self.asset_classes[asset]['expected_return'] for asset in asset_names]
            volatilities = [self.asset_classes[asset]['volatility'] for asset in asset_names]
            
            # Create covariance matrix
            covariance_matrix = self.create_covariance_matrix(asset_names, volatilities)
            
            # Run optimization
            optimal_weights = self.optimize_portfolio_mpt(
                expected_returns, covariance_matrix, self.portfolio_config['target_volatility']
            )
            
            # Calculate portfolio metrics
            portfolio_return = np.dot(optimal_weights, expected_returns)
            portfolio_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(covariance_matrix, optimal_weights)))
            sharpe_ratio = (portfolio_return - self.portfolio_config['risk_free_rate']) / portfolio_volatility
            
            mpt_result = {
                'method': 'modern_portfolio_theory',
                'optimal_weights': dict(zip(asset_names, optimal_weights)),
                'expected_return': portfolio_return,
                'expected_volatility': portfolio_volatility,
                'sharpe_ratio': sharpe_ratio,
                'target_volatility': self.portfolio_config['target_volatility']
            }
            
            print(f"   📈 MPT: Return {portfolio_return:.3f}, Vol {portfolio_volatility:.3f}, Sharpe {sharpe_ratio:.3f}")
            return mpt_result
            
        except Exception as e:
            print(f"   ❌ MPT optimization error: {e}")
            return {'method': 'modern_portfolio_theory', 'error': str(e)}
    
    async def run_risk_parity_optimization(self) -> Dict:
        """Run Risk Parity optimization"""
        print("⚖️ Running Risk Parity Optimization...")
        
        try:
            # Get asset class data
            asset_names = list(self.asset_classes.keys())
            volatilities = [self.asset_classes[asset]['volatility'] for asset in asset_names]
            
            # Create correlation matrix
            correlation_matrix = self.create_correlation_matrix(asset_names)
            
            # Run risk parity optimization
            optimal_weights = self.optimize_risk_parity(asset_names, volatilities, correlation_matrix)
            
            # Calculate portfolio metrics
            expected_returns = [self.asset_classes[asset]['expected_return'] for asset in asset_names]
            portfolio_return = np.dot(optimal_weights, expected_returns)
            portfolio_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(
                self.create_covariance_matrix(asset_names, volatilities), optimal_weights
            )))
            
            risk_parity_result = {
                'method': 'risk_parity',
                'optimal_weights': dict(zip(asset_names, optimal_weights)),
                'expected_return': portfolio_return,
                'expected_volatility': portfolio_volatility,
                'risk_contribution': self.calculate_risk_contribution(optimal_weights, asset_names, volatilities, correlation_matrix)
            }
            
            print(f"   ⚖️ Risk Parity: Return {portfolio_return:.3f}, Vol {portfolio_volatility:.3f}")
            return risk_parity_result
            
        except Exception as e:
            print(f"   ❌ Risk parity optimization error: {e}")
            return {'method': 'risk_parity', 'error': str(e)}
    
    async def run_dynamic_asset_allocation(self) -> Dict:
        """Run Dynamic Asset Allocation based on market conditions"""
        print("🔄 Running Dynamic Asset Allocation...")
        
        try:
            # Get current market regime indicators
            market_regime = self.assess_market_regime()
            
            # Adjust allocations based on regime
            dynamic_weights = self.calculate_regime_based_allocation(market_regime)
            
            # Calculate portfolio metrics
            asset_names = list(self.asset_classes.keys())
            expected_returns = [self.asset_classes[asset]['expected_return'] for asset in asset_names]
            volatilities = [self.asset_classes[asset]['volatility'] for asset in asset_names]
            
            portfolio_return = np.dot(dynamic_weights, expected_returns)
            portfolio_volatility = np.sqrt(np.dot(dynamic_weights.T, np.dot(
                self.create_covariance_matrix(asset_names, volatilities), dynamic_weights
            )))
            
            dynamic_result = {
                'method': 'dynamic_asset_allocation',
                'market_regime': market_regime,
                'optimal_weights': dict(zip(asset_names, dynamic_weights)),
                'expected_return': portfolio_return,
                'expected_volatility': portfolio_volatility,
                'regime_adjustments': self.get_regime_adjustments(market_regime)
            }
            
            print(f"   🔄 Dynamic: Regime {market_regime}, Return {portfolio_return:.3f}, Vol {portfolio_volatility:.3f}")
            return dynamic_result
            
        except Exception as e:
            print(f"   ❌ Dynamic allocation error: {e}")
            return {'method': 'dynamic_asset_allocation', 'error': str(e)}
    
    def create_covariance_matrix(self, asset_names: List[str], volatilities: List[float]) -> np.ndarray:
        """Create covariance matrix from volatilities and correlations"""
        n_assets = len(asset_names)
        covariance_matrix = np.zeros((n_assets, n_assets))
        
        for i in range(n_assets):
            for j in range(n_assets):
                if i == j:
                    covariance_matrix[i, j] = volatilities[i] ** 2
                else:
                    # Use correlation if available, otherwise default
                    correlation = 0.3  # Default correlation
                    if self.asset_classes[asset_names[i]]['correlation_matrix'] is not None:
                        correlation = self.asset_classes[asset_names[i]]['correlation_matrix'][j]
                    
                    covariance_matrix[i, j] = correlation * volatilities[i] * volatilities[j]
        
        return covariance_matrix
    
    def create_correlation_matrix(self, asset_names: List[str]) -> np.ndarray:
        """Create correlation matrix"""
        n_assets = len(asset_names)
        correlation_matrix = np.eye(n_assets)  # Identity matrix
        
        for i in range(n_assets):
            for j in range(n_assets):
                if i != j:
                    if self.asset_classes[asset_names[i]]['correlation_matrix'] is not None:
                        correlation_matrix[i, j] = self.asset_classes[asset_names[i]]['correlation_matrix'][j]
                    else:
                        correlation_matrix[i, j] = 0.3  # Default correlation
        
        return correlation_matrix
    
    def optimize_portfolio_mpt(self, expected_returns: List[float], covariance_matrix: np.ndarray, target_volatility: float) -> np.ndarray:
        """Optimize portfolio using Modern Portfolio Theory"""
        n_assets = len(expected_returns)
        
        # Objective function: maximize Sharpe ratio
        def objective(weights):
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
            sharpe_ratio = (portfolio_return - self.portfolio_config['risk_free_rate']) / portfolio_volatility
            return -sharpe_ratio  # Minimize negative Sharpe ratio
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights sum to 1
            {'type': 'ineq', 'fun': lambda x: target_volatility - np.sqrt(np.dot(x.T, np.dot(covariance_matrix, x)))}  # Volatility constraint
        ]
        
        # Bounds: weights between 0 and max_position_size
        bounds = [(0, self.portfolio_config['max_position_size']) for _ in range(n_assets)]
        
        # Initial guess: equal weights
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Run optimization
        result = minimize(
            objective, initial_weights, method='SLSQP',
            bounds=bounds, constraints=constraints
        )
        
        if result.success:
            return result.x
        else:
            # Fallback to equal weights
            return np.array([1/n_assets] * n_assets)
    
    def optimize_risk_parity(self, asset_names: List[str], volatilities: List[float], correlation_matrix: np.ndarray) -> np.ndarray:
        """Optimize portfolio using Risk Parity approach"""
        n_assets = len(asset_names)
        
        # Objective function: minimize risk contribution variance
        def objective(weights):
            risk_contributions = self.calculate_risk_contribution(weights, asset_names, volatilities, correlation_matrix)
            return np.var(risk_contributions)
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
        ]
        
        # Bounds
        bounds = [(0, self.portfolio_config['max_position_size']) for _ in range(n_assets)]
        
        # Initial guess: inverse volatility weights
        initial_weights = np.array([1/vol for vol in volatilities])
        initial_weights = initial_weights / np.sum(initial_weights)
        
        # Run optimization
        result = minimize(
            objective, initial_weights, method='SLSQP',
            bounds=bounds, constraints=constraints
        )
        
        if result.success:
            return result.x
        else:
            # Fallback to inverse volatility weights
            return initial_weights
    
    def calculate_risk_contribution(self, weights: np.ndarray, asset_names: List[str], volatilities: List[float], correlation_matrix: np.ndarray) -> np.ndarray:
        """Calculate risk contribution of each asset"""
        n_assets = len(asset_names)
        risk_contributions = np.zeros(n_assets)
        
        # Calculate portfolio volatility
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(
            self.create_covariance_matrix(asset_names, volatilities), weights
        )))
        
        if portfolio_vol > 0:
            # Calculate marginal risk contribution
            for i in range(n_assets):
                marginal_risk = 0
                for j in range(n_assets):
                    if i == j:
                        marginal_risk += weights[i] * volatilities[i] ** 2
                    else:
                        correlation = correlation_matrix[i, j]
                        marginal_risk += weights[j] * correlation * volatilities[i] * volatilities[j]
                
                risk_contributions[i] = weights[i] * marginal_risk / portfolio_vol
        
        return risk_contributions
    
    def assess_market_regime(self) -> str:
        """Assess current market regime"""
        # This would typically use market indicators like VIX, yield curves, etc.
        # For now, use a simplified approach
        
        # Calculate average volatility across asset classes
        avg_volatility = np.mean([self.asset_classes[asset]['volatility'] for asset in self.asset_classes])
        
        if avg_volatility < 0.15:
            return 'low_volatility'
        elif avg_volatility < 0.25:
            return 'normal_volatility'
        else:
            return 'high_volatility'
    
    def calculate_regime_based_allocation(self, market_regime: str) -> np.ndarray:
        """Calculate allocation based on market regime"""
        asset_names = list(self.asset_classes.keys())
        n_assets = len(asset_names)
        
        if market_regime == 'low_volatility':
            # Favor equities and alternatives in low volatility
            weights = np.array([0.4, 0.2, 0.15, 0.15, 0.1])
        elif market_regime == 'high_volatility':
            # Favor bonds and defensive assets in high volatility
            weights = np.array([0.2, 0.4, 0.1, 0.2, 0.1])
        else:
            # Balanced allocation in normal volatility
            weights = np.array([0.3, 0.3, 0.15, 0.15, 0.1])
        
        # Ensure weights sum to 1
        weights = weights / np.sum(weights)
        
        return weights
    
    def get_regime_adjustments(self, market_regime: str) -> Dict:
        """Get regime-specific adjustments"""
        adjustments = {
            'low_volatility': {
                'equity_overweight': 0.1,
                'bond_underweight': -0.1,
                'risk_tolerance': 'high'
            },
            'normal_volatility': {
                'equity_overweight': 0.0,
                'bond_underweight': 0.0,
                'risk_tolerance': 'medium'
            },
            'high_volatility': {
                'equity_overweight': -0.1,
                'bond_underweight': 0.1,
                'risk_tolerance': 'low'
            }
        }
        
        return adjustments.get(market_regime, {})
    
    async def select_optimal_portfolio(self, mpt_result: Dict, risk_parity_result: Dict, dynamic_result: Dict) -> Dict:
        """Select optimal portfolio from different optimization methods"""
        print("🎯 Selecting optimal portfolio...")
        
        try:
            # Score each method based on multiple criteria
            method_scores = {}
            
            # MPT scoring
            if 'error' not in mpt_result:
                mpt_score = (
                    mpt_result.get('sharpe_ratio', 0) * 0.4 +
                    (1 - abs(mpt_result.get('expected_volatility', 0) - self.portfolio_config['target_volatility'])) * 0.3 +
                    mpt_result.get('expected_return', 0) * 0.3
                )
                method_scores['mpt'] = mpt_score
            else:
                method_scores['mpt'] = 0
            
            # Risk Parity scoring
            if 'error' not in risk_parity_result:
                risk_parity_score = (
                    (1 - risk_parity_result.get('expected_volatility', 0)) * 0.4 +
                    risk_parity_result.get('expected_return', 0) * 0.3 +
                    0.3  # Bonus for risk parity
                )
                method_scores['risk_parity'] = risk_parity_score
            else:
                method_scores['risk_parity'] = 0
            
            # Dynamic allocation scoring
            if 'error' not in dynamic_result:
                dynamic_score = (
                    dynamic_result.get('expected_return', 0) * 0.4 +
                    (1 - dynamic_result.get('expected_volatility', 0)) * 0.3 +
                    0.3  # Bonus for dynamic approach
                )
                method_scores['dynamic'] = dynamic_score
            else:
                method_scores['dynamic'] = 0
            
            # Select best method
            best_method = max(method_scores, key=method_scores.get)
            print(f"   🏆 Selected method: {best_method} (score: {method_scores[best_method]:.3f})")
            
            # Return optimal portfolio
            if best_method == 'mpt':
                return mpt_result
            elif best_method == 'risk_parity':
                return risk_parity_result
            else:
                return dynamic_result
                
        except Exception as e:
            print(f"   ❌ Portfolio selection error: {e}")
            # Fallback to MPT if available
            if 'error' not in mpt_result:
                return mpt_result
            else:
                return {'error': 'All optimization methods failed'}
    
    async def generate_rebalancing_recommendations(self, optimal_portfolio: Dict) -> Dict:
        """Generate rebalancing recommendations"""
        print("⚖️ Generating rebalancing recommendations...")
        
        try:
            if 'error' in optimal_portfolio:
                return {'error': 'Cannot generate recommendations from failed optimization'}
            
            current_weights = self.current_portfolio.get('allocation', {})
            target_weights = optimal_portfolio.get('optimal_weights', {})
            
            rebalancing_trades = {}
            total_trades_value = 0
            
            for asset in target_weights:
                current_weight = current_weights.get(asset, 0)
                target_weight = target_weights[asset]
                
                weight_diff = target_weight - current_weight
                trade_value = weight_diff * self.current_portfolio['total_value']
                
                if abs(weight_diff) > 0.01:  # 1% threshold
                    rebalancing_trades[asset] = {
                        'current_weight': current_weight,
                        'target_weight': target_weight,
                        'weight_change': weight_diff,
                        'trade_value': trade_value,
                        'trade_type': 'buy' if weight_diff > 0 else 'sell'
                    }
                    total_trades_value += abs(trade_value)
            
            recommendations = {
                'rebalancing_trades': rebalancing_trades,
                'total_trades_value': total_trades_value,
                'rebalancing_threshold': 0.01,
                'estimated_transaction_costs': total_trades_value * 0.001,  # 0.1% transaction costs
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   📊 Generated {len(rebalancing_trades)} rebalancing trades")
            return recommendations
            
        except Exception as e:
            print(f"   ❌ Rebalancing recommendations error: {e}")
            return {'error': str(e)}
    
    async def update_portfolio_state(self, optimal_portfolio: Dict, rebalancing_recommendations: Dict):
        """Update portfolio state with optimization results"""
        print("📋 Updating portfolio state...")
        
        try:
            # Update optimization results
            self.optimization_results.update({
                'optimal_weights': optimal_portfolio.get('optimal_weights', {}),
                'expected_return': optimal_portfolio.get('expected_return', 0),
                'expected_volatility': optimal_portfolio.get('expected_volatility', 0),
                'sharpe_ratio': optimal_portfolio.get('sharpe_ratio', 0),
                'last_optimization': datetime.now().isoformat()
            })
            
            # Update current portfolio allocation
            if 'optimal_weights' in optimal_portfolio:
                self.current_portfolio['allocation'] = optimal_portfolio['optimal_weights']
            
            # Update risk metrics
            self.current_portfolio['risk_metrics'] = {
                'expected_volatility': optimal_portfolio.get('expected_volatility', 0),
                'var_95': self.calculate_portfolio_var_95(),
                'max_drawdown': self.calculate_max_drawdown(),
                'beta': self.calculate_portfolio_beta()
            }
            
            # Add to performance history
            performance_record = {
                'timestamp': datetime.now().isoformat(),
                'allocation': optimal_portfolio.get('optimal_weights', {}),
                'expected_return': optimal_portfolio.get('expected_return', 0),
                'expected_volatility': optimal_portfolio.get('expected_volatility', 0),
                'sharpe_ratio': optimal_portfolio.get('sharpe_ratio', 0)
            }
            
            self.current_portfolio['performance_history'].append(performance_record)
            
            # Keep only last 100 records
            if len(self.current_portfolio['performance_history']) > 100:
                self.current_portfolio['performance_history'] = self.current_portfolio['performance_history'][-100:]
            
            print("   ✅ Portfolio state updated")
            
        except Exception as e:
            print(f"   ❌ Portfolio state update error: {e}")
    
    def calculate_portfolio_var_95(self) -> float:
        """Calculate portfolio 95% Value at Risk"""
        # Simplified VaR calculation
        portfolio_vol = self.optimization_results.get('expected_volatility', 0.15)
        return portfolio_vol * 1.645  # 95% confidence interval
    
    def calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown from performance history"""
        if not self.current_portfolio['performance_history']:
            return 0.0
        
        # Simplified max drawdown calculation
        returns = [record.get('expected_return', 0) for record in self.current_portfolio['performance_history']]
        cumulative = np.cumprod(1 + np.array(returns))
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        return abs(np.min(drawdown))
    
    def calculate_portfolio_beta(self) -> float:
        """Calculate portfolio beta relative to market"""
        # Simplified beta calculation
        portfolio_vol = self.optimization_results.get('expected_volatility', 0.15)
        market_vol = 0.15  # Assume market volatility of 15%
        
        # Assume correlation of 0.7 with market
        correlation = 0.7
        beta = correlation * (portfolio_vol / market_vol)
        
        return beta
    
    def get_portfolio_summary(self) -> Dict:
        """Get comprehensive portfolio summary"""
        return {
            'portfolio_config': self.portfolio_config,
            'current_portfolio': self.current_portfolio,
            'optimization_results': self.optimization_results,
            'asset_classes': self.asset_classes,
            'last_updated': datetime.now().isoformat()
        }

async def main():
    """Test the Enhanced Portfolio Optimization System"""
    print("📊 ENHANCED PORTFOLIO OPTIMIZATION SYSTEM")
    print("🚀 Testing portfolio optimization...")
    
    # Initialize system
    portfolio_system = EnhancedPortfolioOptimizationSystem()
    
    # Sample market data
    market_data = {
        'equities': {'recent_return': 0.12},
        'bonds': {'recent_return': 0.04},
        'commodities': {'recent_return': 0.09},
        'real_estate': {'recent_return': 0.08},
        'alternatives': {'recent_return': 0.15},
        'correlation_matrix': {
            'equities_bonds': -0.2,
            'equities_commodities': 0.3,
            'bonds_commodities': -0.1
        }
    }
    
    # Run portfolio optimization
    results = await portfolio_system.run_portfolio_optimization(market_data)
    
    print("\n📋 PORTFOLIO OPTIMIZATION RESULTS:")
    print(json.dumps(results, indent=2))
    
    print("\n📊 PORTFOLIO SUMMARY:")
    summary = portfolio_system.get_portfolio_summary()
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
