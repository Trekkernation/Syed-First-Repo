import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from indicators import add_indicators, FEATURE_COLS
import config


class TradingModel:
    def __init__(self, symbol: str):
        self.symbol    = symbol
        self.model     = RandomForestClassifier(
            n_estimators=200,
            max_depth=6,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )
        self.scaler    = StandardScaler()
        self.trained   = False
        self.bars_since_retrain = 0

    def _make_labels(self, df: pd.DataFrame, forward_bars: int = 3) -> pd.Series:
        """
        Label each bar:
          1 (BUY)  if future close > current close + 0.3 * ATR
         -1 (SELL) if future close < current close - 0.3 * ATR
          0 (HOLD) otherwise
        """
        threshold = 0.3 * df["atr"]
        future_close = df["Close"].shift(-forward_bars)
        diff = future_close - df["Close"]

        labels = pd.Series(0, index=df.index)
        labels[diff >  threshold] =  1
        labels[diff < -threshold] = -1
        return labels

    def train(self, df: pd.DataFrame):
        df = add_indicators(df.copy())
        labels = self._make_labels(df).iloc[:-3]  # drop last 3 (no future data)
        features = df[FEATURE_COLS].iloc[:-3]

        # Drop neutral bars to sharpen the model (keep BUY and SELL only)
        mask = labels != 0
        X = features[mask]
        y = labels[mask]

        if len(X) < 60:
            print(f"  [{self.symbol}] Not enough data to train ({len(X)} samples). Skipping.")
            return

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.trained = True
        self.bars_since_retrain = 0

        scores = cross_val_score(self.model, X_scaled, y, cv=3, scoring="accuracy")
        print(f"  [{self.symbol}] Model trained | CV accuracy: {scores.mean():.2%} ± {scores.std():.2%} | Samples: {len(X)}")

    def predict(self, df: pd.DataFrame) -> tuple[int, float]:
        """
        Returns (signal, confidence):
          signal: 1=BUY, -1=SELL, 0=no trade
          confidence: 0.0 – 1.0
        """
        if not self.trained:
            return 0, 0.0

        df = add_indicators(df.copy())
        if df.empty:
            return 0, 0.0

        last_row = df[FEATURE_COLS].iloc[[-1]]
        X_scaled = self.scaler.transform(last_row)

        proba = self.model.predict_proba(X_scaled)[0]
        classes = list(self.model.classes_)

        max_idx = int(np.argmax(proba))
        confidence = float(proba[max_idx])
        signal = int(classes[max_idx])

        if confidence < config.SIGNAL_CONFIDENCE:
            return 0, confidence

        return signal, confidence

    def should_retrain(self) -> bool:
        self.bars_since_retrain += 1
        return self.bars_since_retrain >= config.RETRAIN_EVERY
