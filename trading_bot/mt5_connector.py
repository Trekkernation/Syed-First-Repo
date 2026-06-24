import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import config

TIMEFRAME_MAP = {
    "M1":  mt5.TIMEFRAME_M1,
    "M5":  mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1":  mt5.TIMEFRAME_H1,
    "H4":  mt5.TIMEFRAME_H4,
}


def connect():
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialize() failed: {mt5.last_error()}")

    if config.MT5_LOGIN and config.MT5_PASSWORD and config.MT5_SERVER:
        ok = mt5.login(config.MT5_LOGIN, config.MT5_PASSWORD, config.MT5_SERVER)
        if not ok:
            raise RuntimeError(f"MT5 login failed: {mt5.last_error()}")

    info = mt5.account_info()
    print(f"Connected: {info.name} | Balance: {info.balance} {info.currency} | Server: {info.server}")
    return info


def disconnect():
    mt5.shutdown()


def get_balance():
    return mt5.account_info().balance


def get_ohlcv(symbol: str, bars: int = 600) -> pd.DataFrame:
    tf = TIMEFRAME_MAP[config.TIMEFRAME]
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
    if rates is None or len(rates) == 0:
        raise ValueError(f"No data returned for {symbol}. Check symbol name in MT5.")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.rename(columns={"open": "Open", "high": "High", "low": "Low",
                        "close": "Close", "tick_volume": "Volume"}, inplace=True)
    return df[["time", "Open", "High", "Low", "Close", "Volume"]]


def get_open_trades():
    positions = mt5.positions_get(magic=config.MAGIC_NUMBER)
    return [] if positions is None else list(positions)


def get_symbol_info(symbol: str):
    info = mt5.symbol_info(symbol)
    if info is None:
        raise ValueError(f"Symbol '{symbol}' not found in MT5. Check the exact name.")
    if not info.visible:
        mt5.symbol_select(symbol, True)
    return info


def place_order(symbol: str, direction: str, lot: float, sl_price: float, tp_price: float) -> bool:
    info = get_symbol_info(symbol)
    tick = mt5.symbol_info_tick(symbol)

    order_type = mt5.ORDER_TYPE_BUY if direction == "BUY" else mt5.ORDER_TYPE_SELL
    price = tick.ask if direction == "BUY" else tick.bid

    request = {
        "action":    mt5.TRADE_ACTION_DEAL,
        "symbol":    symbol,
        "volume":    lot,
        "type":      order_type,
        "price":     price,
        "sl":        round(sl_price, info.digits),
        "tp":        round(tp_price, info.digits),
        "deviation": 20,
        "magic":     config.MAGIC_NUMBER,
        "comment":   "AI Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"  Order placed: {direction} {lot} {symbol} @ {price} | SL={sl_price:.5f} TP={tp_price:.5f}")
        return True
    else:
        print(f"  Order FAILED for {symbol}: retcode={result.retcode} — {result.comment}")
        return False
