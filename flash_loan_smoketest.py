#!/usr/bin/env python3
import os
from run_hybrid_trading_empire import (
    _load_env_credentials,
    init_algorand_clients,
    run_flash_loan_cycle,
)


def main():
    creds = _load_env_credentials()
    if not creds.get('wallet_address') or not creds.get('wallet_mnemonic'):
        print('❌ Missing wallet credentials in .env')
        return
    clients = init_algorand_clients()
    print('🔬 Running flash-loan smoke test...')
    run_flash_loan_cycle(clients, creds)
    print('✅ Smoke test finished')


if __name__ == '__main__':
    main()


