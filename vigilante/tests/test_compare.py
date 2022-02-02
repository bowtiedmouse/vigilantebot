import pytest

from compare import _compare_holdings


@pytest.fixture
def saved_data():
    return {
        "alias": "Me",
        "usd_balance": 0,
        "last_active": 0,
        "tokens_by_chain": {
            "eth": {
                "PDT": "475.63850932673466",
                "LINK": "169.84653761752556",
                "CVXCRV": "542.54690279384184",
                "PSP": "700.0",
                "CVXFXS": "225.15843445540992",
                "ETH": "1.21453259697220345"
            },
            "arb": {
                "MAGIC": "1155.62757924869086",
                "ETH": "0.7073949818623116",
                "WETH": "2.57279034377025"
            },
            "bsc": {
                "USDC": "117.106"
            },
            "ftm": {
                "BRUSH": "1810.2606114419204"
            },
            "avax": {
                "AVAX": "7.367895972757745"
            },
            "op": {
                "ZIP": "2425.2278482690444",
                "ETH": "0.11459204326855285"
            }
        }
    }


@pytest.fixture
def requested_data():
    return {
        "alias": "Me",
        "usd_balance": 0,
        "last_active": 0,
        "tokens_by_chain": {
            "eth": {
                "PDT": "475.63850932673466",
                "FTM": "69.84653761752556",
                "CVXCRV": "242.54690279384184",
                "PSP": "700.0",
                "CVXFXS": "225.15843445540992",
                "ETH": "0.21453259697220345"
            },
            "arb": {
                "MAGIC": "155.62757924869086",
                "DPX": "0.32030158008708476",
                "ETH": "0.7073949818623116",
                "WETH": "2.57279034377025",
                "USDC": "2618.52978"
            },
            "bsc": {
                "USDC": "117.106"
            },
            "ftm": {
                "MIM": "547.7211225042761",
                "BRUSH": "1810.2606114419204"
            },
            "avax": {
                "AVAX": "7.367895972757745"
            },
            "op": {
                "ZIP": "2425.2278482690444",
                "ETH": "0.11459204326855285"
            }
        }
    }


# def test_compare_holdings(saved_data, requested_data, compared_result):
#     result = _compare_holdings(saved_data, requested_data)
#     assert result == compared_result
