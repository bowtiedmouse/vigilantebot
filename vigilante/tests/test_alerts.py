import alerts


def test_log_new_target(requested_data):
    token_list = alerts.log_new_target('DeFiGod', 1000,
                                       requested_data['tokens_by_chain'])
    assert token_list == ['PDT', 'FTM', 'CVXCRV', 'PSP', 'CVXFXS', 'ETH', 'MAGIC',
                          'DPX', 'ETH', 'WETH', 'USDC', 'USDC', 'MIM', 'BRUSH', 'AVAX',
                          'ZIP', 'ETH']
