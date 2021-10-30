from fastapi import APIRouter

from app.buisness_logic.gate_io import GateIo

router = APIRouter()


@router.get("/tradePairsIds")
async def get_trade_pairs_ids():
    res = GateIo.get_all_trade_pairs_ids()
    return res


