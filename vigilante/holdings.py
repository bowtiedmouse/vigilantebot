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
    balance = requests.get(
        settings.DEBANK_ACCOUNT_BALANCE_URL.format(address=account)
    ).json()["total_usd_value"]

    return int(balance)


def get_token_holdings(target_account: str) -> dict:
    token_list = _request_token_list(target_account).json()
    return _process_token_list(token_list)


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


def _request_token_list(account) -> requests.Response:
    """
    Requests the updated data for the account to Debank API.
    """
    return requests.get(settings.DEBANK_TOKEN_LIST_URL.format(address=account))


def _process_token_list(tokens: dict) -> dict:
    """
    Simplifies request's returned object by getting only needed data and
    adding up token balances from several user's accounts.
    """
    tokens_by_chain = {}
    for token in tokens:
        if not has_min_token_balance(token):
            continue

        chain_id = token["chain"].lower()
        symbol = token["symbol"].upper()
        amount = token["amount"]

        if chain_id not in tokens_by_chain:
            tokens_by_chain[chain_id] = {}

        if symbol in tokens_by_chain[chain_id]:
            amount += float(tokens_by_chain[chain_id][symbol])
        tokens_by_chain[chain_id][symbol] = str(amount)

    return tokens_by_chain
