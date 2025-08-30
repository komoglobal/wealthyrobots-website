#!/usr/bin/env python3
import os
import yaml

from run_hybrid_trading_empire import (
    init_algorand_clients,
    _load_env_credentials,
    try_tinyman_swap_with_retry,
    USDC_ID,
)


def load_trade_size(default_micro: int = 1000) -> int:
    try:
        with open('config/fund_manager.overrides.yaml', 'r') as f:
            ov = yaml.safe_load(f) or {}
        size = int(ov.get('base_trade_micro', default_micro))
        return size
    except Exception:
        return default_micro


def main():
    clients = init_algorand_clients()
    creds = _load_env_credentials()
    if not creds.get('wallet_address') or not creds.get('wallet_mnemonic'):
        print('❌ Missing wallet credentials')
        return

    from algosdk import mnemonic as _mn, account as _acct
    sk = _mn.to_private_key(creds['wallet_mnemonic'])
    sender = _acct.address_from_private_key(sk)

    size = load_trade_size(1000)
    print(f"🔫 Triggering live Tinyman swap: {size} micro ALGO → USDC")
    res = try_tinyman_swap_with_retry(clients, sender, sk, asset_in_id=0, asset_out_id=USDC_ID)
    if res.get('ok'):
        print(f"✅ Swap confirmed in round {res.get('round')} (tx {res.get('tx_id')})")
    else:
        print(f"⚠️ Swap failed: {res}")


if __name__ == '__main__':
    main()


