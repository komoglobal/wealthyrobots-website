#!/usr/bin/env python3
"""
Empire Predictive Analytics System
Provides predictive insights for trading optimization and risk management
"""

import json
import os
import time
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics

class EmpirePredictiveAnalytics:
    def __init__(self):
        self.transaction_history = deque(maxlen=1000)  # Last 1000 transactions
        self.error_patterns = defaultdict(int)
        self.success_patterns = defaultdict(int)
        self.system_metrics = {}
        self.predictions = []

    def analyze_transaction_history(self):
        """Analyze transaction patterns for predictive insights"""
        if not os.path.exists('logs/hybrid_empire_20250826.log'):
            return "No transaction history available"

        with open('logs/hybrid_empire_20250826.log', 'r') as f:
            content = f.read()

        # Extract transaction patterns
        transactions = []
        lines = content.split('\n')

        for line in lines:
            if 'Transaction submitted' in line or 'Opt-in submitted' in line:
                transactions.append({
                    'timestamp': line[:19] if len(line) > 19 else 'unknown',
                    'type': 'optin' if 'Opt-in' in line else 'swap',
                    'status': 'unknown'
                })

        # Analyze patterns
        analysis = {
            'total_transactions': len(transactions),
            'success_rate': self._calculate_success_rate(content),
            'peak_hours': self._identify_peak_hours(transactions),
            'error_patterns': self._analyze_error_patterns(content),
            'performance_trends': self._analyze_performance_trends(transactions),
            'recommendations': self._generate_recommendations(content, transactions)
        }

        return analysis

    def _calculate_success_rate(self, content):
        """Calculate transaction success rate"""
        successes = content.count('✅ Transaction submitted') + content.count('✅ Opt-in submitted')
        failures = content.count('❌ Transaction submission failed') + content.count('❌ Opt-in failed')

        total = successes + failures
        if total == 0:
            return 0.0

        return round((successes / total) * 100, 2)

    def _identify_peak_hours(self, transactions):
        """Identify peak trading hours"""
        hour_counts = defaultdict(int)

        for tx in transactions:
            try:
                # Extract hour from timestamp
                if len(tx['timestamp']) >= 13:  # Format: YYYY-MM-DD HH:MM
                    hour = tx['timestamp'][11:13]
                    hour_counts[hour] += 1
            except (KeyError, IndexError, TypeError) as e:
                # Skip malformed transaction data
                continue
            except Exception as e:
                print(f"   ⚠️ Unexpected error processing transaction timestamp: {e}")
                continue

        # Find top 3 peak hours
        peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        return [f"{hour}:00 ({count} transactions)" for hour, count in peak_hours]

    def _analyze_error_patterns(self, content):
        """Analyze common error patterns"""
        error_patterns = {}

        # Common error patterns
        errors_to_check = [
            'invalid ApplicationArgs index',
            'invalid Accounts index',
            'cannot fetch key',
            'logic eval error',
            'TransactionPool.Remember'
        ]

        for error in errors_to_check:
            count = content.count(error)
            if count > 0:
                error_patterns[error] = count

        return error_patterns

    def _analyze_performance_trends(self, transactions):
        """Analyze performance trends over time"""
        if len(transactions) < 10:
            return {
                'trend': 'INSUFFICIENT_DATA',
                'recent_success_rate': 0.0,
                'analysis_period': f"Only {len(transactions)} transactions available"
            }

        # Group by time periods
        recent = transactions[-10:]  # Last 10 transactions
        success_count = sum(1 for tx in recent if 'submitted' in str(tx))

        trend = "STABLE"
        if success_count >= 8:
            trend = "IMPROVING"
        elif success_count <= 3:
            trend = "DECLINING"

        return {
            'trend': trend,
            'recent_success_rate': round((success_count / len(recent)) * 100, 2),
            'analysis_period': f"Last {len(recent)} transactions"
        }

    def _generate_recommendations(self, content, transactions):
        """Generate predictive recommendations"""
        recommendations = []

        # Analyze opt-in patterns
        optin_attempts = content.count('Trying strategy:')
        optin_successes = content.count('Opt-in confirmed')

        if optin_attempts > 0 and optin_successes == 0:
            recommendations.append({
                'priority': 'HIGH',
                'area': 'Opt-in Strategy',
                'recommendation': 'All opt-in strategies failing - consider manual opt-in or alternative protocols',
                'predicted_impact': 'High - blocking all transactions'
            })

        # Analyze transaction frequency
        if len(transactions) > 50:
            recommendations.append({
                'priority': 'MEDIUM',
                'area': 'Transaction Frequency',
                'recommendation': 'High transaction volume detected - monitor for rate limiting',
                'predicted_impact': 'Medium - potential temporary blocks'
            })

        # Analyze error patterns
        error_patterns = self._analyze_error_patterns(content)
        if error_patterns:
            most_common_error = max(error_patterns.items(), key=lambda x: x[1])
            recommendations.append({
                'priority': 'HIGH',
                'area': 'Error Prevention',
                'recommendation': f'Address most common error: {most_common_error[0]} ({most_common_error[1]} occurrences)',
                'predicted_impact': 'High - reducing this error could improve success rate significantly'
            })

        # Success rate analysis
        success_rate = self._calculate_success_rate(content)
        if success_rate < 50:
            recommendations.append({
                'priority': 'CRITICAL',
                'area': 'Success Rate',
                'recommendation': f'Low success rate ({success_rate}%) - immediate intervention required',
                'predicted_impact': 'Critical - system effectiveness compromised'
            })

        return recommendations

    def generate_predictive_report(self):
        """Generate comprehensive predictive analytics report"""
        analysis = self.analyze_transaction_history()

        if isinstance(analysis, str):
            return f"Predictive Analytics: {analysis}"

        report = {
            'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'analysis_summary': {
                'total_transactions': analysis['total_transactions'],
                'success_rate_percent': analysis['success_rate'],
                'peak_trading_hours': analysis['peak_hours'],
                'performance_trend': analysis['performance_trends']
            },
            'error_analysis': analysis['error_patterns'],
            'predictive_insights': analysis['recommendations'],
            'risk_assessment': self._assess_risks(analysis),
            'optimization_opportunities': self._identify_optimizations(analysis)
        }

        return report

    def _assess_risks(self, analysis):
        """Assess current system risks"""
        risks = []

        success_rate = analysis['success_rate']
        if success_rate < 30:
            risks.append({
                'level': 'CRITICAL',
                'risk': 'System Effectiveness',
                'description': f'Critical: Success rate only {success_rate}%',
                'mitigation': 'Immediate troubleshooting required'
            })

        if analysis['error_patterns']:
            risks.append({
                'level': 'HIGH',
                'risk': 'Recurring Errors',
                'description': f'Multiple error patterns detected: {list(analysis["error_patterns"].keys())}',
                'mitigation': 'Address root causes of common errors'
            })

        return risks

    def _identify_optimizations(self, analysis):
        """Identify optimization opportunities"""
        optimizations = []

        # Success rate optimization
        success_rate = analysis['success_rate']
        if success_rate < 70:
            optimizations.append({
                'opportunity': 'Success Rate Improvement',
                'potential_gain': f'Up to {100 - success_rate}% improvement possible',
                'effort': 'MEDIUM',
                'approach': 'Error pattern analysis and strategy optimization'
            })

        # Peak hours optimization
        if analysis['peak_hours']:
            optimizations.append({
                'opportunity': 'Peak Hours Optimization',
                'potential_gain': 'Better transaction timing and success rates',
                'effort': 'LOW',
                'approach': 'Schedule high-value transactions during peak hours'
            })

        # Error pattern optimization
        if analysis['error_patterns']:
            optimizations.append({
                'opportunity': 'Error Pattern Elimination',
                'potential_gain': 'Reduce transaction failures',
                'effort': 'HIGH',
                'approach': 'Implement preventive measures for common errors'
            })

        return optimizations

