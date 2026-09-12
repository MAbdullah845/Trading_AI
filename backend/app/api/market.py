"""
API routes for market data.
Matches the table in README.md exactly:

GET /api/market/symbols
GET /api/market/ohlcv/{symbol}
GET /api/market/ohlcv/{symbol}/summary
GET /api/market/health
"""

import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.schemas.market import Symbol, OHLCVResponse, SummaryResponse, HealthResponse
from app.services import data_pipeline
from app.data.market_feed import MarketFeedError, data_source_name

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/symbols", response_model=List[Symbol])
def list_symbols():
    """List all PSX symbols."""
    try:
        return data_pipeline.get_symbols()
    except MarketFeedError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch symbols: {e}")


@router.get("/ohlcv/{symbol}", response_model=OHLCVResponse)
def get_ohlcv(
    symbol: str,
    start: Optional[datetime.date] = Query(None, description="YYYY-MM-DD"),
    end: Optional[datetime.date] = Query(None, description="YYYY-MM-DD"),
):
    """Get OHLCV bars for a symbol, optionally bounded by start/end dates."""
    try:
        bars = data_pipeline.get_ohlcv(symbol, start, end)
    except MarketFeedError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch data for {symbol}: {e}")

    if not bars:
        raise HTTPException(status_code=404, detail=f"No data found for symbol '{symbol}'")

    return OHLCVResponse(symbol=symbol.upper(), count=len(bars), bars=bars)


@router.get("/ohlcv/{symbol}/summary", response_model=SummaryResponse)
def get_summary(symbol: str):
    """Get last close, day change, and basic indicators for a symbol."""
    try:
        return data_pipeline.get_summary(symbol)
    except MarketFeedError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/health", response_model=HealthResponse)
def health():
    """Simple health check — also reports which data source is active."""
    return HealthResponse(status="ok", data_source=data_source_name())
