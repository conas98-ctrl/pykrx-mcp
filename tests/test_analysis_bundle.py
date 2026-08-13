"""Single-session analysis bundle tests."""

from unittest.mock import patch

from pykrx_mcp.tools.analysis_bundle import get_stock_analysis_bundle


@patch("pykrx_mcp.tools.analysis_bundle.get_market_trading_value_by_investor")
@patch("pykrx_mcp.tools.analysis_bundle.get_market_trading_volume_by_investor")
@patch("pykrx_mcp.tools.analysis_bundle.get_market_cap_by_date")
@patch("pykrx_mcp.tools.analysis_bundle.get_market_fundamental_by_date")
@patch("pykrx_mcp.tools.analysis_bundle.get_stock_ohlcv")
def test_bundle_fetches_ohlcv_first_then_non_price_groups(
    ohlcv, fundamentals, market_cap, investor_volume, investor_value
):
    order = []
    for mock, name in (
        (ohlcv, "ohlcv"),
        (fundamentals, "fundamentals"),
        (market_cap, "market_cap"),
        (investor_volume, "investor_volume"),
        (investor_value, "investor_value"),
    ):
        mock.side_effect = lambda *args, _name=name, **kwargs: order.append(_name) or {"data": _name}

    result = get_stock_analysis_bundle("005930", "20250101", "20251231")

    assert order == [
        "ohlcv", "fundamentals", "market_cap", "investor_volume", "investor_value"
    ]
    assert list(result) == order
