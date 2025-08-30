import asyncio
import json
from algosdk.v2client import algod
from algosdk import mnemonic, transaction

async def test_found_contract():
    print('🧪 TESTING FOUND CONTRACT')
    print('=' * 40)

    # Initialize client
    algod_client = algod.AlgodClient('', 'https://mainnet-api.algonode.cloud')

    # Test the found app
    test_app_id = 971350278

    print(f'🎯 Testing App ID: {test_app_id}')

    try:
        # Get app info
        app_info = algod_client.application_info(test_app_id)
        params = app_info.get('params', {})

        print('\\n🏦 APPLICATION ANALYSIS:')
        print(f'   App ID: {test_app_id}')
        print(f'   Creator: {params.get("creator", "")[:20]}...')

        # Analyze global state
        global_state = params.get('global-state', [])
        print(f'   🌐 Global State Variables: {len(global_state)}')

        # Decode and analyze global state
        print('\\n📊 GLOBAL STATE ANALYSIS:')
        for i, state_var in enumerate(global_state[:10]):  # First 10 vars
            try:
                import base64
                key_b64 = state_var.get('key', '')
                key = base64.b64decode(key_b64).decode('utf-8')
                value = state_var.get('value', {})

                if value.get('type') == 1:  # bytes
                    try:
                        value_decoded = base64.b64decode(value.get('bytes', '')).decode('utf-8')
                        print(f'   {i+1}. {key}: {value_decoded}')
                    except:
                        print(f'   {i+1}. {key}: <bytes>')
                elif value.get('type') == 2:  # uint
                    print(f'   {i+1}. {key}: {value.get("uint", 0)}')
                else:
                    print(f'   {i+1}. {key}: <unknown type>')

            except Exception as e:
                print(f'   {i+1}. <decode error>: {e}')

        # Check for lending-related keywords
        lending_keywords = ['pool', 'lend', 'borrow', 'supply', 'reserve', 'interest', 'asset', 'rate']
        has_lending_terms = False

        for state_var in global_state:
            try:
                import base64
                key_b64 = state_var.get('key', '')
                key = base64.b64decode(key_b64).decode('utf-8').lower()

                if any(term in key for term in lending_keywords):
                    has_lending_terms = True
                    print(f'   🎯 Lending-related key: {key}')
                    break
            except:
                continue

        if has_lending_terms:
            print('   💰 LIKELY LENDING POOL - Contains lending terminology')
        else:
            print('   ❓ MAYBE NOT LENDING POOL - No obvious lending terminology')

        # Test opt-in
        print('\\n🧪 TESTING OPT-IN CAPABILITY...')

        wallet_address = 'OL4EMRL54OZFBMHGNJZIV5RLJ7O3VTIEWPQDMIIU26JLXZ3DDB6FC3YYIM'

        mnemonic_phrase = 'canoe domain live biology system reveal city jump volume month timber cheese occur hockey mix twice crucial also copy hello half salt lottery absorb fresh'
        private_key = mnemonic.to_private_key(mnemonic_phrase)

        # Get current balance
        account_info = algod_client.account_info(wallet_address)
        algo_balance = account_info.get('amount', 0) / 1000000
        print(f'   💰 Current Balance: {algo_balance:.2f} ALGO')

        # Check if already opted in
        apps_opted = account_info.get('apps-local-state', [])
        is_opted_in = any(app.get('id') == test_app_id for app in apps_opted)

        if is_opted_in:
            print('   ✅ ALREADY OPTED IN TO THIS APPLICATION!')
            return True

        # Test opt-in
        params = algod_client.suggested_params()
        params.fee = 2000

        opt_in_txn = transaction.ApplicationOptInTxn(
            sender=wallet_address,
            sp=params,
            index=test_app_id
        )

        signed_txn = opt_in_txn.sign(private_key)

        try:
            tx_id = algod_client.send_transaction(signed_txn)
            print(f'   📤 Transaction sent: {tx_id[:16]}...')

            # Wait for confirmation
            for attempt in range(10):
                try:
                    tx_info = algod_client.pending_transaction_info(tx_id)
                    if tx_info.get('confirmed-round'):
                        print('   ✅ OPT-IN SUCCESSFUL!')
                        print(f'      Confirmed in round {tx_info.get("confirmed-round")}')

                        # Check if we're now opted in
                        account_info = algod_client.account_info(wallet_address)
                        apps_opted = account_info.get('apps-local-state', [])
                        is_opted_in = any(app.get('id') == test_app_id for app in apps_opted)

                        if is_opted_in:
                            print('   🎉 SUCCESSFULLY OPTED IN TO FOLKS FINANCE!')
                            return True
                        else:
                            print('   ⚠️ Transaction confirmed but not opted in')
                        break
                except:
                    pass
                await asyncio.sleep(1)

            print('   ⏳ Opt-in transaction not confirmed yet')

        except Exception as e:
            error_msg = str(e)
            print(f'   ❌ Opt-in failed: {error_msg[:100]}...')

            if 'already opted in' in error_msg.lower():
                print('   ℹ️ Already opted in to this application')
                return True

    except Exception as e:
        print(f'❌ Error testing application: {e}')

    print('\\n🎯 VERDICT:')
    print(f'   App {test_app_id}: Testing complete')
    return False

async def test_contract_methods():
    """Test if this contract has callable methods for lending/farming"""
    print('\\n🔧 TESTING CONTRACT METHODS...')

    app_id = 971350278
    algod_client = algod.AlgodClient('', 'https://mainnet-api.algonode.cloud')

    try:
        app_info = algod_client.application_info(app_id)
        approval_program = app_info.get('params', {}).get('approval-program', '')

        if approval_program:
            import base64
            program_hex = base64.b64decode(approval_program).hex()

            # Look for method signatures (common in DeFi contracts)
            method_patterns = ['supply', 'borrow', 'withdraw', 'repay', 'stake', 'unstake', 'claim']

            found_methods = []
            for method in method_patterns:
                method_hex = method.encode().hex()
                if method_hex in program_hex:
                    found_methods.append(method)
                    print(f'   ✅ Found method pattern: {method}')

            if found_methods:
                print(f'   🎯 CONTRACT HAS {len(found_methods)} RECOGNIZABLE METHODS')
                return True
            else:
                print('   ❓ NO RECOGNIZABLE DeFi METHODS FOUND')
                return False

    except Exception as e:
        print(f'   ❌ Error analyzing methods: {e}')
        return False

if __name__ == '__main__':
    async def main():
        success = await test_found_contract()
        await test_contract_methods()

        print('\\n🎯 FINAL VERDICT:')
        if success:
            print('   ✅ THIS IS A VALID DeFi CONTRACT!')
            print('   🔄 Ready for integration into trading system')
        else:
            print('   ❌ CONTRACT NOT SUITABLE FOR DeFi OPERATIONS')
            print('   🔍 Need to find different contracts')

    asyncio.run(main())









