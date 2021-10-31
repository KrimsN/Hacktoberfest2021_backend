import requests
from functools import lru_cache

from cachetools.func import ttl_cache
from loguru import logger

from app.buisness_logic.base_exchange import AbstractBaseExchange


class Coinbase(AbstractBaseExchange):
    _api_base: str = "https://api.exchange.coinbase.com"
    platform_name = "Coinbase"

    @classmethod
    @lru_cache
    def get_all_trade_pairs(cls):
        path = "/products"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        return resp

    @classmethod
    @lru_cache
    def get_all_trade_pairs_ids(cls):
        logger.info(f"<Coinbase>. get_all_trade_pairs_ids ")
        resp = cls.get_all_trade_pairs()
        result = sorted([i['id'] for i in resp])
        return result

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_avg_price(cls, symbol: str):
        logger.info(f"<Coinbase>. get_avg_price({symbol = }) ")
        path: str = f"/products/{symbol}/book?level=1"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        res = {
            "price": (float(resp['bids'][0][0]) + float(resp['asks'][0][0])) / 2
        }
        res = cls._add_meta_info(res, symbol)
        return res

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_depth(cls, symbol: str):
        logger.info(f"<Coinbase>. get_depth({symbol = }) ")
        path: str = f"/products/{symbol}/book?level=2"
        res = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()

        res_depth = {"bids": [], "asks": []}
        for bid in res['bids']:
            res_depth["bids"].append({
                "platform": "coinbase",
                "price": bid[0],
                "qty": bid[1]
            })
        for ask in res["asks"]:
            res_depth["asks"].append({
                "platform": "coinbase",
                "price": ask[0],
                "qty": ask[1]
            })

        res_depth = cls._add_meta_info(res_depth, symbol)
        return res_depth



