import json

import pytest

from target import Target

@pytest.fixture
def saved_holdings_data():
    with open('../models/targets_holdings_model.json', 'r') as f:
        return json.load(f)['Whale 1']['wallet_holdings']


@pytest.fixture
def requested_data():
    with open('../models/debank_token_list_model.json', 'r') as f:
        return json.load(f)


@pytest.fixture
def updated_holdings_data():
    with open('../models/targets_holdings_model.json', 'r') as f:
        data = json.load(f)['Whale 1']['wallet_holdings']
    data['eth']['ETH']['amount'] += 2.00
    # usd_price should be excluded from comparison
    data['eth']['ETH']['usd_price'] += 122.00
    data['arb']['DPX'] = {
        "contract_address": "0x1aa61c196e76805fcbe394ea00e4ffced24fc420",
        "symbol": "DPX",
        "amount": "51.344",
        "usd_price": "1668.29"
    }
    del data['arb']['MAGIC']
    return data


@pytest.fixture
def diff_dict():
    return {'dictionary_item_added': {
                "root['arb']['DPX']": {
                    'amount': '51.344',
                    'contract_address': '0x1aa61c196e76805fcbe394ea00e4ffced24fc420',
                    'symbol': 'DPX',
                    'usd_price': '1668.29'}},
            'dictionary_item_removed': {
                "root['arb']['MAGIC']": {
                    'amount': 1551.344,
                    'contract_address': '0x1aa61c196e76805fcbe394ea00e4ffced24fc469',
                    'symbol': 'MAGIC',
                    'usd_price': 8.29}},
            'values_changed': {
                "root['eth']['ETH']['amount']": {
                    'new_value': 3.3440000000000003,
                    'old_value': 1.344}}}


@pytest.fixture
def test_target():
    return Target('Test Target', ['0x3f3e305c4ad49271ebda489dd43d2c8f027d2d41'])
