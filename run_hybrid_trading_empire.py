#!/usr/bin/env python3
"""
Run Hybrid Algorand Trading Empire
- Uses HybridAlgorandTradingEmpire as the core system
- Adds smooth continuous operation, Algorand client init, Folks PC-297 bypass test,
  DeFiLlama scanning, and periodic health checks similar to the Unified system.
"""

import os
import json
import time
from datetime import datetime
from typing import Any, Dict, Optional
from fund_manager import FundManager
import time
import yaml
import json

# Import SDK manager for robust SDK handling
from sdk_imports import get_tinyman_client, get_tinyman_function, get_pact_client, is_sdk_available

USDC_ID = 31566704
ENABLE_ARBITRAGE = True
ENABLE_MOMENTUM = True
ENABLE_YIELD_FARMING = False  # DISABLED: Low ALGO balance
ENABLE_FLASH_LOAN = False     # DISABLED: Low ALGO balance
ENABLE_ASA_EXPANSION = True   # ENABLED: Real trading capability

# ALGO Safety Settings - Enhanced
MIN_ALGO_RESERVE = 10.0      # 10 ALGO minimum - EMERGENCY STOP
WARNING_ALGO_LEVEL = 25.0    # 25 ALGO warning level
TARGET_ALGO_LEVEL = 50.0     # 50 ALGO target for auto-topup
EMERGENCY_MODE = True        # Enable emergency ALGO conservation
ALGO_CHECK_ENABLED = True    # Enable ALGO balance checks on all operations
ALLOW_SAFE_FALLBACK = True  # Enable fallback status checks


def check_algo_balance_safety(algod_client, wallet_address: str) -> tuple:
    """Enhanced ALGO balance check with multiple safety levels"""
    try:
        account_info = algod_client.account_info(wallet_address)
        algo_balance = float(account_info.get('amount', 0)) / 1e6

        # Determine safety status
        if algo_balance < MIN_ALGO_RESERVE:
            status = "CRITICAL"
            is_safe = False
        elif algo_balance < WARNING_ALGO_LEVEL:
            status = "WARNING"
            is_safe = True  # Still safe but warning
        else:
            status = "SAFE"
            is_safe = True

        deficit = max(0, MIN_ALGO_RESERVE - algo_balance)

        return is_safe, algo_balance, deficit, status
    except Exception as e:
        print(f"⚠️ Error checking ALGO balance: {e}")
        return False, 0, MIN_ALGO_RESERVE, "ERROR"

def enforce_algo_safety(algod_client, wallet_address: str, operation_name: str) -> bool:
    """Enhanced ALGO safety enforcement with detailed logging"""
    if not ALGO_CHECK_ENABLED:
        return True  # Skip checks if disabled

    is_safe, balance, deficit, status = check_algo_balance_safety(algod_client, wallet_address)

    if status == "CRITICAL":
        print(f"🚨 ALGO EMERGENCY STOP: {operation_name}")
        print(f"   • Current Balance: {balance:.6f} ALGO")
        print(f"   • Required Minimum: {MIN_ALGO_RESERVE:.6f} ALGO")
        print(f"   • Deficit: {deficit:.6f} ALGO")
        print(f"   • 🚫 ALL TRADING DISABLED")
        return False
    elif status == "WARNING":
        print(f"⚠️ ALGO LOW WARNING: {operation_name}")
        print(f"   • Balance: {balance:.6f} ALGO (below {WARNING_ALGO_LEVEL:.1f})")
        print(f"   • Consider topping up ALGO reserves")
        # Still allow operations but log warning
    elif status == "SAFE":
        print(f"✅ ALGO SAFE: {operation_name} (Balance: {balance:.6f} ALGO)")

    return True  # Allow operation if not critical

def log_algo_balance_status(algod_client, wallet_address: str):
    """Log comprehensive ALGO balance status"""
    try:
        is_safe, balance, deficit, status = check_algo_balance_safety(algod_client, wallet_address)

        print(f"🛡️ ALGO STATUS: {status} - {balance:.6f} ALGO")

        if status == "CRITICAL":
            print(f"   🚨 CRITICAL: Below {MIN_ALGO_RESERVE:.1f} ALGO minimum!")
            print(f"   💡 Need {deficit:.6f} more ALGO to reach safety net")
        elif status == "WARNING":
            print(f"   ⚠️ WARNING: Below {WARNING_ALGO_LEVEL:.1f} ALGO")
            print(f"   💡 Recommended: Top up to {TARGET_ALGO_LEVEL:.1f} ALGO")

        return status, balance
    except Exception as e:
        print(f"⚠️ Error logging ALGO status: {e}")
        return "ERROR", 0

def _load_env_credentials(env_path: str = '.env') -> Dict[str, str]:
    wallet_address = None
    mnemonic_phrase = None
    if not os.path.exists(env_path):
        return {}
    with open(env_path, 'r') as f:
        lines = f.read().splitlines()
    collecting_mnemonic = False
    mnemonic_parts = []
    for line in lines:
        if collecting_mnemonic and line.strip() == '':
            collecting_mnemonic = False
            continue
        if not collecting_mnemonic:
            if line.startswith('ALGORAND_WALLET_ADDRESS='):
                wallet_address = line.split('=', 1)[1].strip()
            elif line.startswith('ALGORAND_WALLET_MNEMONIC='):
                first = line.split('=', 1)[1].strip()
                mnemonic_parts.append(first)
                collecting_mnemonic = True
        else:
            mnemonic_parts.append(line.strip())
    if mnemonic_parts:
        mnemonic_phrase = ' '.join(' '.join(mnemonic_parts).split())
    return {
        'wallet_address': wallet_address or '',
        'wallet_mnemonic': mnemonic_phrase or ''
    }


