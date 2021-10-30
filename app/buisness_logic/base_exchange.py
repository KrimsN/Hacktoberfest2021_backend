from abc import ABC, abstractmethod
import time


class AbstractBaseExchange(ABC):

    @classmethod
    @property
    @abstractmethod
    def _api_base(cls) -> str:
        raise NotImplementedError()

    @classmethod
    @property
    @abstractmethod
    def _platform_name(cls) -> str:
        raise NotImplementedError()

    @classmethod
    @property
    def _headers(cls) -> dict[str, str]:
        return {"Accept": "application/json"}

    @classmethod
    def _add_meta_info(cls, d: dict, symbol: str) -> dict:
        d['symbol'] = symbol
        d['platform'] = cls._platform_name
        d['timestamp_UTC+7'] = time.time()
        return d

    @classmethod
    @abstractmethod
    def get_all_trade_pairs_ids(cls) -> list[str]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_avg_price(cls, symbol: str) -> dict:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_depth(cls, symbol: str) -> dict:
        raise NotImplementedError()

