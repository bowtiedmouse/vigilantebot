from deepdiff import DeepDiff

import settings
import holdings


def compare_target_last_holdings_with_prev(user_alias, last_holdings):
    prev_holdings = holdings.get_holdings_from_file(user_alias)
    return compare_holdings(prev_holdings, last_holdings)


def compare_holdings(prev, last):
    """
    The core function that check for differences in balances of a wallet from a user.
    """
    diff = DeepDiff(prev['tokens_by_chain'],
                    last['tokens_by_chain'],
                    verbose_level=2,
                    exclude_paths=settings.EXCLUDED,
                    ignore_numeric_type_changes=True,
                    ignore_string_case=True
                    ).to_dict()

    return {
        "removed": _parse_diff_results(diff['dictionary_item_removed']) if 'dictionary_item_removed' in diff else {},
        "added": _parse_diff_results(diff['dictionary_item_added']) if 'dictionary_item_added' in diff else {},
        "changed": _parse_diff_results(diff['values_changed']) if 'values_changed' in diff else {}
    }


def _parse_diff_results(diff_results):
    """
    Parses DeepDiff data into something more manageable.

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
        try:
            # DeepDiff has a extract() function, but it only returns value, and we also need key
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
