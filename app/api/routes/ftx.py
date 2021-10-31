from fastapi import APIRouter

from app.buisness_logic.ftx import Ftx

router = APIRouter()


@router.get("/tradePairsIds")
async def get_trade_pairs_ids():
    res = Ftx.get_all_trade_pairs_ids()
    return res


@router.get("/avgPrice")
async def get_avg_price(symbol: str):
    res = Ftx.get_avg_price(symbol)
    return res


@router.get("/depth")
async def get_price(symbol: str):
    res = Ftx.get_depth(symbol)
    return res

