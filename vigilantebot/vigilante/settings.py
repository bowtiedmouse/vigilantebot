import guild_config


# Min token's USD amount to consider it a holding (to avoid dust left or small airdrops)
MIN_TOKEN_BALANCE = 300

# Min % that a token balance needs to change to be reported. Helps to avoid
# reporting gas consumption
MIN_PC_DIFF = 5
MIN_PORTFOLIO_PC = 0.49

# GUILD_ID = os.getenv('DISCORD_GUILD_ID')
# GUILD_NAME = os.getenv('GUILD_NAME').replace(' ', '')
GUILD_NAME = guild_config.get_guild_name()
TARGET_ACCOUNTS_FILE = f"target_accounts_{GUILD_NAME}.json"
TARGETS_HOLDINGS_FILE = f"data/targets_holdings_{GUILD_NAME}.json"
ALERTS_LOG_FILE = F"data/log_{GUILD_NAME}"
VIGILANTE_LOG_FILE = f"logs/vigilante_{GUILD_NAME}.log"

GAS_TOKENS = ['ETH', 'FTM', 'AVAX']
# optional: &chain_id=eth
DEBANK_TOKEN_LIST_URL = "https://openapi.debank.com/v1/user/token_list?id={address}&is_all=false"
DEBANK_ACCOUNT_BALANCE_URL = "https://openapi.debank.com/v1/user/total_balance?id={address}"
# EXCLUDED_CHAINS = ["root['" + chain + "']" for chain in os.getenv('EXCLUDED_CHAINS').split(',')]
EXCLUDED_CHAINS = ["root['" + chain + "']" for chain in guild_config.get_excluded_chains()]
