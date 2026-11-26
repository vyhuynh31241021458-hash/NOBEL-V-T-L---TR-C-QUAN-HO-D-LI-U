"""House style duy nhất của P03.

Gộp các quy tắc màu, font, định dạng số, bố cục và mô phỏng thị giác
từ package p03_style cũ. Các quy tắc và hàm xử lý được giữ nguyên.

Trong notebook: from house_style.house_style import apply_style, PARTNER_COLORS
Từ gốc repository: from notebooks.house_style.house_style import apply_style
Font, ảnh minh chứng và kiểm thử nằm cùng thư mục với file code này.
"""


# ========================================================================
# colour_rules
# ========================================================================
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


# ========================================================================
# typography
# ========================================================================
from functools import lru_cache
from pathlib import Path

from matplotlib import font_manager

FONT_DIR = Path(__file__).with_name("fonts")
SANS_FONTS = ("Bricolage Grotesque", "DejaVu Sans")
EDITORIAL_FONTS = ("Platypi", "DejaVu Sans")
AXIS_TEXT_COLOR = "#444444"
AXIS_TEXT_WEIGHT = "normal"
FONT_FILES = (
    "BricolageGrotesque-Regular.ttf",
    "BricolageGrotesque-Medium.ttf",
    "BricolageGrotesque-Bold.ttf",
    "Platypi.ttf",
)


@lru_cache(maxsize=1)
def register_fonts():
    """Register bundled font files once for the current Python process."""
    for filename in FONT_FILES:
        path = FONT_DIR / filename
        if path.is_file():
            font_manager.fontManager.addfont(path)


TYPOGRAPHY = {
    "font.family": SANS_FONTS,
    "font.size": 10,
    "font.weight": AXIS_TEXT_WEIGHT,
    "text.color": "#222222",
    "figure.titlesize": 18,
    "figure.titleweight": "bold",
    "axes.titlesize": 18,
    "axes.titleweight": "bold",
    "axes.titlelocation": "center",
    "axes.labelsize": 11,
    "axes.labelweight": AXIS_TEXT_WEIGHT,
    "axes.labelcolor": AXIS_TEXT_COLOR,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "xtick.labelcolor": AXIS_TEXT_COLOR,
    "ytick.labelcolor": AXIS_TEXT_COLOR,
    "legend.fontsize": 10,
}
SUBTITLE = {"fontfamily": EDITORIAL_FONTS, "fontsize": 12, "color": "#555555", "ha": "center"}
ANNOTATION = {"fontfamily": EDITORIAL_FONTS, "ha": "center"}
DIRECT_LABEL = {"fontfamily": SANS_FONTS, "fontsize": 10, "fontweight": "medium"}
KPI = {"fontfamily": SANS_FONTS, "fontweight": "bold"}
SOURCE = {"fontfamily": SANS_FONTS, "fontsize": 9, "color": "#555555", "ha": "center"}


# ========================================================================
# sequential
# ========================================================================
from math import isfinite
from matplotlib import colormaps
from matplotlib.colors import Normalize

SEQUENTIAL_CMAP = "Blues"
SEQUENTIAL_COLORS = colormaps[SEQUENTIAL_CMAP].with_extremes(bad=MISSING_COLOR)


def sequential_norm(vmin: float, vmax: float) -> Normalize:
    if not (isfinite(vmin) and isfinite(vmax) and vmin <= vmax):
        raise ValueError("Expected finite limits in increasing order.")
    if vmin == vmax:
        vmax += max(1, abs(vmax) * 0.01)
    return Normalize(vmin=vmin, vmax=vmax)


# ========================================================================
# diverging
# ========================================================================
from math import isfinite

from matplotlib import colormaps
from matplotlib.colors import TwoSlopeNorm

DIVERGING_CMAP = colormaps["RdBu"].resampled(257).with_extremes(bad=MISSING_COLOR)


def diverging_norm(vmin: float, vmax: float) -> TwoSlopeNorm:
    if not (isfinite(vmin) and isfinite(vmax) and vmin <= vmax):
        raise ValueError("Expected finite limits in increasing order.")
    limit = max(abs(vmin), abs(vmax)) or 1
    return TwoSlopeNorm(vmin=-limit, vcenter=0, vmax=limit)