def init_algorand_clients() -> Dict[str, Any]:
    from algosdk.v2client import algod, indexer
    algod_address = os.getenv('ALGOD_ADDRESS', 'https://mainnet-api.algonode.cloud')
    indexer_address = os.getenv('INDEXER_ADDRESS', 'https://mainnet-idx.algonode.cloud')
    algod_client = algod.AlgodClient(os.getenv('ALGOD_TOKEN', ''), algod_address)
    indexer_client = indexer.IndexerClient(os.getenv('INDEXER_TOKEN', ''), indexer_address)
    # Sanity checks
    status = algod_client.status()
    health = indexer_client.health()
    print(f"✅ Algorand connected. Round: {status.get('last-round')} | Indexer: {health.get('status', 'Unknown')}")
    return {'algod': algod_client, 'indexer': indexer_client}


def init_folks_pc297_client(algod_client, wallet_address: str, wallet_mnemonic: str):
    from algosdk import mnemonic
    from FINAL_DEFI_SOLUTION import FinalDeFiSolution
    private_key = mnemonic.to_private_key(wallet_mnemonic)
    folks_client = FinalDeFiSolution(
        algod_client=algod_client,
        wallet_address=wallet_address,
        private_key=private_key
    )
    return folks_client


def test_pc297_bypass(folks_client) -> Dict[str, Any]:
    try:
        print('🧪 Testing PC 297 bypass via Folks Finance...')
        result = folks_client.execute_folks_finance_operation(
            operation='TestUpdate', app_args=[b'test'], assets=[0]
        )
        ok = bool(result.get('pc_297_bypassed') or result.get('success'))
        status = 'bypassed' if result.get('pc_297_bypassed') else 'pending' if ok else 'failed'
        print(f"PC 297 status: {status}")
        return {'ok': ok, 'status': status, 'raw': result}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def do_defillama_sweep() -> Dict[str, Any]:
    # Use comprehensive scanner which includes DeFiLlama
    from comprehensive_opportunity_scanner import ComprehensiveOpportunityScanner
    import asyncio

    try:
        scanner = ComprehensiveOpportunityScanner()
        opportunities: list = asyncio.run(scanner.scan_all_opportunities())
        top = scanner.get_top_opportunities(5)
        print(f"🔎 DeFiLlama+ scan found {len(opportunities)} opportunities; top={len(top)}")

        return {
            'count': len(opportunities),
            'top': top,
        }
    except Exception as e:
        print(f"❌ Sweep failed: {e}")
        import traceback
        traceback.print_exc()
        # Return empty result to prevent crashes
        return {
            'count': 0,
            'top': [],
        }


def _load_exploration_cfg(path: str = 'config/exploration.yaml') -> Dict[str, Any]:
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
    except Exception:
        pass
    return {}


def explore_new_protocols(top: list, clients: Dict[str, Any], creds: Dict[str, str]) -> None:
    PROVEN_PATH = 'config/proven.yaml'
    SCORE_PATH = 'data/exploration_score.json'
    os.makedirs('data', exist_ok=True)

    cfg = _load_exploration_cfg()
    filters = cfg.get('filters', {})
    sizing = cfg.get('sizing', {})
    safety = cfg.get('safety', {})
    min_tvl = float(filters.get('min_tvl_usd', 0))
    min_apy = float(filters.get('min_net_apy_pct', 0))
    allow = set([str(x).lower() for x in filters.get('allow_protocols', [])])
    max_seed = int(sizing.get('max_seed_trade_micro', 5_000_000))
    min_reserve = int(sizing.get('min_algo_reserve_micro', 5_000_000))
    throttle = int(safety.get('throttle_seconds', 60))
    dry_run = bool(safety.get('dry_run', False))

    # Load proven set
    proven = set()
    try:
        if os.path.exists(PROVEN_PATH):
            with open(PROVEN_PATH, 'r') as f:
                p = yaml.safe_load(f) or {}
                proven = set(str(x).lower() for x in p.get('protocols', []))
    except Exception:
        proven = set()

    # Load scores
    score = {}
    try:
        if os.path.exists(SCORE_PATH):
            with open(SCORE_PATH, 'r') as f:
                score = json.load(f) or {}
    except Exception:
        score = {}

    def _save_score():
        try:
            with open(SCORE_PATH, 'w') as f:
                json.dump(score, f)
        except Exception:
            pass

    def _promote_if_ready(proto_key: str, threshold: int = 3) -> None:
        nonlocal proven
        if score.get(proto_key, 0) >= threshold and proto_key not in proven:
            try:
                # Append to proven.yaml
                current = {'protocols': sorted(list(proven | {proto_key}))}
                if os.path.exists(PROVEN_PATH):
                    with open(PROVEN_PATH, 'r') as f:
                        cur = yaml.safe_load(f) or {}
                        cur_set = set(str(x).lower() for x in cur.get('protocols', []))
                        current = {'protocols': sorted(list(cur_set | {proto_key}))}
                os.makedirs('config', exist_ok=True)
                with open(PROVEN_PATH, 'w') as f:
                    yaml.safe_dump(current, f)
                proven.add(proto_key)
                print(f"   ✅ Promoted protocol to proven: {proto_key}")
            except Exception as e:
                print(f"   ⚠️ Promotion save error: {e}")

    from algosdk import mnemonic as _mn, account as _acct
    try:
        sk = _mn.to_private_key(creds['wallet_mnemonic'])
        sender = _acct.address_from_private_key(sk)
    except Exception:
        return

    last = 0.0
    for opp in (top or []):
        proto = str(opp.get('protocol_name') or opp.get('source') or '').lower()
        if proto in proven:
            continue
        tvl = float(opp.get('tvl_usd', opp.get('tvl', 0)) or 0)
        apy = float(opp.get('estimated_apy', opp.get('apy', 0)) or 0)
        if allow and proto not in allow:
            continue
        if tvl < min_tvl or apy < min_apy:
            continue
        if time.time() - last < throttle:
            continue
        # Seed only Tinyman pools here; other protocols can be integrated similarly
        if 'tinyman' in proto or 'dex' in (opp.get('opportunity_type','').lower()):
            try:
                from algosdk import mnemonic as _mn, account as _acct
                # Use small seed, bounded by availability in helper
                acct = clients['algod'].account_info(sender)
                avail = int(acct.get('amount',0))
                amount = min(max_seed, 1_000_000)
                if avail - amount < min_reserve:
                    print(f"   ⚠️ Exploration skipped (reserve): avail={avail} need_reserve={min_reserve}")
                    continue
                res = build_tinyman_fixed_input_swap(clients, sender, sk, asset_in_id=0, asset_out_id=USDC_ID, amount_in_micro=amount)
                print(f"   🔎 Exploration seed on {proto}: {res}")
                # Record success and check for promotion
                if res and res.get('ok'):
                    score[proto] = score.get(proto, 0) + 1
                    _save_score()
                    _promote_if_ready(proto)
                last = time.time()
                if dry_run:
                    break
            except Exception as e:
                print(f"   ⚠️ Exploration seed error: {e}")


