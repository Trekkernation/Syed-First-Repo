"""
AI Trading Bot — ETHUSD & XAUUSDm on Exness MT5
Run this script on the Windows PC where MT5 is installed.
"""

import time
import traceback
from datetime import datetime, date

import mt5_connector as conn
import risk_manager as risk
from ai_model import TradingModel
from indicators import add_indicators
import config


def get_current_atr(symbol: str) -> float:
    df = conn.get_ohlcv(symbol, bars=100)
    df = add_indicators(df)
    return float(df["atr"].iloc[-1])


def already_in_trade(symbol: str) -> bool:
    trades = conn.get_open_trades()
    return any(t.symbol == symbol for t in trades)


def run():
    print("=" * 60)
    print("  AI Trading Bot Starting")
    print(f"  Symbols : {config.SYMBOLS}")
    print(f"  Timeframe: {config.TIMEFRAME}")
    print(f"  Risk/trade: {config.RISK_PERCENT}%")
    print("=" * 60)

    conn.connect()

    # Initialise one AI model per symbol
    models = {sym: TradingModel(sym) for sym in config.SYMBOLS}

    # Initial training
    print("\n[INIT] Training AI models on historical data...")
    for sym, model in models.items():
        df = conn.get_ohlcv(sym, bars=config.LOOKBACK_BARS)
        model.train(df)

    trades_today = 0
    last_trade_date = date.today()

    print("\n[BOT] Live trading started. Press Ctrl+C to stop.\n")

    while True:
        try:
            now = datetime.now()

            # Reset daily trade counter at midnight
            if date.today() != last_trade_date:
                trades_today = 0
                last_trade_date = date.today()
                print(f"\n[{now:%H:%M:%S}] New trading day — counter reset.")

            open_trades = conn.get_open_trades()
            total_open  = len(open_trades)

            print(f"[{now:%H:%M:%S}] Checking signals | Open: {total_open}/{config.MAX_OPEN_TRADES} | Today: {trades_today}/{config.MAX_TRADES_PER_DAY}")

            for sym in config.SYMBOLS:
                if trades_today >= config.MAX_TRADES_PER_DAY:
                    print(f"  [{sym}] Daily trade limit reached. Skipping.")
                    continue

                if total_open >= config.MAX_OPEN_TRADES:
                    print(f"  [{sym}] Max open trades reached. Skipping.")
                    break

                if already_in_trade(sym):
                    print(f"  [{sym}] Already in a trade. Skipping.")
                    continue

                df = conn.get_ohlcv(sym, bars=config.LOOKBACK_BARS)
                model = models[sym]

                # Periodic retraining
                if model.should_retrain():
                    print(f"  [{sym}] Retraining model...")
                    model.train(df)

                signal, confidence = model.predict(df)
                direction = {1: "BUY", -1: "SELL", 0: "HOLD"}.get(signal, "HOLD")

                print(f"  [{sym}] Signal: {direction} | Confidence: {confidence:.2%}")

                if signal == 0:
                    continue

                # Calculate SL/TP and lot size
                atr = get_current_atr(sym)
                sl_price, tp_price, sl_pts = risk.calculate_sl_tp(sym, direction, atr)
                lot = risk.calculate_lot(sym, sl_pts)

                print(f"  [{sym}] Attempting {direction} | Lot: {lot} | SL: {sl_price:.5f} | TP: {tp_price:.5f}")

                success = conn.place_order(sym, direction, lot, sl_price, tp_price)
                if success:
                    trades_today += 1
                    total_open   += 1

        except KeyboardInterrupt:
            print("\n[BOT] Stopped by user.")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            traceback.print_exc()
            print("  Continuing in 60 seconds...")
            time.sleep(60)
            continue

        print(f"  Next check in {config.CHECK_INTERVAL_SEC // 60} minutes...\n")
        time.sleep(config.CHECK_INTERVAL_SEC)

    conn.disconnect()
    print("[BOT] Disconnected from MT5. Goodbye.")


if __name__ == "__main__":
    run()
