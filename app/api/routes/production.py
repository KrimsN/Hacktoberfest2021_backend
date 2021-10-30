from fastapi import APIRouter

router = APIRouter()


@router.get("/aggregatedCurrentPrice")
async def get_aggregated_current_price(symbol: str): # TODO: implement
    tmp = {
        "symbol": symbol,
        "data": [
            {'Binance': "61235.13"},
            {'CoinBase': "61251.23"},
            {'KuCoin': "612341.543"},
            {'Gate.io': "61234.45645"},
        ]
    }
    return tmp
