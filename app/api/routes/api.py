from fastapi import APIRouter

from app.api.routes import (
    default,
    binance,
    coinbase,
    kucoin,
    gate_io,
    dydx,
    production,
    ftx
)


api_router = APIRouter()

api_router.include_router(default.router, tags=["default"])
api_router.include_router(production.router, tags=["Production routes"], prefix='/prod')
api_router.include_router(binance.router, tags=["Binance"], prefix='/binance')
api_router.include_router(coinbase.router, tags=["Coinbase"], prefix='/coinbase')
api_router.include_router(kucoin.router, tags=["KuCoin"], prefix='/kucoin')
api_router.include_router(gate_io.router, tags=["Gate.io"], prefix='/gate_io')
api_router.include_router(dydx.router, tags=["dYdX"], prefix='/dydx')
api_router.include_router(ftx.router, tags=["Ftx"], prefix='/ftx')

