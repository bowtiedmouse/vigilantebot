import holdings


def test_compare_holdings_diff(saved_data, requested_data, diff_dict):
    diff = holdings._compare_holdings(saved_data, requested_data)
    assert diff == diff_dict
