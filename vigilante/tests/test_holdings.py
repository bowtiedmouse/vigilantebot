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
