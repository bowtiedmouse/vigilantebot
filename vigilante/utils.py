import json
import requests

from pprint import pprint
from deepdiff import DeepDiff

import settings


# tests:
# prev_test = {'eth': {'PDT': '475.63850932673466', 'FTM': '69.84653761752556', 'CVXCRV': '242.54690279384184'},
#         'arb': {'MAGIC': '155.62757924869086', 'DPX': '0.23860662271384542', 'ETH': '0.661955993077381'}}
# current_test = {
#     'eth': {'FTM': '69.84653761752556', 'CVXCRV': '242.54690279384184',
#             'PSP': '700.0', 'CVXFXS': '225.15843445540992',
#             'ETH': '0.21453259697220345'},
#     'arb': {'MAGIC': '155.62757924869086', 'DPX': '0.32030158008708476', 'ETH': '0.7073949818623116',
#             'WETH': '2.57279034377025', 'USDC': '2618.52978'},
#     'bsc': {'USDC': '117.106'},
#     'ftm': {'MIM': '547.7211225042761', 'BRUSH': '1810.2606114419204'},
#     'avax': {'AVAX': '7.367895972757745'},
#     'op': {'ZIP': '2425.2278482690444', 'ETH': '0.11459204326855285'}}
#
# a = {"a": 1}
# b = {"a": 1, "b": 2}
# compare_last_balances_with_prev("a", current_test)


def has_min_token_balance(token: json):
    """Avoids including dust left in the wallet."""
    return token['amount'] * token['price'] >= settings.MIN_TOKEN_BALANCE


def get_account_usd_balance(account):
    """Get current account's USD value from Debank API."""
    balance = requests.get(settings.DEBANK_ACCOUNT_BALANCE_URL.format(address=account)).json()["total_usd_value"]
    return int(balance)


def request_token_list(account):
    """Request the updated data for the account to Debank API."""
    return requests.get(settings.DEBANK_TOKEN_LIST_URL.format(address=account))


def update_balances_file(user_alias: str, user_holdings: dict):
    # todo: only updates current user
    with open(settings.WALLETS_BALANCE_FILE, "w") as f:
        print("Updating file...")
        json.dump(user_holdings, f)


def get_balances_from_file(user_alias: str) -> dict:
    """Gets the last saved data for an user."""
    # todo: only get provided user
    with open(settings.WALLETS_BALANCE_FILE, "r") as f:
        return json.load(f)


def compare_last_balances_with_prev(user_alias, last_balances):
    """The core function that check for differences in balances of a wallet from a user."""
    prev_balances = get_balances_from_file(user_alias)

    # todo: remove prints
    # print("BEFORE:")
    # pprint(prev_balances['tokens_by_chain'])
    # print("AFTER:")
    # pprint(last_balances['tokens_by_chain'])
    diff = DeepDiff(prev_balances['tokens_by_chain'],
                    last_balances['tokens_by_chain'],
                    verbose_level=2,
                    exclude_paths=settings.EXCLUDED,
                    ignore_numeric_type_changes=True,
                    ignore_string_case=True
                    ).to_dict()

    updates = {
        "removed": _parse_diff_results(diff['dictionary_item_removed']) if 'dictionary_item_removed' in diff else {},
        "added": _parse_diff_results(diff['dictionary_item_added']) if 'dictionary_item_added' in diff else {},
        "changed": _parse_diff_results(diff['values_changed']) if 'values_changed' in diff else {}
    }

    print("PARSED:")
    pprint(updates)


def _parse_diff_results(diff_results):
    """Parses DeepDiff data into something more manageable.

    DeepDiff model:
    {
        'dictionary_item_added':    {"root['arb']['WETH']": '0.661955993077381'},
        'dictionary_item_removed':  {"root['eth']['PDT']": '475.63850932673466'},
        'values_changed':           {"root['arb']['DPX']":{
                                        'new_value': '10.23860662271384542',
                                        'old_value': '0.23860662271384542'},
                                    "root['eth']['FTM']": {
                                        'new_value': '68.84653761752556',
                                        'old_value': '69.84653761752556'}
                                    }
    }
    """
    last_chain_id = ""
    parsed = {}

    for chain_token, balance in diff_results.items():
        # print(f"chain: {chain_token}, amount: {balance}")

        try:
            chain_id, symbol = chain_token.replace("root['", "").replace("']", "").split("['")
            _add_parsed_result(last_chain_id, chain_id, parsed, symbol, balance)
            last_chain_id = chain_id
        except ValueError:
            # If a user adds tokens to a new chain the format returned from DeepDiff will be different
            chain_id = chain_token.replace("root['", "").replace("']", "")
            for symbol, amount in balance.items():
                _add_parsed_result(last_chain_id, chain_id, parsed, symbol, amount)
                last_chain_id = chain_id

    return parsed


def _add_parsed_result(last_chain_id, chain_id: str, parsed, symbol, amount):
    if chain_id != last_chain_id:
        parsed[chain_id] = {}
    parsed[chain_id][symbol] = amount
