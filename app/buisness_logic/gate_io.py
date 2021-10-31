import requests
from functools import lru_cache

from cachetools.func import ttl_cache
from loguru import logger

from app.buisness_logic.base_exchange import AbstractBaseExchange


class GateIo(AbstractBaseExchange):
    _api_base = "https://api.gateio.ws"
    platform_name = "gate.io"

    @classmethod
    @lru_cache
    def get_all_trade_pairs_ids(cls):
        logger.info(f"<GateIo>. get_all_trade_pairs ")
        path = "/api/v4/spot/currency_pairs"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        result = sorted([i['id'] for i in resp])
        return result

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_avg_price(cls, symbol: str) -> dict:
        logger.info(f"<GateIo>. get_avg_price({symbol = }) ")
        resp = cls.get_depth(symbol)
        highest_bid = sorted(resp['bids'], key=lambda x: float(x['price']), reverse=True)[0]
        lowest_ask = sorted(resp['asks'], key=lambda x: float(x['price']))[0]
        res = {
            'price': (float(lowest_ask['price']) + float(highest_bid['price'])) / 2,
        }
        res = cls._add_meta_info(res, symbol)
        return res

    @classmethod
    @ttl_cache(ttl=60 * 5)
    def get_depth(cls, symbol: str) -> dict:
        logger.info(f"<GateIo>. get_depth({symbol = }) ")
        path: str = "/api/v4/spot/order_book"
        query: str = f"?currency_pair={symbol}"
        resp = requests.get(f"{cls._api_base}{path}{query}", allow_redirects=True, headers=cls._headers).json()

        res_depth = {"bids": [], "asks": []}

        for bid in resp["bids"]:
            res_depth["bids"].append({
                "platform": "gate_io",
                "price": bid[0],
                "qty": bid[1]
            })
        for ask in resp["asks"]:
            res_depth["asks"].append({
                "platform": "gate_io",
                "price": ask[0],
                "qty": ask[1]
            })

        res_depth = cls._add_meta_info(res_depth, symbol)
        return res_depth