def execute_infra_self_transfer(algod_client, wallet_address: str, wallet_mnemonic: str) -> Dict[str, Any]:
    # DISABLED: This function has been disabled to prevent wasteful wallet-to-wallet transactions
    # It now returns a safe status check instead
    try:
        status = algod_client.status()
        current_round = status.get('last-round', 0)
        return {'ok': True, 'status_check': True, 'round': current_round, 'message': 'Status check only - no transaction'}
    except Exception as e:
        return {'ok': False, 'error': f'Status check failed: {str(e)}'}


def ensure_asset_optin(algod, sender_addr: str, sender_sk: bytes, asset_id: int) -> None:
    # Use SDK manager for tinyman imports
    prepare_asset_optin_transactions = get_tinyman_function('prepare_asset_optin_transactions')
    if not prepare_asset_optin_transactions:
        print("⚠️ Tinyman not available for asset opt-in, skipping")
        return

    # Check holdings to avoid redundant opt-in
    try:
        acct = algod.account_info(sender_addr)
        held = {a.get('asset-id') for a in acct.get('assets', [])}
        if asset_id in held:
            return
    except Exception:
        pass
    params = algod.suggested_params()
    group = prepare_asset_optin_transactions(asset_id=asset_id, sender=sender_addr, suggested_params=params)
    group.sign_with_private_key(sender_addr, sender_sk)
    try:
        group.submit(algod, wait=True)
    except Exception:
        # Likely already opted-in or transient
        pass


def _load_asa_targets_config(path: str = 'config/asa_targets.yaml') -> list:
    try:
        import yaml
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = yaml.safe_load(f) or {}
            assets = data.get('assets', [])
            # normalize types
            normalized = []
            for a in assets:
                try:
                    normalized.append({
                        'symbol': str(a.get('symbol', '')).upper(),
                        'asset_id': int(a.get('asset_id', 0)),
                        'enabled': bool(a.get('enabled', False)),
                        'seed_trade_micro': int(a.get('seed_trade_micro', 10_000))
                    })
                except Exception:
                    continue
            return normalized
    except Exception:
        return []
    return []


def build_tinyman_fixed_input_swap(clients: Dict[str, Any], sender_addr: str, sender_sk: bytes,
                                   asset_in_id: int = 0, asset_out_id: int = USDC_ID,
                                   amount_in_micro: int = 1000) -> Dict[str, Any]:
    """Build and submit a Tinyman fixed-input swap with minimal slippage protection."""
    try:
        # Use SDK manager for robust imports - try real SDK first, fallback if needed
        print("🔄 Initializing Tinyman swap...")

        prepare_swap_transactions = get_tinyman_function('prepare_swap_transactions')
        get_pool_info = get_tinyman_function('get_pool_info')
        calculate_fixed_input_swap = get_tinyman_function('calculate_fixed_input_swap')
        FIXED_INPUT_APP_ARGUMENT = get_tinyman_function('FIXED_INPUT_APP_ARGUMENT')

        # Check if we have fallback functions available
        if not all([prepare_swap_transactions, get_pool_info, calculate_fixed_input_swap]):
            print("⚠️ Tinyman functions not available, using fallback")
            return {'ok': False, 'error': 'Tinyman functions not available'}

        if not is_sdk_available('tinyman'):
            print("⚠️ Tinyman SDK not available, using fallback functions")

        algod = clients['algod']

        # Handle fallback client initialization
        if is_sdk_available('tinyman'):
            client = get_tinyman_client(algod)
            validator_app_id = client.validator_app_id
        else:
            # Use fallback client with mock validator_app_id
            # Check if emergency fallback has been activated
            import os
            switch_file = '/tmp/tinyman_app_switch.txt'
            if os.path.exists(switch_file):
                with open(switch_file, 'r') as f:
                    validator_app_id = int(f.read().strip())
                print(f"🔄 EMERGENCY FALLBACK ACTIVE - Using alternative app: {validator_app_id}")
                print("🎯 All future transactions will use this alternative app")
            else:
                validator_app_id = 1002541853  # RESTORE WORKING Tinyman validator app ID (was working before)
                print(f"🔄 Using fallback client with validator_app_id: {validator_app_id}")

            client = get_tinyman_client()

        # Ensure USDC opt-in
        if asset_out_id != 0:
            ensure_asset_optin(algod, sender_addr, sender_sk, asset_out_id)

        # Determine pool order and fetch pool reserves
        a1, a2 = (0, asset_out_id) if 0 < asset_out_id else (asset_out_id, 0)
        pool = get_pool_info(algod, validator_app_id, a1, a2)
        reserve_a = int(pool.get('asset_1_reserves', 0))
        reserve_b = int(pool.get('asset_2_reserves', 0))
        total_fee_share = int(pool.get('total_fee_share', 3000))  # default 0.3%

        # Map reserves to input/output based on asset ids
        if asset_in_id == a1:
            input_supply, output_supply = reserve_a, reserve_b
        else:
            input_supply, output_supply = reserve_b, reserve_a

        # For stability, use a minimal min-out to avoid validator assert on tiny sizes
        min_out = 1

        params = algod.suggested_params()
        group = prepare_swap_transactions(
            validator_app_id=validator_app_id,
            asset_1_id=a1,
            asset_2_id=a2,
            asset_in_id=asset_in_id,
            asset_in_amount=amount_in_micro,
            asset_out_amount=min_out,
            swap_type=FIXED_INPUT_APP_ARGUMENT,
            sender=sender_addr,
            suggested_params=params,
            app_call_note=b'wr_hybrid_swap_quoted'
        )
        group.sign_with_private_key(sender_addr, sender_sk)
        submit_res = group.submit(algod, wait=True)
        txid = submit_res.get('txid')
        return {'ok': True, 'tx_id': txid, 'round': submit_res.get('confirmed-round')}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def try_tinyman_swap_with_retry(clients: Dict[str, Any], sender: str, sk: bytes,
                                asset_in_id: int = 0, asset_out_id: int = USDC_ID) -> Dict[str, Any]:
    first = build_tinyman_fixed_input_swap(clients, sender, sk, asset_in_id=asset_in_id, asset_out_id=asset_out_id, amount_in_micro=1000)
    if first.get('ok'):
        return first
    # Retry with slightly larger input to avoid tiny-amount assertions
    second = build_tinyman_fixed_input_swap(clients, sender, sk, asset_in_id=asset_in_id, asset_out_id=asset_out_id, amount_in_micro=3000)
    if second.get('ok'):
        return second
    # Final attempt: 0.01 ALGO
    third = build_tinyman_fixed_input_swap(clients, sender, sk, asset_in_id=asset_in_id, asset_out_id=asset_out_id, amount_in_micro=10000)
    if third.get('ok'):
        return third
    return third or second or first


