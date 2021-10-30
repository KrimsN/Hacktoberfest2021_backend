import requests
import time


class Binance:
    _api_base: str = "https://api.binance.com"
    _headers: dict[str, str] = {"Accept": "application/json"}

    @staticmethod
    def _add_meta_info(d: dict, symbol: str) -> dict:
        d['symbol'] = symbol
        d['platform'] = "binance"
        d['timestamp_UTC+7'] = time.time()
        return d

    @classmethod
    def get_avg_price(cls, symbol: str) -> dict:
        path: str = "/api/v3/avgPrice"
        query: str = f"?symbol={symbol}USDT"
        res = requests.get(f"{cls._api_base}{path}{query}", allow_redirects=True, headers=cls._headers)
        res_j: dict = res.json()
        res_j = cls._add_meta_info(res_j, symbol)
        return res_j

    @classmethod
    def get_depth(cls, symbol: str) -> dict:
        path: str = "/api/v3/depth"
        query: str = f"?symbol={symbol}USDT"
        res = requests.get(f"{cls._api_base}{path}{query}", allow_redirects=True, headers=cls._headers)
        res_j: dict = res.json()

        res_depth = {"bids": [], "asks": []}

        for bid in res_j["bids"]:
            res_depth["bids"].append({
                "price": bid[0],
                "qty": bid[1]
            })
        for ask in res_j["asks"]:
            res_depth["asks"].append({
                "price": ask[0],
                "qty": ask[1]
            })

        res_depth = cls._add_meta_info(res_depth, symbol)
        return res_depth
