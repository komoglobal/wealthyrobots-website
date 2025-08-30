#!/usr/bin/env python3
"""
Manual Tinyman Opt-in Helper
Helps you opt-in to Tinyman applications manually
"""

import json
from algosdk.v2client.algod import AlgodClient
from algosdk.transaction import ApplicationOptInTxn
from algosdk import mnemonic

# Your wallet details
WALLET_ADDRESS = "OL4EMRL54OZFBMHGNJZIV5RLJ7O3VTIEWPQDMIIU26JLXZ3DDB6FC3YYIM"
# You'll need to provide your mnemonic or private key
# MNEMONIC = "your 25-word mnemonic here"

def check_tinyman_apps():
    """Check available Tinyman applications"""
    algod_token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    algod_address = 'https://mainnet-api.algonode.cloud'

    algod_client = AlgodClient(algod_token, algod_address)

    # Known Tinyman apps (check which ones exist)
    potential_apps = [1002541853, 552635992, 552635991, 553099957, 611592103]

    print("🔍 Checking Tinyman applications...")
    working_apps = []

    for app_id in potential_apps:
        try:
            app_info = algod_client.application_info(app_id)
            print(f"✅ App {app_id}: EXISTS")

            # Check if wallet is already opted in
            account_info = algod_client.account_info(WALLET_ADDRESS)
            opted_in_apps = [app.get('id') for app in account_info.get('apps-local-state', [])]

            if app_id in opted_in_apps:
                print(f"   ✅ Already opted in to app {app_id}")
            else:
                print(f"   ❌ Not opted in to app {app_id}")
                working_apps.append(app_id)

        except Exception as e:
            print(f"❌ App {app_id}: {str(e)[:50]}...")

    return working_apps

def manual_optin(app_id):
    """Attempt manual opt-in to a specific app"""
    print(f"\n🔧 Attempting manual opt-in to app {app_id}")

    algod_token = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    algod_address = 'https://mainnet-api.algonode.cloud'

    algod_client = AlgodClient(algod_token, algod_address)

    # You'll need to uncomment and provide your mnemonic
    # private_key = mnemonic.to_private_key(MNEMONIC)

    print("📝 To complete opt-in:")
    print(f"1. Go to https://explorer.perawallet.app/application/{app_id}")
    print("2. Click 'Opt-in' or 'Opt In to App'")
    print("3. Sign the transaction with your wallet")
    print("4. Wait for confirmation")
    print()
    print("Alternative methods:")
    print("- Use Pera Wallet mobile app")
    print("- Use MyAlgo Wallet")
    print("- Use any Algorand-compatible wallet")

if __name__ == "__main__":
    print("🤖 Manual Tinyman Opt-in Helper")
    print("=" * 50)

    working_apps = check_tinyman_apps()

    if working_apps:
        print(f"\n🎯 Found {len(working_apps)} apps you can opt-in to:")
        for app_id in working_apps:
            manual_optin(app_id)
    else:
        print("\n❌ No working Tinyman apps found or all already opted in to")
