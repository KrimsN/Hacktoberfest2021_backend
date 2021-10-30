from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.buisness_logic.binance import Binance

router = APIRouter()


@router.get("/avgPrice")
async def get_price(symbol: str):
    res = Binance.get_avg_price(symbol)
    return res


@router.get("/depth")
async def get_price(symbol: str):
    res = Binance.get_depth(symbol)
    return res



