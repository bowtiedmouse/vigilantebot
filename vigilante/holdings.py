import json
import requests

import settings
import fileutils


def has_min_token_balance(token: json):
    """
    Avoids including dust left in the wallet.
    """
    return token['amount'] * token['price'] >= settings.MIN_TOKEN_BALANCE


def get_account_usd_balance(account) -> int:
    """
    Gets current account's USD value from Debank API.
    """
    balance = requests.get(
        settings.DEBANK_ACCOUNT_BALANCE_URL.format(address=account)
    ).json()["total_usd_value"]

    return int(round(balance, 0))


def get_token_holdings(target_account: str, target_holdings) -> dict:
    token_list = _request_token_list(target_account).json()
    return _process_token_list(target_holdings, token_list)


def get_holdings_from_file(target_alias: str) -> dict:
    """
    Gets the last saved data for a user.
    """
    return fileutils.get_file_key_content(settings.TARGETS_HOLDINGS_FILE, target_alias)


def update_holdings_file(target_alias: str, target_holdings: dict,
                         usd_balance: int = 0):
    """
    Updates the json file with target data.
    """
    if usd_balance:
        fileutils.update_file_key(settings.TARGETS_HOLDINGS_FILE, target_alias,
                                  'usd_balance', usd_balance)
    fileutils.update_file_key(settings.TARGETS_HOLDINGS_FILE, target_alias,
                              'tokens_by_chain', target_holdings)


def _request_token_list(account) -> requests.Response:
    """
    Requests the updated data for the account to Debank API.
    """
    return requests.get(settings.DEBANK_TOKEN_LIST_URL.format(address=account))


def _process_token_list(target_holdings_by_chain: dict, tokens: dict) -> dict:
    """
    Simplifies request's returned object by getting only needed data and
    adding up token balances from several user's accounts.
    """
    for token in tokens:
        if not has_min_token_balance(token):
            continue

        chain_id = token["chain"].lower()
        symbol = token["symbol"].upper()
        amount = token["amount"]

        if chain_id not in target_holdings_by_chain:
            target_holdings_by_chain[chain_id] = {}

        if symbol in target_holdings_by_chain[chain_id]:
            amount += float(target_holdings_by_chain[chain_id][symbol])
        target_holdings_by_chain[chain_id][symbol] = str(amount)

    return target_holdings_by_chain
