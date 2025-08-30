#!/usr/bin/env python3
"""
Safe Real Self Transfer
Sends a tiny amount (0.001 ALGO) from the configured wallet to itself on Algorand mainnet.
This is a safe on-chain test that verifies signing and submission work without moving funds externally.
"""

import os
import json
from datetime import datetime


def _load_env_credentials(env_path: str = '.env'):
    wallet_address = None
    mnemonic_phrase = None

    if not os.path.exists(env_path):
        raise FileNotFoundError(f".env not found at {env_path}")

    with open(env_path, 'r') as f:
        lines = f.read().splitlines()

    # Parse ALGORAND_WALLET_ADDRESS and handle multi-line ALGORAND_WALLET_MNEMONIC
    collecting_mnemonic = False
    mnemonic_parts = []
    for line in lines:
        # Stop mnemonic collection on blank separator
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
            # Continue collecting until blank line
            mnemonic_parts.append(line.strip())

    if mnemonic_parts:
        mnemonic_phrase = ' '.join(' '.join(mnemonic_parts).split())

    if not wallet_address or not mnemonic_phrase:
        raise ValueError('Wallet credentials not found or incomplete in .env')

    return wallet_address, mnemonic_phrase


def main() -> bool:
    print('🚀 SAFE REAL SELF TRANSFER')
    print('=' * 60)
    print('🎯 Sends 0.001 ALGO from your wallet to itself (safe on-chain test)')

    try:
        wallet_address, mnemonic_phrase = _load_env_credentials()
        print(f"✅ Wallet loaded: {wallet_address[:10]}...{wallet_address[-10:]}")

        # Import Algorand SDK lazily
        from algosdk import mnemonic, account, v2client, transaction

        # Convert mnemonic to private key
        print('🔑 Converting mnemonic to private key...')
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        print(f'✅ Private key generated: {len(private_key)} bytes')

        # Verify derived address
        derived_address = account.address_from_private_key(private_key)
        if derived_address != wallet_address:
            print(f'❌ Address mismatch: {derived_address} vs {wallet_address}')
            return False
        print('✅ Address verified')

        # Connect to Algorand mainnet (Algonode)
        print('🔗 Connecting to Algorand mainnet...')
        algod_client = v2client.algod.AlgodClient(
            algod_token=os.getenv('ALGOD_TOKEN', ''),
            algod_address=os.getenv('ALGOD_ADDRESS', 'https://mainnet-api.algonode.cloud')
        )

        # Network status
        status = algod_client.status()
        print(f"✅ Connected to mainnet: Block {status.get('last-round')}")

        # Balance check
        account_info = algod_client.account_info(wallet_address)
        algo_balance = account_info['amount'] / 1_000_000
        print(f"💰 Current balance: {algo_balance:.6f} ALGO")
        if algo_balance < 0.01:
            print('❌ Insufficient balance (need at least 0.01 ALGO for fee and safety)')
            return False

        # Suggested params
        params = algod_client.suggested_params()
        print('✅ Got transaction parameters')

        # Prepare self-payment of 0.001 ALGO
        amount_microalgos = 1_000  # 0.001 ALGO
        txn = transaction.PaymentTxn(
            sender=wallet_address,
            sp=params,
            receiver=wallet_address,
            amt=amount_microalgos
        )
        print('✅ Transaction created (self-transfer 0.001 ALGO)')

        # Sign and send
        print('🔐 Signing transaction...')
        signed_txn = txn.sign(private_key)
        print('📤 Submitting transaction...')
        tx_id = algod_client.send_transaction(signed_txn)
        print(f'✅ Transaction submitted: {tx_id}')

        # Wait for confirmation using round-based polling with retries
        import time
        timeout_rounds = 20
        try:
            status = algod_client.status()
            current_round = int(status.get('last-round', 0)) + 1
            end_round = current_round + timeout_rounds

            info = {}
            while current_round <= end_round:
                try:
                    info = algod_client.pending_transaction_info(tx_id)
                    if info.get('confirmed-round'):
                        print(f"✅ Confirmed in round {info['confirmed-round']}")
                        break
                except Exception as poll_err:
                    # Transient pool lookup error; wait and continue
                    time.sleep(1)

                # Wait for next round
                try:
                    algod_client.status_after_block(current_round)
                except Exception:
                    time.sleep(1)
                current_round += 1

            if not info.get('confirmed-round'):
                raise RuntimeError('Transaction not confirmed within timeout')
        except Exception as e_wait:
            print(f'❌ Confirmation wait error: {e_wait}')
            return False

        # Save details
        details = {
            'timestamp': datetime.now().isoformat(),
            'transaction_id': tx_id,
            'confirmed_round': info.get('confirmed-round'),
            'sender': wallet_address,
            'receiver': wallet_address,
            'amount': '0.001 ALGO',
            'type': 'real_self_transfer',
            'status': 'confirmed'
        }
        with open('real_self_transfer.json', 'w') as f:
            json.dump(details, f, indent=2)
        print('📄 Details saved to real_self_transfer.json')

        return True

    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    if success:
        print('\n🎯 SUCCESS: Real self-transfer executed!')
    else:
        print('\n❌ FAILED: Could not execute real self-transfer')


