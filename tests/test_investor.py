"""Tests for investor trading data tools."""

from unittest.mock import patch

import pandas as pd

from pykrx_mcp.tools.investor import (
    get_market_net_purchases_of_equities,
    get_market_trading_value_by_investor,
    get_market_trading_volume_by_investor,
)


def test_get_market_trading_volume_by_investor_stock():
    """Test getting investor trading volume for a stock."""
    result = get_market_trading_volume_by_investor("20240101", "20240105", "005930")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["ticker"] == "005930"


def test_get_market_trading_volume_by_investor_market():
    """Test getting investor trading volume for a market."""
    result = get_market_trading_volume_by_investor("20240101", "20240105", "KOSPI")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["ticker"] == "KOSPI"


def test_get_market_trading_value_by_investor():
    """Test getting investor trading value."""
    result = get_market_trading_value_by_investor("20240101", "20240105", "KOSDAQ")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)


@patch("pykrx_mcp.tools.investor.stock")
def test_investor_volume_aggregates_duplicate_investor_labels(mock_stock):
    mock_stock.get_market_trading_volume_by_investor.return_value = pd.DataFrame(
        {
            "매도": [10, 20, 7],
            "매수": [15, 25, 8],
            "순매수": [5, 5, 1],
        },
        index=["외국인", "외국인", "개인"],
    )

    result = get_market_trading_volume_by_investor(
        "20240101", "20240105", "005930"
    )

    assert result["data"] == {
        "외국인": {"매도": 30, "매수": 40, "순매수": 10},
        "개인": {"매도": 7, "매수": 8, "순매수": 1},
    }


@patch("pykrx_mcp.tools.investor.stock")
def test_investor_value_aggregates_duplicate_investor_labels(mock_stock):
    mock_stock.get_market_trading_value_by_investor.return_value = pd.DataFrame(
        {
            "매도": [100, 200, 70],
            "매수": [150, 250, 80],
            "순매수": [50, 50, 10],
        },
        index=["기관합계", "기관합계", "개인"],
    )

    result = get_market_trading_value_by_investor(
        "20240101", "20240105", "005930"
    )

    assert result["data"] == {
        "기관합계": {"매도": 300, "매수": 400, "순매수": 100},
        "개인": {"매도": 70, "매수": 80, "순매수": 10},
    }


def test_get_market_net_purchases_of_equities():
    """Test getting net purchases by investor type."""
    result = get_market_net_purchases_of_equities(
        "20240101", "20240105", "KOSPI", "외국인"
    )

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["market"] == "KOSPI"
        assert result["investor"] == "외국인"


def test_get_market_net_purchases_invalid_market():
    """Test error handling for invalid market."""
    result = get_market_net_purchases_of_equities(
        "20240101", "20240105", "INVALID", "외국인"
    )

    assert "error" in result
    assert "Invalid market" in result["error"]


def test_get_market_net_purchases_invalid_investor():
    """Test error handling for invalid investor type."""
    result = get_market_net_purchases_of_equities(
        "20240101", "20240105", "KOSPI", "INVALID"
    )

    assert "error" in result
    assert "Invalid investor" in result["error"]
