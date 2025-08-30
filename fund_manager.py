#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional


class FundManager:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or self._load_config_file()
        self.aggressiveness = cfg.get('aggressiveness', 'balanced')  # conservative|balanced|aggressive
        self.base_trade_micro = int(cfg.get('base_trade_micro', 1000))
        self.enable_arbitrage = bool(cfg.get('enable_arbitrage', True))
        self.enable_momentum = bool(cfg.get('enable_momentum', True))
        self.enable_yield = bool(cfg.get('enable_yield', True))
        self.enable_flash = bool(cfg.get('enable_flash', True))

        # Thresholds (basis points)
        self.arbitrage_threshold_bps = int(cfg.get('arbitrage_threshold_bps', 100))  # 1%
        self.momentum_threshold_bps = int(cfg.get('momentum_threshold_bps', 100))    # 1%

        # Schedules
        self.consult_interval_sec = int(cfg.get('consult_interval_sec', 3600))
        self.last_consult_ts = 0.0

        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)

        # AGI overrides support
        self.overrides_path = cfg.get('overrides_path', 'config/fund_manager.overrides.yaml')
        self._overrides_mtime = 0.0
        # Capitalism Lab knowledge
        self.knowledge_path = 'knowledge/capitalism_lab/strategy_guidelines.yaml'
        self._knowledge = self._load_capitalism_knowledge()
        # Exploration/sandbox flags
        self.sandbox_enabled = bool(self._knowledge.get('exploration', {}).get('enable_sandbox', False))
        self.sandbox_budget_usd = float(self._knowledge.get('exploration', {}).get('max_sandbox_budget_usd', 0))

    def _load_config_file(self) -> Dict[str, Any]:
        try:
            import yaml
            cfg_path = 'config/fund_manager.yaml'
            if os.path.exists(cfg_path):
                with open(cfg_path, 'r') as f:
                    return yaml.safe_load(f) or {}
        except Exception:
            pass
        return {}

    def _load_capitalism_knowledge(self) -> Dict[str, Any]:
        try:
            import yaml
            if os.path.exists(self.knowledge_path):
                with open(self.knowledge_path, 'r') as f:
                    return yaml.safe_load(f) or {}
        except Exception:
            pass
        return {}

    def _size_factor(self) -> float:
        if self.aggressiveness == 'conservative':
            return 1.0
        if self.aggressiveness == 'aggressive':
            return 10.0
        return 3.0  # balanced

    def decide_plan(self, market_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        market_state keys:
          - tinyman_px, pact_px, spread (float), nav_usd (float), round (int)
        Returns per-strategy enable flags and sizes.
        """
        # Apply live overrides from AGI if present
        self.refresh_overrides_if_any()
        plan: Dict[str, Any] = {
            'arbitrage': {'enable': self.enable_arbitrage, 'size_micro': self.base_trade_micro},
            'momentum': {'enable': self.enable_momentum, 'size_micro': self.base_trade_micro},
            'yield': {'enable': self.enable_yield},
            'flash': {'enable': self.enable_flash},
        }

        # Dynamic thresholds
        spread = float(market_state.get('spread', 0.0) or 0.0)
        spread_bps = abs(spread) * 10000.0
        arb_min_bps = self.arbitrage_threshold_bps
        try:
            arb_min_bps = int(self._knowledge.get('thresholds', {}).get('arbitrage_min_spread_bps', arb_min_bps))
        except Exception:
            pass
        plan['arbitrage']['enable'] = self.enable_arbitrage and (spread_bps >= arb_min_bps)

        # Momentum sizing: scale with aggressiveness
        size_factor = self._size_factor()
        plan['momentum']['size_micro'] = int(self.base_trade_micro * size_factor)
        plan['arbitrage']['size_micro'] = int(self.base_trade_micro * size_factor)

        return plan

    def refresh_overrides_if_any(self) -> None:
        try:
            import yaml, os
            if not os.path.exists(self.overrides_path):
                return
            mtime = os.path.getmtime(self.overrides_path)
            if mtime <= self._overrides_mtime:
                return
            with open(self.overrides_path, 'r') as f:
                overrides = yaml.safe_load(f) or {}
            # Merge selected keys
            updated = {}
            for key in (
                'aggressiveness', 'base_trade_micro', 'enable_arbitrage', 'enable_momentum',
                'enable_yield', 'enable_flash', 'arbitrage_threshold_bps', 'momentum_threshold_bps'
            ):
                if key in overrides:
                    setattr(self, key, overrides[key] if key != 'base_trade_micro' else int(overrides[key]))
                    updated[key] = getattr(self, key)
            self._overrides_mtime = mtime
            with open('logs/fund_manager.log', 'a') as logf:
                logf.write(json.dumps({'event': 'overrides_applied', 'timestamp': datetime.now().isoformat(), 'overrides': updated}) + '\n')
        except Exception as e:
            try:
                with open('logs/fund_manager.log', 'a') as logf:
                    logf.write(json.dumps({'event': 'overrides_error', 'timestamp': datetime.now().isoformat(), 'error': str(e)}) + '\n')
            except Exception:
                pass

    def get_trade_size(self, requested_micro: int) -> int:
        """Optionally cap trade size when sandbox exploration is enabled."""
        try:
            if self.sandbox_enabled:
                return min(int(requested_micro), 3000)  # cap ~0.003 ALGO while sandboxing
        except Exception:
            pass
        return int(requested_micro)

    def should_promote_strategy(self, sandbox_pnl_usd: float) -> bool:
        """Promote from sandbox to live when PnL turns positive beyond small threshold."""
        try:
            return sandbox_pnl_usd >= 5.0
        except Exception:
            return False

    def compute_nav_based_size(self, nav_usd: float, price_usd_per_algo: float, fallback_micro: int) -> int:
        """Compute trade size (micro ALGO) from NAV percentage setting; fallback to provided size."""
        try:
            # Use exploration pool when exploring, otherwise production per-trade cap
            exploration_nav_pct = float(self._knowledge.get('exploration', {}).get('exploration_nav_pct', 0.0))
            per_trade_pct_of_pool = float(self._knowledge.get('exploration', {}).get('per_trade_pct_of_pool', 0.0))
            production_per_trade_pct = float(self._knowledge.get('risk', {}).get('per_trade_nav_pct_production', 0.0))
            base_per_trade_pct = float(self._knowledge.get('risk', {}).get('per_trade_nav_pct', 0.0))

            # Pool for exploration; per-trade size is fraction of that pool; else fallback to production cap
            if self.sandbox_enabled and exploration_nav_pct > 0 and per_trade_pct_of_pool > 0:
                pool_usd = nav_usd * (exploration_nav_pct / 100.0)
                pct = (per_trade_pct_of_pool / 100.0) * (pool_usd / max(nav_usd, 1e-9)) * 100.0
            else:
                pct = production_per_trade_pct or base_per_trade_pct

            if pct <= 0 or price_usd_per_algo <= 0 or nav_usd <= 0:
                return self.get_trade_size(fallback_micro)
            size_usd = nav_usd * (pct / 100.0)
            micro = int(max(1, (size_usd / price_usd_per_algo) * 1_000_000))
            return self.get_trade_size(micro)
        except Exception:
            return self.get_trade_size(fallback_micro)

    def maybe_consult_ceo_and_agi(self) -> Optional[Dict[str, Any]]:
        now = time.time()
        if now - self.last_consult_ts < self.consult_interval_sec:
            return None
        self.last_consult_ts = now
        advice = {
            'timestamp': datetime.now().isoformat(),
            'ceo_advice': 'Maintain diversified small-size executions; prioritize reliable DEX flows.',
            'agi_directive': 'Continue scanning DeFiLlama; propose new pools/assets; auto-tune thresholds.'
        }
        with open('logs/fund_manager.log', 'a') as f:
            f.write(json.dumps({'event': 'consult', **advice}) + '\n')
        # Try to consult the unified AGI for upgrade suggestions
        try:
            import subprocess, shlex
            env = os.environ.copy()
            env['PYTHONPATH'] = env.get('PYTHONPATH', '') + (':' if env.get('PYTHONPATH') else '') + os.getcwd()
            cmd = shlex.split('python3 /home/ubuntu/wealthyrobot/ask_unified_agi_needs.py')
            out = subprocess.check_output(cmd, env=env, timeout=20)
            agi_out = out.decode(errors='ignore')
            with open('logs/fund_manager.log', 'a') as f:
                f.write(json.dumps({'event': 'agi_consult_output', 'timestamp': datetime.now().isoformat(), 'output': agi_out[:2000]}) + '\n')
            advice['agi_output_excerpt'] = agi_out[:500]
        except Exception as e:
            with open('logs/fund_manager.log', 'a') as f:
                f.write(json.dumps({'event': 'agi_consult_error', 'timestamp': datetime.now().isoformat(), 'error': str(e)}) + '\n')
        return advice

    def propose_new_strategy(self, title: str, details: Dict[str, Any]) -> None:
        entry = {
            'timestamp': datetime.now().isoformat(),
            'title': title,
            'details': details
        }
        with open('data/strategy_proposals.jsonl', 'a') as f:
            f.write(json.dumps(entry) + '\n')


