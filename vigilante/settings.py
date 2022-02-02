WATCH_FREQUENCY = 60 * 15

MIN_TOKEN_BALANCE = 100
TARGET_ACCOUNTS_FILE = "target_accounts.json"
TARGETS_HOLDINGS_FILE = "targets_holdings.json"

# optional: &chain_id=eth
DEBANK_TOKEN_LIST_URL = "https://openapi.debank.com/v1/user/token_list?id={address}&is_all=false"
DEBANK_ACCOUNT_BALANCE_URL = "https://openapi.debank.com/v1/user/total_balance?id={address}"
EXCLUDED = ["root['bsc']"]
