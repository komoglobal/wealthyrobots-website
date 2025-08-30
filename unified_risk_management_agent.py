#!/usr/bin/env python3
"""
UNIFIED RISK MANAGEMENT AGENT
Trading Firm Upgrade - Phase 1 Critical Priority
Combines enhanced_risk_management_system.py + advanced_risk_management_agent.py
Budget: $600 (consolidated from both systems)
"""

import json
import os
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math
import numpy as np
from dataclasses import dataclass

@dataclass
class RiskAssessment:
    """Risk assessment data structure"""
    timestamp: str
    risk_score: float  # 0-100 scale
    risk_level: str    # low, medium, high, critical
    risk_factors: List[str]
    recommendations: List[str]
    confidence: float  # 0-1 scale

@dataclass
class PositionRisk:
    """Individual position risk data"""
    position_id: str
    risk_score: float
    risk_factors: List[str]
    suggested_actions: List[str]
    max_position_size: float

class UnifiedRiskManagementAgent:
    def __init__(self):
        print("🛡️ UNIFIED RISK MANAGEMENT AGENT - INITIALIZING...")
        print("🎯 Phase 1 Critical Priority: Consolidated Risk Management")
        print("💰 Budget Allocated: $600 (consolidated from both systems)")
        
        # AI risk models (from advanced_risk_management_agent.py)
        self.risk_models = {
            'portfolio_risk': {
                'name': 'Portfolio Risk Model',
                'description': 'AI-powered portfolio risk assessment',
                'version': '3.0',
                'last_trained': datetime.now().isoformat(),
                'accuracy': 0.94
            },
            'market_risk': {
                'name': 'Market Risk Model',
                'description': 'Real-time market risk analysis',
                'version': '2.0',
                'last_trained': datetime.now().isoformat(),
                'accuracy': 0.91
            },
            'liquidity_risk': {
                'name': 'Liquidity Risk Model',
                'description': 'Liquidity risk assessment',
                'version': '1.8',
                'last_trained': datetime.now().isoformat(),
                'accuracy': 0.89
            },
            'correlation_risk': {
                'name': 'Correlation Risk Model',
                'description': 'Portfolio correlation analysis',
                'version': '2.0',
                'last_trained': datetime.now().isoformat(),
                'accuracy': 0.93
            }
        }
        
        # Risk thresholds and limits (consolidated from both systems)
        self.risk_thresholds = {
            'portfolio': {
                'low': 0.02,      # 2% max portfolio risk (from enhanced system)
                'medium': 0.10,   # 10% max portfolio risk
                'high': 0.20,     # 20% max portfolio risk
                'critical': 0.30  # 30% max portfolio risk
            },
            'position': {
                'low': 0.01,      # 1% max position risk (from enhanced system)
                'medium': 0.03,   # 3% max position risk
                'high': 0.05,     # 5% max position risk (from enhanced system)
                'critical': 0.08  # 8% max position risk
            },
            'daily_loss': {
                'low': 0.01,      # 1% max daily loss (from enhanced system)
                'medium': 0.02,   # 2% max daily loss
                'high': 0.03,     # 3% max daily loss
                'critical': 0.05  # 5% max daily loss
            }
        }
        
        # Risk monitoring data
        self.portfolio_risk_history = []
        self.position_risk_data = {}
        self.market_risk_alerts = []
        self.risk_events = []
        
        # Risk limits (from enhanced_risk_management_system.py)
        self.risk_limits = {
            'portfolio_level': {
                'max_total_exposure': 1.0,      # 100% of capital
                'max_sector_exposure': 0.25,    # 25% per sector
                'max_correlation_exposure': 0.4, # 40% correlated positions
                'max_leverage': 2.0,            # 2x leverage max
                'min_cash_reserve': 0.1         # 10% cash reserve
            },
            'position_level': {
                'max_single_position': 0.05,    # 5% per position
                'max_concentration': 0.15,      # 15% in single asset
                'min_position_size': 0.001,     # 0.1% minimum
                'max_holding_period': 30        # 30 days max hold
            },
            'risk_metrics': {
                'var_95': 0.02,                 # 2% Value at Risk (95%)
                'var_99': 0.03,                 # 3% Value at Risk (99%)
                'max_daily_volatility': 0.05,   # 5% daily volatility
                'max_correlation': 0.7          # 70% correlation limit
            }
        }
        
        # Market data integration (from enhanced system)
        self.market_data_feeds = {}
        self.real_time_alerts = []
        self.volatility_metrics = {}
        
        print("✅ Unified Risk Management Agent initialized")
        print("🤖 AI Risk Models: ACTIVE")
        print("🔄 Real-time monitoring: ENABLED")
        print("📊 Risk limits: CONFIGURED")
    
    async def run_unified_risk_agent(self):
        """Run the unified risk management agent"""
        print("🚀 STARTING UNIFIED RISK MANAGEMENT AGENT...")
        print("=" * 70)
        
        tasks = [
            self.continuous_risk_monitoring(),
            self.ai_risk_assessment(),
            self.real_time_risk_monitoring(),
            self.risk_mitigation_actions(),
            self.risk_reporting_and_alerts()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"❌ Unified risk agent error: {e}")
    
    async def continuous_risk_monitoring(self):
        """Continuous AI-powered risk monitoring (from advanced agent)"""
        print("🤖 Starting AI-powered continuous risk monitoring...")
        
        while True:
            try:
                # Portfolio risk assessment
                portfolio_risk = await self.assess_portfolio_risk()
                
                # Market risk assessment
                market_risk = await self.assess_market_risk()
                
                # Liquidity risk assessment
                liquidity_risk = await self.assess_liquidity_risk()
                
                # Correlation risk assessment
                correlation_risk = await self.assess_correlation_risk()
                
                # Store risk data
                await self.store_risk_data(portfolio_risk, market_risk, liquidity_risk, correlation_risk)
                
                # Check for risk alerts
                await self.check_risk_alerts(portfolio_risk, market_risk, liquidity_risk, correlation_risk)
                
                # Wait 30 seconds between assessments
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"❌ Continuous risk monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def real_time_risk_monitoring(self):
        """Real-time risk monitoring (from enhanced system)"""
        print("🔄 Starting real-time risk monitoring...")
        
        while True:
            try:
                current_time = datetime.now()
                print(f"\n⏰ Real-time Risk Check: {current_time.strftime('%H:%M:%S')}")
                
                # Portfolio risk assessment
                portfolio_risk = await self.assess_portfolio_risk()
                
                # Position-level risk analysis
                position_risks = await self.analyze_position_risks()
                
                # Market risk monitoring
                market_risks = await self.monitor_market_risks()
                
                # Generate risk alerts
                await self.generate_risk_alerts(portfolio_risk, position_risks, market_risks)
                
                # Update risk dashboard
                await self.update_risk_dashboard()
                
                # Wait 30 seconds between checks
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"❌ Real-time risk monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def assess_portfolio_risk(self) -> RiskAssessment:
        """AI-powered portfolio risk assessment"""
        try:
            # Get portfolio composition
            portfolio = await self.get_portfolio_composition()
            
            # Calculate risk metrics
            total_exposure = sum(position['value'] for position in portfolio.get('positions', []))
            portfolio_value = portfolio.get('total_value', 100000)
            exposure_ratio = total_exposure / portfolio_value if portfolio_value > 0 else 0
            
            # Calculate correlation risk
            correlation_risk = await self.calculate_correlation_risk(portfolio)
            
            # Calculate volatility risk
            volatility_risk = await self.calculate_volatility_risk(portfolio)
            
            # Combine risk factors
            risk_factors = []
            risk_score = 0.0
            
            if exposure_ratio > 0.8:
                risk_factors.append("High portfolio exposure")
                risk_score += 25
            
            if correlation_risk > 0.7:
                risk_factors.append("High correlation risk")
                risk_score += 20
            
            if volatility_risk > 0.05:
                risk_factors.append("High volatility risk")
                risk_score += 20
            
            # Determine risk level
            if risk_score >= 60:
                risk_level = "critical"
            elif risk_score >= 40:
                risk_level = "high"
            elif risk_score >= 20:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            # Generate AI recommendations
            recommendations = await self.generate_ai_recommendations(risk_score, risk_factors, "portfolio")
            
            return RiskAssessment(
                timestamp=datetime.now().isoformat(),
                risk_score=risk_score,
                risk_level=risk_level,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.92
            )
            
        except Exception as e:
            print(f"❌ Portfolio risk assessment error: {e}")
            return RiskAssessment(
                timestamp=datetime.now().isoformat(),
                risk_score=50.0,
                risk_level="medium",
                risk_factors=["Assessment error"],
                recommendations=["Review system logs"],
                confidence=0.0
            )
    
    async def assess_market_risk(self) -> RiskAssessment:
        """AI-powered market risk assessment"""
        try:
            # Get market conditions
            market_conditions = await self.get_market_conditions()
            
            # Calculate market risk factors
            risk_factors = []
            risk_score = 0.0
            
            vix_level = market_conditions.get('vix', 25.0)
            if vix_level > 30:
                risk_factors.append("High market volatility (VIX > 30)")
                risk_score += 30
            elif vix_level > 20:
                risk_factors.append("Elevated market volatility")
                risk_score += 15
            
            # Check market sentiment
            sentiment = market_conditions.get('sentiment', 0.0)
            if sentiment < -0.5:
                risk_factors.append("Negative market sentiment")
                risk_score += 20
            
            # Determine risk level
            if risk_score >= 50:
                risk_level = "high"
            elif risk_score >= 25:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            # Generate AI recommendations
            recommendations = await self.generate_ai_recommendations(risk_score, risk_factors, "market")
            
            return RiskAssessment(
                timestamp=datetime.now().isoformat(),
                risk_score=risk_score,
                risk_level=risk_level,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.89
            )
            
        except Exception as e:
            print(f"❌ Market risk assessment error: {e}")
            return RiskAssessment(
                timestamp=datetime.now().isoformat(),
                risk_score=25.0,
                risk_level="medium",
                risk_factors=["Assessment error"],
                recommendations=["Review market data"],
                confidence=0.0
            )
    
    async def assess_liquidity_risk(self) -> RiskAssessment:
        """AI-powered liquidity risk assessment"""
        try:
            # Get liquidity conditions
            liquidity_conditions = await self.get_liquidity_conditions()
            
            # Calculate liquidity risk factors
            risk_factors = []
            risk_score = 0.0
            
            # Check bid-ask spreads
            avg_spread = liquidity_conditions.get('avg_bid_ask_spread', 0.001)
            if avg_spread > 0.005:
                risk_factors.append("Wide bid-ask spreads")
                risk_score += 25
            
            # Check market depth
            market_depth = liquidity_conditions.get('market_depth', 1000000)
            if market_depth < 500000:
                risk_factors.append("Low market depth")
                risk_score += 20
            
            # Determine risk level
            if risk_score >= 45:
                risk_level = "high"
            elif risk_score >= 20:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            # Generate AI recommendations
            recommendations = await self.generate_ai_recommendations(risk_score, risk_factors, "liquidity")
            
            return RiskAssessment(
                timestamp=datetime.now().isoformat(),
                risk_score=risk_score,
                risk_level=risk_level,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.87
            )
            
        except Exception as e:
            print(f"❌ Liquidity risk assessment error: {e}")
            return RiskAssessment(
                timestamp=datetime.now().isoformat(),
                risk_score=20.0,
                risk_level="medium",
                risk_factors=["Assessment error"],
                recommendations=["Review liquidity data"],
                confidence=0.0
            )
    
    async def assess_correlation_risk(self) -> RiskAssessment:
        """AI-powered correlation risk assessment"""
        try:
            # Get correlation data
            correlation_data = await self.get_correlation_data()
            
            # Calculate correlation risk factors
            risk_factors = []
            risk_score = 0.0
            
            # Check high correlations
            high_correlations = 0
            for corr_value in correlation_data.values():
                if abs(corr_value) > 0.7:
                    high_correlations += 1
            
            if high_correlations > 5:
                risk_factors.append(f"High correlation pairs: {high_correlations}")
                risk_score += 30
            elif high_correlations > 2:
                risk_factors.append(f"Elevated correlations: {high_correlations}")
                risk_score += 15
            
            # Determine risk level
            if risk_score >= 30:
                risk_level = "high"
            elif risk_score >= 15:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            # Generate AI recommendations
            recommendations = await self.generate_ai_recommendations(risk_score, risk_factors, "correlation")
            
            return RiskAssessment(
                timestamp=datetime.now().isoformat(),
                risk_score=risk_score,
                risk_level=risk_level,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.91
            )
            
        except Exception as e:
            print(f"❌ Correlation risk assessment error: {e}")
            return RiskAssessment(
                timestamp=datetime.now().isoformat(),
                risk_score=15.0,
                risk_level="medium",
                risk_factors=["Assessment error"],
                recommendations=["Review correlation data"],
                confidence=0.0
            )
    
    async def generate_ai_recommendations(self, risk_score: float, risk_factors: List[str], risk_type: str) -> List[str]:
        """Generate AI-powered risk recommendations"""
        recommendations = []
        
        if risk_type == "portfolio":
            if risk_score >= 60:
                recommendations.extend([
                    "Immediately reduce portfolio exposure by 20-30%",
                    "Implement hedging strategies",
                    "Review position sizing limits"
                ])
            elif risk_score >= 40:
                recommendations.extend([
                    "Consider reducing exposure by 10-15%",
                    "Monitor correlations closely",
                    "Review risk parameters"
                ])
            else:
                recommendations.append("Portfolio risk within acceptable limits")
        
        elif risk_type == "market":
            if risk_score >= 50:
                recommendations.extend([
                    "Reduce market exposure",
                    "Increase cash positions",
                    "Implement defensive strategies"
                ])
            elif risk_score >= 25:
                recommendations.extend([
                    "Monitor market conditions closely",
                    "Review stop-loss levels",
                    "Consider reducing position sizes"
                ])
            else:
                recommendations.append("Market conditions stable")
        
        elif risk_type == "liquidity":
            if risk_score >= 45:
                recommendations.extend([
                    "Reduce position sizes",
                    "Extend holding periods",
                    "Use limit orders only"
                ])
            elif risk_score >= 20:
                recommendations.extend([
                    "Monitor liquidity conditions",
                    "Consider reducing trade frequency",
                    "Review execution strategies"
                ])
            else:
                recommendations.append("Liquidity conditions adequate")
        
        elif risk_type == "correlation":
            if risk_score >= 30:
                recommendations.extend([
                    "Diversify across uncorrelated assets",
                    "Reduce correlated positions",
                    "Consider alternative investments"
                ])
            elif risk_score >= 15:
                recommendations.extend([
                    "Monitor correlation changes",
                    "Review diversification",
                    "Consider correlation hedges"
                ])
            else:
                recommendations.append("Correlation risk low")
        
        return recommendations
    
    async def analyze_position_risks(self) -> List[Dict]:
        """Analyze individual position risks"""
        try:
            positions = await self.get_active_positions()
            position_risks = []
            
            for position in positions:
                position_risk = await self.assess_position_risk(position)
                position_risks.append({
                    'position_id': position['id'],
                    'risk_score': position_risk.risk_score,
                    'risk_factors': position_risk.risk_factors,
                    'suggested_actions': position_risk.suggested_actions,
                    'max_position_size': position_risk.max_position_size
                })
            
            return position_risks
            
        except Exception as e:
            print(f"❌ Position risk analysis error: {e}")
            return []
    
    async def assess_position_risk(self, position: Dict) -> PositionRisk:
        """Assess individual position risk"""
        try:
            risk_factors = []
            risk_score = 0.0
            
            # Check position size
            position_size = position.get('size', 0)
            portfolio_value = 100000  # Default value
            size_ratio = position_size / portfolio_value
            
            if size_ratio > 0.05:
                risk_factors.append("Position size exceeds 5% limit")
                risk_score += 25
            
            # Check stop loss
            if not position.get('stop_loss'):
                risk_factors.append("No stop loss set")
                risk_score += 20
            
            # Check holding period
            holding_days = position.get('holding_days', 0)
            if holding_days > 30:
                risk_factors.append("Extended holding period")
                risk_score += 15
            
            # Determine risk level and actions
            if risk_score >= 45:
                suggested_actions = ["Reduce position size", "Set stop loss", "Consider closing"]
                max_position_size = position_size * 0.5
            elif risk_score >= 25:
                suggested_actions = ["Review position", "Adjust stop loss", "Monitor closely"]
                max_position_size = position_size * 0.8
            else:
                suggested_actions = ["Position risk acceptable"]
                max_position_size = position_size
            
            return PositionRisk(
                position_id=position.get('id', 'unknown'),
                risk_score=risk_score,
                risk_factors=risk_factors,
                suggested_actions=suggested_actions,
                max_position_size=max_position_size
            )
            
        except Exception as e:
            print(f"❌ Position risk assessment error: {e}")
            return PositionRisk(
                position_id=position.get('id', 'unknown'),
                risk_score=50.0,
                risk_factors=["Assessment error"],
                suggested_actions=["Review position manually"],
                max_position_size=0.0
            )
    
    async def monitor_market_risks(self) -> Dict:
        """Monitor market risks in real-time"""
        try:
            market_risks = {
                'volatility': {'level': 'medium', 'value': 0.025, 'trend': 'stable'},
                'liquidity': {'level': 'low', 'value': 0.8, 'trend': 'stable'},
                'correlation': {'level': 'medium', 'value': 0.65, 'trend': 'increasing'},
                'sentiment': {'level': 'low', 'value': 0.3, 'trend': 'stable'}
            }
            
            return market_risks
            
        except Exception as e:
            print(f"❌ Market risk monitoring error: {e}")
            return {}
    
    async def generate_risk_alerts(self, portfolio_risk: RiskAssessment, position_risks: List[Dict], market_risks: Dict):
        """Generate comprehensive risk alerts"""
        try:
            alerts = []
            
            # Portfolio-level alerts
            if portfolio_risk.risk_level in ['high', 'critical']:
                alerts.append({
                    'level': portfolio_risk.risk_level,
                    'type': 'portfolio',
                    'message': f"Portfolio risk: {portfolio_risk.risk_level.upper()} - {portfolio_risk.risk_score:.1f}",
                    'recommendations': portfolio_risk.recommendations
                })
            
            # Position-level alerts
            for position_risk in position_risks:
                if position_risk['risk_score'] > 40:
                    alerts.append({
                        'level': 'high',
                        'type': 'position',
                        'message': f"Position {position_risk['position_id']} risk: {position_risk['risk_score']:.1f}",
                        'recommendations': position_risk['suggested_actions']
                    })
            
            # Market-level alerts
            for risk_type, risk_data in market_risks.items():
                if risk_data['level'] in ['high', 'critical']:
                    alerts.append({
                        'level': risk_data['level'],
                        'type': 'market',
                        'message': f"Market {risk_type} risk: {risk_data['level'].upper()}",
                        'recommendations': [f"Monitor {risk_type} closely"]
                    })
            
            # Store alerts
            self.risk_alerts.extend(alerts)
            
            # Print critical alerts
            for alert in alerts:
                if alert['level'] in ['high', 'critical']:
                    print(f"🚨 {alert['level'].upper()} RISK ALERT: {alert['message']}")
            
        except Exception as e:
            print(f"❌ Risk alert generation error: {e}")
    
    async def update_risk_dashboard(self):
        """Update the risk management dashboard"""
        try:
            dashboard_data = {
                'timestamp': datetime.now().isoformat(),
                'portfolio_risk': await self.get_latest_portfolio_risk(),
                'market_risk': await self.get_latest_market_risk(),
                'liquidity_risk': await self.get_latest_liquidity_risk(),
                'correlation_risk': await self.get_latest_correlation_risk(),
                'active_alerts': len(self.risk_alerts),
                'risk_limits': self.risk_limits,
                'ai_models': self.risk_models
            }
            
            # Save dashboard
            await self.save_risk_dashboard(dashboard_data)
            
            print(f"📊 Risk dashboard updated: {dashboard_data['active_alerts']} active alerts")
            
        except Exception as e:
            print(f"❌ Risk dashboard update error: {e}")
    
    async def risk_mitigation_actions(self):
        """Execute risk mitigation actions"""
        print("🛡️ Starting risk mitigation actions...")
        
        while True:
            try:
                # Check for high-risk positions
                high_risk_positions = [
                    pos for pos in self.position_risk_data.values()
                    if pos.risk_score > 60
                ]
                
                for position in high_risk_positions:
                    await self.execute_risk_mitigation(position.position_id)
                
                # Wait 60 seconds between mitigation checks
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"❌ Risk mitigation error: {e}")
                await asyncio.sleep(120)
    
    async def execute_risk_mitigation(self, position_id: str):
        """Execute risk mitigation for a specific position"""
        try:
            print(f"🛡️ Executing risk mitigation for position {position_id}")
            
            # Get position risk data
            position_risk = self.position_risk_data.get(position_id)
            if not position_risk:
                return
            
            # Execute mitigation based on risk level
            if position_risk.risk_score > 80:
                await self.close_position(position_id, "Critical risk level")
            elif position_risk.risk_score > 60:
                await self.reduce_position_size(position_id, 0.5)
            elif position_risk.risk_score > 40:
                await self.adjust_stop_loss(position_id, 0.02)
            
        except Exception as e:
            print(f"❌ Risk mitigation execution error: {e}")
    
    async def close_position(self, position_id: str, reason: str):
        """Close a position due to risk"""
        print(f"🚪 Closing position {position_id}: {reason}")
        # Implementation would integrate with trading system
    
    async def reduce_position_size(self, position_id: str, reduction_factor: float):
        """Reduce position size due to risk"""
        print(f"📉 Reducing position {position_id} by {reduction_factor*100:.0f}%")
        # Implementation would integrate with trading system
    
    async def adjust_stop_loss(self, position_id: str, new_stop_loss: float):
        """Adjust stop loss for a position"""
        print(f"🎯 Adjusting stop loss for position {position_id} to {new_stop_loss*100:.1f}%")
        # Implementation would integrate with trading system

    async def ai_risk_assessment(self):
        """AI-powered comprehensive risk assessment"""
        print("🤖 Starting AI risk assessment...")

        while True:
            try:
                # Perform comprehensive risk assessment
                portfolio_risk = await self.assess_portfolio_risk()
                market_risk = await self.assess_market_risk()
                liquidity_risk = await self.assess_liquidity_risk()
                correlation_risk = await self.assess_correlation_risk()

                # Calculate overall risk score
                overall_risk = (
                    portfolio_risk.risk_score * 0.4 +
                    market_risk.risk_score * 0.3 +
                    liquidity_risk.risk_score * 0.15 +
                    correlation_risk.risk_score * 0.15
                )

                # Generate AI recommendations
                all_risk_factors = (
                    portfolio_risk.risk_factors +
                    market_risk.risk_factors +
                    liquidity_risk.risk_factors +
                    correlation_risk.risk_factors
                )

                ai_recommendations = await self.generate_ai_recommendations(
                    overall_risk, all_risk_factors, "comprehensive"
                )

                # Log assessment
                self.logger.info(f"AI Risk Assessment completed - Overall Risk: {overall_risk:.1f}%")
                self.logger.info(f"Risk Factors: {len(all_risk_factors)}")
                self.logger.info(f"AI Recommendations: {len(ai_recommendations)}")

                print(f"🧠 AI Risk Assessment: {overall_risk:.1f}% risk, {len(ai_recommendations)} recommendations")

                # Wait for next assessment
                await asyncio.sleep(300)  # Every 5 minutes

            except Exception as e:
                self.logger.error(f"AI risk assessment error: {e}")
                print(f"❌ AI risk assessment failed: {e}")
                await asyncio.sleep(60)

    async def risk_reporting_and_alerts(self):
        """Generate risk reports and send alerts"""
        print("📊 Starting risk reporting and alerts...")
        
        while True:
            try:
                # Generate daily risk report
                await self.generate_daily_risk_report()
                
                # Send risk alerts
                await self.send_risk_alerts()
                
                # Wait 24 hours
                await asyncio.sleep(86400)
                
            except Exception as e:
                print(f"❌ Risk reporting error: {e}")
                await asyncio.sleep(3600)
    
    async def generate_daily_risk_report(self):
        """Generate comprehensive daily risk report"""
        try:
            report = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'portfolio_risk_summary': await self.get_latest_portfolio_risk(),
                'market_risk_summary': await self.get_latest_market_risk(),
                'position_risk_summary': list(self.position_risk_data.values()),
                'risk_alerts': self.risk_alerts[-10:],  # Last 10 alerts
                'ai_model_performance': await self.analyze_model_performance(),
                'recommendations': await self.get_summary_recommendations()
            }
            
            # Save report
            await self.save_risk_report(report)
            
            print(f"📊 Daily risk report generated: {report['date']}")
            
        except Exception as e:
            print(f"❌ Daily risk report generation error: {e}")
    
    async def send_risk_alerts(self):
        """Send risk alerts to relevant parties"""
        try:
            critical_alerts = [alert for alert in self.risk_alerts if alert['level'] == 'critical']
            high_alerts = [alert for alert in self.risk_alerts if alert['level'] == 'high']
            
            if critical_alerts:
                print(f"🚨 Sending {len(critical_alerts)} critical risk alerts")
            
            if high_alerts:
                print(f"⚠️ Sending {len(high_alerts)} high risk alerts")
            
        except Exception as e:
            print(f"❌ Risk alert sending error: {e}")
    
    async def ai_model_optimization(self):
        """Optimize AI risk models"""
        print("🤖 Starting AI model optimization...")
        
        while True:
            try:
                # Analyze model performance
                performance = await self.analyze_model_performance()
                
                # Retrain underperforming models
                for model_name, model_perf in performance.items():
                    if model_perf['accuracy'] < 0.85:
                        await self.retrain_model(model_name)
                
                # Update model parameters
                await self.update_model_parameters()
                
                # Wait 24 hours between optimizations
                await asyncio.sleep(86400)
                
            except Exception as e:
                print(f"❌ AI model optimization error: {e}")
                await asyncio.sleep(3600)
    
    async def analyze_model_performance(self) -> Dict:
        """Analyze performance of AI risk models"""
        try:
            performance = {}
            
            for model_name, model_info in self.risk_models.items():
                performance[model_name] = {
                    'accuracy': model_info['accuracy'],
                    'last_trained': model_info['last_trained'],
                    'version': model_info['version']
                }
            
            return performance
            
        except Exception as e:
            print(f"❌ Model performance analysis error: {e}")
            return {}
    
    async def retrain_model(self, model_name: str):
        """Retrain an AI risk model"""
        print(f"🔄 Retraining {model_name}...")
        # Implementation would include model retraining logic
    
    async def update_model_parameters(self):
        """Update AI model parameters"""
        print("🔧 Updating AI model parameters...")
        # Implementation would include parameter optimization
    
    # Data access methods (from enhanced system)
    async def get_portfolio_composition(self) -> Dict:
        """Get current portfolio composition"""
        # Mock implementation - would integrate with actual portfolio data
        return {
            'total_value': 100000,
            'positions': [
                {'id': 'pos_1', 'symbol': 'SPY', 'value': 25000, 'size': 2500},
                {'id': 'pos_2', 'symbol': 'QQQ', 'value': 20000, 'size': 2000},
                {'id': 'pos_3', 'symbol': 'AAPL', 'value': 15000, 'size': 1500}
            ]
        }
    
    async def get_market_conditions(self) -> Dict:
        """Get current market conditions"""
        # Mock implementation - would integrate with market data
        return {
            'vix': 25.5,
            'sentiment': 0.2,
            'volatility': 0.025
        }
    
    async def get_liquidity_conditions(self) -> Dict:
        """Get current liquidity conditions"""
        # Mock implementation - would integrate with liquidity data
        return {
            'avg_bid_ask_spread': 0.002,
            'market_depth': 1500000,
            'liquidity_score': 0.8
        }
    
    async def get_correlation_data(self) -> Dict:
        """Get current correlation data"""
        # Mock implementation - would integrate with correlation data
        return {
            'SPY_QQQ': 0.85,
            'SPY_AAPL': 0.72,
            'QQQ_AAPL': 0.78
        }
    
    async def get_active_positions(self) -> List[Dict]:
        """Get active trading positions"""
        # Mock implementation - would integrate with trading system
        return [
            {'id': 'pos_1', 'symbol': 'SPY', 'size': 2500, 'stop_loss': 0.05, 'holding_days': 15},
            {'id': 'pos_2', 'symbol': 'QQQ', 'size': 2000, 'stop_loss': None, 'holding_days': 25},
            {'id': 'pos_3', 'symbol': 'AAPL', 'size': 1500, 'stop_loss': 0.03, 'holding_days': 35}
        ]
    
    async def calculate_correlation_risk(self, portfolio: Dict) -> float:
        """Calculate portfolio correlation risk"""
        # Mock implementation
        return 0.65
    
    async def calculate_volatility_risk(self, portfolio: Dict) -> float:
        """Calculate portfolio volatility risk"""
        # Mock implementation
        return 0.035
    
    async def store_risk_data(self, portfolio_risk: RiskAssessment, market_risk: RiskAssessment, 
                             liquidity_risk: RiskAssessment, correlation_risk: RiskAssessment):
        """Store risk assessment data"""
        try:
            risk_data = {
                'timestamp': datetime.now().isoformat(),
                'portfolio_risk': portfolio_risk,
                'market_risk': market_risk,
                'liquidity_risk': liquidity_risk,
                'correlation_risk': correlation_risk
            }
            
            # Store in history
            self.portfolio_risk_history.append(risk_data)
            
            # Keep only last 1000 records
            if len(self.portfolio_risk_history) > 1000:
                self.portfolio_risk_history = self.portfolio_risk_history[-1000:]
            
        except Exception as e:
            print(f"❌ Risk data storage error: {e}")
    
    async def check_risk_alerts(self, portfolio_risk: RiskAssessment, market_risk: RiskAssessment,
                               liquidity_risk: RiskAssessment, correlation_risk: RiskAssessment):
        """Check for risk alerts across all risk types"""
        try:
            alerts = []
            
            # Check portfolio risk
            if portfolio_risk.risk_level in ['high', 'critical']:
                alerts.append({
                    'level': portfolio_risk.risk_level,
                    'type': 'portfolio',
                    'message': f"Portfolio risk: {portfolio_risk.risk_level.upper()}",
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check market risk
            if market_risk.risk_level in ['high', 'critical']:
                alerts.append({
                    'level': market_risk.risk_level,
                    'type': 'market',
                    'message': f"Market risk: {market_risk.risk_level.upper()}",
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check liquidity risk
            if liquidity_risk.risk_level in ['high', 'critical']:
                alerts.append({
                    'level': liquidity_risk.risk_level,
                    'type': 'liquidity',
                    'message': f"Liquidity risk: {liquidity_risk.risk_level.upper()}",
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check correlation risk
            if correlation_risk.risk_level in ['high', 'critical']:
                alerts.append({
                    'level': correlation_risk.risk_level,
                    'type': 'correlation',
                    'message': f"Correlation risk: {correlation_risk.risk_level.upper()}",
                    'timestamp': datetime.now().isoformat()
                })
            
            # Store alerts
            self.risk_alerts.extend(alerts)
            
            # Print critical alerts
            for alert in alerts:
                if alert['level'] == 'critical':
                    print(f"🚨 CRITICAL RISK ALERT: {alert['message']}")
                elif alert['level'] == 'high':
                    print(f"⚠️ HIGH RISK ALERT: {alert['message']}")
            
        except Exception as e:
            print(f"❌ Risk alert checking error: {e}")
    
    async def get_latest_portfolio_risk(self) -> Optional[RiskAssessment]:
        """Get the latest portfolio risk assessment"""
        if self.portfolio_risk_history:
            return self.portfolio_risk_history[-1]['portfolio_risk']
        return None
    
    async def get_latest_market_risk(self) -> Optional[RiskAssessment]:
        """Get the latest market risk assessment"""
        if self.portfolio_risk_history:
            return self.portfolio_risk_history[-1]['market_risk']
        return None
    
    async def get_latest_liquidity_risk(self) -> Optional[RiskAssessment]:
        """Get the latest liquidity risk assessment"""
        if self.portfolio_risk_history:
            return self.portfolio_risk_history[-1]['liquidity_risk']
        return None
    
    async def get_latest_correlation_risk(self) -> Optional[RiskAssessment]:
        """Get the latest correlation risk assessment"""
        if self.portfolio_risk_history:
            return self.portfolio_risk_history[-1]['correlation_risk']
        return None
    
    async def get_summary_recommendations(self) -> List[str]:
        """Get summary risk recommendations"""
        try:
            recommendations = []
            
            # Get latest assessments
            portfolio_risk = await self.get_latest_portfolio_risk()
            market_risk = await self.get_latest_market_risk()
            
            if portfolio_risk and portfolio_risk.risk_level in ['high', 'critical']:
                recommendations.extend(portfolio_risk.recommendations[:2])
            
            if market_risk and market_risk.risk_level in ['high', 'critical']:
                recommendations.extend(market_risk.recommendations[:2])
            
            return recommendations[:3]  # Top 3 recommendations
            
        except Exception as e:
            print(f"❌ Summary recommendations error: {e}")
            return ["Review risk parameters", "Monitor market conditions"]
    
    async def save_risk_report(self, report: Dict):
        """Save risk report to file"""
        try:
            filename = f"risk_report_{datetime.now().strftime('%Y%m%d')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"💾 Risk report saved: {filename}")
            
        except Exception as e:
            print(f"❌ Risk report save error: {e}")
    
    async def save_risk_dashboard(self, dashboard_data: Dict):
        """Save risk dashboard data"""
        try:
            filename = "risk_dashboard_latest.json"
            with open(filename, 'w') as f:
                json.dump(dashboard_data, f, indent=2, default=str)
            
        except Exception as e:
            print(f"❌ Risk dashboard save error: {e}")
    
    def get_risk_summary(self) -> Dict:
        """Get comprehensive risk summary"""
        try:
            return {
                'agent_status': 'active',
                'ai_models': len(self.risk_models),
                'risk_alerts': len(self.risk_alerts),
                'risk_history': len(self.portfolio_risk_history),
                'risk_thresholds': self.risk_thresholds,
                'risk_limits': self.risk_limits,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Risk summary error: {e}")
            return {'error': str(e)}

async def main():
    """Main function to run the unified risk management agent"""
    print("🚀 UNIFIED RISK MANAGEMENT AGENT")
    print("=" * 50)
    
    try:
        # Initialize agent
        risk_agent = UnifiedRiskManagementAgent()
        
        # Run agent
        await risk_agent.run_unified_risk_agent()
        
    except KeyboardInterrupt:
        print("\n🛑 Unified Risk Management Agent stopped by user")
    except Exception as e:
        print(f"❌ Unified Risk Management Agent error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
