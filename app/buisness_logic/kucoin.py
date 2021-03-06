import requests
from functools import lru_cache
from cachetools.func import ttl_cache
from loguru import logger

from app.buisness_logic.base_exchange import AbstractBaseExchange


class KuCoin(AbstractBaseExchange):
    _api_base: str = "https://openapi-sandbox.kucoin.com"
    platform_name = "KuCoin"

    @classmethod
    @lru_cache
    def get_all_trade_pairs_ids(cls):
        logger.info(f"<KuCoin>. get_all_trade_pairs ")
        path = "/api/v1/symbols"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        result = sorted([i['symbol'] for i in resp['data']])
        return result

    @classmethod
    @ttl_cache(ttl=60*5)
    def get_avg_price(cls, symbol: str):
        logger.info(f"<KuCoin>. get_avg_price({symbol = }) ")
        path: str = "/api/v1/market/stats"
        query: str = f"?symbol={symbol}"
        resp = requests.get(f"{cls._api_base}{path}{query}", headers=cls._headers, allow_redirects=True).json()
        res = {"price": resp['data']["averagePrice"]}
        res = cls._add_meta_info(res, symbol)
        return res

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_depth(cls, symbol: str):
        logger.info(f"<KuCoin>. get_depth({symbol = }) ")
        path: str = "/api/v1/market/orderbook/level2"
        query: str = f"?symbol={symbol}"
        resp = requests.get(f"{cls._api_base}{path}{query}", headers=cls._headers, allow_redirects=True).json()

        res_depth = {"bids": [], "asks": []}
        for bid in resp['data']['bids']:
            res_depth["bids"].append({
                "platform": "kucoin",
                "price": bid[0],
                "qty": bid[1]
            })
        for ask in resp['data']["asks"]:
            res_depth["asks"].append({
                "platform": "kucoin",
                "price": ask[0],
                "qty": ask[1]
            })

        res_depth = cls._add_meta_info(res_depth, symbol)
        return res_depth
