__all__ = ['MIN_TOKEN_BALANCE', 'DEBANK_ACCOUNT_BALANCE_URL', 'DEBANK_ACCOUNT_BALANCE_URL', 'WALLETS_BALANCE_FILE']

MIN_TOKEN_BALANCE = 100
WALLETS_BALANCE_FILE = "wallets_balances.json"
DEBANK_TOKEN_LIST_URL = "https://openapi.debank.com/v1/user/token_list?id={address}&is_all=false"  # optional: &chain_id=eth
DEBANK_ACCOUNT_BALANCE_URL = "https://openapi.debank.com/v1/user/total_balance?id={address}"
