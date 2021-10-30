import requests
import time
from functools import lru_cache


class GateIo:
    _api_base = "https://api.gateio.ws"
    _headers: dict[str, str] = {"Accept": "application/json"}

    @staticmethod
    def _add_meta_info(d: dict, symbol: str) -> dict:
        d['symbol'] = symbol
        d['platform'] = "gate.io"
        d['timestamp_UTC+7'] = time.time()
        return d

    @classmethod
    @lru_cache
    def get_all_trade_pairs_ids(cls):
        path = "/api/v4/spot/currency_pairs"
        resp = requests.get(f"{cls._api_base}{path}", headers=cls._headers, allow_redirects=True).json()
        result = sorted([i['id'] for i in resp])
        return result
