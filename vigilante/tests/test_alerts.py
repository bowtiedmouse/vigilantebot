import alerts


def test_log_new_target(updated_holdings_data):
    # This needs to return token_list from log_new_target to pass
    token_list = alerts.log_new_target('DeFiGod', 1000,
                                       updated_holdings_data)
    assert token_list == ['ETH', 'DPX']
