WATCH_FREQUENCY = 60 * 15

# Min token's USD amount to consider it a holding (to avoid dust left or small airdrops)
MIN_TOKEN_BALANCE = 300

# Min % that a token balance needs to change to be reported. Helps to avoid
# reporting gas consumption
MIN_PC_DIFF = 5

MIN_PORTFOLIO_PC = 0.49

TARGET_ACCOUNTS_FILE = "target_accounts.json"
TARGETS_HOLDINGS_FILE = "targets_holdings.json"

GAS_TOKENS = ['ETH', 'FTM', 'AVAX']
# optional: &chain_id=eth
DEBANK_TOKEN_LIST_URL = "https://openapi.debank.com/v1/user/token_list?id={address}&is_all=false"
DEBANK_ACCOUNT_BALANCE_URL = "https://openapi.debank.com/v1/user/total_balance?id={address}"
EXCLUDED = ["root['bsc']"]
