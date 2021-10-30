import requests
import time
from functools import lru_cache


class KuCoin:
    _api_base: str = "https://openapi-sandbox.kucoin.com"
    _headers: dict[str, str] = {"Accept": "application/json"}

    @staticmethod
    def _add_meta_info(d: dict, symbol: str) -> dict:
        d['symbol'] = symbol
        d['platform'] = "KuCoin"
        d['timestamp_UTC+7'] = time.time()
        return d

    @classmethod
    @lru_cache
    def get_all_trade_pairs_ids(cls):
        path = "/api/v1/symbols"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        result = sorted([i['symbol'] for i in resp['data']])
        return result

    @classmethod
    def get_avg_price(cls, symbol: str):
        path: str = "/api/v1/market/stats"
        query: str = f"?symbol={symbol}"
        resp = requests.get(f"{cls._api_base}{path}{query}", headers=cls._headers, allow_redirects=True).json()
        res = {"price": resp["averagePrice"]}
        res = cls._add_meta_info(res, symbol)
        return res

    @classmethod
    def get_depth(cls, symbol: str):
        path: str = "/api/v3/market/orderbook/level2"
        query: str = f"?symbol={symbol}"
        resp = requests.get(f"{cls._api_base}{path}{query}", headers=cls._headers, allow_redirects=True).json()

        res_depth = {"bids": [], "asks": []}
        for bid in resp['bids']:
            res_depth["bids"].append({
                "price": bid[0],
                "qty": bid[1]
            })
        for ask in resp["asks"]:
            res_depth["asks"].append({
                "price": ask[0],
                "qty": ask[1]
            })

        res_depth = cls._add_meta_info(res_depth, symbol)
        return res_depth
