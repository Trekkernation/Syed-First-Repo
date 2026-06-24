# CLAUDE.md

This file is a running log of context, decisions, and notes for AI assistants (Claude) working in this repository. Update it after any meaningful discussion or decision.

## Repository

- **Owner:** Trekkernation (Syed)
- **Repo:** trekkernation/syed-first-repo
- **Purpose:** Personal learning/sandbox repository

## Notes & Decisions

_Add entries here as discussions happen. Most recent at the top._

### 2026-06-24 (update 2)
- Built an AI trading bot in `trading_bot/` targeting MT5 via Exness broker.
- Symbols: ETHUSD and XAUUSDm. Timeframe: M5. Risk: 1% per trade.
- Stack: Python + MetaTrader5 library + scikit-learn RandomForest + pandas.
- Bot architecture: `config.py` → `mt5_connector.py` → `indicators.py` → `ai_model.py` → `risk_manager.py` → `main.py`.
- Signal generation: 8 technical features (RSI, MACD, Bollinger %B, EMA slopes, ATR ratio, volume ratio, momentum) fed into a RandomForest classifier trained on rolling historical data.
- Trades only when confidence ≥ 62%. SL = 1.5×ATR, TP = 2.5×ATR (positive R:R).
- Safety limits: max 2 open trades, max 8 trades/day. Retrains every 50 bars.
- Syed runs this on his Windows PC where MT5 is installed (cloud env can't reach MT5 directly).
- SETUP_GUIDE.md has step-by-step instructions for a non-developer to get running.
- Next steps: test on demo account first, tune SIGNAL_CONFIDENCE and RISK_PERCENT based on results.

### 2026-06-24 (initial)
- Repository is essentially empty — just an `index.html` (a basic GitHub Pages hello-world page) and an empty `helloagain` file from an old commit.
- CLAUDE.md created as a living document to accumulate context and notes over time. No complex structure needed yet.
- Development branch for Claude sessions: `claude/claude-md-docs-khehja`
