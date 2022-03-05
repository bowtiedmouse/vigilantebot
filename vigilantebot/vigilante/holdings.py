#
#   Functions to interact with the holdings saved data and compare it with updated
#   data from the blockchain
#

# todo: replace requests for aiohttp
# async with aiohttp.ClientSession() as session:
#     async with session.get('http://aws.random.cat/meow') as r:
#         if r.status == 200:
#             js = await r.json()
#             await channel.send(js['file'])

from os.path import isfile
import json
import logging

import requests
from deepdiff import DeepDiff

from vigilante import settings
from vigilante import fileutils

logger = logging.getLogger(__name__)


def has_min_token_balance(token: json) -> bool:
    """
    Avoids including dust left in the wallet.
    """
    try:
        return token['amount'] * token['price'] >= settings.MIN_TOKEN_BALANCE
    except TypeError as e:
        print('Error: ', token)
        logger.error(f"{e} attempting access to {token} by string indices.")
        return False


def has_changed_by_min_pc(new_value: float, old_value: float) -> bool:
    return abs(100 * (new_value - old_value) / old_value) >= settings.MIN_PC_DIFF


def get_token_pc_of_portfolio(token_data: dict, target) -> float:
    if token_data.keys() >= {'amount', 'usd_price'}:
        # total_portfolio = get_target_usd_balance(target)
        token_investment = token_data['amount'] * token_data['usd_price']
        return round(100 * token_investment / target.usd_balance, 1)
    else:
        raise ValueError("Couldn't calculate portfolio % of token.")


def get_target_usd_balance(target) -> int:
    """
    Gets the total USD balance of all the accounts of a target.

    :return: int
    """
    return sum(
        get_account_usd_balance(account) for account in target.addresses
    )


def get_account_usd_balance(account: str) -> int:
    """
    Gets current account's USD value from Debank API.
    """
    try:
        balance = requests.get(
            settings.DEBANK_ACCOUNT_BALANCE_URL.format(address=account)
        ).json()['total_usd_value']
    except Exception:
        return 0
    return int(round(balance, 0))


def holdings_file_exists() -> bool:
    return isfile(settings.TARGETS_HOLDINGS_FILE)


def create_holdings_file() -> None:
    fileutils.create_empty_json_file(settings.TARGETS_HOLDINGS_FILE)
    print(f'Created file: {settings.TARGETS_HOLDINGS_FILE}')


def is_target_in_file(target_alias: str) -> bool:
    return {} != fileutils.get_file_key_content(settings.TARGETS_HOLDINGS_FILE,
                                                target_alias)


def get_token_holdings(target_account: str, target_holdings: dict) -> dict:
    try:
        token_list = _request_token_list(target_account).json()
        return _process_token_list(target_holdings, token_list)
    except Exception as e:
        logger.error(f'Exception reading the JSON from DeBank: {e}')
        return {}



def get_holdings_from_file(target_alias: str) -> dict:
    """
    Gets the last saved data for a user.
    """
    return fileutils.get_file_key_content(settings.TARGETS_HOLDINGS_FILE, target_alias,
                                          'wallet_holdings')


def update_holdings_file(target_alias: str, target_holdings: dict,
                         usd_balance: int = 0):
    """
    Updates the json file with target data.
    """
    if usd_balance:
        fileutils.update_file_key(settings.TARGETS_HOLDINGS_FILE, target_alias,
                                  usd_balance, 'usd_balance')
    fileutils.update_file_key(settings.TARGETS_HOLDINGS_FILE, target_alias,
                              target_holdings, 'wallet_holdings')


def get_target_holdings_diff(target_alias: str, updated_holdings: dict) -> dict:
    """
    Gets a DeepDiff dictionary with the differences in holdings between saved data and
    requested data.

    :param target_alias: target alias
    :param updated_holdings: last requested data
    :return: DeepDiff dict
    """
    prev_holdings = get_holdings_from_file(target_alias)
    return _compare_holdings(prev_holdings, updated_holdings)


def _compare_holdings(prev: dict, last: dict) -> DeepDiff:
    """
    Checks for differences in balances of the holdings of a wallet from a user.
    """
    return DeepDiff(prev,
                    last,
                    verbose_level=2,
                    exclude_paths=settings.EXCLUDED_CHAINS,
                    ignore_numeric_type_changes=True,
                    ignore_string_case=True,
                    math_epsilon=0.001,
                    exclude_regex_paths=r"\['usd_price'\]"
                    ).to_dict()


def _request_token_list(account) -> requests.Response:
    """
    Requests the updated data for the account to Debank API.
    """
    return requests.get(settings.DEBANK_TOKEN_LIST_URL.format(address=account))


def _process_token_list(target_holdings_by_chain: dict, token_list: dict) -> dict:
    """
    Simplifies request's returned object by getting only needed data and
    adding up token balances from several user's accounts.
    """
    for token in token_list:
        if not has_min_token_balance(token):
            continue

        chain_id = token['chain'].lower()
        token_address = token['id']
        symbol = token['symbol'].upper()
        amount = token['amount']
        token_price = token['price']

        if chain_id not in target_holdings_by_chain:
            target_holdings_by_chain[chain_id] = {}

        if symbol in target_holdings_by_chain[chain_id]:
            amount += float(target_holdings_by_chain[chain_id][symbol]['amount'])

        target_holdings_by_chain[chain_id][symbol] = {
            'contract_address': token_address,
            'symbol': symbol,
            'amount': amount,
            'usd_price': token_price
        }

    return target_holdings_by_chain
