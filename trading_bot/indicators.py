import pandas as pd
import numpy as np


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    c = df["Close"]
    h = df["High"]
    l = df["Low"]
    v = df["Volume"]

    # EMAs
    df["ema9"]  = c.ewm(span=9,  adjust=False).mean()
    df["ema21"] = c.ewm(span=21, adjust=False).mean()
    df["ema50"] = c.ewm(span=50, adjust=False).mean()

    # EMA slopes (rate of change over 3 bars)
    df["ema9_slope"]  = df["ema9"].diff(3)
    df["ema21_slope"] = df["ema21"].diff(3)

    # RSI (14)
    delta = c.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_loss = loss.ewm(com=13, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD (12, 26, 9)
    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    df["macd"]        = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"]   = df["macd"] - df["macd_signal"]

    # Bollinger Bands (20, 2)
    bb_mid  = c.rolling(20).mean()
    bb_std  = c.rolling(20).std()
    bb_upper = bb_mid + 2 * bb_std
    bb_lower = bb_mid - 2 * bb_std
    bb_range = (bb_upper - bb_lower).replace(0, np.nan)
    df["bb_pct"] = (c - bb_lower) / bb_range   # 0 = at lower band, 1 = at upper band

    # ATR (14) — used for SL/TP sizing
    tr = pd.concat([
        h - l,
        (h - c.shift()).abs(),
        (l - c.shift()).abs()
    ], axis=1).max(axis=1)
    df["atr"] = tr.ewm(com=13, adjust=False).mean()

    # ATR ratio — current ATR vs 50-bar average (detects volatility spikes)
    df["atr_ratio"] = df["atr"] / df["atr"].rolling(50).mean()

    # Volume ratio — current volume vs 20-bar average
    vol_ma = v.rolling(20).mean().replace(0, np.nan)
    df["vol_ratio"] = v / vol_ma

    # Price momentum (close vs close 5 bars ago, normalised by ATR)
    df["momentum"] = (c - c.shift(5)) / df["atr"].replace(0, np.nan)

    return df.dropna()


FEATURE_COLS = [
    "rsi", "macd_hist", "bb_pct",
    "ema9_slope", "ema21_slope",
    "atr_ratio", "vol_ratio", "momentum",
]
