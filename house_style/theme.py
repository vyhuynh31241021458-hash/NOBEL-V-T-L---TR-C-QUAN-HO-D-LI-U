"""Matplotlib defaults and axis decoration."""

from matplotlib import rc_context
from matplotlib.ticker import MaxNLocator
from .typography import TYPOGRAPHY, register_fonts

SLIDE_SIZE = (12, 6.75)
BAR_WIDTH = 0.7
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
    "grid.color": "#E5E5E5",
    "grid.linewidth": 0.7,
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
    ax.grid(axis=quantitative_axis)
    axis = ax.xaxis if quantitative_axis == "x" else ax.yaxis
    axis.set_major_locator(MaxNLocator(nbins=6))
    ax.tick_params(length=0)
