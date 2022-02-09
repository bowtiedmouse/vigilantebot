import pytest

from vigilante import holdings


def test_compare_holdings_diff(saved_holdings_data, updated_holdings_data, diff_dict):
    diff = holdings._compare_holdings(saved_holdings_data, updated_holdings_data)
    assert diff == diff_dict


def test_process_target_token_list(updated_holdings_data, requested_data):
    data = holdings._process_token_list({}, requested_data)
    assert data == {'arb': {'ETH': {'amount': 1.387234568968202,
                                    'contract_address': 'arb',
                                    'symbol': 'ETH',
                                    'usd_price': 2840.69}}}


@pytest.mark.parametrize('new_value, old_value, expected', [
    (190, 100, True),
    (1.0, 1.001, False)
])
def test_new_value_is_min_diff_than_old_value(new_value, old_value, expected):
    assert holdings.has_changed_by_min_pc(new_value, old_value) == expected
