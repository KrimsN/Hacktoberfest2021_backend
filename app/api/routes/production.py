from fastapi import APIRouter


from app.buisness_logic.binance import Binance
from app.buisness_logic.dydx import Dydx
from app.buisness_logic.kucoin import KuCoin
from app.buisness_logic.gate_io import GateIo
from app.buisness_logic.coinbase import Coinbase

from app.core.config import SYMBOL_TABLE

router = APIRouter()


@router.get('/symbols')
async def get_accessable_symbols():
    return sorted(list(SYMBOL_TABLE.keys()))


@router.get('/symbolsFull')
async def get_info_about_accessable_symbols():
    return SYMBOL_TABLE


@router.get("/aggregatedCurrentPrice")
async def get_aggregated_current_price(symbol: str):

    symbol_aliases = SYMBOL_TABLE[symbol]

    if symbol_aliases['binance'] is not None:
        binance_avg = Binance.get_avg_price(symbol_aliases['binance'])
    else:
        binance_avg = None# TODO: implement
        
    if symbol_aliases['coinbase'] is not None:
        coinbase_avg = Coinbase.get_avg_price(symbol_aliases['coinbase'])
    else:
        coinbase_avg = None
        
    if symbol_aliases['kucoin'] is not None:
        kucoin_avg = KuCoin.get_avg_price(symbol_aliases['kucoin'])
    else:
        kucoin_avg = None
        
    if symbol_aliases['gateio'] is not None:
        gateio_avg = GateIo.get_avg_price(symbol_aliases['gateio'])
    else:
        gateio_avg = None
        
    if symbol_aliases['dydx'] is not None:
        dydx_avg = Dydx.get_avg_price(symbol_aliases['dydx'])
    else:
        dydx_avg = None

    res = {
        "symbol": symbol,
        "data": [
            {'Binance': binance_avg},
            {'CoinBase': coinbase_avg},
            {'KuCoin': kucoin_avg},
            {'Gate.io': gateio_avg},
            {'dYdX': dydx_avg},
        ]
    }
    return res
