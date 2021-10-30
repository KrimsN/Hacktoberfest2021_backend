from fastapi import APIRouter

from app.buisness_logic.kucoin import KuCoin

router = APIRouter()


@router.get("/tradePairsIds")
async def get_trade_pairs_ids():
    res = KuCoin.get_all_trade_pairs_ids()
    return res


@router.get("/avgPrice")
async def get_avg_price(symbol: str):
    res = KuCoin.get_avg_price(symbol)
    return res


@router.get("/depth")
async def get_price(symbol: str):
    res = KuCoin.get_depth(symbol)
    return res