# ========================================================================
# formatters
# ========================================================================
from math import isfinite


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


# ========================================================================
# hs_palette
# ========================================================================
from types import MappingProxyType

_SECTIONS = (
    ("I", "Động vật và sản phẩm động vật", "#4477AA"),
    ("II", "Sản phẩm thực vật", "#228833"),
    ("III", "Dầu, mỡ động thực vật", "#CCBB44"),
    ("IV", "Thực phẩm chế biến, đồ uống", "#EE6677"),
    ("V", "Khoáng sản", "#886644"),
    ("VI", "Hóa chất", "#AA3377"),
    ("VII", "Nhựa và cao su", "#66CCEE"),
    ("VIII", "Da và sản phẩm từ da", "#994455"),
    ("IX", "Gỗ và sản phẩm gỗ", "#667744"),
    ("X", "Bột giấy và giấy", "#88CCAA"),
    ("XI", "Dệt may", "#332288"),
    ("XII", "Giày dép, mũ và phụ kiện", "#DDCC77"),
    ("XIII", "Đá, gốm và thủy tinh", "#6699CC"),
    ("XIV", "Đá quý và kim loại quý", "#CC6677"),
    ("XV", "Kim loại cơ bản", "#555555"),
    ("XVI", "Máy móc, thiết bị điện", "#117733"),
    ("XVII", "Phương tiện vận tải", "#882255"),
    ("XVIII", "Thiết bị quang học, y tế", "#44AA99"),
    ("XIX", "Vũ khí và đạn dược", "#AA4499"),
    ("XX", "Hàng hóa khác", "#999933"),
    ("XXI", "Tác phẩm nghệ thuật, đồ cổ", "#661100"),
    (OTHER, "Khác", OTHER_COLOR),
)
HS_ORDER = tuple(code for code, _, _ in _SECTIONS)
HS_COLORS = MappingProxyType({code: color for code, _, color in _SECTIONS})
HS_LABELS = MappingProxyType({
    code: label if code == OTHER else f"{code} · {label}"
    for code, label, _ in _SECTIONS
})


# ========================================================================
# partner_palette
# ========================================================================
from types import MappingProxyType

COUNTRY_COLORS = MappingProxyType({"VNM": "#A51C30"})

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


# ========================================================================
# trade_flow
# ========================================================================
from types import MappingProxyType

TRADE_FLOW_ORDER = ("Export", "Import")
TRADE_FLOW_COLORS = MappingProxyType({"Export": "#22577A", "Import": "#B86E24"})
TRADE_FLOW_LABELS = MappingProxyType({"Export": "Xuất khẩu", "Import": "Nhập khẩu"})
TRADE_FLOW_LINESTYLES = MappingProxyType({"Export": "solid", "Import": "dashed"})
TRADE_FLOW_MARKERS = MappingProxyType({"Export": "o", "Import": "s"})
TRADE_FLOW_HATCHES = MappingProxyType({"Export": "/", "Import": chr(92)})


# ========================================================================
# highlight
# ========================================================================
from collections.abc import Iterable, Mapping

ACCENT_COLOR = "#0072B2"
CONTEXT_COLOR = OTHER_COLOR
HIGHLIGHT_LINEWIDTH = 3


def highlight_colors(
    labels: Iterable[str], selected: str | Iterable[str], palette: Mapping[str, str] | None = None,
) -> list[str]:
    keys = {selected} if isinstance(selected, str) else set(selected)
    fixed = palette if palette is not None else {}
    return [fixed.get(label, ACCENT_COLOR) if label in keys else CONTEXT_COLOR for label in labels]


# ========================================================================
# accessibility
# ========================================================================
import numpy as np
from colorspacious import cspace_convert

CVD_TYPES = ("protanomaly", "deuteranomaly", "tritanomaly")


def simulate_cvd(rgb, cvd_type: str, severity: int = 100):
    """Transform sRGB values in [0, 1] using the Machado model."""
    if cvd_type not in CVD_TYPES or not 0 <= severity <= 100:
        raise ValueError("Expected a supported deficiency and severity in [0, 100].")
    space = {"name": "sRGB1+CVD", "cvd_type": cvd_type, "severity": severity}
    return np.clip(cspace_convert(rgb, space, "sRGB1"), 0, 1)