def attempt_execute_top_opportunity(top: list, clients: Dict[str, Any], creds: Dict[str, str], folks_client) -> None:
    if not top:
        return
    first = top[0]
    name = (first.get('protocol_name') or first.get('pool_name') or '').lower()
    print(f"🚀 Attempting execution for top opportunity: {first.get('source')} - {name}")
    try:
        if 'folks' in name:
            res = folks_client.execute_folks_finance_operation(operation='TestUpdate', app_args=[b'test'], assets=[0])
            print(f"   Folks test update result: {res.get('note', res)}")
            return
        if 'tinyman' in name or 'dex' in name or 'swap' in name or 'ultra' in name:
            # Attempt a tiny ALGO->USDC swap via Tinyman
            try:
                from algosdk import mnemonic as _mn, account as _acct
                sk = _mn.to_private_key(creds['wallet_mnemonic'])
                sender = _acct.address_from_private_key(sk)
                swapr = try_tinyman_swap_with_retry(clients, sender, sk)
                if swapr.get('ok'):
                    print(f"   ✅ Tinyman swap confirmed in round {swapr.get('round')} (tx {swapr.get('tx_id')})")
                    return
                elif swapr.get('fallback_to_status'):
                    print(f"   🔄 Swap failed due to missing application, falling back to status check")
                else:
                    print(f"   ⚠️ Tinyman swap failed: {swapr}")
            except Exception as dex_e:
                print(f"   ⚠️ Tinyman swap exception: {dex_e}")
        # Optional fallback: lightweight status check (no gas fees)
        if ALLOW_SAFE_FALLBACK:
            try:
                status = clients['algod'].status()
                current_round = status.get('last-round', 0)
                print(f"   ✅ Infra status check passed - Round {current_round}")
            except Exception as e:
                print(f"   ⚠️ Infra status check failed: {e}")
    except Exception as e:
        print(f"   ❌ Execution error: {e}")


def _get_tinyman_mid_price(algod, asset_1_id: int, asset_2_id: int) -> Optional[float]:
    try:
        if not is_sdk_available('tinyman'):
            return None

        get_pool_info = get_tinyman_function('get_pool_info')
        if not get_pool_info:
            return None

        client = get_tinyman_client(algod)
        validator_app_id = client.validator_app_id
        a1, a2 = (asset_1_id, asset_2_id) if asset_1_id < asset_2_id else (asset_2_id, asset_1_id)
        pool = get_pool_info(algod, validator_app_id, a1, a2)
        r1 = float(pool.get('asset_1_reserves', 0))
        r2 = float(pool.get('asset_2_reserves', 0))
        if r1 <= 0 or r2 <= 0:
            return None
        # Price = USDC per ALGO when asset_1_id == 0 (ALGO) and asset_2_id == USDC
        if a1 == 0 and a2 == USDC_ID:
            return r2 / r1
        # If reversed, invert
        if a1 == USDC_ID and a2 == 0:
            return r1 / r2
        return None
    except Exception:
        return None


def _get_pact_mid_price(algod) -> Optional[float]:
    """Fetch Pact ALGO/USDC mid price from pool reserves if available."""
    try:
        from pactsdk import PactClient
        pc = PactClient(algod, network='mainnet')
        pools = pc.fetch_pools_by_assets(0, USDC_ID)  # list
        if not pools:
            return None
        p = pools[0]
        # p may have properties asset_1_reserves, asset_2_reserves or similar
        r1 = float(getattr(p, 'asset1_reserves', getattr(p, 'asset_1_reserves', 0)))
        r2 = float(getattr(p, 'asset2_reserves', getattr(p, 'asset_2_reserves', 0)))
        # Determine orientation
        aid1 = int(getattr(p, 'asset1_id', getattr(p, 'asset_1_id', 0)))
        aid2 = int(getattr(p, 'asset2_id', getattr(p, 'asset_2_id', 0)))
        if r1 <= 0 or r2 <= 0:
            return None
        if aid1 == 0 and aid2 == USDC_ID:
            return r2 / r1
        if aid1 == USDC_ID and aid2 == 0:
            return r1 / r2
        return None
    except Exception:
        return None


