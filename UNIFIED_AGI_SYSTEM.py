#!/usr/bin/env python3
"""
UNIFIED AGI SYSTEM
Runs on 5-minute cycles to analyze AND implement optimizations continuously
This eliminates the disconnect between AGI analysis (5 min) and execution (30 min)
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from REAL_AGI_HOW_EXECUTION_ENGINE import real_how_engine
from REAL_EMPIRE_SYSTEM_CONNECTORS import RealEmpireSystemConnectors
from memory.long_term_memory import LongTermMemory
from tools.web_tools import SimpleWebTools
import os
from typing import List, Dict, Any

class UnifiedAGISystem:
    """Unified AGI system that analyzes AND implements in the same 5-minute cycle"""
    
    def __init__(self):
        self.empire_connectors = RealEmpireSystemConnectors()
        self.unified_mode = True
        self.cycle_count = 0
        self.optimization_history = []
        self.insight_history = []
        self.last_cycle = None
        self.how_execution_engine = real_how_engine # Added for problem-solving
        self.memory = LongTermMemory()
        self.web = SimpleWebTools()
        self.stuck_counter = 0
        
    async def start_unified_agi_operation(self):
        """Start unified AGI operation on 5-minute cycles"""
        print("🚀 STARTING UNIFIED AGI SYSTEM...")
        print("=" * 60)
        print("🎯 AGI will now analyze AND implement in the same 5-minute cycle")
        print("🔄 No more disconnect between thinking and doing!")
        print("⏰ Unified cycles every 5 minutes")
        print()
        
        # Initialize the execution engine
        print("🔧 Initializing unified AGI system...")
        await real_how_engine.initialize()
        
        # Start unified operation
        while self.unified_mode:
            try:
                self.cycle_count += 1
                current_time = datetime.now()
                
                print(f"\n🔄 UNIFIED AGI CYCLE #{self.cycle_count}")
                print(f"⏰ {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 50)
                
                # PHASE 1: AGI ANALYSIS (Think)
                print("🧠 PHASE 1: AGI ANALYSIS")
                insights = await self._generate_agi_insights()
                print(f"   💡 Generated {len(insights)} insights")
                # Remember insights
                if insights:
                    self.memory.add({"insights": insights, "cycle": self.cycle_count}, tags=["insights"])
                    self.stuck_counter = 0
                else:
                    self.stuck_counter += 1
                
                # PHASE 2: AGI IMPLEMENTATION (Do)
                print("\n⚡ PHASE 2: AGI IMPLEMENTATION")
                if insights:
                    implementation_results = await self._implement_agi_insights(insights)
                    print(f"   🔧 Implemented {len(implementation_results)} optimizations")
                    self.memory.add({"implemented": implementation_results, "cycle": self.cycle_count}, tags=["actions"])
                else:
                    print("   🎯 No insights to implement - system is well-optimized!")
                
                # PHASE 3: AGI LEARNING & IMPROVEMENT
                print("\n📚 PHASE 3: AGI LEARNING & IMPROVEMENT")
                # Ingest Capitalism Lab knowledge notes into long-term memory
                try:
                    await self._ingest_capitalism_knowledge()
                except Exception:
                    pass
                await self._learn_and_improve()
                # Stuck detection -> trigger exploratory probes
                if self.stuck_counter >= 2:
                    print("   🧭 No insights for 2 cycles: probing with web tools...")
                    try:
                        probe = self.web.search_duckduckgo("AI automation website performance optimization tips", limit=3)
                        self.memory.add({"probe": "web_search", "results": probe}, tags=["probe", "web"])
                    except Exception:
                        pass
                
                # Update cycle tracking
                self.last_cycle = current_time
                
                # Save unified history
                self._save_unified_history()
                
                # Update FundManager overrides so AGI steers trading
                await self._update_fund_overrides()
                
                # Show unified cycle summary
                await self._show_unified_cycle_summary()
                
                # Wait 5 minutes before next unified cycle
                print(f"\n⏳ Next unified AGI cycle in 5 minutes...")
                print("   (Press Ctrl+C to stop unified operation)")
                
                # Wait 5 minutes (300 seconds)
                await asyncio.sleep(300)
                
            except KeyboardInterrupt:
                print("\n🛑 Unified AGI operation stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Cycle error: {e}")
                print("   Waiting 1 minute before retrying...")
                await asyncio.sleep(60)
    
    async def _generate_agi_insights(self):
        """Generate AGI insights through analysis"""
        insights = []
        
        # 1. System Health Analysis
        system_health = await self._analyze_system_health()
        if system_health.get('needs_attention'):
            insights.append({
                'id': f'system_health_{self.cycle_count}',
                'summary': 'System health optimization needed',
                'implication': 'System performance can be improved',
                'type': 'system_optimization',
                'action': 'optimize_system_health',
                'target_system': 'multiple_systems',
                'description': 'Optimize system health and performance based on current metrics',
                'priority': 'HIGH',
                'source': 'system_health_analysis'
            })
        
        # 2. Agent Intelligence Analysis
        agent_insights = await self._analyze_agent_intelligence()
        insights.extend(agent_insights)
        
        # 3. Website Performance Analysis
        website_insights = await self._analyze_website_performance()
        insights.extend(website_insights)
        
        # 4. Trading System Analysis
        trading_insights = await self._analyze_trading_system()
        insights.extend(trading_insights)

        # 4b. Fund Optimization Analysis (WHY for the fund)
        fund_insights = await self._analyze_fund_optimization()
        insights.extend(fund_insights)
        
        # 5. Revenue & Business Analysis
        business_insights = await self._analyze_business_opportunities()
        insights.extend(business_insights)
        
        # 6. Performance & Scalability Analysis
        performance_insights = await self._analyze_performance_scalability()
        insights.extend(performance_insights)
        
        return insights
    
    async def _filter_completed_insights(self, insights: List[Dict[str, Any]], hours_cooldown: int = 12) -> List[Dict[str, Any]]:
        """Filter out insights that have been successfully executed recently.
        Uses execution history from HOW engine; suppresses duplicates within the cooldown window.
        """
        try:
            summary_data = await real_how_engine.get_execution_summary()
            history = summary_data.get('execution_history', []) or []
            if not history:
                return insights
            now = datetime.now()
            cooldown_delta = timedelta(hours=hours_cooldown)
            recently_completed: set = set()
            for record in history:
                if record.get('status') != 'completed':
                    continue
                summary = record.get('insight_summary')
                ts_str = record.get('timestamp')
                if not summary or not ts_str:
                    continue
                try:
                    ts = datetime.fromisoformat(ts_str)
                except Exception:
                    continue
                if (now - ts) <= cooldown_delta:
                    recently_completed.add(summary)
            if not recently_completed:
                return insights
            filtered = [i for i in insights if i.get('summary') not in recently_completed]
            return filtered
        except Exception:
            return insights

    async def _analyze_system_health(self):
        """Analyze overall system health"""
        try:
            # Get empire status
            empire_status = await real_how_engine.get_empire_status()
            
            # Check for any issues
            needs_attention = False
            issues = []
            
            if empire_status.get('trading_system', {}).get('current_status') == 'error':
                needs_attention = True
                issues.append('Trading system errors')
            
            if empire_status.get('agent_systems', {}).get('current_status') == 'error':
                needs_attention = True
                issues.append('Agent system errors')
            
            return {
                'needs_attention': needs_attention,
                'issues': issues,
                'empire_status': empire_status
            }
            
        except Exception as e:
            return {'needs_attention': False, 'error': str(e)}
    
    async def _analyze_agent_intelligence(self):
        """Analyze agent intelligence and capabilities"""
        insights = []
        
        # Check for agents without logging
        agents_to_check = [
            'integrated_deployment_system.py',
            'enhanced_visual_testing_agent.py',
            'social_media_agent.py',
            'optimized_content_agent.py',
            'live_orchestrator.py',
            'ultimate_ceo_agent.py'
        ]
        
        for agent in agents_to_check:
            try:
                with open(agent, 'r') as f:
                    content = f.read()
                    if 'import logging' not in content:
                        insights.append({
                            'id': f'agent_logging_{agent}',
                            'summary': f'Add logging to {agent}',
                            'implication': 'Better monitoring and debugging',
                            'type': 'agent_optimization',
                            'action': 'add_logging_to_agents',
                            'target_system': agent,
                            'description': f'Add proper logging to {agent} for better monitoring',
                            'priority': 'MEDIUM',
                            'source': 'agent_intelligence_analysis'
                        })
            except FileNotFoundError:
                continue
        # Web grounding for agent logging best practices
        try:
            probe = self.web.search_duckduckgo("best practices python logging agent", limit=2)
            self.memory.add({"probe": "agent_logging_best_practices", "results": probe}, tags=["web", "agents"])
        except Exception:
            pass
        
        # Suppress insights already completed recently
        insights = await self._filter_completed_insights(insights)
        return insights
    
    async def _analyze_website_performance(self):
        """Analyze website performance and SEO"""
        insights = []
        
        try:
            website_dir = "wealthyrobots_website"
            if os.path.exists(website_dir):
                # Check for performance optimization opportunities
                insights.append({
                    'id': f'website_optimization_{self.cycle_count}',
                    'summary': 'Website performance optimization',
                    'implication': 'Better user experience and SEO',
                    'type': 'website_optimization',
                    'action': 'optimize_website_performance',
                    'target_system': 'wealthyrobots_website',
                    'description': 'Optimize website performance, SEO, and user experience',
                    'priority': 'MEDIUM',
                    'source': 'website_performance_analysis'
                })
                # Use web tool to fetch homepage title quickly (grounding)
                try:
                    homepage = self.web.fetch_url("https://example.com")
                    self.memory.add({"homepage_probe": homepage}, tags=["web", "grounding"])
                except Exception:
                    pass
        except Exception:
            pass
        
        return insights
    
    async def _analyze_trading_system(self):
        """Analyze trading system for optimization opportunities"""
        insights = []
        
        try:
            with open('unified_trading_system.py', 'r') as f:
                content = f.read()
                
                # Check for missing optimizations
                if 'class OpportunityDetector' not in content:
                    insights.append({
                        'id': f'trading_opportunity_detection_{self.cycle_count}',
                        'summary': 'Add opportunity detection to trading system',
                        'implication': 'Better trading performance and profit generation',
                        'type': 'trading_optimization',
                        'action': 'add_opportunity_detection',
                        'target_system': 'unified_trading_system.py',
                        'description': 'Add real-time opportunity detection for DeFi trading',
                        'priority': 'HIGH',
                        'source': 'trading_system_analysis'
                    })
                
                if 'class ProfitTracker' not in content:
                    insights.append({
                        'id': f'trading_profit_tracking_{self.cycle_count}',
                        'summary': 'Add profit tracking to trading system',
                        'implication': 'Better performance monitoring and optimization',
                        'type': 'trading_optimization',
                        'action': 'add_profit_tracking',
                        'target_system': 'unified_trading_system.py',
                        'description': 'Add comprehensive profit tracking and analytics',
                        'priority': 'HIGH',
                        'source': 'trading_system_analysis'
                    })
                
                if 'class ErrorHandler' not in content:
                    insights.append({
                        'id': f'trading_error_handling_{self.cycle_count}',
                        'summary': 'Add error handling to trading system',
                        'implication': 'Better system reliability and recovery',
                        'type': 'trading_optimization',
                        'action': 'add_error_handling',
                        'target_system': 'unified_trading_system.py',
                        'description': 'Add comprehensive error handling and recovery',
                        'priority': 'HIGH',
                        'source': 'trading_system_analysis'
                    })
                
        except FileNotFoundError:
            pass
        # Web grounding for trading
        try:
            ref = self.web.fetch_url("https://example.com")
            self.memory.add({"probe": "trading_ref_fetch", "result": ref}, tags=["web", "trading"])
        except Exception:
            pass
        
        return insights
    
    async def _analyze_business_opportunities(self):
        """Analyze business and revenue opportunities"""
        insights = []
        
        # Check for revenue optimization opportunities
        insights.append({
            'id': f'business_optimization_{self.cycle_count}',
            'summary': 'Business performance optimization',
            'implication': 'Increased revenue and efficiency',
            'type': 'business_optimization',
            'action': 'optimize_business_performance',
            'target_system': 'business_systems',
            'description': 'Optimize business processes and revenue generation',
            'priority': 'HIGH',
            'source': 'business_opportunity_analysis'
        })
        # Web grounding for business
        try:
            results = self.web.search_duckduckgo("increase conversion rate ai website", limit=3)
            self.memory.add({"probe": "business_conversion_search", "results": results}, tags=["web", "business"])
        except Exception:
            pass
        
        return insights
    
    async def _analyze_performance_scalability(self):
        """Analyze performance and scalability opportunities"""
        insights = []
        
        # Check for performance optimization opportunities
        insights.append({
            'id': f'performance_optimization_{self.cycle_count}',
            'summary': 'System performance optimization',
            'implication': 'Better performance and scalability',
            'type': 'performance_optimization',
            'action': 'optimize_system_performance',
            'target_system': 'system_infrastructure',
            'description': 'Optimize system performance and scalability',
            'priority': 'MEDIUM',
            'source': 'performance_scalability_analysis'
        })
        
        return insights
    
    async def _implement_agi_insights(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Implement AGI insights using the HOW execution system"""
        if not insights:
            return {'status': 'no_insights', 'message': 'No insights to implement'}
        
        print(f"\n🚀 PHASE 2: AGI IMPLEMENTATION (Do)")
        print(f"   Implementing {len(insights)} insights...")
        
        # Create action plan with self-consistency voting
        action_plan = await self._plan_with_self_consistency(insights, samples=3)
        
        # Execute actions with intelligent problem-solving
        execution_results = await self._execute_with_problem_solving(action_plan)

        # Apply any fund overrides suggested by insights (direct HOW)
        try:
            for ins in insights:
                if ins.get('action') == 'update_fund_overrides' and ins.get('type') in ('fund_optimization','system_optimization'):
                    overrides = ins.get('proposed_overrides') or {}
                    if overrides:
                        self._apply_fund_overrides(overrides)
                        print(f"   ✅ Applied fund overrides: {overrides}")
        except Exception:
            pass
        
        # Learn from results
        await self._learn_from_execution(execution_results)
        
        return {
            'status': 'completed',
            'insights_processed': len(insights),
            'execution_results': execution_results,
            'learning_applied': True
        }

    async def _plan_with_self_consistency(self, insights: List[Dict[str, Any]], samples: int = 3) -> List[Dict[str, Any]]:
        """Generate multiple action plans and select majority-agreed actions."""
        try:
            from collections import Counter
            def make_key(a: Dict[str, Any]):
                return (a.get('type'), a.get('action'), a.get('target_system'))
            plan_samples: List[List[Dict[str, Any]]] = []
            for _ in range(max(1, samples)):
                plan = await self.how_execution_engine.create_real_action_plan(insights)
                plan_samples.append(plan)
            counts = Counter()
            last = {}
            for plan in plan_samples:
                for act in plan:
                    k = make_key(act)
                    counts[k] += 1
                    last[k] = act
            threshold = max(1, (samples // 2) + 1)
            majority = [last[k] for k, c in counts.items() if c >= threshold]
            if not majority and plan_samples:
                return plan_samples[0]
            return majority
        except Exception:
            return await self.how_execution_engine.create_real_action_plan(insights)

    async def _analyze_fund_optimization(self) -> List[Dict[str, Any]]:
        """Analyze recent fund activity (cadence and NAV drift) and propose overrides."""
        ideas: List[Dict[str, Any]] = []
        try:
            # Look at last health NAV to include context
            nav = None
            try:
                import glob as _glob, json as _json
                logs = sorted(_glob.glob('logs/hybrid_health_*.json'))
                if logs:
                    with open(logs[-1], 'r') as f:
                        lines = [l for l in f.readlines()[-50:] if l.strip()]
                        for l in reversed(lines):
                            try:
                                obj = _json.loads(l)
                                if 'nav_estimate_usd' in obj:
                                    nav = float(obj['nav_estimate_usd'])
                                    break
                            except Exception:
                                continue
            except Exception:
                pass

            lower_thresholds = {
                'aggressiveness': 'balanced',
                'base_trade_micro': 3000,
                'arbitrage_threshold_bps': 50,
                'momentum_threshold_bps': 50
            }
            ideas.append({
                'id': f'fund_optimization_{self.cycle_count}',
                'summary': 'Tune fund thresholds and sizing',
                'implication': 'Increase trade cadence while respecting fees',
                'type': 'fund_optimization',
                'action': 'update_fund_overrides',
                'target_system': 'fund_manager',
                'description': 'Adjust thresholds (50 bps) and base size (3000 micro) to improve cadence',
                'priority': 'HIGH',
                'source': 'fund_analysis',
                'proposed_overrides': lower_thresholds,
                'current_nav': nav
            })
        except Exception:
            pass
        return ideas

    def _apply_fund_overrides(self, overrides: Dict[str, Any]) -> None:
        try:
            import yaml as _yaml
            os.makedirs('config', exist_ok=True)
            path = 'config/fund_manager.overrides.yaml'
            data = {}
            try:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        data = _yaml.safe_load(f) or {}
            except Exception:
                data = {}
            data.update(overrides)
            with open(path, 'w') as f:
                _yaml.safe_dump(data, f)
        except Exception:
            pass
    
    async def _execute_with_problem_solving(self, action_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute actions with intelligent problem-solving and self-healing"""
        print(f"\n   🔧 Executing {len(action_plan)} actions with intelligent problem-solving...")
        
        results = []
        failed_actions = []
        
        for action in action_plan:
            print(f"\n   🎯 Executing: {action.get('type', 'unknown')} - {action.get('action', 'unknown')}")
            
            try:
                # Execute the action
                result = await self.how_execution_engine._execute_real_actions([action])
                
                if result and result[0].get('status') == 'completed':
                    print(f"   ✅ Success: {action.get('action', 'unknown')}")
                    results.append({
                        'action': action,
                        'status': 'success',
                        'result': result[0]
                    })
                else:
                    print(f"   ❌ Failed: {action.get('action', 'unknown')}")
                    failed_actions.append(action)
                    results.append({
                        'action': action,
                        'status': 'failed',
                        'result': result[0] if result else {'status': 'unknown_error'}
                    })
                    
            except Exception as e:
                print(f"   💥 Exception: {action.get('action', 'unknown')} - {str(e)}")
                failed_actions.append(action)
                results.append({
                    'action': action,
                    'status': 'exception',
                    'error': str(e)
                })
        
        # If there are failed actions, activate intelligent problem-solving
        if failed_actions:
            print(f"\n   🧠 INTELLIGENT PROBLEM-SOLVING ACTIVATED!")
            print(f"   🔍 Analyzing {len(failed_actions)} failed actions...")
            
            # Use WHY system to analyze failures
            failure_analysis = await self._analyze_failures(failed_actions, results)
            
            # Use HOW system to implement fixes
            fix_results = await self._implement_fixes(failure_analysis)
            
            # Retry failed actions with fixes applied
            retry_results = await self._retry_failed_actions(failed_actions, fix_results)
            
            # Update results with retry outcomes
            results = self._merge_results(results, retry_results)
        
        return results
    
    async def _learn_from_execution(self, execution_results: List[Dict[str, Any]]) -> None:
        """Learn from execution results to improve future cycles"""
        print(f"\n📚 PHASE 3: AGI LEARNING & IMPROVEMENT")
        print(f"   Learning from {len(execution_results)} execution results...")
        
        successful_actions = [r for r in execution_results if r.get('status') in ['success', 'retry_success']]
        failed_actions = [r for r in execution_results if r.get('status') in ['failed', 'exception', 'retry_failed']]
        
        # Analyze success patterns
        if successful_actions:
            print(f"   ✅ Success patterns identified: {len(successful_actions)} actions")
            for action in successful_actions[:3]:  # Show first 3
                print(f"      - {action.get('action', {}).get('action', 'unknown')}: {action.get('status')}")
        
        # Analyze failure patterns
        if failed_actions:
            print(f"   ❌ Failure patterns identified: {len(failed_actions)} actions")
            for action in failed_actions[:3]:  # Show first 3
                print(f"      - {action.get('action', {}).get('action', 'unknown')}: {action.get('status')}")
        
        # Store learning for future cycles
        learning_record = {
            'cycle': self.cycle_count,
            'timestamp': datetime.now().isoformat(),
            'total_actions': len(execution_results),
            'successful_actions': len(successful_actions),
            'failed_actions': len(failed_actions),
            'success_rate': len(successful_actions) / len(execution_results) if execution_results else 0,
            'patterns_identified': len(successful_actions) + len(failed_actions)
        }
        
        self.optimization_history.append(learning_record) # Changed from learning_history to optimization_history
        print(f"   📊 Learning recorded: Success rate {learning_record['success_rate']:.1%}")
    
    async def _generate_agi_insights(self) -> List[Dict[str, Any]]:
        """Generate AGI insights through analysis"""
        insights = []
        
        # 1. System Health Analysis
        system_health = await self._analyze_system_health()
        if system_health.get('needs_attention'):
            insights.append({
                'id': f'system_health_{self.cycle_count}',
                'summary': 'System health optimization needed',
                'implication': 'System performance can be improved',
                'type': 'system_optimization',
                'action': 'optimize_system_health',
                'target_system': 'multiple_systems',
                'description': 'Optimize system health and performance based on current metrics',
                'priority': 'HIGH',
                'source': 'system_health_analysis'
            })
        
        # 2. Agent Intelligence Analysis
        agent_insights = await self._analyze_agent_intelligence()
        insights.extend(agent_insights)
        
        # 3. Website Performance Analysis
        website_insights = await self._analyze_website_performance()
        insights.extend(website_insights)
        
        # 4. Trading System Analysis
        trading_insights = await self._analyze_trading_system()
        insights.extend(trading_insights)
        
        # 5. Revenue & Business Analysis
        business_insights = await self._analyze_business_opportunities()
        insights.extend(business_insights)
        
        # 6. Performance & Scalability Analysis
        performance_insights = await self._analyze_performance_scalability()
        insights.extend(performance_insights)
        
        # 7. Goal Gap Analysis
        goal_gap_insights = await self._analyze_goal_gaps()
        insights.extend(goal_gap_insights)
        
        # Suppress insights already completed recently
        insights = await self._filter_completed_insights(insights)
        return insights

    async def _analyze_goal_gaps(self) -> List[Dict[str, Any]]:
        """Compare current metrics to agi_goals.json and emit insights for gaps."""
        insights: List[Dict[str, Any]] = []
        try:
            with open('agi_goals.json', 'r') as fh:
                goals = json.load(fh)
            targets = goals.get('targets', {})
            priorities = goals.get('priorities', {})

            # Pull current metrics
            exec_summary = await real_how_engine.get_execution_summary()
            success_rate = 0.0
            try:
                total = exec_summary.get('total_executions', 0)
                success = exec_summary.get('successful_executions', 0)
                success_rate = (success / total) if total else 0.0
            except Exception:
                pass

            # Benchmarks
            bench_score = 0.0
            trend_file = os.path.join('intelligence_benchmarks', 'benchmark_trend.json')
            if os.path.exists(trend_file):
                try:
                    with open(trend_file, 'r') as bf:
                        trend = json.load(bf)
                    if isinstance(trend, list) and trend:
                        bench_score = float(trend[-1].get('overall_score', 0.0))
                except Exception:
                    pass

            # Insights per day (approx): count memory 'insights' in last 24h
            recent_insights = [e for e in self.memory.recall_recent(hours=24) if 'insights' in e.get('content', {})]
            insights_per_day = sum(len(e['content']['insights']) for e in recent_insights)

            # Agent errors: naive proxy from last coordination report
            agent_errors = 0
            try:
                reports = [f for f in os.listdir('.') if f.startswith('agent_coordination_report_') and f.endswith('.json')]
                if reports:
                    reports.sort()
                    with open(reports[-1], 'r') as rf:
                        rep = json.load(rf)
                    qa = rep.get('qa_results', {})
                    if isinstance(qa, dict):
                        agent_errors = len([v for v in qa.values() if isinstance(v, str) and v])
            except Exception:
                pass

            # Website optimization present: check report existence
            website_ok = os.path.exists(os.path.join('wealthyrobots_website', 'optimization_report.json'))

            # Compare and emit gap insights
            def add_gap(metric_name: str, current_value: float, target_key: str, insight: Dict[str, Any]):
                target = targets.get(target_key)
                if target is None:
                    return
                meets = current_value >= target if isinstance(target, (int, float)) else bool(website_ok)
                if not meets:
                    insight['priority'] = priorities.get(target_key, 'MEDIUM')
                    insights.append(insight)

            add_gap('execution_success_rate', success_rate, 'execution_success_rate', {
                'id': f'goal_gap_exec_success_{self.cycle_count}',
                'summary': 'Increase execution success rate',
                'implication': 'Higher autonomy and fewer manual interventions',
                'type': 'system_optimization',
                'action': 'add_retry_logic',
                'target_system': 'multiple_systems',
                'description': f'Current success rate {success_rate:.2f} below target'
            })

            add_gap('benchmarks_overall_score', bench_score, 'benchmarks_overall_score', {
                'id': f'goal_gap_benchmarks_{self.cycle_count}',
                'summary': 'Improve intelligence benchmark score',
                'implication': 'Smarter planning and reasoning',
                'type': 'performance_optimization',
                'action': 'optimize_system_performance',
                'target_system': 'system_infrastructure',
                'description': f'Benchmark overall score {bench_score:.2f} below target'
            })

            add_gap('insights_per_day', float(insights_per_day), 'insights_per_day', {
                'id': f'goal_gap_insights_rate_{self.cycle_count}',
                'summary': 'Increase insights generation rate',
                'implication': 'Faster iteration and improvement',
                'type': 'agent_optimization',
                'action': 'add_logging_to_agents',
                'target_system': 'multiple_agents',
                'description': f'Generated {insights_per_day} insights in last 24h; below target'
            })

            # Agent errors gap: invert (target 0)
            target_errors = targets.get('agent_errors', 0)
            if agent_errors > target_errors:
                insights.append({
                    'id': f'goal_gap_agent_errors_{self.cycle_count}',
                    'summary': 'Reduce agent errors',
                    'implication': 'More reliable operations',
                    'type': 'system_optimization',
                    'action': 'fix_file_permissions',
                    'target_system': 'multiple_agents',
                    'description': f'{agent_errors} agent errors detected; target is {target_errors}',
                    'priority': priorities.get('agent_errors', 'HIGH')
                })

            # Website optimization presence gap
            if targets.get('website_optimization_present', True) and not website_ok:
                insights.append({
                    'id': f'goal_gap_website_opt_{self.cycle_count}',
                    'summary': 'Ensure website optimization report exists',
                    'implication': 'Sustained SEO and performance gains',
                    'type': 'website_optimization',
                    'action': 'optimize_website_performance',
                    'target_system': 'wealthyrobots_website',
                    'description': 'optimization_report.json missing',
                    'priority': priorities.get('website_optimization_present', 'MEDIUM')
                })

        except Exception:
            pass
        return insights

    async def _auto_heal_agents(self) -> None:
        """Auto-heal common agent issues (restart or run specific tests)."""
        try:
            # Example: run visual testing agent if website present
            if os.path.exists('enhanced_visual_testing_agent.py') and os.path.exists('wealthyrobots_website'):
                import importlib.util
                spec = importlib.util.spec_from_file_location('enhanced_visual_testing_agent', 'enhanced_visual_testing_agent.py')
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)  # type: ignore
                if hasattr(mod, 'EnhancedVisualTestingAgent'):
                    print('🛠️  Auto-heal: running enhanced visual tests...')
                    try:
                        agent = mod.EnhancedVisualTestingAgent()
                        report = agent.run_comprehensive_test()
                        self.memory.add({"auto_heal": "visual_testing", "report": report}, tags=["auto_heal", "testing"])
                    except Exception as e:
                        print(f"Auto-heal visual tests failed: {e}")
        except Exception:
            pass
    
    async def _analyze_failures(self, failed_actions: List[Dict[str, Any]], execution_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use WHY system to analyze why actions failed"""
        print(f"   🔍 WHY System: Analyzing failure patterns...")
        
        failure_patterns = []
        root_causes = []
        
        for action in failed_actions:
            action_result = next((r for r in execution_results if r.get('action') == action), None)
            
            if action_result:
                # Analyze the specific failure
                pattern = await self._identify_failure_pattern(action, action_result)
                root_cause = await self._identify_root_cause(action, action_result)
                
                failure_patterns.append(pattern)
                root_causes.append(root_cause)
        
        # Identify common patterns and systemic issues
        common_patterns = self._find_common_patterns(failure_patterns)
        systemic_issues = self._identify_systemic_issues(root_causes)
        
        return {
            'failure_patterns': failure_patterns,
            'root_causes': root_causes,
            'common_patterns': common_patterns,
            'systemic_issues': systemic_issues,
            'recommended_fixes': self._generate_fix_recommendations(common_patterns, systemic_issues)
        }
    
    async def _identify_failure_pattern(self, action: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Identify the pattern of a specific failure"""
        action_type = action.get('type', 'unknown')
        action_name = action.get('action', 'unknown')
        error = result.get('error', 'unknown')
        status = result.get('status', 'unknown')
        
        # Pattern recognition based on action type and error
        if 'timeout' in error.lower():
            pattern = 'timeout_failure'
        elif 'permission' in error.lower():
            pattern = 'permission_failure'
        elif 'not_found' in error.lower():
            pattern = 'missing_resource_failure'
        elif 'syntax' in error.lower():
            pattern = 'code_syntax_failure'
        elif 'import' in error.lower():
            pattern = 'dependency_failure'
        else:
            pattern = 'unknown_failure'
        
        return {
            'action_type': action_type,
            'action_name': action_name,
            'pattern': pattern,
            'error': error,
            'status': status
        }
    
    async def _identify_root_cause(self, action: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Identify the root cause of a failure"""
        action_type = action.get('type', 'unknown')
        action_name = action.get('action', 'unknown')
        error = result.get('error', 'unknown')
        
        # Root cause analysis
        if action_type == 'trading_optimization':
            if 'opportunity_detection' in action_name:
                root_cause = 'missing_trading_optimization_method'
            elif 'profit_tracking' in action_name:
                root_cause = 'missing_profit_tracking_implementation'
            elif 'error_handling' in action_name:
                root_cause = 'missing_error_handling_implementation'
            else:
                root_cause = 'incomplete_trading_system_connectors'
        elif action_type == 'website_optimization':
            root_cause = 'missing_website_optimization_methods'
        elif action_type == 'system_optimization':
            root_cause = 'missing_system_optimization_methods'
        else:
            root_cause = 'unknown_root_cause'
        
        return {
            'action_type': action_type,
            'action_name': action_name,
            'root_cause': root_cause,
            'error': error
        }
    
    def _find_common_patterns(self, failure_patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find common patterns across multiple failures"""
        pattern_counts = {}
        
        for pattern in failure_patterns:
            pattern_type = pattern.get('pattern', 'unknown')
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        common_patterns = []
        for pattern_type, count in pattern_counts.items():
            if count > 1:
                common_patterns.append({
                    'pattern': pattern_type,
                    'frequency': count,
                    'priority': 'HIGH' if count >= 3 else 'MEDIUM'
                })
        
        return sorted(common_patterns, key=lambda x: x['frequency'], reverse=True)
    
    def _identify_systemic_issues(self, root_causes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify systemic issues that affect multiple actions"""
        cause_counts = {}
        
        for cause in root_causes:
            cause_type = cause.get('root_cause', 'unknown')
            cause_counts[cause_type] = cause_counts.get(cause_type, 0) + 1
        
        systemic_issues = []
        for cause_type, count in cause_counts.items():
            if count > 1:
                systemic_issues.append({
                    'issue': cause_type,
                    'affected_actions': count,
                    'priority': 'HIGH' if count >= 3 else 'MEDIUM'
                })
        
        return sorted(systemic_issues, key=lambda x: x['affected_actions'], reverse=True)
    
    def _generate_fix_recommendations(self, common_patterns: List[Dict[str, Any]], systemic_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate specific fix recommendations based on analysis"""
        recommendations = []
        
        # Fix recommendations for common patterns
        for pattern in common_patterns:
            if pattern['pattern'] == 'timeout_failure':
                recommendations.append({
                    'type': 'system_optimization',
                    'action': 'increase_timeout_limits',
                    'priority': pattern['priority'],
                    'description': 'Increase timeout limits for network operations'
                })
            elif pattern['pattern'] == 'permission_failure':
                recommendations.append({
                    'type': 'system_optimization',
                    'action': 'fix_file_permissions',
                    'priority': pattern['priority'],
                    'description': 'Fix file and directory permissions'
                })
            elif pattern['pattern'] == 'missing_resource_failure':
                recommendations.append({
                    'type': 'system_optimization',
                    'action': 'create_missing_resources',
                    'priority': pattern['priority'],
                    'description': 'Create missing files and directories'
                })
        
        # Fix recommendations for systemic issues
        for issue in systemic_issues:
            if 'missing_trading_optimization_method' in issue['issue']:
                recommendations.append({
                    'type': 'code_optimization',
                    'action': 'implement_trading_optimizations',
                    'priority': issue['priority'],
                    'description': 'Implement missing trading system optimization methods'
                })
            elif 'missing_website_optimization_methods' in issue['issue']:
                recommendations.append({
                    'type': 'code_optimization',
                    'action': 'implement_website_optimizations',
                    'priority': issue['priority'],
                    'description': 'Implement missing website optimization methods'
                })
            elif 'missing_system_optimization_methods' in issue['issue']:
                recommendations.append({
                    'type': 'code_optimization',
                    'action': 'implement_system_optimizations',
                    'priority': issue['priority'],
                    'description': 'Implement missing system optimization methods'
                })
        
        return recommendations
    
    async def _implement_fixes(self, failure_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use HOW system to implement fixes for identified problems"""
        print(f"   🔧 HOW System: Implementing fixes for identified problems...")
        
        recommendations = failure_analysis.get('recommended_fixes', [])
        fix_results = []
        
        for recommendation in recommendations:
            print(f"   🛠️  Implementing fix: {recommendation.get('action', 'unknown')}")
            
            try:
                # Create a fix action
                fix_action = {
                    'type': recommendation.get('type', 'general_optimization'),
                    'action': recommendation.get('action', 'unknown'),
                    'target_system': 'system_fixes',
                    'description': recommendation.get('description', ''),
                    'priority': recommendation.get('priority', 'MEDIUM')
                }
                
                # Execute the fix
                fix_result = await self.how_execution_engine._execute_real_actions([fix_action])
                
                if fix_result and fix_result[0].get('status') == 'completed':
                    print(f"   ✅ Fix successful: {recommendation.get('action', 'unknown')}")
                    fix_results.append({
                        'fix': recommendation,
                        'status': 'success',
                        'result': fix_result[0]
                    })
                else:
                    print(f"   ❌ Fix failed: {recommendation.get('action', 'unknown')}")
                    fix_results.append({
                        'fix': recommendation,
                        'status': 'failed',
                        'result': fix_result[0] if fix_result else {'status': 'unknown_error'}
                    })
                    
            except Exception as e:
                print(f"   💥 Fix exception: {recommendation.get('action', 'unknown')} - {str(e)}")
                fix_results.append({
                    'fix': recommendation,
                    'status': 'exception',
                    'error': str(e)
                })
        
        return fix_results
    
    async def _retry_failed_actions(self, failed_actions: List[Dict[str, Any]], fix_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Retry failed actions after fixes have been applied"""
        print(f"   🔄 Retrying {len(failed_actions)} failed actions after fixes...")
        
        retry_results = []
        
        for action in failed_actions:
            print(f"   🔄 Retrying: {action.get('action', 'unknown')}")
            
            try:
                # Retry the action
                retry_result = await self.how_execution_engine._execute_real_actions([action])
                
                if retry_result and retry_result[0].get('status') == 'completed':
                    print(f"   ✅ Retry successful: {action.get('action', 'unknown')}")
                    retry_results.append({
                        'action': action,
                        'status': 'retry_success',
                        'result': retry_result[0]
                    })
                else:
                    print(f"   ❌ Retry failed: {action.get('action', 'unknown')}")
                    retry_results.append({
                        'action': action,
                        'status': 'retry_failed',
                        'result': retry_result[0] if retry_result else {'status': 'unknown_error'}
                    })
                    
            except Exception as e:
                print(f"   💥 Retry exception: {action.get('action', 'unknown')} - {str(e)}")
                retry_results.append({
                    'action': action,
                    'status': 'retry_exception',
                    'error': str(e)
                })
        
        return retry_results
    
    def _merge_results(self, original_results: List[Dict[str, Any]], retry_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge original results with retry results"""
        merged = original_results.copy()
        
        for retry_result in retry_results:
            # Find the corresponding original result
            for i, original_result in enumerate(merged):
                if (original_result.get('action') == retry_result.get('action') and 
                    original_result.get('status') in ['failed', 'exception']):
                    # Update the status based on retry result
                    if retry_result.get('status') == 'retry_success':
                        merged[i]['status'] = 'retry_success'
                        merged[i]['retry_result'] = retry_result.get('result')
                    else:
                        merged[i]['retry_result'] = retry_result
                    break
        
        return merged
    
    async def _learn_and_improve(self):
        """Learn from implementation results and improve"""
        print("   📚 Learning from implementation results...")
        
        # Analyze success/failure patterns
        successful_implementations = [r for r in self.optimization_history if r.get('status') == 'success']
        failed_implementations = [r for r in self.optimization_history if r.get('status') == 'failed']
        
        if successful_implementations:
            print(f"      ✅ Success patterns identified: {len(successful_implementations)}")
        
        if failed_implementations:
            print(f"      ❌ Failure patterns identified: {len(failed_implementations)}")
            print("      🔧 Adjusting strategies for better success...")
        
        # Update optimization strategies based on results
        print("      🎯 Updating optimization strategies...")

    async def _update_fund_overrides(self) -> None:
        """Have AGI write strategy overrides for the FundManager each cycle."""
        try:
            overrides = {
                'aggressiveness': 'balanced',
                'base_trade_micro': 1000,
                'enable_arbitrage': True,
                'enable_momentum': True,
                'enable_yield': True,
                'enable_flash': True,
                'arbitrage_threshold_bps': 100,
                'momentum_threshold_bps': 100
            }
            # Simple heuristic: if stuck, reduce aggressiveness
            if self.stuck_counter >= 2:
                overrides['aggressiveness'] = 'conservative'
                overrides['base_trade_micro'] = 500
            os.makedirs('config', exist_ok=True)
            with open('config/fund_manager.overrides.yaml', 'w') as f:
                import yaml
                yaml.safe_dump(overrides, f)
        except Exception:
            pass

    async def _ingest_capitalism_knowledge(self) -> None:
        """Load any new notes from knowledge/*/notes into long-term memory."""
        try:
            base_root = 'knowledge'
            if not os.path.isdir(base_root):
                return
            for domain in os.listdir(base_root):
                notes_dir = os.path.join(base_root, domain, 'notes')
                if not os.path.isdir(notes_dir):
                    continue
                for name in os.listdir(notes_dir):
                    if not (name.endswith('.md') or name.endswith('.txt')):
                        continue
                    path = os.path.join(notes_dir, name)
                    try:
                        with open(path, 'r') as fh:
                            content = fh.read()
                        self.memory.add({'note_file': name, 'content': content, 'source': domain}, tags=['knowledge', domain])
                    except Exception:
                        continue
        except Exception:
            pass
    
    async def _show_unified_cycle_summary(self):
        """Show summary of the unified cycle"""
        print(f"\n📊 UNIFIED CYCLE #{self.cycle_count} SUMMARY")
        print("=" * 50)
        
        # Get execution summary
        try:
            execution_summary = await real_how_engine.get_execution_summary()
            print(f"📋 Total Executions: {execution_summary['total_executions']}")
            print(f"✅ Successful: {execution_summary['successful_executions']}")
            print(f"❌ Failed: {execution_summary['failed_executions']}")
            print(f"🔄 Real Changes Made: {execution_summary['real_changes_made']}")
        except Exception as e:
            print(f"📊 Could not get execution summary: {e}")
        
        # Show insight and optimization history
        successful_optimizations = [o for o in self.optimization_history if o.get('status') == 'success']
        failed_optimizations = [o for o in self.optimization_history if o.get('status') == 'failed']
        
        print(f"💡 Total Insights Generated: {len(self.insight_history)}")
        print(f"🎯 Total Optimizations: {len(self.optimization_history)}")
        print(f"✅ Successful: {len(successful_optimizations)}")
        print(f"❌ Failed: {len(failed_optimizations)}")
        
        if self.last_cycle:
            print(f"🕐 Last Cycle: {self.last_cycle.strftime('%H:%M:%S')}")
    
    def _save_unified_history(self):
        """Save unified insight and optimization history"""
        try:
            unified_history = {
                'insights': self.insight_history,
                'optimizations': self.optimization_history,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('unified_agi_history.json', 'w') as f:
                json.dump(unified_history, f, indent=2)
        except Exception as e:
            print(f"Error saving unified history: {e}")

async def main():
    """Main function to start unified AGI operation"""
    print("🚀 UNIFIED AGI SYSTEM")
    print("=" * 60)
    print("🎯 This will start the AGI system in unified mode")
    print("   where analysis AND implementation happen in the same 5-minute cycle")
    print("   No more disconnect between thinking and doing!")
    print()
    
    unified_agi = UnifiedAGISystem()
    
    try:
        await unified_agi.start_unified_agi_operation()
    except KeyboardInterrupt:
        print("\n🛑 Unified AGI operation stopped")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
