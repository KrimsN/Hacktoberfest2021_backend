from fastapi import APIRouter

from app.api.routes import (
    default,
    binance,
)


api_router = APIRouter()

api_router.include_router(default.router, tags=["default"])
api_router.include_router(binance.router, tags=["binance"], prefix='/binance')
