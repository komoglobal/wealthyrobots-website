#!/usr/bin/env python3
"""
Enhanced Market Data System
Comprehensive market data generation and analysis for trading strategies
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import random
import requests
from typing import Dict, List, Optional

class EnhancedMarketData:
    def __init__(self):
        print("🚀 ENHANCED MARKET DATA SYSTEM - INITIALIZING")
        
        # Market data sources
        self.data_sources = {
            'equity': ['SPY', 'QQQ', 'IWM', 'GLD', 'TLT', 'VTI', 'EFA', 'EEM'],
            'crypto': ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'UNI', 'AAVE', 'COMP'],
            'forex': ['EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 'USD/CAD'],
            'commodities': ['GOLD', 'SILVER', 'OIL', 'COPPER', 'NATURAL_GAS', 'CORN']
        }
        
        # Enhanced data parameters
        self.data_parameters = {
            'lookback_days': 252,  # Full trading year
            'update_frequency': '1min',  # More frequent updates
            'volatility_window': 20,  # Shorter volatility window
            'correlation_threshold': 0.6,  # Lower correlation threshold
            'trend_strength_threshold': 0.015,  # Lower trend threshold
            'volume_threshold': 0.1  # Lower volume threshold
        }
        
        # Market regime detection
        self.regime_detection = {
            'trending': {'enabled': True, 'threshold': 0.02},
            'mean_reverting': {'enabled': True, 'threshold': 0.01},
            'volatile': {'enabled': True, 'threshold': 0.03},
            'quiet': {'enabled': True, 'threshold': 0.005}
        }
        
        # Generate comprehensive market data
        self.market_data = self.generate_comprehensive_market_data()
        self.technical_indicators = self.calculate_technical_indicators()
        self.market_regime = self.detect_market_regime()
        
    def generate_comprehensive_market_data(self):
        """Generate comprehensive market data for all asset classes"""
        print("📊 Generating comprehensive market data...")
        
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2025-08-09', freq='D')
        n_days = len(dates)
        
        all_assets = []
        all_prices = []
        all_volumes = []
        all_returns = []
        
        # Generate data for each asset class
        for asset_class, assets in self.data_sources.items():
            for asset in assets:
                all_assets.append(f"{asset_class}_{asset}")
                
                # Generate realistic price data
                base_price = random.uniform(50, 200)
                base_return = random.uniform(0.0001, 0.001)
                base_volatility = random.uniform(0.015, 0.035)
                
                # Generate daily returns with trends and volatility clustering
                returns = np.random.normal(base_return, base_volatility, n_days)
                
                # Add volatility clustering (GARCH-like behavior)
                for i in range(1, n_days):
                    if abs(returns[i-1]) > 2 * base_volatility:
                        returns[i] *= 1.5  # Volatility spike
                
                # Add trends
                trend_strength = random.uniform(-0.0002, 0.0004)
                trend = np.linspace(0, trend_strength * n_days, n_days)
                returns += trend
                
                # Convert to prices
                prices = base_price * np.exp(np.cumsum(returns))
                
                # Generate volumes
                base_volume = random.uniform(1000000, 10000000)
                volume_volatility = random.uniform(0.3, 0.7)
                volumes = np.random.lognormal(np.log(base_volume), volume_volatility, n_days)
                
                # Add volume spikes on large price moves
                for i in range(n_days):
                    if abs(returns[i]) > 2 * base_volatility:
                        volumes[i] *= random.uniform(1.5, 3.0)
                
                all_prices.append(prices)
                all_volumes.append(volumes)
                all_returns.append(returns)
        
        # Convert to numpy arrays
        prices_array = np.array(all_prices).T
        volumes_array = np.array(all_volumes).T
        returns_array = np.array(all_returns).T
        
        # Add market-wide regime changes
        regime_changes = np.random.choice([0, 1], size=n_days, p=[0.97, 0.03])
        for i in range(n_days):
            if regime_changes[i]:
                # Market-wide volatility spike
                returns_array[i, :] *= random.uniform(1.3, 2.0)
                volumes_array[i, :] *= random.uniform(1.5, 2.5)
        
        return {
            'dates': dates,
            'assets': all_assets,
            'prices': prices_array,
            'volumes': volumes_array,
            'returns': returns_array,
            'asset_classes': self.data_sources
        }
    
    def calculate_technical_indicators(self):
        """Calculate comprehensive technical indicators"""
        print("📊 Calculating technical indicators...")
        
        prices = self.market_data['prices']
        volumes = self.market_data['volumes']
        returns = self.market_data['returns']
        
        indicators = {}
        
        for i, asset in enumerate(self.market_data['assets']):
            asset_prices = prices[:, i]
            asset_volumes = volumes[:, i]
            asset_returns = returns[:, i]
            
            indicators[asset] = {
                'moving_averages': self.calculate_moving_averages(asset_prices),
                'momentum_indicators': self.calculate_momentum_indicators(asset_prices, asset_returns),
                'volatility_indicators': self.calculate_volatility_indicators(asset_returns),
                'volume_indicators': self.calculate_volume_indicators(asset_prices, asset_volumes),
                'trend_indicators': self.calculate_trend_indicators(asset_prices),
                'oscillators': self.calculate_oscillators(asset_prices, asset_volumes)
            }
        
        return indicators
    
    def calculate_moving_averages(self, prices):
        """Calculate various moving averages"""
        try:
            if len(prices) < 50:
                return {}
            
            return {
                'sma_5': np.mean(prices[-5:]),
                'sma_10': np.mean(prices[-10:]),
                'sma_20': np.mean(prices[-20:]),
                'sma_50': np.mean(prices[-50:]),
                'ema_12': self.calculate_ema(prices, 12),
                'ema_26': self.calculate_ema(prices, 26)
            }
        except:
            return {}
    
    def calculate_ema(self, prices, period):
        """Calculate exponential moving average"""
        try:
            if len(prices) < period:
                return np.mean(prices)
            
            alpha = 2 / (period + 1)
            ema = prices[0]
            
            for price in prices[1:]:
                ema = alpha * price + (1 - alpha) * ema
            
            return ema
        except:
            return np.mean(prices)
    
    def calculate_momentum_indicators(self, prices, returns):
        """Calculate momentum indicators"""
        try:
            if len(prices) < 20:
                return {}
            
            # RSI
            gains = np.where(returns > 0, returns, 0)
            losses = np.where(returns < 0, -returns, 0)
            
            avg_gain = np.mean(gains[-14:])
            avg_loss = np.mean(losses[-14:])
            
            if avg_loss > 0:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            else:
                rsi = 100
            
            # MACD
            ema_12 = self.calculate_ema(prices, 12)
            ema_26 = self.calculate_ema(prices, 26)
            macd_line = ema_12 - ema_26
            signal_line = self.calculate_ema(np.array([macd_line]), 9)
            
            return {
                'rsi': rsi,
                'macd': macd_line,
                'macd_signal': signal_line,
                'macd_histogram': macd_line - signal_line,
                'momentum': np.mean(returns[-5:]) - np.mean(returns[-20:])
            }
        except:
            return {}
    
    def calculate_volatility_indicators(self, returns):
        """Calculate volatility indicators"""
        try:
            if len(returns) < 20:
                return {}
            
            # Bollinger Bands
            sma_20 = np.mean(returns[-20:])
            std_20 = np.std(returns[-20:])
            
            upper_band = sma_20 + (2 * std_20)
            lower_band = sma_20 - (2 * std_20)
            
            # ATR (Average True Range approximation)
            atr = np.mean(np.abs(returns[-20:]))
            
            return {
                'bollinger_upper': upper_band,
                'bollinger_lower': lower_band,
                'bollinger_width': upper_band - lower_band,
                'atr': atr,
                'volatility': std_20,
                'volatility_ratio': std_20 / np.mean(np.abs(returns[-50:])) if len(returns) >= 50 else 1.0
            }
        except:
            return {}
    
    def calculate_volume_indicators(self, prices, volumes):
        """Calculate volume indicators"""
        try:
            if len(prices) < 20:
                return {}
            
            # Volume moving average
            volume_sma = np.mean(volumes[-20:])
            
            # Price-volume trend
            pvt = np.sum(np.where(prices[1:] > prices[:-1], volumes[1:], -volumes[1:]))
            
            # On-balance volume approximation
            obv = 0
            for i in range(1, len(prices)):
                if prices[i] > prices[i-1]:
                    obv += volumes[i]
                elif prices[i] < prices[i-1]:
                    obv -= volumes[i]
            
            return {
                'volume_sma': volume_sma,
                'volume_ratio': volumes[-1] / volume_sma,
                'pvt': pvt,
                'obv': obv,
                'volume_trend': np.mean(volumes[-5:]) / np.mean(volumes[-20:])
            }
        except:
            return {}
    
    def calculate_trend_indicators(self, prices):
        """Calculate trend indicators"""
        try:
            if len(prices) < 30:
                return {}
            
            # ADX (Average Directional Index approximation)
            price_changes = np.diff(prices)
            positive_moves = np.sum(price_changes > 0)
            negative_moves = np.sum(price_changes < 0)
            
            trend_strength = abs(positive_moves - negative_moves) / len(price_changes)
            
            # Parabolic SAR approximation
            sar = prices[-1] * (1 + trend_strength * 0.02)
            
            return {
                'trend_strength': trend_strength,
                'trend_direction': 1 if positive_moves > negative_moves else -1,
                'parabolic_sar': sar,
                'linear_regression': self.calculate_linear_regression(prices)
            }
        except:
            return {}
    
    def calculate_linear_regression(self, prices):
        """Calculate linear regression slope"""
        try:
            if len(prices) < 10:
                return 0
            
            x = np.arange(len(prices))
            slope = np.polyfit(x, prices, 1)[0]
            return slope
        except:
            return 0
    
    def calculate_oscillators(self, prices, volumes):
        """Calculate oscillator indicators"""
        try:
            if len(prices) < 14:
                return {}
            
            # Stochastic oscillator
            high_14 = np.max(prices[-14:])
            low_14 = np.min(prices[-14:])
            
            if high_14 != low_14:
                k_percent = 100 * (prices[-1] - low_14) / (high_14 - low_14)
            else:
                k_percent = 50
            
            # Williams %R
            if high_14 != low_14:
                williams_r = -100 * (high_14 - prices[-1]) / (high_14 - low_14)
            else:
                williams_r = -50
            
            return {
                'stochastic_k': k_percent,
                'stochastic_d': np.mean([k_percent]),  # Simplified
                'williams_r': williams_r,
                'cci': self.calculate_cci(prices)
            }
        except:
            return {}
    
    def calculate_cci(self, prices):
        """Calculate Commodity Channel Index"""
        try:
            if len(prices) < 20:
                return 0
            
            typical_price = prices[-1]  # Simplified
            sma_tp = np.mean(prices[-20:])
            mean_deviation = np.mean(np.abs(prices[-20:] - sma_tp))
            
            if mean_deviation > 0:
                cci = (typical_price - sma_tp) / (0.015 * mean_deviation)
            else:
                cci = 0
            
            return cci
        except:
            return 0
    
    def detect_market_regime(self):
        """Detect current market regime"""
        print("📊 Detecting market regime...")
        
        try:
            # Aggregate market data
            all_returns = self.market_data['returns']
            market_returns = np.mean(all_returns, axis=1)
            
            # Calculate regime indicators
            volatility = np.std(market_returns[-20:])
            trend_strength = abs(np.mean(market_returns[-5:]) - np.mean(market_returns[-20:]))
            mean_reversion_strength = abs(market_returns[-1] - np.mean(market_returns[-20:]))
            
            # Determine regime
            if volatility > self.regime_detection['volatile']['threshold']:
                regime = 'volatile'
                confidence = min(0.9, volatility * 10)
            elif trend_strength > self.regime_detection['trending']['threshold']:
                regime = 'trending'
                confidence = min(0.9, trend_strength * 20)
            elif mean_reversion_strength > self.regime_detection['mean_reverting']['threshold']:
                regime = 'mean_reverting'
                confidence = min(0.9, mean_reversion_strength * 15)
            else:
                regime = 'quiet'
                confidence = 0.7
            
            return {
                'regime': regime,
                'confidence': confidence,
                'indicators': {
                    'volatility': volatility,
                    'trend_strength': trend_strength,
                    'mean_reversion_strength': mean_reversion_strength
                }
            }
            
        except Exception as e:
            print(f"Market regime detection error: {e}")
            return {'regime': 'unknown', 'confidence': 0.5, 'indicators': {}}
    
    def generate_trading_signals(self):
        """Generate trading signals based on market data analysis"""
        print("📊 Generating trading signals from market data...")
        
        signals = []
        
        for asset in self.market_data['assets']:
            if asset in self.technical_indicators:
                indicators = self.technical_indicators[asset]
                
                # Generate signals based on technical indicators
                asset_signals = self.analyze_asset_signals(asset, indicators)
                signals.extend(asset_signals)
        
        # Filter and rank signals
        filtered_signals = self.filter_signals(signals)
        
        print(f"📊 Generated {len(filtered_signals)} trading signals from market data")
        return filtered_signals
    
    def analyze_asset_signals(self, asset, indicators):
        """Analyze individual asset for trading signals"""
        signals = []
        
        try:
            # RSI signals
            if 'rsi' in indicators.get('momentum_indicators', {}):
                rsi = indicators['momentum_indicators']['rsi']
                if rsi < 30:  # Oversold
                    signals.append({
                        'asset': asset,
                        'signal': 'buy',
                        'confidence': min(0.8, (30 - rsi) / 30 * 0.8),
                        'indicator': 'rsi_oversold',
                        'value': rsi,
                        'strategy': 'technical_analysis'
                    })
                elif rsi > 70:  # Overbought
                    signals.append({
                        'asset': asset,
                        'signal': 'sell',
                        'confidence': min(0.8, (rsi - 70) / 30 * 0.8),
                        'indicator': 'rsi_overbought',
                        'value': rsi,
                        'strategy': 'technical_analysis'
                    })
            
            # MACD signals
            if 'macd' in indicators.get('momentum_indicators', {}):
                macd = indicators['momentum_indicators']['macd']
                macd_signal = indicators['momentum_indicators'].get('macd_signal', 0)
                
                if macd > macd_signal and macd > 0:  # Bullish crossover
                    signals.append({
                        'asset': asset,
                        'signal': 'buy',
                        'confidence': min(0.7, abs(macd - macd_signal) * 10),
                        'indicator': 'macd_bullish',
                        'value': macd,
                        'strategy': 'technical_analysis'
                    })
                elif macd < macd_signal and macd < 0:  # Bearish crossover
                    signals.append({
                        'asset': asset,
                        'signal': 'sell',
                        'confidence': min(0.7, abs(macd - macd_signal) * 10),
                        'indicator': 'macd_bearish',
                        'value': macd,
                        'strategy': 'technical_analysis'
                    })
            
            # Bollinger Bands signals
            if 'bollinger_upper' in indicators.get('volatility_indicators', {}):
                current_price = self.market_data['prices'][-1, self.market_data['assets'].index(asset)]
                bb_upper = indicators['volatility_indicators']['bollinger_upper']
                bb_lower = indicators['volatility_indicators']['bollinger_lower']
                
                if current_price < bb_lower:  # Below lower band
                    signals.append({
                        'asset': asset,
                        'signal': 'buy',
                        'confidence': min(0.8, (bb_lower - current_price) / bb_lower * 2),
                        'indicator': 'bollinger_oversold',
                        'value': current_price,
                        'strategy': 'technical_analysis'
                    })
                elif current_price > bb_upper:  # Above upper band
                    signals.append({
                        'asset': asset,
                        'signal': 'sell',
                        'confidence': min(0.8, (current_price - bb_upper) / bb_upper * 2),
                        'indicator': 'bollinger_overbought',
                        'value': current_price,
                        'strategy': 'technical_analysis'
                    })
            
            # Volume signals
            if 'volume_ratio' in indicators.get('volume_indicators', {}):
                volume_ratio = indicators['volume_indicators']['volume_ratio']
                if volume_ratio > 1.5:  # High volume
                    # Combine with price action
                    if 'momentum_indicators' in indicators:
                        momentum = indicators['momentum_indicators'].get('momentum', 0)
                        if momentum > 0:  # Price rising with volume
                            signals.append({
                                'asset': asset,
                                'signal': 'buy',
                                'confidence': min(0.7, (volume_ratio - 1) * 0.5),
                                'indicator': 'volume_breakout',
                                'value': volume_ratio,
                                'strategy': 'technical_analysis'
                            })
        
        except Exception as e:
            print(f"Asset signal analysis error for {asset}: {e}")
        
        return signals
    
    def filter_signals(self, signals):
        """Filter and rank trading signals"""
        try:
            # Filter by confidence threshold
            min_confidence = 0.3  # Lower threshold for more signals
            filtered = [s for s in signals if s['confidence'] >= min_confidence]
            
            # Sort by confidence
            filtered.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Limit number of signals
            max_signals = 20
            if len(filtered) > max_signals:
                filtered = filtered[:max_signals]
            
            return filtered
            
        except Exception as e:
            print(f"Signal filtering error: {e}")
            return signals
    
    def get_market_summary(self):
        """Get comprehensive market summary"""
        try:
            return {
                'market_regime': self.market_regime,
                'total_assets': len(self.market_data['assets']),
                'data_points': len(self.market_data['dates']),
                'last_update': datetime.now().isoformat(),
                'technical_indicators_available': len(self.technical_indicators),
                'data_quality': 'high'
            }
        except Exception as e:
            print(f"Market summary error: {e}")
            return {}

# Main execution
if __name__ == "__main__":
    market_data = EnhancedMarketData()
    signals = market_data.generate_trading_signals()
    summary = market_data.get_market_summary()
    
    print(f"\n📊 MARKET DATA SUMMARY: {summary}")
    print(f"📈 GENERATED SIGNALS: {len(signals)}")