def run_arbitrage_cycle(clients: Dict[str, Any], creds: Dict[str, str], fund: Optional[FundManager] = None, size_override_micro: Optional[int] = None) -> None:
    if not ENABLE_ARBITRAGE:
        return

    # ALGO Safety Check
    if not enforce_algo_safety(clients['algod'], creds['wallet_address'], 'Arbitrage'):
        return

    algod = clients['algod']
    tinyman_px = _get_tinyman_mid_price(algod, 0, USDC_ID)
    pact_px = _get_pact_mid_price(algod)
    if not tinyman_px or not pact_px:
        return
    spread = (tinyman_px - pact_px) / pact_px
    print(f"   ℹ️ Arbitrage check: Tinyman {tinyman_px:.6f} vs Pact {pact_px:.6f} -> spread {spread*100:.2f}%")
    # Only proceed if notable spread
    threshold = 0.01  # default 1%
    if fund and hasattr(fund, 'arbitrage_threshold_bps'):
        try:
            threshold = max(0.0, float(fund.arbitrage_threshold_bps) / 10000.0)
        except Exception:
            pass
    if abs(spread) < threshold:
        return
    try:
        from algosdk import mnemonic as _mn, account as _acct
        sk = _mn.to_private_key(creds['wallet_mnemonic'])
        sender = _acct.address_from_private_key(sk)
        # Use ALGO->USDC leg only (sells ALGO where price is higher) for safety
        trade_size = size_override_micro or (fund.base_trade_micro if fund else 1000)
        if fund:
            # Compute NAV-based micro size (per_trade_nav_pct) if price is known
            nav = estimate_nav_usd(clients, creds['wallet_address']) or 0.0
            px = _get_tinyman_mid_price(clients['algod'], 0, USDC_ID) or 0.0
            trade_size = fund.compute_nav_based_size(nav, px, trade_size)
        use_tinyman = tinyman_px > pact_px
        if use_tinyman:
            res = build_tinyman_fixed_input_swap(clients, sender, sk, asset_in_id=0, asset_out_id=USDC_ID, amount_in_micro=trade_size)
            if res.get('ok'):
                print(f"   ✅ Arbitrage leg: Sold ALGO on Tinyman at favorable price; round {res.get('round')} tx {res.get('tx_id')}")
            else:
                print(f"   ⚠️ Arbitrage Tinyman leg failed: {res}")
        else:
            # Attempt Pact leg: sell ALGO->USDC on Pact if Pact shows higher price
            try:
                import pactsdk
                from pactsdk import PactClient
                from algosdk import mnemonic as _mn, account as _acct
                algod = clients['algod']
                pc = PactClient(algod, network='mainnet')
                pools = pc.fetch_pools_by_assets(0, USDC_ID)
                if not pools:
                    print("   ⚠️ Arbitrage: No Pact pool found")
                    return
                pool = pools[0]
                # Prepare fixed-input swap of ALGO amount trade_size to USDC with 10% slippage cap
                swap = pool.prepare_swap(asset=pool.asset1 if getattr(pool, 'asset1_id', 0) == 0 else pool.asset2,
                                         amount=trade_size,
                                         slippage_pct=10.0,
                                         swap_for_exact=False)
                tg = pool.prepare_swap_tx_group(swap, sender)
                tg.sign_with_private_key(sender, sk)
                res = tg.submit(algod, wait=True)
                print(f"   ✅ Arbitrage Pact leg: Sold ALGO on Pact; round {res.get('confirmed-round')} tx {res.get('txid')}")
            except Exception as pe:
                print(f"   ⚠️ Arbitrage Pact leg error: {pe}")
    except Exception as e:
        print(f"   ⚠️ Arbitrage error: {e}")


def run_momentum_cycle(clients: Dict[str, Any], creds: Dict[str, str], fund: Optional[FundManager] = None, size_override_micro: Optional[int] = None) -> None:
    if not ENABLE_MOMENTUM:
        return

    # ALGO Safety Check
    if not enforce_algo_safety(clients['algod'], creds['wallet_address'], 'Momentum'):
        return

    algod = clients['algod']
    # Price from Tinyman ALGO/USDC mid
    px = _get_tinyman_mid_price(algod, 0, USDC_ID)
    if not px:
        return
    os.makedirs('data', exist_ok=True)
    hist_path = 'data/price_history.jsonl'
    try:
        with open(hist_path, 'a') as f:
            f.write(json.dumps({'ts': datetime.now().isoformat(), 'price': px}) + '\n')
    except Exception:
        pass
    # Read last 20 points
    hist = []
    try:
        with open(hist_path, 'r') as f:
            for line in f.readlines()[-20:]:
                try:
                    obj = json.loads(line.strip())
                    if 'price' in obj:
                        hist.append(float(obj['price']))
                except Exception:
                    continue
    except Exception:
        return
    if len(hist) < 5:
        return
    sma = sum(hist) / len(hist)
    # Simple rule: if price below SMA by >1%, trim ALGO a tiny amount (sell to USDC)
    momentum_thr = 0.01
    if fund and hasattr(fund, 'momentum_threshold_bps'):
        try:
            momentum_thr = max(0.0, float(fund.momentum_threshold_bps) / 10000.0)
        except Exception:
            pass
    if px < sma * (1.0 - momentum_thr):
        try:
            from algosdk import mnemonic as _mn, account as _acct
            sk = _mn.to_private_key(creds['wallet_mnemonic'])
            sender = _acct.address_from_private_key(sk)
            trade_size = size_override_micro or (fund.base_trade_micro if fund else 1000)
            if fund:
                nav = estimate_nav_usd(clients, creds['wallet_address']) or 0.0
                px = _get_tinyman_mid_price(clients['algod'], 0, USDC_ID) or 0.0
                trade_size = fund.compute_nav_based_size(nav, px, trade_size)
            res = build_tinyman_fixed_input_swap(clients, sender, sk, asset_in_id=0, asset_out_id=USDC_ID, amount_in_micro=trade_size)
            if res.get('ok'):
                print(f"   ✅ Momentum: Sold small ALGO as downtrend hedge; round {res.get('round')} tx {res.get('tx_id')}")
            else:
                print(f"   ⚠️ Momentum sell failed: {res}")
        except Exception as e:
            print(f"   ⚠️ Momentum error: {e}")


