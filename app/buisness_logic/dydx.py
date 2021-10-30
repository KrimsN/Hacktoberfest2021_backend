import requests
from functools import lru_cache

from app.buisness_logic.base_exchange import AbstractBaseExchange


class Dydx(AbstractBaseExchange):
    _api_base: str = "https://api.dydx.exchange"
    platform_name = "dYdX"

    @classmethod
    @lru_cache
    def get_all_trade_pairs_ids(cls):
        path = "/v3/markets"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        result = sorted([i for i in resp['markets'].keys()])
        return result

    @classmethod
    def get_avg_price(cls, symbol: str) -> dict:
        resp = cls.get_depth(symbol)
        # почему то цены спроса тут выше чем цены предлоэенией
        lowest_bid = sorted(resp['bids'], key=lambda x: float(x['price']), reverse=True)[0]
        highest_ask = sorted(resp['asks'], key=lambda x: float(x['price']))[0]
        # -------------------------------
        res = {
            'price': (float(highest_ask['price']) + float(lowest_bid['price'])) / 2,
            "highest_ask": highest_ask['price'],
            "lowest_bid": lowest_bid['price']
        }
        res = cls._add_meta_info(res, symbol)
        return res

    @classmethod
    def get_depth(cls, symbol: str) -> dict:
        path: str = "/v3/orderbook"
        query: str = f"/{symbol}"
        resp = requests.get(f"{cls._api_base}{path}{query}", allow_redirects=True, headers=cls._headers).json()

        res_depth = {"bids": [], "asks": []}

        for bid in resp["bids"]:
            res_depth["bids"].append({
                "price": bid['price'],
                "qty": bid['size']
            })
        for ask in resp["asks"]:
            res_depth["asks"].append({
                "price": ask['price'],
                "qty": ask['size']
            })

        res_depth = cls._add_meta_info(res_depth, symbol)
        return res_depth


