import math
import MetaTrader5 as mt5
import mt5_connector as conn
import config


def calculate_lot(symbol: str, sl_pips: float) -> float:
    """
    Calculate lot size so that the loss on a stopped-out trade
    equals RISK_PERCENT % of current account balance.
    """
    balance    = conn.get_balance()
    risk_amount = balance * (config.RISK_PERCENT / 100)

    info = conn.get_symbol_info(symbol)
    tick_value = info.trade_tick_value   # value of 1 tick move in account currency
    tick_size  = info.trade_tick_size

    if tick_size == 0 or tick_value == 0:
        return info.volume_min

    # pip value per lot
    pip_value_per_lot = (tick_value / tick_size) * info.point

    if sl_pips <= 0 or pip_value_per_lot <= 0:
        return info.volume_min

    lot = risk_amount / (sl_pips * pip_value_per_lot)

    # Clamp to broker limits
    lot = max(info.volume_min, min(info.volume_max, lot))
    lot = round(lot / info.volume_step) * info.volume_step
    lot = round(lot, 2)

    return lot


def calculate_sl_tp(symbol: str, direction: str, atr: float):
    """
    Returns (sl_price, tp_price, sl_distance_in_points).
    SL = 1.5 * ATR, TP = 2.5 * ATR from entry.
    """
    info = conn.get_symbol_info(symbol)
    tick = mt5.symbol_info_tick(symbol)
    price = tick.ask if direction == "BUY" else tick.bid

    sl_dist = atr * config.ATR_SL_MULTIPLIER
    tp_dist = atr * config.ATR_TP_MULTIPLIER

    if direction == "BUY":
        sl_price = price - sl_dist
        tp_price = price + tp_dist
    else:
        sl_price = price + sl_dist
        tp_price = price - tp_dist

    sl_distance_pts = sl_dist / info.point

    return sl_price, tp_price, sl_distance_pts
