"""Reusable Matplotlib conventions for P03."""

from .colour_rules import MISSING_COLOR, OTHER_COLOR
from .diverging import DIVERGING_CMAP, diverging_norm
from .formatters import (
    format_balance, format_growth, format_number, format_percent,
    format_percentage_points, format_usd, format_vnd, format_year,
)
from .hs_palette import HS_COLORS, HS_ORDER
from .partner_palette import PARTNER_COLORS, PARTNER_ORDER
from .sequential import SEQUENTIAL_CMAP, sequential_norm
from .theme import apply_style
from .trade_flow import TRADE_FLOW_COLORS, TRADE_FLOW_ORDER

style_context = apply_style

__all__ = [
    "HS_COLORS", "HS_ORDER", "OTHER_COLOR", "PARTNER_COLORS", "PARTNER_ORDER",
    "DIVERGING_CMAP", "SEQUENTIAL_CMAP", "diverging_norm", "sequential_norm",
    "format_number", "format_percent", "format_percentage_points", "format_usd",
    "format_vnd", "format_balance", "format_growth", "apply_style", "style_context",
    "MISSING_COLOR", "TRADE_FLOW_COLORS", "TRADE_FLOW_ORDER", "format_year",
]
