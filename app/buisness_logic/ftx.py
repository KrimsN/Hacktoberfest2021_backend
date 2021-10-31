import requests
from functools import lru_cache

from cachetools.func import ttl_cache
from loguru import logger

from app.buisness_logic.base_exchange import AbstractBaseExchange


class Ftx(AbstractBaseExchange):
    _api_base = "https://ftx.com/api"
    platform_name = "ftx"

    @classmethod
    @lru_cache
    def get_all_trade_pairs_ids(cls):
        logger.info(f"<Ftx>. get_all_trade_pairs ")
        path = "/markets"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        if not resp['success']:
            return []
        resp = resp['result']
        result = []
        for sym in resp:
            if (sym['baseCurrency'] is not None) and (sym['quoteCurrency'] is not None):
                result.append(sym['name'])
        return sorted(result)

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_avg_price(cls, symbol: str) -> dict:
        logger.info(f"<Ftx>. get_avg_price({symbol = }) ")
        path: str = f"/markets/{symbol}"
        resp = requests.get(f"{cls._api_base}{path}", allow_redirects=True, headers=cls._headers).json()
        res = {
            'price': resp['result']['price']
        }
        res = cls._add_meta_info(res, symbol)
        return res

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_depth(cls, symbol: str) -> dict:
        logger.info(f"<Ftx>. get_depth({symbol = }) ")
        path: str = f"/markets/{symbol}/orderbook"
        query: str = f"?depth=100"
        resp = requests.get(f"{cls._api_base}{path}{query}", allow_redirects=True, headers=cls._headers).json()
        resp = resp['result']

        res_depth = {"bids": [], "asks": []}

        for bid in resp["bids"]:
            res_depth["bids"].append({
                "platform": "ftx",
                "price": bid[0],
                "qty": bid[1]
            })
        for ask in resp["asks"]:
            res_depth["asks"].append({
                "platform": "ftx",
                "price": ask[0],
                "qty": ask[1]
            })

        res_depth = cls._add_meta_info(res_depth, symbol)
        return res_depth
