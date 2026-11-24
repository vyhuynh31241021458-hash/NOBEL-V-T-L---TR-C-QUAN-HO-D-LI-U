"""Fixed partner ordering and visual channels for BACI 2005–2024."""

from types import MappingProxyType
from .colour_rules import OTHER, OTHER_COLOR, is_partner_code

PARTNER_ORDER = ("CHN", "USA", "KOR", "JPN", "THA", OTHER)
PARTNER_COLORS = MappingProxyType(dict(zip(
    PARTNER_ORDER, ("#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", OTHER_COLOR),
)))
PARTNER_MARKERS = MappingProxyType(dict(zip(PARTNER_ORDER, ("o", "s", "^", "D", "P", "x"))))
PARTNER_HATCHES = MappingProxyType(dict(zip(PARTNER_ORDER, ("/", chr(92), "x", ".", "+", ""))))
PARTNER_LINESTYLES = MappingProxyType(dict(zip(
    PARTNER_ORDER, ("solid", "dashed", "dashdot", "dotted", (0, (8, 3)), (0, (2, 2))),
)))
PARTNER_LABELS = MappingProxyType(dict(zip(
    PARTNER_ORDER, ("Trung Quốc", "Hoa Kỳ", "Hàn Quốc", "Nhật Bản", "Thái Lan", "Khác"),
)))


def partner_group(iso3: str | None) -> str | None:
    """Return a fixed group, or None for missing/aggregate codes."""
    key = iso3.strip().upper() if iso3 else ""
    if key == OTHER.upper():
        return OTHER
    if not is_partner_code(key):
        return None
    return key if key in PARTNER_COLORS else OTHER
