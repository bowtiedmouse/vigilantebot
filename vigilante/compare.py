from deepdiff import DeepDiff
import settings
import holdings


def get_target_holdings_changes(target_alias, updated_holdings) -> dict:
    """
    Gets a DeepDiff dictionary with the differences in holdings between saved data and
    requested data.

    :param target_alias: target alias
    :param updated_holdings: last requested data
    :return: DeepDiff dict
    """
    prev_holdings = holdings.get_holdings_from_file(target_alias)
    return _compare_holdings(prev_holdings, updated_holdings)


def _compare_holdings(prev, last):
    """
    Checks for differences in balances of the holdings of a wallet from a user.
    """
    return DeepDiff(prev,
                    last,
                    verbose_level=2,
                    exclude_paths=settings.EXCLUDED,
                    ignore_numeric_type_changes=True,
                    ignore_string_case=True
                    ).to_dict()