def grayscale(rgb):
    """Convert sRGB to gray using relative luminance in linear RGB."""
    linear = cspace_convert(rgb, "sRGB1", "sRGB1-linear")
    luminance = linear @ np.array([0.2126, 0.7152, 0.0722])
    neutral = np.repeat(luminance[..., np.newaxis], 3, axis=-1)
    return np.clip(cspace_convert(neutral, "sRGB1-linear", "sRGB1"), 0, 1)


# ========================================================================
# theme
# ========================================================================
from matplotlib import rc_context
from matplotlib.ticker import MaxNLocator

SLIDE_SIZE = (12, 6.75)
BAR_WIDTH = 0.7
AXIS_LABEL_GAP = 5
ZERO_LINE = {"color": "#777777", "linewidth": 1}
THEME = {
    "figure.figsize": (10, 6),
    "figure.facecolor": "#FFFFFF",
    "axes.facecolor": "#FFFFFF",
    "savefig.facecolor": "#FFFFFF",
    "savefig.dpi": 300,
    "savefig.format": "png",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#AAAAAA",
    "axes.axisbelow": True,
    "axes.grid": False,
    "axes.labelpad": AXIS_LABEL_GAP,
    "xtick.major.pad": AXIS_LABEL_GAP,
    "ytick.major.pad": AXIS_LABEL_GAP,
    "xtick.minor.pad": AXIS_LABEL_GAP,
    "ytick.minor.pad": AXIS_LABEL_GAP,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "xtick.minor.size": 0,
    "ytick.minor.size": 0,
    "legend.frameon": False,
    "lines.linewidth": 2,
    "lines.markersize": 5,
}


def apply_style():
    """Return a context manager that restores the caller's settings on exit."""
    register_fonts()
    return rc_context(TYPOGRAPHY | THEME)


def declutter(ax, quantitative_axis="y"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(False, which="both", axis="both")
    axis = ax.xaxis if quantitative_axis == "x" else ax.yaxis
    axis.set_major_locator(MaxNLocator(nbins=6))


style_context = apply_style

__all__ = ['HS_COLORS', 'HS_ORDER', 'OTHER_COLOR', 'COUNTRY_COLORS', 'PARTNER_COLORS', 'PARTNER_ORDER', 'DIVERGING_CMAP', 'SEQUENTIAL_CMAP', 'diverging_norm', 'sequential_norm', 'format_number', 'format_percent', 'format_percentage_points', 'format_usd', 'format_vnd', 'format_balance', 'format_growth', 'apply_style', 'style_context', 'MISSING_COLOR', 'TRADE_FLOW_COLORS', 'TRADE_FLOW_ORDER', 'format_year', 'OTHER', 'MISSING_LABEL', 'WORLD_CODES', 'ColorRole', 'is_partner_code', 'ordered_present', 'color_for_value', 'FONT_DIR', 'SANS_FONTS', 'EDITORIAL_FONTS', 'AXIS_TEXT_COLOR', 'AXIS_TEXT_WEIGHT', 'FONT_FILES', 'register_fonts', 'TYPOGRAPHY', 'SUBTITLE', 'ANNOTATION', 'DIRECT_LABEL', 'KPI', 'SOURCE', 'SEQUENTIAL_COLORS', 'HS_LABELS', 'PARTNER_MARKERS', 'PARTNER_HATCHES', 'PARTNER_LINESTYLES', 'PARTNER_LABELS', 'partner_group', 'TRADE_FLOW_LABELS', 'TRADE_FLOW_LINESTYLES', 'TRADE_FLOW_MARKERS', 'TRADE_FLOW_HATCHES', 'ACCENT_COLOR', 'CONTEXT_COLOR', 'HIGHLIGHT_LINEWIDTH', 'highlight_colors', 'CVD_TYPES', 'simulate_cvd', 'grayscale', 'SLIDE_SIZE', 'BAR_WIDTH', 'AXIS_LABEL_GAP', 'ZERO_LINE', 'THEME', 'declutter']
