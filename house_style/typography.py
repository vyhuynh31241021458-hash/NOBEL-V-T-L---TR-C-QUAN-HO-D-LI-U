"""Modern Editorial font families and text hierarchy."""

from functools import lru_cache
from pathlib import Path

from matplotlib import font_manager

FONT_DIR = Path(__file__).with_name("fonts")
SANS_FONTS = ("Bricolage Grotesque", "DejaVu Sans")
EDITORIAL_FONTS = ("Platypi", "DejaVu Sans")
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
    "text.color": "#222222",
    "figure.titlesize": 18,
    "figure.titleweight": "bold",
    "axes.titlesize": 18,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.labelsize": 11,
    "axes.labelweight": "medium",
    "axes.labelcolor": "#333333",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "legend.fontsize": 10,
}
SUBTITLE = {"fontfamily": EDITORIAL_FONTS, "fontsize": 12, "color": "#555555", "ha": "left"}
ANNOTATION = {"fontfamily": EDITORIAL_FONTS}
DIRECT_LABEL = {"fontfamily": SANS_FONTS, "fontsize": 10, "fontweight": "medium"}
KPI = {"fontfamily": SANS_FONTS, "fontweight": "bold"}
SOURCE = {"fontfamily": SANS_FONTS, "fontsize": 9, "color": "#555555", "ha": "left"}