def run_yield_farming_cycle(clients: Dict[str, Any], creds: Dict[str, str]) -> None:
    if not ENABLE_YIELD_FARMING:
        return

    # ALGO Safety Check
    if not enforce_algo_safety(clients['algod'], creds['wallet_address'], 'Yield Farming'):
        return

    try:
        if not is_sdk_available('tinyman'):
            print("⚠️ Yield farming error: Tinyman SDK not available")
            return

        get_pool_info = get_tinyman_function('get_pool_info')
        prepare_flexible_add_liquidity_transactions = get_tinyman_function('prepare_flexible_add_liquidity_transactions')

        if not get_pool_info:
            print("⚠️ Yield farming error: get_pool_info not available")
            return

        from algosdk import mnemonic as _mn, account as _acct
        algod = clients['algod']
        sk = _mn.to_private_key(creds['wallet_mnemonic'])
        sender = _acct.address_from_private_key(sk)

        client = get_tinyman_client(algod)
        validator_app_id = client.validator_app_id
        # Target ALGO/USDC pool
        a1, a2 = (0, USDC_ID) if 0 < USDC_ID else (USDC_ID, 0)
        pool = get_pool_info(algod, validator_app_id, a1, a2)
        reserve_a = int(pool.get('asset_1_reserves', 0))
        reserve_b = int(pool.get('asset_2_reserves', 0))
        pta = pool.get('pool_token_asset_id')
        if not pta:
            # Sometimes Tinyman returns nested object or raw id under different key
            pta_obj = pool.get('pool_token_asset')
            if isinstance(pta_obj, dict):
                pta = pta_obj.get('id')
            elif isinstance(pta_obj, int):
                pta = pta_obj
        try:
            pool_token_asset_id = int(pta)
        except Exception:
            pool_token_asset_id = 0
        print(f"   ℹ️ Yield farming: pool info ok; pta={pta}, pool_token_asset_id={pool_token_asset_id}, reserves=({reserve_a},{reserve_b})")
        if pool_token_asset_id <= 0:
            print("   ⚠️ Yield farming: missing pool token id; skipping")
            return

        # Opt-in target assets and pool token
        ensure_asset_optin(algod, sender, sk, USDC_ID)
        ensure_asset_optin(algod, sender, sk, pool_token_asset_id)

        # Compute small proportional amounts based on reserves
        if reserve_a <= 0 or reserve_b <= 0:
            # No liquidity in pool; skip to avoid bootstrapping
            print("   ⚠️ Yield farming: pool has no reserves; skipping")
            return
        # Deposit ~0.01 ALGO worth to avoid min-mint assertions
        algo_in = 10000 if a1 == 0 else max(10000, int(10000 * reserve_a / max(1, reserve_b)))
        usdc_in = int(algo_in * reserve_b / max(1, reserve_a)) if a1 == 0 else 10000
        asset_1_amount = algo_in if a1 == 0 else usdc_in
        asset_2_amount = usdc_in if a1 == 0 else algo_in

        params = algod.suggested_params()
        import traceback
        try:
            group = prepare_flexible_add_liquidity_transactions(
                validator_app_id=validator_app_id,
                asset_1_id=a1,
                asset_2_id=a2,
                pool_token_asset_id=pool_token_asset_id,
                asset_1_amount=asset_1_amount,
                asset_2_amount=asset_2_amount,
                min_pool_token_asset_amount=1,
                sender=sender,
                suggested_params=params,
                app_call_note=b'wr_yield_add_liquidity'
            )
            group.sign_with_private_key(sender, sk)
            submit_res = group.submit(algod, wait=True)
            print(f"   ✅ Yield farming: Added tiny liquidity; round {submit_res.get('confirmed-round')} tx {submit_res.get('txid')}")
        except Exception as e:
            # Fallback to single-asset add (ALGO side if available)
            try:
                prepare_single_asset_add_liquidity_transactions = get_tinyman_function('prepare_single_asset_add_liquidity_transactions')
                if not prepare_single_asset_add_liquidity_transactions:
                    print("⚠️ Single asset add liquidity not available")
                    return

                single_asset_amount = 30000  # 0.03 ALGO equivalent
                # Try asset_1 side first
                sa1 = single_asset_amount
                sa2 = None
                group2 = prepare_single_asset_add_liquidity_transactions(
                    validator_app_id=validator_app_id,
                    asset_1_id=a1,
                    asset_2_id=a2,
                    pool_token_asset_id=pool_token_asset_id,
                    min_pool_token_asset_amount=1,
                    sender=sender,
                    suggested_params=params,
                    asset_1_amount=sa1,
                    asset_2_amount=sa2,
                    app_call_note=b'wr_yield_single_asset_add'
                )
                group2.sign_with_private_key(sender, sk)
                submit_res2 = group2.submit(algod, wait=True)
                print(f"   ✅ Yield farming: Single-asset add; round {submit_res2.get('confirmed-round')} tx {submit_res2.get('txid')}")
            except Exception as e2:
                # Try asset_2 side if first side failed
                try:
                    sa1 = None
                    sa2 = single_asset_amount
                    group3 = prepare_single_asset_add_liquidity_transactions(
                        validator_app_id=validator_app_id,
                        asset_1_id=a1,
                        asset_2_id=a2,
                        pool_token_asset_id=pool_token_asset_id,
                        min_pool_token_asset_amount=1,
                        sender=sender,
                        suggested_params=params,
                        asset_1_amount=sa1,
                        asset_2_amount=sa2,
                        app_call_note=b'wr_yield_single_asset_add_b'
                    )
                    group3.sign_with_private_key(sender, sk)
                    submit_res3 = group3.submit(algod, wait=True)
                    print(f"   ✅ Yield farming: Single-asset add (asset_2); round {submit_res3.get('confirmed-round')} tx {submit_res3.get('txid')}")
                except Exception as e3:
                    print("   ⚠️ Yield farming errors:\n", traceback.format_exc())
    except Exception as e:
        print(f"   ⚠️ Yield farming error: {e}")


def write_health(status: Dict[str, Any]) -> None:
    os.makedirs('logs', exist_ok=True)
    health_file = f"logs/hybrid_health_{datetime.now().strftime('%Y%m%d')}.json"
    with open(health_file, 'a') as f:
        f.write(json.dumps(status) + '\n')


