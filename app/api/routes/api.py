from fastapi import APIRouter

from app.api.routes import (
    default,
    binance,
    coinbase,
    kukoin,
)


api_router = APIRouter()

api_router.include_router(default.router, tags=["default"])
api_router.include_router(binance.router, tags=["Binance"], prefix='/binance')
api_router.include_router(coinbase.router, tags=["Coinbase"], prefix='/coinbase')
api_router.include_router(kukoin.router, tags=["KuCoin"], prefix='/kucoin')
