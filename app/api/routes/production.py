from fastapi import APIRouter, Query


from app.buisness_logic.production import (
    accessable_symbols,
    info_about_accessable_symbols,
    calculate_sell,
    aggregate_current_price,
    aggregate_bids_asks,
    calculate_buy
)


router = APIRouter()


@router.get('/symbols')
async def get_accessable_symbols():
    return accessable_symbols()


@router.get('/symbolsFull')
async def get_info_about_accessable_symbols():
    return info_about_accessable_symbols()


@router.get("/aggregatedCurrentPrice")
async def get_aggregated_current_price(symbol: str = Query("ETH-USDT")):
    return aggregate_current_price(symbol)


@router.get("/allBidAsks")
async def get_all_aggregated_bids_asks(symbol: str = Query("ETH-USDT")):
    return aggregate_bids_asks(symbol)


@router.get('/calculateSell')
async def get_calculating_for_sell(symbol: str = Query("ETH-USDT"), total_amount: float = Query(10)):
    return calculate_sell(symbol, total_amount)


@router.get('/calculateBuy')
async def get_calculating_for_buy(symbol: str = Query("ETH-USDT"), total_amount: float = Query(10)):
    return calculate_buy(symbol, total_amount)





