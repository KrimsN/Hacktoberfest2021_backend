import decimal
from loguru import logger

from app.buisness_logic.binance import Binance
from app.buisness_logic.coinbase import Coinbase
from app.buisness_logic.dydx import Dydx
from app.buisness_logic.ftx import Ftx
from app.buisness_logic.gate_io import GateIo
from app.buisness_logic.kucoin import KuCoin


from app.core.config import SYMBOL_TABLE


def accessable_symbols():
    return sorted(list(SYMBOL_TABLE.keys()))


def info_about_accessable_symbols():
    return SYMBOL_TABLE.copy()


def aggregate_current_price(symbol: str):
    symbol_aliases = SYMBOL_TABLE[symbol]

    if symbol_aliases.get('binance') is not None:
        binance_avg = Binance.get_avg_price(symbol_aliases['binance'])
    else:
        binance_avg = {"platform": Binance.platform_name, 'price': None, "symbol": None}

    if symbol_aliases.get('coinbase') is not None:
        coinbase_avg = Coinbase.get_avg_price(symbol_aliases['coinbase'])
    else:
        coinbase_avg = {"platform": Coinbase.platform_name, 'price': None, "symbol": None}

    if symbol_aliases.get('kucoin') is not None:
        kucoin_avg = KuCoin.get_avg_price(symbol_aliases['kucoin'])
    else:
        kucoin_avg = {"platform": KuCoin.platform_name, 'price': None, "symbol": None}

    if symbol_aliases.get('gateio') is not None:
        gateio_avg = GateIo.get_avg_price(symbol_aliases['gateio'])
    else:
        gateio_avg = {"platform": GateIo.platform_name, 'price': None, "symbol": None}

    if symbol_aliases.get('dydx') is not None:
        dydx_avg = Dydx.get_avg_price(symbol_aliases['dydx'])
    else:
        dydx_avg = {"platform": Dydx.platform_name, 'price': None, "symbol": None}

    if symbol_aliases.get('ftx') is not None:
        ftx_avg = Ftx.get_avg_price(symbol_aliases['ftx'])
    else:
        ftx_avg = {"platform": Ftx.platform_name, 'price': None, "symbol": None}

    res = {
        "symbol": symbol,
        "data": [
            binance_avg,
            coinbase_avg,
            kucoin_avg,
            gateio_avg,
            dydx_avg,
            ftx_avg
        ]
    }
    return res


def aggregate_bids_asks(symbol):
    symbol_aliases = SYMBOL_TABLE[symbol]

    logger.info(f'Aggregate bid/asks by {symbol = }')
    logger.debug(f"{symbol_aliases = }")

    res = {"bids": [], "asks": []}

    if symbol_aliases.get('binance') is not None:
        try:
            binance = Binance.get_depth(symbol_aliases['binance'])
            res['bids'].extend(binance['bids'])
            res['asks'].extend(binance['asks'])
        except Exception as e:
            logger.error("binance error")
            logger.error(e)

    if symbol_aliases.get('coinbase') is not None:
        try:
            coinbase = Coinbase.get_depth(symbol_aliases['coinbase'])
            res['bids'].extend(coinbase['bids'])
            res['asks'].extend(coinbase['asks'])
        except Exception as e:
            logger.error("coinbase error")
            logger.error(e)

    if symbol_aliases.get('dydx') is not None:
        try:
            dydx = Dydx.get_depth(symbol_aliases['dydx'])
            res['bids'].extend(dydx['bids'])
            res['asks'].extend(dydx['asks'])
        except Exception as e:
            logger.error("dydx error")
            logger.error(e)

    if symbol_aliases.get('gateio') is not None:
        try:
            gateio = GateIo.get_depth(symbol_aliases['gateio'])
            res['bids'].extend(gateio['bids'])
            res['asks'].extend(gateio['asks'])
        except Exception as e:
            logger.error("gateio error")
            logger.error(e)

    if symbol_aliases.get('kucoin') is not None:
        try:
            kucoin = KuCoin.get_depth(symbol_aliases['kucoin'])
            res['bids'].extend(kucoin['bids'])
            res['asks'].extend(kucoin['asks'])
        except Exception as e:
            logger.error("kucoin error")
            logger.error(e)

    if symbol_aliases.get('ftx') is not None:
        try:
            ftx = Ftx.get_depth(symbol_aliases['ftx'])
            res['bids'].extend(ftx['bids'])
            res['asks'].extend(ftx['asks'])
        except Exception as e:
            logger.error("ftx error")
            logger.error(e)

    res['bids'].sort(key=lambda x: float(x['price']), reverse=True)
    res['asks'].sort(key=lambda x: float(x['price']))
    return res


def calculate_sell(symbol, total_amount):
    logger.info('Calculate to sell')
    total_amount = decimal.Decimal(total_amount)

    bids = aggregate_bids_asks(symbol)['bids']

    sum = {
        'price': decimal.Decimal(0),
        'amount': decimal.Decimal(0),
        'completed': False,
        'avgPrice': None,
        "bids": [],
    }

    for bid in bids:
        price = decimal.Decimal(bid['price'])
        qty = decimal.Decimal(bid['qty'])
        platform = bid['platform']
        sum['amount'] += qty
        sum['price'] += price * qty
        sum["bids"].append(bid)
        if platform not in sum.keys():
            sum[platform] = 1
        else:
            sum[platform] += 1

        if sum["amount"] >= total_amount:
            diff = sum['amount'] - total_amount
            sum['amount'] -= diff
            sum['price'] -= diff * price
            sum['bids'][-1]['qty'] = decimal.Decimal(sum['bids'][-1]['qty']) - diff
            sum['completed'] = True
            break

    sum['avgPrice'] = sum['price']/sum['amount']
    return sum


def calculate_buy(symbol, total_amount):
    logger.info('Calculate to buy')
    total_amount = decimal.Decimal(total_amount)

    asks = aggregate_bids_asks(symbol)['asks']

    sum = {
        'price': decimal.Decimal(0),
        'amount': decimal.Decimal(0),
        'completed': False,
        'avgPrice': None,
        "asks": [],
    }

    for ask in asks:
        price = decimal.Decimal(ask['price'])
        qty = decimal.Decimal(ask['qty'])
        platform = ask['platform']
        sum['amount'] += qty
        sum['price'] += price * qty
        sum["asks"].append(ask)
        if platform not in sum.keys():
            sum[platform] = 1
        else:
            sum[platform] += 1

        if sum["amount"] >= total_amount:
            diff = sum['amount'] - total_amount
            sum['amount'] -= diff
            sum['price'] -= diff * price
            sum['asks'][-1]['qty'] = decimal.Decimal(sum['asks'][-1]['qty']) - diff

            sum['completed'] = True
            break

    sum['avgPrice'] = sum['price'] / sum['amount']
    return sum


