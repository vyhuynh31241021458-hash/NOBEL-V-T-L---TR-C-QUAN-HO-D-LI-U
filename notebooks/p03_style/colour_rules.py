"""Shared semantics for categorical, missing and quantitative colors."""

from enum import Enum
from math import isfinite
import re

OTHER = "Other"
OTHER_COLOR = "#BDBDBD"
MISSING_COLOR = "#EEEEEE"
MISSING_LABEL = "N/A"
WORLD_CODES = frozenset({"WLD", "WORLD", "ALL", "TOT", "TOTAL", "XXX"})


class ColorRole(Enum):
    PARTNER = "partner"
    HS_SECTION = "hs_section"
    TRADE_FLOW = "trade_flow"
    MAGNITUDE = "sequential"
    DEVIATION = "diverging"
    HIGHLIGHT = "highlight"
    CONTEXT = "context"
    OTHER = "other"
    MISSING = "missing"


def is_partner_code(code: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]{3}", code)) and code not in WORLD_CODES


def ordered_present(order, categories):
    """Keep the relative order of displayed categories after filtering."""
    present = set(categories)
    return tuple(key for key in order if key in present)


def color_for_value(value, *, cmap, norm):
    if value is None or not isfinite(value):
        return MISSING_COLOR
    return cmap(norm(value))
