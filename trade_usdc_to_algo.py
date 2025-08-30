#!/usr/bin/env python3
"""
Trade USDC to ALGO to replenish wallet balance
"""

import os
import sys
from typing import Dict
from algosdk import mnemonic, account
from algosdk.v2client import algod
from sdk_imports import get_tinyman_client, get_tinyman_function, is_sdk_available

def _load_env_credentials(env_path: str = '.env') -> Dict[str, str]:
    """Load credentials from .env file (same as trading engine)"""
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

def main():
    print('🔄 TRADING USDC -> ALGO TO REPLENISH BALANCE')
    print('=' * 50)

    # Load credentials from .env file
    creds = _load_env_credentials()
    wallet_address = creds.get('wallet_address', '')
    wallet_mnemonic = creds.get('wallet_mnemonic', '')

    if not wallet_address or not wallet_mnemonic:
        print('❌ Wallet credentials not found in .env file')
        return

    print(f'📱 Wallet: {wallet_address[:20]}...')

    # Initialize Algod client using hardcoded values (same as trading engine)
    algod_client = algod.AlgodClient(
        algod_token="",
        algod_address="https://mainnet-api.algonode.cloud"
    )

    # Decode mnemonic and get private key
    sk = mnemonic.to_private_key(wallet_mnemonic)
    sender = account.address_from_private_key(sk)

    # Check current balance
    account_info = algod_client.account_info(wallet_address)
    algo_balance = float(account_info.get('amount', 0)) / 1e6
    usdc_balance = 0

    for asset in account_info.get('assets', []):
        if asset.get('asset-id') == 31566704:  # USDC
            usdc_balance = asset.get('amount', 0) / 1e6
            break

    print(f'📊 Current balances:')
    print(f'   • ALGO: {algo_balance:.6f}')
    print(f'   • USDC: {usdc_balance:.6f}')
    print(f'   • Target: {algo_balance + 100:.6f} ALGO (after trade)')

    # Check if Tinyman SDK is available
    if not is_sdk_available('tinyman'):
        print('❌ Tinyman SDK not available for trading')
        return

    print()
    print('🔍 Getting pool information...')

    # Get Tinyman client and functions
    client = get_tinyman_client(algod_client)
    get_pool_info = get_tinyman_function('get_pool_info')
    prepare_swap_transactions = get_tinyman_function('prepare_swap_transactions')
    calculate_fixed_input_swap = get_tinyman_function('calculate_fixed_input_swap')

    if not all([get_pool_info, prepare_swap_transactions, calculate_fixed_input_swap]):
        print('❌ Required Tinyman functions not available')
        return

    # Get ALGO/USDC pool info
    validator_app_id = client.validator_app_id
    pool = get_pool_info(algod_client, validator_app_id, 0, 31566704)  # ALGO = 0, USDC = 31566704

    if not pool:
        print('❌ Could not get pool information')
        return

    algo_reserve = pool.get('asset_1_reserves', 0)
    usdc_reserve = pool.get('asset_2_reserves', 0)

    print(f'📊 Pool reserves:')
    print(f'   • ALGO reserve: {algo_reserve / 1e6:,.0f} ALGO')
    print(f'   • USDC reserve: {usdc_reserve / 1e6:,.0f} USDC')

    # Calculate price
    if usdc_reserve > 0 and algo_reserve > 0:
        algo_per_usdc = algo_reserve / usdc_reserve
        usdc_per_algo = usdc_reserve / algo_reserve
        print(f'💱 Exchange rates:')
        print(f'   • 1 USDC = {algo_per_usdc:.6f} ALGO')
        print(f'   • 1 ALGO = {usdc_per_algo:.6f} USDC')

    # Calculate amount needed (target 100 ALGO gain)
    target_algo_gain = 100.0
    usdc_to_trade = target_algo_gain / algo_per_usdc
    usdc_to_trade_micro = int(usdc_to_trade * 1e6)

    print(f'🎯 Trade calculation:')
    print(f'   • Target ALGO gain: {target_algo_gain:.6f} ALGO')
    print(f'   • USDC needed: {usdc_to_trade:.6f} USDC')
    print(f'   • USDC available: {usdc_balance:.6f} USDC')

    if usdc_to_trade > usdc_balance:
        print(f'❌ Not enough USDC! Need {usdc_to_trade:.6f}, have {usdc_balance:.6f}')
        return

    # Estimate expected output (rough calculation)
    expected_algo_out = target_algo_gain
    swap_fees = 0.1  # Rough estimate of swap fees
    print(f'📈 Swap preview:')
    print(f'   • Expected ALGO out: ~{expected_algo_out:.6f}')
    print(f'   • Estimated fees: ~{swap_fees:.6f} ALGO')
    print(f'   • Final ALGO gain: ~{expected_algo_out - swap_fees:.6f}')

    # Confirm trade
    print()
    response = input('🚀 Execute USDC -> ALGO swap? (yes/no): ')
    if response.lower() not in ['yes', 'y']:
        print('❌ Trade cancelled')
        return

    print()
    print('🚀 EXECUTING USDC -> ALGO SWAP...')
    print('=' * 40)

    # Prepare swap transaction
    params = algod_client.suggested_params()

    # Calculate minimum ALGO output (with some slippage tolerance)
    min_algo_out_micro = int(target_algo_gain * 0.95 * 1e6)  # 5% slippage tolerance

    group = prepare_swap_transactions(
        validator_app_id=validator_app_id,
        asset_1_id=0,  # ALGO
        asset_2_id=31566704,  # USDC
        asset_in_id=31566704,  # Trading USDC in
        asset_in_amount=usdc_to_trade_micro,
        asset_out_amount=min_algo_out_micro,
        swap_type='fixed-input',
        sender=sender,
        suggested_params=params
    )

    # Sign and submit
    group.sign_with_private_key(sender, sk)
    try:
        result = group.submit(algod_client, wait=True)
        print(f'✅ SWAP SUCCESSFUL!')
        print(f'   • Transaction: {result.get("txid", "Unknown")}')
        print(f'   • Block: {result.get("confirmed-round", "Unknown")}')
        print(f'   • Expected ALGO received: {expected_algo_out:.6f}')
    except Exception as e:
        print(f'❌ Swap failed: {e}')
        return

    # Check final balance
    print()
    print('🔍 Checking final balance...')
    final_account_info = algod_client.account_info(wallet_address)
    final_algo_balance = float(final_account_info.get('amount', 0)) / 1e6

    print(f'💰 Final ALGO balance: {final_algo_balance:.6f}')
    print(f'   • ALGO gained: {final_algo_balance - algo_balance:.6f}')
    print(f'   • Safety net status: {"✅ SAFE" if final_algo_balance >= 10.0 else "🚨 STILL LOW"}')

    if final_algo_balance >= 10.0:
        print('🎉 SUCCESS! Wallet ALGO balance is now above safety net!')
    else:
        print('⚠️ WARNING: Wallet still below safety net')

if __name__ == "__main__":
    main()
