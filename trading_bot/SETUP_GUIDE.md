# Setup Guide — AI Trading Bot (MT5 + Exness)

## Prerequisites
- Windows PC (MT5 only works on Windows)
- Python 3.10 or higher installed — download from https://python.org
- MetaTrader 5 installed and logged into your Exness account
- Git installed — download from https://git-scm.com

---

## Step 1 — Get the Code

Open Command Prompt (search "cmd" in Start Menu) and run:

```
git clone https://github.com/Trekkernation/Syed-First-Repo.git
cd Syed-First-Repo\trading_bot
```

---

## Step 2 — Install Python Packages

In the same Command Prompt window:

```
pip install -r requirements.txt
```

---

## Step 3 — Find Your Exact Symbol Names in MT5

1. Open MetaTrader 5
2. Click **View → Market Watch** (or press Ctrl+M)
3. Right-click any symbol → **Symbols**
4. Search for "ETH" and "XAU" — note the exact names shown
   - Common on Exness: `ETHUSDm`, `XAUUSDm` or `ETHUSD`, `XAUUSD`

---

## Step 4 — Edit config.py

Open `config.py` in Notepad and fill in:

```python
MT5_LOGIN    = 12345678          # Your Exness account number
MT5_PASSWORD = "yourpassword"    # Your Exness password
MT5_SERVER   = "Exness-MT5Real"  # Your server name (shown in MT5 login screen)

SYMBOLS = ["ETHUSDm", "XAUUSDm"]  # Use exact names from Step 3
```

**Start with a DEMO account first!** Change your server to the demo server (e.g. `Exness-MT5Trial`).

---

## Step 5 — Run the Bot

Make sure MT5 is open and logged in, then in Command Prompt:

```
python main.py
```

You will see output like:
```
Connected: Your Name | Balance: 10000.0 USD | Server: Exness-MT5Real
[INIT] Training AI models on historical data...
  [ETHUSDm] Model trained | CV accuracy: 64.23% ± 2.1% | Samples: 312
  [XAUUSDm] Model trained | CV accuracy: 67.41% ± 1.8% | Samples: 298
[BOT] Live trading started. Press Ctrl+C to stop.
```

Press **Ctrl+C** at any time to stop the bot safely.

---

## Important Settings to Tune

| Setting | Default | What it does |
|---|---|---|
| `RISK_PERCENT` | 1.0 | % of balance risked per trade. Start at 0.5% |
| `SIGNAL_CONFIDENCE` | 0.62 | Higher = fewer but better trades |
| `MAX_TRADES_PER_DAY` | 8 | Hard limit on daily trades |
| `TIMEFRAME` | M5 | M1 = more trades (riskier), H1 = fewer (safer) |

---

## What to Watch For

- **CV accuracy above 60%** = model is learning real patterns
- **CV accuracy below 55%** = market is choppy, reduce RISK_PERCENT
- Check MT5 trade history to track actual win rate
- Never risk more than 2% per trade

---

## Troubleshooting

**"Symbol not found"** — Check exact symbol name in MT5 Market Watch  
**"MT5 initialize() failed"** — Make sure MT5 is open and logged in  
**"login failed"** — Check your credentials and server name in config.py  
**No trades being placed** — Confidence threshold may be too high; try lowering to 0.58
