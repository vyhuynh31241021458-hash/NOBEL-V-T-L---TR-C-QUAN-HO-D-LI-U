"""Matplotlib defaults and axis decoration."""

from matplotlib import rc_context
from matplotlib.ticker import MaxNLocator
from .typography import TYPOGRAPHY, register_fonts

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