def write_plan_history(plan: Dict[str, Any], market_state: Dict[str, Any]) -> None:
    os.makedirs('data', exist_ok=True)
    entry = {
        'timestamp': datetime.now().isoformat(),
        'plan': plan,
        'market_state': market_state
    }
    with open('data/plan_history.jsonl', 'a') as f:
        f.write(json.dumps(entry) + '\n')


def estimate_nav_usd(clients: Dict[str, Any], wallet_address: str) -> Optional[float]:
    """Estimate NAV in USD using ALGO and USDC balances and Tinyman mid price."""
    try:
        algod = clients['algod']
        acct = algod.account_info(wallet_address)
        algo = float(acct.get('amount', 0)) / 1e6
        usdc_micro = 0
        for a in acct.get('assets', []):
            if int(a.get('asset-id', 0)) == USDC_ID:
                usdc_micro = int(a.get('amount', 0))
                break
        usdc = float(usdc_micro) / 1e6
        px = _get_tinyman_mid_price(algod, 0, USDC_ID) or 0.0
        return usdc + algo * px
    except Exception:
        return None


def run_flash_loan_cycle(clients: Dict[str, Any], creds: Dict[str, str]) -> None:
    if not ENABLE_FLASH_LOAN:
        return

    # ALGO Safety Check
    if not enforce_algo_safety(clients['algod'], creds['wallet_address'], 'Flash Loan'):
        return

    # Very small, safe flash-loan test: borrow tiny USDC and immediately repay within group
    try:
        if not is_sdk_available('tinyman'):
            print("⚠️ Flash loan error: Tinyman SDK not available")
            return

        prepare_flash_loan_transactions = get_tinyman_function('prepare_flash_loan_transactions')
        if not prepare_flash_loan_transactions:
            print("⚠️ Flash loan error: prepare_flash_loan_transactions not available")
            return

        from algosdk import mnemonic as _mn, account as _acct
        algod = clients['algod']
        sk = _mn.to_private_key(creds['wallet_mnemonic'])
        sender = _acct.address_from_private_key(sk)

        client = get_tinyman_client(algod)
        validator_app_id = client.validator_app_id

        # Ensure USDC opt-in
        ensure_asset_optin(algod, sender, sk, USDC_ID)

        params = algod.suggested_params()
        # Order so that asset_2_id is ALGO (0) to let helper create PaymentTxn for repay
        a1, a2 = (USDC_ID, 0)
        asset_1_loan_amount = 0
        asset_2_loan_amount = 10_000  # 0.01 ALGO
        # Pay back loan + small premium
        asset_1_payment_amount = 0
        asset_2_payment_amount = asset_2_loan_amount + 200
        tx_list = []  # no intermediate transactions for the smoke test
        group = prepare_flash_loan_transactions(
            validator_app_id,
            a1,
            a2,
            asset_1_loan_amount,
            asset_2_loan_amount,
            asset_1_payment_amount,
            asset_2_payment_amount,
            tx_list,
            sender,
            params,
            app_call_note=b'wr_flash_loan_test'
        )
        group.sign_with_private_key(sender, sk)
        res = group.submit(algod, wait=True)
        print(f"   ✅ Flash loan test executed; round {res.get('confirmed-round')} tx {res.get('txid')}")
    except Exception as e:
        print(f"   ⚠️ Flash loan error: {e}")


def run_asa_expansion_cycle(clients: Dict[str, Any], creds: Dict[str, str]) -> None:
    """Seed small ALGO->ASA swaps for enabled targets to expand asset coverage and test liquidity paths."""
    try:
        # ALGO Safety Check
        if not enforce_algo_safety(clients['algod'], creds['wallet_address'], 'ASA Expansion'):
            return

        targets = _load_asa_targets_config()
        if not targets:
            return
        from algosdk import mnemonic as _mn, account as _acct
        algod = clients['algod']
        sk = _mn.to_private_key(creds['wallet_mnemonic'])
        sender = _acct.address_from_private_key(sk)
        for t in targets:
            if not t.get('enabled'):
                continue
            aid = int(t.get('asset_id', 0))
            if aid <= 0:
                continue
            # Ensure opt-in
            ensure_asset_optin(algod, sender, sk, aid)
            # Attempt a tiny swap ALGO->ASA via Tinyman
            res = build_tinyman_fixed_input_swap(
                clients, sender, sk, asset_in_id=0, asset_out_id=aid, amount_in_micro=int(t.get('seed_trade_micro', 10_000))
            )
            if res.get('ok'):
                print(f"   ✅ ASA expansion: Seeded {t.get('symbol')} ({aid}) in round {res.get('round')} tx {res.get('tx_id')}")
            else:
                print(f"   ⚠️ ASA expansion failed for {t.get('symbol')} ({aid}): {res}")
    except Exception as e:
        print(f"   ⚠️ ASA expansion error: {e}")


