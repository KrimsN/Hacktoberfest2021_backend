from fastapi import APIRouter

from app.buisness_logic.gate_io import GateIo

router = APIRouter()


@router.get("/tradePairsIds")
async def get_trade_pairs_ids():
    res = GateIo.get_all_trade_pairs_ids()
    return res


@router.get("/avgPrice")
async def get_avg_price(symbol: str):
    res = GateIo.get_avg_price(symbol)
    return res


@router.get("/depth")
async def get_price(symbol: str):
    res = GateIo.get_depth(symbol)
    return res

