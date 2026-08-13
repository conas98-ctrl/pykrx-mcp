"""Single-session Korean equity data bundle for analysis clients."""

from __future__ import annotations

from typing import Any

from pykrx_mcp.utils.credential_output import safe_dependency_output

from .fundamental import get_market_fundamental_by_date
from .investor import (
    get_market_trading_value_by_investor,
    get_market_trading_volume_by_investor,
)
from .market_cap import get_market_cap_by_date
from .stock_price import get_stock_ohlcv


def get_stock_analysis_bundle(
    ticker: str,
    start_date: str,
    end_date: str,
    adjusted: bool = True,
    fields: list[str] | None = None,
) -> dict[str, Any]:
    """Fetch requested groups sequentially in one authenticated process.

    OHLCV is always fetched first so callers can establish their price
    source-lock before consuming non-price groups.
    """

    requested = set(fields or ("ohlcv", "fundamentals", "market_cap", "investor_flow"))
    with safe_dependency_output():
        result: dict[str, Any] = {
            "ohlcv": get_stock_ohlcv(ticker, start_date, end_date, adjusted)
        }
        if "fundamentals" in requested:
            result["fundamentals"] = get_market_fundamental_by_date(
                ticker, start_date, end_date
            )
        if "market_cap" in requested:
            result["market_cap"] = get_market_cap_by_date(ticker, start_date, end_date)
        if "investor_flow" in requested:
            result["investor_volume"] = get_market_trading_volume_by_investor(
                start_date, end_date, ticker
            )
            result["investor_value"] = get_market_trading_value_by_investor(
                start_date, end_date, ticker
            )
    return result
