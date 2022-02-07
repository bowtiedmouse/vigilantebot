import pytest

import alerts


def test_log_new_target(updated_holdings_data):
    alerts.log_new_target('DeFiGod', 1000, updated_holdings_data)

    assert alerts._log[0].token_list == ['ETH', 'DPX']


@pytest.mark.parametrize('token_data, expected', [
    ({'amount': 5001.344, 'usd_price': 3668.29}, True),
    ({'amount': 1.344, 'usd_price': 668.29}, False)
])
def test_adds_new_token_alert_with_portfolio_pc(test_target, token_data, expected):
    alerts._add_alert('added', test_target, 'eth', 'ETH', token_data)
    assert ('%' in alerts._log[0].msg) == expected
