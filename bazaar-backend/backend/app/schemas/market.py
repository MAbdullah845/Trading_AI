"""
Pydantic schemas — define the exact JSON shape the API sends/receives.
Matches the "Normalized OHLCV model" from the README:
timestamp, open, high, low, close, volume, symbol
"""

from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class Symbol(BaseModel):
    symbol: str          # e.g. "ENGRO"
    name: Optional[str] = None
    sector: Optional[str] = None


class OHLCVBar(BaseModel):
    symbol: str
    timestamp: date
    open: float
    high: float
    low: float
    close: float
    volume: int


class OHLCVResponse(BaseModel):
    symbol: str
    count: int
    bars: List[OHLCVBar]


class SummaryResponse(BaseModel):
    symbol: str
    last_close: float
    change: float
    change_percent: float
    # Basic indicators — extend as Phase 2 (SMA/EMA/RSI/MACD) gets built out
    sma_20: Optional[float] = None
    rsi_14: Optional[float] = None


class HealthResponse(BaseModel):
    status: str
    data_source: str
