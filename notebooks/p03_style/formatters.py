"""Vietnamese number labels for charts."""

from math import isfinite
from .colour_rules import MISSING_LABEL


def format_number(value: float | None, decimals: int = 0, *, signed: bool = False) -> str:
    if value is None or not isfinite(value):
        return MISSING_LABEL
    rounded = round(value, decimals)
    if rounded == 0:
        rounded = 0
    prefix = "+" if signed and rounded > 0 else ""
    return prefix + f"{rounded:,.{decimals}f}".replace("-", "−")


def _with_unit(value, decimals, unit, *, factor=1, signed=False):
    scaled = None if value is None else value * factor
    number = format_number(scaled, decimals, signed=signed)
    return number if number == MISSING_LABEL else number + unit


def format_usd(value, decimals: int = 1, *, millions: bool = False) -> str:
    factor, unit = (1e-6, " triệu USD") if millions else (1e-9, " tỷ USD")
    return _with_unit(value, decimals, unit, factor=factor)


def format_balance(value, decimals: int = 1) -> str:
    return _with_unit(value, decimals, " tỷ USD", factor=1e-9, signed=True)

def format_vnd(value, *, per: str = "") -> str:
    return _with_unit(value, 0, f" VND/{per}" if per else " VND")

def format_percent(fraction, decimals: int = 1) -> str:
    return _with_unit(fraction, decimals, "%", factor=100)

def format_growth(fraction, decimals: int = 1) -> str:
    return _with_unit(fraction, decimals, "%", factor=100, signed=True)

def format_percentage_points(delta_points, decimals: int = 1) -> str:
    return _with_unit(delta_points, decimals, " pp")


def format_year(value: int | None) -> str:
    return MISSING_LABEL if value is None or not isfinite(value) else f"{value:.0f}"
