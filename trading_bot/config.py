# ============================================================
#  CONFIGURATION - Edit this file before running the bot
# ============================================================

# --- MT5 Login (your Exness credentials) ---
MT5_LOGIN    = 0          # Replace with your Exness account number
MT5_PASSWORD = ""         # Replace with your Exness password
MT5_SERVER   = ""         # Replace with Exness server, e.g. "Exness-MT5Real"

# --- Symbols to trade ---
# Check exact names in MT5: View > Market Watch > right-click > Symbols
SYMBOLS = ["ETHUSD", "XAUUSDm"]

# --- Timeframe ---
# M1=1min, M5=5min, M15=15min, M30=30min, H1=1hour
TIMEFRAME = "M5"

# --- Risk Management ---
RISK_PERCENT       = 1.0   # % of account balance to risk per trade (start low!)
ATR_SL_MULTIPLIER  = 1.5   # Stop loss = 1.5 x ATR
ATR_TP_MULTIPLIER  = 2.5   # Take profit = 2.5 x ATR (always bigger than SL)

# --- AI Signal Settings ---
SIGNAL_CONFIDENCE  = 0.62  # Minimum confidence (0-1) to place a trade
LOOKBACK_BARS      = 500   # Historical bars used to train the AI model
RETRAIN_EVERY      = 50    # Retrain model every N new candles

# --- Safety Limits ---
MAX_OPEN_TRADES    = 2     # Max simultaneous open positions (all symbols combined)
MAX_TRADES_PER_DAY = 8     # Stop trading after this many trades in one day
CHECK_INTERVAL_SEC = 300   # How often to check signals (seconds) - matches timeframe

# --- Bot Identity (do not change) ---
MAGIC_NUMBER = 20240624    # Unique tag for orders placed by this bot
