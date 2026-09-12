"""
market_feed.py — connects to the PSX data provider.

This is the ONE file that knows how to talk to the outside world for
market data. Everything else in the app (routes, pipeline) just calls
functions here and gets back plain data — it never knows or cares
HOW the data was fetched.

Data source used right now:
    We use the free, unofficial `psx-data-reader` package, which scrapes
    the official PSX website for historical end-of-day OHLCV data. No API
    key is required for this.

    `PSX_API_KEY` / `PSX_API_URL` / `PSX_API_SECRET` are wired in below
    and used automatically IF a real key is ever set in .env — but until
    your team confirms a real paid provider, PSX_API_KEY is empty, so we
    silently fall back to the free scraper. This keeps the switch to a
    real provider a one-line change later, with no code restructuring.
"""

import logging
import datetime
from typing import List, Optional
import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class MarketFeedError(Exception):
    """Raised when the upstream PSX data source fails or returns nothing usable."""


def _using_real_api() -> bool:
    """True only once a real PSX_API_KEY has actually been set in .env."""
    return bool(settings.PSX_API_KEY)


# ---------------------------------------------------------------------------
# Path A: real, key-based PSX API (used automatically once PSX_API_KEY is set)
# ---------------------------------------------------------------------------

def _fetch_symbols_from_api() -> List[dict]:
    url = f"{settings.PSX_API_URL}/symbols"
    headers = {"Authorization": f"Bearer {settings.PSX_API_KEY}"}
    try:
        resp = httpx.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as e:
        logger.error(f"PSX API symbols request failed: {e}")
        raise MarketFeedError(str(e))


def _fetch_ohlcv_from_api(symbol: str, start: datetime.date, end: datetime.date) -> List[dict]:
    url = f"{settings.PSX_API_URL}/ohlcv/{symbol}"
    headers = {"Authorization": f"Bearer {settings.PSX_API_KEY}"}
    params = {"start": start.isoformat(), "end": end.isoformat()}
    try:
        resp = httpx.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as e:
        logger.error(f"PSX API OHLCV request failed for {symbol}: {e}")
        raise MarketFeedError(str(e))


# ---------------------------------------------------------------------------
# Path B: free scraper fallback (psx-data-reader) — active by default
# ---------------------------------------------------------------------------

def _fetch_symbols_from_scraper() -> List[dict]:
    from psx import tickers  # imported lazily so the app can boot without it installed
    try:
        df = tickers()
        return [
            {"symbol": row["symbol"], "name": row.get("name"), "sector": row.get("sectorName")}
            for _, row in df.iterrows()
        ]
    except Exception as e:
        logger.error(f"psx-data-reader tickers() failed: {e}")
        raise MarketFeedError(str(e))


def _fetch_ohlcv_from_scraper(symbol: str, start: datetime.date, end: datetime.date) -> List[dict]:
    from psx import stocks
    try:
        df = stocks(symbol, start=start, end=end)
        if df.empty:
            return []
        df = df.reset_index()
        return [
            {
                "symbol": symbol,
                "timestamp": row["Date"].date() if hasattr(row["Date"], "date") else row["Date"],
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            }
            for _, row in df.iterrows()
        ]
    except Exception as e:
        logger.error(f"psx-data-reader stocks() failed for {symbol}: {e}")
        raise MarketFeedError(str(e))


# ---------------------------------------------------------------------------
# Public functions — this is what the rest of the app calls
# ---------------------------------------------------------------------------

def get_symbols() -> List[dict]:
    """Return every tradeable PSX symbol."""
    if _using_real_api():
        return _fetch_symbols_from_api()
    return _fetch_symbols_from_scraper()


def get_ohlcv(symbol: str, start: Optional[datetime.date] = None,
              end: Optional[datetime.date] = None) -> List[dict]:
    """Return raw OHLCV rows for a single symbol between start and end."""
    end = end or datetime.date.today()
    start = start or (end - datetime.timedelta(days=180))

    if _using_real_api():
        return _fetch_ohlcv_from_api(symbol, start, end)
    return _fetch_ohlcv_from_scraper(symbol, start, end)


def data_source_name() -> str:
    return "psx-real-api" if _using_real_api() else "psx-data-reader (free scraper)"
