"""Modern Editorial font families and text hierarchy."""

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
