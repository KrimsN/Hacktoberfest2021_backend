import requests
from functools import lru_cache

from cachetools.func import ttl_cache
from loguru import logger

from app.buisness_logic.base_exchange import AbstractBaseExchange


class Binance(AbstractBaseExchange):
    _api_base: str = "https://api.binance.com"
    platform_name = "Binance"

    @classmethod
    @lru_cache
    def get_all_trade_pairs_ids(cls):
        logger.info(f"<Binance>. get_all_trade_pairs ")
        path = "/api/v3/ticker/price"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        result = sorted([i['symbol'] for i in resp])
        return result

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_avg_price(cls, symbol: str) -> dict:
        logger.info(f"<Binance>. get_avg_price({symbol = })")
        path: str = "/api/v3/avgPrice"
        query: str = f"?symbol={symbol}"
        res = requests.get(f"{cls._api_base}{path}{query}", allow_redirects=True, headers=cls._headers)
        res_j: dict = res.json()
        res_j = cls._add_meta_info(res_j, symbol)
        return res_j

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_depth(cls, symbol: str) -> dict:
        logger.info(f"<Binance>. get_depth({symbol = })")
        path: str = "/api/v3/depth"
        query: str = f"?symbol={symbol}"
        res = requests.get(f"{cls._api_base}{path}{query}", allow_redirects=True, headers=cls._headers)
        res_j: dict = res.json()

        res_depth = {"bids": [], "asks": []}

        for bid in res_j["bids"]:
            res_depth["bids"].append({
                "platform": "binance",
                "price": bid[0],
                "qty": bid[1]
            })
        for ask in res_j["asks"]:
            res_depth["asks"].append({
                "platform": "binance",
                "price": ask[0],
                "qty": ask[1]
            })

        res_depth = cls._add_meta_info(res_depth, symbol)
        return res_depth