def run_predictive_analytics():
    """Run predictive analytics and display results"""
    print('🔮 EMPIRE PREDICTIVE ANALYTICS SYSTEM')
    print('=' * 45)

    analytics = EmpirePredictiveAnalytics()
    report = analytics.generate_predictive_report()

    if isinstance(report, str):
        print(report)
        return

    print('📊 ANALYSIS SUMMARY:')
    summary = report['analysis_summary']
    print(f"   📈 Total Transactions: {summary['total_transactions']}")
    print(f"   ✅ Success Rate: {summary['success_rate_percent']}%")
    print(f"   🕐 Peak Hours: {', '.join(summary['peak_trading_hours'][:2])}")
    print(f"   📊 Performance Trend: {summary['performance_trend']['trend']}")

    print()
    print('🚨 RISK ASSESSMENT:')
    for risk in report['risk_assessment']:
        print(f"   [{risk['level']}] {risk['risk']}: {risk['description']}")

    print()
    print('🎯 PREDICTIVE INSIGHTS:')
    for insight in report['predictive_insights'][:3]:
        print(f"   [{insight['priority']}] {insight['area']}: {insight['recommendation']}")

    print()
    print('🔧 OPTIMIZATION OPPORTUNITIES:')
    for opt in report['optimization_opportunities']:
        print(f"   📈 {opt['opportunity']} ({opt['effort']} effort)")
        print(f"      💰 Potential: {opt['potential_gain']}")

    print()
    print('🎖️  PREDICTIVE ANALYTICS: ACTIVE AND OPTIMIZING')

if __name__ == "__main__":
    run_predictive_analytics()
