import json
import requests

import settings


def has_min_token_balance(token: json):
    """
    Avoids including dust left in the wallet.
    """
    return token['amount'] * token['price'] >= settings.MIN_TOKEN_BALANCE


def get_account_usd_balance(account):
    """
    Gets current account's USD value from Debank API.
    """
    balance = requests.get(settings.DEBANK_ACCOUNT_BALANCE_URL.format(address=account)).json()["total_usd_value"]
    return int(balance)


def request_token_list(account):
    """
    Requests the updated data for the account to Debank API.
    """
    return requests.get(settings.DEBANK_TOKEN_LIST_URL.format(address=account))


def update_holdings_file(user_alias: str, user_holdings: dict):
    # todo: only updates current user
    with open(settings.WALLETS_BALANCE_FILE, "w") as f:
        print("Updating file...")
        json.dump(user_holdings, f)


def get_holdings_from_file(user_alias: str) -> dict:
    """
    Gets the last saved data for a user.
    """
    # todo: only get provided user
    with open(settings.WALLETS_BALANCE_FILE, "r") as f:
        return json.load(f)