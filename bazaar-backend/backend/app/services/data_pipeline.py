"""
data_pipeline.py — turns raw market_feed.py output into clean,
validated data the API can safely return, and computes basic indicators.
"""

from typing import List, Optional
import datetime
import pandas as pd

from app.data import market_feed
from app.data.market_feed import MarketFeedError
from app.schemas.market import OHLCVBar, Symbol, SummaryResponse


def normalize_symbols(raw: List[dict]) -> List[Symbol]:
    return [Symbol(**row) for row in raw if row.get("symbol")]


def get_symbols() -> List[Symbol]:
    raw = market_feed.get_symbols()
    return normalize_symbols(raw)


def normalize_ohlcv(raw: List[dict]) -> List[OHLCVBar]:
    bars = []
    for row in raw:
        try:
            bars.append(OHLCVBar(**row))
        except Exception:
            # Skip malformed rows rather than failing the whole response
            continue
    return sorted(bars, key=lambda b: b.timestamp)


def get_ohlcv(symbol: str, start: Optional[datetime.date] = None,
              end: Optional[datetime.date] = None) -> List[OHLCVBar]:
    raw = market_feed.get_ohlcv(symbol.upper(), start, end)
    return normalize_ohlcv(raw)


def get_summary(symbol: str) -> SummaryResponse:
    bars = get_ohlcv(symbol)
    if not bars:
        raise MarketFeedError(f"No data available for symbol '{symbol}'")

    closes = pd.Series([b.close for b in bars])
    last_close = float(closes.iloc[-1])
    prev_close = float(closes.iloc[-2]) if len(closes) > 1 else last_close
    change = last_close - prev_close
    change_percent = (change / prev_close * 100) if prev_close else 0.0

    sma_20 = float(closes.tail(20).mean()) if len(closes) >= 20 else None
    rsi_14 = _rsi(closes, period=14) if len(closes) >= 15 else None

    return SummaryResponse(
        symbol=symbol.upper(),
        last_close=round(last_close, 2),
        change=round(change, 2),
        change_percent=round(change_percent, 2),
        sma_20=round(sma_20, 2) if sma_20 is not None else None,
        rsi_14=round(rsi_14, 2) if rsi_14 is not None else None,
    )


def _rsi(closes: pd.Series, period: int = 14) -> float:
    """Standard Wilder RSI calculation."""
    delta = closes.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean().iloc[-1]
    avg_loss = loss.rolling(window=period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
