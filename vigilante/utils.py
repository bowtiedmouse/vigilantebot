import json
import requests
import settings


def _has_min_token_balance(token: json):
    return token['amount'] * token['price'] >= settings.MIN_TOKEN_BALANCE


def _get_account_usd_balance(account):
    balance = requests.get(settings.DEBANK_ACCOUNT_BALANCE_URL.format(address=account)).json()["total_usd_value"]
    return int(balance)


def request_token_list(account):
    # print("Requesting data from Debank...")
    return requests.get(settings.DEBANK_TOKEN_LIST_URL.format(address=account))


def update_balances_file(user_alias: str, user_holdings: dict):
    with open(settings.WALLETS_BALANCE_FILE, "w") as f:
        print("Updating file...")
        json.dump(user_holdings, f)


def get_balances_from_file(user_alias: str) -> dict:
    with open(settings.WALLETS_BALANCE_FILE, "r") as f:
        return json.load(f)


def compare_last_balances_with_prev(user_alias, current_holdings):
    prev = get_balances_from_file(user_alias)

