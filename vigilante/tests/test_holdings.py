import holdings


def test_compare_holdings_diff(saved_holdings_data, updated_holdings_data, diff_dict):
    diff = holdings._compare_holdings(saved_holdings_data, updated_holdings_data)
    assert diff == diff_dict


def test_process_target_token_list(updated_holdings_data, requested_data):
    data = holdings._process_token_list({}, requested_data)
    assert data == {'arb': {'ETH': {'amount': 1.387234568968202,
                                    'contract_address': 'arb',
                                    'symbol': 'ETH',
                                    'usd_price': 2840.69}}}


def test_new_value_is_min_diff_than_old_value():
    assert holdings.is_min_diff(190, 100)
    assert not holdings.is_min_diff(1.0, 1.001)