def run_continuous(scan_interval: int = 300, health_interval: int = 600):
    print("🔄 RUN_CONTINUOUS FUNCTION STARTED")
    print("📦 Importing HybridAlgorandTradingEmpire...")

    from hybrid_algorand_trading_empire import HybridAlgorandTradingEmpire
    print("✅ Import successful")

    print("🔑 Loading credentials...")
    # Load creds and init clients
    creds = _load_env_credentials()
    if not creds.get('wallet_address') or not creds.get('wallet_mnemonic'):
        print('❌ Missing wallet credentials in .env')
        return

    print("🔗 Initializing Algorand clients...")
    clients = init_algorand_clients()
    print("✅ Algorand clients initialized")

    print("🏦 Initializing Folks Finance client...")
    folks_client = init_folks_pc297_client(
        clients['algod'], creds['wallet_address'], creds['wallet_mnemonic']
    )
    print("✅ Folks Finance client initialized")

    print("🧪 Testing PC 297 bypass...")
    pc297 = test_pc297_bypass(folks_client)
    print("✅ PC 297 bypass tested")

    print("🏗️ Instantiating Hybrid core...")
    # Instantiate Hybrid core
    hybrid = HybridAlgorandTradingEmpire()
    print("✅ Hybrid core instantiated")

    # Timers and fund manager
    last_scan = 0
    last_health = 0
    fund = FundManager()

    print('🚀 Starting Hybrid Trading Empire continuous operation...')
    try:
        while True:
            now = time.time()
            print(f"🔄 Main loop iteration at {now:.0f} (last_scan: {last_scan:.0f})")
            # Write to debug file
            with open('debug_main_loop.txt', 'a') as f:
                f.write(f"MAIN LOOP ITERATION AT: {now}\\n")

            # Health
            if now - last_health >= health_interval:
                # ALGO Safety Monitoring
                algo_status, algo_balance = log_algo_balance_status(clients['algod'], creds['wallet_address'])

                status = {
                    'timestamp': datetime.now().isoformat(),
                    'system': 'Hybrid Algorand Trading Empire',
                    'pc297_status': pc297.get('status', 'unknown'),
                    'algorand_round': clients['algod'].status().get('last-round'),
                    'nav_estimate_usd': estimate_nav_usd(clients, creds['wallet_address']),
                    'algo_balance': algo_balance,
                    'algo_status': algo_status,
                    'algo_safety_enabled': ALGO_CHECK_ENABLED
                }
                write_health(status)
                last_health = now

            # Opportunity sweep (includes DeFiLlama)
            if now - last_scan >= scan_interval:
                print(f"⏰ Scan interval triggered: now={now:.0f}, last_scan={last_scan:.0f}, diff={now-last_scan:.0f}s, interval={scan_interval}s")
                print("🔄 Starting opportunity sweep...")
                try:
                    sweep = do_defillama_sweep()
                    print(f"📊 Sweep completed - found {len(sweep.get('top', []))} top opportunities")

                    if sweep.get('top'):
                        print(f"🎯 Top opp summary: {[ (o.get('source'), o.get('opportunity_type'), o.get('opportunity_score')) for o in sweep['top'] ]}")
                        # Attempt single safe execution tied to top opp
                        print("🚀 Triggering execution attempt...")
                        attempt_execute_top_opportunity(sweep['top'], clients, creds, folks_client)
                        print("✅ Execution attempt completed")
                    else:
                        print("⚠️ No top opportunities found - skipping execution")

                except Exception as e:
                    print(f"❌ Opportunity sweep failed: {e}")
                    import traceback
                    traceback.print_exc()

                print(f"🔄 Updating last_scan from {last_scan:.0f} to {now:.0f}")
                last_scan = now
                # Exploration: try seeding new protocols/pools with tiny trades based on filters
                try:
                    explore_new_protocols(sweep['top'], clients, creds)
                except Exception as e:
                    print(f"   ⚠️ Exploration error: {e}")
                # Run strategy executors (non-blocking, small size)
                # Build market state for fund manager
                tinyman_px = _get_tinyman_mid_price(clients['algod'], 0, USDC_ID) or 0.0
                pact_px = _get_pact_mid_price(clients['algod']) or tinyman_px or 0.0
                spread = 0.0 if not pact_px else (tinyman_px - pact_px) / pact_px
                nav = estimate_nav_usd(clients, creds['wallet_address']) or 0.0
                plan = fund.decide_plan({'tinyman_px': tinyman_px, 'pact_px': pact_px, 'spread': spread, 'nav_usd': nav})
                # Persist plan history
                write_plan_history(plan, {'tinyman_px': tinyman_px, 'pact_px': pact_px, 'spread': spread, 'nav_usd': nav, 'round': clients['algod'].status().get('last-round')})
                if plan['arbitrage']['enable']:
                    try:
                        run_arbitrage_cycle(clients, creds, fund=fund, size_override_micro=plan['arbitrage']['size_micro'])
                    except Exception as e:
                        print(f"   ⚠️ Arbitrage cycle error: {e}")
                if plan['momentum']['enable']:
                    try:
                        run_momentum_cycle(clients, creds, fund=fund, size_override_micro=plan['momentum']['size_micro'])
                    except Exception as e:
                        print(f"   ⚠️ Momentum cycle error: {e}")
                try:
                    run_yield_farming_cycle(clients, creds)
                except Exception as e:
                    print(f"   ⚠️ Yield farming cycle error: {e}")
                try:
                    run_flash_loan_cycle(clients, creds)
                except Exception as e:
                    print(f"   ⚠️ Flash loan cycle error: {e}")
                try:
                    run_asa_expansion_cycle(clients, creds)
                except Exception as e:
                    print(f"   ⚠️ ASA expansion cycle error: {e}")
                # Periodic consult
                advice = fund.maybe_consult_ceo_and_agi()
                if advice:
                    print(f"   🧭 FundManager consult: {advice.get('ceo_advice')} | {advice.get('agi_directive')}")
                last_scan = now

            time.sleep(2)
    except KeyboardInterrupt:
        print('\n🛑 Stopped by user')


def main():
    print("🚀 MAIN FUNCTION STARTED")
    print("🔧 Step 1: Initializing debug logging...")

    # Write debug info to a file
    with open('debug_main_function.txt', 'w') as f:
        f.write("MAIN FUNCTION REACHED AT: " + str(time.time()) + "\\n")

    print("🔧 Step 2: Reading configuration...")
    # Read optional scan/health intervals from config if present
    scan_interval = 300
    health_interval = 600
    try:
        import yaml
        cfg_path = 'config/development.yaml'
        if os.path.exists(cfg_path):
            with open(cfg_path, 'r') as f:
                cfg = yaml.safe_load(f) or {}
            monitoring = cfg.get('monitoring', {})
            scan_interval = int(monitoring.get('opportunity_scan_interval', 60))
            health_interval = int(monitoring.get('health_check_interval', 300))
    except Exception:
        pass

    print(f"🔄 Calling run_continuous with scan_interval={scan_interval}, health_interval={health_interval}")
    print("🚀 About to enter main trading loop...")
    run_continuous(scan_interval=scan_interval, health_interval=health_interval)


if __name__ == '__main__':
    main()


